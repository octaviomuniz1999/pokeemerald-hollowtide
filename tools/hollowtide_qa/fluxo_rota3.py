#!/usr/bin/env python3
"""QA da Route 3 jogada de verdade (estado pos-Jay), visao dos treinadores LIGADA:
Teatro -> Breezeport -> praia oeste (conexao) -> Rui -> Tomas -> Iara -> Bento (as trilhas se juntam na serra) -> Davi ->
3 itens (ponta de areia, clareira, planalto) -> saida norte. Time de QA nivel 100; sem selvagens.
Uso: fluxo_rota3.py ROM RUNNER WORKDIR ESTADO_POS_JAY
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
R3 = "MAP_PALM_ROUTE03"
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work, estado):
    q = QA(rom, runner, work)
    q.load(estado)
    q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"])
    q.strong()
    if q.mapname() == "MAP_PALM_TEATRO":
        q.goto("MAP_PALM_TEATRO", 5, 13); q.run(["press DOWN 30 0", "wait 120"])
    q.goto("MAP_PALM_BRISA", 1, 40); q.run(["press LEFT 20 0", "wait 60", "shot r3_praia.png"])
    ok(q.mapname() == R3, "Breezeport -> Route 3 pela praia (conexao)")
    # (aproximacao fora da visao, passo para dentro dela, nome, id)
    for (ax, ay, walk, nome, tid) in [(33, 64, "walk UP 2", "RUI", 11), (40, 46, "walk UP 2", "TOMAS", 12),
                                      (31, 33, "walk UP 3", "IARA", 15), (14, 28, "walk UP 2", "BENTO", 13),
                                      (33, 10, "walk LEFT 3", "DAVI", 29)]:
        before = getattr(q, "battles", 0)
        q.goto(R3, ax, ay)
        if q.flag(TF + tid) and getattr(q, "battles", 0) > before:   # desafiou no caminho (ex.: Davi na estrada)
            ok(True, f"{nome} avistou o jogador e desafiou (no caminho)")
            ok(True, f"Venceu {nome}")
            continue
        q.run([walk, "wait 60"])
        seen = False
        for _ in range(15):
            if q.in_battle():
                seen = True
                break
            q.run(["press A 4 30"])
        ok(seen, f"{nome} avistou o jogador e desafiou")
        ok(battle(q, TF + tid), f"Venceu {nome}")
        q.run(["mash B 16"])
    for (x, y, face, flag, nome) in [(8, 10, "UP", 0x455, "Revive do planalto"), (17, 29, "RIGHT", 0x450, "Great Ball da clareira"),
                                     (3, 73, "DOWN", 0x408, "Big Pearl da ponta de areia")]:
        q.goto(R3, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(flag), f"{nome} coletado")
    q.goto(R3, 25, 1); q.run(["shot r3_planalto.png", "press UP 30 0", "wait 120"])
    ok(q.mapname() == "MAP_PALM_FERRALIA", "Route 3 -> Ferralia pelo planalto")
    print("\nRESUMO ROUTE 3")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
