#!/usr/bin/env python3
"""Tidemouth (Cidade das Mares, "A Mare Anormal") — 64x48, General + Lilycove.

Cidade portuaria e turistica: entrada norte pela Route 10 (colunas 30-31; Route 10 x = Tidemouth x - 12),
avenida calcada, hoteis (motel e o grande hotel da orla), canais rasos que cortam a cidade, parque aquatico
(piscinas), Centro Pokemon, Mart, casas, o ginasio da Nami (o grande predio sobre o canal) e, ao sul, o porto
com o terminal que leva ao Complexo Oceanico da Team Palm. O mar ocupa a borda sul e o leste.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 64, 48
NORTH = (30, 31)
OFFSET_ROUTE10 = -12          # Route 10 comeca 12 colunas a direita do inicio de Tidemouth
AVENUE = (16, 17)
SHORE = 38                    # da linha 38 para baixo: praia, cais e mar
SEAM = 7                      # linhas 0-6 so primario (a Route 10 enxerga)
BUILDINGS = [
    ("lily_dept_store", 40, 8, "hotel"),        # grande hotel da orla (com cobertura)
    ("lily_motel", 6, 9, "motel"),
    ("lily_pokecenter", 20, 11, "pc"),
    ("gen_mart", 26, 12, "mart"),
    ("lily_museum", 14, 19, "gym"),             # ginasio da Nami (predio grande, piscinas internas)
    ("lily_house_blue", 4, 24, "house_1"),
    ("lily_house_blue", 44, 22, "house_2"),
    ("lily_harbor", 30, 31, "terminal"),        # terminal do porto -> Complexo Oceanico
]
DOOR_OFF = {"lily_dept_store": (4, 8), "lily_motel": (1, 4), "lily_pokecenter": (1, 3), "gen_mart": (1, 2),
            "lily_museum": (4, 5), "lily_house_blue": (1, 3), "lily_harbor": (3, 5)}
LAMPS = [(12, 18), (26, 18), (36, 18), (50, 18), (30, 24), (44, 37)]


def door(label):
    for (name, x, y, lab) in BUILDINGS:
        if lab == label:
            dx, dy = DOOR_OFF[name]
            ex = 2 if name == "lily_dept_store" else 0          # o hotel ganha a cobertura de 2 linhas em cima
            return x + dx, y + dy + ex
    raise KeyError(label)


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    # mar ao sul e a leste, praia e cais
    c.rect(0, SHORE + 3, W - 1, H - 1, "sea")
    c.rect(56, 0, W - 1, H - 1, "sea")
    c.rect(0, SHORE, 55, SHORE + 2, "sand")
    c.rect(54, 0, 55, SHORE + 2, "sand")
    c.rect(0, SHORE + 3, 55, SHORE + 3, "shallow")
    # canal que corta a cidade (agua rasa, atravessavel por ponte de areia)
    c.rect(40, 19, 42, SHORE - 1, "pond")
    # parque aquatico (piscinas com borda de areia)
    c.rect(44, 28, 53, 36, "sand"); c.rect(45, 29, 48, 32, "pond"); c.rect(50, 30, 52, 35, "pond")
    paths = []
    def path(x0, y0, x1, y1, cls="cobble"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(NORTH[0], 0, NORTH[1], SEAM - 1, "sand")              # estrada de terra (a Route 10 enxerga)
    path(NORTH[0], SEAM, NORTH[1], AVENUE[1])
    path(2, AVENUE[0], 53, AVENUE[1])
    path(0, 28, 53, 29)                                          # rua sul: segue para oeste (Route 11)
    for (name, x, y, label) in BUILDINGS:
        if name == "lily_dept_store":
            c.dept_store(x, y)
        else:
            c.stamp(name, x, y)
    for (name, x, y, _) in BUILDINGS:                         # o carimbo do pavilhao traz cantos da Lilycove
        if name == "lily_museum":
            for (dx, dy) in ((0, 0), (1, 0), (8, 0), (9, 0), (0, 1), (1, 1), (8, 1), (9, 1)):
                c.put(x + dx, y + dy, 1, collision=0)
                c.terrain[y + dy][x + dx] = "grass"
    for label in ("motel", "pc", "mart", "hotel"):
        x, y = door(label); path(x, y + 1, x, AVENUE[0] - 1)
    gx, gy = door("gym"); path(gx, gy + 4, gx + 1, 27)             # da escada do ginasio a rua
    for label in ("house_1", "house_2"):
        x, y = door(label); path(x, y + 1, x, 27)
    x, y = door("terminal"); path(x, y + 1, x, SHORE)
    for (x, y) in LAMPS:
        c.lamp(x, y, floor="grass")
    c.rect(8, 33, 14, 35, "flower"); c.rect(22, 33, 26, 35, "flower")
    water = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] in ("sea", "shallow", "pond", "sand")}
    blocks = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "other"}
    lamps = {(x, y + d) for (x, y) in LAMPS for d in (0, 1)}
    avoid = set(paths) | water | blocks | lamps
    c.forest(lambda x, y: (y < 2 or x < 2) and y < SHORE, avoid, margin=0)
    for bl in [blob(10, 4, 7, 2.5), blob(46, 3, 6, 2), blob(20, 4, 4, 2), blob(3, 32, 1.5, 4)]:
        c.forest(bl, avoid)
    return c


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
