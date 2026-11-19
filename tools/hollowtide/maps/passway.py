#!/usr/bin/env python3
"""Passway Village (Vila da Passagem, "A Montanha que Espera") — 36x32, General + Lavaridge.

Vila de pouso de viajantes ao pe da montanha: fonte termal (posto de descanso), estalagens, Centro Pokemon,
Mart, a casa da anciã e o mural. Ao norte, a escadaria de pedra para o cume sobe um patamar e esta
interditada (so abre no pos-jogo). Mirante a oeste. Entrada sul pela Route 8 (colunas 16-17;
Route 8 x = Passway x + 2) e saida leste (linhas 18-19) para a Route 9, fechada por enquanto.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 36, 32
SOUTH = (16, 17)
EAST = (18, 19)
OFFSET_ROUTE8 = -2        # conexao da Route 8 (up): Passway comeca 2 colunas a esquerda da Route 8... ver instalador
STAIRWAY = (17, 18)       # escadaria interditada para o cume
SEAM = 25                 # da linha 25 ao fim so primario (a Route 8 enxerga 7 linhas)
BUILDINGS = [
    ("lav_spring", 25, 4, "spring"),
    ("lav_pokecenter", 4, 13, "pc"),
    ("lav_mart", 10, 13, "mart"),
    ("lav_house", 22, 12, "inn"),
    ("lav_house2", 28, 12, "elder"),
    ("lav_house", 4, 20, "house"),
]
DOOR_OFF = {"lav_pokecenter": (1, 3), "lav_mart": (1, 3), "lav_house": (1, 3), "lav_house2": (1, 3), "lav_spring": (2, 4)}


def door(label):
    for (name, x, y, lab) in BUILDINGS:
        if lab == label:
            dx, dy = DOOR_OFF[name]
            return x + dx, y + dy
    raise KeyError(label)


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    # patamar da escadaria (norte) — a montanha comeca aqui
    for y in range(0, 8):
        for x in range(10, 26):
            c.level[y][x] = 5
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(SOUTH[0], EAST[1], SOUTH[1], H - 1)                 # da Route 8 ate a praca
    path(2, EAST[0], W - 1, EAST[1])                         # rua principal (leste -> Route 9)
    path(STAIRWAY[0], 10, STAIRWAY[1], EAST[0])              # ate o pe da escadaria
    c.stairs(STAIRWAY[0], 7, 2)
    path(STAIRWAY[0], 0, STAIRWAY[1], 6)                     # escadaria continua para o cume (interditada)
    for (name, x, y, label) in BUILDINGS:
        c.stamp(name, x, y)
    for label in ("pc", "mart", "inn", "elder"):
        x, y = door(label); path(x, y + 1, x, EAST[0] - 1)
    x, y = door("house"); path(x, y + 1, x, 25); path(x, 25, SOUTH[0] - 1, 25)
    sx, sy = door("spring"); path(sx, sy + 1, sx + 1, 11); path(STAIRWAY[1] + 1, 10, sx + 1, 11)
    path(2, 9, 7, 10)                                        # mirante oeste
    c.rect(20, 22, 27, 23, "flower"); c.rect(9, 9, 9, 10, "flower")
    stair = set()
    for (x, y) in c.stair_cols:
        stair |= {(x, y), (x, y + 1)}
    avoid = set(paths) | stair | {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "other"}
    c.forest(lambda x, y: x < 2 or y < 2 or y >= H - 2 or (x >= W - 2 and not EAST[0] - 1 <= y <= EAST[1] + 1), avoid, margin=0)
    for bl in [blob(5, 4, 4, 3), blob(31, 25, 4, 3), blob(10, 28, 4, 2), blob(24, 28, 4, 2), blob(32, 12, 2, 3)]:
        c.forest(bl, avoid | c.cliff_cells())
    for (x, y) in [(12, 4), (22, 3), (14, 2)]:
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
