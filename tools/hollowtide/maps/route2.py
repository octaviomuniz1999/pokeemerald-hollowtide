#!/usr/bin/env python3
"""Route 2 (Rota 02) — campo verde -> grama costeira -> enseada e praia -> Breezeport.

Bordas: topo liga a Harvestvale (trilha nas colunas 17-19, mesmo x da calcada de la); base liga a Breezeport
(calcamento nas colunas 18-21, mesmo x da rua de entrada da cidade). Tudo no nivel 3, exceto o mirante (plato).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 40, 48
TOP_PATH = (17, 19)
BOTTOM_ROAD = (18, 21)


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    # moldura de arvores (bordas leste/oeste e topo, com abertura da trilha)
    c.rect(0, 0, 1, H - 1, "tree")
    c.rect(W - 2, 0, W - 1, H - 1, "tree")
    c.rect(0, 0, 15, 1, "tree"); c.rect(22, 0, W - 1, 1, "tree")
    # --- campo (norte) ---
    c.rect(TOP_PATH[0], 0, TOP_PATH[1], 9, "sand")          # trilha descendo da Harvestvale
    c.rect(17, 8, 25, 10, "sand")                            # curva para leste
    c.rect(23, 10, 25, 17, "sand")
    c.rect(17, 16, 25, 18, "sand")                           # volta para o centro
    c.rect(17, 18, 19, 23, "sand")
    # manchas de mato alto com contorno irregular
    c.ascii(3, 3, [
        "  ,,,,,   ",
        " ,,,,,,,, ",
        ",,,,,,,,,,",
        ",,,,,,,,, ",
        " ,,,,,,,  ",
        "   ,,,    ",
    ])
    c.ascii(26, 2, [
        "   ,,,,   ",
        " ,,,,,,,, ",
        ",,,,,,,,,,",
        " ,,,,,,,, ",
        "  ,,,,,   ",
    ])
    c.ascii(4, 13, [
        "   ,,,,     ",
        " ,,,,,,,,,  ",
        ",,,,,,,,,,, ",
        " ,,,,,,,,,, ",
        "   ,,,,,,   ",
    ])
    # bosque escalonado (arvores 2x2 em posicoes pares) e arvores isoladas
    for (x, y) in [(28, 10), (30, 10), (32, 10), (34, 10), (30, 12), (32, 12), (34, 12), (32, 14), (34, 14)]:
        c.rect(x, y, x + 1, y + 1, "tree")
    for (x, y) in [(2, 2), (2, 4), (2, 6), (2, 8), (14, 10), (12, 2)]:
        c.rect(x, y, x + 1, y + 1, "tree")
    c.rect(14, 5, 15, 6, "flower"); c.rect(20, 12, 21, 13, "flower"); c.rect(30, 17, 33, 18, "flower")
    c.rect(8, 10, 9, 10, "flower"); c.rect(26, 8, 27, 8, "flower")
    # --- ladeiras de mao unica (atalho para o sul), abertura na trilha ---
    c.rect(2, 21, 15, 21, "ledge_s")
    c.rect(22, 21, W - 3, 21, "ledge_s")
    # --- grama costeira ---
    c.ascii(23, 23, [
        "  ,,,,,,    ",
        " ,,,,,,,,,  ",
        ",,,,,,,,,,, ",
        ",,,,,,,,,,,,",
        " ,,,,,,,,,, ",
        "   ,,,,,,   ",
    ])
    for (x, y) in [(26, 30), (28, 30), (30, 30), (32, 30), (34, 30), (24, 32), (26, 32), (28, 32), (30, 32), (32, 32), (34, 32)]:
        c.rect(x, y, x + 1, y + 1, "tree")
    c.rect(20, 27, 21, 27, "flower"); c.rect(14, 24, 15, 25, "flower")
    c.rect(17, 23, 19, 33, "sand")                           # trilha continua
    # mirante rochoso (plato) com escada
    c.rect(3, 24, 12, 30, "high")
    c.rect(5, 26, 10, 27, "flower")
    c.stairs(8, 30, width=2)
    # --- enseada e praia ---
    c.rect(0, 32, 16, 43, "sand")
    c.ascii(0, 34, [                                          # baia aberta para o oeste (some alem da borda)
        "~~~~~~~      ",
        "~~~~~~~~~    ",
        "~~~~~~~~~~   ",
        "~~~~~~~~~~   ",
        "~~~~~~~~~    ",
        "~~~~~~~~     ",
        "~~~~~~       ",
    ])
    c.rect(13, 33, 21, 39, "sand")
    c.stamp("lily_house_blue", 13, 33)                       # casa do pescador, de frente para a enseada
    # --- chegada a Breezeport: calcamento ---
    c.rect(BOTTOM_ROAD[0], 39, BOTTOM_ROAD[1], H - 1, "cobble")
    c.rect(2, 44, 17, H - 1, "tree"); c.rect(22, 35, W - 3, H - 1, "tree")
    c.lamp(17, 42, "grass")
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
