#!/usr/bin/env python3
"""Storm Mountain — a crista (setores altos), 36x46, General + Lavaridge.

Continua a trilha pelo norte (trilha x 8-9 = crista x 8-9; mesmo x). No pe da crista, o posto da Joy: a cabana
de campanha da Liga com a enfermeira na porta (cura e ponto de preparo). Dali o caminho sobe por dois patamares de
pedra solta ate a ultima escadaria, longa e reta, que leva ao cume (parte 3). A Cynthia esta no pe da ultima
escadaria e nao deixa ninguem passar.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 36, 46
SOUTH = (8, 9)
OFFSET_TRAIL = 0              # crista x = trilha x
CABIN = (12, 34)              # lav_house (4x4): porta em (13, 37)
SIGN = (16, 37)              # placa do posto (a Joy fica dentro da cabana)
LONG_STAIR = 11              # a ultima escadaria: linhas 0..11, na garganta entre paredes do patamar 9
STAIR_X = (17, 18)            # a ultima escadaria
CYNTHIA = (18, 13)           # na boca da garganta da ultima escadaria
GAP_ROCK = (16, 13)          # fecha o lado esquerdo da boca (o direito e onde a Cynthia se afasta)
NORTH = STAIR_X


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    for y in range(H):
        for x in range(W):
            if y <= 31:
                c.level[y][x] = 5
            if y <= 19:
                c.level[y][x] = 7
            if y <= LONG_STAIR and not (STAIR_X[0] <= x <= STAIR_X[1]):
                c.level[y][x] = 9
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    S = lambda L, x: max(y for y in range(H) if c.level[y][x] >= L)
    # da trilha ate o posto da Joy e a escada do patamar 5
    path(SOUTH[0], 39, SOUTH[1], H - 1)
    path(SOUTH[0], 38, 19, 39)
    path(18, S(5, 18) + 2, 19, 37); c.stairs(18, S(5, 18), 2)
    # patamar 5: pedra solta, o caminho vai ate o pe do patamar 7
    path(18, 24, 19, S(5, 18) - 1)
    path(STAIR_X[0], S(7, STAIR_X[0]) + 2, STAIR_X[1], 25); c.stairs(STAIR_X[0], S(7, STAIR_X[0]), 2)
    # patamar 7 e a ultima escadaria (o corredor entre as rochas do patamar 9 ate o cume)
    path(STAIR_X[0], 0, STAIR_X[1], S(7, STAIR_X[0]) - 1)
    c.stamp("lav_house", *CABIN)
    for y in range(0, LONG_STAIR + 1):           # a ultima escadaria, longa e reta
        for x in STAIR_X:
            c.put(x, y, 175, collision=0, elevation=0)
    stair = set()
    for (x, y) in c.stair_cols:
        stair |= {(x, y), (x, y + 1)}
    paths.extend(stair)
    # pedra solta e mato ralo
    for (x0, y0, rows) in [(22, 24, ["sss", "ssss", " ss"]), (9, 18, ["ss", "sss"]), (26, 12, ["sss", " ss"]),
                           (6, 26, ["sss", "ss"]), (24, 41, ["ss", "sss"]), (11, 10, ["sss"])]:
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch == "s" and c.terrain[y0 + dy][x0 + dx] == "grass":
                    c.terrain[y0 + dy][x0 + dx] = "sand"
    for (x0, y0, rows) in [(24, 33, [" ,,,,", ",,,,,,", ",,,,,"]), (8, 22, [",,,,", ",,,,,", " ,,,"]), (23, 9, [",,,,,", " ,,,"])]:
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch != " " and c.terrain[y0 + dy][x0 + dx] == "grass":
                    c.terrain[y0 + dy][x0 + dx] = "tall"
    c.put(*GAP_ROCK, 226, collision=1, elevation=7)
    keep = {SIGN, CYNTHIA, (CYNTHIA[0] + 1, CYNTHIA[1]), GAP_ROCK, (CABIN[0] + 1, CABIN[1] + 4)}
    avoid = set(paths) | stair | c.cliff_cells() | keep | {(x, y) for x in range(CABIN[0] - 1, CABIN[0] + 5)
                                                           for y in range(CABIN[1] - 1, CABIN[1] + 6)}
    c.forest(lambda x, y: x < 3 or x >= W - 3, avoid, margin=0)
    for bl in [blob(4, 40, 2, 4), blob(30, 40, 3, 3), blob(28, 21, 4, 3), blob(5, 12, 3, 3), blob(30, 3, 3, 2)]:
        c.forest(bl, avoid)
    for (x, y) in [(11, 42), (20, 41), (22, 27), (12, 25), (25, 18), (14, 13), (22, 11), (27, 27), (10, 31), (21, 33),
                   (13, 20), (24, 15), (8, 14)]:
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


if __name__ == "__main__":
    import storm_trail
    c = compose()
    print("coesao:", c.check_cohesion())
    print(storm_trail.render(c, sys.argv[1]))
