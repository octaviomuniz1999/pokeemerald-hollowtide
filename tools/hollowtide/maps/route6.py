#!/usr/bin/env python3
"""Route 6 (Caminho dos Jardins) — Pillarton -> Serenia, 54x36 (General + Lavaridge, como Serenia).

Jardim de pedra ao norte (areia "rastelada" com pedras dispostas), bosques fechados (no lugar do bambu),
canal tranquilo ao sul, pequenos santuarios de beira de estrada (pares de pedras e placa), mato alto.
A trilha sai da Pillarton (linhas 20-21, offset 0) e chega a Serenia (linhas 20-21).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 54, 36
ROAD = (20, 21)


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    paths = []
    def path(x0, y0, x1, y1):
        c.rect(x0, y0, x1, y1, "sand")
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(0, ROAD[0], 13, ROAD[1]); path(12, 14, 13, ROAD[1]); path(12, 14, 31, 15)
    path(30, 14, 31, 23); path(30, 22, 41, 23); path(40, ROAD[0], 41, 23); path(40, ROAD[0], W - 1, ROAD[1])
    # jardim de pedra (areia lisa com pedras dispostas) e canteiros em volta
    c.rect(15, 4, 28, 10, "sand")
    c.rect(14, 3, 29, 3, "flower"); c.rect(14, 11, 29, 11, "flower")
    # canal tranquilo ao sul
    c.rect(6, 27, 47, 30, "pond")
    water = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "pond"}
    garden = {(x, y) for y in range(3, 12) for x in range(14, 30)}
    avoid = set(paths) | water | garden
    c.forest(lambda x, y: x < 2 or x >= W - 2 or y < 2 or y >= H - 2, avoid, margin=0)
    def blob(cx, cy, rx, ry):
        return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
    for b in [blob(6, 9, 4, 5), blob(38, 7, 6, 4), blob(48, 12, 3, 5), blob(22, 19, 5, 2.5), blob(5, 31, 3, 2),
              blob(50, 30, 2, 3), blob(36, 18, 2, 2)]:
        c.forest(b, avoid)
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = "tall"
    BL = ["  ,,,,,, ", ",,,,,,,,,", ",,,,,,,,,", "  ,,,,,  "]
    tall(2, 22, BL); tall(42, 23, BL); tall(32, 9, BL[:3]); tall(16, 23, BL[:3])
    c.rect(44, 15, 47, 15, "flower"); c.rect(3, 15, 6, 15, "flower")
    # pedras do jardim (pares e trios, como num karesansui) e santuarios de beira de estrada
    for (x, y) in [(17, 5), (18, 5), (21, 8), (24, 5), (25, 6), (26, 5), (19, 9)]:
        c.put(x, y, 226, collision=1)
    for (x, y) in [(10, 18), (11, 18), (43, 18), (44, 18)]:
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
