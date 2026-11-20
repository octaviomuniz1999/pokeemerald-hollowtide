#!/usr/bin/env python3
"""Route 14 (Atlas Lookout) — rota opcional a oeste da Passway Village, 40x32 (General + Lavaridge, como a Passway).

A estrada principal da Passway (linhas 18-19, offset 0) segue para o oeste pela encosta. Ao norte da estrada, um
patamar alto com escada: no alto, o mirante — uma pedra de marco e uma placa que lembra a historia do guardiao fiel
que a anciã da Passway conta. Embaixo, campos de mato alto dos dois lados da estrada e um desvio ao sul ate um
bosque. Pokemon do canone (POKEDEX_LUNIA): Houndour, Absol (raro), Lillipup/Herdier/Stoutland, Rockruff.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 40, 32
EAST = (18, 19)               # entrada leste (linhas) = estrada principal da Passway (offset 0)
OFFSET_PASSWAY = 0
HILL = [(6, 3, 17, 4), (4, 5, 24, 13)]   # patamar do mirante (degraus de 2 tiles; borda sul reta)
STAIRS = 14                   # escada (2 colunas)
MARKER = (8, 6)               # pedra de marco do mirante


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    for (x0, y0, x1, y1) in HILL:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c.level[y][x] = 5
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    S = lambda x: max(y for y in range(H) if c.level[y][x] >= 5)
    path(6, EAST[0], W - 1, EAST[1])                   # estrada
    path(STAIRS, S(STAIRS) + 2, STAIRS + 1, EAST[0])   # da estrada a escada
    c.stairs(STAIRS, S(STAIRS), 2)
    for (x, y) in c.stair_cols:
        paths.extend([(x, y), (x, y + 1)])
    path(STAIRS, 7, STAIRS + 1, S(STAIRS) - 1)          # no alto, ate o mirante
    path(8, 7, STAIRS + 1, 8)
    path(24, EAST[1] + 1, 25, 26); path(18, 25, 25, 26)   # desvio ao sul
    c.rect(6, 4, 11, 5, "flower")                       # canteiro na beira do mirante
    hilltop = {(x, y) for y in range(H) for x in range(W) if c.level[y][x] >= 5}
    avoid = set(paths)
    c.forest(lambda x, y: x < 2 or x >= W - 2 and not EAST[0] - 1 <= y <= EAST[1] + 1 or y < 2 or y >= H - 2,
             avoid, margin=0)
    for b in [blob(32, 6, 6, 4), blob(30, 13, 3, 2), blob(6, 26, 4, 3), blob(12, 29, 4, 2), blob(33, 27, 5, 3),
              blob(21, 29, 3, 1.5)]:
        c.forest(b, avoid | hilltop)
    for b in [blob(20, 9, 3, 3), blob(6, 11, 2, 2)]:          # bosquetes no alto do patamar
        c.forest(b, avoid)
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass" and c.level[y][x] == 3:
                    c.terrain[y][x] = "tall"
    tall(26, 14, [" ,,,,,,", ",,,,,,,,", ",,,,,,,"])      # ao norte da estrada, a leste do patamar
    tall(8, 21, [",,,,,,,", ",,,,,,,,", " ,,,,,"])        # ao sul da estrada, a oeste
    tall(27, 21, [",,,,,", ",,,,,,", ",,,,"])            # ao sul da estrada, a leste
    for (x, y) in [(17, 8), (18, 8), (17, 9), (16, 10), (17, 10), (18, 10)]:   # no alto do patamar
        if c.terrain[y][x] == "grass":
            c.terrain[y][x] = "tall"
    c.rect(4, 15, 6, 16, "flower"); c.rect(20, 15, 22, 15, "flower")
    for (x, y) in [(3, 20), (36, 16), (10, 15)]:
        if c.terrain[y][x] == "grass":
            c.put(x, y, 226, collision=1)
    c.put(*MARKER, 226, collision=1)
    return c


def flatten(bl):
    """Patamar so visual (elevacao 3 nos tiles andaveis), como na Route 7."""
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
