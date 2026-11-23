#!/usr/bin/env python3
"""Balanceamento do Cap. 1: a Route 1 (MAP_ROUTE101) ia so ate Lv 6, mas o canone do capitulo e Lv 3-9 e o teste de
balanco mostra que o inicial sozinho, sem itens, vence o Nevard (Shroomish 12, Treecko 14) a partir do Lv 10 (no Lv 8
perde). Os encontros comuns continuam baixos (3-5) e os raros sobem ate 9, para o jogador conseguir treinar ate ~10.
Mesmas especies do canone (Zigzagoon, Fletchling, Sewaddle, Bidoof, Shinx raro). Idempotente.
"""
import collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave

OD = collections.OrderedDict
LAND = [("SPECIES_ZIGZAGOON", 3, 4), ("SPECIES_FLETCHLING", 3, 4), ("SPECIES_SEWADDLE", 4, 5), ("SPECIES_BIDOOF", 3, 5),
        ("SPECIES_ZIGZAGOON", 4, 6), ("SPECIES_FLETCHLING", 4, 6), ("SPECIES_SEWADDLE", 6, 8), ("SPECIES_BIDOOF", 6, 8),
        ("SPECIES_SHINX", 7, 9), ("SPECIES_SEWADDLE", 7, 9), ("SPECIES_SHINX", 8, 9), ("SPECIES_ZIGZAGOON", 8, 9)]


def main():
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    for e in wj["wild_encounter_groups"][0]["encounters"]:
        if e.get("map") == "MAP_ROUTE101":
            e["land_mons"]["mons"] = [OD([("min_level", a), ("max_level", b), ("species", s)]) for (s, a, b) in LAND]
            break
    else:
        raise SystemExit("MAP_ROUTE101 sem encontros")
    jsave(wp, wj)
    print("Route 1: selvagens Lv 3-9 (canone do Cap. 1)")


if __name__ == "__main__":
    main()
