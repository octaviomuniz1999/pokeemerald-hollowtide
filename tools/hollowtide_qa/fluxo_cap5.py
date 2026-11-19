#!/usr/bin/env python3
"""QA do Capitulo 5 (Route 5) jogado de verdade a partir do Tradepost depois de "O Preco da Troca":
saida norte aberta -> Route 5 (conexao; o canal vira o rio) -> Tiago, Odair, Lia, Dudu com visao -> 3 itens
-> fim norte fechado (obras da barragem) -> volta ao Tradepost.
Uso: fluxo_cap5.py ROM RUNNER WORKDIR ESTADO_POS_TROCA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
T, R5 = "MAP_PALM_TRADEPOST", "MAP_PALM_ROUTE05"
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work, estado):
    q = QA(rom, runner, work)
    q.load(estado); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"]); q.strong()
    q.goto(T, 26, 1); q.run(["press UP 30 0", "wait 90", "shot cap5_rota5.png"])
    ok(q.mapname() == R5, "Tradepost -> Route 5 (conexao, apos o evento)")
    for (ax, ay, walk, nome, tid) in [(20, 47, "walk UP 3", "TIAGO", 88), (14, 30, "walk UP 3", "ODAIR", 92),
                                      (33, 23, "walk RIGHT 2", "DUDU", 106), (17, 8, "walk UP 3", "LIA", 95)]:
        before = getattr(q, "battles", 0)
        q.goto(R5, ax, ay)
        if q.flag(TF + tid) and getattr(q, "battles", 0) > before:
            ok(True, f"{nome} desafiou (no caminho)"); ok(True, f"Venceu {nome}")
            continue
        q.run([walk, "wait 60"])
        seen = False
        for _ in range(25):
            if q.in_battle():
                seen = True
                break
            q.run(["press A 4 30"])
        ok(seen, f"{nome} avistou o jogador e desafiou")
        ok(battle(q, TF + tid), f"Venceu {nome}")
        q.run(["mash B 16"])
    for (x, y, face, flag, nome) in [(14, 32, "LEFT", 0x454, "Super Potion da ilha"), (36, 22, "RIGHT", 0x47C, "Soft Sand do leito seco"),
                                     (7, 11, "LEFT", 0x409, "Ether da varzea")]:
        q.goto(R5, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(flag), f"Route 5: {nome} coletado")
    q.goto(R5, 16, 2); q.run(["press UP 30 0", "wait 60"])
    ok(q.mapname() == R5 and q.where[3] == 2, "Route 5: fim norte fechado (obras da barragem)")
    q.goto(R5, 20, 51); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == T, "Route 5 -> Tradepost (conexao)")
    print("\nRESUMO CAPITULO 5 (Route 5)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
