#!/usr/bin/env python3
"""QA de eventos do Capitulo 2, jogado de verdade a partir do estado pos-Nevard:
Harvestvale -> Route 2 -> Breezeport -> anfitria -> 3 postes -> Teatro -> holofotes (E, D, E) -> Jay -> insignia
-> saida oeste para a Route 3 liberada. Time de QA nivel 100; sem selvagens.
Uso: fluxo_cap2_eventos.py ROM RUNNER WORKDIR ESTADO_POS_NEVARD
"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

TF = 0x500
JAY = TF + 861
FLAG_STARTED, FLAG_LAMP1, FLAG_LAMP2, FLAG_LAMP3, FLAG_LIGHTS, FLAG_JAY_WON = 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C
FLAG_BADGE2 = 0x860 + 8
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def talk(q, mapa, x, y, d):
    q.goto(mapa, x, y)
    q.run([f"press {d} 10 10", "press A 4 40", "mash B 14"])


def battle(q, flag, tries=80):
    for _ in range(tries):
        if q.flag(flag) and not q.in_battle():
            q.run(["mash B 20"])
            return True
        if q.in_battle():
            # alterna os 4 golpes (o 1o pode nao afetar o alvo, ex.: Normal contra Fantasma)
            nav = [[], ["press DOWN 4 6"], [], ["press DOWN 4 6"], ["press RIGHT 4 6"], ["press DOWN 4 6", "press RIGHT 4 6"]][_ % 6]  # prioriza slots 0 e 2
            q.run(["press B 4 8", "press UP 4 6", "press LEFT 4 6", "press A 4 20", "press UP 4 6", "press LEFT 4 6"]
                  + nav + ["press A 4 20", "wait 150", "mash B 4"])
        else:
            q.run(["mash B 6", "press A 4 30"])
    return q.flag(flag)


def main(rom, runner, work, estado):
    q = QA(rom, runner, work)
    q.load(estado); q.run(["mash B 10"])
    q.run(["setflag 1270 31", "setflag 1270 30"])
    q.strong()
    G = "MAP_RUSTBORO_CITY_GYM"
    if q.mapname() == G:
        q.goto(G, 5, 19); q.run(["press DOWN 30 0", "wait 120"])
    q.goto("MAP_OLDALE_TOWN", 18, 36); q.run(["press DOWN 30 0", "wait 120"])
    q.goto("MAP_PALM_ROUTE02", 19, 47); q.run(["press DOWN 30 0", "wait 150"])
    ok(q.mapname() == "MAP_PALM_BRISA", "Chegou a Breezeport pela Route 2")
    B = "MAP_PALM_BRISA"
    # Postes antes da anfitria: nao acendem
    talk(q, B, 33, 23, "UP")
    ok(not q.flag(FLAG_LAMP2), "Poste da praca nao acende antes de falar com a anfitria")
    talk(q, B, 45, 30, "UP")
    ok(q.flag(FLAG_STARTED), "Anfitria do festival pediu ajuda")
    for (x, y, f, nome) in [(12, 22, FLAG_LAMP1, "bairro oeste"), (33, 23, FLAG_LAMP2, "praca"), (60, 36, FLAG_LAMP3, "calcadao")]:
        talk(q, B, x, y, "UP")
        ok(q.flag(f), f"Poste do {nome} aceso")
    ok(q.flag(FLAG_LIGHTS), "Tres postes acesos: Teatro aberto")
    q.run(["shot cap2_postes.png"])
    q.goto(B, 47, 28); q.run(["press UP 30 0", "wait 120", "shot cap2_teatro.png"])
    ok(q.mapname() == "MAP_PALM_TEATRO", "Entrou no Teatro dos Ecos")
    T = "MAP_PALM_TEATRO"
    for (x, d) in [(3, "L"), (7, "R"), (3, "L")]:   # holofotes: esquerda, direita, esquerda
        talk(q, T, x, 9, "UP")
    q.goto(T, 5, 3); q.run(["press UP 10 10", "press A 4 40"])
    ok(battle(q, JAY), "Venceu JAY")
    for _ in range(10):
        q.run(["mash A 10", "mash B 6"])
        if q.flag(FLAG_BADGE2):
            break
    q.run(["mash B 20", "shot cap2_insignia.png"])
    ok(q.flag(FLAG_BADGE2) and q.flag(FLAG_JAY_WON), "Insignia Eco recebida")
    shutil.copy(q.state, f"{work}/cap2_pos_jay.ss")
    q.goto(T, 5, 13); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == B, "Saiu do Teatro")
    q.goto(B, 1, 40); q.run(["press LEFT 30 0", "wait 120", "shot cap2_rota3.png"])
    ok(q.mapname() == "MAP_PALM_ROUTE03", "Route 3 liberada pela praia oeste apos a Jay")
    print("\nRESUMO CAPITULO 2 (eventos)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
