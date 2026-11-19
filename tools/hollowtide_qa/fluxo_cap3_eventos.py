#!/usr/bin/env python3
"""QA de eventos do Capitulo 3 (Ferralia), jogado de verdade a partir da chegada pela Route 3:
ginasio trancado -> Vessel no patio de carga pede ajuda -> 2 recrutas da Team Palm (visao ligada) -> Vessel
agradece e volta -> ginasio aberto -> chaves das barreiras -> Vessel -> Insignia da Ressonancia -> saida.
Uso: fluxo_cap3_eventos.py ROM RUNNER WORKDIR ESTADO_NA_FERRALIA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
GRUNT1, GRUNT2, VESSEL = TF + 0x00, TF + 0x00, TF + 0x00   # preenchidos em main() a partir de opponents.h
FLAG_CARGO, FLAG_GYM, FLAG_BADGE3 = 0x34, 0x4F2, 0x860 + 9
F, G = "MAP_PALM_FERRALIA", "MAP_MAUVILLE_CITY_GYM"
GYM_DOOR = (49, 12)
SWITCHES = [(0, 15), (4, 12), (3, 9), (8, 9)]
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def trainer_id(name):
    import re
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    t = open(os.path.join(root, "include/constants/opponents.h")).read()
    ids = {m.group(1): m.group(2) for m in re.finditer(r"#define (TRAINER_\w+)\s+(\w+)", t)}
    v = ids[name]
    while not v.isdigit():
        v = ids[v]
    return int(v)


def main(rom, runner, work, estado):
    g1, g2, ve = (TF + trainer_id(n) for n in ("TRAINER_PALM_YARD_GRUNT_1", "TRAINER_PALM_YARD_GRUNT_2", "TRAINER_PALM_VESSEL"))
    q = QA(rom, runner, work)
    q.load(estado)
    q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"])
    q.strong()
    ok(q.mapname() == F, "Na Ferralia (chegada pela Route 3)")
    q.goto(F, GYM_DOOR[0], GYM_DOOR[1] + 1); q.run(["press UP 30 0", "wait 90"])
    ok(q.mapname() == F, "Ginasio trancado antes da Carga Desviada")
    q.goto(F, 62, 29); q.run(["press RIGHT 10 10", "press A 4 40", "mash B 40", "wait 60", "mash B 10", "shot cap3_vessel_patio.png"])
    ok(not q.flag(FLAG_CARGO), "Vessel pede ajuda (evento ainda aberto)")
    for (ax, ay, walk, nome, fl) in [(64, 28, "walk RIGHT 1", "Recruta 1", g1), (64, 33, "walk RIGHT 2", "Recruta 2", g2)]:
        q.goto(F, ax, ay); q.run([walk, "wait 60"])
        seen = False
        for _ in range(25):
            if q.in_battle():
                seen = True
                break
            q.run(["press A 4 30"])
        ok(seen, f"{nome} da Team Palm avistou o jogador")
        ok(battle(q, fl), f"Venceu {nome}")
        q.run(["mash B 16"])
    q.goto(F, 62, 29); q.run(["press RIGHT 10 10", "press A 4 40"])
    for _ in range(12):
        q.run(["mash A 6", "mash B 4"])
        if q.flag(FLAG_CARGO):
            break
    q.run(["mash B 20", "shot cap3_carga.png"])
    ok(q.flag(FLAG_CARGO), "Carga recuperada: Vessel voltou ao ginasio")
    q.goto(F, GYM_DOOR[0], GYM_DOOR[1] + 1); q.run(["press UP 30 0", "wait 120", "shot cap3_ginasio.png"])
    ok(q.mapname() == G, "Ginasio aberto: entrou")
    # chaves das barreiras: tenta chegar ao lider sem pisar em chave; sem caminho, pisa na proxima chave
    # alcancavel (desviando das outras) e tenta de novo
    q.run(["setflag 1270 30"])   # treinadores do ginasio nao interrompem a navegacao do quebra-cabeca
    for tentativa in range(12):
        try:
            q.goto(G, 5, 3, avoid=SWITCHES)
            break
        except AssertionError:
            for sw in SWITCHES[tentativa % 4:] + SWITCHES[:tentativa % 4]:
                if tuple(q.where[2:]) == sw:
                    continue
                try:
                    q.goto(G, *sw, avoid=[s for s in SWITCHES if s != sw]); q.run(["wait 40"])
                    break
                except AssertionError:
                    continue
    ok(tuple(q.where[2:]) == (5, 3), "Chaves das barreiras: caminho ate o lider aberto")
    q.run(["press UP 10 10", "press A 4 40"])
    ok(battle(q, ve, tries=140), "Venceu VESSEL")
    for _ in range(10):
        q.run(["mash A 10", "mash B 6"])
        if q.flag(FLAG_BADGE3):
            break
    q.run(["mash B 20", "shot cap3_insignia.png"])
    ok(q.flag(FLAG_BADGE3) and q.flag(FLAG_GYM), "Insignia da Ressonancia recebida")
    import shutil
    shutil.copy(q.state, f"{work}/cap3_pos_vessel.ss")
    q.goto(G, 5, 19); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == F and tuple(q.where[2:]) in ((49, 13), (49, 14)), "Saiu do ginasio na porta certa")
    print("\nRESUMO CAPITULO 3 (eventos)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
