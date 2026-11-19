#!/usr/bin/env python3
"""Breezeport City (Cidade da Brisa) — v2. Cidade costeira ampla inspirada no Rio de Janeiro (referencia, nao copia).

Norte: entrada da Route 2 (x 18-21) e o Morro (plato florestado com mirante). Centro: avenida principal,
Centro Pokemon junto a entrada, Mart, praca com canteiros, Teatro dos Ecos (ginasio da Jay).
Oeste e leste: bairros com quintais cercados. Orla: avenida, predios altos, calcadao com postes, praia longa.
Leste: pontal de areia (farol virá em etapa propria). Oeste: praia segue ate a borda -> Route 3.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 72, 56
ENTRADA_ROUTE2 = (18, 21)   # colunas da rua que chega do norte
SAIDA_ROUTE3 = (37, 45)     # linhas da faixa de praia na borda oeste


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
    # --- Morro (patamares 5/7/9 de contorno irregular; mata nas encostas; mirante no cume) ---
    c.rect(24, 2, 63, 16, "dense")             # base de mata da encosta
    c.levels(26, 2, [
        "   55555555555555555555555555555555  ",
        "  5555555555555555555555555555555555 ",
        " 555555577777777777777777777755555555",
        " 555555777777777777777777777775555555",
        " 555557777777799999999997777777555555",
        "  55557777777999999999999777777555555",
        "  55557777777999999999999777777555555",
        "   5557777777799999999997777777555555",
        "   555577777777777777777777777555555 ",
        "    55557777777777777777777777555555 ",
        "     555555555777777777555555555555  ",
        "      555555555555555555555555555    ",
        "        55555555555555555555555      ",
    ])
    c.rect(41, 6, 48, 9, "grass")              # mirante no cume (nivel 9)
    c.rect(42, 6, 47, 6, "flower")
    c.rect(44, 10, 45, 13, "cobble")            # trilha descendo pelos patamares
    c.stairs(44, 9, 2); c.stairs(44, 12, 2); c.stairs(44, 14, 2)
    # --- ruas ---
    c.rect(ENTRADA_ROUTE2[0], 0, ENTRADA_ROUTE2[1], 17, "cobble")
    c.rect(2, 18, W - 3, 19, "cobble")    # avenida principal
    c.rect(44, 16, 45, 17, "cobble")      # pe da escadaria do morro
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
    c.rect(0, 38, W - 1, 46, "sand")
    c.rect(0, 47, W - 1, H - 1, "sea")
    c.rect(0, 45, 55, 46, "shallow")      # faixa de agua rasa na arrebentacao (para antes do pontal)
    c.rect(58, 44, 69, 50, "sand")         # pontal leste
    c.rect(61, 51, 67, 52, "sand")
    c.stamp("lily_harbor", 60, 38)         # casa do faroleiro (provisoria)
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
