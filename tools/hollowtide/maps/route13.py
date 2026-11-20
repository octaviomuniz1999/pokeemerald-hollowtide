#!/usr/bin/env python3
"""Route 13 (Mirror Grove) — rota opcional a leste da Route 7, 40x32 (General + Lavaridge, como a Route 7).

Um bosque fechado: a trilha entra pela borda oeste (linhas 16-17, alinhadas com a trilha do Circulo da Lua na
Route 7: Route 13 y = Route 7 y - 8) e da a volta no bosque em anel. Lagoas paradas como espelhos entre as
arvores, uma clareira no meio com pedras em roda e um desvio a leste que termina num recanto escondido.
Pokemon do canone (POKEDEX_LUNIA): Zorua de Hisui (raro), Mime Jr., Shuppet, Litwick, Foongus.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 40, 32
WEST = (16, 17)               # entrada oeste (linhas) = Route 7 linhas 24-25
OFFSET_ROUTE07 = 8            # Route 13 y = Route 7 y - 8
PONDS = [(12, 12, 15, 14), (33, 9, 36, 11), (3, 22, 6, 25), (14, 20, 17, 21)]
CLEARING = (16, 12, 23, 19)
STONES = [(17, 13), (22, 13), (17, 18), (22, 18)]


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lavaridge")
    c.fill("grass")
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(0, WEST[0], 9, WEST[1])                       # entrada
    path(8, 5, 9, 26)                                  # anel: lado oeste
    path(8, 5, 19, 6); path(18, 5, 19, 8)              # anel: norte, com degrau
    path(18, 7, 31, 8)
    path(30, 7, 31, 24)                                # anel: leste
    path(20, 23, 31, 24); path(20, 23, 21, 26)         # anel: sul, com degrau
    path(8, 25, 21, 26)
    path(23, 9, 24, CLEARING[1] - 1)                   # do anel a clareira
    path(32, 15, 36, 16)                               # desvio ao recanto
    for (x0, y0, x1, y1) in PONDS:
        c.rect(x0, y0, x1, y1, "pond")
    c.rect(*CLEARING, "grass")
    c.rect(18, 15, 21, 16, "flower")
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = "tall"
    tall(10, 8, [",,,,,,", ",,,,,", " ,,,"])         # dentro do anel, a noroeste
    tall(25, 10, [",,,,", ",,,,", " ,,"])              # dentro do anel, a nordeste
    tall(10, 21, [",,,,,", ",,,,,,", " ,,,"])         # dentro do anel, a sudoeste
    tall(2, 18, [",,,,", ",,,,", ",,,"])              # fora do anel, a oeste
    tall(33, 19, [",,,,", ",,,,,", ",,,"])            # fora do anel, a leste
    clearing = {(x, y) for x in range(CLEARING[0], CLEARING[2] + 1) for y in range(CLEARING[1], CLEARING[3] + 1)}
    open_cells = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] != "grass"} | clearing
    near_path = {(x + dx, y + dy) for (x, y) in paths for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    # mata fechada: encosta no mato alto, nas lagoas e na clareira; deixa 1 tile de grama ao lado da trilha
    c.forest(lambda x, y: not any((int(x - 0.5) + dx, int(y - 0.5) + dy) in near_path for dx in (0, 1) for dy in (0, 1)),
             open_cells, margin=0)
    for (x, y) in STONES:
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
