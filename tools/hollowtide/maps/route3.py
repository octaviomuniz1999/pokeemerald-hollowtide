#!/usr/bin/env python3
"""Route 3 (Rota 03) — sai da praia oeste da Breezeport e sobe a serra ate o planalto de Ferralia.

Progressao (cânone): praia urbanizada -> costa natural -> grama/terra -> encostas com penhascos e escadas ->
serra (mata atlantica) -> planalto -> aproximacao da metropole. Bifurcacoes: trilha principal pelas escadas,
trilha alternativa pela mata (treinadores e item), enseada escondida a oeste e atalho de ladeiras na descida.

Emendas: borda leste (linhas 20-75) = borda oeste da Breezeport (linhas 0-55, offset 20): mata, avenida,
calcadao (56-57), areia (58-67), agua rasa (68-71) e mar (72-75). Borda norte: estrada para Ferralia (x 24-27).
Os patamares (5/7/9) sao so visuais: no fim todo piso andavel vai para a elevacao 3 (as faces de rocha
bloqueiam; escadas ficam em 0), o que deixa as duas emendas no mesmo nivel.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 56, 80
OFFSET_BREEZEPORT = 20        # linha 0 da Breezeport = linha 20 da Route 3
NORTH_ROAD = (24, 27)         # colunas da estrada para Ferralia


def b(x, base, amp, freq, ph):
    return base + round(amp * math.sin(x / freq + ph))


def blob(cx, cy, rx, ry, ph=0.0, amp=(0.12, 0.07)):
    def inside(x, y):
        dx, dy = (x - cx) / rx, (y - cy) / ry
        t = math.atan2(dy, dx)
        r = 1 + amp[0] * math.sin(3 * t + ph) + amp[1] * math.sin(5 * t + 2 * ph)
        return dx * dx + dy * dy <= r * r
    return inside


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    # --- relevo: patamares com contorno organico, de borda a borda (sem paredes laterais) ---
    e5 = {x: b(x, 47, 1.6, 7.0, 0.3) for x in range(W)}
    e7 = {x: b(x, 32, 2.0, 6.0, 1.9) for x in range(W)}
    e9 = {x: b(x, 17, 1.7, 5.0, 4.1) for x in range(W)}
    # a borda fica reta em volta de cada escada (degrau diagonal vira quina de rocha e tranca a subida)
    for e, cols in ((e5, (40,)), (e7, (30, 14)), (e9, (36, 20))):
        for sx in cols:
            for x in range(sx - 2, sx + 4):
                e[x] = e[sx]
    for x in range(W):
        for y in range(H):
            c.level[y][x] = 9 if y <= e9[x] else 7 if y <= e7[x] else 5 if y <= e5[x] else 3
    # --- trilhas (largura 2, na grade par para nao cortar arvores) ---
    paths = []
    def path(x0, y0, x1, y1, cls="sand"):
        c.rect(x0, y0, x1, y1, cls)
        paths.extend((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    S = lambda L, x: max(y for y in range(H) if c.level[y][x] >= L)
    # principal: praia -> escada A -> encosta -> escada B -> serra -> escada C -> planalto -> norte
    path(40, S(5, 40) + 2, 41, 55); c.stairs(40, S(5, 40), 2)
    path(40, 40, 41, S(5, 40) - 1); path(30, 40, 41, 41)
    path(30, S(7, 30) + 2, 31, 41); c.stairs(30, S(7, 30), 2)
    path(30, 26, 31, S(7, 30) - 1); path(30, 26, 37, 27)
    path(36, S(9, 36) + 2, 37, 27); c.stairs(36, S(9, 36), 2)
    path(36, 10, 37, S(9, 36) - 1); path(20, 10, 37, 11)
    path(26, 2, 27, 11); path(NORTH_ROAD[0], 0, NORTH_ROAD[1], 3)
    # alternativa pela mata (oeste): encosta -> escada D -> clareira da serra -> escada E -> planalto
    path(28, 40, 31, 43); path(14, 42, 29, 43)
    path(14, S(7, 14) + 2, 15, 43); c.stairs(14, S(7, 14), 2)
    path(14, 22, 15, S(7, 14) - 1); path(14, 22, 21, 23)
    path(20, S(9, 20) + 2, 21, 23); c.stairs(20, S(9, 20), 2)
    path(20, 10, 21, S(9, 20) - 1)
    stair = set()
    for (x, y) in c.stair_cols:
        stair |= {(x, y), (x, y + 1)}
    paths.extend(stair)
    # --- costa: calcadao que vem da Breezeport, areia, agua rasa e mar ---
    for x in range(W):
        # leste = emenda com a Breezeport; oeste: a praia vira ponta de areia que desce ate a borda (o mar nao
        # encosta na borda oeste, onde o jogo desenharia a moldura de arvores)
        shore = 67 if x >= 40 else b(x, 65, 1.3, 5.0, 0.8) if x >= 12 else min(H - 1, 65 + (12 - x) * 3)
        deep = 71 if x >= 40 else shore + 3 + round(0.8 * math.sin(x / 7.0 + 0.5))
        c.rect(x, 58, x, shore, "sand"); c.rect(x, shore + 1, x, deep, "shallow"); c.rect(x, deep + 1, x, H - 1, "sea")
    c.rect(0, 56, 9, 57, "sand")
    path(38, 56, W - 1, 57, "cobble")                                 # calcadao (termina na praia natural)
    # --- matas ---
    c.forest(lambda x, y: (x >= 44 and y < 52) or (x < 2 and y < 54) or y < 2, paths, margin=0)  # moldura + emenda
    c.forest(blob(8, 40, 9, 5.5, 0.4), paths)                          # encosta oeste
    c.forest(blob(24, 36, 5, 2.4, 1.2), paths)
    c.forest(blob(37, 45, 3.2, 1.6, 2.0), paths)
    c.forest(blob(6, 26, 6, 5, 2.4), paths)                            # serra: mata atlantica
    c.forest(blob(24, 28, 4, 3, 0.9), paths)
    c.forest(blob(40, 22, 5, 4, 3.3), paths)
    c.forest(blob(8, 52, 7, 3, 1.0), paths)                            # restinga com arvores
    c.forest(blob(22, 22, 5, 2.6, 0.2), paths)                         # mais mata no miolo da serra
    c.forest(blob(20, 37, 4, 2.2, 1.7), paths)                         # e na encosta
    c.forest(blob(34, 35, 3, 2.0, 2.9), paths)
    c.forest(blob(28, 6, 3, 2.0, 0.6), paths)                          # bosque no planalto
    c.forest(blob(28, 51, 5, 2.2, 2.2), paths)
    for (x, y) in [(18, 4), (44, 4), (6, 12), (44, 12), (12, 6)]:    # arvores isoladas no planalto
        c.forest(lambda xx, yy, x=x, y=y: x <= xx < x + 2 and y <= yy < y + 2, paths)
    # --- mato alto e flores so sobre grama (nunca corta arvore) ---
    def tall(x0, y0, rows, cls="tall"):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                x, y = x0 + dx, y0 + dy
                if ch != " " and 0 <= x < W and 0 <= y < H and c.terrain[y][x] == "grass":
                    c.terrain[y][x] = cls
    BLOB = ["   ,,,,,,    ", " ,,,,,,,,,,  ", ",,,,,,,,,,,, ", " ,,,,,,,,,,  ", "   ,,,,,     "]
    tall(4, 4, BLOB); tall(30, 4, BLOB); tall(40, 13, BLOB[:4])       # planalto
    tall(16, 30, BLOB[1:4]); tall(33, 30, BLOB[:4])                   # serra
    tall(18, 44, BLOB[:4]); tall(2, 47, BLOB[1:4])                    # encosta / restinga
    tall(14, 52, BLOB[:4]); tall(30, 53, BLOB[1:4])
    tall(16, 24, BLOB); tall(24, 33, BLOB[:3])                        # miolo da serra e da encosta
    tall(20, 15, ["ffff"], "flower"); tall(10, 38, ["ff"], "flower"); tall(33, 44, ["fff"], "flower")
    tall(14, 12, ["ffff"], "flower"); tall(28, 13, ["fff"], "flower"); tall(34, 48, ["ff"], "flower")
    # moldura sem frestas: o que sobrou de grama entre a mata 2x2 e a rocha nas bordas vira mata fechada
    cliffs = c.cliff_cells()
    for y in range(H):
        for x in range(W):
            frame = (x < 2 and y < 56) or y < 2 and not NORTH_ROAD[0] <= x <= NORTH_ROAD[1]
            if frame and (x, y) not in cliffs and c.terrain[y][x] not in ("tree", "sand"):
                c.terrain[y][x] = "dense"
    # --- praia natural: casa de praia, poste no fim do calcadao, pedras ---
    c.stamp("lily_house_blue", 18, 58)
    c.lamp(38, 54, "grass")
    for (x, y) in [(12, 63), (27, 62), (33, 59), (6, 70)]:
        c.put(x, y, 226, collision=1)
    return c


def flatten(bl):
    """Patamares visuais: todo piso andavel elevado vai para 3 (faces de rocha tem colisao; escadas em 0)."""
    out = []
    for v in bl:
        e = v >> 12
        if e in (5, 7, 9) and (v >> 10) & 3 == 0:
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
