#!/usr/bin/env python3
"""QA do Capitulo 10 (parte 1): Voltara -> Route 10 (conexao, aberta pela Insignia Circuito; Tomas, Rita, Jonas,
Luana com visao; 3 itens) -> Tidemouth (conexao): Nami na evacuacao, porto e ginasio fechados, Centro Pokemon
-> volta pela Route 10.
Uso: fluxo_cap10.py ROM RUNNER WORKDIR ESTADO_POS_HOC
"""
import shutil, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap8 import battle

TF = 0x500
VT, R10, TD = "MAP_PALM_VOLTARA", "MAP_PALM_ROUTE10", "MAP_PALM_TIDEMOUTH"
PC = "MAP_PACIFIDLOG_TOWN_POKEMON_CENTER_1F"
res = []
MOVED = {(20, 18), (15, 26), (19, 36), (21, 48)}   # onde Tomas, Rita, Jonas e Luana param depois de avistar


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def talk(q, mapa, x, y, face, extra=("mash B 20",)):
    q.goto(mapa, x, y, avoid=MOVED if mapa == R10 else ())
    q.run([f"press {face} 10 10", "press A 4 40"] + list(extra))


def sighted(q, mapa, ax, ay, walk, nome, tid):
    q.strong()
    q.goto(mapa, ax, ay, avoid=(MOVED - {(ax, ay)}) if mapa == R10 else ())
    if q.flag(TF + tid):
        ok(True, f"{nome} desafiou (no caminho)"); ok(True, f"Venceu {nome}")
        return
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


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"]); q.strong()
    q.goto(VT, 30, 43, avoid={(32, 40)}); q.run(["press DOWN 30 0", "wait 90", "shot cap10_rota10.png"])
    ok(q.mapname() == R10, "Voltara -> Route 10 (conexao)")
    sighted(q, R10, 19, 16, "walk DOWN 2", "TOMAS", 493)
    sighted(q, R10, 16, 24, "walk DOWN 2", "RITA", 59)
    sighted(q, R10, 18, 34, "walk DOWN 2", "JONAS", 337)
    sighted(q, R10, 20, 46, "walk DOWN 2", "LUANA", 444)
    items = [(5, 21, "RIGHT", "FLAG_ITEM_ROUTE_110_RARE_CANDY", "Deep Sea Scale do farol norte"),
             (8, 42, "LEFT", "FLAG_ITEM_ROUTE_110_DIRE_HIT", "Damp Rock do farol sul"),
             (26, 23, "UP", "FLAG_ITEM_ROUTE_111_STARDUST", "Max Repel da restinga")]
    import re
    flags = {m.group(1): int(m.group(2), 16) for m in re.finditer(r"#define (FLAG_ITEM_\w+)\s+(0x[0-9A-Fa-f]+)",
                                                                   open(os.path.join(os.path.dirname(__file__), "..", "..", "include", "constants", "flags.h")).read())}
    for (x, y, face, fname, nome) in items:
        talk(q, R10, x, y, face, ("mash B 12",))
        ok(q.flag(flags[fname]), f"Route 10: {nome} coletado")
    q.goto(R10, 18, 59, avoid=MOVED); q.run(["press DOWN 30 0", "wait 90", "shot cap10_tidemouth.png"])
    ok(q.mapname() == TD, "Route 10 -> Tidemouth (conexao)")
    q.goto(TD, 33, 38); q.run(["press UP 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == TD and tuple(q.where[2:]) == (33, 38), "Porto fechado: balsas suspensas antes da Nami (recua)")
    talk(q, TD, 31, 19, "UP", ("mash B 80", "wait 30", "mash B 30", "shot cap10_nami.png"))
    ok(q.flag(0x54), "Nami recebeu o jogador na evacuacao")
    q.goto(TD, 18, 26); q.run(["press UP 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == TD and tuple(q.where[2:]) == (18, 26), "Ginasio da Nami fechado durante a evacuacao (recua)")
    q.goto(TD, 21, 15); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == PC, "Tidemouth -> Centro Pokemon")
    q.goto(PC, 7, 8); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == TD and tuple(q.where[2:]) in ((21, 14), (21, 15)), "Centro Pokemon -> Tidemouth (porta certa)")
    shutil.copy(q.state, f"{work}/c10tide.ss")
    q.goto(TD, 30, 0); q.run(["press UP 30 0", "wait 90"])
    ok(q.mapname() == R10, "Tidemouth -> Route 10 (conexao)")
    q.goto(R10, 18, 0, avoid=MOVED); q.run(["press UP 30 0", "wait 90"])
    ok(q.mapname() == VT, "Route 10 -> Voltara (conexao)")
    print("\nRESUMO CAPITULO 10 (parte 1)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
