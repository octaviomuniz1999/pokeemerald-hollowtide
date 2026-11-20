#!/usr/bin/env python3
"""Storm Mountain — trilha (Montanha da tempestade, setores baixos), 40x50, General + Lavaridge.

Sobe da escadaria da Passway (Passway x 17-18 = trilha x 19-20; trilha x = Passway x + 2) em tres patamares:
- encosta inferior (patamar 5): pedras, mato alto, o Steven perto do caminho;
- o desfiladeiro (patamar 7): o caminho entra num corredor entre paredes do patamar 9; o Leon esta no meio;
- o alto (patamar 9): a trilha segue para o norte (posto da Joy e a ultima escadaria entram na parte 2).
Mesmo secundario da Passway (Lavaridge), entao a emenda nao precisa de faixa so de primario.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 40, 50
SOUTH = (19, 20)
OFFSET_PASSWAY = 2            # trilha x = Passway x + 2
GORGE = (7, 11)               # colunas do corredor do desfiladeiro (patamar 7 entre paredes do patamar 9)
STEVEN = (22, 38)
LEON = (9, 19)
NORTH = (8, 9)                # a trilha sai pelo norte (parte 2)


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    for y in range(H):
        for x in range(W):
            if y <= 43:
                c.level[y][x] = 5
            if y <= 29:
                c.level[y][x] = 7
            if y <= 13 or (y <= 22 and not (GORGE[0] <= x <= GORGE[1])):
                c.level[y][x] = 9
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    S = lambda L, x: max(y for y in range(H) if c.level[y][x] >= L)
    # da Passway ate a escada do patamar 5
    path(SOUTH[0], S(5, SOUTH[0]) + 2, SOUTH[1], H - 1); c.stairs(SOUTH[0], S(5, SOUTH[0]), 2)
    # patamar 5: sobe e vira para oeste
    path(SOUTH[0], 35, SOUTH[1], S(5, SOUTH[0]) - 1)
    path(GORGE[0] + 1, 34, SOUTH[1], 35)
    path(GORGE[0] + 1, S(7, GORGE[0] + 1) + 2, GORGE[0] + 2, 33); c.stairs(GORGE[0] + 1, S(7, GORGE[0] + 1), 2)
    # patamar 7: o desfiladeiro (corredor entre as paredes do patamar 9)
    path(GORGE[0] + 1, S(9, GORGE[0] + 1) + 2, GORGE[0] + 2, S(7, GORGE[0] + 1) - 1)
    c.stairs(NORTH[0], S(9, NORTH[0]), 2)
    # patamar 9: a trilha segue para o norte
    path(NORTH[0], 0, NORTH[1], S(9, NORTH[0]) - 1)
    stair = set()
    for (x, y) in c.stair_cols:
        stair |= {(x, y), (x, y + 1)}
    paths.extend(stair)
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = "tall"
    tall(24, 40, [" ,,,,,", ",,,,,,,", ",,,,,,", " ,,,, "])        # encosta inferior (leste)
    tall(12, 37, [",,,,,", ",,,,,,", " ,,,,"])                     # encosta inferior (oeste)
    tall(14, 25, [",,,,,,,,", " ,,,,,,,", "  ,,,,"])                          # boca do desfiladeiro
    tall(16, 5, [" ,,,,,,", ",,,,,,,,", ",,,,,,,", "  ,,,, "])       # alto
    # chao de pedra solta (terra) em volta das rochas: a montanha nao e um gramado
    for (x0, y0, rows) in [(26, 31, ["sss", "ssss", " ss"]), (14, 45, ["ss", "sss"]), (22, 2, ["ssss", "sssss", " sss"]),
                           (12, 9, ["sss", "ss"]), (33, 46, ["sss", " ss"]), (16, 30, ["ss"])]:
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch == "s" and c.terrain[y0 + dy][x0 + dx] == "grass":
                    c.terrain[y0 + dy][x0 + dx] = "sand"
    avoid = set(paths) | stair | c.cliff_cells() | {STEVEN, (STEVEN[0] + 1, STEVEN[1]), LEON, (LEON[0], LEON[1] - 1)}
    c.forest(lambda x, y: x < 3 or x >= W - 3, avoid, margin=0)
    c.forest(lambda x, y: (x >= GORGE[1] + 3 and 15 <= y <= 20) or (x <= GORGE[0] - 2 and 15 <= y <= 20), avoid)   # cristas da garganta
    for bl in [blob(32, 33, 5, 2.5), blob(4, 40, 3, 4), blob(30, 8, 6, 3), blob(3, 7, 2, 4), blob(33, 26, 4, 2), blob(20, 10, 3, 2)]:
        c.forest(bl, avoid)
    for (x, y) in [(23, 35), (15, 42), (26, 46), (13, 31), (21, 31), (24, 3), (13, 10), (30, 45), (27, 32), (15, 46),
                   (34, 47), (23, 2), (26, 4), (14, 10), (19, 12), (28, 29), (35, 40), (6, 31), (17, 30), (24, 26), (27, 25), (12, 2), (34, 3), (15, 13)]:
        if c.terrain[y][x] == "grass" and (x, y) not in avoid:
            c.put(x, y, 226, collision=1, elevation=c.level[y][x] if c.level[y][x] > 3 else 3)
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
