#!/usr/bin/env python3
"""Route 10 (Costa dos Farois) — Voltara -> Tidemouth, 38x60 (General + Lilycove).

A estrada desce de Voltara pela encosta (norte, colunas 18-19; Voltara x = Route 10 x + 12), chega ao litoral
e segue para o sul pela praia, entre o mar (oeste) e as falesias com mata (leste). Pontas de pedra com
farois-guia (postes da orla), enseada de agua rasa, mato alto na restinga. Saida sul (colunas 18-19) para
Tidemouth. As faixas que Voltara e Tidemouth enxergam usam so primario.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 38, 60
NORTH = (18, 19)
SOUTH = (18, 19)
OFFSET_VOLTARA = 12          # Voltara x = Route 10 x + 12 (saida sul de Voltara nas colunas 30-31)
BEACONS = [(6, 22), (9, 41)]  # farois-guia nas pontas de pedra (poste composto sobre areia)


def coast(y):
    """Coluna onde comeca a areia (o mar fica a oeste), com recortes."""
    return 12 + round(3 * math.sin(y / 6.0) + 2 * math.sin(y / 2.7 + 1.3))


def north_edge(x):
    """Linha onde comeca o litoral em cada coluna (praia curva ao norte, em degraus de 2)."""
    return 14 - 2 * (x >= 6) - 2 * (x >= 11) + 2 * (x >= 17)


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    # litoral: mar -> agua rasa -> areia (a partir da linha 14; acima e encosta com mata)
    for y in range(10, H):
        cx = coast(y)
        road = max(coast(y) + 4, 16)
        for x in range(0, cx):
            if y >= north_edge(x):
                c.terrain[y][x] = "sea" if x < cx - 2 else "shallow"
        for x in range(cx, min(W, road + 3)):
            if y >= north_edge(x) - 1:
                c.terrain[y][x] = "sand"
    # enseada rasa e pontas de pedra (onde ficam os farois)
    c.rect(3, 30, 9, 35, "shallow")
    for (bx, by) in BEACONS:
        c.rect(bx - 2, by - 1, bx + 2, by + 2, "sand")
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    # estrada: encosta (terra) ate a praia e depois pela areia firme ate o sul
    path(NORTH[0], 0, NORTH[1], 16)
    for y in range(14, H):
        x = max(coast(y) + 4, 16)
        path(x, y, x + 1, y)
    path(SOUTH[0], H - 6, SOUTH[1], H - 1)
    # restinga com mato alto e falesia com mata a leste
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = "tall"
    BL = ["  ,,,,,, ", ",,,,,,,,,", ",,,,,,,,,", "  ,,,,,  "]
    tall(24, 20, BL); tall(23, 38, BL); tall(25, 6, BL[:3])
    water = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] in ("sea", "shallow", "sand")}
    avoid = set(paths) | water
    c.forest(lambda x, y: x >= W - 2 or y < 2 or (y >= H - 2) or (x < 2 and y < 14), avoid, margin=0)
    for bl in [blob(31, 14, 5, 4), blob(32, 30, 4, 5), blob(31, 48, 5, 4), blob(8, 6, 6, 4), blob(28, 55, 4, 2.5)]:
        c.forest(bl, avoid)
    for (bx, by) in BEACONS:
        c.lamp(bx, by, floor="sand")
    for (x, y) in [(5, 25), (11, 44), (7, 52)]:
        if c.terrain[y][x] in ("sand", "shallow"):
            c.put(x, y, 226, collision=1)
    # restinga: canteiros de flores e pedras soltas na faixa de grama entre a praia e a mata (fora das linhas de visao)
    keep = {(21, 18), (13, 26), (20, 36), (22, 48), (26, 22), (20, 4), (21, 54)}
    for (x0, y0, rows) in [(23, 6, ["ff", "fff"]), (24, 26, [" ff", "ff "]), (23, 40, ["fff", " f "]), (25, 52, ["ff"]), (21, 12, ["f f"])]:
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch == "f" and c.terrain[y][x] == "grass" and (x, y) not in keep:
                    c.terrain[y][x] = "flower"
    for (x, y) in [(25, 9), (24, 33), (25, 44), (23, 29)]:
        if c.terrain[y][x] == "grass" and (x, y) not in keep:
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
