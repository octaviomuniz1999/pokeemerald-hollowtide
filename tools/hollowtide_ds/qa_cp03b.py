#!/usr/bin/env python3
"""QA do rascunho da Route 1 setor N (provas/cp03b): bloco gerado da grade rota1_n.txt na celula (22,12)
(mundo x 704-735, z 384-415), a partir do estado do quarto (ds_intro.py) e do atalho de QA no PC.
Passos: entra pela entrada oeste; anda pelo caminho sinuoso ate a saida sul; colisao contra a lagoa, uma arvore e o
mato alto (o mato e livre: so encontros); capturas em cada ponto. Uso: qa_cp03b.py ROM ESTADO_QUARTO PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import goto, face

MAPA, X0, Z0, CELLS = 31, 704, 384, [(22, 12)]


def W(x, z):
    return (X0 + x, Z0 + z)


def main(rom, state, out):
    os.makedirs(out, exist_ok=True)
    d = DS(rom); d.load(state); d.wait(30)
    ok, log = {}, []
    def step(tag):
        w = d.where(); log.append((tag, w)); d.shot(f"{out}/{tag}.png"); return w
    d.press("UP", 16, 24); d.press("UP", 4, 20); d.press("A", 4, 30)
    for _ in range(20):
        d.wait(30)
        if d.where() and d.where()[0] == MAPA:
            break
    d.wait(120)
    ok["entrada"] = step("1_entrada_oeste")
    go = lambda goal, tag: goto(d, rom, W(*goal), CELLS, MAPA, out, tag, fight_ok=False)
    go((12, 11), "c"); step("2_caminho")
    go((17, 7), "c")
    for _ in range(3):
        d.press("RIGHT", 16, 24)
    ok["lagoa"] = step("3_contra_a_lagoa")
    go((14, 16), "c"); step("4_meio")
    go((16, 18), "c"); ok["mato_leste"] = step("5_perto_do_mato_leste")
    go((18, 27), "c"); step("6_perto_da_saida_sul")
    go((17, 30), "c")
    for _ in range(3):
        d.press("DOWN", 16, 24)
    ok["fim_da_prova"] = step("7_fim_do_caminho")
    go((8, 24), "c")
    for _ in range(3):
        d.press("LEFT", 16, 24)
    ok["arvore"] = step("8_contra_a_arvore")
    for t, w in log:
        print(f"{t:24} {w}")
    good = (ok["entrada"] and ok["entrada"][0] == MAPA and ok["lagoa"][1:] == W(17, 7)
            and ok["fim_da_prova"][1:] == W(17, 30) and ok["arvore"][1:] == W(8, 24))
    print("RESULTADO CP-DS-03B setor N:", "ok" if good else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
