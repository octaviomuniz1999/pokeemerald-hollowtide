#!/usr/bin/env python3
"""QA de transicoes ida e volta: Colheita -> Rota 02 -> Brisa -> Rota 03 -> Ferralia -> ... -> Vila Inicial.

As travas de historia sao liberadas por injecao de flag na RAM (FLAG_DEFEATED_RUSTBORO_GYM e
FLAG_PALM_JAY_WON), porque o objetivo aqui e validar mapas e passagens, nao as batalhas.
Uso: fluxo_transicoes.py ROM RUNNER WORKDIR ESTADO_NA_COLHEITA
"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA, MAPS

FLAGS_OFF = "1270"  # offsetof(struct SaveBlock1, flags) nesta build
FLAG_DEFEATED_RUSTBORO_GYM = "4F0"
FLAG_PALM_JAY_WON = "2C"

resultados = []


def check(q, esperado, rotulo):
    ok = q.mapname() == esperado
    resultados.append((rotulo, "OK" if ok else "FALHA", q.mapname(), q.where[2:]))
    print(("OK   " if ok else "FALHA"), rotulo, "->", q.mapname(), q.where[2:], flush=True)
    if not ok:
        q.run([f"shot falha_{len(resultados):02d}.png"])
        raise SystemExit(1)


def cruzar(q, mapa, x, y, direcao, destino, rotulo, shot=None):
    q.no_wild()
    q.goto(mapa, x, y)
    q.run([f"press {direcao} 30 0", "wait 120"] + ([f"shot {shot}"] if shot else []))
    check(q, destino, rotulo)


def main(rom, runner, work, estado):
    q = QA(rom, runner, work)
    q.load(estado)
    q.run([])
    q.no_wild()

    # Trava 1: sem vitoria sobre o Nevard a saida sudeste deve continuar fechada.
    # (conexao continua: a trava e um gatilho na calcada que faz o jogador recuar um passo)
    q.goto("MAP_OLDALE_TOWN", 18, 34)
    q.run(["press DOWN 18 0", "wait 60", "mash A 24", "mash B 6", "wait 60"])
    check(q, "MAP_OLDALE_TOWN", "Colheita: saida para Rota 02 bloqueada antes do Nevard")
    ok = tuple(q.where[2:]) == (18, 34)
    resultados.append(("Colheita: jogador recua um passo na trava", "OK" if ok else "FALHA", q.mapname(), q.where[2:]))
    print("OK   " if ok else "FALHA", "Colheita: jogador recua um passo na trava", q.where[2:], flush=True)
    if not ok:
        raise SystemExit(1)

    q.run([f"setflag {FLAGS_OFF} {FLAG_DEFEATED_RUSTBORO_GYM}"])
    cruzar(q, "MAP_OLDALE_TOWN", 18, 36, "DOWN", "MAP_PALM_ROUTE02", "Colheita -> Rota 02 (conexao)", "qa_rota02.png")
    cruzar(q, "MAP_PALM_ROUTE02", 19, 47, "DOWN", "MAP_PALM_BRISA", "Rota 02 -> Breezeport (conexao)", "qa_brisa.png")

    # Servicos da Breezeport: Centro Pokemon e volta
    cruzar(q, "MAP_PALM_BRISA", 23, 17, "UP", "MAP_DEWFORD_TOWN_POKEMON_CENTER_1F", "Breezeport -> Centro Pokemon")
    cruzar(q, "MAP_DEWFORD_TOWN_POKEMON_CENTER_1F", 7, 8, "DOWN", "MAP_PALM_BRISA", "Centro Pokemon -> Breezeport")
    # Teatro trancado ate religar os postes do festival
    q.goto("MAP_PALM_BRISA", 47, 28); q.run(["press UP 30 0", "wait 90"])
    check(q, "MAP_PALM_BRISA", "Breezeport: Teatro trancado antes dos postes")

    # Trava 2: saida oeste (praia -> Rota 3, conexao continua) fechada antes da Jay: recua um passo.
    q.goto("MAP_PALM_BRISA", 1, 40)
    q.run(["press LEFT 18 0", "wait 60", "mash A 24", "mash B 6", "wait 60"])
    check(q, "MAP_PALM_BRISA", "Breezeport: saida para Rota 03 bloqueada antes da Jay")
    ok = tuple(q.where[2:]) == (1, 40)
    resultados.append(("Breezeport: jogador recua um passo na trava", "OK" if ok else "FALHA", q.mapname(), q.where[2:]))
    print("OK   " if ok else "FALHA", "Breezeport: jogador recua um passo na trava", q.where[2:], flush=True)
    if not ok:
        raise SystemExit(1)

    q.run([f"setflag {FLAGS_OFF} {FLAG_PALM_JAY_WON}"])
    cruzar(q, "MAP_PALM_BRISA", 0, 40, "LEFT", "MAP_PALM_ROUTE03", "Breezeport -> Rota 03 (conexao)", "qa_rota03.png")
    ok = q.where[3] == 60 and q.where[2] in (54, 55)   # mesma linha da praia (pode dar 1 passo a mais)
    resultados.append(("Rota 03: chegada alinhada a praia (55,60)", "OK" if ok else "FALHA", q.mapname(), q.where[2:]))
    print("OK   " if ok else "FALHA", "Rota 03: chegada alinhada a praia", q.where[2:], flush=True)
    if not ok:
        raise SystemExit(1)
    # subida da serra ate o planalto e a saida norte (Ferralia provisoria, por warp)
    cruzar(q, "MAP_PALM_ROUTE03", 25, 1, "UP", "MAP_PALM_FERRALIA", "Rota 03 (serra) -> Ferralia", "qa_ferralia.png")
    shutil.copy(q.state, f"{work}/qa_ferralia.ss")

    # Volta
    cruzar(q, "MAP_PALM_FERRALIA", 1, 10, "LEFT", "MAP_PALM_ROUTE03", "Ferralia -> Rota 03")
    cruzar(q, "MAP_PALM_ROUTE03", 55, 60, "RIGHT", "MAP_PALM_BRISA", "Rota 03 -> Breezeport (conexao)")
    cruzar(q, "MAP_PALM_BRISA", 19, 0, "UP", "MAP_PALM_ROUTE02", "Breezeport -> Rota 02 (conexao)")
    cruzar(q, "MAP_PALM_ROUTE02", 18, 0, "UP", "MAP_OLDALE_TOWN", "Rota 02 -> Colheita (conexao)")
    cruzar(q, "MAP_OLDALE_TOWN", 9, 1, "UP", "MAP_ROUTE101", "Colheita -> Rota 01")
    cruzar(q, "MAP_ROUTE101", 2, 4, "LEFT", "MAP_LITTLEROOT_TOWN", "Rota 01 -> Vila Inicial")

    print("\nRESUMO")
    for r in resultados:
        print(" ", r[1], r[0])
    print("paradas para batalha/dialogo:", q.battles)


if __name__ == "__main__":
    main(*sys.argv[1:5])
