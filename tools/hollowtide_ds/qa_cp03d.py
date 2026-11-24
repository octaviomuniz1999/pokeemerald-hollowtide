#!/usr/bin/env python3
"""QA dos eventos de Dawnmere nas posicoes do GBA (provas/cp03c com 0922/0923), pelo fluxo do jogo, sem atalho:
quarto -> mae -> porta da casa do jogador (GBA 2,9) -> placa da casa -> saida leste sem Pokemon (trava, um passo para
oeste) -> placa do laboratorio -> porta do laboratorio -> Prof. Alex e o inicial -> volta pela porta -> guia ->
saida leste com Pokemon -> Route 1 (header 33). Capturas em cada passo.
Uso: qa_cp03d.py ROM ESTADO_QUARTO PASTA   (ESTADO_QUARTO de ds_intro.py na mesma ROM)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import walk, goto, face, advance, starter_screen

X0, Z0 = 672, 416
CELLS = [(cx, cy) for cx in range(21, 25) for cy in range(13, 17)]
DAWNMERE, ROUTE1, LAB = 60, 33, 61
NPCS = {(697, 436), (685, 442), (697, 428)}              # guia, vizinho, mirante (fora da colisao dos blocos)


def g(x, z):
    return (X0 + x, Z0 + z)


def main(rom, state, out):
    os.makedirs(out, exist_ok=True)
    d = DS(rom); d.load(state); d.wait(30)
    log = []

    def step(tag, extra=""):
        w = d.where(); log.append((tag, w, extra)); d.shot(f"{out}/{tag}.png"); print(tag, w, flush=True); return w

    def go(goal, tag):
        try:
            goto(d, rom, goal, CELLS, (DAWNMERE, ROUTE1), out, tag, fight_ok=False, avoid=NPCS)
        except KeyError:                                  # alvo inalcancavel de onde o robo esta: registra e segue
            print("sem caminho de", d.where(), "ate", goal)
        return d.where()

    def ler(tag):
        face(d, "UP"); d.press("A", 4, 60); d.wait(40); step(tag); advance(d, 8); d.wait(30)

    walk(d, ["UP", "UP", "LEFT", "LEFT", "LEFT", "UP", "LEFT", "LEFT"]); d.wait(200)
    advance(d, 45); d.wait(60)
    walk(d, ["DOWN"] * 8, stop_map=DAWNMERE); d.wait(200); advance(d, 6)
    step("1_porta_da_casa", "esperado (60, 676, 428): um passo abaixo da porta do GBA (2,9)")
    go(g(13, 22), "c"); ler("2_placa_da_casa")
    go(g(30, 23), "c"); d.press("RIGHT", 16, 24); d.wait(40)
    step("3_trava_leste")
    advance(d, 25); d.wait(90)
    step("4_depois_da_trava", "esperado x 702 (um passo para oeste)")
    go(g(17, 12), "c"); ler("5_placa_do_lab")
    go(g(15, 12), "c")
    walk(d, ["UP"] * 4, stop_map=LAB); d.wait(200)
    step("6_lab")
    walk(d, ["UP"] * 8 + ["RIGHT"] * 2 + ["UP"])
    d.press("A", 4, 60)
    for _ in range(60):
        if starter_screen(d):
            break
        d.press("A", 4, 50)
    for _ in range(6):
        if not starter_screen(d):
            break
        d.wait(300); d.press("A", 4, 120)
        d.touch(128, 110, 8, 150); d.touch(128, 110, 8, 150)
        for _ in range(10):
            d.wait(30)
    for _ in range(40):
        d.wait(30)
    advance(d, 70); step("7_inicial")
    walk(d, ["LEFT", "LEFT"] + ["DOWN"] * 9, stop_map=DAWNMERE); d.wait(200); advance(d, 4)
    step("8_saida_do_lab", "esperado (60, 687, 427): abaixo da porta do laboratorio")
    go(g(25, 21), "c"); ler("9_guia")
    go(g(31, 23), "c")
    for _ in range(5):
        d.press("RIGHT", 16, 24)
    d.wait(60); step("10_route1")
    for t, w, e in log:
        print(f"{t:20} {w}  {e}")
    r = {t: w for t, w, _ in log}
    checks = {"porta da casa": r["1_porta_da_casa"] == (DAWNMERE, 676, 428),
              "trava": r["4_depois_da_trava"] and r["4_depois_da_trava"][1] == 702,
              "porta do lab": r["6_lab"] and r["6_lab"][0] == LAB,
              "volta do lab": r["8_saida_do_lab"] == (DAWNMERE, 687, 427),
              "route 1": r["10_route1"] and r["10_route1"][0] == ROUTE1}
    for k, v in checks.items():
        print(f"  {k:14} {'ok' if v else 'FALHOU'}")
    print("RESULTADO CP-DS-03B eventos de Dawnmere:", "ok" if all(checks.values()) else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
