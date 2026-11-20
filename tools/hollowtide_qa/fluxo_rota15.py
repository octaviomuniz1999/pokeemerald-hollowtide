#!/usr/bin/env python3
"""QA da rota opcional 15 (Coastal Grotto), a partir de Tidemouth depois da Nami (8 insignias):
Tidemouth -> Route 11 -> praia ate a borda oeste -> Route 15 (conexao) -> Oscar, Nina e Pedro (na gruta) com visao
-> 3 itens -> placa -> volta a Route 11 pela mesma emenda.
Uso: fluxo_rota15.py ROM RUNNER WORKDIR ESTADO_TIDEMOUTH (c10nami.ss)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
TD, R11, R15 = "MAP_PALM_TIDEMOUTH", "MAP_PALM_ROUTE11", "MAP_PALM_ROUTE15"
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
    q.goto(TD, 0, 28); q.run(["press LEFT 40 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == R11, "Tidemouth -> Route 11")
    q.goto(R11, 0, 26); q.run(["press LEFT 30 0", "wait 90", "shot rota15_entrada.png"])
    ok(q.mapname() == R15 and 25 <= q.where[3] <= 28, "Route 11 -> Route 15 pela praia (conexao)")
    for (ax, ay, walk, nome, tid) in [(28, 27, "walk LEFT 6", "OSCAR", IDS["TRAINER_LUIS"]),
                                      (28, 24, "walk UP 2", "NINA", IDS["TRAINER_MELISSA"]),
                                      (27, 14, "walk UP 4", "PEDRO", IDS["TRAINER_DOMINIK"])]:
        q.goto(R15, ax, ay)
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
    for (x, y, face, flag, nome) in [(30, 9, "UP", 0x26D, "Pearl String da gruta"),
                                     (4, 19, "UP", 0x26E, "Deep Sea Tooth da enseada"),
                                     (36, 23, "RIGHT", 0x26F, "Shell Bell das dunas")]:
        q.goto(R15, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(flag), f"Route 15: {nome} coletado")
    q.goto(R15, 37, 25); q.run(["press UP 10 10", "press A 4 40", "shot rota15_placa.png", "mash B 10"])
    ok(q.mapname() == R15, "Placa da Route 15")
    q.goto(R15, 39, 27); q.run(["press RIGHT 30 0", "wait 90"])
    ok(q.mapname() == R11 and tuple(q.where[2:]) in ((0, 27), (1, 27)), "Route 15 -> Route 11 (mesma emenda)")
    print("\nRESUMO ROUTE 15")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
