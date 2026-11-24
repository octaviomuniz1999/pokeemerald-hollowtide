#!/usr/bin/env python3
"""QA curto de Breezeport a partir do estado salvo depois do Nevard (qa_cp03d.py --cap1 grava depois_do_nevard.dst):
Harvestvale -> Route 2 -> Breezeport, ate a praia do farol (decisao do diretor 24/11: o farol de Olivine, abaixo do
faroleiro). Capturas do farol e da casa do faroleiro. Uso: qa_farol.py ROM ESTADO PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import goto, advance
from lunia_mundo import CELLS, HV, R2, gba

BR = lambda x, y: gba("Brisa", x, y)
MAPS = (67, 34, 77)


def main(rom, state, out):
    os.makedirs(out, exist_ok=True)
    d = DS(rom); d.load(state); d.wait(60)
    log = []

    def step(tag):
        w = d.where(); log.append((tag, w)); d.shot(f"{out}/{tag}.png"); print(tag, w, flush=True)

    for goal, tag in ((HV(18, 34), "h"), (R2(19, 46), "r2"), (BR(58, 44), "br"), (BR(62, 46), "br")):
        goto(d, rom, goal, CELLS, MAPS, out, tag, fight_ok=True, max_steps=700)
    d.wait(60); step("1_farol_e_faroleiro")
    goto(d, rom, BR(56, 44), CELLS, MAPS, out, "br", fight_ok=True); d.wait(60); step("2_casa_do_faroleiro")
    ok = log[0][1] and log[0][1][0] == 77
    print("RESULTADO farol:", "ok" if ok else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
