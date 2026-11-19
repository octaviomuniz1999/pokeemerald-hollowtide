#!/usr/bin/env python3
"""Horizon City ("As Aguas do Horizonte") — 56x44, General + Lilycove.

Um lago cercado de mata ocupa o norte; a orla tem um jardim (que a agua invadiu: o lago esta subindo sem
chuva) e um passeio calcado com postes. A estacao de controle do lago (por onde se desce a estacao sob a
agua) fica na margem oeste; o Pavilhao das Estrelas (observatorio) na margem leste; o ginasio da Chelsia
(cupula) a leste do centro; Centro Pokemon, Mart e casas a oeste e ao sul. Entrada sul pela Route 7
(colunas 26-27; Horizon x = Route 7 x + 10); saida norte (colunas 52-53) para a Route 8, fechada por enquanto.
compose(flooded=True) = jardim alagado; compose(False) = depois do evento (agua baixou).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 56, 44
SOUTH = (26, 27)
NORTH = (52, 53)
OFFSET_ROUTE7 = 10        # Horizon x = Route 7 x + 10
PROM = (20, 21)           # passeio da orla
STREET = (32, 33)         # rua dos bairros
SEAM = 36                 # da linha 36 ao fim so primario (a Route 7 enxerga ~7 linhas)
LAKE = [(18, 5, 33, 6), (14, 7, 37, 8), (11, 9, 39, 15), (13, 16, 37, 17)]
GARDEN = (13, 18, 37, 19)                                         # jardim da orla (alagado antes do evento)
BUILDINGS = [
    ("lily_harbor", 2, 10, "station"),          # estacao de controle do lago (desce para a estacao sob a agua)
    ("lily_museum", 42, 4, "pavilion"),         # Pavilhao das Estrelas
    ("lily_pokecenter", 6, 25, "pc"),
    ("gen_mart", 13, 26, "mart"),
    ("lily_contest_hall", 36, 23, "gym"),       # ginasio da Chelsia (cupula)
    ("lily_house_blue", 5, 33, "house_1"),
    ("lily_house_blue", 12, 33, "house_2"),
    ("lily_house_blue", 46, 25, "house_3"),
]
DOOR_OFF = {"lily_harbor": (3, 5), "lily_museum": (4, 5), "lily_pokecenter": (1, 3), "gen_mart": (1, 2),
            "lily_contest_hall": (3, 6), "lily_house_blue": (1, 3)}
LAMPS = [(9, 22), (19, 22), (33, 22), (44, 22), (22, 30), (31, 30)]


def door(label):
    for (name, x, y, lab) in BUILDINGS:
        if lab == label:
            dx, dy = DOOR_OFF[name]
            return x + dx, y + dy
    raise KeyError(label)


def compose(flooded=True):
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    paths = []
    def path(x0, y0, x1, y1, cls="cobble"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    # lago e jardim da orla
    for (x0, y0, x1, y1) in LAKE:
        c.rect(x0, y0, x1, y1, "pond")
    gx0, gy0, gx1, gy1 = GARDEN
    if flooded:
        c.rect(gx0, gy0, gx1, gy1, "pond")
    else:
        for x in range(gx0, gx1 + 1):
            c.terrain[gy0][x] = "flower" if x % 3 else "grass"
            c.terrain[gy1][x] = "grass" if x % 3 else "flower"
    # passeio da orla, avenida sul, rua dos bairros e acessos
    path(4, PROM[0], NORTH[1], PROM[1])
    path(SOUTH[0], PROM[1], SOUTH[1], H - 1)
    path(4, STREET[0], 51, STREET[1])
    path(NORTH[0], 0, NORTH[1], PROM[1])
    for (name, x, y, label) in BUILDINGS:
        c.stamp(name, x, y)
    # o carimbo do pavilhao traz pedacos de arvore e margem da Lilycove nos cantos de cima: vira grama
    for (name, x, y, _) in BUILDINGS:
        if name == "lily_museum":
            for (dx, dy) in ((0, 0), (1, 0), (8, 0), (9, 0), (0, 1), (1, 1), (8, 1), (9, 1)):
                c.put(x + dx, y + dy, 1, collision=0)
                c.terrain[y + dy][x + dx] = "grass"
    sx, sy = door("station"); path(sx, sy + 1, sx, PROM[0] - 1)
    px, py = door("pavilion"); path(px, py + 4, px + 1, PROM[0] - 1)     # da escada do pavilhao ao passeio
    for label in ("pc", "mart", "gym", "house_3"):
        x, y = door(label); path(x, y + 1, x, STREET[0] - 1 if label != "house_3" else STREET[0] - 1)
    for label in ("house_1", "house_2"):
        x, y = door(label); path(x, y + 1, x, 38, "sand")
    path(6, 38, SOUTH[0] - 1, 39, "sand")                                  # vila sul (terra: a Route 7 enxerga)
    path(SOUTH[0], SEAM, SOUTH[1], H - 1, "sand")                          # fim da avenida vira estrada de terra
    # canteiros e pracinha do cruzamento
    c.rect(29, 24, 33, 28, "grass"); c.rect(30, 25, 32, 27, "flower")
    c.rect(19, 24, 23, 28, "grass"); c.rect(20, 25, 22, 27, "flower")
    c.rect(29, 35, 34, 37, "flower"); c.rect(40, 35, 44, 36, "flower"); c.rect(16, 36, 20, 36, "flower")
    for (x, y) in LAMPS:
        c.lamp(x, y, floor="grass")
    # mata: moldura e bosques (fora das trilhas, agua e construcoes)
    water = {(x, y) for (x0, y0, x1, y1) in LAKE + [GARDEN] for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    blocks = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] == "other"}
    lamps = {(x, y + d) for (x, y) in LAMPS for d in (0, 1)}
    avoid = set(paths) | water | blocks | lamps
    c.forest(lambda x, y: x < 2 or x >= W - 2 or y < 2 or y >= H - 2, avoid, margin=0)
    def blob(cx, cy, rx, ry):
        return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
    for b in [blob(6, 4, 5, 3), blob(40, 2, 3, 1.5), blob(10, 2, 8, 1), blob(26, 2.5, 13, 1.5), blob(46, 2, 3, 1.5),
              blob(48, 14, 4, 3), blob(44, 40, 6, 2.5), blob(36, 41, 4, 1.5), blob(16, 42, 6, 1.2),
              blob(53, 30, 1.5, 6), blob(3, 28, 1.5, 4), blob(40, 31, 1.5, 1.5)]:
        c.forest(b, avoid)
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
    c = compose(len(sys.argv) < 3)
    print("coesao:", c.check_cohesion())
    print(render(c, sys.argv[1]))
