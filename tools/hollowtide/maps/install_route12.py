#!/usr/bin/env python3
"""Rota opcional 12 (River Bend): mapa novo a oeste da Route 5, com conexao continua.

- Route 5: so o map.bin muda (mesmo tamanho) — tabuado sobre o braco oeste e trilha ate a borda oeste
  (linhas 29-30); conexao para a esquerda (offset 15). Os eventos da Route 5 nao mudam.
- Route 12: rio em S com tabuado, prados, ponta de areia, prainha da curva e um remanso de pesca;
  treinadores Artur (pescador), Bia (piquenique) e Nico (campista) em vagas de treinadores de Hoenn sem uso;
  3 itens (FLAG_HT_R12_ITEM_1..3 = 0x264-0x266, sem uso no Emerald); placa; Pokemon do canone em terra,
  surf e pesca (Lv 26-29, nivel do Cap. 5).
Rodar depois de install_pillarton.py (que reinstala a Route 5); nao reroda nenhum instalador anterior.
"""
import collections, os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route5 as R5, route12 as R12
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, map_json, register, walkable
from install_cap9b import new_map

OD = collections.OrderedDict
FLAGS = [("FLAG_UNUSED_0x264", "0x264", "FLAG_HT_R12_ITEM_1", "Route 12: Mystic Water"),
         ("FLAG_UNUSED_0x265", "0x265", "FLAG_HT_R12_ITEM_2", "Route 12: Water Stone"),
         ("FLAG_UNUSED_0x266", "0x266", "FLAG_HT_R12_ITEM_3", "Route 12: Big Pearl")]
ALIASES = [("TRAINER_PALM_ROUTE12_ARTUR", "TRAINER_BARNY"), ("TRAINER_PALM_ROUTE12_BIA", "TRAINER_HAILEY"),
           ("TRAINER_PALM_ROUTE12_NICO", "TRAINER_CLARK")]
TRAINERS = [(20, 12, "FISHERMAN", "LEFT", 2, "Palm250_RouteARTUR", "TRAINER_PALM_ROUTE12_ARTUR"),
            (4, 18, "PICNICKER", "RIGHT", 1, "Palm250_RouteBIA", "TRAINER_PALM_ROUTE12_BIA"),
            (29, 20, "CAMPER", "RIGHT", 1, "Palm250_RouteNICO", "TRAINER_PALM_ROUTE12_NICO")]
PARTIES = {
    "TRAINER_BARNY": ("ARTUR", "Fisherman", "Fisherman", "Male", "Hiker", [("Basculin", 28), ("Corphish", 29)]),
    "TRAINER_HAILEY": ("BIA", "Picnicker", "Picnicker", "Female", "Girl", [("Marill", 28), ("Ducklett", 29)]),
    "TRAINER_CLARK": ("NICO", "Camper", "Camper", "Male", "Male", [("Tympole", 27), ("Ducklett", 27), ("Palpitoad", 29)]),
}
ITEMS = [(14, 6, "ITEM_MYSTIC_WATER", "FLAG_HT_R12_ITEM_1"), (19, 23, "ITEM_WATER_STONE", "FLAG_HT_R12_ITEM_2"),
         (33, 25, "ITEM_BIG_PEARL", "FLAG_HT_R12_ITEM_3")]
SIGNS = [(37, 13, "Palm250_SignEast")]
LAND = [("SPECIES_TYMPOLE", 26, 28), ("SPECIES_DUCKLETT", 26, 28), ("SPECIES_TYMPOLE", 27, 29), ("SPECIES_DUCKLETT", 27, 29),
        ("SPECIES_CORPHISH", 26, 28), ("SPECIES_CORPHISH", 27, 29), ("SPECIES_TYMPOLE", 28, 29), ("SPECIES_DUCKLETT", 28, 29),
        ("SPECIES_CORPHISH", 28, 29), ("SPECIES_TYMPOLE", 28, 29), ("SPECIES_FROAKIE", 26, 28), ("SPECIES_FROAKIE", 27, 29)]
WATER = [("SPECIES_BASCULIN", 25, 30), ("SPECIES_DUCKLETT", 25, 30), ("SPECIES_CORPHISH", 25, 30), ("SPECIES_BASCULIN", 28, 32),
         ("SPECIES_BASCULIN", 30, 33)]
FISH = [("SPECIES_BASCULIN", 10, 15), ("SPECIES_CORPHISH", 10, 15), ("SPECIES_BASCULIN", 25, 30), ("SPECIES_CORPHISH", 25, 30),
        ("SPECIES_BASCULIN", 25, 30), ("SPECIES_BASCULIN", 30, 35), ("SPECIES_CORPHISH", 30, 35), ("SPECIES_BASCULIN", 30, 35),
        ("SPECIES_CORPHISH", 32, 36), ("SPECIES_BASCULIN", 35, 38)]
IV = "IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe"


def mons(lst):
    return [OD([("min_level", a), ("max_level", b), ("species", s)]) for (s, a, b) in lst]


def main():
    # ---------------- flags e apelidos de treinadores
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    for old, val, new, why in FLAGS:
        if new not in t:
            t, n = re.subn(r"#define %s\s+%s[^\n]*\n" % (old, val), f"#define {new:<36} {val} // {why}\n", t, count=1)
            assert n == 1, old
    open(fp, "w").write(t)
    op = f"{ROOT}/include/constants/opponents.h"
    t = open(op).read()
    if "TRAINER_PALM_ROUTE12_ARTUR" not in t:
        anchor = "// Pillarton: admin Lela"
        assert anchor in t
        block = "// Route 12 (River Bend, opcional)\n" + "".join(f"#define {a:<27} {b}\n" for a, b in ALIASES)
        t = t.replace(anchor, block + anchor, 1)
        open(op, "w").write(t)
    pp = f"{ROOT}/src/data/trainers.party"
    t = open(pp).read()
    for tid, (name, cls, pic, gender, music, party) in PARTIES.items():
        body = (f"=== {tid} ===\nName: {name}\nClass: {cls}\nPic: {pic}\nGender: {gender}\nMusic: {music}\n"
                f"Double Battle: No\nAI: Check Bad Move\n\n" + "".join(f"{s}\nLevel: {lv}\n{IV}\n\n" for s, lv in party))
        t, n = re.subn(r"=== %s ===\n.*?(?=\n=== )" % tid, body.rstrip("\n") + "\n", t, count=1, flags=re.S)
        assert n == 1, tid
    open(pp, "w").write(t)

    # ---------------- Route 5: tabuado oeste (so o map.bin, mesmo tamanho) + conexao
    c5 = R5.compose(north_open=True)
    for (x, y) in [(19, 48), (18, 8)]:                  # placas do install_cap5
        c5.put(x, y, 3, collision=1)
    bl5 = c5.build()
    lp = f"{ROOT}/data/layouts/PalmRoute05/map.bin"
    old = open(lp, "rb").read()
    new = struct.pack(f"<{len(bl5)}H", *bl5)
    assert len(old) == len(new)
    open(lp, "wb").write(new)
    p5 = f"{ROOT}/data/maps/PalmRoute05/map.json"
    j5 = jload(p5)
    j5["connections"] = [cn for cn in j5["connections"] if cn["map"] != "MAP_PALM_ROUTE12"] + \
                        [OD([("map", "MAP_PALM_ROUTE12"), ("offset", R12.OFFSET_ROUTE05), ("direction", "left")])]
    jsave(p5, j5)

    # ---------------- Route 12
    new_map("PalmRoute12")
    c = R12.compose()
    for (x, y, _) in SIGNS:
        c.put(x, y, 3, collision=1)
    bl = c.build()
    register("PalmRoute12", "LAYOUT_PALM_ROUTE12", c, bl)
    for y in R12.EAST:                                  # a trilha chega andavel nas duas bordas
        assert walkable(bl, c.w, c.w - 1, y) and walkable(bl5, c5.w, 0, y + R12.OFFSET_ROUTE05), y
    j = map_json("MAP_PALM_ROUTE12", "PalmRoute12", "LAYOUT_PALM_ROUTE12", "MUS_ROUTE104", "MAPSEC_ROUTE_112", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_ROUTE05"), ("offset", -R12.OFFSET_ROUTE05), ("direction", "right")])])
    for (x, y, gfx, d, sight, script, _) in TRAINERS:
        assert walkable(bl, c.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute12/map.json", j)
    sc = ["PalmRoute12_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in TRAINERS:
        k = script.replace("Palm250_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm250_Text{k}Intro, Palm250_Text{k}Loss\n"
                  f"\tmsgbox Palm250_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s) in SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute12/scripts.inc", "w").write("\n".join(sc))

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE12"]
    entry = OD([("map", "MAP_PALM_ROUTE12"), ("base_label", "gPalmRoute12"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", mons(LAND))])),
                ("water_mons", OD([("encounter_rate", 4), ("mons", mons(WATER))])),
                ("fishing_mons", OD([("encounter_rate", 30), ("mons", mons(FISH))]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE05") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/route12.txt"], check=True)
    print("Route 12 instalada:", c.w, "x", c.h)


if __name__ == "__main__":
    main()
