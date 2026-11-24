#!/usr/bin/env python3
"""Gerador v2 de blocos de mapa: o setor desenhado numa grade de texto (CP-DS-03B).

Arquivo do setor (texto, revisavel no repositorio):
  [doadores]  numeros dos blocos de onde vem os materiais (mesma area), ex.: 57 59
  [tiles]     32 linhas de 32 letras:
                .  grama            =  caminho de terra     e  mato alto (encontros)    f  flores
                ~  agua (lagoa)     T  arvore (floresta)    #  bloqueado (beira de penhasco, lados de rampa)
                S  objeto (o tile fica bloqueado; o modelo vem de [objetos])
  [alturas]   32 linhas de 32 caracteres: altura do chao em tiles (0-9); r = rampa (sobe para o vizinho mais alto
              no eixo norte-sul)
  [objetos]   linhas "modelo x z" (construcoes da lista da area; altura = a do tile)
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
UP = 511 << 10
MAXQ = 4
FLOOR = {".": "grass01", "=": "road01", "e": "grass01", "f": "grass01", "T": "grass01", "#": "grass01", "S": "grass01", "~": None}
PERM = {"T": 0x8000, "#": 0x8000, "S": 0x8000, "e": 0x0002, "~": 0x0015}
ORDER = ["grass01", "road01", "road01_r", "egrass", "wall01_g", "sea_un", "sea_on", "flower01", "tree01_un", "tree01_re", "tree01"]


def nrm(x, y, z):
    q = lambda v: int(round(max(-1, min(0.998, v)) * 512)) & 0x3FF
    return q(x) | (q(y) << 10) | (q(z) << 20)


def load(path):
    sec, out = None, {"doadores": [], "tiles": [], "alturas": [], "objetos": []}
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("[") and line.endswith("]"):
            sec = line[1:-1]; continue
        if not line.strip() or line.lstrip().startswith(";"):
            continue
        if sec == "doadores":
            out["doadores"] += [int(v) for v in line.split()]
        elif sec in ("tiles", "alturas"):
            assert len(line) == 32, f"{sec}: linha com {len(line)} colunas: {line!r}"
            out[sec].append(line)
        elif sec == "objetos":
            mdl, x, z = line.split()
            out["objetos"].append((int(mdl), int(x), int(z)))
    assert len(out["tiles"]) == 32 and len(out["alturas"]) == 32, "a grade tem de ter 32 linhas"
    return out


def heights(g):
    """Altura no centro de cada tile; rampas interpoladas entre os vizinhos norte e sul fora da rampa."""
    H = [[None] * 32 for _ in range(32)]
    for z in range(32):
        for x in range(32):
            c = g["alturas"][z][x]
            if c != "r":
                H[z][x] = float(c)
    ramps = []
    for x in range(32):
        z = 0
        while z < 32:
            if g["alturas"][z][x] == "r":
                z0 = z
                while z < 32 and g["alturas"][z][x] == "r":
                    z += 1
                hn = H[z0 - 1][x] if z0 > 0 else None
                hs = H[z][x] if z < 32 else None
                for k in range(z0, z):
                    t = (k - z0 + 0.5) / (z - z0)
                    H[k][x] = hn + (hs - hn) * t
                ramps.append((x, z0, z, hn, hs))
            else:
                z += 1
    return H, ramps


def rects(cells):
    """Agrupa um conjunto de tiles (x, z) em retangulos de ate MAXQ x MAXQ (guloso, linha a linha)."""
    left, out = set(cells), []
    for z in range(32):
        for x in range(32):
            if (x, z) not in left:
                continue
            w = 1
            while w < MAXQ and (x + w, z) in left:
                w += 1
            h = 1
            while h < MAXQ and all((x + i, z + h) in left for i in range(w)):
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
    for z in range(32):
        for x in range(32):
            if (x, z) in ramp_cells:
                continue
            c = tiles[z][x]
            mat = FLOOR[c]
            if mat:
                groups.setdefault((mat, H[z][x]), set()).add((x, z))
    for (mat, h), cells in sorted(groups.items()):
        for r in rects(cells):
            m.flat(mat, r, h + (0.01 if mat == "road01" else 0))
    # agua: duas camadas meio tile abaixo do chao, como no HGSS
    water = {(x, z) for z in range(32) for x in range(32) if tiles[z][x] == "~"}
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
    # faces de penhasco: toda aresta entre tiles nao-rampa com alturas diferentes (e margem da agua)
    def top(x, z):
        return H[z][x] - (0.5 if tiles[z][x] == "~" else 0)
    for z in range(32):
        for x in range(32):
            for dx, dz in ((1, 0), (0, 1)):
                x2, z2 = x + dx, z + dz
                if x2 > 31 or z2 > 31 or (x, z) in ramp_cells or (x2, z2) in ramp_cells:
                    continue
                a, b = top(x, z), top(x2, z2)
                if a == b:
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
                    out = 0.0
                    pts = [(ex, lo, z + 1), (ex, lo, z), (ex, hi, z), (ex, hi, z + 1)]
                    n = nrm(0.83 if a > b else -0.83, 0.55, 0)
                    if a < b:
                        pts = pts[::-1]
                uvs = [(256 * (p[0] + p[2]), 248 if p[1] == lo else 8) for p in pts]
                if dz and a < b:
                    pts, uvs = pts[::-1], uvs[::-1]
                m.quad("wall01_g", [(p[0], p[1], p[2], u, v) for p, (u, v) in zip(pts, uvs)], n)
    # lados das rampas (o desnivel entre a rampa e os vizinhos de fora)
    for x, z0, z1, hn, hs in ramps:
        for xs, nb in ((x, x - 1), (x + 1, x + 1)):
            if 0 <= nb < 32 and (nb, z0) not in ramp_cells:
                base = H[z0][nb] if tiles[z0][nb] != "~" else H[z0][nb] - 0.5
                lowest, highest = min(hn, hs), max(hn, hs)
                if base < highest:
                    zt = z0 if hn > hs else z1
                    zb = z1 if hn > hs else z0
                    tri = [(xs, base, zb, 256 * zb, 248), (xs, base, zt, 256 * zt, 248), (xs, highest, zt, 256 * zt, 8), (xs, highest, zt, 256 * zt, 8)]
                    m.quad("wall01_g", tri if xs == x + 1 else tri[::-1], nrm(0, 0.55, 0.83))
    # bordas do caminho como no HGSS (road01_r): faixa de 1 tile no lado da grama, u 250 junto ao caminho -> 6 na grama,
    # v ao longo da borda; canto externo (caminho so na diagonal) com a outra metade da textura (u, v 259..505)
    road = {(x, z) for z in range(32) for x in range(32) if tiles[z][x] == "=" and (x, z) not in ramp_cells}
    soft = {".", "f", "#", "S"}
    def ccw(q):                                  # mesmo sentido dos quads do HGSS (area com sinal negativa em x-z)
        a = sum(q[i][0] * q[(i + 1) % 4][2] - q[(i + 1) % 4][0] * q[i][2] for i in range(4))
        return q if a < 0 else q[::-1]
    for z in range(32):
        for x in range(32):
            if (x, z) in road or tiles[z][x] not in soft or (x, z) in ramp_cells:
                continue
            h = H[z][x] + 0.008
            same = lambda xx, zz: (xx, zz) in road and H[zz][xx] == H[z][x]
            orth = False
            for dx, dz in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                if not same(x + dx, z + dz):
                    continue
                orth = True
                if dz:                               # caminho ao norte/sul: borda horizontal
                    zi, zo = (z, z + 1) if dz < 0 else (z + 1, z)
                    q = [(x + 1, h, zo, 6, 256 * (x + 1)), (x + 1, h, zi, 250, 256 * (x + 1)),
                         (x, h, zi, 250, 256 * x), (x, h, zo, 6, 256 * x)]
                else:                                # caminho a oeste/leste: borda vertical
                    xi, xo = (x, x + 1) if dx < 0 else (x + 1, x)
                    q = [(xo, h, z + 1, 6, 256 * (z + 1)), (xi, h, z + 1, 250, 256 * (z + 1)),
                         (xi, h, z, 250, 256 * z), (xo, h, z, 6, 256 * z)]
                m.quad("road01_r", ccw(q))
            if orth:
                continue
            for sx, sz in ((1, -1), (1, 1), (-1, -1), (-1, 1)):
                if same(x + sx, z + sz):
                    nx, nz = x + (1 if sx > 0 else 0), z + (1 if sz > 0 else 0)
                    fx, fz = x + (0 if sx > 0 else 1), z + (0 if sz > 0 else 1)
                    q = [(nx, h, nz, 259, 259), (fx, h, nz, 259, 508), (fx, h, fz, 505, 508), (nx, h, fz, 505, 259)]
                    m.quad("road01_r", ccw(q))
                    break
    # mato alto e flores por cima da grama
    for c, mat, dy, uv0 in (("e", "egrass", 0.12, (-22528, 2048)), ("f", "flower01", 0.06, (-22528, 1024))):
        cells = {(x, z) for z in range(32) for x in range(32) if tiles[z][x] == c}
        for hz in sorted({H[z][x] for x, z in cells}):
            for r in rects({(x, z) for x, z in cells if H[z][x] == hz}):
                m.flat(mat, r, hz + dy, uv0)
    # arvores: os tiles T sao cobertos por arvores de 2x2 a partir do canto noroeste de cada uma (varredura linha a
    # linha); cada arvore e um quad inclinado como os do HGSS (3,08 tiles de altura, recua 2,54). Pares lado a lado
    # na mesma linha viram um quad de 4 tiles (textura de duas arvores, tree01); uma arvore so, tree01_re (u 0-512).
    # (metade da textura tree01 mostra meia arvore: a textura e espelhada; visto no DeSmuME.)
    trees = {(x, z) for z in range(32) for x in range(32) if tiles[z][x] == "T"}
    done, blocks = set(), []
    for z in range(32):
        for x in range(32):
            if (x, z) in trees and (x, z) not in done:
                w = 2 if (x + 1, z) in trees and (x + 1, z) not in done else 1
                h = 2 if all((x + i, z + 1) in trees and (x + i, z + 1) not in done for i in range(w)) else 1
                for i in range(w):
                    for j in range(h):
                        done.add((x + i, z + j))
                blocks.append((x, z, w, h))
    rows = {}
    for x, z, w, h in blocks:
        rows.setdefault((z, h), []).append((x, w))
    for (z, h), items in rows.items():
        items.sort()
        i = 0
        while i < len(items):
            x0, w = items[i]
            if w == 2 and i + 1 < len(items) and items[i + 1] == (x0 + 2, 2):
                w, i = 4, i + 2
            else:
                i += 1
            hz = H[min(z + h - 1, 31)][x0]
            zb = z + h
            mat, uw = ("tree01", 1024) if w == 4 else ("tree01_re", 512 if w == 2 else 256)
            m.quad(mat, [(x0, hz, zb + 0.62, 0, 1024), (x0 + w, hz, zb + 0.62, uw, 1024),
                         (x0 + w, hz + 3.08, zb - 1.92, uw, 0), (x0, hz + 3.08, zb - 1.92, 0, 0)], 0x18b51800)
    return m, H, ramps


def build_bdhc(g, H, ramps):
    ramp_cells = {(x, z) for x, z0, z1, _, _ in ramps for z in range(z0, z1)}
    plates = []
    groups = {}
    for z in range(32):
        for x in range(32):
            if (x, z) not in ramp_cells:
                groups.setdefault(H[z][x], set()).add((x, z))
    for h, cells in sorted(groups.items()):
        left = set(cells)
        for z in range(32):
            for x in range(32):
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
    return [PERM.get(g["tiles"][z][x], 0) for z in range(32) for x in range(32)]


def gerar(block, blocos, arquivo):
    g = load(arquivo)
    ld = Land(block)
    mesh, H, ramps = build_mesh(g)
    donors = [Land(blocos[d]).rest[:Land(blocos[d]).sizes[2]] for d in g["doadores"]]
    assert set(mesh.quads) <= set(ORDER), set(mesh.quads) - set(ORDER)
    model = compose(ld.rest[:ld.sizes[2]], donors, [(n, mesh.dl(n)) for n in ORDER if n in mesh.quads])
    heights_b = build_bdhc(g, H, ramps).pack()
    ld.perms = perms(g)
    ld.objs = [Land.obj(mdl, x, z, H[z][x]) for mdl, x, z in g["objetos"]]
    ld.sizes[2], ld.sizes[3] = len(model), len(heights_b)
    ld.rest = model + heights_b
    return ld.pack()


if __name__ == "__main__":
    g = load(sys.argv[1])
    for z in range(32):
        print("".join({0x8000: "#", 0x0002: "e", 0x0015: "~", 0: "."}[v] for v in perms(g)[z * 32:z * 32 + 32]))
