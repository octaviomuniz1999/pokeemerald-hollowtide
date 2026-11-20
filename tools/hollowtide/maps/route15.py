#!/usr/bin/env python3
"""Route 15 (Coastal Grotto) — rota opcional a oeste da Route 11, 40x36 (General + Lilycove, como a Route 11).

A praia da Route 11 continua para o oeste (mesmas linhas: areia 25-28, agua rasa 29, mar 30+; offset 0). As
falesias da serra fecham o norte e, numa reentrancia da rocha, ficam a gruta: um recanto de areia com uma poca de
mare. A oeste, uma enseada de mar aberta entre as dunas; mato alto nas dunas. Sem Surf no jogo: os Pokemon de agua
vem pela pesca (Super Rod) e o mato das dunas tem os de praia.
Pokemon do canone (POKEDEX_LUNIA): Shellder, Clamperl, Relicanth (raro), Corsola, Dhelmise.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 40, 36
OFFSET_ROUTE11 = 0
EAST_ROWS = (25, 28)                     # faixa de areia andavel na emenda
CLIFF = [(2, 2, 37, 13)]                 # serra (patamar so visual)
GROTTO = (24, 6, 31, 13)                 # reentrancia da rocha (a gruta), areia
POOL = (26, 8, 29, 9)                    # poca de mare dentro da gruta
COVE_SEA = (6, 20, 17, 29)               # enseada


def blob(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    for (x0, y0, x1, y1) in CLIFF:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c.level[y][x] = 5
    for y in range(GROTTO[1], GROTTO[3] + 1):
        for x in range(GROTTO[0], GROTTO[2] + 1):
            c.level[y][x] = 3
    c.rect(*GROTTO, "sand")
    c.rect(*POOL, "shallow")
    # costa: igual a Route 11 na emenda
    c.rect(0, 30, W - 1, H - 1, "sea")
    c.rect(0, 29, W - 1, 29, "shallow")
    c.rect(0, 25, W - 1, 28, "sand")
    # enseada: areia em volta, agua rasa na borda, mar no meio
    c.rect(COVE_SEA[0] - 3, COVE_SEA[1] - 3, COVE_SEA[2] + 3, 28, "sand")
    c.rect(COVE_SEA[0] - 1, COVE_SEA[1] - 1, COVE_SEA[2] + 1, 29, "shallow")
    c.rect(*COVE_SEA, "sea")
    c.rect(18, 24, 19, 29, "shallow")
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    path(27, GROTTO[3] + 1, 28, 24)                     # da praia ate a gruta
    open_cells = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] != "grass"} | set(paths)
    cliff = {(x, y) for y in range(H) for x in range(W) if c.level[y][x] >= 5}
    c.forest(lambda x, y: (x < 2 or x >= W - 2) and y < 25 or y < 2, open_cells, margin=0)
    for b in [blob(35, 18, 3, 3), blob(21, 16, 2, 2), blob(4, 15, 2, 1.5)]:
        c.forest(b, open_cells | cliff)
    top = {(x, y) for y in range(H) for x in range(W) if c.level[y][x] >= 5}
    c.forest(lambda x, y: (int(x), int(y)) in top and (int(x) + 1, int(y) + 1) in top, open_cells, margin=0)   # mata no alto da serra
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass" and c.level[y][x] == 3:
                    c.terrain[y][x] = "tall"
    tall(29, 19, [" ,,,,", ",,,,,,", ",,,,,", " ,,,"])        # dunas a leste
    tall(21, 19, [",,,,", ",,,,,", ",,,"])                    # dunas a oeste da trilha
    c.rect(32, 15, 34, 15, "flower")
    for (x, y) in [(23, 27), (34, 26), (4, 26), (19, 18)]:      # pedras na areia
        if c.terrain[y][x] == "sand":
            c.put(x, y, 226, collision=1)
    return c


def flatten(bl):
    """Serra so visual (elevacao 3 nos tiles andaveis), como na Route 11."""
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
