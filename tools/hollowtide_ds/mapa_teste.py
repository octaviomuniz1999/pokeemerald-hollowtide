#!/usr/bin/env python3
"""CP-DS-03A — mapa de teste com terreno 3D gerado (prova do pipeline de mapas originais; NAO e conteudo de Lunia).

Substitui o bloco 57 (metade sul da Route 39, celula (8,6) da matriz 0, mapa 43), que se liga a pe ao corredor norte
de Breezeport/Olivine. Do bloco original so ficam os MATERIAIS (texturas do conjunto da area 7: grama, estrada,
penhasco, arvore, mato alto, flores) e a estrutura do modelo; a geometria, as alturas (BDHC) e a colisao sao geradas
aqui a partir do desenho abaixo:

  - borda de floresta (fileiras de arvores) em volta, aberta so no sul (colunas 21-25: emenda com Breezeport, altura 1);
  - campina baixa (altura 1) com caminho de terra, mato alto (encontros) e flores;
  - plato alto (altura 2) ao norte, com face de penhasco na linha z=12 e uma RAMPA de terra (colunas 14-16, z 12-15)
    que liga os dois niveis — o desnivel real (modelo, BDHC e colisao combinando);
  - arvores soltas na campina e no plato; uma placa (construcao 34 da lista da area) no plato, com colisao.
Unidades: tile do bloco (0..32); no modelo 1 tile = 1024, centro do bloco = 0; altura h -> y = h*1024.
Uso como modulo: gerar(bloco_original) -> bloco novo (land_data.py chama pelo campo "gerador" do land.json).
"""
import math, struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from land_data import Land
from nsbmd import Model, decode_dl, encode_dl
import bdhc

T = 1024
LOW, HIGH = 1.0, 2.0
CLIFF_Z = 12.0                       # face do penhasco: plato (z < 12) / campina (z >= 12)
RAMP = (14, 17, 12, 15)              # x0, x1, z0, z1 (altura 2 em z0 -> 1 em z1)
PATH_SEAM = (21, 26)                 # colunas abertas na emenda sul (iguais as de Breezeport)
UP = (0 & 0x3FF) | (511 << 10) | (0 << 20)


def nrm(x, y, z):
    q = lambda v: int(round(max(-1, min(0.998, v)) * 512)) & 0x3FF
    return q(x) | (q(y) << 10) | (q(z) << 20)


class Mesh:
    def __init__(self):
        self.quads = {}              # material -> [(4 vertices (x, y, z, u, v), normal)]

    def quad(self, mat, verts, normal=UP):
        self.quads.setdefault(mat, []).append((verts, normal))

    def flat(self, mat, x0, z0, x1, z1, h, uv0=(0, 0), du=256, dv=256):
        """Retangulo horizontal; UV linear (256 por tile, como os blocos do HGSS)."""
        u = lambda x: int(uv0[0] + du * (x - 16)); v = lambda z: int(uv0[1] + dv * (z - 16))
        self.quad(mat, [(x0, h, z1, u(x0), v(z1)), (x1, h, z1, u(x1), v(z1)), (x1, h, z0, u(x1), v(z0)), (x0, h, z0, u(x0), v(z0))])

    def dl(self, mat):
        cmds = [(0x40, [1])]
        for verts, n in self.quads.get(mat, []):
            for i, (x, y, z, u, v) in enumerate(verts):
                cmds.append((0x22, [(u & 0xFFFF) | ((v & 0xFFFF) << 16)]))
                if i == 0:
                    cmds.append((0x21, [n]))
                X, Y, Z = int(round((x - 16) * T)), int(round(y * T)), int(round((z - 16) * T))
                cmds.append((0x23, [(X & 0xFFFF) | ((Y & 0xFFFF) << 16), Z & 0xFFFF]))
        cmds.append((0x41, []))
        return encode_dl(cmds) if self.quads.get(mat) else b""


def height(x, z):
    """Altura do terreno no tile (centro) — a mesma regra do BDHC abaixo."""
    x0, x1, z0, z1 = RAMP
    if x0 <= x < x1 and z0 <= z < z1:
        return HIGH - (z + 0.5 - z0) / (z1 - z0) * (HIGH - LOW)
    return HIGH if z < CLIFF_Z else LOW


def layout():
    """Grade de colisao 32x32: '#' bloqueado (arvore, penhasco, placa), 'e' mato alto, '.' livre."""
    g = [["." for _ in range(32)] for _ in range(32)]
    for z in range(32):
        for x in range(32):
            if x < 4 or x >= 28 or z < 4:
                g[z][x] = "#"                          # floresta (borda)
            if z >= 28 and not (PATH_SEAM[0] <= x < PATH_SEAM[1]):
                g[z][x] = "#"                          # floresta sul, menos o caminho
            if z == 12 and not (RAMP[0] <= x < RAMP[1]) and 4 <= x < 28:
                g[z][x] = "#"                          # penhasco
            if z in (12, 13, 14) and x in (RAMP[0] - 1, RAMP[1]):
                g[z][x] = "#"                          # lados da rampa
    for x0, z0 in TREES:
        for dz in (0, 1):
            for dx in (0, 1):
                g[z0 + dz][x0 + dx] = "#"
    for z in range(20, 26):
        for x in range(6, 12):
            g[z][x] = "e"                              # mato alto
    g[SIGN[1]][SIGN[0]] = "#"
    return g


TREES = [(8, 15), (24, 16), (6, 6), (24, 6), (10, 26)]   # arvores soltas (2x2, canto noroeste)
SIGN = (19, 8)                                          # placa no plato


def build_mesh():
    m = Mesh()
    # chao: plato e campina (inteiros, as arvores e o penhasco ficam por cima)
    m.flat("grass01", 0, 0, 32, CLIFF_Z, HIGH)
    m.flat("grass01", 0, CLIFF_Z, RAMP[0] - 1, 32, LOW)
    m.flat("grass01", RAMP[1] + 1, CLIFF_Z, 32, 32, LOW)
    m.flat("grass01", RAMP[0] - 1, RAMP[3], RAMP[1] + 1, 32, LOW)
    # caminho de terra: emenda sul -> norte -> oeste -> pe da rampa; no plato, da rampa ate a placa
    m.flat("road01", PATH_SEAM[0], 18, PATH_SEAM[1], 32, LOW + 0.01)
    m.flat("road01", RAMP[0], 18, PATH_SEAM[0], 21, LOW + 0.01)
    m.flat("road01", RAMP[0], RAMP[3], RAMP[1], 18, LOW + 0.01)
    m.flat("road01", RAMP[0], 7, RAMP[1], CLIFF_Z, HIGH + 0.01)
    m.flat("road01", RAMP[1], 7, SIGN[0], 10, HIGH + 0.01)
    # rampa: superficie inclinada de terra entre os dois niveis
    x0, x1, z0, z1 = RAMP
    k = (HIGH - LOW) / (z1 - z0)
    n = nrm(0, 1 / math.hypot(1, k), k / math.hypot(1, k))
    u = lambda x: int(256 * (x - 16)); v = lambda z: int(256 * (z - 16))
    m.quad("road01", [(x0, LOW + 0.01, z1, u(x0), v(z1)), (x1, LOW + 0.01, z1, u(x1), v(z1)),
                      (x1, HIGH + 0.01, z0, u(x1), v(z0)), (x0, HIGH + 0.01, z0, u(x0), v(z0))], n)
    # face do penhasco (plato -> campina), inclinada para fora como as do HGSS; e os lados da rampa
    wn = nrm(0, 0.55, 0.83)
    for a, b in ((4, x0), (x1, 28)):
        m.quad("wall01_g", [(a, LOW, CLIFF_Z + 0.67, 256 * a, 248), (b, LOW, CLIFF_Z + 0.67, 256 * b, 248),
                            (b, HIGH, CLIFF_Z, 256 * b, 8), (a, HIGH, CLIFF_Z, 256 * a, 8)], wn)
    for xs, sx in ((x0, -1), (x1, 1)):                # paredes laterais da rampa (triangulo como quad degenerado)
        m.quad("wall01_g", [(xs, LOW, z1, 256 * z1, 248), (xs, LOW, z0, 256 * z0, 248),
                            (xs, HIGH, z0, 256 * z0, 8), (xs, HIGH, z0, 256 * z0, 8)], nrm(sx * 0.9, 0.43, 0))
    # mato alto e flores
    for z in range(20, 26):
        m.flat("egrass", 6, z, 12, z + 1, LOW + 0.12, uv0=(-22528, 2048))
    for fx, fz in ((22, 14), (23, 15), (25, 14), (9, 9), (12, 7), (26, 22)):
        m.flat("flower01", fx, fz, fx + 1, fz + 1, (HIGH if fz < CLIFF_Z else LOW) + 0.06, uv0=(-22528, 1024))
    # arvores: fileiras de quads inclinados (como os blocos do HGSS: 3,08 tiles de altura, recuam 2,54)
    def tree(x0_, x1_, zb, h, wide=True):
        mat = "tree01" if wide else "tree01_re"
        uw = 1024 if wide else 512
        m.quad(mat, [(x0_, h, zb + 0.62, 0, 1024), (x1_, h, zb + 0.62, uw, 1024),
                     (x1_, h + 3.08, zb - 1.92, uw, 0), (x0_, h + 3.08, zb - 1.92, 0, 0)], 0x18b51800)
    for zb in range(2, 34, 2):                         # bordas leste e oeste
        h = HIGH if zb - 1 < CLIFF_Z else LOW
        tree(0, 4, zb, h); tree(28, 32, zb, h)
    for zb in (2, 4):                                  # borda norte
        for xa in range(4, 28, 4):
            tree(xa, xa + 4, zb, HIGH)
    for zb in (30, 32):                                # borda sul, menos o caminho
        for xa, xb in ((4, 8), (8, 12), (12, 16), (16, 20), (20, PATH_SEAM[0]), (PATH_SEAM[1], 28)):
            tree(xa, xb, zb, LOW, wide=(xb - xa == 4))
    for tx, tz in TREES:
        tree(tx, tx + 2, tz + 2, HIGH if tz < CLIFF_Z else LOW, wide=False)
        m.flat("tree01_un", tx, tz, tx + 2, tz + 2, (HIGH if tz < CLIFF_Z else LOW) + 0.02, uv0=(0, 0), du=256, dv=256)
    return m


def build_bdhc():
    x0, x1, z0, z1 = RAMP
    return bdhc.build([
        (0, 0, 32, CLIFF_Z, HIGH, HIGH, None),
        (0, CLIFF_Z, x0, 32, LOW, LOW, None),
        (x1, CLIFF_Z, 32, 32, LOW, LOW, None),
        (x0, CLIFF_Z, x1, z1, HIGH, LOW, "z"),         # rampa
        (x0, z1, x1, 32, LOW, LOW, None),
    ])


def gerar(block):
    ld = Land(block)
    mdl = Model(ld.rest[:ld.sizes[2]])
    mesh = build_mesh()
    sm = mdl.shape_material()
    used = set(mesh.quads)
    missing = used - set(sm.values())
    assert not missing, f"materiais que o bloco doador nao tem: {missing}"
    dls = [mesh.dl(sm[i]) for i in range(len(mdl.dls))]
    nv = sum(4 * len(q) for q in mesh.quads.values()); nq = sum(len(q) for q in mesh.quads.values())
    model = mdl.pack(dls, counts=(nv, nq, 0, nq))
    heights = build_bdhc().pack()
    g = layout()
    perms = []
    for z in range(32):
        for x in range(32):
            perms.append({"#": 0x8000, "e": 0x0002, ".": 0x0000}[g[z][x]])
    ld.perms = perms
    ld.objs = [Land.obj(34, SIGN[0], SIGN[1], HIGH)]
    ld.sizes[2], ld.sizes[3] = len(model), len(heights)
    ld.rest = model + heights
    return ld.pack()


if __name__ == "__main__":
    for row in layout():
        print("".join(row))
