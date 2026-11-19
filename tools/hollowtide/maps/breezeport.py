#!/usr/bin/env python3
"""Breezeport City (Cidade da Brisa) — v2. Cidade costeira ampla inspirada no Rio de Janeiro (referencia, nao copia).

Norte: entrada da Route 2 (x 18-21) e o Morro (plato florestado com mirante). Centro: avenida principal,
Centro Pokemon junto a entrada, Mart, praca com canteiros, Teatro dos Ecos (ginasio da Jay).
Oeste e leste: bairros com quintais cercados. Orla: avenida, predios altos, calcadao com postes, praia longa.
Leste: pontal de areia (farol virá em etapa propria). Oeste: praia segue ate a borda -> Route 3.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 72, 56
ENTRADA_ROUTE2 = (18, 21)   # colunas da rua que chega do norte
SAIDA_ROUTE3 = (37, 45)     # linhas da faixa de praia na borda oeste


def _inside(x, y, cx, cy, rx, ry, phase, amp):
    """Contorno organico: elipse com ondulacao de baixa frequencia (sem degraus repetitivos)."""
    dx, dy = (x - cx) / rx, (y - cy) / ry
    t = math.atan2(dy, dx)
    r = 1 + amp[0] * math.sin(3 * t + phase) + amp[1] * math.sin(5 * t + 2 * phase)
    return dx * dx + dy * dy <= r * r


def morro(c, X0=22, X1=66, Y0=2, Y1=16):
    """Morro tipo Corcovado (referencia): mata 2x2 quantizada na grade par, patamar e cume. Devolve as linhas
    da borda sul de cada nivel na coluna da escadaria (44)."""
    for by in range(Y0 & ~1, Y1 + 1, 2):
        for bx in range(X0 & ~1, X1 + 1, 2):
            if _inside(bx + 0.5, by + 0.5, 44, 8.5, 21, 8.5, 0.7, (0.08, 0.05)):
                c.rect(bx, by, bx + 1, by + 1, "tree")
    for L, (cx, cy, rx, ry, ph, amp) in ((5, (44.5, 8.0, 14, 5.4, 2.1, (0.09, 0.05))),
                                         (7, (44.5, 6.0, 6.5, 2.4, 4.0, (0.06, 0.03)))):
        for y in range(Y0, Y1 + 1):
            for x in range(X0, X1 + 1):
                if _inside(x, y, cx, cy, rx, ry, ph, amp):
                    c.level[y][x] = L
                    c.terrain[y][x] = "grass"
    south = lambda L: max(y for y in range(Y0, Y1 + 1) if c.level[y][44] >= L)
    return south(5), south(7)


def house_yard(c, x, y, flowers_left=True):
    """Casa 4x4 com quintal: canteiro de flores na frente e cerca no fundo."""
    c.stamp("lily_house_blue", x, y)
    c.fence_h(x - 1, x + 4, y + 4 + 1) if False else None
    fx = x - 2 if flowers_left else x + 4
    c.rect(fx, y + 2, fx + 1, y + 3, "flower")


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    # moldura de mata (norte e laterais ate a orla)
    c.rect(0, 0, W - 1, 1, "tree")
    c.rect(0, 0, 1, 31, "tree")
    c.rect(W - 2, 0, W - 1, 31, "tree")
    # --- Morro: mata de arvores 2x2, patamar (5) e cume-mirante (7) de contorno organico; escadaria ao sul ---
    e5, e7 = morro(c)
    c.rect(44, e5 + 2, 45, 17, "cobble"); c.stairs(44, e5, 2)        # avenida -> patamar
    c.rect(44, e7 + 2, 45, e5 - 1, "cobble"); c.stairs(44, e7, 2)    # patamar -> cume
    for (x, y) in [(36, 10), (52, 10)]:                                # arvores no patamar (2x2 inteiras)
        c.rect(x, y, x + 1, y + 1, "tree")
    c.rect(39, 11, 41, 11, "flower"); c.rect(48, 11, 50, 11, "flower")
    c.rect(41, 5, 42, 5, "flower"); c.rect(47, 5, 48, 5, "flower")     # cume florido
    # --- ruas ---
    c.rect(ENTRADA_ROUTE2[0], 0, ENTRADA_ROUTE2[1], 17, "cobble")
    c.rect(2, 18, W - 3, 19, "cobble")    # avenida principal
    c.rect(10, 20, 11, 33, "cobble")      # rua do bairro oeste
    c.rect(60, 20, 61, 33, "cobble")      # rua do bairro leste
    c.rect(2, 34, W - 3, 35, "cobble")    # avenida da orla
    # --- praca central e teatro ---
    c.rect(26, 21, 41, 30, "cobble")
    c.rect(28, 23, 30, 24, "flower"); c.rect(37, 23, 39, 24, "flower")
    c.rect(28, 27, 30, 28, "flower"); c.rect(37, 27, 39, 28, "flower")
    c.rect(32, 24, 35, 27, "grass")              # canteiro de grama com arvore no centro
    c.small_tree(33, 25)
    for (x, y) in [(27, 22), (40, 22), (27, 28), (40, 28)]:
        c.lamp(x, y, "cobble")
    c.stamp("lily_contest_hall", 44, 21)          # Teatro dos Ecos
    c.rect(43, 28, 51, 29, "cobble")              # adro do teatro
    c.lamp(43, 26, "grass"); c.lamp(51, 26, "grass")
    # --- parque noroeste (bosque com clareira florida e poste) ---
    c.rect(2, 2, 15, 11, "tree")
    c.rect(4, 6, 11, 9, "grass"); c.rect(5, 7, 10, 8, "flower")
    c.lamp(8, 5, "grass") if False else None
    c.rect(2, 12, 11, 13, "tall")
    # --- servicos junto a entrada ---
    c.stamp("gen_pokecenter", 22, 13)
    c.rect(22, 17, 25, 17, "cobble")
    c.stamp("gen_mart", 13, 14)
    c.rect(13, 17, 16, 17, "cobble")
    # --- bairro oeste ---
    for (x, y, fl) in [(3, 21, False), (3, 27, False), (14, 21, True), (14, 27, True)]:
        house_yard(c, x, y, fl)
    c.small_tree(20, 23)
    # --- bairro leste: loja de departamentos (com cobertura) e casas ---
    c.dept_store(52, 25)
    c.rect(53, 21, 57, 22, "flower")
    for (x, y, fl) in [(63, 21, False), (63, 27, False)]:
        house_yard(c, x, y, fl)
    # --- arvores de rua (sobre grama, com uma linha de respiro ate a avenida) ---
    c.small_tree(6, 31); c.small_tree(22, 31); c.small_tree(46, 31)
    # --- calcadao + praia + mar ---
    c.rect(0, 36, W - 1, 37, "cobble")
    for x in range(4, W - 3, 8):
        if x != 60:
            c.lamp(x, 34, "cobble")
    # praia: linha de costa organica, faixa de agua rasa (laguna mais larga no centro-oeste), mar fundo
    shore, deep = {}, {}
    for x in range(W):
        shore[x] = 46 + round(1.4 * math.sin(x / 9.0 + 0.6))  # ondas longas: degraus de 1 tile espacados
        lagoon = round(3.0 * math.exp(-((x - 19) / 8.0) ** 2))
        deep[x] = shore[x] + 3 + round(0.8 * math.sin(x / 11.0 + 1.0)) + lagoon
    for _ in range(2):                                         # sem colunas isoladas (degraus de 1 tile so)
        for x in range(1, W - 1):
            if deep[x - 1] == deep[x + 1] != deep[x]:
                deep[x] = deep[x - 1]
    for x in range(W):
        c.rect(x, 38, x, shore[x], "sand")
        c.rect(x, shore[x] + 1, x, deep[x], "shallow")
        c.rect(x, deep[x] + 1, x, H - 1, "sea")
    by = shore[19] + 2
    assert min(deep[x] for x in range(15, 22)) >= by + 3, "banco de areia encostaria no mar fundo"
    c.rect(16, by, 19, by + 1, "sand")                 # banco de areia na laguna (cercado de agua rasa)
    # pontal leste: nasce da praia; anel de agua rasa so onde antes era agua
    for x in range(57, 71):
        for y in range(44, 55):
            if y > shore[x]:
                c.rect(x, y, x, y, "shallow")
    c.rect(58, 44, 69, 50, "sand")
    c.rect(61, 51, 67, 52, "sand")
    c.stamp("lily_harbor", 60, 38)         # casa do faroleiro
    c.lamp(64, 51, "sand")                  # farol provisorio na ponta do pontal (o farol caiu na tempestade)
    # pedras: na areia (226), na agua rasa (404), rochedo no mar (2x2) e o rochedo do antigo farol (3x4)
    for (x, y) in [(8, 41), (29, 43), (51, 40), (66, 47)]:
        c.put(x, y, 226, collision=1)
    for x in (5, 33, 46):
        c.put(x, shore[x] + 1, 404, collision=1, elevation=0) if deep[x] > shore[x] + 1 else None
    for (dx, dy), m in zip([(0, 0), (1, 0), (0, 1), (1, 1)], [373, 374, 381, 382]):
        c.put(26 + dx, 52 + dy, m, collision=1, elevation=0)
    for dy, row in enumerate([(370, 379, 372), (378, 113, 380), (378, 113, 380), (386, 121, 388)]):
        for dx, m in enumerate(row):
            c.put(49 + dx, 51 + dy, m, collision=1, elevation=0)
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
    print(render(compose(), sys.argv[1]))
