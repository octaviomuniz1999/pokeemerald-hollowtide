#!/usr/bin/env python3
"""Pokedex regional (POKEDEX_LUNIA): encontros do canone que faltavam nas tabelas (levantamento de 23/11).
- Route 4 (G): Growlithe, Drilbur, Roggenrola entram (Meowth/Timburr ja estavam); mesmos niveis da rota.
- Route 5 (S/P reservatorio): Marill, Wooper, Barboach, Lotad (surf e pesca).
- Pillarton (P, represa): Chinchou/Lanturn.
- Tidemouth (S/P): Horsea, Clauncher, Dhelmise (raro, naufragio); Wailord vem por evolucao (Wailmer na pesca).
Sem mato alto nos mapas: Onix (Pillarton), Lunatone/Solrock (Horizon), Smeargle/Chansey (Passway) ficam para
presentes/NPCs (registrado na AUDITORIA). Idempotente.
"""
import collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave

OD = collections.OrderedDict
def mons(lst):
    return [OD([("min_level", a), ("max_level", b), ("species", "SPECIES_" + s)]) for (s, a, b) in lst]

R4_LAND = [("MEOWTH", 19, 22), ("GROWLITHE", 19, 22), ("TIMBURR", 20, 22), ("DRILBUR", 20, 22), ("ROGGENROLA", 20, 22),
           ("ELECTRIKE", 20, 22), ("MEOWTH", 20, 23), ("GROWLITHE", 20, 23), ("DRILBUR", 21, 23), ("ROGGENROLA", 21, 23),
           ("TRUBBISH", 21, 23), ("DWEBBLE", 21, 23)]
R5_WATER = [("MARILL", 24, 28), ("WOOPER", 24, 28), ("LOTAD", 24, 28), ("BARBOACH", 25, 28), ("MARILL", 26, 29)]
R5_FISH = [("MAGIKARP", 5, 10), ("BARBOACH", 5, 10), ("BARBOACH", 15, 20), ("MAGIKARP", 15, 20), ("WOOPER", 15, 20),
           ("BARBOACH", 25, 28), ("WHISCASH", 26, 30), ("BARBOACH", 26, 28), ("MARILL", 25, 28), ("WHISCASH", 28, 30)]
PL_WATER = [("CHINCHOU", 27, 31), ("MARILL", 27, 31), ("WOOPER", 27, 31), ("CHINCHOU", 29, 32), ("LANTURN", 30, 33)]
PL_FISH = [("MAGIKARP", 5, 10), ("CHINCHOU", 5, 10), ("CHINCHOU", 15, 20), ("MAGIKARP", 15, 20), ("BARBOACH", 15, 20),
           ("CHINCHOU", 27, 31), ("LANTURN", 29, 33), ("CHINCHOU", 28, 31), ("BARBOACH", 27, 30), ("LANTURN", 31, 33)]
TD_WATER = [("TENTACOOL", 47, 51), ("HORSEA", 47, 51), ("WAILMER", 47, 51), ("CLAUNCHER", 48, 51), ("DHELMISE", 49, 52)]
TD_FISH = [("MAGIKARP", 10, 15), ("HORSEA", 10, 15), ("HORSEA", 25, 30), ("CLAUNCHER", 25, 30), ("TENTACOOL", 25, 30),
           ("HORSEA", 47, 51), ("CLAUNCHER", 47, 51), ("WAILMER", 47, 51), ("SEADRA", 49, 52), ("DHELMISE", 49, 52)]


def main():
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    enc = wj["wild_encounter_groups"][0]["encounters"]
    def get(mid, label, after):
        for e in enc:
            if e.get("map") == mid:
                return e
        e = OD([("map", mid), ("base_label", label)])
        idx = next(i for i, x in enumerate(enc) if x.get("map") == after) + 1
        enc.insert(idx, e)
        return e
    get("MAP_PALM_ROUTE04", "gPalmRoute04", None)["land_mons"]["mons"] = mons(R4_LAND)
    r5 = get("MAP_PALM_ROUTE05", "gPalmRoute05", None)
    r5["water_mons"] = OD([("encounter_rate", 4), ("mons", mons(R5_WATER))])
    r5["fishing_mons"] = OD([("encounter_rate", 30), ("mons", mons(R5_FISH))])
    pl = get("MAP_PALM_PILLARTON", "gPalmPillarton", "MAP_PALM_ROUTE05")
    pl["water_mons"] = OD([("encounter_rate", 4), ("mons", mons(PL_WATER))])
    pl["fishing_mons"] = OD([("encounter_rate", 30), ("mons", mons(PL_FISH))])
    td = get("MAP_PALM_TIDEMOUTH", "gPalmTidemouth", "MAP_PALM_ROUTE10")
    td["water_mons"] = OD([("encounter_rate", 4), ("mons", mons(TD_WATER))])
    td["fishing_mons"] = OD([("encounter_rate", 30), ("mons", mons(TD_FISH))])
    jsave(wp, wj)
    print("Pokedex: lacunas de encontro aplicadas (Route 4, Route 5, Pillarton, Tidemouth)")


if __name__ == "__main__":
    main()
