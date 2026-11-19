#!/usr/bin/env python3
"""QA de eventos do Capitulo 1, jogando de verdade (sem injetar flags de historia):
recruta da Team Palm -> valvula -> ginasio (3 comportas, Josh, Tommy) -> Nevard -> insignia -> Rota 2 liberada.

Usa o "modo forte" (1o Pokemon nivel 100 em RAM) para que as batalhas nao interrompam o teste de eventos;
o balanceamento tem teste proprio. Encontros selvagens desligados pela flag de QA.
Uso: fluxo_cap1_eventos.py ROM RUNNER WORKDIR ESTADO_NA_COLHEITA
"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

TF = 0x500  # TRAINER_FLAGS_START
RECRUIT, JOSH, TOMMY, NEVARD = TF + 857, TF + 320, TF + 321, TF + 265
FLAG_IRRIGATION, FLAG_BADGE1, FLAG_GYM = 0x25, 0x860 + 7, 0x4F0
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def battle(q, flag, tries=40):
    """Avanca dialogo e batalha (FIGHT -> 1o golpe) ate a flag do treinador ligar."""
    for _ in range(tries):
        if q.flag(flag) and not q.in_battle():
            q.run(["mash B 20"])
            return True
        if q.in_battle():
            # alterna os 4 golpes (o 1o pode nao afetar o alvo, ex.: Normal contra Fantasma)
            nav = [[], ["press RIGHT 4 6"], ["press DOWN 4 6"], ["press DOWN 4 6", "press RIGHT 4 6"]][_ % 4]
            q.run(["press B 4 8", "press UP 4 6", "press LEFT 4 6", "press A 4 20", "press UP 4 6", "press LEFT 4 6"]
                  + nav + ["press A 4 20", "wait 150", "mash B 4"])
        else:
            q.run(["mash B 6", "press A 4 30"])  # dialogo pre-batalha (falando de frente para o treinador)
    return q.flag(flag)


def talk(q, mapa, x, y, direcao):
    q.goto(mapa, x, y)
    q.run([f"press {direcao} 10 10", "press A 4 40"])


def main(rom, runner, work, estado):
    q = QA(rom, runner, work)
    q.load(estado); q.run([])
    q.run(["setflag 1270 31"])  # sem selvagens (QA)
    q.strong()

    # Recruta no quiosque
    talk(q, "MAP_OLDALE_TOWN", 7, 33, "UP")
    ok(battle(q, RECRUIT), "Venceu o recruta da Team Palm (quiosque)")
    q.run(["shot cap1_recruta.png"])

    # Valvula
    talk(q, "MAP_OLDALE_TOWN", 27, 24, "UP")
    q.run(["mash B 12"])
    ok(q.flag(FLAG_IRRIGATION), "Valvula aberta: irrigacao restaurada")

    # Ginasio
    q.goto("MAP_OLDALE_TOWN", 5, 22); q.run(["press UP 30 0", "wait 120", "shot cap1_ginasio.png"])
    ok(q.mapname() == "MAP_RUSTBORO_CITY_GYM", "Porta do ginasio abriu")
    G = "MAP_RUSTBORO_CITY_GYM"
    talk(q, G, 4, 15, "LEFT"); q.run(["mash B 10", "shot cap1_comporta1.png"])  # comporta 1
    talk(q, G, 6, 11, "RIGHT"); q.run(["mash B 10"])                           # comporta 2 antes do Josh: deve pedir batalha
    talk(q, G, 7, 14, "RIGHT")
    ok(battle(q, JOSH), "Venceu Josh")
    talk(q, G, 6, 11, "RIGHT"); q.run(["mash B 10", "shot cap1_comporta2.png"])
    talk(q, G, 3, 10, "LEFT")
    ok(battle(q, TOMMY), "Venceu Tommy")
    talk(q, G, 4, 7, "LEFT"); q.run(["mash B 10", "shot cap1_comporta3.png"])
    q.goto(G, 5, 3)
    ok(True, "Ponte baixou: caminho ate o Nevard aberto")
    q.run(["press UP 10 10", "press A 4 40"])
    ok(battle(q, NEVARD, tries=40), "Venceu NEVARD")
    for _ in range(10):
        q.run(["mash A 10", "mash B 6"])
        if q.flag(FLAG_BADGE1):
            break
    q.run(["mash B 20", "shot cap1_insignia.png"])
    ok(q.flag(FLAG_BADGE1) and q.flag(FLAG_GYM), "Insignia da Colheita recebida")
    shutil.copy(q.state, f"{work}/cap1_pos_nevard.ss")

    # Persistencia: sair e voltar ao ginasio mantem a ponte; depois a Rota 2 abre
    q.goto(G, 5, 18); q.goto(G, 5, 19)
    q.run(["press DOWN 20 0", "wait 120"])
    ok(q.mapname() == "MAP_OLDALE_TOWN", "Saiu do ginasio")
    q.goto("MAP_OLDALE_TOWN", 18, 34); q.run(["press DOWN 20 0", "wait 120", "shot cap1_rota2.png"])
    ok(q.mapname() == "MAP_PALM_ROUTE02", "Rota 2 liberada apos o Nevard")
    print("\nRESUMO CAPITULO 1 (eventos)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
