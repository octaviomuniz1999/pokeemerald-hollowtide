#!/usr/bin/env python3
"""QA do Capitulo 4 jogado de verdade: trava leste da Ferralia (antes e depois da Insignia da Ressonancia) ->
Route 4 (Yue, Qiao, Mara com visao; 3 itens) -> Tradepost (conexao) -> "O Preco da Troca" (Wen -> operador
da estacao -> Wen: mensageira da Palm vai embora, Amulet Coin) -> item do cais -> Centro Pokemon ida e volta.
Uso: fluxo_cap4.py ROM RUNNER WORKDIR ESTADO_PRE_VESSEL ESTADO_POS_VESSEL
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
F, R4, T = "MAP_PALM_FERRALIA", "MAP_PALM_ROUTE04", "MAP_PALM_TRADEPOST"
WEN_ASKED, PERMIT, DONE = 0x35, 0x36, 0x37
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def talk(q, mapa, x, y, face):
    q.goto(mapa, x, y)
    q.run([f"press {face} 10 10", "press A 4 40"])


def main(rom, runner, work, pre, pos):
    q = QA(rom, runner, work)
    # trava antes do Vessel
    q.load(pre); q.run(["mash B 10"]); q.no_wild()
    q.goto(F, 69, 40); q.run(["press RIGHT 18 0", "wait 60", "mash A 24", "mash B 6", "wait 60"])
    ok(q.mapname() == F and tuple(q.where[2:]) == (69, 40), "Ferralia: saida leste fechada antes da insignia (recua)")
    # depois do Vessel
    q.load(pos); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"]); q.strong()
    if q.mapname() == "MAP_MAUVILLE_CITY_GYM":
        q.goto("MAP_MAUVILLE_CITY_GYM", 5, 19); q.run(["press DOWN 30 0", "wait 120"])
    q.goto(F, 70, 40); q.run(["press RIGHT 30 0", "wait 90", "shot cap4_rota4.png"])
    ok(q.mapname() == R4, "Ferralia -> Route 4 (conexao, apos a insignia)")
    for (ax, ay, walk, nome, tid) in [(14, 17, "walk RIGHT 2", "YUE", 39), (36, 16, "walk RIGHT 2", "QIAO", 45),
                                      (44, 13, "walk RIGHT 1", "MARA", 75)]:
        before = getattr(q, "battles", 0)
        q.goto(R4, ax, ay)
        if q.flag(TF + tid):   # ja desafiou e perdeu no caminho ate o ponto de aproximacao
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
    for (x, y, face, flag, nome) in [(19, 13, "UP", 0x406, "Super Potion"), (16, 22, "RIGHT", 0x407, "Oran Berry 1"),
                                     (16, 23, "RIGHT", 0x44F, "Oran Berry 2")]:
        talk(q, R4, x, y, face); q.run(["mash B 12"])
        ok(q.flag(flag), f"Route 4: {nome} coletado")
    q.goto(R4, 51, 16); q.run(["press RIGHT 30 0", "wait 90", "shot cap4_tradepost.png"])
    ok(q.mapname() == T, "Route 4 -> Tradepost (conexao)")
    # O Preco da Troca (antes: a saida norte para a Route 5 esta trancada)
    q.goto(T, 26, 2); q.run(["press UP 18 0", "wait 60", "mash A 24", "mash B 6", "wait 60"])
    ok(q.mapname() == T and tuple(q.where[2:]) == (26, 2), "Tradepost: saida norte fechada antes do evento (recua)")
    talk(q, T, 21, 26, "UP"); q.run(["mash B 50", "wait 30", "mash B 10"])
    ok(q.flag(WEN_ASKED) and not q.flag(PERMIT), "Mestre Wen pediu a autorizacao de carga")
    talk(q, T, 14, 10, "UP"); q.run(["mash B 30", "wait 60", "mash B 20"])
    ok(q.flag(PERMIT), "Operador da estacao entregou a autorizacao original")
    talk(q, T, 21, 26, "UP")
    for _ in range(12):
        q.run(["mash A 6", "mash B 4"])
        if q.flag(DONE):
            break
    q.run(["mash B 30", "shot cap4_troca.png"])
    ok(q.flag(DONE), "O Preco da Troca resolvido: feira reaberta")
    import shutil
    shutil.copy(q.state, f"{work}/cap4_pos_troca.ss")
    talk(q, T, 36, 24, "RIGHT"); q.run(["mash B 12"])
    ok(q.flag(0x453), "Tradepost: Great Ball do cais coletada (ponte do canal)")
    q.goto(T, 13, 15); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == "MAP_VERDANTURF_TOWN_POKEMON_CENTER_1F", "Tradepost -> Centro Pokemon")
    q.goto("MAP_VERDANTURF_TOWN_POKEMON_CENTER_1F", 7, 8); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == T and tuple(q.where[2:]) in ((13, 15), (13, 16)), "Centro Pokemon -> Tradepost (porta certa)")
    q.goto(T, 0, 16); q.run(["press LEFT 30 0", "wait 90"])
    ok(q.mapname() == R4, "Tradepost -> Route 4 (conexao)")
    q.goto(R4, 0, 16); q.run(["press LEFT 30 0", "wait 90"])
    ok(q.mapname() == F, "Route 4 -> Ferralia (conexao)")
    print("\nRESUMO CAPITULO 4")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:6])
