#!/usr/bin/env python3
"""Tradepost (Entreposto Comercial "Duas Margens") — 40x32, General + Rustboro (continua a ferrovia da Route 4).

Sem ginasio. Entrada oeste pela estrada das caravanas (linhas 16-17, offset 0 com a Route 4); estacao no
fim da linha ferrea (fechada ate o capitulo do Hoc); Centro Pokemon e Mart junto a entrada; praca do mercado
com a fonte; Associacao de Mercadores ao sul; canal com ponte de tabuado para o cais leste, onde fica o
quiosque da Team Palm; saida norte para a Route 5 (Pillarton) ainda fechada.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas, extract

W, H = 40, 32
ROAD = (16, 17)
RAILS = (2, 8)
CANAL = (29, 32)
BRIDGE = (836, 844, 845)
NORTH_EXIT = (26, 27)
BUILDINGS = [
    ("rb_office_long", 10, 2, "station"),
    ("rb_house_grey", 20, 3, "house_n"),
    ("rb_pokecenter", 12, 11, "pc"),
    ("rb_mart", 19, 11, "mart"),
    ("rb_office_long", 11, 23, "association"),
    ("rb_house_grey", 24, 24, "house_s"),
    ("rb_office_small", 33, 3, "palm_kiosk"),
]
LAMPS = [(11, 15), (24, 15), (28, 18), (20, 22), (28, 22), (9, 21)]


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Rustboro")
    c.fill("plaza")
    ids = json.load(open(os.path.join(os.path.dirname(__file__), "..", "mapgen", "custom_ids.json")))["rustboro"]
    # moldura
    c.rect(0, 0, W - 1, 1, "tree"); c.rect(0, H - 2, W - 1, H - 1, "tree"); c.rect(W - 2, 0, W - 1, H - 1, "tree")
    c.rect(NORTH_EXIT[0], 0, NORTH_EXIT[1], 1, "tree")          # saida norte (Route 5) fechada por ora
    # corredor ferroviario (inacessivel): grama entre as linhas, cerca viva e mata fechada embaixo
    c.rect(0, 3, 9, 7, "grass"); c.rect(0, 9, 9, 9, "dense"); c.rect(0, 10, 9, 11, "tree")
    c.rect(0, 12, 1, 15, "tree"); c.rect(0, 18, 1, 29, "tree")
    # entrada oeste: estrada vira avenida
    c.rect(0, ROAD[0], 1, ROAD[1], "sand")
    c.rect(2, ROAD[0], 29, ROAD[1], "road")
    c.rect(NORTH_EXIT[0], 2, NORTH_EXIT[1], 15, "road")
    # canal e cais leste
    c.rect(CANAL[0], 2, CANAL[1], H - 1, "pond")
    c.rect(CANAL[1] + 1, 2, W - 3, H - 3, "plaza")
    # praca do mercado: jardins em volta da fonte e canteiros das bancas
    c.rect(19, 18, 27, 23, "grass"); c.rect(20, 18, 26, 18, "flower"); c.rect(20, 23, 26, 23, "flower")
    c.rect(3, 19, 7, 21, "grass"); c.rect(4, 20, 6, 20, "flower")
    c.rect(3, 24, 8, 27, "grass"); c.small_tree(4, 25)
    for (name, x, y, _) in BUILDINGS:
        c.stamp(name, x, y)
    c.stamp("rb_fountain", 22, 19)
    for (x, y) in LAMPS:
        c.stamp("rb_lamp", x, y)
    for ry in RAILS:                                            # trilhos chegando da Route 4 ate a estacao
        for x in range(0, 9):
            c.put(x, ry, ids["rail_h"], collision=1)
        c.put(9, ry, ids["rail_end_e"], collision=1)
    for x in range(CANAL[0], CANAL[1] + 1):                     # ponte de tabuado para o cais
        c.put(x, 20, BRIDGE[0], collision=0)
        c.put(x, 21, BRIDGE[1], collision=0)
        c.put(x, 22, BRIDGE[2], collision=1)
    c.rect(35, 25, 37, 28, "grass"); c.small_tree(36, 26)
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
