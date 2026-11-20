#!/usr/bin/env python3
"""QA da rota opcional 13 (Mirror Grove), a partir da Horizon City depois do ginasio da Chelsia:
Horizon -> Route 7 -> trilha do Circulo da Lua ate a borda leste -> Route 13 (conexao) -> Luna, Kaio e Raul com
visao -> 3 itens -> placa -> volta a Route 7 pela mesma emenda.
Uso: fluxo_rota13.py ROM RUNNER WORKDIR ESTADO_HORIZON (c7chelsia.ss)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
HZ, R7, R13 = "MAP_PALM_HORIZON", "MAP_PALM_ROUTE07", "MAP_PALM_ROUTE13"
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
    q.goto(HZ, 26, 43); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == R7, "Horizon City -> Route 7")
    q.goto(R7, 35, 24); q.run(["press RIGHT 30 0", "wait 90", "shot rota13_entrada.png"])
    ok(q.mapname() == R13 and q.where[3] in (16, 17), "Route 7 -> Route 13 pela trilha do Circulo da Lua (conexao)")
    for (ax, ay, walk, nome, tid) in [(21, 8, "walk RIGHT 6", "LUNA", IDS["TRAINER_NED"]),
                                      (9, 15, "walk DOWN 4", "KAIO", IDS["TRAINER_DEAN"]),
                                      (21, 23, "walk RIGHT 6", "RAUL", IDS["TRAINER_EVERETT"])]:
        q.goto(R13, ax, ay)
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
    for (x, y, face, flag, nome) in [(19, 15, "UP", 0x267, "Spell Tag da clareira"),
                                     (35, 15, "RIGHT", 0x268, "Dusk Stone do recanto"),
                                     (8, 23, "LEFT", 0x269, "Big Mushroom da lagoa")]:
        q.goto(R13, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(flag), f"Route 13: {nome} coletado")
    q.goto(R13, 2, 16); q.run(["press UP 10 10", "press A 4 40", "shot rota13_placa.png", "mash B 10"])
    ok(q.mapname() == R13, "Placa da Route 13")
    q.goto(R13, 0, 17); q.run(["press LEFT 30 0", "wait 90"])
    ok(q.mapname() == R7 and tuple(q.where[2:]) in ((35, 25), (34, 25)), "Route 13 -> Route 7 (mesma emenda)")
    print("\nRESUMO ROUTE 13")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
