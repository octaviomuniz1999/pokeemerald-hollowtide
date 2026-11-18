#!/usr/bin/env python3
"""Fluxo E2E: casa -> lab (Snivy) -> Rota 01 -> Colheita. Uso: fluxo_inicial.py ROM RUNNER WORKDIR ESTADO_CASA"""
import shutil, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

def main(rom, runner, work, casa):
    q = QA(rom, runner, work)
    q.load(casa); q.run([])
    q.goto("MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F", 8, 8); q.run(["walk DOWN 1", "wait 90"])
    assert q.mapname() == "MAP_LITTLEROOT_TOWN", q.where
    q.goto("MAP_LITTLEROOT_TOWN", 14, 9); q.run(["press UP 10 0", "wait 90"])
    assert q.mapname() == "MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB", q.where
    q.goto("MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB", 6, 5)
    q.run(["press UP 10 10", "press A 4 60", "mash A 3", "press A 4 40"])  # SIM para Snivy
    for _ in range(12):  # dialogos ate liberar (A de frente para o Alex reabre a conversa)
        q.run(["mash A 15", "walk DOWN 1"])
        if q.where[3] != 5:
            break
    q.run(["shot fluxo_lab.png"]); shutil.copy(q.state, f"{work}/e2e_starter.ss")
    q.goto("MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB", 6, 12); q.run(["walk DOWN 1", "wait 90"])
    q.goto("MAP_LITTLEROOT_TOWN", 33, 21); q.run(["wait 120"])
    assert q.mapname() == "MAP_ROUTE101", q.where
    q.goto("MAP_ROUTE101", 9, 51); q.run(["walk DOWN 1", "wait 120", "shot fluxo_colheita.png"])
    assert q.mapname() == "MAP_OLDALE_TOWN", q.where
    shutil.copy(q.state, f"{work}/e2e_colheita.ss")
    print("FLUXO OK ate a Colheita; paradas para batalha/dialogo:", q.battles)

if __name__ == "__main__":
    main(*sys.argv[1:5])
