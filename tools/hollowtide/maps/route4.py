#!/usr/bin/env python3
"""Route 4 (Estrada das Caravanas) — Ferralia -> Tradepost, 52x32 (General + Rustboro, como Ferralia e Tradepost).

Linha ferrea ao norte (linhas 2 e 8), continuacao do patio de carga de Ferralia: leito fechado (trilhos com
colisao, cerca viva de arvores abaixo) — a ferrovia so abre no capitulo do Hoc. Estrada das caravanas nas
linhas 16-17 (= avenida "Paulista" de Ferralia, offset 24), antigo abrigo de carga, canal com a unica
ponte a pe (x 29-34), mirante a nordeste (desafio opcional), desvios com itens e mata ao sul.
"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 52, 32
OFFSET_FERRALIA = 24          # linha 0 da Route 4 = linha 24 da Ferralia
ROAD = (16, 17)
RAILS = (2, 8)
CANAL = (29, 34)
BRIDGE = (836, 844, 845)      # tabuado horizontal da Route 104 (topo, meio andaveis; sombra bloqueada)


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Rustboro")
    c.fill("grass")
    ids = json.load(open(os.path.join(os.path.dirname(__file__), "..", "mapgen", "custom_ids.json")))["rustboro"]
    # --- moldura e corredor ferroviario (inacessivel) ---
    c.rect(0, 0, W - 1, 1, "tree")
    c.rect(0, 9, W - 1, 9, "sand")                 # acostamento do leito
    for x in range(4, W - 2, 12):                  # entre as linhas: capim e arvores esparsas
        c.rect(x, 4, x + 1, 5, "tree")
    c.rect(10, 4, 13, 6, "tall"); c.rect(34, 4, 37, 6, "tall")
    c.rect(0, 10, W - 1, 11, "tree")               # cerca viva separando a ferrovia da estrada
    # --- canal (entra pela borda sul; nasce numa bacia com margem logo abaixo da cerca viva) ---
    c.rect(CANAL[0], 12, CANAL[1], H - 1, "pond")
    # --- estrada das caravanas ---
    c.rect(0, ROAD[0], 5, ROAD[1], "road")
    c.rect(6, ROAD[0], W - 1, ROAD[1], "sand")
    c.rect(10, 18, 13, 22, "sand"); c.rect(10, 22, 17, 23, "sand")      # desvio sul (frutas)
    c.rect(18, 12, 19, 15, "sand")                                      # desvio norte (item)
    c.rect(40, 12, 47, 13, "sand"); c.rect(40, 14, 41, 15, "sand")      # subida ao mirante (NE)
    # --- matas e mato alto ---
    paths = {(x, y) for y in range(H) for x in range(W) if c.terrain[y][x] in ("sand", "road", "pond")}
    c.forest(lambda x, y: y >= 26, paths)                               # mata ao sul (o canal a atravessa)
    def blob(cx, cy, rx, ry):
        return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
    for b in [blob(3, 21, 3, 4), blob(23, 21, 4, 3), blob(39, 22, 4, 3), blob(49, 21, 3, 4), blob(25, 13, 3, 1.5),
              blob(50, 13, 2, 2)]:
        c.forest(b, paths)
    def tall(x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = "tall"
    BL = ["  ,,,,,,  ", ",,,,,,,,,,", ",,,,,,,,,,", "  ,,,,,,  "]
    tall(14, 19, BL); tall(42, 19, BL); tall(20, 12, BL[:3]); tall(35, 12, ["  ,,,", ",,,,,", ",,,,,"])
    c.rect(6, 20, 8, 20, "flower"); c.rect(44, 14, 46, 14, "flower")
    # --- antigo abrigo de carga (sobre a cerca viva, de frente para a estrada) ---
    c.stamp("rb_office_long", 3, 10)
    # --- trilhos (por cima de tudo; colisao: o leito e fechado) ---
    for ry in RAILS:
        for x in range(W):
            c.put(x, ry, ids["rail_h"], collision=1)
    # --- ponte: tabuado horizontal sobre o canal, na linha da estrada ---
    for x in range(CANAL[0], CANAL[1] + 1):
        c.put(x, ROAD[0], BRIDGE[0], collision=0, elevation=3)
        c.put(x, ROAD[1], BRIDGE[1], collision=0, elevation=3)
        c.put(x, ROAD[1] + 1, BRIDGE[2], collision=1, elevation=3)
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
