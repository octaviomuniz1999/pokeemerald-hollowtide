#!/usr/bin/env python3
"""Ferralia City — metropole (referencia: Sao Paulo; atmosfera de Goldenrod/Castelia, sem copiar).

Malha de avenidas de 2 tiles (General + Rustboro): avenida norte (linhas 18-19), "Paulista" (40-41) e tres
avenidas N-S (x 16-17, 40-41, 58-59). Bairros: residencial (NO), sede da ferrovia e siderurgia (N), ginasio do
Vessel com torres (NE), praca da fonte com Centro Pokemon e Mart (centro), torres de escritorio ao longo da
Paulista, patio de carga cercado com o deposito ferroviario (L), escritorios ao sul e o parque (S), que faz a
emenda com a Route 3 (so metatiles do primario nas 5 linhas que a rota enxerga).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas, extract

W, H = 72, 64
SOUTH_PATH = (40, 43)          # trilha do parque = estrada da Route 3 (x 24-27) com offset 16
OFFSET_ROUTE3 = 16             # Route 3 x = Ferralia x - 16
PARK_TOP = 50
RAIL_ROWS = (26, 32)           # linhas pares: a moldura de arvores 2x2 fica inteira acima e abaixo
FENCE_L, FENCE_M, FENCE_R, FENCE_V = 702, 679, 850, 793

# (carimbo, x, y, rotulo) — rotulo identifica a porta no instalador
BUILDINGS = [
    ("rb_apartment", 3, 4, "flat_nw"),
    ("rb_house_grey", 10, 7, "house_nw"),
    ("rb_office_small", 18, 6, "office_n"),
    ("rb_devon", 24, 4, "hq"),
    ("rb_house_grey", 35, 7, "house_n"),
    ("rb_gym", 46, 8, "gym"),
    ("rb_tower", 53, 4, "tower_ne"),
    ("rb_office_long", 60, 3, "depot"),
    ("rb_office_long", 4, 22, "school"),
    ("rb_house_grey", 4, 32, "house_w1"),
    ("rb_house_grey", 10, 32, "house_w2"),
    ("rb_pokecenter", 19, 21, "pc"),
    ("rb_mart", 35, 21, "mart"),
    ("rb_office_mid", 43, 21, "office_e1"),
    ("rb_office_six", 51, 21, "office_e2"),
    ("rb_tower", 43, 30, "tower_1"),
    ("rb_tower", 48, 30, "tower_2"),
    ("rb_tower", 53, 30, "tower_3"),
    ("rb_office_six", 4, 43, "office_s1"),
    ("rb_office_mid", 19, 43, "office_s2"),
    ("rb_office_small", 30, 43, "office_s3"),
    ("rb_house_grey", 46, 43, "house_s"),
    ("rb_office_small", 52, 43, "office_s4"),
    ("rb_office_six", 61, 43, "office_se"),
]
LAMPS = [(4, 16), (9, 16), (14, 16), (23, 13), (35, 13), (45, 14), (52, 14),
         (21, 24), (35, 24), (21, 35), (35, 35), (20, 38), (26, 38), (31, 38), (47, 38), (52, 38), (57, 38), (8, 38), (13, 38)]


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Rustboro")
    c.fill("plaza")
    # --- parque ao sul (emenda com a Route 3) ---
    c.rect(0, PARK_TOP, W - 1, H - 1, "grass")
    # --- moldura ---
    c.rect(0, 0, W - 1, 1, "tree"); c.rect(0, 0, 1, H - 1, "tree"); c.rect(W - 2, 0, W - 1, H - 1, "tree")
    # --- avenidas ---
    c.rect(2, 18, W - 3, 19, "road"); c.rect(2, 40, W - 1, 41, "road")   # Paulista sai a leste: Route 4
    for x in (16, 40, 58):
        c.rect(x, 2, x + 1, 47, "road")
    # --- praca da fonte (jardim com canteiros) ---
    c.rect(23, 25, 33, 33, "grass")
    c.rect(24, 26, 32, 26, "flower"); c.rect(24, 32, 32, 32, "flower")
    c.rect(24, 27, 24, 31, "flower"); c.rect(32, 27, 32, 31, "flower")
    # --- canteiros residenciais ---
    c.rect(3, 14, 9, 15, "grass"); c.rect(4, 14, 8, 14, "flower")
    c.rect(18, 12, 21, 15, "grass")
    c.rect(42, 13, 43, 16, "grass"); c.rect(54, 13, 56, 16, "grass")     # canteiros na praca do ginasio
    c.rect(43, 14, 43, 15, "flower"); c.rect(55, 14, 55, 15, "flower")
    # --- patio de carga cercado (areia), com abertura para a avenida leste ---
    c.rect(61, 22, W - 3, 37, "sand")
    for (x, y) in BUILDINGS_STAMPS(c):
        pass
    c.stamp("rb_fountain", 27, 28)
    for (x, y) in LAMPS:
        c.stamp("rb_lamp", x, y)
    # cercas do patio (horizontais em cima/embaixo, verticais nas laterais; vao de entrada nas linhas 28-29)
    fence_h(c, 60, 69, 21); fence_h(c, 60, 69, 38)
    for y in list(range(22, 28)) + list(range(30, 38)):
        c.put(60, y, FENCE_V, collision=1)
    # --- arvores em canteiro na praca (2x2 sobre grama) ---
    for (x, y) in [(25, 27), (30, 27), (25, 30), (30, 30)]:
        pass
    c.small_tree(19, 13)
    # --- ferrovia: duas linhas no patio de carga, com para-choque a oeste; seguem para leste (futura Route 4) ---
    import json
    ids = json.load(open(os.path.join(os.path.dirname(__file__), "..", "mapgen", "custom_ids.json")))["rustboro"]
    for ry in RAIL_ROWS:
        c.put(62, ry, ids["rail_end"], collision=0)
        for x in range(63, W):
            c.put(x, ry, ids["rail_h"], collision=0)
        c.rect(W - 2, ry + 1, W - 1, ry + 1, "dense")   # sem passagem pelo leito: a ferrovia esta fechada
    # --- parque: cerca separando a cidade, entrada pela avenida central ---
    fence_h(c, 2, 38, PARK_TOP - 1); fence_h(c, 45, W - 3, PARK_TOP - 1)
    c.rect(38, 48, 45, PARK_TOP - 1, "plaza")
    c.rect(SOUTH_PATH[0], PARK_TOP, SOUTH_PATH[1], H - 1, "sand")
    c.rect(20, 54, 61, 55, "sand")                        # alameda leste-oeste do parque
    c.rect(18, 53, 19, 56, "flower"); c.rect(62, 53, 63, 56, "flower")   # canteiros nas pontas da alameda
    paths = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "sand" and y >= PARK_TOP}
    import math
    def blob(cx, cy, rx, ry):
        return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
    c.forest(lambda x, y: y >= 60 and not SOUTH_PATH[0] - 2 <= x <= SOUTH_PATH[1] + 2, paths, margin=0)
    c.forest(blob(10, 56, 7, 4), paths); c.forest(blob(31, 58, 6, 3), paths)
    c.forest(blob(51, 58, 6, 3), paths); c.forest(blob(66, 55, 4, 4), paths)
    for (x0, y0, rows) in [(24, 51, [" ,,,,,,  ", ",,,,,,,, ", " ,,,,,   "]),            # mato alto do parque
                           (48, 51, ["  ,,,,,, ", ",,,,,,,,,", "  ,,,,   "])]:
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch != " " and c.terrain[y0 + dy][x0 + dx] == "grass":
                    c.terrain[y0 + dy][x0 + dx] = "tall"
    c.rect(4, 51, 9, 51, "flower"); c.rect(64, 51, 68, 51, "flower"); c.rect(34, 52, 37, 52, "flower")
    return c


def fence_h(c, x0, x1, y):
    c.put(x0, y, FENCE_L, collision=1)
    for x in range(x0 + 1, x1):
        c.put(x, y, FENCE_M, collision=1)
    c.put(x1, y, FENCE_R, collision=1)


def BUILDINGS_STAMPS(c):
    """Carimba os predios conferindo sobreposicao (nada de predio sobre avenida ou outro predio)."""
    taken = set()
    for (name, x, y, _) in BUILDINGS:
        blocks, _sec = extract(name)
        cells = {(x + dx, y + dy) for dy in range(len(blocks)) for dx in range(len(blocks[0]))}
        clash = cells & taken
        road = {p for p in cells if c.terrain[p[1]][p[0]] == "road"}
        assert not clash and not road, f"{name} em {(x, y)} sobrepoe {sorted(clash | road)[:4]}"
        taken |= cells
        c.stamp(name, x, y)
    return []


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
