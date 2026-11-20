#!/usr/bin/env python3
"""Rota opcional 13 (Mirror Grove): mapa novo a leste da Route 7, com conexao continua.

- Route 7: so o map.bin muda (mesmo tamanho) — a trilha do Circulo da Lua segue ate a borda leste (linhas
  24-25); conexao para a direita (offset 8). Os eventos da Route 7 nao mudam.
- Route 13: bosque fechado com trilha em anel, lagoas paradas, clareira com pedras em roda e um recanto;
  treinadores Luna (Hex Maniac), Kaio (Psychic) e Raul (Ruin Maniac) em vagas de Hoenn sem uso; 3 itens
  (FLAG_HT_R13_ITEM_1..3 = 0x267-0x269); placa; Pokemon do canone (Lv 36-40, nivel do Cap. 7).
Rodar depois de install_cap7.py; nao reroda nenhum instalador anterior.
"""
import collections, os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route7 as R7, route13 as R13
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, map_json, register, walkable
from install_cap9b import new_map
from install_cap7 import R7_SIGNS

OD = collections.OrderedDict
FLAGS = [("FLAG_UNUSED_0x267", "0x267", "FLAG_HT_R13_ITEM_1", "Route 13: Spell Tag"),
         ("FLAG_UNUSED_0x268", "0x268", "FLAG_HT_R13_ITEM_2", "Route 13: Dusk Stone"),
         ("FLAG_UNUSED_0x269", "0x269", "FLAG_HT_R13_ITEM_3", "Route 13: Big Mushroom")]
ALIASES = [("TRAINER_PALM_ROUTE13_LUNA", "TRAINER_NED"), ("TRAINER_PALM_ROUTE13_KAIO", "TRAINER_DEAN"),
           ("TRAINER_PALM_ROUTE13_RAUL", "TRAINER_EVERETT")]
TRAINERS = [(26, 9, "HEX_MANIAC", "UP", 1, "Palm251_RouteLUNA", "TRAINER_PALM_ROUTE13_LUNA"),
            (10, 18, "PSYCHIC_M", "LEFT", 1, "Palm251_RouteKAIO", "TRAINER_PALM_ROUTE13_KAIO"),
            (25, 22, "HIKER", "DOWN", 1, "Palm251_RouteRAUL", "TRAINER_PALM_ROUTE13_RAUL")]
PARTIES = {
    "TRAINER_NED": ("LUNA", "Hex Maniac", "Hex Maniac", "Female", "Suspicious", [("Shuppet", 37), ("Lampent", 39)]),
    "TRAINER_DEAN": ("KAIO", "Psychic", "Psychic M", "Male", "Intense", [("Mime Jr.", 37), ("Mr. Mime", 39)]),
    "TRAINER_EVERETT": ("RAUL", "Ruin Maniac", "Ruin Maniac", "Male", "Hiker", [("Foongus", 37), ("Litwick", 37), ("Amoonguss", 39)]),
}
ITEMS = [(19, 14, "ITEM_SPELL_TAG", "FLAG_HT_R13_ITEM_1"), (36, 15, "ITEM_DUSK_STONE", "FLAG_HT_R13_ITEM_2"),
         (7, 23, "ITEM_BIG_MUSHROOM", "FLAG_HT_R13_ITEM_3")]
SIGNS = [(2, 15, "Palm251_SignWest")]
LAND = [("SPECIES_SHUPPET", 36, 38), ("SPECIES_LITWICK", 36, 38), ("SPECIES_FOONGUS", 36, 38), ("SPECIES_MIME_JR", 36, 38),
        ("SPECIES_SHUPPET", 37, 39), ("SPECIES_LITWICK", 37, 39), ("SPECIES_FOONGUS", 37, 39), ("SPECIES_MIME_JR", 37, 39),
        ("SPECIES_SHUPPET", 38, 40), ("SPECIES_FOONGUS", 38, 40), ("SPECIES_ZORUA_HISUI", 36, 38), ("SPECIES_ZORUA_HISUI", 37, 39)]
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
    if "TRAINER_PALM_ROUTE13_LUNA" not in t:
        anchor = "// Pillarton: admin Lela"
        assert anchor in t
        block = "// Route 13 (Mirror Grove, opcional)\n" + "".join(f"#define {a:<27} {b}\n" for a, b in ALIASES)
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

    # ---------------- Route 7: trilha ate a borda leste (so o map.bin, mesmo tamanho) + conexao
    c5 = R7.compose()
    for (x, y, _) in R7_SIGNS:
        c5.put(x, y, 3, collision=1)
    bl5 = R7.flatten(c5.build())
    lp = f"{ROOT}/data/layouts/PalmRoute07/map.bin"
    old = open(lp, "rb").read()
    new = struct.pack(f"<{len(bl5)}H", *bl5)
    assert len(old) == len(new)
    open(lp, "wb").write(new)
    p5 = f"{ROOT}/data/maps/PalmRoute07/map.json"
    j5 = jload(p5)
    j5["connections"] = [cn for cn in j5["connections"] if cn["map"] != "MAP_PALM_ROUTE13"] + \
                        [OD([("map", "MAP_PALM_ROUTE13"), ("offset", R13.OFFSET_ROUTE07), ("direction", "right")])]
    jsave(p5, j5)

    # ---------------- Route 13
    new_map("PalmRoute13")
    c = R13.compose()
    for (x, y, _) in SIGNS:
        c.put(x, y, 3, collision=1)
    bl = c.build()
    register("PalmRoute13", "LAYOUT_PALM_ROUTE13", c, bl)
    for y in R13.WEST:                                  # a trilha chega andavel nas duas bordas
        assert walkable(bl, c.w, 0, y) and walkable(bl5, c5.w, c5.w - 1, y + R13.OFFSET_ROUTE07), y
    j = map_json("MAP_PALM_ROUTE13", "PalmRoute13", "LAYOUT_PALM_ROUTE13", "MUS_ROUTE120", "MAPSEC_ROUTE_113", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_ROUTE07"), ("offset", -R13.OFFSET_ROUTE07), ("direction", "left")])])
    for (x, y, gfx, d, sight, script, _) in TRAINERS:
        assert walkable(bl, c.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute13/map.json", j)
    sc = ["PalmRoute13_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in TRAINERS:
        k = script.replace("Palm251_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm251_Text{k}Intro, Palm251_Text{k}Loss\n"
                  f"\tmsgbox Palm251_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s) in SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute13/scripts.inc", "w").write("\n".join(sc))

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE13"]
    entry = OD([("map", "MAP_PALM_ROUTE13"), ("base_label", "gPalmRoute13"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", mons(LAND))]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE07") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/route13.txt"], check=True)
    print("Route 13 instalada:", c.w, "x", c.h)


if __name__ == "__main__":
    main()
