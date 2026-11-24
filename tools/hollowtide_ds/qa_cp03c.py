#!/usr/bin/env python3
"""QA dos mapas convertidos do GBA (provas/cp03c): Dawnmere e Route 1 no desenho global das celulas (21,13)-(24,16)
da matriz 0 (origem do desenho = mundo 672, 416). A partir do estado do quarto, o atalho de QA no PC leva a um
caminho de Dawnmere; o robo anda ate a saida leste (GBA 33,21 = desenho 35,23), atravessa a divisa para a Route 1
(header 33) e desce a rota. Capturas em cada ponto. Uso: qa_cp03c.py ROM ESTADO_QUARTO PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import goto

X0, Z0 = 672, 416
CELLS = [(cx, cy) for cx in range(21, 25) for cy in range(13, 17)]
DAWNMERE, ROUTE1 = 60, 33


GRID = os.path.join(os.path.dirname(__file__), "..", "..", "hollowtide_ds", "data", "mapas", "lunia_cap1.txt")


def free_near(x, z):
    """Tile andavel (grama, caminho, flor) mais proximo do alvo, lido da propria grade."""
    lines = open(GRID).read().split("\n"); t = lines.index("[tiles]")
    rows = lines[t + 1:t + 129]
    best = min(((abs(xx - x) + abs(zz - z), xx, zz) for zz in range(len(rows)) for xx in range(len(rows[0]))
                if rows[zz][xx] in ".=f"), default=(0, x, z))
    return best[1], best[2]


def W(x, z):
    x, z = free_near(x, z)
    return (X0 + x, Z0 + z)


def main(rom, state, out):
    os.makedirs(out, exist_ok=True)
    d = DS(rom); d.load(state); d.wait(30)
    log = []
    def step(tag):
        w = d.where(); log.append((tag, w)); d.shot(f"{out}/{tag}.png"); return w
    d.press("UP", 16, 24); d.press("UP", 4, 20); d.press("A", 4, 30)
    for _ in range(20):
        d.wait(30)
        if d.where() and d.where()[0] == DAWNMERE:
            break
    d.wait(120); step("1_dawnmere_chegada")
    for goal, tag in (((15, 12), "2_dawnmere_lab"), ((27, 20), "3_dawnmere_centro"), ((35, 23), "4_saida_leste")):
        goto(d, rom, W(*goal), CELLS, (DAWNMERE, ROUTE1), out, "c", fight_ok=False); step(tag)
    for _ in range(4):
        d.press("RIGHT", 16, 24)
    d.wait(60); r = step("5_route1_entrada")
    for goal, tag in (((44, 30), "6_route1_lago"), ((46, 50), "7_route1_meio"), ((45, 66), "8_route1_sul")):
        goto(d, rom, W(*goal), CELLS, (DAWNMERE, ROUTE1, 67), out, "c", fight_ok=False); step(tag)
    for t, w in log:
        print(f"{t:22} {w}")
    good = log[0][1] and log[0][1][0] == DAWNMERE and r and r[0] == ROUTE1
    print("RESULTADO CP-DS-03B conversao (Dawnmere -> Route 1):", "ok" if good else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
