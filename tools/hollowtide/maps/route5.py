#!/usr/bin/env python3
"""Route 5 (delta) — Tradepost -> Pillarton, 42x52 (General + Rustboro, como o Tradepost).

O canal do Tradepost continua para o norte como o rio principal (x 23-26, offset 6). Um braco oeste contorna
a ilha do meio (mato alto, treinadores, item) e e atravessado por dois tabuados; a leste do rio, o leito
antigo esta seco (a barragem de Pillarton segura a agua): areia, pedras e pocas na varzea. Saida norte
(trilha x 16-17) para Pillarton.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 42, 52
OFFSET_TRADEPOST = 6          # Route 5 x = Tradepost x - 6
RIVER = (22, 25)           # = canal do Tradepost (x 28-31)
SOUTH_PATH = (20, 21)         # = avenida norte do Tradepost (x 26-27)
NORTH_PATH = (16, 17)
WEST_ROWS = (29, 30)           # saida oeste para a Route 12 (River Bend), por um tabuado sobre o braco oeste
VBOARD = (846, 847)           # tabuado vertical (Route 104)
HBOARD = (836, 844, 845)      # tabuado horizontal (topo, meio andaveis; sombra bloqueada)


def compose(north_open=False):
    c = Canvas(W, H, "gTileset_General", "gTileset_Rustboro")
    c.fill("grass")
    # agua: rio principal, braco oeste em volta da ilha
    c.rect(RIVER[0], 0, RIVER[1], H - 1, "pond")
    c.rect(8, 10, RIVER[0], 13, "pond")
    c.rect(8, 10, 11, 38, "pond")
    c.rect(8, 35, RIVER[0], 38, "pond")
    # leito seco a leste (areia e pedras) e varzea com pocas
    c.rect(RIVER[1] + 1, 19, 38, 23, "sand")
    c.ascii(29, 30, [" xxx  ", "xxxxx ", " xxx  "])
    c.ascii(33, 40, ["  xx ", " xxxx", "  xx "])
    # trilhas
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(SOUTH_PATH[0], 39, SOUTH_PATH[1], H - 1)          # chegada do Tradepost
    path(18, 39, 21, 40)
    path(18, 33, 19, 34); path(14, 22, 19, 23); path(14, 22, 15, 34); path(14, 33, 19, 34)   # trilha na ilha
    path(16, 14, 17, 21); path(16, 14, 19, 15)
    path(NORTH_PATH[0], 0, NORTH_PATH[1], 9)               # para Pillarton
    path(RIVER[1] + 1, 26, 30, 27)                        # do tabuado leste ao leito seco
    path(0, WEST_ROWS[0], 7, WEST_ROWS[1])                # para a Route 12 (oeste)
    path(12, WEST_ROWS[0], 13, WEST_ROWS[1])              # da ilha ao tabuado oeste
    water = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "pond"}
    # mata (moldura e bosques), sem encostar em trilha nem agua
    c.forest(lambda x, y: x < 2 or x >= W - 2 or (y < 2 and not NORTH_PATH[0] - 1 <= x <= NORTH_PATH[1] + 1
                                                         and not RIVER[0] <= x <= RIVER[1])
             or (y >= H - 2 and not SOUTH_PATH[0] - 1 <= x <= SOUTH_PATH[1] + 1 and not RIVER[0] <= x <= RIVER[1]),
             set(paths) | water, margin=0)
    def blob(cx, cy, rx, ry):
        return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
    for b in [blob(5, 44, 4, 5), blob(13, 46, 4, 3), blob(4, 5, 3, 4), blob(34, 5, 5, 4), blob(36, 14, 4, 3),
              blob(20, 28, 2.5, 3), blob(34, 46, 4, 3), blob(4, 24, 2, 8)]:
        c.forest(b, set(paths) | water)
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = "tall"
    tall(12, 16, [" ,,,  ", ",,,,, ", ",,,,,,", " ,,,, "])
    tall(16, 25, [",,,,,", ",,,,,", ",,,, "])
    tall(2, 40, [" ,,,,,", ",,,,,,", ",,,,,", " ,,,"])
    tall(28, 9, ["  ,,,,,", ",,,,,,,", ",,,,,,", "  ,,,"])
    tall(30, 34, [",,,,,", " ,,,,"])
    c.rect(16, 30, 17, 31, "flower"); c.rect(29, 15, 31, 15, "flower")
    if not north_open:                                     # Pillarton ainda nao existe: trilha termina na mata
        c.rect(NORTH_PATH[0], 0, NORTH_PATH[1], 1, "tree")
    # tabuados por cima da agua
    for y in range(35, 39):
        c.put(18, y, VBOARD[0], collision=0); c.put(19, y, VBOARD[1], collision=0)
    for y in range(10, 14):
        c.put(16, y, VBOARD[0], collision=0); c.put(17, y, VBOARD[1], collision=0)
    for x in range(RIVER[0], RIVER[1] + 1):
        c.put(x, 26, HBOARD[0], collision=0); c.put(x, 27, HBOARD[1], collision=0); c.put(x, 28, HBOARD[2], collision=1)
    c.rect(20, 26, 21, 27, "sand")                         # da ilha ao tabuado leste
    for x in range(8, 12):                                 # tabuado sobre o braco oeste (Route 12)
        c.put(x, WEST_ROWS[0], HBOARD[0], collision=0); c.put(x, WEST_ROWS[1], HBOARD[1], collision=0)
        c.put(x, WEST_ROWS[1] + 1, HBOARD[2], collision=1)
    # pedras no leito seco
    for (x, y) in [(29, 20), (33, 22), (36, 20)]:
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
