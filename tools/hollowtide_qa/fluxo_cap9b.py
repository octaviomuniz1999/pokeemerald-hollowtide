#!/usr/bin/env python3
"""QA do Capitulo 9 (parte 2): Route 9 -> Voltara (conexao) -> Centro de Dados fechado antes do Hoc -> Hoc na
estacao -> Centro de Dados: 2 recrutas -> 2F: Vega -> 3 retransmissores -> energia de volta -> saida sul
fechada ate a 7a insignia -> Centro Pokemon -> volta para a Route 9.
Uso: fluxo_cap9b.py ROM RUNNER WORKDIR ESTADO_NA_ROUTE9
"""
import shutil, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap8 import battle
from fluxo_cap7 import interact_until

TF = 0x500
R9, VT, D1, D2 = "MAP_PALM_ROUTE09", "MAP_PALM_VOLTARA", "MAP_PALM_DATA_CENTER_1F", "MAP_PALM_DATA_CENTER_2F"
PC = "MAP_MAUVILLE_CITY_POKEMON_CENTER_1F"
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def sighted(q, mapa, ax, ay, walk, nome, tid, avoid=()):
    q.strong()
    q.goto(mapa, ax, ay, avoid=avoid)
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
    q.goto(R9, 47, 18); q.run(["press RIGHT 30 0", "wait 90", "shot cap9_voltara.png"])
    ok(q.mapname() == VT, "Route 9 -> Voltara (conexao)")
    q.goto(VT, 48, 18); q.run(["press UP 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == VT and tuple(q.where[2:]) == (48, 18), "Centro de Dados fechado antes do Hoc (recua)")
    q.goto(VT, 27, 19); q.run(["press UP 10 10", "press A 4 40", "mash B 80", "wait 30", "mash B 30", "shot cap9_hoc.png"])
    ok(q.flag(0x4B), "Hoc recebeu o jogador na estacao")
    q.goto(VT, 48, 17); q.run(["press UP 30 0", "wait 120", "shot cap9_datacenter.png"])
    ok(q.mapname() == D1, "Voltara -> Centro de Dados")
    sighted(q, D1, 8, 9, "walk UP 1", "Recruta do saguao 1", 22)
    sighted(q, D1, 12, 2, "walk RIGHT 1", "Recruta do saguao 2", 116)
    q.goto(D1, 13, 2, avoid={(13, 3)}); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == D2, "Saguao -> sala dos servidores (2F)")
    sighted(q, D2, 13, 3, "walk DOWN 2", "VEGA", 30)
    for (x, fl, n) in [(2, 0x4C, 1), (5, 0x4D, 2), (8, 0x4E, 3)]:
        interact_until(q, D2, x, 8, "UP", fl)
        ok(q.flag(fl), f"Retransmissor {n} desligado")
    q.run(["mash B 30", "shot cap9_energia.png"])
    ok(q.flag(0x4F), "Energia de volta em Voltara")
    q.goto(D2, 13, 2, avoid={(13, 4), (12, 5)}); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == D1, "2F -> saguao")
    q.goto(D1, 8, 8, avoid={(13, 3)}); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == VT and tuple(q.where[2:]) in ((48, 16), (48, 17)), "Centro de Dados -> Voltara (porta certa)")
    q.goto(VT, 30, 40); q.run(["press DOWN 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == VT and tuple(q.where[2:]) == (30, 40), "Saida sul fechada ate a 7a insignia (recua)")
    q.goto(VT, 9, 26); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == PC, "Voltara -> Centro Pokemon")
    q.goto(PC, 7, 8); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == VT and tuple(q.where[2:]) in ((9, 25), (9, 26)), "Centro Pokemon -> Voltara (porta certa)")
    shutil.copy(q.state, f"{work}/c9voltara.ss")
    # ginasio do Hoc: 4 consoles em ordem (cada um corta o feixe que guarda o proximo), 3 treinadores, Hoc
    G = "MAP_PALM_HOC_GYM"
    q.goto(VT, 41, 31); q.run(["press UP 30 0", "wait 120", "shot cap9_ginasio.png"])
    ok(q.mapname() == G, "Ginasio do Hoc aberto com a energia de volta")
    q.strong()
    q.goto(G, 0, 15); q.run(["wait 30", "mash B 20"])
    q.goto(G, 4, 12); q.run(["wait 30", "mash B 20"])
    ok(tuple(q.where[2:]) == (4, 12), "Console 1 cortou o feixe baixo (ala leste alcancada)")
    q.run(["wait 30", "mash B 20"])
    sighted(q, G, 6, 12, "walk RIGHT 1", "Guitarrista do Circuito", 702)
    sighted(q, G, 7, 12, "walk UP 2", "Especialista do Circuito 1", 511, avoid={(8, 12)})
    q.goto(G, 8, 9, avoid={(8, 12), (7, 9)}); q.run(["wait 30", "mash B 20"])
    ok(tuple(q.where[2:]) == (8, 9), "Console 2 cortou o feixe leste (sala direita alcancada)")
    sighted(q, G, 4, 10, "walk LEFT 1", "Especialista do Circuito 2", 594, avoid={(8, 12), (7, 9)})
    q.goto(G, 3, 9, avoid={(8, 12), (7, 9), (2, 10)}); q.run(["wait 30", "mash B 20"])
    ok(tuple(q.where[2:]) == (3, 9), "Console 3 cortou o feixe central (sala esquerda alcancada)")
    q.goto(G, 5, 3, avoid={(8, 12), (7, 9), (2, 10)}); q.run(["wait 20", "shot cap9_circuito.png"])
    ok(tuple(q.where[2:]) == (5, 3), "Console 4 abriu o palco do Hoc")
    q.strong()
    q.goto(G, 5, 3, avoid={(8, 12), (7, 9), (2, 10)}); q.run(["press UP 10 10", "press A 4 40"])
    ok(battle(q, TF + 268), "Venceu HOC")
    for _ in range(12):
        q.run(["mash A 8", "mash B 6"])
        if q.flag(0x860 + 13):
            break
    q.run(["mash B 90", "wait 30", "mash B 30", "shot cap9_insignia.png"])
    ok(q.flag(0x860 + 13), "Insignia Circuito recebida")
    q.goto(G, 4, 19, avoid={(8, 12), (7, 9), (2, 10)}); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == VT and tuple(q.where[2:]) in ((41, 30), (41, 31)), "Saiu do ginasio na porta certa")
    q.goto(VT, 30, 40); q.run(["press DOWN 30 0", "wait 60", "mash B 10"])
    ok(q.mapname() == VT and tuple(q.where[2:]) in ((30, 41), (30, 42), (30, 43)), "Saida sul liberada pela Insignia Circuito")
    shutil.copy(q.state, f"{work}/c9hoc.ss")
    q.goto(VT, 0, 18, avoid={(32, 40)}); q.run(["press LEFT 30 0", "wait 90"])
    ok(q.mapname() == R9, "Voltara -> Route 9 (conexao)")
    print("\nRESUMO CAPITULO 9 (parte 2)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
