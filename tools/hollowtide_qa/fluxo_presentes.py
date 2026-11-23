#!/usr/bin/env python3
"""QA dos presentes do canone: Eevee (jardineiro de Serenia, apos o arco de Lau), Porygon (sede da ferrovia de
Ferralia, apos a 3a insignia), Furfrou (salao do Tradepost, apos O Preco da Troca) e Rotom (sala dos servidores do
Centro de Dados, apos o Vega). Recusa o apelido (B no SIM/NAO).
Uso: fluxo_presentes.py ROM RUNNER WORKDIR  (usa c6jade.ss, cap3_pos_vessel.ss, cap4_pos_troca.ss, c9voltara.ss do WORKDIR)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def receive(q, face, flag):
    q.run([f"press {face} 10 10"])
    for _ in range(6):
        q.run(["press A 4 40", "mash B 24", "wait 30"])
        if q.flag(flag):
            break
    q.run(["mash B 10"])
    return q.flag(flag)


def main(rom, runner, work):
    q = QA(rom, runner, work)
    # Eevee: Serenia
    q.load(f"{work}/c6jade.ss"); q.no_wild(); q.run(["mash B 10"])
    q.goto("MAP_PALM_SERENIA", 13, 34)
    ok(receive(q, "UP", 0x271), "Serenia: jardineiro entrega o EEVEE depois do arco de Lau")
    # Porygon: sede da ferrovia de Ferralia
    q.load(f"{work}/cap3_pos_vessel.ss"); q.no_wild(); q.run(["mash B 10"])
    q.goto("MAP_PALM_FERRALIA", 28, 13); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == "MAP_PALM_STATION_FERRALIA", "Ferralia -> sede da ferrovia")
    q.goto("MAP_PALM_STATION_FERRALIA", 14, 2)
    ok(receive(q, "UP", 0x273), "Ferralia: funcionario da ferrovia entrega o PORYGON depois da 3a insignia")
    # Furfrou: salao do Tradepost
    q.load(f"{work}/cap4_pos_troca.ss"); q.no_wild(); q.run(["mash B 10"])
    q.goto("MAP_PALM_TRADEPOST", 22, 8); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == "MAP_VERDANTURF_TOWN_HOUSE", "Tradepost -> salao de tosa")
    q.goto("MAP_VERDANTURF_TOWN_HOUSE", 4, 6)
    ok(receive(q, "UP", 0x274), "Tradepost: o salao entrega o FURFROU depois de O Preco da Troca")
    # Rotom: sala dos servidores
    q.load(f"{work}/c9voltara.ss"); q.no_wild(); q.run(["mash B 10"])
    q.goto("MAP_PALM_VOLTARA", 48, 17); q.run(["press UP 30 0", "wait 120"])
    q.goto("MAP_PALM_DATA_CENTER_1F", 13, 2, avoid={(13, 3)}); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == "MAP_PALM_DATA_CENTER_2F", "Voltara -> sala dos servidores")
    q.goto("MAP_PALM_DATA_CENTER_2F", 5, 2)
    ok(receive(q, "LEFT", 0x272), "Centro de Dados: o ROTOM livre vai com o jogador")
    q.run(["shot presentes_rotom.png"])
    print("\nRESUMO PRESENTES")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:4])
