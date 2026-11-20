#!/usr/bin/env python3
"""Route 9 (Corredor de Ferro) — Passway Village -> Voltara, 48x36 (General + Rustboro: trilhos e casa de forca).

A estrada desce da montanha (entrada oeste nas linhas 18-19, alinhada com a Passway) e corre ao lado da
ferrovia que vem de Voltara: os trilhos terminam num para-choque (linha morta de carga) antes da faixa que a
Passway enxerga. Subestacao, mato alto
(Pokemon eletricos) e bosques. Saida leste (linhas 18-19) para Voltara.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 48, 36
WEST = (18, 19)            # = estrada leste da Passway (offset 0)
EAST = (18, 19)            # para Voltara
RAILS = (8, 10)            # duas linhas de trilho, de x = RAIL_START ate a borda leste
RAIL_START = 12            # para-choque: a Passway enxerga as colunas 0-7 da rota (so primario ali)
POLES = []


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Rustboro")
    c.fill("grass")
    ids = json.load(open(os.path.join(os.path.dirname(__file__), "..", "mapgen", "custom_ids.json")))["rustboro"]
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    # estrada: oeste -> sobe para a linha do trem -> corre ao lado dos trilhos -> desce -> leste
    path(0, WEST[0], 15, WEST[1])
    path(14, 13, 15, WEST[1])
    path(14, 12, 41, 13, "plaza")                          # calcada de servico ao longo da ferrovia
    path(40, 12, 41, EAST[1]); path(40, EAST[0], W - 1, EAST[1])
    # ramal ate a porta da subestacao
    c.stamp("rb_office_small", 34, 20)
    path(24, 13, 25, 26); path(24, 25, 36, 26)
    # mato alto (eletricos) e bosques
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass" and c.level[y][x] == 3:
                    c.terrain[y][x] = "tall"
    BL = ["  ,,,,,, ", ",,,,,,,,,", ",,,,,,,,,", "  ,,,,,  "]
    tall(4, 21, BL); tall(26, 15, ["  ,,,,,,,,,", ",,,,,,,,,,,", " ,,,,,,,,, "]); tall(42, 21, BL[:3])
    blocks = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "other"}
    rails = {(x, y) for y in RAILS for x in range(RAIL_START, W)} | {(x, y + 1) for y in RAILS for x in range(RAIL_START, W)}
    poles = {(x, y + d) for (x, y) in POLES for d in (0, 1)}
    avoid = set(paths) | blocks | rails | poles
    c.forest(lambda x, y: x < 2 or x >= W - 2 or y < 2 or y >= H - 2, avoid, margin=0)
    for bl in [blob(6, 6, 5, 4), blob(6, 30, 5, 4), blob(42, 30, 4, 3), blob(10, 14, 2, 2.5), blob(46, 6, 2, 3),
               blob(22, 6, 6, 2), blob(18, 31, 6, 3), blob(31, 31, 5, 2.5), blob(12, 24, 2, 2)]:
        c.forest(bl, avoid | c.cliff_cells())
    # trilhos (leito fechado) com para-choque no comeco
    for ry in RAILS:
        c.put(RAIL_START, ry, ids["rail_end"], collision=1)
        for x in range(RAIL_START + 1, W):
            c.put(x, ry, ids["rail_h"], collision=1)
    for (x, y) in [(20, 22), (30, 31), (8, 25), (44, 15)]:
        if c.terrain[y][x] == "grass" and (x, y) not in avoid:
            c.put(x, y, 226, collision=1)
    return c


def flatten(bl):
    out = []
    for v in bl:
        if (v >> 12) in (5, 7, 9) and (v >> 10) & 3 == 0:
            v = (v & 0x0FFF) | (3 << 12)
        out.append(v)
    return out


def render(c, out):
    bl = c.build()
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "hollowtide_qa"))
    import render_map as R
    from PIL import Image
    ts = R.TilesetPair(c.primary, c.secondary)
    im = Image.new("RGB", (c.w * 16, c.h * 16))
    for i, v in enumerate(bl):
        im.paste(ts.metatile(v & 0x3FF), ((i % c.w) * 16, (i // c.w) * 16))
    im.save(out)
    return out


if __name__ == "__main__":
    c = compose()
    print("coesao:", c.check_cohesion())
    print(render(c, sys.argv[1]))
