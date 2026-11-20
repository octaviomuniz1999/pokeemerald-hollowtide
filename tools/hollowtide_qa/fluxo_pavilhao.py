#!/usr/bin/env python3
"""QA do Pavilhao das Estrelas (Horizon): fechado com o lago alto (FLAG_HT_HORIZON_DONE desligada so para o teste);
aberto depois: as duas folhas da porta, uma constelacao, o atendente da escada e a volta pela porta certa.
Uso: fluxo_pavilhao.py ROM RUNNER WORKDIR ESTADO_HORIZON (c7chelsia.ss)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

HZ, PV = "MAP_PALM_HORIZON", "MAP_PALM_STAR_PAVILION"
DONE = 0x49
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "setflag 1270 30"])
    if q.mapname() != HZ:
        raise AssertionError(f"estado fora de Horizon: {q.mapname()}")
    q.goto(HZ, 46, 11)
    q.run([f"clearflag 1270 {DONE:X}", "press UP 20 0", "wait 30"])
    for _ in range(10):
        q.run(["press A 4 30", "wait 10"])
        if q.where[3] >= 11:
            break
    ok(q.mapname() == HZ and q.where[3] >= 11, "Pavilhao fechado com o lago alto (recua)")
    q.run([f"setflag 1270 {DONE:X}", "mash B 4"])
    for x in (46, 47):
        q.goto(HZ, x, 10); q.run(["press UP 20 0", "wait 120"])
        ok(q.mapname() == PV, f"Porta ({x},9) -> Pavilhao das Estrelas")
        q.goto(PV, 9 if x == 46 else 10, 12); q.run(["press DOWN 20 0", "wait 120"])
        ok(q.mapname() == HZ and tuple(q.where[2:]) == (x, 10), f"Pavilhao -> Horizon pela porta ({x},9)")
    q.goto(HZ, 46, 10); q.run(["press UP 20 0", "wait 120"])
    q.goto(PV, 2, 2); q.run(["press UP 10 10", "press A 4 40", "mash A 8", "mash B 6", "shot pavilhao_lanterna.png"])
    ok(q.mapname() == PV, "Constelacao no quadro (THE LANTERN)")
    q.goto(PV, 16, 3); q.run(["press UP 10 10", "press A 4 40", "mash A 8", "mash B 6"])
    ok(q.mapname() == PV and tuple(q.where[2:]) == (16, 3), "Atendente segura a escada do mirante")
    print("\nRESUMO PAVILHAO")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
