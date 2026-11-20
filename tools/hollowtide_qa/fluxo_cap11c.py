#!/usr/bin/env python3
"""QA do Capitulo 11 (parte 3): creditos -> tela de titulo -> Continuar -> quarto em Dawnmere -> o PC apita com
os dados de Hoc, Riven e Jade e a convocacao do Doge (FLAG_HT_POSTGAME_DATA) -> a escadaria da Passway abre.
Uso: fluxo_cap11c.py ROM RUNNER WORKDIR ESTADO_FIM (c11fim.ss)
"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA, MAPNUM

ROOMS = ("MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F", "MAP_LITTLEROOT_TOWN_MAYS_HOUSE_2F")
POSTGAME = 0x68
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def where_name(q):
    try:
        return MAPNUM[q.where[:2]]["id"]
    except KeyError:
        return None


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre)
    home = False
    for i in range(60):                       # creditos (~5 min de jogo), "THE END", titulo, menu, Continuar
        q.run(["wait 900", "press A 4 30"] + (["shot cap11c_creditos_%02d.png" % i] if i % 10 == 0 else []))
        if where_name(q) in ROOMS:
            home = True
            break
    ok(home, "Depois dos creditos: Continuar -> quarto em Dawnmere")
    for _ in range(30):
        q.run(["wait 30", "mash A 8"])
        if q.flag(POSTGAME):
            break
    q.run(["mash B 10", "shot cap11c_quarto.png"])
    ok(q.flag(POSTGAME), "PC do quarto: dados de Hoc, Riven e Jade + convocacao do Doge")
    q.run(["wait 120"])
    ok(where_name(q) in ROOMS, "Jogo livre no quarto depois da cena")
    shutil.copy(q.state, f"{work}/c11pos.ss")
    print("\nRESUMO CAPITULO 11 (parte 3)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
