#!/usr/bin/env python3
"""Route 8 (Encostas Antigas) — Horizon City -> Passway Village, 34x48 (General + Lilycove, como a Horizon:
a Route 8 enxerga o Pavilhao das Estrelas na emenda sul).

Encosta de montanha em tres patamares de contorno organico, subidos por escadas; ressaltos (ledges) dao
atalhos de descida; bosques de pinheiro (mata 2x2), pedras soltas, um mirante sobre o lago e um abrigo de
pedra. Entrada sul pela Horizon (colunas 16-17; Horizon x = Route 8 x + 36) e saida norte (colunas 18-19)
para a Passway Village.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 34, 48
SOUTH = (16, 17)
NORTH = (18, 19)
OFFSET_HORIZON = 36       # Horizon x = Route 8 x + 36 (saida norte da Horizon nas colunas 52-53)


def b(x, base, amp, freq, ph):
    return base + round(amp * math.sin(x / freq + ph))


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    e5 = {x: b(x, 36, 1.5, 5.0, 0.7) for x in range(W)}
    e7 = {x: b(x, 24, 1.8, 4.5, 2.2) for x in range(W)}
    e9 = {x: b(x, 12, 1.4, 4.0, 4.0) for x in range(W)}
    STAIRS = ((e5, 22), (e7, 10), (e9, 24))
    for e, sx in STAIRS:                          # borda reta em volta de cada escada
        for x in range(sx - 2, sx + 4):
            e[x] = e[sx]
    for x in range(W):
        for y in range(H):
            c.level[y][x] = 9 if y <= e9[x] else 7 if y <= e7[x] else 5 if y <= e5[x] else 3
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    S = lambda L, x: max(y for y in range(H) if c.level[y][x] >= L)
    # trilha: Horizon -> escada 1 (leste) -> encosta -> escada 2 (oeste) -> escada 3 (leste) -> cume -> Passway
    path(SOUTH[0], 42, SOUTH[1], H - 1); path(SOUTH[0], 42, 23, 43)
    path(22, S(5, 22) + 2, 23, 43); c.stairs(22, S(5, 22), 2)
    path(22, 30, 23, S(5, 22) - 1); path(10, 30, 23, 31)
    path(10, S(7, 10) + 2, 11, 31); c.stairs(10, S(7, 10), 2)
    path(10, 18, 11, S(7, 10) - 1); path(10, 18, 25, 19)
    path(24, S(9, 24) + 2, 25, 19); c.stairs(24, S(9, 24), 2)
    path(24, 6, 25, S(9, 24) - 1); path(NORTH[0], 6, 25, 7); path(NORTH[0], 0, NORTH[1], 7)
    stair = set()
    for (x, y) in c.stair_cols:
        stair |= {(x, y), (x, y + 1)}
    paths.extend(stair)
    # mirante (oeste, no patamar 7) e mato alto
    path(3, 20, 7, 21)
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = "tall"
    tall(25, 38, ["  ,,,,", ",,,,,,", ",,,,,,", " ,,,, "]); tall(13, 25, [" ,,,,,,", ",,,,,,,", " ,,,,, "])
    tall(27, 14, [",,,,", ",,,,", ",,, "]); tall(12, 8, [" ,,,,", ",,,,,", ",,,, "])
    avoid = set(paths) | c.cliff_cells()
    c.forest(lambda x, y: x < 2 or x >= W - 2 or y < 2 or y >= H - 2, avoid, margin=0)
    for bl in [blob(5, 42, 4, 3), blob(28, 46, 3, 1.5), blob(4, 32, 2.5, 2), blob(30, 31, 2.5, 2.5),
               blob(5, 12, 3, 4), blob(17, 13, 3, 2), blob(30, 7, 2, 3), blob(10, 3, 5, 2), blob(18, 37, 2, 2)]:
        c.forest(bl, avoid)
    for (x, y) in [(20, 40), (14, 33), (27, 27), (8, 24), (20, 15), (14, 4), (29, 22)]:
        if c.terrain[y][x] == "grass" and (x, y) not in avoid:
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
