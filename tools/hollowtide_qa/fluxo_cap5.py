#!/usr/bin/env python3
"""QA do Capitulo 5 (Route 5) jogado de verdade a partir do Tradepost depois de "O Preco da Troca":
saida norte aberta -> Route 5 (conexao; o canal vira o rio) -> Tiago, Odair, Lia, Dudu com visao -> 3 itens
-> Pillarton (conexao): Tchum, Lela recusa antes das valvulas, 2 recrutas, 3 valvulas, Lela -> agua de volta
-> Centro Pokemon -> volta a Route 5 e ao Tradepost.
Uso: fluxo_cap5.py ROM RUNNER WORKDIR ESTADO_POS_TROCA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
T, R5, P = "MAP_PALM_TRADEPOST", "MAP_PALM_ROUTE05", "MAP_PALM_PILLARTON"
G1, G2, LELA = 17, 26, 32   # TRAINER_GRUNT_WEATHER_INST_1/_4, TRAINER_SHELLY_WEATHER_INSTITUTE
TCHUM = 270                 # TRAINER_WINONA_1 (Tchum)
FORTREE_DEFEATED = 0x4F5
GYM = "MAP_FORTREE_CITY_GYM"
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
    for (x, y, face, flag, nome) in [(14, 32, "LEFT", 0x454, "Super Potion da ilha"), (36, 22, "RIGHT", 0x47C, "Soft Sand do leito seco"),
                                     (7, 11, "LEFT", 0x409, "Ether da varzea")]:
        q.goto(R5, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(flag), f"Route 5: {nome} coletado")
    q.goto(R5, 16, 1); q.run(["press UP 30 0", "wait 90", "shot cap5_pillarton.png"])
    ok(q.mapname() == P, "Route 5 -> Pillarton (conexao)")
    import shutil
    shutil.copy(q.state, f"{work}/cap5_pillarton.ss")
    q.goto(P, 23, 37); q.run(["press UP 10 10", "press A 4 40", "mash B 40", "wait 30", "mash B 10"])
    ok(q.mapname() == P, "Tchum recebe o jogador")
    q.goto(P, 47, 8); q.run(["press RIGHT 10 10", "press A 4 40", "mash B 30", "wait 30"])
    ok(not q.in_battle() and not q.flag(TF + LELA), "Lela nao luta antes das valvulas")
    q.run(["setflag 1270 30"])            # os recrutas da crista sao enfrentados de proposito logo abaixo
    q.goto(P, 16, 7); q.run(["press UP 10 10", "press A 4 40", "mash B 20", "clearflag 1270 30"])
    ok(q.flag(0x38), "Valvula 1 aberta")
    for (ax, ay, walk, nome, tid) in [(18, 7, "walk RIGHT 1", "Recruta da barragem 1", G1), (29, 8, "walk RIGHT 1", "Recruta da barragem 2", G2)]:
        before = getattr(q, "battles", 0)
        q.goto(P, ax, ay)
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
        ok(seen, f"{nome} avistou o jogador")
        ok(battle(q, TF + tid), f"Venceu {nome}")
        q.run(["mash B 16"])
    DAM = {(20, 7), (31, 8)}             # onde os recrutas da crista param depois de avistar o jogador
    for (x, fl, n) in [(26, 0x39, 2), (36, 0x3A, 3)]:
        q.goto(P, x, 7, avoid=DAM); q.run(["press UP 10 10", "press A 4 40", "mash B 20"])
        ok(q.flag(fl), f"Valvula {n} aberta")
    q.run(["shot cap5_valvulas.png"])
    q.strong()   # cura antes da admin
    q.goto(P, 47, 8, avoid=DAM); q.run(["press RIGHT 10 10", "press A 4 40"])
    ok(battle(q, TF + LELA, tries=140), "Venceu a admin LELA")
    for _ in range(10):
        q.run(["mash A 8", "mash B 6"])
        if q.flag(0x3B):
            break
    q.run(["mash B 20", "shot cap5_agua.png"])
    ok(q.flag(0x3B), "Agua de volta: Lela deixou a barragem")
    shutil.copy(q.state, f"{work}/cap5_pos_lela.ss")
    # ginasio do Tchum: portoes giratorios (BFS sobre posicao + orientacao, porta de rotating_gate.c)
    q.run(["setflag 1270 30"])            # treinadores do ginasio nao interrompem a travessia dos portoes
    q.goto(P, 43, 19, avoid=DAM); q.run(["press UP 30 0", "wait 120", "shot cap5_ginasio.png"])
    ok(q.mapname() == GYM, "Ginasio do Tchum aberto depois da Lela")
    import qa_driver as D
    m = D.MAPS[GYM]
    path = D.gate_bfs(m, tuple(q.where[2:]), (15, 3), D.FORTREE_GATES)
    ok(path is not None, f"Portoes: solucao encontrada ({len(path or [])} passos)")
    pos, oris = tuple(q.where[2:]), tuple(g[3] for g in D.FORTREE_GATES)
    DXY = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    for i in range(0, len(path), 6):
        chunk = path[i:i + 6]
        for d in chunk:
            nx, ny = pos[0] + DXY[d][0], pos[1] + DXY[d][1]
            _, oris = D._gate_move(m, D.FORTREE_GATES, oris, nx, ny, d)
            pos = (nx, ny)
        q.run(sum([[f"walk {d} 1", "wait 6"] for d in chunk], []))
        if tuple(q.where[2:]) != pos:
            q.run(["shot cap5_portoes_falha.png"])
            ok(False, f"Portoes: posicao divergiu no passo {i} (jogo {q.where[2:]}, simulado {pos})")
    ok(tuple(q.where[2:]) == (15, 3), "Portoes: chegou diante do Tchum")
    q.strong()   # cura antes do lider
    q.run(["press UP 10 10", "press A 4 40"])
    ok(battle(q, TF + TCHUM, tries=140), "Venceu TCHUM")
    for _ in range(10):
        q.run(["mash A 8", "mash B 6"])
        if q.flag(0x860 + 10):
            break
    q.run(["mash B 20", "shot cap5_insignia.png"])
    ok(q.flag(0x860 + 10) and q.flag(FORTREE_DEFEATED), "Insignia dos Pilares recebida")
    shutil.copy(q.state, f"{work}/cap5_pos_tchum.ss")
    back = D.gate_bfs(m, (15, 3), (15, 23), [(gx, gy, sh, o) for (gx, gy, sh, _), o in zip(D.FORTREE_GATES, oris)])
    ok(back is not None, "Portoes: caminho de volta a partir do estado atual")
    for i in range(0, len(back), 6):
        q.run(sum([[f"walk {d} 1", "wait 6"] for d in back[i:i + 6]], []))
    q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == P and tuple(q.where[2:]) in ((43, 19), (43, 20)), "Saiu do ginasio na porta certa")
    shutil.copy(q.state, f"{work}/c5rua.ss")
    q.run(["clearflag 1270 30"])
    q.goto(P, 10, 17); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == "MAP_LAVARIDGE_TOWN_POKEMON_CENTER_1F", "Pillarton -> Centro Pokemon")
    q.goto("MAP_LAVARIDGE_TOWN_POKEMON_CENTER_1F", 7, 8); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == P and tuple(q.where[2:]) in ((10, 17), (10, 18)), "Centro Pokemon -> Pillarton (porta certa)")
    q.goto(P, 20, 43); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == R5, "Pillarton -> Route 5 (conexao)")
    q.goto(R5, 20, 51); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == T, "Route 5 -> Tradepost (conexao)")
    print("\nRESUMO CAPITULO 5 (Route 5 e Pillarton)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
