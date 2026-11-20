#!/usr/bin/env python3
"""Rota opcional 15 (Coastal Grotto): mapa novo a oeste da Route 11, com conexao continua pela praia.

- Route 11: nada muda no mapa (a praia ja chega andavel na borda oeste, linhas 25-28); so a conexao para a
  esquerda (offset 0).
- Route 15: falesias com mata e, numa reentrancia da rocha, a gruta (recanto de areia com poca de mare);
  enseada de mar, dunas com mato alto; treinadores Oscar (Sailor), Pedro (Fisherman) e Nina (Beauty) em vagas de
  Hoenn sem uso; 3 itens (FLAG_HT_R15_ITEM_1..3 = 0x26D-0x26F); placa; Pokemon do canone Lv 50-54 (Cap. 11) — no
  mato das dunas e na pesca (o jogo nao entrega Surf).
Rodar depois de install_cap11.py; nao reroda nenhum instalador anterior.
"""
import collections, os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route15 as R15
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, map_json, register, walkable
from install_cap9b import new_map

OD = collections.OrderedDict
FLAGS = [("FLAG_UNUSED_0x26D", "0x26D", "FLAG_HT_R15_ITEM_1", "Route 15: Pearl String"),
         ("FLAG_UNUSED_0x26E", "0x26E", "FLAG_HT_R15_ITEM_2", "Route 15: Deep Sea Tooth"),
         ("FLAG_UNUSED_0x26F", "0x26F", "FLAG_HT_R15_ITEM_3", "Route 15: Shell Bell")]
ALIASES = [("TRAINER_PALM_ROUTE15_OSCAR", "TRAINER_LUIS"), ("TRAINER_PALM_ROUTE15_PEDRO", "TRAINER_DOMINIK"),
           ("TRAINER_PALM_ROUTE15_NINA", "TRAINER_MELISSA")]
TRAINERS = [(24, 25, "SAILOR", "DOWN", 2, "Palm253_RouteOSCAR", "TRAINER_PALM_ROUTE15_OSCAR"),
            (25, 11, "FISHERMAN", "RIGHT", 2, "Palm253_RoutePEDRO", "TRAINER_PALM_ROUTE15_PEDRO"),
            (29, 23, "BEAUTY", "LEFT", 1, "Palm253_RouteNINA", "TRAINER_PALM_ROUTE15_NINA")]
PARTIES = {
    "TRAINER_LUIS": ("OSCAR", "Sailor", "Sailor", "Male", "Male", [("Corsola", 52), ("Cloyster", 54)]),
    "TRAINER_DOMINIK": ("PEDRO", "Fisherman", "Fisherman", "Male", "Hiker", [("Clamperl", 52), ("Relicanth", 54)]),
    "TRAINER_MELISSA": ("NINA", "Beauty", "Beauty", "Female", "Female", [("Gorebyss", 53), ("Dhelmise", 54)]),
}
ITEMS = [(30, 8, "ITEM_PEARL_STRING", "FLAG_HT_R15_ITEM_1"), (4, 18, "ITEM_DEEP_SEA_TOOTH", "FLAG_HT_R15_ITEM_2"),
         (37, 23, "ITEM_SHELL_BELL", "FLAG_HT_R15_ITEM_3")]
SIGNS = [(37, 24, "Palm253_SignEast")]
LAND = [("SPECIES_CORSOLA", 50, 52), ("SPECIES_SHELLDER", 50, 52), ("SPECIES_DHELMISE", 50, 52), ("SPECIES_CLAMPERL", 50, 52),
        ("SPECIES_CORSOLA", 51, 53), ("SPECIES_SHELLDER", 51, 53), ("SPECIES_CORSOLA", 52, 54), ("SPECIES_SHELLDER", 52, 54),
        ("SPECIES_DHELMISE", 52, 54), ("SPECIES_CLAMPERL", 51, 53), ("SPECIES_DHELMISE", 53, 54), ("SPECIES_CORSOLA", 53, 54)]
WATER = [("SPECIES_SHELLDER", 50, 54), ("SPECIES_CLAMPERL", 50, 54), ("SPECIES_CORSOLA", 50, 54), ("SPECIES_DHELMISE", 52, 54),
         ("SPECIES_RELICANTH", 52, 54)]
FISH = [("SPECIES_SHELLDER", 20, 25), ("SPECIES_CLAMPERL", 20, 25), ("SPECIES_SHELLDER", 40, 45), ("SPECIES_CLAMPERL", 40, 45),
        ("SPECIES_CORSOLA", 40, 45), ("SPECIES_CORSOLA", 50, 54), ("SPECIES_DHELMISE", 50, 54), ("SPECIES_SHELLDER", 50, 54),
        ("SPECIES_CLAMPERL", 52, 54), ("SPECIES_RELICANTH", 52, 54)]
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
    if "TRAINER_PALM_ROUTE15_OSCAR" not in t:
        anchor = "// Pillarton: admin Lela"
        assert anchor in t
        block = "// Route 15 (Coastal Grotto, opcional)\n" + "".join(f"#define {a:<27} {b}\n" for a, b in ALIASES)
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

    # ---------------- Route 11: so a conexao (a praia ja chega andavel na borda oeste)
    import json
    lay = {l["id"]: l for l in jload(f"{ROOT}/data/layouts/layouts.json")["layouts"] if "id" in l}["LAYOUT_PALM_ROUTE11"]
    w11, h11 = lay["width"], lay["height"]
    bl5 = struct.unpack(f"<{w11 * h11}H", open(f"{ROOT}/{lay['blockdata_filepath']}", "rb").read())
    p5 = f"{ROOT}/data/maps/PalmRoute11/map.json"
    j5 = jload(p5)
    j5["connections"] = [cn for cn in j5["connections"] if cn["map"] != "MAP_PALM_ROUTE15"] + \
                        [OD([("map", "MAP_PALM_ROUTE15"), ("offset", R15.OFFSET_ROUTE11), ("direction", "left")])]
    jsave(p5, j5)

    # ---------------- Route 15
    new_map("PalmRoute15")
    c = R15.compose()
    for (x, y, _) in SIGNS:
        c.put(x, y, 3, collision=1)
    bl = R15.flatten(c.build())
    register("PalmRoute15", "LAYOUT_PALM_ROUTE15", c, bl)
    for y in range(R15.EAST_ROWS[0], R15.EAST_ROWS[1] + 1):   # a praia chega andavel nas duas bordas
        assert walkable(bl, c.w, c.w - 1, y) and walkable(bl5, w11, 0, y + R15.OFFSET_ROUTE11), y
    j = map_json("MAP_PALM_ROUTE15", "PalmRoute15", "LAYOUT_PALM_ROUTE15", "MUS_ROUTE110", "MAPSEC_ROUTE_115", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_ROUTE11"), ("offset", -R15.OFFSET_ROUTE11), ("direction", "right")])])
    for (x, y, gfx, d, sight, script, _) in TRAINERS:
        assert walkable(bl, c.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute15/map.json", j)
    sc = ["PalmRoute15_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in TRAINERS:
        k = script.replace("Palm253_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm253_Text{k}Intro, Palm253_Text{k}Loss\n"
                  f"\tmsgbox Palm253_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s) in SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute15/scripts.inc", "w").write("\n".join(sc))

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE15"]
    entry = OD([("map", "MAP_PALM_ROUTE15"), ("base_label", "gPalmRoute15"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", mons(LAND))])),
                ("water_mons", OD([("encounter_rate", 4), ("mons", mons(WATER))])),
                ("fishing_mons", OD([("encounter_rate", 30), ("mons", mons(FISH))]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE11") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/route15.txt"], check=True)
    print("Route 15 instalada:", c.w, "x", c.h)


if __name__ == "__main__":
    main()
