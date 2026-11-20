#!/usr/bin/env python3
"""QA do Capitulo 12 (parte 1): escadaria da Passway (fechada sem a convocacao do Doge; aberta com ela) ->
Storm Mountain: Steven na encosta, Leon no desfiladeiro, 3 itens, o alto da trilha.
Parte de c8passway.ss (o conteudo da montanha so depende de FLAG_HT_POSTGAME_DATA, ligada aqui como no
pos-creditos; o caminho Liga -> creditos -> convocacao e conferido em fluxo_cap11b/11c).
Uso: fluxo_cap12.py ROM RUNNER WORKDIR ESTADO_PASSWAY (c8passway.ss)
"""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

PW, ST = "MAP_PALM_PASSWAY", "MAP_PALM_STORM_TRAIL"
POSTGAME, STEVEN, LEON = 0x68, 0xE9, 0x1AA
FLAGS = {m.group(1): int(m.group(2), 16) for m in re.finditer(r"#define (FLAG_ITEM_\w+)\s+(0x[0-9A-Fa-f]+)",
         open(os.path.join(os.path.dirname(__file__), "..", "..", "include", "constants", "flags.h")).read())}
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "setflag 1270 30", f"clearflag 1270 {POSTGAME:X}"]); q.strong()
    q.goto(PW, 17, 10); q.run(["press UP 16 0", "wait 30"])
    for _ in range(15):                      # o guardiao fala e o jogador recua um passo
        q.run(["press A 4 30", "wait 20"])
        if q.where[3] >= 10:
            break
    q.run(["mash B 6", "wait 40"])
    ok(q.mapname() == PW and q.where[3] >= 10, "Passway: escadaria fechada antes da convocacao do Doge")
    q.run([f"setflag 1270 {POSTGAME:X}"])
    q.goto(PW, 17, 0); q.run(["press UP 30 0", "wait 60", "shot cap12_trilha.png"])
    ok(q.mapname() == ST and q.where[2] == 19 and q.where[3] >= 47, "Escadaria -> Storm Mountain (conexao continua, x da trilha = x da Passway + 2)")
    q.goto(ST, 19, 39); q.run(["press UP 8 0", "wait 40"])
    for _ in range(20):
        if q.flag(STEVEN):
            break
        q.run(["wait 30", "mash A 6"])
    q.run(["mash B 6", "shot cap12_steven.png"])
    ok(q.flag(STEVEN), "Steven na encosta (falas do roteiro)")
    q.goto(ST, 8, 21); q.run(["press UP 8 0", "wait 40"])
    for _ in range(20):
        if q.flag(LEON):
            break
        q.run(["wait 30", "mash A 6"])
    q.run(["mash B 6", "shot cap12_leon.png"])
    ok(q.flag(LEON), "Leon no desfiladeiro (falas do roteiro)")
    for (x, y, face, fname, nome) in [(29, 47, "RIGHT", "FLAG_ITEM_ROUTE_114_RARE_CANDY", "Max Elixir"),
                                      (35, 28, "RIGHT", "FLAG_ITEM_ROUTE_133_STAR_PIECE", "Full Restore"),
                                      (13, 3, "RIGHT", "FLAG_ITEM_ROUTE_121_REVIVE", "Max Revive")]:
        q.goto(ST, x, y); q.run([f"press {face} 10 10", "press A 4 40", "mash B 12"])
        ok(q.flag(FLAGS[fname]), f"Storm Mountain: {nome} coletado")
    q.goto(ST, 8, 0); q.run(["shot cap12_alto.png"])
    ok(q.mapname() == ST and tuple(q.where[2:]) == (8, 0), "Alto da trilha (o caminho segue para o norte)")
    shutil.copy(q.state, f"{work}/c12trilha.ss")
    q.goto(ST, 19, 49); q.run(["press DOWN 30 0", "wait 60"])
    ok(q.mapname() == PW, "Trilha -> Passway (volta)")
    print("\nRESUMO CAPITULO 12 (parte 1)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
