#!/usr/bin/env python3
"""QA da caverna do pico (area de treino pos-Liga): fechada pelo vento antes do Tavinho (FLAG_HT_SUMMIT_DONE desligada
so para o teste); aberta depois: entrada, montanhista, os 3 itens (Salamencite, Garchompite, Full Restore) e a volta.
Uso: fluxo_caverna.py ROM RUNNER WORKDIR ESTADO_CUME (c12fim.ss)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

SM, HW = "MAP_PALM_STORM_SUMMIT", "MAP_PALM_STORM_HOLLOW"
SUMMIT_DONE = 0x1DA
ITEMS = [(19, 4, "UP", 0x1E1, "Salamencite"), (5, 17, "LEFT", 0x1E2, "Garchompite"), (23, 16, "UP", 0x1E3, "Full Restore")]
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "setflag 1270 30"])
    ok(q.mapname() == SM, "No cume depois do epilogo")
    q.goto(SM, 7, 15)
    q.run([f"clearflag 1270 {SUMMIT_DONE:X}", "press UP 20 0", "wait 30"])
    for _ in range(10):
        q.run(["press A 4 30", "wait 10"])
        if q.where[3] >= 15:
            break
    ok(q.mapname() == SM and q.where[3] >= 15, "Caverna fechada pelo vento antes do Tavinho (recua)")
    q.run([f"setflag 1270 {SUMMIT_DONE:X}", "mash B 4"])
    q.goto(SM, 7, 14); q.run(["press UP 20 0", "wait 120", "shot caverna_entrada.png"])
    ok(q.mapname() == HW, "Boca da caverna do pico -> area de treino")
    q.goto(HW, 11, 28); q.run(["press UP 10 10", "press A 4 40", "mash A 10", "mash B 6"])
    ok(q.mapname() == HW, "Montanhista na entrada")
    for (x, y, face, flag, nome) in ITEMS:
        q.goto(HW, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(flag), f"Caverna do pico: {nome} coletado")
    q.goto(HW, 10, 28); q.run(["press DOWN 40 0", "wait 120"])
    ok(q.mapname() == SM and tuple(q.where[2:]) in ((7, 14), (7, 13)), "Caverna -> cume (boca certa)")
    print("\nRESUMO CAVERNA DO PICO")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
