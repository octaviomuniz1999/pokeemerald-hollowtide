#!/usr/bin/env python3
"""QA do Capitulo 9 (parte 1): Passway -> Route 9 pela estrada leste (aberta, conexao) -> Joseph, Drew, Heidi,
Fabian com visao -> 3 itens -> portao de Voltara fechado (recua) -> volta para a Passway.
Uso: fluxo_cap9.py ROM RUNNER WORKDIR ESTADO_NA_PASSWAY
"""
import shutil, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap8 import battle

TF = 0x500
PW, R9 = "MAP_PALM_PASSWAY", "MAP_PALM_ROUTE09"
MOVED = {(8, 18)}
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def av(mapa):
    return MOVED if mapa == R9 else ()


def talk(q, mapa, x, y, face, extra=("mash B 20",)):
    q.goto(mapa, x, y, avoid=av(mapa))
    q.run([f"press {face} 10 10", "press A 4 40"] + list(extra))


def sighted(q, mapa, ax, ay, walk, nome, tid):
    q.strong()
    q.goto(mapa, ax, ay, avoid=av(mapa))
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
    q.goto(PW, 34, 18); q.run(["press RIGHT 30 0", "wait 90", "shot cap9_rota9.png"])
    ok(q.mapname() == R9, "Passway -> Route 9 (estrada leste aberta, conexao)")
    sighted(q, R9, 6, 19, "walk RIGHT 2", "JOSEPH", 700)
    sighted(q, R9, 15, 17, "walk UP 2", "DREW", 211)
    sighted(q, R9, 28, 13, "walk RIGHT 2", "HEIDI", 469)
    sighted(q, R9, 41, 18, "walk UP 2", "FABIAN", 759)
    for (x, y, face, flag, nome) in [(5, 21, "DOWN", 0x3E9, "Magnet"), (33, 15, "DOWN", 0x3FF, "Thunder Stone"),
                                     (36, 25, "DOWN", 0x452, "Electric Seed")]:
        talk(q, R9, x, y, face, ("mash B 12",))
        ok(q.flag(flag), f"Route 9: {nome} coletado")
    q.goto(R9, 45, 18, avoid=MOVED); q.run(["press RIGHT 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == R9 and tuple(q.where[2:]) == (45, 18), "Portao de Voltara fechado (sem energia, recua)")
    shutil.copy(q.state, f"{work}/c9rota9.ss")
    q.goto(R9, 0, 18, avoid=MOVED); q.run(["press LEFT 30 0", "wait 90"])
    ok(q.mapname() == PW, "Route 9 -> Passway (conexao)")
    print("\nRESUMO CAPITULO 9 (parte 1)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
