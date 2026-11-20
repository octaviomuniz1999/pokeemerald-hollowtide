#!/usr/bin/env python3
"""QA da rota opcional 14 (Atlas Lookout), a partir da Passway Village:
Passway -> rua principal ate a borda oeste -> Route 14 (conexao) -> Clara, Beto e Otto (no alto do patamar) com
visao -> 3 itens -> placas da entrada e do mirante -> volta a Passway pela mesma emenda.
Uso: fluxo_rota14.py ROM RUNNER WORKDIR ESTADO_PASSWAY (c8passway.ss)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
PW, R14 = "MAP_PALM_PASSWAY", "MAP_PALM_ROUTE14"
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
    q.goto(PW, 0, 18); q.run(["press LEFT 30 0", "wait 90", "shot rota14_entrada.png"])
    ok(q.mapname() == R14 and q.where[3] in (18, 19), "Passway -> Route 14 pela rua principal (conexao)")
    for (ax, ay, walk, nome, tid) in [(33, 19, "walk LEFT 5", "CLARA", IDS["TRAINER_PAT"]),
                                      (24, 18, "walk LEFT 6", "BETO", IDS["TRAINER_SEBASTIAN"]),
                                      (9, 8, "walk RIGHT 5", "OTTO", IDS["TRAINER_JARED"])]:
        q.goto(R14, ax, ay)
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
    for (x, y, face, flag, nome) in [(9, 7, "UP", 0x26A, "Scope Lens do mirante"),
                                     (18, 25, "LEFT", 0x26B, "Razor Claw do desvio sul"),
                                     (6, 18, "LEFT", 0x26C, "HP Up do fim da estrada")]:
        q.goto(R14, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(flag), f"Route 14: {nome} coletado")
    q.goto(R14, 10, 7); q.run(["press UP 10 10", "press A 4 40", "shot rota14_mirante.png", "mash B 14"])
    ok(q.mapname() == R14, "Placa do mirante")
    q.goto(R14, 37, 18); q.run(["press UP 10 10", "press A 4 40", "mash B 10"])
    ok(q.mapname() == R14, "Placa da Route 14")
    q.goto(R14, 39, 19); q.run(["press RIGHT 30 0", "wait 90"])
    ok(q.mapname() == PW and tuple(q.where[2:]) in ((0, 19), (1, 19)), "Route 14 -> Passway (mesma emenda)")
    print("\nRESUMO ROUTE 14")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
