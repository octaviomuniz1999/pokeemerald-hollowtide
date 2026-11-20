#!/usr/bin/env python3
"""QA do Capitulo 6 jogado de verdade: trava leste da Pillarton (antes/depois da Insignia dos Pilares) ->
Route 6 (Ren, Mika, Sayo, Hana com visao; 3 itens) -> Serenia (conexao): ilusao solida antes da Jade -> Jade e
Lau -> 3 ilusoes desfeitas -> fragmento -> altar (inscricao) -> Centro Pokemon -> volta pela Route 6.
Uso: fluxo_cap6.py ROM RUNNER WORKDIR ESTADO_POS_LELA ESTADO_POS_TCHUM_RUA
"""
import shutil, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle

TF = 0x500
P, R6, S = "MAP_PALM_PILLARTON", "MAP_PALM_ROUTE06", "MAP_PALM_SERENIA"
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


GONE = set()   # objetos ja removidos (ilusoes desfeitas, fragmento coletado)


def talk(q, mapa, x, y, face, extra=("mash B 20",)):
    q.goto(mapa, x, y, ignore=GONE)
    q.run([f"press {face} 10 10", "press A 4 40"] + list(extra))


def main(rom, runner, work, pre, pos):
    q = QA(rom, runner, work)
    q.load(pre); q.run(["mash B 10"]); q.no_wild()
    q.goto(P, 53, 20, avoid={(20, 7), (31, 8)}); q.run(["press RIGHT 18 0", "wait 60", "mash A 24", "mash B 6", "wait 60"])
    ok(q.mapname() == P and tuple(q.where[2:]) == (53, 20), "Pillarton: saida leste fechada antes da insignia (recua)")
    q.load(pos); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"]); q.strong()
    q.goto(P, 54, 20, avoid={(20, 7), (31, 8)}); q.run(["press RIGHT 30 0", "wait 90", "shot cap6_rota6.png"])
    ok(q.mapname() == R6, "Pillarton -> Route 6 (conexao, apos a insignia)")
    for (ax, ay, walk, nome, tid) in [(6, 20, "walk RIGHT 2", "MIKA", 137), (22, 14, "walk RIGHT 2", "REN", 107),
                                      (31, 16, "walk DOWN 2", "SAYO", 159), (43, 20, "walk RIGHT 2", "HANA", 160)]:
        q.goto(R6, ax, ay)
        if q.flag(TF + tid):
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
    for (x, y, face, flag, nome) in [(23, 7, "LEFT", 0x40A, "Twisted Spoon do jardim de pedra"), (50, 5, "UP", 0x40B, "PP Up"),
                                     (7, 31, "LEFT", 0x40C, "Revive")]:
        talk(q, R6, x, y, face, ("mash B 12",))
        ok(q.flag(flag), f"Route 6: {nome} coletado")
    q.goto(R6, 53, 20); q.run(["press RIGHT 30 0", "wait 90", "shot cap6_serenia.png"])
    ok(q.mapname() == S, "Route 6 -> Serenia (conexao)")
    talk(q, S, 20, 17, "UP")
    ok(not q.flag(0x3D), "Ilusao continua solida antes de falar com a Jade")
    talk(q, S, 24, 20, "UP", ("mash B 60", "wait 30", "mash B 20"))
    ok(q.flag(0x3C), "Jade e Lau receberam o jogador")
    for (y, fl, n) in [(17, 0x3D, 1), (14, 0x3E, 2), (11, 0x3F, 3)]:
        talk(q, S, 20, y, "UP")
        ok(q.flag(fl), f"Ilusao {n} desfeita")
        GONE.update({(20, y - 1), (21, y - 1)})
    talk(q, S, 21, 9, "UP", ("mash B 24",))
    ok(q.flag(0x40), "Fragmento do santuario recuperado")
    GONE.add((21, 8))
    talk(q, S, 20, 7, "UP", ("mash B 40", "wait 30", "mash B 20", "shot cap6_altar.png"))
    ok(q.flag(0x41), "Fragmento devolvido ao altar: inscricao revelada")
    # ginasio da Jade: espelhos (LUA, ESTRELA, SOL), portas com simbolos, porta errada volta a entrada
    J = "MAP_PALM_JADE_GYM"
    q.run(["setflag 1270 30"])
    q.goto(S, 33, 19, ignore=GONE); q.run(["press UP 30 0", "wait 120", "shot cap6_ginasio.png"])
    ok(q.mapname() == J, "Ginasio da Jade aberto depois do altar")
    def door(x, y):
        q.goto(J, x, y + 1)
        q.run(["press UP 4 10"] + ["press A 4 50"] * 4 + ["wait 160"])
        if q.mapname() == J and tuple(q.where[2:]) == (x, y + 1):      # texto ainda aberto: mais um A
            q.run(["press A 4 50", "wait 160"])
        return tuple(q.where[2:])
    door(1, 41)                                        # entrada -> sala A
    ok(q.where[3] == 37, "Entrada -> sala A")
    door(1, 31)                                        # A: LUA (certa) -> sala B
    ok(q.where[3] == 27, "Sala A: porta da LUA leva a sala B")
    door(1, 21)                                        # B: SOL (errada) -> volta a entrada
    ok(q.mapname() == J and q.where[3] in (41, 42), "Sala B: porta errada devolve a entrada")
    door(1, 41); door(1, 31); door(7, 21)              # B: ESTRELA (certa) -> sala C
    ok(q.where[3] == 17, "Sala B: porta da ESTRELA leva a sala C")
    door(1, 11)                                        # C: SOL (certa) -> sala da lider
    ok(q.where[3] == 7, "Sala C: porta do SOL leva a sala da Jade")
    q.strong()
    q.goto(J, 4, 3); q.run(["press UP 10 10", "press A 4 40"])
    ok(battle(q, TF + 269, tries=140), "Venceu JADE")
    for _ in range(10):
        q.run(["mash A 8", "mash B 6"])
        if q.flag(0x860 + 11):
            break
    q.run(["mash B 20", "shot cap6_insignia.png"])
    ok(q.flag(0x860 + 11), "Insignia da Serenidade recebida")
    q.goto(J, 2, 6); q.run(["press DOWN 50 0", "wait 120"])     # piso de baixo da sala volta a entrada
    q.goto(J, 4, 46); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == S and tuple(q.where[2:]) in ((33, 19), (33, 20)), "Saiu do ginasio na porta certa")
    shutil.copy(q.state, f"{work}/c6jade.ss")          # ponto de partida do Cap. 7 (5 insignias, em Serenia)
    q.run(["clearflag 1270 30"])
    q.goto(S, 6, 18, ignore=GONE); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == "MAP_FORTREE_CITY_POKEMON_CENTER_1F", "Serenia -> Centro Pokemon")
    q.goto("MAP_FORTREE_CITY_POKEMON_CENTER_1F", 7, 8); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == S and tuple(q.where[2:]) in ((6, 18), (6, 19)), "Centro Pokemon -> Serenia (porta certa)")
    q.goto(S, 0, 20); q.run(["press LEFT 30 0", "wait 90"])
    ok(q.mapname() == R6, "Serenia -> Route 6 (conexao)")
    q.goto(R6, 0, 20); q.run(["press LEFT 30 0", "wait 90"])
    ok(q.mapname() == P, "Route 6 -> Pillarton (conexao)")
    print("\nRESUMO CAPITULO 6")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:6])
