#!/usr/bin/env python3
"""Pillarton City ("A Cidade das Aguas Presas") — 56x44, General + Rustboro.

Norte: a barragem (patamar com o reservatorio represado) com a crista onde ficam as tres valvulas e, a leste,
a usina da Team Palm. Do pe da barragem sai o rio (fraco: a usina segura a agua), que cruza a cidade sob
duas pontes e segue para a Route 5 (offset 4). Um canal antigo, seco, mostra a rocha nua. Margem oeste:
Centro Pokemon, Mart, moradias; margem leste: ginasio do Tchum, jardins "de contrato" da Palm.
Sul: parque (so primario nas linhas que a Route 5 enxerga). Patamares so visuais (piso andavel -> elevacao 3).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas, extract

W, H = 56, 44
OFFSET_ROUTE5 = 4             # Pillarton x = Route 5 x + 4
RIVER = (26, 29)              # = rio da Route 5 (x 22-25)
SOUTH_PATH = (20, 21)         # = trilha norte da Route 5 (x 16-17)
VALVES = [(16, 6), (26, 6), (36, 6)]
PARK_TOP = 38
HBOARD = (836, 844, 845)
BUILDINGS = [
    ("rb_office_long", 43, 2, "plant"),          # usina da Team Palm (na crista, a leste)
    ("rb_pokecenter", 9, 13, "pc"),
    ("rb_mart", 16, 13, "mart"),
    ("rb_apartment", 2, 20, "flat"),
    ("rb_house_grey", 12, 30, "house_w"),
    ("rb_gym", 40, 14, "gym"),
    ("rb_house_grey", 33, 30, "house_e"),
    ("rb_office_small", 44, 30, "office_e"),
]
LAMPS = [(14, 18), (23, 18), (32, 18), (38, 22), (23, 29), (32, 29)]


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Rustboro")
    c.fill("plaza")
    ids = json.load(open(os.path.join(os.path.dirname(__file__), "..", "mapgen", "custom_ids.json")))["rustboro"]
    # barragem: patamar com reservatorio e crista
    c.rect(2, 2, W - 3, 9, "high")
    c.rect(6, 3, 38, 5, "pond")                  # agua represada
    c.rect(4, 6, 40, 8, "sand")                  # crista (caminho de servico)
    c.rect(39, 2, W - 3, 8, "plaza")             # patio da usina
    c.stairs(10, 9, 2)                           # escada da crista
    # parque ao sul e moldura
    c.rect(0, PARK_TOP, W - 1, H - 1, "grass")
    c.rect(0, 0, W - 1, 1, "tree"); c.rect(0, 0, 1, H - 1, "tree"); c.rect(W - 2, 0, W - 1, H - 1, "tree")
    # rio: poco ao pe da barragem e leito ate a borda sul
    c.rect(24, 11, 31, 13, "pond")
    c.rect(RIVER[0], 11, RIVER[1], H - 1, "pond")
    # canal antigo seco (rocha nua) para oeste
    c.rect(6, 24, RIVER[0] - 1, 26, "sand")
    # ruas
    c.rect(2, 16, RIVER[0] - 1, 17, "road"); c.rect(RIVER[1] + 1, 19, W - 3, 20, "road")
    c.rect(8, 10, 9, 23, "road"); c.rect(SOUTH_PATH[0], 18, SOUTH_PATH[1], PARK_TOP - 1, "road")
    c.rect(2, 28, RIVER[0] - 1, 29, "road"); c.rect(RIVER[1] + 1, 27, W - 3, 28, "road")
    c.rect(36, 10, 37, 18, "road")
    # jardins "de contrato" da Palm (flores em canteiros cercados de grama)
    c.rect(46, 22, 52, 25, "grass"); c.rect(47, 23, 51, 24, "flower")
    c.rect(32, 22, 36, 25, "grass"); c.rect(33, 23, 35, 24, "flower")
    for (name, x, y, _) in BUILDINGS:
        c.stamp(name, x, y)
    for (x, y) in LAMPS:
        c.stamp("rb_lamp", x, y)
    # parque
    c.rect(SOUTH_PATH[0], PARK_TOP, SOUTH_PATH[1], H - 1, "sand")
    paths = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] in ("sand", "pond") and y >= PARK_TOP - 1}
    c.forest(lambda x, y: y >= 40 and not (SOUTH_PATH[0] - 1 <= x <= SOUTH_PATH[1] + 1) and not (RIVER[0] - 1 <= x <= RIVER[1] + 1),
             paths, margin=0)
    c.forest(lambda x, y: ((x - 8) / 5) ** 2 + ((y - 40) / 2) ** 2 <= 1, paths)
    c.forest(lambda x, y: ((x - 44) / 6) ** 2 + ((y - 40) / 2) ** 2 <= 1, paths)
    c.rect(34, 38, 38, 38, "flower"); c.rect(12, 38, 15, 38, "flower")
    # valvulas na crista (fechadas), pontes sobre o rio, pedras no canal seco
    for (x, y) in VALVES:
        c.put(x, y, ids["valve_closed"], collision=1)
    for row in (21, 33):
        for x in range(RIVER[0], RIVER[1] + 1):
            c.put(x, row, HBOARD[0], collision=0); c.put(x, row + 1, HBOARD[1], collision=0)
            c.put(x, row + 2, HBOARD[2], collision=1)
    for (x, y) in [(9, 25), (15, 24), (21, 26)]:
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
