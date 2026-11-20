#!/usr/bin/env python3
"""QA da rota opcional 12 (River Bend), a partir de Pillarton depois de chegar pela Route 5:
Pillarton -> Route 5 -> tabuado oeste -> Route 12 (conexao) -> Artur, Bia e Nico com visao -> 3 itens -> placa
-> volta a Route 5 pela mesma emenda.
Uso: fluxo_rota12.py ROM RUNNER WORKDIR ESTADO_PILLARTON (cap5_pillarton.ss)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
P, R5, R12 = "MAP_PALM_PILLARTON", "MAP_PALM_ROUTE05", "MAP_PALM_ROUTE12"
IDS = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define (TRAINER_\w+)\s+(\d+)",
       open(os.path.join(os.path.dirname(__file__), "..", "..", "include", "constants", "opponents.h")).read())}
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work, estado):
    q = QA(rom, runner, work)
    q.load(estado); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"]); q.strong()
    q.goto(P, 20, 43); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == R5, "Pillarton -> Route 5")
    q.goto(R5, 0, 29); q.run(["press LEFT 30 0", "wait 90", "shot rota12_entrada.png"])
    ok(q.mapname() == R12 and q.where[3] in (14, 15), "Route 5 -> Route 12 pelo tabuado oeste (conexao)")
    for (ax, ay, walk, nome, tid) in [(19, 14, "walk UP 3", "ARTUR", IDS["TRAINER_BARNY"]),
                                      (5, 15, "walk DOWN 4", "BIA", IDS["TRAINER_HAILEY"]),
                                      (30, 16, "walk DOWN 5", "NICO", IDS["TRAINER_CLARK"])]:
        q.goto(R12, ax, ay)
        if q.flag(TF + tid):
            ok(True, f"{nome} desafiou (no caminho)"); ok(True, f"Venceu {nome}")
            continue
        q.run([walk, "wait 60"])
        seen = False
        for _ in range(25):
            if q.in_battle():
                seen = True
                break
            q.run(["press A 4 30"])
        ok(seen, f"{nome} avistou o jogador e desafiou")
        ok(battle(q, TF + tid), f"Venceu {nome}")
        q.run(["mash B 16"])
    for (x, y, face, flag, nome) in [(14, 7, "UP", 0x264, "Mystic Water da ponta de areia"),
                                     (18, 23, "RIGHT", 0x265, "Water Stone da prainha"),
                                     (32, 25, "RIGHT", 0x266, "Big Pearl do remanso")]:
        q.goto(R12, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(flag), f"Route 12: {nome} coletado")
    q.goto(R12, 37, 14); q.run(["press UP 10 10", "press A 4 40", "shot rota12_placa.png", "mash B 10"])
    ok(q.mapname() == R12, "Placa da Route 12")
    q.goto(R12, 39, 15); q.run(["press RIGHT 30 0", "wait 90"])
    ok(q.mapname() == R5 and tuple(q.where[2:]) in ((0, 30), (1, 30)), "Route 12 -> Route 5 (mesma emenda)")
    print("\nRESUMO ROUTE 12")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
