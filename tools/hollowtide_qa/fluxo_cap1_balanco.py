#!/usr/bin/env python3
"""Balanceamento do Capitulo 1: joga recruta -> ginasio -> Nevard com o inicial no nivel de chegada
(sem modo forte), escolhendo um golpe fixo por inicial. Relata vitorias, derrotas e nivel final.
Uso: HT_STARTER=0|1|2 fluxo_cap1_balanco.py ROM RUNNER WORKDIR ESTADO_NA_COLHEITA NIVEL SLOT
SLOT: 0 sup.esq, 1 sup.dir, 2 inf.esq, 3 inf.dir (posicao do golpe no menu FIGHT)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA, SYMS

TF = 0x500
RECRUIT, JOSH, TOMMY, NEVARD = TF + 857, TF + 320, TF + 321, TF + 265
NAV = {0: [], 1: ["press RIGHT 4 6"], 2: ["press DOWN 4 6"], 3: ["press DOWN 4 6", "press RIGHT 4 6"]}


def level(q):
    return q.peek32(SYMS["gParties"] + 0x54) & 0xFF


def fight(q, flag, slot, home_maps, tries=60):
    for _ in range(tries):
        if q.mapname() in home_maps:
            return "DERROTA"
        if q.flag(flag) and not q.in_battle():
            q.run(["mash B 20"])
            return "VITORIA"
        if q.in_battle():
            q.run(["press B 4 8", "press UP 4 6", "press LEFT 4 6", "press A 4 20",
                   "press UP 4 6", "press LEFT 4 6"] + NAV[slot] + ["press A 4 30", "mash B 6"])
        else:
            q.run(["mash B 6", "press A 4 30"])
    return "INDEFINIDO"


def talk(q, mapa, x, y, d):
    q.goto(mapa, x, y)
    q.run([f"press {d} 10 10", "press A 4 40"])


def main(rom, runner, work, estado, nivel, slot):
    nivel, slot = int(nivel), int(slot)
    q = QA(rom, runner, work)
    q.load(estado); q.run([])
    q.run(["setflag 1270 31"])
    q.set_level(nivel)
    home = {"MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F", "MAP_OLDALE_TOWN_POKEMON_CENTER_1F"}
    out = []
    talk(q, "MAP_OLDALE_TOWN", 7, 33, "UP"); out.append(("Recruta", fight(q, RECRUIT, slot, home), level(q)))
    if out[-1][1] != "VITORIA":
        return report(out)
    talk(q, "MAP_OLDALE_TOWN", 27, 24, "UP"); q.run(["mash B 12"])
    # jogador cura no Centro antes do ginasio (comportamento normal)
    q.goto("MAP_OLDALE_TOWN", 12, 22); q.run(["press UP 30 0", "wait 120"])
    q.goto("MAP_OLDALE_TOWN_POKEMON_CENTER_1F", 7, 4); q.run(["press UP 10 10", "press A 4 30", "mash A 25", "mash B 15"])
    q.goto("MAP_OLDALE_TOWN_POKEMON_CENTER_1F", 7, 8); q.run(["press DOWN 30 0", "wait 120"])
    q.goto("MAP_OLDALE_TOWN", 5, 22); q.run(["press UP 30 0", "wait 120"])
    G = "MAP_RUSTBORO_CITY_GYM"
    talk(q, G, 4, 15, "LEFT"); q.run(["mash B 10"])
    talk(q, G, 7, 14, "RIGHT"); out.append(("Josh", fight(q, JOSH, slot, home), level(q)))
    if out[-1][1] != "VITORIA":
        return report(out)
    talk(q, G, 6, 11, "RIGHT"); q.run(["mash B 10"])
    talk(q, G, 3, 10, "LEFT"); out.append(("Tommy", fight(q, TOMMY, slot, home), level(q)))
    if out[-1][1] != "VITORIA":
        return report(out)
    talk(q, G, 4, 7, "LEFT"); q.run(["mash B 10"])
    if os.environ.get("HT_HEAL_BEFORE_LEADER", "1") == "1":  # jogador cura no Centro antes do lider
        q.goto(G, 5, 19); q.run(["press DOWN 30 0", "wait 120"])
        q.goto("MAP_OLDALE_TOWN", 12, 22); q.run(["press UP 30 0", "wait 120"])
        q.goto("MAP_OLDALE_TOWN_POKEMON_CENTER_1F", 7, 4); q.run(["press UP 10 10", "press A 4 30", "mash A 25", "mash B 15"])
        q.goto("MAP_OLDALE_TOWN_POKEMON_CENTER_1F", 7, 8); q.run(["press DOWN 30 0", "wait 120"])
        q.goto("MAP_OLDALE_TOWN", 5, 22); q.run(["press UP 30 0", "wait 120"])
    q.goto(G, 5, 3); q.run(["press UP 10 10", "press A 4 40"])
    out.append(("NEVARD", fight(q, NEVARD, slot, home, tries=90), level(q)))
    q.run(["shot balanco_fim.png"])
    report(out)


def report(out):
    print(f"BALANCO inicial={os.environ.get('HT_STARTER', '1')}")
    for nome, r, lv in out:
        print(f"  {nome}: {r} (nivel do inicial depois: {lv})")


if __name__ == "__main__":
    main(*sys.argv[1:7])
