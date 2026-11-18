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
    q.run([f"press {direcao} 18 0", "wait 120"] + ([f"shot {shot}"] if shot else []))
    check(q, destino, rotulo)


def main(rom, runner, work, estado):
    q = QA(rom, runner, work)
    q.load(estado)
    q.run([])
    q.no_wild()

    # Trava 1: sem vitoria sobre o Nevard a saida sudeste deve continuar fechada.
    q.goto("MAP_OLDALE_TOWN", 18, 34)
    q.run(["press DOWN 18 0", "wait 60", "mash A 6", "mash B 4"])
    check(q, "MAP_OLDALE_TOWN", "Colheita: saida para Rota 02 bloqueada antes do Nevard")

    q.run([f"setflag {FLAGS_OFF} {FLAG_DEFEATED_RUSTBORO_GYM}", "walk UP 1", "wait 30"])
    if q.mapname() == "MAP_OLDALE_TOWN":
        q.goto("MAP_OLDALE_TOWN", 18, 34)
        q.run(["press DOWN 18 0", "wait 120"])
    q.run(["shot qa_rota02.png"])
    check(q, "MAP_PALM_ROUTE02", "Colheita -> Rota 02")

    cruzar(q, "MAP_PALM_ROUTE02", 25, 32, "DOWN", "MAP_PALM_BRISA", "Rota 02 -> Brisa", "qa_brisa.png")

    # Trava 2: leste da Brisa fechado antes da Jay.
    q.goto("MAP_PALM_BRISA", 17, 17)
    q.run(["press RIGHT 18 0", "wait 60", "mash A 6", "mash B 4"])
    check(q, "MAP_PALM_BRISA", "Brisa: saida para Rota 03 bloqueada antes da Jay")

    q.run([f"setflag {FLAGS_OFF} {FLAG_PALM_JAY_WON}"])
    cruzar(q, "MAP_PALM_BRISA", 17, 17, "RIGHT", "MAP_PALM_ROUTE03", "Brisa -> Rota 03", "qa_rota03.png")

    r3 = MAPS["MAP_PALM_ROUTE03"]
    # Emenda: na Rota 03 o corredor ocupa as linhas 9-13, mas na Ferralia so 9-11 sao passaveis.
    q.goto("MAP_PALM_ROUTE03", r3["w"] - 1, 13)
    q.run(["press RIGHT 18 0", "wait 60"])
    check(q, "MAP_PALM_ROUTE03", "Rota 03 linha 13: emenda bloqueada (defeito conhecido)")
    cruzar(q, "MAP_PALM_ROUTE03", r3["w"] - 1, 10, "RIGHT", "MAP_PALM_FERRALIA",
           "Rota 03 -> Ferralia (conexao, linha 10)", "qa_ferralia.png")
    shutil.copy(q.state, f"{work}/qa_ferralia.ss")

    # Volta
    cruzar(q, "MAP_PALM_FERRALIA", 0, 10, "LEFT", "MAP_PALM_ROUTE03", "Ferralia -> Rota 03 (conexao)")
    cruzar(q, "MAP_PALM_ROUTE03", 2, 10, "LEFT", "MAP_PALM_BRISA", "Rota 03 -> Brisa")
    cruzar(q, "MAP_PALM_BRISA", 8, 10, "UP", "MAP_PALM_ROUTE02", "Brisa -> Rota 02")
    cruzar(q, "MAP_PALM_ROUTE02", 11, 2, "UP", "MAP_OLDALE_TOWN", "Rota 02 -> Colheita")
    cruzar(q, "MAP_OLDALE_TOWN", 9, 1, "UP", "MAP_ROUTE101", "Colheita -> Rota 01")
    cruzar(q, "MAP_ROUTE101", 2, 4, "LEFT", "MAP_LITTLEROOT_TOWN", "Rota 01 -> Vila Inicial")

    print("\nRESUMO")
    for r in resultados:
        print(" ", r[1], r[0])
    print("paradas para batalha/dialogo:", q.battles)


if __name__ == "__main__":
    main(*sys.argv[1:5])
