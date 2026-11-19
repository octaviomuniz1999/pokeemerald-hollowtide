#!/usr/bin/env python3
"""Route 7 (Caminho dos Espelhos) — Serenia -> Horizon City, 36x56 (General + Lavaridge, como Serenia).

O lago-espelho ocupa o oeste; a trilha sobe pela margem leste. A leste, o Circulo da Lua: um patamar com um
anel de pedras (onde os Clefairy dancam a noite), acessado por escada. Campo de flores ao sul, mato alto no
meio e ao norte. Entrada pela Serenia (sul, colunas 20-21; Serenia x = Route 7 x + 18) e saida para a
Horizon City (norte, colunas 16-17). As faixas que as cidades enxergam usam so metatiles do primario.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 36, 56
SOUTH = (20, 21)          # trilha que vem da Serenia
NORTH = (16, 17)          # trilha que segue para a Horizon City
OFFSET_SERENIA = 18       # Serenia x = Route 7 x + 18 (porta norte da Serenia nas colunas 38-39)
HILL_STAIRS = 26          # escada do Circulo da Lua (2 colunas)
# lago e patamar em retangulos com degraus de 2 tiles (degrau de 1 tile nao tem quina no autotile)
LAKE = [(6, 8, 11, 11), (4, 12, 13, 15), (3, 16, 14, 39), (4, 40, 12, 43), (6, 44, 10, 45)]
HILL = [(24, 5, 31, 6), (22, 7, 33, 16)]
RING = [(27, 9), (30, 9), (25, 11), (32, 11), (27, 13), (30, 13)]   # anel de pedras no alto


def blob(cx, cy, rx, ry, ph=0.0, amp=(0.12, 0.07)):
    def inside(x, y):
        dx, dy = (x - cx) / rx, (y - cy) / ry
        t = math.atan2(dy, dx)
        r = 1 + amp[0] * math.sin(3 * t + ph) + amp[1] * math.sin(5 * t + 2 * ph)
        return dx * dx + dy * dy <= r * r
    return inside


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    # patamar do Circulo da Lua (borda sul reta em volta da escada)
    for (x0, y0, x1, y1) in HILL:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c.level[y][x] = 5
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    S = lambda x: max(y for y in range(H) if c.level[y][x] >= 5)
    # trilha principal: Serenia -> curva para a margem -> margem leste do lago -> Horizon
    path(SOUTH[0], 44, SOUTH[1], H - 1)
    path(NORTH[0], 44, SOUTH[1], 45)
    path(NORTH[0], 0, NORTH[1], 45)
    # ramal para a escada do Circulo da Lua
    path(NORTH[1], 24, HILL_STAIRS + 1, 25)
    path(HILL_STAIRS, S(HILL_STAIRS) + 2, HILL_STAIRS + 1, 25)
    c.stairs(HILL_STAIRS, S(HILL_STAIRS), 2)
    path(HILL_STAIRS, 12, HILL_STAIRS + 1, S(HILL_STAIRS) - 1)
    stair = set()
    for (x, y) in c.stair_cols:
        stair |= {(x, y), (x, y + 1)}
    paths.extend(stair)
    # lago-espelho (oeste), contorno organico
    for (x0, y0, x1, y1) in LAKE:
        c.rect(x0, y0, x1, y1, "pond")
    # pradaria de flores ao sul (Flabebe) e canteiros na margem
    c.rect(24, 46, 31, 49, "flower"); c.rect(23, 47, 23, 48, "flower")
    c.rect(4, 49, 9, 49, "flower")
    water = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "pond"}
    hilltop = {(x, y) for y in range(H) for x in range(W) if c.level[y][x] >= 5}
    meadow = {(x, y) for x in range(22, 33) for y in range(45, 51)}
    avoid = set(paths) | water | meadow
    c.forest(lambda x, y: x < 2 or x >= W - 2 or y < 2 or y >= H - 2, avoid, margin=0)
    for b in [blob(27, 34, 4, 3), blob(31, 41, 3, 2.5), blob(8, 52, 5, 2), blob(30, 52, 4, 2),
              blob(8, 4, 5, 2.5), blob(26, 2, 5, 1.5), blob(20, 18, 2, 3), blob(12, 49, 3, 2), blob(32, 25, 2, 4),
              blob(20, 50, 1.5, 2.5), blob(24, 40, 2, 2)]:
        c.forest(b, avoid | hilltop)
    # mato alto (fora das trilhas)
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass" and c.level[y][x] == 3:
                    c.terrain[y][x] = "tall"
    BL = ["  ,,,,,, ", ",,,,,,,,,", ",,,,,,,,,", ",,,,,,,,,", "  ,,,,,  "]
    tall(22, 27, BL); tall(19, 36, BL[:4]); tall(18, 5, BL[:4]); tall(28, 19, ["  ,,,,", ",,,,,,", ",,,,,,"])
    tall(2, 46, [" ,,,,", ",,,,,", " ,,, "])
    c.rect(28, 10, 29, 12, "flower")
    # anel de pedras do Circulo da Lua e pedras soltas na margem
    for (x, y) in RING:
        c.put(x, y, 226, collision=1)
    for (x, y) in [(15, 12), (15, 38), (22, 43)]:
        if c.terrain[y][x] == "grass":
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
