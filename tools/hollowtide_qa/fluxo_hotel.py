#!/usr/bin/env python3
"""QA do Grand Hotel de Tidemouth: fechado durante a crise (FLAG_HT_TIDEMOUTH_COMPLEX_DONE desligada so para o
teste); aberto depois: porta, pernoite na recepcao, funcionario da escada e volta pela porta certa.
Uso: fluxo_hotel.py ROM RUNNER WORKDIR ESTADO_TIDEMOUTH (c10nami.ss)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

TD, GH = "MAP_PALM_TIDEMOUTH", "MAP_PALM_GRAND_HOTEL"
DONE = 0x55
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "setflag 1270 30"])
    if q.mapname() != TD:
        raise AssertionError(f"estado fora de Tidemouth: {q.mapname()}")
    # porto depois da crise: o marinheiro fala do mar calmo e ainda leva ao complexo (Nami la, com o Surf)
    q.goto(TD, 33, 38, avoid={(33, 37)}); q.run(["press UP 20 0", "wait 90", "shot porto_calmo.png"])
    for _ in range(8):                                   # passa as paginas e responde NAO (o jogador recua)
        q.run(["press B 4 40", "wait 30"])
        if q.where[3] == 38:
            break
    q.run(["mash B 4"])
    ok(q.mapname() == TD and tuple(q.where[2:]) == (33, 38), "Porto depois da crise: barco oferecido (mar calmo); NAO recua")
    q.goto(TD, 44, 18, avoid={(46, 18), (33, 37)})
    q.run([f"clearflag 1270 {DONE:X}", "press UP 20 0", "wait 30"])
    for _ in range(10):
        q.run(["press A 4 30", "wait 10"])
        if q.where[3] >= 18:
            break
    ok(q.mapname() == TD and q.where[3] >= 18, "Grand Hotel fechado durante a crise (recua)")
    q.run([f"setflag 1270 {DONE:X}", "mash B 4"])
    q.goto(TD, 44, 17, avoid={(46, 18), (33, 37)}); q.run(["press UP 20 0", "wait 120"])
    ok(q.mapname() == GH, "Porta do hotel -> saguao")
    q.goto(GH, 8, 4); q.run(["press UP 10 10", "press A 4 40"])
    for _ in range(12):
        q.run(["press A 4 40", "wait 30"])
    q.run(["wait 200", "mash A 6", "mash B 6", "shot hotel_recepcao.png"])
    ok(q.mapname() == GH and tuple(q.where[2:]) == (8, 4), "Recepcao: pernoite por conta da casa, cena termina")
    q.goto(GH, 16, 2); q.run(["press UP 10 10", "press A 4 40", "mash A 6", "mash B 6"])
    ok(q.mapname() == GH and tuple(q.where[2:]) == (16, 2), "Funcionario segura a escada")
    q.goto(GH, 8, 6); q.run(["press DOWN 40 0", "wait 120"])
    ok(q.mapname() == TD and tuple(q.where[2:]) == (44, 17), "Saguao -> Tidemouth (porta certa)")
    print("\nRESUMO GRAND HOTEL")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
