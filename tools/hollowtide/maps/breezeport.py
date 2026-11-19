#!/usr/bin/env python3
"""Breezeport City (Cidade da Brisa) — cidade costeira ampla inspirada no Rio de Janeiro.

Leitura de cima para baixo: entrada da Route 2 (norte) -> morro florestado com mirante (Corcovado como
referencia, nao copia) -> bairros e centro (Centro Pokemon, Mart, praca, Teatro da Jay) -> avenida da orla com
predios altos e postes -> calcadao -> praia longa -> mar. Ponta rochosa a leste reservada ao farol.
Saida para a Route 3 a oeste, pela faixa de praia.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mapgen"))
from canvas import Canvas

W, H = 72, 56


def compose():
    c = Canvas(W, H, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass")
    # moldura de mata nas bordas norte/leste (cidade encaixada entre morro e mar)
    c.rect(0, 0, W - 1, 1, "tree")
    c.rect(0, 0, 1, 33, "tree")
    c.rect(W - 2, 0, W - 1, 27, "tree")
    # entrada da Route 2 no norte (x 18-21)
    c.rect(18, 0, 21, 1, "cobble")
    # Morro (centro-norte): mata densa com trilha em zigue-zague ate o mirante
    c.rect(28, 2, 55, 15, "dense")
    c.rect(32, 2, 51, 3, "tree")
    c.ascii(30, 4, [
        "TT..........................",
        "TT.cccccccccccccccccccccc..TT",
    ])
    c.rect(38, 6, 45, 9, "grass")          # plato do mirante
    c.rect(41, 9, 42, 15, "cobble")         # escadaria/trilha descendo
    # rua principal leste-oeste (avenida do centro)
    c.rect(2, 17, W - 3, 18, "cobble")
    c.rect(18, 2, 21, 16, "cobble")         # rua vinda da Route 2
    # bairro oeste (residencial): ruas transversais
    c.rect(6, 19, 7, 33, "cobble")
    c.rect(16, 19, 17, 33, "cobble")
    # praca central com flores
    c.rect(30, 20, 41, 27, "cobble")
    c.rect(33, 22, 38, 25, "flower")
    # avenida da orla
    c.rect(2, 34, W - 3, 35, "cobble")
    # calcadao (faixa larga de pedra) + praia + mar
    c.rect(0, 36, W - 1, 37, "cobble")
    c.rect(0, 38, W - 1, 46, "sand")
    c.rect(0, 47, W - 1, H - 1, "sea")
    # saida oeste para a Route 3: faixa de praia continua ate a borda (x=0, y 38-46)
    # ponta rochosa leste (farol): areia avancando no mar
    c.rect(60, 40, 69, 50, "sand")
    c.rect(62, 51, 67, 53, "sand")

    # predios
    c.stamp("lily_pokecenter", 22, 12)
    c.stamp("lily_contest_hall", 44, 19)     # Teatro dos Ecos (ginasio da Jay)
    c.stamp("lily_dept_store", 24, 27)       # edificio da orla 1
    c.stamp("lily_motel", 52, 28)            # edificio da orla 2 (hotel)
    for i, (x, y) in enumerate([(2, 20), (9, 20), (2, 27), (9, 27), (19, 20)]):
        c.stamp("lily_house_blue", x, y)
    c.stamp("lily_harbor", 60, 33)
    # postes ao longo do calcadao
    for x in range(4, W - 4, 8):
        c.stamp("lily_lamp", x, 35)
    return c


if __name__ == "__main__":
    c = compose()
    out = sys.argv[1] if len(sys.argv) > 1 else None
    if out:
        bl = c.build()
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "hollowtide_qa"))
        import render_map as R
        from PIL import Image
        ts = R.TilesetPair(c.primary, c.secondary)
        im = Image.new("RGB", (W * 16, H * 16))
        for i, v in enumerate(bl):
            im.paste(ts.metatile(v & 0x3FF), ((i % W) * 16, (i // W) * 16))
        im.save(out)
        print("render:", out)
