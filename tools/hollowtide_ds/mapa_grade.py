#!/usr/bin/env python3
"""Gerador v2 de blocos de mapa: o setor desenhado numa grade de texto (CP-DS-03B).

Arquivo do setor (texto, revisavel no repositorio):
  [doadores]  numeros dos blocos de onde vem os materiais (mesma area), ex.: 57 59
  [tiles]     32 linhas de 32 letras:
                .  grama            =  caminho de terra     e  mato alto (encontros)    f g h  flores (3 tipos)
                c  cerca (bloqueada; trechos horizontais e verticais como os de New Bark)
                B  construcao (bloqueado; o modelo vem de [objetos])   D  porta (bloqueada com comportamento 0x69, como no HGSS)
                ~  agua (lagoa)     T  arvore (floresta)    #  bloqueado (beira de penhasco, lados de rampa)
                S  objeto (o tile fica bloqueado; o modelo vem de [objetos])
                v  ressalto (pulo so para o sul, 0x803B; beirada baixa desenhada na borda sul)
                R  rocha solta (pedra na areia ou no mar; bloqueada, topo e faces de rocha, 1 tile acima do chao)
  [alturas]   32 linhas de 32 caracteres: altura do chao em tiles (0-9); r = rampa (sobe para o vizinho mais alto
              no eixo norte-sul)
  [objetos]   linhas "modelo x z [dy]" (construcoes da lista da area; x e z em tiles, podem ter fracao; altura = a do
              tile + dy)
Do desenho saem: chao por material (retangulos de ate 4x4 tiles), faces de penhasco em todo desnivel entre tiles
que nao sao rampa, margem da agua, rampas inclinadas, fileiras de arvores (como as do HGSS), alturas BDHC (placas
planas e rampas) e colisao (bloqueado, mato alto 0x02, agua 0x15, livre).
Uso como modulo: gerar(bloco, blocos, arquivo) ; linha de comando: mapa_grade.py ARQUIVO (mostra a colisao)
"""
import math, os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
from land_data import Land
from nsbmd import encode_dl, compose
import bdhc

T = 1024
GW = GH = 32                           # tamanho da grade carregada (um bloco = 32x32; desenho global = varios blocos)


def set_size(g):
    global GW, GH
    GH, GW = len(g["tiles"]), len(g["tiles"][0])
UP = 511 << 10
MAXQ = 4
FLOOR = {"R": "wall01_g", ".": "grass01", "=": "road01", "e": "grass01", "f": "grass01", "g": "grass01", "h": "grass01", "c": "grass01",
         "T": "grass01", "#": "grass01", "S": "grass01", "~": None, "B": "grass01", "D": "road01", "v": "grass01"}
PERM = {"R": 0x8000, "T": 0x8000, "#": 0x8000, "S": 0x8000, "c": 0x8000, "B": 0x8000, "D": 0x8069, "e": 0x0002, "~": 0x0015, "v": 0x803B}
ORDER = ["grass01", "road01", "road01_r", "egrass", "wall01_g", "sea_un", "sea_on", "pond_line", "sea_line02", "flower01", "flower02", "flower03", "fence_b", "tree01_un", "tree01_re", "tree01"]


def ccw(q):
    """Mesmo sentido dos quads do HGSS (area com sinal negativa no plano x-z)."""
    a = sum(q[i][0] * q[(i + 1) % 4][2] - q[(i + 1) % 4][0] * q[i][2] for i in range(4))
    return q if a < 0 else q[::-1]


def nrm(x, y, z):
    q = lambda v: int(round(max(-1, min(0.998, v)) * 512)) & 0x3FF
    return q(x) | (q(y) << 10) | (q(z) << 20)


# margem de lagoa copiada de New Bark (bloco 0): perfis (d = distancia da borda, + para a terra; y com chao 1,0; v)
# (perfis reduzidos aos pontos que dao a forma: 3 na margem, 2 na espuma; com os 5+3 pontos de New Bark, um canal
#  longo passava de 4 mil vertices num bloco, contra 1,2-2,3 mil nos blocos do HGSS)
POND_LINE = [(-0.29, 0.52, 250), (-0.11, 0.96, 89), (0.22, 1.13, 5)]
SEA_LINE = [(-0.55, 0.40, 1024), (-0.16, 0.91, 640)]


def load(path):
    sec, out = None, {"doadores": [], "tiles": [], "alturas": [], "objetos": [], "tamanho": (32, 32)}
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("[") and line.endswith("]"):
            sec = line[1:-1]; continue
        if not line.strip() or line.lstrip().startswith(";"):
            continue
        if sec == "tamanho":
            out["tamanho"] = tuple(int(v) for v in line.split()); continue
        if sec == "doadores":
            out["doadores"] += [int(v) for v in line.split()]
        elif sec in ("tiles", "alturas"):
            assert len(line) == out["tamanho"][0], f"{sec}: linha com {len(line)} colunas: {line!r}"
            out[sec].append(line)
        elif sec == "objetos":
            f = line.split()                             # modelo x z [dy]: x, z em tiles (podem ter fracao)
            out["objetos"].append((int(f[0]), float(f[1]), float(f[2]), float(f[3]) if len(f) > 3 else 0.0))
    assert len(out["tiles"]) == out["tamanho"][1] and len(out["alturas"]) == out["tamanho"][1], "numero de linhas da grade"
    set_size(out)
    return out


def heights(g):
    """Altura no centro de cada tile; rampas interpoladas entre os vizinhos norte e sul fora da rampa."""
    H = [[None] * GW for _ in range(GH)]
    for z in range(GH):
        for x in range(GW):
            c = g["alturas"][z][x]
            if c != "r":
                H[z][x] = float(c)
    ramps = []
    for x in range(GW):
        z = 0
        while z < GH:
            if g["alturas"][z][x] == "r":
                z0 = z
                while z < GH and g["alturas"][z][x] == "r":
                    z += 1
                hn = H[z0 - 1][x] if z0 > 0 else None
                hs = H[z][x] if z < GH else None
                for k in range(z0, z):
                    t = (k - z0 + 0.5) / (z - z0)
                    H[k][x] = hn + (hs - hn) * t
                ramps.append((x, z0, z, hn, hs))
            else:
                z += 1
    return H, ramps


def rects(cells, maxq=None):
    """Agrupa um conjunto de tiles (x, z) em retangulos de ate MAXQ x MAXQ (guloso, linha a linha)."""
    MAXQ = maxq or globals()["MAXQ"]
    left, out = set(cells), []
    for z in range(GH):
        for x in range(GW):
            if (x, z) not in left:
                continue
            w = 1
            while w < MAXQ and (x + w, z) in left and (x + w) % 32:
                w += 1
            h = 1
            while h < MAXQ and all((x + i, z + h) in left for i in range(w)) and (z + h) % 32:
                h += 1
            for i in range(w):
                for j in range(h):
                    left.discard((x + i, z + j))
            out.append((x, z, x + w, z + h))
    return out


class Mesh:
    def __init__(self):
        self.quads = {}

    def quad(self, mat, verts, n=UP):
        self.quads.setdefault(mat, []).append((verts, n))

    def flat(self, mat, r, h, uv0=(0, 0)):
        x0, z0, x1, z1 = r
        u = lambda x: int(uv0[0] + 256 * (x - 16)); v = lambda z: int(uv0[1] + 256 * (z - 16))
        self.quad(mat, [(x0, h, z1, u(x0), v(z1)), (x1, h, z1, u(x1), v(z1)), (x1, h, z0, u(x1), v(z0)), (x0, h, z0, u(x0), v(z0))])

    def dl(self, mat):
        cmds, last, prev = [(0x40, [1])], None, None
        for verts, n in self.quads[mat]:
            for x, y, z, u, v in verts:
                u, v = int(round(u)), int(round(v))
                cmds.append((0x22, [(u & 0xFFFF) | ((v & 0xFFFF) << 16)]))
                if n != last:
                    cmds.append((0x21, [n])); last = n
                X, Y, Z = int(round((x - 16) * T)), int(round(y * T)), int(round((z - 16) * T))
                p16 = lambda a, b: (a & 0xFFFF) | ((b & 0xFFFF) << 16)
                if prev and prev[1] == Y:
                    cmds.append((0x26, [p16(X, Z)]))
                elif prev and prev[2] == Z:
                    cmds.append((0x25, [p16(X, Y)]))
                elif prev and prev[0] == X:
                    cmds.append((0x27, [p16(Y, Z)]))
                else:
                    cmds.append((0x23, [p16(X, Y), Z & 0xFFFF]))
                prev = (X, Y, Z)
        cmds.append((0x41, []))
        return encode_dl(cmds)


def build_mesh(g):
    tiles = g["tiles"]
    H, ramps = heights(g)
    ramp_cells = {(x, z) for x, z0, z1, _, _ in ramps for z in range(z0, z1)}
    m = Mesh()
    # chao plano: por (material, altura), sem rampas
    groups = {}

    # Chao dos bloqueados (construcao, porta, objeto, rocha do penhasco): cada grupo ligado deles pega o chao da
    # maioria dos vizinhos andaveis em volta do grupo. Na areia ou na calcada, a parte da planta do GBA que o modelo
    # nao cobre aparecia como um quadrado de grama (construcoes da praia, lampioes; auditoria de 25/11).
    piso_bloq = {}
    for z0 in range(GH):
        for x0 in range(GW):
            if tiles[z0][x0] not in "BSD#" or (x0, z0) in piso_bloq:
                continue
            comp, pilha, viz = [], [(x0, z0)], []
            piso_bloq[(x0, z0)] = None
            while pilha:
                x, z = pilha.pop(); comp.append((x, z))
                for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, zz = x + dx, z + dz
                    if not (0 <= xx < GW and 0 <= zz < GH):
                        continue
                    c2 = tiles[zz][xx]
                    if c2 in "BSD#":
                        if (xx, zz) not in piso_bloq:
                            piso_bloq[(xx, zz)] = None; pilha.append((xx, zz))
                    elif c2 not in "T~R":
                        viz.append(c2)
            mat = "road01" if viz and sum(v == "=" for v in viz) * 2 > len(viz) else None
            for k in comp:
                piso_bloq[k] = mat

    def piso(x, z):
        return piso_bloq.get((x, z)) or FLOOR[tiles[z][x]]
    for z in range(GH):
        for x in range(GW):
            if (x, z) in ramp_cells:
                continue
            c = tiles[z][x]
            mat = piso(x, z)
            if mat:
                groups.setdefault((mat, H[z][x]), set()).add((x, z))
    for (mat, h), cells in sorted(groups.items()):
        for r in rects(cells):
            m.flat(mat, r, h + (0.01 if mat == "road01" else 0))
    # forro de grama 0,03 tile abaixo do chao, em retangulos grandes: onde dois quads do chao se encontram com
    # vertices em posicoes diferentes (junta em T), o DS deixa escapar pixels do fundo preto; com o forro, o que
    # aparece na fresta e grama (os "pontinhos/linhas pretas" entre tiles da auditoria de 25/11)
    under = {}
    for (mat, h), cells in groups.items():
        under.setdefault(h, set()).update(cells)
    for h, cells in sorted(under.items()):
        for r in rects(cells, 8):
            m.flat("grass01", r, h - 0.03)
    # agua: duas camadas meio tile abaixo do chao, como no HGSS
    water = {(x, z) for z in range(GH) for x in range(GW) if tiles[z][x] == "~"}
    for hz in sorted({H[z][x] for x, z in water}):
        cells = {(x, z) for x, z in water if H[z][x] == hz}
        for r in rects(cells):
            m.flat("sea_un", r, hz - 0.56); m.flat("sea_on", r, hz - 0.5)
    # rampas: superficie inclinada (terra), um quad por coluna
    for x, z0, z1, hn, hs in ramps:
        k = (hs - hn) / (z1 - z0)
        n = nrm(0, 1 / math.hypot(1, k), -k / math.hypot(1, k))
        m.quad("road01", [(x, hs + 0.01, z1, 256 * (x - 16), 256 * (z1 - 16)), (x + 1, hs + 0.01, z1, 256 * (x - 15), 256 * (z1 - 16)),
                          (x + 1, hn + 0.01, z0, 256 * (x - 15), 256 * (z0 - 16)), (x, hn + 0.01, z0, 256 * (x - 16), 256 * (z0 - 16))], n)
    # margem: faixas pond_line e sea_line02 ao longo da aresta agua/terra, com a face virada para a agua e para cima
    bank_edges = []

    def bank(x, z, dx, dz, water_first, h):
        """Guarda a aresta agua/terra; as arestas retas seguidas viram uma faixa so (ate MAXQ tiles, sem cruzar divisa
        de bloco) em emit_banks()."""
        if dz:
            bank_edges.append(("h", z + 1, x, 1 if water_first else -1, h))
        else:
            bank_edges.append(("v", x + 1, z, 1 if water_first else -1, h))

    def emit_banks():
        runs = []
        for e in sorted(bank_edges):
            o, c, a, land, h = e
            if runs and runs[-1][:2] == (o, c) and runs[-1][3] == land and runs[-1][4] == h and runs[-1][2][1] == a \
                    and runs[-1][2][1] - runs[-1][2][0] < MAXQ and a % 32:
                runs[-1][2][1] = a + 1
            else:
                runs.append([o, c, [a, a + 1], land, h])
        for o, c, (a0, a1), land, h in runs:
            pt = (lambda t, d, y: (t, y, c + land * d)) if o == "h" else (lambda t, d, y: (c + land * d, y, t))
            toward_water = (0, 0, -land) if o == "h" else (-land, 0, 0)
            for prof, mat in ((POND_LINE, "pond_line"), (SEA_LINE, "sea_line02")):
                for (d0, y0, v0), (d1, y1, v1) in zip(prof, prof[1:]):
                    A, B = pt(a0, d0, y0 - 1 + h), pt(a1, d0, y0 - 1 + h)
                    C, D = pt(a1, d1, y1 - 1 + h), pt(a0, d1, y1 - 1 + h)
                    q = [(*A, 256 * a0, v0), (*B, 256 * a1, v0), (*C, 256 * a1, v1), (*D, 256 * a0, v1)]
                    u = [B[i] - A[i] for i in range(3)]; w = [D[i] - A[i] for i in range(3)]
                    n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
                    if n[0] * toward_water[0] + n[1] + n[2] * toward_water[2] < 0:
                        q = q[::-1]
                    m.quad(mat, q, nrm(toward_water[0] * 0.5, 0.85, toward_water[2] * 0.5))

    # cantos convexos da agua (terra nos dois lados perpendiculares): o mesmo perfil girado um quarto de volta em torno
    # da quina, em 3 segmentos, fechando o corte entre as duas faixas retas
    def is_w(xx, zz):
        return 0 <= xx < GW and 0 <= zz < GH and tiles[zz][xx] == "~"
    for z in range(GH):
        for x in range(GW):
            if not is_w(x, z):
                continue
            for sx, sz in ((1, -1), (1, 1), (-1, -1), (-1, 1)):
                if is_w(x + sx, z) or is_w(x, z + sz):
                    continue                             # nao e canto convexo
                cx, cz = x + (1 if sx > 0 else 0), z + (1 if sz > 0 else 0)
                h = H[z][x]
                a0 = math.atan2(sz, 0)                   # direcao da terra no lado de z
                a1 = math.atan2(0, sx)                   # direcao da terra no lado de x
                if abs(a1 - a0) > math.pi:
                    a1 += 2 * math.pi if a1 < a0 else -2 * math.pi
                steps = [a0, a1]                     # canto em 1 segmento (chanfro): orcamento de vertices
                for prof, mat in ((POND_LINE, "pond_line"), (SEA_LINE, "sea_line02")):
                    for (d0, y0, v0), (d1, y1, v1) in zip(prof, prof[1:]):
                        for t0, t1 in zip(steps, steps[1:]):
                            P = lambda t, d, y: (cx + d * math.cos(t), y - 1 + h, cz + d * math.sin(t))
                            A, B, C, D = P(t0, d0, y0), P(t1, d0, y0), P(t1, d1, y1), P(t0, d1, y1)
                            uu0, uu1 = 256 * (t0 - a0) * 0.6, 256 * (t1 - a0) * 0.6
                            q = [(*A, uu0, v0), (*B, uu1, v0), (*C, uu1, v1), (*D, uu0, v1)]
                            u = [B[i] - A[i] for i in range(3)]; w = [D[i] - A[i] for i in range(3)]
                            n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
                            # a face visivel aponta para a agua (para dentro da quina) e para cima
                            tw = (-(math.cos(t0) + math.cos(t1)), -(math.sin(t0) + math.sin(t1)))
                            if n[0] * tw[0] + n[1] + n[2] * tw[1] < 0:
                                q = q[::-1]
                            m.quad(mat, q, nrm(tw[0] * 0.25, 0.85, tw[1] * 0.25))

    # cantos concavos da lagoa = quina de terra entrando na agua (agua nos dois lados perpendiculares do tile de terra
    # e na diagonal): o perfil gira pelo lado da agua em volta da quina, fechando o corte entre as faixas
    for z in range(GH):
        for x in range(GW):
            if is_w(x, z):
                continue
            for sx, sz in ((1, -1), (1, 1), (-1, -1), (-1, 1)):
                if not (is_w(x + sx, z) and is_w(x, z + sz) and is_w(x + sx, z + sz)):
                    continue
                px, pz = x + (1 if sx > 0 else 0), z + (1 if sz > 0 else 0)
                h = H[z][x]
                a0, a1 = math.atan2(0, sx), math.atan2(sz, 0)     # direcoes da agua
                if abs(a1 - a0) > math.pi:
                    a1 += 2 * math.pi if a1 < a0 else -2 * math.pi
                steps = [a0, a1]                     # canto em 1 segmento (chanfro): orcamento de vertices
                for prof, mat in ((POND_LINE, "pond_line"), (SEA_LINE, "sea_line02")):
                    for (d0, y0, v0), (d1, y1, v1) in zip(prof, prof[1:]):
                        for t0, t1 in zip(steps, steps[1:]):
                            P = lambda t, d, y: (px - d * math.cos(t), y - 1 + h, pz - d * math.sin(t))
                            A, B, C, D = P(t0, d0, y0), P(t1, d0, y0), P(t1, d1, y1), P(t0, d1, y1)
                            uu0, uu1 = 256 * (t0 - a0) * 0.6, 256 * (t1 - a0) * 0.6
                            q = [(*A, uu0, v0), (*B, uu1, v0), (*C, uu1, v1), (*D, uu0, v1)]
                            u = [B[i] - A[i] for i in range(3)]; w = [D[i] - A[i] for i in range(3)]
                            n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
                            tw = (math.cos(t0) + math.cos(t1), math.sin(t0) + math.sin(t1))
                            if n[0] * tw[0] + n[1] + n[2] * tw[1] < 0:
                                q = q[::-1]
                            m.quad(mat, q, nrm(tw[0] * 0.25, 0.85, tw[1] * 0.25))

    # faces de penhasco: toda aresta entre tiles nao-rampa com alturas diferentes
    def top(x, z):
        return H[z][x] - (0.5 if tiles[z][x] == "~" else 0)
    for z in range(GH):
        for x in range(GW):
            for dx, dz in ((1, 0), (0, 1)):
                x2, z2 = x + dx, z + dz
                if x2 > GW - 1 or z2 > GH - 1 or (x, z) in ramp_cells or (x2, z2) in ramp_cells:
                    continue
                a, b = top(x, z), top(x2, z2)
                if a == b:
                    continue
                wa, wb = tiles[z][x] == "~", tiles[z2][x2] == "~"
                if wa != wb and abs(H[z][x] - H[z2][x2]) < 1e-6:
                    bank(x, z, dx, dz, water_first=wa, h=H[z][x])
                    continue
                hi, lo = max(a, b), min(a, b)
                if dz:                                   # aresta horizontal em z = z2
                    ez = z2
                    out = 0.67 if a > b else -0.67       # a face avanca para o lado baixo
                    if tiles[z][x] == "~" or tiles[z2][x] == "~":
                        out = 0
                    pts = [(x, lo, ez + out), (x + 1, lo, ez + out), (x + 1, hi, ez), (x, hi, ez)]
                    n = nrm(0, 0.55, 0.83 if a > b else -0.83)
                else:                                    # aresta vertical em x = x2
                    ex = x2
                    # a face lateral avanca 0,5 tile para o lado baixo: vertical, a camera de cima a via de quina, como
                    # uma linha escura solta (auditoria de 25/11); inclinada, aparece como uma faixa estreita de rocha
                    out = 0.5 if a > b else -0.5
                    if tiles[z][x] == "~" or tiles[z][x2] == "~":
                        out = 0
                    pts = [(ex + out, lo, z + 1), (ex + out, lo, z), (ex, hi, z), (ex, hi, z + 1)]
                    n = nrm(0.83 if a > b else -0.83, 0.55, 0)
                    if a < b:
                        pts = pts[::-1]
                uvs = [(256 * (p[0] + p[2]), 248 if p[1] == lo else 8) for p in pts]
                if dz and a < b:
                    pts, uvs = pts[::-1], uvs[::-1]
                m.quad("wall01_g", [(p[0], p[1], p[2], u, v) for p, (u, v) in zip(pts, uvs)], n)
    emit_banks()
    # ressaltos (v: pulo so para o sul, comportamento 0x3B como nos de Johto): beirada baixa na borda sul do tile
    for z in range(GH):
        for x in range(GW):
            if tiles[z][x] == "v":
                h = H[z][x]
                pts = [(x, h, z + 1), (x + 1, h, z + 1), (x + 1, h + 0.3, z + 0.55), (x, h + 0.3, z + 0.55)]
                uvs = [(256 * (p[0] + p[2]), 248 if p[1] == h else 168) for p in pts]
                m.quad("wall01_g", [(p[0], p[1], p[2], u, v) for p, (u, v) in zip(pts, uvs)], nrm(0, 0.55, 0.83))
    # lados das rampas (o desnivel entre a rampa e os vizinhos de fora)
    for x, z0, z1, hn, hs in ramps:
        for xs, nb in ((x, x - 1), (x + 1, x + 1)):
            if 0 <= nb < GW and (nb, z0) not in ramp_cells:
                base = H[z0][nb] if tiles[z0][nb] != "~" else H[z0][nb] - 0.5
                lowest, highest = min(hn, hs), max(hn, hs)
                if base < highest:
                    zt = z0 if hn > hs else z1
                    zb = z1 if hn > hs else z0
                    tri = [(xs, base, zb, 256 * zb, 248), (xs, base, zt, 256 * zt, 248), (xs, highest, zt, 256 * zt, 8), (xs, highest, zt, 256 * zt, 8)]
                    m.quad("wall01_g", tri if xs == x + 1 else tri[::-1], nrm(0, 0.55, 0.83))
    # bordas do caminho como no HGSS (road01_r): faixa de 1 tile no lado da grama, u 250 junto ao caminho -> 6 na grama,
    # v ao longo da borda; canto externo (caminho so na diagonal) com a outra metade da textura (u, v 259..505)
    road = {(x, z) for z in range(GH) for x in range(GW) if (tiles[z][x] == "=" or tiles[z][x] in "BSD#" and
            piso(x, z) == "road01") and (x, z) not in ramp_cells}
    road_strips = []
    # tiles de grama que recebem a borda: grama, flores, mato alto, arvore, cerca, ressalto, bloqueado (a borda fica
    # por baixo das flores, do mato e das arvores; sem ela o caminho terminava num corte reto junto a esses tiles)
    soft = {".", "f", "g", "h", "e", "T", "c", "v", "#", "S"}
    def ccw(q):                                  # mesmo sentido dos quads do HGSS (area com sinal negativa em x-z)
        a = sum(q[i][0] * q[(i + 1) % 4][2] - q[(i + 1) % 4][0] * q[i][2] for i in range(4))
        return q if a < 0 else q[::-1]

    def clip(poly, f):
        """Sutherland-Hodgman: parte do poligono convexo (pontos (a, d)) onde f(p) >= 0."""
        out = []
        for i, P in enumerate(poly):
            Q = poly[(i + 1) % len(poly)]
            fp, fq = f(P), f(Q)
            if fp >= 0:
                out.append(P)
            if (fp >= 0) != (fq >= 0):
                t = fp / (fp - fq)
                out.append((P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t))
        return out
    # direcao do caminho -> (ponto de mundo a partir de (a ao longo da borda, d para dentro da grama), sinal do v,
    # coordenada de mundo que vai no v); mesmos sentidos de v das faixas retas abaixo (como na Route 29)
    SIDES = {(0, -1): (lambda x, z, a, d: (x + a, z + d), 256, "x"), (0, 1): (lambda x, z, a, d: (x + a, z + 1 - d), -256, "x"),
             (-1, 0): (lambda x, z, a, d: (x + d, z + a), -256, "z"), (1, 0): (lambda x, z, a, d: (x + 1 - d, z + a), 256, "z")}
    # vizinhos ao longo da borda: para (0,-1) [caminho ao norte], a = 0 e o lado oeste e a = 1 o leste
    ALONG = {(0, -1): ((-1, 0), (1, 0)), (0, 1): ((-1, 0), (1, 0)), (-1, 0): ((0, -1), (0, 1)), (1, 0): ((0, -1), (0, 1))}
    for z in range(GH):
        for x in range(GW):
            if (x, z) in road or tiles[z][x] not in soft or (x, z) in ramp_cells:
                continue
            h = H[z][x] + 0.008
            same = lambda xx, zz: (xx, zz) in road and H[zz][xx] == H[z][x]
            dirs = [d for d in ((0, -1), (0, 1), (-1, 0), (1, 0)) if same(x + d[0], z + d[1])]
            if len(dirs) == 1:                           # borda reta: faixa de 1 tile (juntada com as vizinhas abaixo)
                dx, dz = dirs[0]
                if dz:
                    zi, zo = (z, z + 1) if dz < 0 else (z + 1, z)
                    road_strips.append(("h", zi, zo, x, 256 if dz < 0 else -256, h))
                else:
                    xi, xo = (x, x + 1) if dx < 0 else (x + 1, x)
                    road_strips.append(("v", xi, xo, z, 256 if dx > 0 else -256, h))
                continue
            if dirs:
                # canto concavo (caminho em dois lados vizinhos) e grama entre dois caminhos: cada borda vira um
                # poligono cortado em meia-esquadria na diagonal (cantos) ou na metade do tile (lados opostos); antes
                # as duas faixas inteiras se sobrepunham e o canto ficava com um quadrado escuro
                for d in dirs:
                    f, sv, axis = SIDES[d]
                    depth = 0.5 if (-d[0], -d[1]) in dirs else 1.0
                    poly = [(0, 0), (1, 0), (1, depth), (0, depth)]
                    lo, hi = ALONG[d]
                    if lo in dirs:
                        poly = clip(poly, lambda p: p[0] - p[1])
                    if hi in dirs:
                        poly = clip(poly, lambda p: (1 - p[0]) - p[1])
                    if len(poly) < 3:
                        continue
                    pts = []
                    for aa, dd in poly:
                        wx, wz = f(x, z, aa, dd)
                        pts.append((wx, h, wz, 250 - 244 * dd, sv * (wx if axis == "x" else wz)))
                    for k in range(1, len(pts) - 1):     # leque de triangulos (quad com o ultimo vertice repetido)
                        m.quad("road01_r", ccw([pts[0], pts[k], pts[k + 1], pts[k + 1]]))
                continue
            for sx, sz in ((1, -1), (1, 1), (-1, -1), (-1, 1)):
                if same(x + sx, z + sz):
                    nx, nz = x + (1 if sx > 0 else 0), z + (1 if sz > 0 else 0)
                    fx, fz = x + (0 if sx > 0 else 1), z + (0 if sz > 0 else 1)
                    q = [(nx, h, nz, 259, 259), (fx, h, nz, 259, 508), (fx, h, fz, 505, 508), (nx, h, fz, 505, 259)]
                    m.quad("road01_r", ccw(q))
                    break
    # faixas retas seguidas da borda do caminho viram uma so (ate MAXQ tiles, sem cruzar divisa de bloco)
    runs = []
    for o, inner, outer, a, sv, h in sorted(road_strips):
        if runs and runs[-1][:3] == [o, inner, outer] and runs[-1][4:] == [sv, h] and runs[-1][3][1] == a \
                and runs[-1][3][1] - runs[-1][3][0] < MAXQ and a % 32:
            runs[-1][3][1] = a + 1
        else:
            runs.append([o, inner, outer, [a, a + 1], sv, h])
    for o, inner, outer, (a0, a1), sv, h in runs:
        if o == "h":
            q = [(a1, h, outer, 6, sv * a1), (a1, h, inner, 250, sv * a1), (a0, h, inner, 250, sv * a0), (a0, h, outer, 6, sv * a0)]
        else:
            q = [(outer, h, a1, 6, sv * a1), (inner, h, a1, 250, sv * a1), (inner, h, a0, 250, sv * a0), (outer, h, a0, 6, sv * a0)]
        m.quad("road01_r", ccw(q))
    # mato alto e flores por cima da grama
    # cercas como as de New Bark (fence_b): trecho horizontal = quad inclinado na linha (y +0,02 -> +0,73, recua 0,71),
    # u 128 + 256 por tile; trecho vertical = faixa plana de 0,5 a +0,38, ligando as linhas, u 256 por tile, v 448 -> 320
    fence = {(x, z) for z in range(GH) for x in range(GW) if tiles[z][x] == "c"}
    for z in range(GH):
        x = 0
        while x < GW:
            if (x, z) in fence and ((x + 1, z) in fence or (x - 1, z) not in fence and (x, z - 1) not in fence and (x, z + 1) not in fence):
                x0 = x
                while x < GW and (x, z) in fence:
                    x += 1
                if x - x0 >= 2 or not any((x0, z + d) in fence for d in (-1, 1)):
                    h = H[z][x0]
                    m.quad("fence_b", [(x0, h + 0.02, z + 0.73, 128, 256), (x, h + 0.02, z + 0.73, 128 + 256 * (x - x0), 256),
                                       (x, h + 0.73, z + 0.02, 128 + 256 * (x - x0), 0), (x0, h + 0.73, z + 0.02, 128, 0)])
            else:
                x += 1
    for x in range(GW):
        z = 0
        while z < GH:
            if (x, z) in fence and (x, z + 1) in fence:
                z0 = z
                while z < GH and (x, z) in fence:
                    z += 1
                h = H[z0][x]
                q = [(x, h + 0.38, z - 1 + 0.38, 256 * (z - 1 - z0), 448), (x + 0.5, h + 0.38, z - 1 + 0.38, 256 * (z - 1 - z0), 320),
                     (x + 0.5, h + 0.38, z0 + 0.38, 0, 320), (x, h + 0.38, z0 + 0.38, 0, 448)]
                m.quad("fence_b", ccw(q))
            else:
                z += 1
    for c, mat, dy, uv0 in (("e", "egrass", 0.12, (-22528, 2048)), ("f", "flower01", 0.06, (-23296, -768)),
                            ("g", "flower02", 0.06, (-23296, -768)), ("h", "flower03", 0.06, (-23296, -768))):
        cells = {(x, z) for z in range(GH) for x in range(GW) if tiles[z][x] == c}
        for hz in sorted({H[z][x] for x, z in cells}):
            for r in rects({(x, z) for x, z in cells if H[z][x] == hz}):
                m.flat(mat, r, hz + dy, uv0)
    # arvores: os tiles T sao cobertos por arvores de 2x2 a partir do canto noroeste de cada uma (varredura linha a
    # linha); cada arvore e um quad inclinado como os do HGSS (3,08 tiles de altura, recua 2,54). Geometria e UV
    # medidas na Route 29 (bloco 2, auditoria de 25/11):
    #  - tree01 (textura tree01gs, 64x64, UMA arvore inteira): quad de 4 tiles de largura centrado na arvore, u 0-1024;
    #  - tree01_re (textura que repete, uma arvore a cada 2 tiles): fileira de arvores lado a lado, u 512 por arvore.
    # (Antes: par = tree01 inteiro em 4 tiles, arvore so = u 384-896 em 2 tiles, que mostrava meia arvore cortada, e
    #  coluna de 1 tile = fatia do meio da textura: as arvores "cortadas" e as fatias verticais da auditoria.)
    trees = {(x, z) for z in range(GH) for x in range(GW) if tiles[z][x] == "T"}
    done, blocks = set(), []
    for z in range(GH):
        for x in range(GW):
            if (x, z) in trees and (x, z) not in done:
                w = 2 if (x + 1, z) in trees and (x + 1, z) not in done else 1
                h = 2 if all((x + i, z + 1) in trees and (x + i, z + 1) not in done for i in range(w)) else 1
                for i in range(w):
                    for j in range(h):
                        done.add((x + i, z + j))
                blocks.append((x, z, w, h))
    rows = {}

    def tree_quad(mat, xa, xb, ua, ub, z, h, x_alt, k=1.0):
        hz = H[min(z + h - 1, GH - 1)][min(max(int(x_alt), 0), GW - 1)]
        zb = z + h
        m.quad(mat, [(xa, hz, zb + 0.62 * k, ua, 1024), (xb, hz, zb + 0.62 * k, ub, 1024),
                     (xb, hz + 3.08 * k, zb - 1.92 * k, ub, 0), (xa, hz + 3.08 * k, zb - 1.92 * k, ua, 0)], 0x18b51800)
    for x, z, w, h in blocks:
        if w == 2 and h == 2:
            rows.setdefault((z, h), []).append((x, w))
        else:
            # sobra de 1 tile de largura ou de altura: no GBA sao os arbustos de 1 tile (cercas vivas em volta das
            # casas, beiras de floresta impares). Arbusto = a arvore inteira em meia escala, um por tile; em tamanho
            # cheio, a arvore de 4 tiles cobria o telhado das construcoes vizinhas
            for i in range(w):
                for j in range(h):
                    tree_quad("tree01", x + i - 0.5, x + i + 1.5, 0, 1024, z + j, 1, x + i, 0.5)
    for (z, h), items in rows.items():
        items.sort()
        i = 0
        while i < len(items):
            x0, w = items[i]
            if w == 2:                                   # fileira de arvores 2x2 encostadas: uma faixa tree01_re
                k = i
                while k + 1 < len(items) and items[k + 1] == (items[k][0] + 2, 2) and (k + 1 - i) < 4:   # ate 4 arvores por quad, como na Route 29
                    k += 1
                n = k - i + 1
                if n >= 2:
                    tree_quad("tree01_re", x0, x0 + 2 * n, 0, 512 * n, z, h, x0)
                    i = k + 1
                    continue
            tree_quad("tree01", x0 - 1, x0 + 3, 0, 1024, z, h, x0)     # arvore 2x2 sozinha: a arvore inteira
            i += 1
    return m, H, ramps


def build_bdhc(g, H, ramps):
    ramp_cells = {(x, z) for x, z0, z1, _, _ in ramps for z in range(z0, z1)}
    plates = []
    groups = {}
    for z in range(GH):
        for x in range(GW):
            if (x, z) not in ramp_cells:
                groups.setdefault(H[z][x], set()).add((x, z))
    for h, cells in sorted(groups.items()):
        left = set(cells)
        for z in range(GH):
            for x in range(GW):
                if (x, z) not in left:
                    continue
                w = 1
                while (x + w, z) in left:
                    w += 1
                hh = 1
                while all((x + i, z + hh) in left for i in range(w)):
                    hh += 1
                for i in range(w):
                    for j in range(hh):
                        left.discard((x + i, z + j))
                plates.append((x, z, x + w, z + hh, h, h, None))
    # rampas vizinhas na mesma faixa de z viram uma placa so
    by_span = {}
    for x, z0, z1, hn, hs in ramps:
        by_span.setdefault((z0, z1, hn, hs), []).append(x)
    for (z0, z1, hn, hs), xs in by_span.items():
        xs.sort()
        start = prev = xs[0]
        for xv in xs[1:] + [None]:
            if xv is not None and xv == prev + 1:
                prev = xv; continue
            plates.append((start, z0, prev + 1, z1, hn, hs, "z"))
            if xv is not None:
                start = prev = xv
    return bdhc.build(plates)


def perms(g):
    return [PERM.get(g["tiles"][z][x], 0) for z in range(GH) for x in range(GW)]


def gerar(block, blocos, arquivo):
    g = load(arquivo)
    ld = Land(block)
    mesh, H, ramps = build_mesh(g)
    donors = [Land(blocos[d]).rest[:Land(blocos[d]).sizes[2]] for d in g["doadores"]]
    assert set(mesh.quads) <= set(ORDER), set(mesh.quads) - set(ORDER)
    model = compose(ld.rest[:ld.sizes[2]], donors, [(n, mesh.dl(n)) for n in ORDER if n in mesh.quads])
    heights_b = build_bdhc(g, H, ramps).pack()
    ld.perms = perms(g)
    ld.objs = [Land.obj(mdl, x, z, H[int(z)][int(x)] + dy) for mdl, x, z, dy in g["objetos"]]
    ld.sizes[2], ld.sizes[3] = len(model), len(heights_b)
    ld.rest = model + heights_b
    return ld.pack()


if __name__ == "__main__":
    g = load(sys.argv[1])
    for z in range(GH):
        print("".join({0x8000: "#", 0x0002: "e", 0x0015: "~", 0: "."}[v] for v in perms(g)[z * 32:z * 32 + 32]))
