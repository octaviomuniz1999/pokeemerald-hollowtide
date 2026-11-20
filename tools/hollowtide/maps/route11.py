#!/usr/bin/env python3
"""Route 11 (Caminho da Liga) — Tidemouth -> Liga, 48x36 (General + Lilycove).

Sai de Tidemouth pelo oeste (linhas 20-21; Tidemouth y = Route 11 y + 8), corre pela praia sob as falesias e
sobe dois patamares ate a boca da caverna (o tunel que atravessa a serra ate a ilha da Liga). O mar fica ao
sul; mato alto nas encostas; um posto de guarda confere as 8 insignias antes da subida.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 48, 36
EAST = (20, 21)
OFFSET_TIDEMOUTH = 8           # Tidemouth y = Route 11 y + 8
CAVE = (9, 7)                  # boca da caverna (na parede sul do patamar alto, linhas 6-7)
STAIRS1 = 30                   # escada do patamar 5


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    # relevo: patamar 5 (linhas 0-15) e patamar 7 (canto noroeste, linhas 0-5) com bordas retas nas escadas
    for y in range(H):
        for x in range(W):
            if y <= 15 and x <= 40:
                c.level[y][x] = 5
            if y <= 5 and 2 <= x <= 22:
                c.level[y][x] = 7
    # mar e praia ao sul
    c.rect(0, 30, W - 1, H - 1, "sea")
    c.rect(0, 29, W - 1, 29, "shallow")
    c.rect(0, 25, W - 1, 28, "sand")
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    S = lambda L, x: max(y for y in range(H) if c.level[y][x] >= L)
    path(STAIRS1, EAST[0], W - 1, EAST[1])                        # estrada que vem de Tidemouth
    path(STAIRS1, S(5, STAIRS1) + 2, STAIRS1 + 1, EAST[1]); c.stairs(STAIRS1, S(5, STAIRS1), 2)
    path(CAVE[0], 10, STAIRS1 + 1, 11)                              # no patamar 5, para oeste
    path(STAIRS1, 10, STAIRS1 + 1, S(5, STAIRS1) - 1)
    path(CAVE[0], CAVE[1] + 1, CAVE[0] + 1, 11)                      # ate o pe da parede da serra
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
    tall(20, 17, [" ,,,,,,", ",,,,,,,", " ,,,,, "]); tall(34, 4, [",,,,,", ",,,,,", " ,,, "]); tall(4, 9, [",,,,,,", ",,,,,,"])
    water = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] in ("sea", "shallow", "sand")}
    avoid = set(paths) | water | c.cliff_cells()
    c.forest(lambda x, y: (x < 2 or y < 2 or x >= W - 2) and y < 25, avoid, margin=0)
    for bl in [blob(40, 9, 4, 3), blob(6, 18, 4, 3), blob(26, 2, 3, 1.5), blob(44, 16, 2, 2)]:
        c.forest(bl, avoid)
    for (x, y) in [(12, 22), (38, 23), (24, 13)]:
        if c.terrain[y][x] == "grass":
            c.put(x, y, 226, collision=1)
    c.put(CAVE[0], CAVE[1], 0xA7, collision=0)                      # boca da caverna na parede do patamar alto
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
