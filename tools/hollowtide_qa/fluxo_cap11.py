#!/usr/bin/env python3
"""QA do Capitulo 11 (parte 1): Tidemouth -> Route 11 (guarda das 8 insignias; Vincent, Felix, Leroy com visao;
3 itens) -> tunel -> ilha da Liga (Ever Grande, parte alta) -> saguao da Liga (guardas liberam com 8 insignias).
Uso: fluxo_cap11.py ROM RUNNER WORKDIR ESTADO_POS_NAMI
"""
import shutil, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap8 import battle

TF = 0x500
TD, R11, EG, L1 = "MAP_PALM_TIDEMOUTH", "MAP_PALM_ROUTE11", "MAP_EVER_GRANDE_CITY", "MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F"
BADGE8 = 0x860 + 14
MOVED = {(36, 19)}
res = []
FLAGS = {m.group(1): int(m.group(2), 16) for m in re.finditer(r"#define (FLAG_ITEM_\w+)\s+(0x[0-9A-Fa-f]+)",
         open(os.path.join(os.path.dirname(__file__), "..", "..", "include", "constants", "flags.h")).read())}


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def av(m):
    return MOVED if m == R11 else ()


def sighted(q, mapa, ax, ay, walk, nome, tid):
    q.strong()
    q.goto(mapa, ax, ay, avoid=av(mapa) - {(ax, ay)} if mapa == R11 else ())
    if q.flag(TF + tid):
        ok(True, f"{nome} desafiou (no caminho)"); ok(True, f"Venceu {nome}")
        return
    q.run([walk, "wait 60"])
    seen = False
    for _ in range(40):
        if q.in_battle():
            seen = True
            break
        q.run(["press A 4 30"])
    ok(seen, f"{nome} avistou o jogador e desafiou")
    ok(battle(q, TF + tid), f"Venceu {nome}")
    q.run(["mash B 16"])


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30", f"clearflag 1270 {BADGE8:X}"]); q.strong()
    q.goto(TD, 0, 28); q.run(["press LEFT 40 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == R11 and tuple(q.where[2:]) == (47, 20), "Route 11: guarda barra sem as 8 insignias (recua)")
    q.run([f"setflag 1270 {BADGE8:X}"])
    ids = {}
    for line in open(os.path.join(os.path.dirname(__file__), "..", "..", "include", "constants", "opponents.h")):
        m = re.match(r"#define (TRAINER_\w+)\s+(\d+)", line)
        if m:
            ids[m.group(1)] = int(m.group(2))
    sighted(q, R11, 38, 20, "walk LEFT 2", "VINCENT", ids["TRAINER_VINCENT"])
    sighted(q, R11, 26, 11, "walk LEFT 2", "FELIX", ids["TRAINER_FELIX"])
    sighted(q, R11, 16, 10, "walk LEFT 2", "LEROY", ids["TRAINER_LEROY"])
    for (x, y, face, fname, nome) in [(5, 22, "LEFT", "FLAG_ITEM_ROUTE_111_HP_UP", "Full Restore"),
                                      (38, 5, "UP", "FLAG_ITEM_ROUTE_112_NUGGET", "Max Revive"),
                                      (22, 27, "LEFT", "FLAG_ITEM_ROUTE_113_MAX_ETHER", "PP Max")]:
        q.goto(R11, x, y, avoid=MOVED); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(FLAGS[fname]), f"Route 11: {nome} coletado")
    q.goto(R11, 9, 8, avoid=MOVED); q.run(["press UP 30 0", "wait 120", "shot cap11_ilha.png"])
    ok(q.mapname() == EG, "Tunel da Liga -> ilha da Liga")
    q.goto(EG, 18, 6); q.run(["press UP 30 0", "wait 120", "shot cap11_saguao.png"])
    ok(q.mapname() == L1, "Ilha -> saguao da Liga")
    shutil.copy(q.state, f"{work}/c11liga.ss")
    q.goto(L1, 9, 10); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == EG, "Saguao -> ilha")
    q.goto(EG, 18, 28); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == R11, "Ilha -> tunel -> Route 11")
    print("\nRESUMO CAPITULO 11 (parte 1)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
