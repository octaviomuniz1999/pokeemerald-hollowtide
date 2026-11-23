#!/usr/bin/env python3
"""Balanceamento antes da Jay (Cap. 2): a Breezeport nao tinha Pokemon selvagens. Entram os do canone (POKEDEX_LUNIA,
Cap. 2 Lv 9-21): no mato (a faixa de grama alta do noroeste, junto da mata) Hoothoot, Pidove, Shuppet e Misdreavus
(raro, o as da Jay); na orla (surf/pesca) Tentacool, Wingull, Krabby, Staryu e Corsola (raro). Lv 14-18 no mato
preenche o salto Route 2 (ate 13) -> Jay (Shuppet 18, Misdreavus 21, niveis do canone, sem mudanca).
Idempotente; rodar a qualquer momento depois de install_breezeport.py.
"""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave

OD = collections.OrderedDict
LAND = [("SPECIES_PIDOVE", 14, 16), ("SPECIES_HOOTHOOT", 14, 16), ("SPECIES_PIDOVE", 15, 17), ("SPECIES_HOOTHOOT", 15, 17),
        ("SPECIES_SHUPPET", 15, 17), ("SPECIES_PIDOVE", 16, 18), ("SPECIES_HOOTHOOT", 16, 18), ("SPECIES_SHUPPET", 16, 18),
        ("SPECIES_PIDOVE", 17, 18), ("SPECIES_HOOTHOOT", 17, 18), ("SPECIES_SHUPPET", 17, 18), ("SPECIES_MISDREAVUS", 16, 18)]
WATER = [("SPECIES_TENTACOOL", 15, 25), ("SPECIES_WINGULL", 15, 25), ("SPECIES_STARYU", 15, 25), ("SPECIES_TENTACOOL", 20, 28),
         ("SPECIES_CORSOLA", 20, 28)]
FISH = [("SPECIES_TENTACOOL", 5, 10), ("SPECIES_KRABBY", 5, 10), ("SPECIES_KRABBY", 15, 20), ("SPECIES_TENTACOOL", 15, 20),
        ("SPECIES_STARYU", 15, 20), ("SPECIES_STARYU", 25, 30), ("SPECIES_KRABBY", 25, 30), ("SPECIES_TENTACOOL", 25, 30),
        ("SPECIES_STARYU", 28, 32), ("SPECIES_CORSOLA", 28, 32)]


def mons(lst):
    return [OD([("min_level", a), ("max_level", b), ("species", s)]) for (s, a, b) in lst]


def main():
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_BRISA"]
    entry = OD([("map", "MAP_PALM_BRISA"), ("base_label", "gPalmBrisa"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", mons(LAND))])),
                ("water_mons", OD([("encounter_rate", 4), ("mons", mons(WATER))])),
                ("fishing_mons", OD([("encounter_rate", 30), ("mons", mons(FISH))]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE02") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    print("Breezeport: selvagens do canone (mato Lv 14-18, orla)")


if __name__ == "__main__":
    main()
