#!/usr/bin/env python3
"""Storm Mountain — o cume, 24x22, General + Lavaridge.

A ultima escadaria da crista (crista x 17-18) termina aqui (cume x = crista x - 6). O cume e um pico de pedra
(patamar 5) cercado de rocha solta, com uma escadinha ao sul; o antigo Campeao esta no meio do pico, na
tempestade. Sem treinadores no caminho (roteiro, sec. 17).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 24, 22
SOUTH = (11, 12)
OFFSET_RIDGE = 6              # cume x = crista x - 6
TAVINHO = (11, 6)
DOGE_IN = (12, 15)            # por onde o Doge chega depois da luta (sobe a escadinha)


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    for y in range(H):
        for x in range(W):
            if 3 <= y <= 12 and 4 <= x <= 19:
                c.level[y][x] = 5
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(SOUTH[0], 14, SOUTH[1], H - 1)
    c.stairs(SOUTH[0], 12, 2)
    path(SOUTH[0], 8, SOUTH[1], 11)
    # topo do pico: pedra solta em volta do antigo Campeao
    for (x0, y0, rows) in [(7, 4, ["  ssssssss", " ssssssssss", "ssssssssssss", " ssssssssss", "  ssssssss"])]:
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch == "s" and c.terrain[y0 + dy][x0 + dx] == "grass":
                    c.terrain[y0 + dy][x0 + dx] = "sand"
    stair = set()
    for (x, y) in c.stair_cols:
        stair |= {(x, y), (x, y + 1)}
    stair |= c.cliff_cells()
    for (x0, y0, rows) in [(1, 13, ["sss", " ss"]), (19, 17, ["ss", "sss"]), (16, 0, ["sss"]), (2, 4, ["ss", "ss"])]:
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch == "s" and c.terrain[y0 + dy][x0 + dx] == "grass" and (x0 + dx, y0 + dy) not in stair:
                    c.terrain[y0 + dy][x0 + dx] = "sand"
    for (x, y) in [(5, 5), (18, 4), (6, 10), (17, 10), (2, 16), (21, 15), (3, 2), (20, 1), (8, 18), (16, 19), (1, 9),
                   (22, 8), (14, 17), (5, 20), (19, 12), (4, 8)]:
        if c.terrain[y][x] == "grass" and (x, y) not in stair and (x, y) not in paths:
            c.put(x, y, 226, collision=1, elevation=c.level[y][x] if c.level[y][x] > 3 else 3)
    return c


def flatten(bl):
    out = []
    for v in bl:
        if (v >> 12) in (5, 7, 9) and (v >> 10) & 3 == 0:
            v = (v & 0x0FFF) | (3 << 12)
        out.append(v)
    return out


if __name__ == "__main__":
    import storm_trail
    c = compose()
    print("coesao:", c.check_cohesion())
    print(storm_trail.render(c, sys.argv[1]))
