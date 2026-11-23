#!/usr/bin/env python3
"""QA das trocas do Tradepost: os 4 negociantes da praca falam, oferecem a troca e aceitam a recusa (NAO) sem
travar o jogo nem marcar a troca. A troca completa (escolha do Pokemon e cena de evolucao) nao e automatizada.
Uso: fluxo_trocas.py ROM RUNNER WORKDIR  (usa cap4_pos_troca.ss do WORKDIR)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA

TP = "MAP_PALM_TRADEPOST"
TRADERS = [("KADABRA", 14, 18, 0x275), ("MACHOKE", 16, 22, 0x276), ("GRAVELER", 17, 19, 0x277), ("HAUNTER", 11, 18, 0x278)]
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def main(rom, runner, work):
    q = QA(rom, runner, work)
    q.load(f"{work}/cap4_pos_troca.ss"); q.no_wild(); q.run(["mash B 10"])
    # entra e sai de uma casa: recarrega os objetos do mapa (o estado pode ter sido salvo com dados antigos)
    q.goto(TP, 22, 8); q.run(["press UP 30 0", "wait 120"])
    q.goto("MAP_VERDANTURF_TOWN_HOUSE", 3, 7); q.run(["press DOWN 40 0", "wait 120"])
    ok(q.mapname() == TP, "Tradepost recarregado (entra e sai do salao)")
    for (nome, x, y, flag) in TRADERS:
        q.goto(TP, x, y + 1)
        q.run(["press UP 10 10", "press A 4 40", "wait 90", f"shot troca_{nome.lower()}.png", "press A 4 40", "wait 90",
               "press A 4 40", "wait 60", "press B 4 40", "wait 60", "mash B 10"])
        ok(q.mapname() == TP and not q.flag(flag), f"Tradepost: troca do {nome} oferecida e recusada sem travar")
    print("\nRESUMO TROCAS")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:4])
