#!/usr/bin/env python3
"""Fluxo E2E: casa -> lab (Snivy) -> Rota 01 -> Colheita. Uso: fluxo_inicial.py ROM RUNNER WORKDIR ESTADO_CASA"""
import shutil, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

def main(rom, runner, work, casa):
    q = QA(rom, runner, work)
    q.load(casa); q.run([])
    # Saida de casa: a mae entrega o Medalhao de Atlas (gatilho na frente da porta)
    q.goto("MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F", 8, 7)
    for _ in range(6):
        q.run(["mash A 12", "mash B 4", "shot fluxo_medalhao.png"])
        if q.flag(0x32):
            break
    assert q.flag(0x32), "Medalhao de Atlas nao entregue"
    print("OK   Mae entregou o Medalhao de Atlas", flush=True)
    q.goto("MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F", 8, 8); q.run(["press DOWN 18 0", "wait 90"])
    assert q.mapname() == "MAP_LITTLEROOT_TOWN", q.where
    q.goto("MAP_LITTLEROOT_TOWN", 14, 9); q.run(["press UP 18 0", "wait 90"])
    assert q.mapname() == "MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB", q.where
    q.goto("MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB", 6, 5)
    q.run(["press UP 10 10", "press A 4 60"])
    starter = int(os.environ.get("HT_STARTER", "1"))  # 0 Snivy (esq.), 1 Fennekin (meio), 2 Mudkip (dir.)
    for i in range(30):  # dialogo -> tela das 3 Poke Balls -> Pokedex
        if not q.flag(0x860) and q.in_starter_screen():
            mv = {0: ["press LEFT 4 20"], 1: [], 2: ["press RIGHT 4 20"]}[starter]
            q.run(["wait 30"] + mv + ["press A 4 40", "shot fluxo_escolha.png", "press A 4 60"])
            continue
        key = "B" if q.flag(0x860) else "A"  # depois da escolha, B avanca o texto sem reabrir a conversa
        q.run([f"mash {key} 3" if key == "A" else "mash B 10", f"shot fluxo_lab_{i:02d}.png"] + (["walk DOWN 1"] if key == "B" else []))
        if q.where[3] != 5:
            break
    assert q.flag(0x860), "FLAG_SYS_POKEMON_GET nao ligada"
    q.run(["shot fluxo_lab.png"]); shutil.copy(q.state, f"{work}/e2e_starter.ss")
    print("OK   Inicial recebido no laboratorio", flush=True)
    q.no_wild()  # QA de mapas: sem encontros selvagens (balanceamento tem teste proprio)
    q.goto("MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB", 6, 12); q.run(["walk DOWN 1", "wait 90"])
    q.goto("MAP_LITTLEROOT_TOWN", 33, 21); q.run(["wait 120"])
    assert q.mapname() == "MAP_ROUTE101", q.where
    q.no_wild()
    q.goto("MAP_ROUTE101", 9, 51); q.run(["walk DOWN 1", "wait 120", "shot fluxo_colheita.png"])
    assert q.mapname() == "MAP_OLDALE_TOWN", q.where
    shutil.copy(q.state, f"{work}/e2e_colheita.ss")
    print("FLUXO OK ate a Colheita; paradas para batalha/dialogo:", q.battles)

if __name__ == "__main__":
    main(*sys.argv[1:5])
