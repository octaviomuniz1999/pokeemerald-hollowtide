#!/usr/bin/env python3
"""Route 12 (River Bend) — rota opcional a oeste da Route 5, 40x30 (General + Rustboro, como a Route 5).

Um rio em S atravessa o mapa de norte a sul: no alto ele corre a oeste, no meio cruza o centro (onde fica o
tabuado da trilha) e embaixo corre a leste. A trilha chega pela borda leste (linhas 14-15, alinhadas com o
tabuado novo do braco oeste da Route 5: Route 12 y = Route 5 y - 15), atravessa o rio e se divide:
- margem leste, no alto: prado com mato alto e uma ponta de areia na curva de dentro;
- margem oeste, embaixo: o prado e a prainha da curva ("river bend"), com o item maior;
- da entrada, uma trilha desce para o sul ate um remanso de pesca.
Pokemon do canone (POKEDEX_LUNIA): Froakie (raro), Ducklett, Basculin, Corphish, Tympole.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 40, 30
EAST = (14, 15)               # saida leste (linhas) = Route 5 linhas 29-30
OFFSET_ROUTE05 = 15           # Route 12 y = Route 5 y - 15
HBOARD = (836, 844, 845)      # tabuado horizontal (topo, meio andaveis; sombra bloqueada) — o mesmo da Route 5
BOARD_ROWS = (14, 15, 16)


def river_center(y):
    if 13 <= y <= 17:
        return 17                                   # trecho reto sob o tabuado
    return 17 + round(6 * math.sin((y - 15) / 5.5))


def river_cols(y):
    cx = river_center(y)
    return range(cx - 2, cx + 2)                    # 4 de largura


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Rustboro")
    c.fill("grass")
    for y in range(H):
        for x in river_cols(y):
            c.terrain[y][x] = "pond"
    # curvas de dentro: areia na margem
    for y in range(4, 8):                                         # ponta de areia (margem leste, no alto)
        x0 = river_cols(y)[-1] + 1
        c.rect(x0, y, x0 + 5 - abs(y - 5), y, "sand")
    for y in range(21, 26):                                       # prainha da curva (margem oeste, embaixo)
        x1 = river_cols(y)[0] - 1
        c.rect(x1 - 6 + abs(y - 23), y, x1, y, "sand")
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(19, EAST[0], W - 1, EAST[1])                  # entrada leste ate o tabuado
    path(5, EAST[0], 14, EAST[1])                      # margem oeste
    path(5, 16, 6, 22); path(5, 22, 15, 23)            # desce para a prainha
    path(19, 7, 20, 13)                                # sobe pela margem ate a ponta de areia
    path(30, 16, 31, 24); path(30, 24, 33, 25)         # desce para o remanso
    c.rect(32, 26, 35, 27, "pond")                     # remanso (pesca)
    water = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "pond"}
    sand = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "sand"}
    avoid = set(paths) | water | sand
    c.forest(lambda x, y: x < 2 or (x >= W - 2 and not EAST[0] - 1 <= y <= EAST[1] + 1) or y < 2 or y >= H - 2,
             avoid, margin=0)
    for b in [blob(5, 6, 4, 4), blob(34, 6, 4, 3), blob(9, 27, 4, 2), blob(26, 21, 3, 2.5), blob(37, 22, 2, 4)]:
        c.forest(b, avoid)
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = "tall"
    tall(27, 8, [" ,,,,,", ",,,,,,,", ",,,,,,", " ,,,,"])        # margem leste, no alto
    tall(7, 17, [",,,,", ",,,,,", ",,,,", " ,,"])                # prado oeste
    tall(33, 17, [",,,", ",,,", ",,"])                           # descida para o remanso
    c.rect(9, 11, 11, 12, "flower"); c.rect(28, 19, 29, 19, "flower")
    # tabuado sobre o rio (linhas 14-15 andaveis, 16 sombra)
    for x in river_cols(14):
        c.put(x, BOARD_ROWS[0], HBOARD[0], collision=0)
        c.put(x, BOARD_ROWS[1], HBOARD[1], collision=0)
        c.put(x, BOARD_ROWS[2], HBOARD[2], collision=1)
    for (x, y) in [(18, 5), (18, 25)]:                 # pedras na areia
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
