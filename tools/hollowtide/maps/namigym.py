#!/usr/bin/env python3
"""Ginasio da Nami ("As Eclusas") — arena aquatica a ceu aberto, 24x40 (General + Lilycove).

Tres piscinas atravessam a arena (sul -> norte). Cada uma tem uma eclusa: a alavanca ao lado drena um canal de
2 tiles que atravessa a piscina. A alavanca da piscina seguinte so e alcancavel depois de drenar a anterior,
entao a ordem e imposta pela agua. A lider fica no palco ao norte. compose(drained) devolve o estado com os
canais secos (o mapa salvo) ou cheios (aplicado por script ate cada eclusa abrir).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 24, 40
POOLS = [(27, 31), (17, 21), (8, 12)]          # linhas (topo, base) das piscinas: sul -> norte
CHANNEL = (11, 12)                             # colunas do canal drenado
LEVERS = [(4, 33), (19, 23), (4, 14)]          # alavancas (uma por piscina)
ENTRANCE = (11, 12)                            # porta (linha H-1)


def compose(drained=(True, True, True)):
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("sand")
    c.rect(0, 0, W - 1, 1, "tree"); c.rect(0, 0, 1, H - 1, "tree"); c.rect(W - 2, 0, W - 1, H - 1, "tree")
    c.rect(0, H - 1, W - 1, H - 1, "tree")
    c.rect(ENTRANCE[0], H - 1, ENTRANCE[1], H - 1, "cobble")
    for i, (y0, y1) in enumerate(POOLS):
        c.rect(2, y0, W - 3, y1, "pond")
        if drained[i]:
            c.rect(CHANNEL[0], y0, CHANNEL[1], y1, "cobble")
    # palco da lider (calcamento com canteiros)
    c.rect(6, 2, 17, 6, "cobble"); c.rect(3, 3, 4, 5, "flower"); c.rect(19, 3, 20, 5, "flower")
    # passarela central calcada entre as piscinas
    c.rect(CHANNEL[0], 7, CHANNEL[1], H - 2, "cobble")
    for i, (y0, y1) in enumerate(POOLS):
        if not drained[i]:
            c.rect(CHANNEL[0], y0, CHANNEL[1], y1, "pond")
    for (x, y) in LEVERS:
        c.put(x, y, 226, collision=1)        # pedra-base da alavanca (o sinal fica nela)
    for (x, y) in [(4, 24), (19, 15), (19, 34)]:
        c.lamp(x, y, floor="sand")
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
    full = len(sys.argv) > 2
    c = compose((not full,) * 3)
    print("coesao:", c.check_cohesion())
    print(render(c, sys.argv[1]))
