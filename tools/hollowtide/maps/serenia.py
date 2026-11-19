#!/usr/bin/env python3
"""Serenia (Vila Serenia, "O Jardim das Lembrancas") — 44x40, General + Lavaridge.

Vila de santuario: a fonte sagrada ao norte (o altar dos fragmentos), trilha de pedras ate ela (onde ficam as
tres ilusoes), Centro Pokemon e Mart a oeste, ginasio da Jade a leste, casas ao sul, bosques fechados e
jardins de pedra. Entrada oeste pela Route 6 (linhas 20-21, offset 0).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 44, 40
ROAD = (20, 21)
SHRINE_PATH = (20, 21)        # colunas da trilha ate a fonte
ILLUSIONS = [(20, 16), (20, 13), (20, 10)]   # cada ilusao ocupa (x, y) e (x + 1, y)
BUILDINGS = [
    ("lav_spring", 18, 2, "spring"),
    ("lav_pokecenter", 5, 14, "pc"),
    ("lav_mart", 11, 14, "mart"),
    ("lav_gym", 30, 14, "gym"),
    ("lav_house", 6, 27, "house_1"),
    ("lav_house2", 14, 27, "house_2"),
    ("lav_house", 30, 27, "house_3"),
]


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    paths = []
    def path(x0, y0, x1, y1):
        c.rect(x0, y0, x1, y1, "sand")
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(0, ROAD[0], W - 3, ROAD[1])                                   # rua principal
    path(SHRINE_PATH[0], 7, SHRINE_PATH[1], ROAD[0])                   # trilha da fonte (ilusoes)
    path(16, 7, 25, 8)                                                  # patio da fonte
    path(6, 18, 7, ROAD[0]); path(12, 18, 13, ROAD[0]); path(33, 19, 34, ROAD[0])   # portas
    path(7, 31, 32, 32)                                                 # rua sul (portas das casas)
    path(24, ROAD[1], 25, 31)                                           # liga a rua sul a principal
    c.rect(26, 26, 28, 29, "pond")                                      # pequeno lago do jardim
    water = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "pond"}
    blocks = set()
    for (name, x, y, _) in BUILDINGS:
        c.stamp(name, x, y)
    for y in range(H):
        for x in range(W):
            if c.terrain[y][x] == "other":
                blocks.add((x, y))
    avoid = set(paths) | water | blocks
    c.forest(lambda x, y: x < 2 or y < 2 or x >= W - 2 or y >= H - 2, avoid, margin=0)
    def blob(cx, cy, rx, ry):
        return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
    for b in [blob(8, 6, 5, 4), blob(34, 6, 6, 4), blob(25, 15, 2, 3), blob(39, 25, 2, 4), blob(4, 34, 2, 2), blob(22, 35, 5, 2)]:
        c.forest(b, avoid)
    # trilha da fonte entre moitas: as ilusoes fecham as duas faixas
    c.rect(18, 9, 19, 19, "dense"); c.rect(22, 9, 23, 19, "dense")
    c.rect(16, 10, 17, 17, "flower"); c.rect(9, 23, 13, 23, "flower")
    c.rect(36, 23, 38, 23, "flower")
    for (x, y) in [(29, 25), (35, 24)]:                                # pedras do jardim
        c.put(x, y, 226, collision=1)
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
