#!/usr/bin/env python3
"""QA da Route 2 jogada de verdade (a partir do estado pos-Nevard), com visao dos treinadores LIGADA:
Harvestvale -> Route 2 (conexao) -> Liang, Mei-Lan e Qin desafiam ao avistar o jogador -> Super Potion no
mirante (escada) -> placa sul -> Breezeport (conexao). Time de QA nivel 100; sem selvagens.
Uso: fluxo_rota2.py ROM RUNNER WORKDIR ESTADO_POS_NEVARD
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
FLAG_ITEM_LOOKOUT = 0x3E8          # FLAG_ITEM_ROUTE_102_POTION reaproveitada no mirante
R2 = "MAP_PALM_ROUTE02"
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work, estado):
    q = QA(rom, runner, work)
    q.load(estado)
    q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"])   # sem selvagens; treinadores enxergam
    q.strong()
    G = "MAP_RUSTBORO_CITY_GYM"
    if q.mapname() == G:
        q.goto(G, 5, 19); q.run(["press DOWN 30 0", "wait 120"])
    q.goto("MAP_OLDALE_TOWN", 18, 36); q.run(["press DOWN 30 0", "wait 120", "shot r2_entrada.png"])
    ok(q.mapname() == R2, "Harvestvale -> Route 2 sem fade (conexao)")
    # aproxima-se fora da linha de visao e entra nela andando
    for (x, y, nome, tid) in [(24, 10, "LIANG", 858), (18, 24, "MEI-LAN", 859), (18, 32, "QIN", 860)]:
        q.goto(R2, x, y)
        q.run(["walk DOWN 4", "wait 60"])
        seen = False
        for _ in range(15):                       # dialogo de desafio -> batalha
            if q.in_battle():
                seen = True
                break
            q.run(["press A 4 30"])
        ok(seen, f"{nome} avistou o jogador e desafiou")
        ok(battle(q, TF + tid), f"Venceu {nome}")
    q.run(["shot r2_treinadores.png"])
    # mirante: sobe a escada e pega o item
    q.goto(R2, 7, 27); q.run(["press UP 10 10", "press A 4 40", "mash B 12", "shot r2_mirante.png"])
    ok(q.flag(FLAG_ITEM_LOOKOUT), "Super Potion do mirante coletada")
    q.goto(R2, 19, 47); q.run(["press DOWN 30 0", "wait 150", "shot r2_breezeport.png"])
    ok(q.mapname() == "MAP_PALM_BRISA", "Route 2 -> Breezeport sem fade (conexao)")
    print("\nRESUMO ROUTE 2")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
