#!/usr/bin/env python3
"""Voltara ("O Sinal da Tempestade") — 60x44, General + Rustboro.

Cidade da energia e da ferrovia: os trilhos chegam pelo oeste (linhas 8 e 10, continuando os da Route 9) e
terminam na estacao, que fica de frente para a avenida; o Centro de Dados da Team Palm (predio grande) a
leste; o ginasio do Hoc ao sul; Centro Pokemon, Mart, apartamentos e casas; parque a sudeste. Entrada oeste
pela Route 9 (linhas 18-19, offset 0); saida sul (colunas 30-31) para a Route 10, fechada por enquanto.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 60, 44
WEST = (18, 19)
SOUTH = (30, 31)
RAILS = (8, 10)
RAIL_END = 30                    # para-choque leste dos trilhos (dentro da estacao)
AVENUE = (18, 19)
BUILDINGS = [
    ("rb_office_long", 22, 12, "station"),       # estacao de Voltara (porta na avenida)
    ("rb_devon", 44, 8, "datacenter"),           # Centro de Dados da Team Palm
    ("rb_gym", 38, 26, "gym"),                   # ginasio do Hoc
    ("rb_pokecenter", 8, 22, "pc"),
    ("rb_mart", 14, 22, "mart"),
    ("rb_apartment", 2, 30, "flat"),
    ("rb_house_grey", 14, 31, "house_1"),
    ("rb_house_grey", 21, 31, "house_2"),
    ("rb_office_six", 34, 2, "office"),
    ("rb_tower", 53, 22, "tower"),
    ("rb_office_mid", 22, 2, "office_2"),
]
DOOR_OFF = {"rb_house_grey": (2, 4), "rb_office_long": (4, 5), "rb_pokecenter": (1, 3), "rb_mart": (1, 3),
            "rb_apartment": (2, 8), "rb_gym": (3, 4), "rb_devon": (4, 8), "rb_office_six": (2, 4), "rb_tower": (1, 7), "rb_office_mid": (3, 4)}
LAMPS = [(6, 16), (20, 16), (36, 16), (52, 20), (29, 23), (36, 23)]


def door(label):
    for (name, x, y, lab) in BUILDINGS:
        if lab == label:
            dx, dy = DOOR_OFF[name]
            return x + dx, y + dy
    raise KeyError(label)


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Rustboro")
    c.fill("plaza")
    ids = json.load(open(os.path.join(os.path.dirname(__file__), "..", "mapgen", "custom_ids.json")))["rustboro"]
    # moldura de mata e parque a sudeste
    c.rect(0, 0, W - 1, 1, "tree"); c.rect(0, H - 2, W - 1, H - 1, "tree")
    c.rect(0, 0, 1, H - 1, "tree"); c.rect(W - 2, 0, W - 1, H - 1, "tree")
    c.rect(2, 2, 21, 6, "grass")                                   # gramado ao norte dos trilhos (oeste)
    c.rect(44, 32, W - 3, H - 3, "grass")                         # parque
    # avenida, ruas e saidas
    c.rect(0, AVENUE[0], W - 3, AVENUE[1], "road")
    c.rect(SOUTH[0], AVENUE[1], SOUTH[1], H - 1, "road")
    c.rect(2, 28, 43, 29, "road")
    c.rect(0, WEST[0], 1, WEST[1], "road")
    c.rect(0, 7, 1, 11, "plaza")                                   # os trilhos da Route 9 entram pela moldura
    # canteiros (grama com flores) na praca
    for (x0, y0, x1, y1) in [(22, 21, 27, 25), (42, 21, 47, 24), (4, 11, 9, 14), (34, 32, 39, 36)]:
        c.rect(x0, y0, x1, y1, "grass"); c.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, "flower")
    for (name, x, y, _) in BUILDINGS:
        c.stamp(name, x, y)
    for (x, y) in LAMPS:
        c.stamp("rb_lamp", x, y)
    # trilhos (leito fechado), para-choque dentro da estacao
    for ry in RAILS:
        for x in range(0, RAIL_END):
            c.put(x, ry, ids["rail_h"], collision=1)
        c.put(RAIL_END, ry, ids["rail_end_e"], collision=1)
    # parque: arvores e flores; mata da moldura
    c.forest(lambda x, y: x >= 46 and y >= 34 and not (48 <= x <= 53 and 36 <= y <= 39), set())
    c.rect(48, 36, 53, 39, "flower")
    c.forest(lambda x, y: x < 20 and 2 <= y <= 6 and not (x < 8), set())
    c.rect(38, 8, 42, 12, "grass"); c.small_tree(39, 9); c.rect(41, 11, 41, 11, "flower")   # arvore em canteiro
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
