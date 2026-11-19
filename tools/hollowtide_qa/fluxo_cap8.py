#!/usr/bin/env python3
"""QA do Capitulo 8 jogado de verdade: Horizon -> Route 8 (conexao, aberta pela Insignia do Horizonte; Alan,
Kiyo, Cora, Auron com visao; 3 itens) -> Passway Village: escadaria do cume interditada (recua), estrada leste
fechada (recua), fonte termal cura, casa da ancia, Centro Pokemon -> volta pela Route 8 ate a Horizon.
Uso: fluxo_cap8.py ROM RUNNER WORKDIR ESTADO_POS_CHELSIA
"""
import shutil, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
HZ, R8, PW = "MAP_PALM_HORIZON", "MAP_PALM_ROUTE08", "MAP_PALM_PASSWAY"
ELDER, PC = "MAP_SOOTOPOLIS_CITY_HOUSE7", "MAP_FALLARBOR_TOWN_POKEMON_CENTER_1F"
MOVED = {(24, 41), (16, 30), (18, 18), (22, 6)}      # onde os treinadores param depois de avistar
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def avoid(mapa):
    return MOVED if mapa == R8 else ()


def talk(q, mapa, x, y, face, extra=("mash B 20",)):
    q.goto(mapa, x, y, avoid=avoid(mapa))
    q.run([f"press {face} 10 10", "press A 4 40"] + list(extra))


def sighted(q, mapa, ax, ay, walk, nome, tid):
    q.goto(mapa, ax, ay, avoid=avoid(mapa) - {(ax, ay)})
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
    ok(battle(q, TF + tid, tries=140), f"Venceu {nome}")
    q.run(["mash B 16"])


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"]); q.strong()
    q.goto(HZ, 52, 0, ignore={(24, 20), (25, 20)}); q.run(["press UP 30 0", "wait 90", "shot cap8_rota8.png"])
    ok(q.mapname() == R8, "Horizon -> Route 8 (conexao, apos a Insignia do Horizonte)")
    sighted(q, R8, 23, 43, "walk UP 2", "ALAN", 630)
    sighted(q, R8, 14, 31, "walk RIGHT 2", "KIYO", 181)
    sighted(q, R8, 16, 19, "walk RIGHT 2", "CORA", 428)
    sighted(q, R8, 20, 7, "walk RIGHT 2", "AURON", 506)
    for (x, y, face, flag, nome) in [(4, 20, "LEFT", 0x404, "Never-Melt Ice do mirante"), (29, 16, "UP", 0x405, "Hyper Potion"),
                                     (14, 10, "UP", 0x400, "Ice Stone")]:
        talk(q, R8, x, y, face, ("mash B 12",))
        ok(q.flag(flag), f"Route 8: {nome} coletado")
    q.goto(R8, 18, 0, avoid=MOVED); q.run(["press UP 30 0", "wait 90", "shot cap8_passway.png"])
    ok(q.mapname() == PW, "Route 8 -> Passway Village (conexao)")
    q.goto(PW, 17, 10); q.run(["press UP 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == PW and tuple(q.where[2:]) == (17, 10), "Escadaria do cume interditada pelo guardiao (recua)")
    q.goto(PW, 33, 18); q.run(["press RIGHT 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == PW and tuple(q.where[2:]) == (33, 18), "Estrada leste fechada pelo deslizamento (recua)")
    talk(q, PW, 27, 9, "UP", ("press A 4 40", "press A 4 40", "press A 4 40", "wait 200", "mash A 10", "mash B 10", "shot cap8_fonte.png"))
    ok(q.mapname() == PW, "Fonte termal (descanso)")
    q.goto(PW, 29, 16); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == ELDER, "Passway -> casa da ancia")
    talk(q, ELDER, 5, 4, "UP", ("mash B 60", "shot cap8_ancia.png", "mash B 20"))
    q.goto(ELDER, 3, 5); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == PW and tuple(q.where[2:]) in ((29, 15), (29, 16)), "Casa da ancia -> Passway (porta certa)")
    q.goto(PW, 5, 17); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == PC, "Passway -> Centro Pokemon")
    q.goto(PC, 7, 8); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == PW and tuple(q.where[2:]) in ((5, 16), (5, 17)), "Centro Pokemon -> Passway (porta certa)")
    shutil.copy(q.state, f"{work}/c8passway.ss")
    q.goto(PW, 16, 31); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == R8, "Passway -> Route 8 (conexao)")
    q.goto(R8, 16, 47, avoid=MOVED); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == HZ, "Route 8 -> Horizon (conexao)")
    print("\nRESUMO CAPITULO 8")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
