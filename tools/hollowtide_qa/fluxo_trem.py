#!/usr/bin/env python3
"""QA da ferrovia: antes do Vega (Tradepost, Cap. 4) a bilheteira diz que os trens estao suspensos e a porta da
estacao funciona nos dois sentidos; depois do Vega (Voltara, Cap. 9): Voltara -> Ferralia e Ferralia -> Voltara de
trem, saindo nas portas certas das duas cidades.
Uso: fluxo_trem.py ROM RUNNER WORKDIR ESTADO_TRADEPOST (cap4_pos_troca.ss) ESTADO_VOLTARA (c9hoc.ss)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

TP, VT, FR = "MAP_PALM_TRADEPOST", "MAP_PALM_VOLTARA", "MAP_PALM_FERRALIA"
STV, STF, STT = "MAP_PALM_STATION_VOLTARA", "MAP_PALM_STATION_FERRALIA", "MAP_PALM_STATION_TRADEPOST"
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def enter(q, city, door, station, label):
    q.goto(city, door[0], door[1] + 1); q.run(["press UP 20 0", "wait 120"])
    ok(q.mapname() == station, f"{label}: porta da estacao -> saguao")


def leave(q, station, city, door, label):
    q.goto(station, 5, 7); q.run(["press DOWN 20 0", "wait 120"])
    ok(q.mapname() == city and tuple(q.where[2:]) == (door[0], door[1] + 1), f"{label}: saguao -> cidade (porta certa)")


def ride_first(q, station, dest, label):
    """Fala com a bilheteira e aceita o primeiro destino oferecido."""
    q.goto(station, 5, 5); q.run(["press UP 10 10", "press A 4 40"])
    for _ in range(40):
        q.run(["press A 4 30", "wait 20"])
        if q.mapname() == dest:
            break
    q.run(["wait 60", "mash B 6"])
    ok(q.mapname() == dest, label)


def main(rom, runner, work, pre_tp, pre_vt):
    q = QA(rom, runner, work)
    q.load(pre_tp); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "setflag 1270 30"])
    enter(q, TP, (14, 7), STT, "Tradepost")
    q.goto(STT, 5, 5); q.run(["press UP 10 10", "press A 4 40", "mash A 12", "mash B 6", "shot trem_suspenso.png"])
    ok(q.mapname() == STT, "Antes do Vega: trens suspensos (a bilheteira nao vende)")
    leave(q, STT, TP, (14, 7), "Tradepost")

    q.load(pre_vt); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "setflag 1270 30"])
    if q.mapname() != VT:
        q.goto(q.mapname(), *_exit_of(q)); q.run(["press DOWN 20 0", "wait 120"])
    enter(q, VT, (26, 17), STV, "Voltara")
    ride_first(q, STV, STF, "Trem: Voltara -> Ferralia")
    q.run(["shot trem_ferralia.png"])
    leave(q, STF, FR, (28, 12), "Ferralia")
    enter(q, FR, (29, 12), STF, "Ferralia (segunda folha da porta)")
    ride_first(q, STF, STV, "Trem: Ferralia -> Voltara")
    leave(q, STV, VT, (26, 17), "Voltara")
    print("\nRESUMO FERROVIA")
    for r in res:
        print(" ", r[0], r[1])


def _exit_of(q):
    raise AssertionError(f"estado de Voltara fora de Voltara: {q.mapname()}")


if __name__ == "__main__":
    main(*sys.argv[1:6])
