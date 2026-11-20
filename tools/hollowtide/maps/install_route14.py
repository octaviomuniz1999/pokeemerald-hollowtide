#!/usr/bin/env python3
"""Rota opcional 14 (Atlas Lookout): mapa novo a oeste da Passway Village, com conexao continua.

- Passway: so o map.bin muda (mesmo tamanho) — a rua principal segue ate a borda oeste (linhas 18-19);
  conexao para a esquerda (offset 0). Os eventos da Passway nao mudam.
- Route 14: estrada pela encosta, patamar alto com escada e o mirante (pedra de marco e placa com a historia do
  guardiao fiel), mato alto e um desvio ao sul; treinadores Beto (Pkmn Ranger), Clara (Pkmn Breeder) e Otto
  (Hiker) em vagas de Hoenn sem uso; 3 itens (FLAG_HT_R14_ITEM_1..3 = 0x26A-0x26C); 2 placas; Pokemon do
  canone (Lv 41-45, nivel do Cap. 8).
Rodar depois de install_cap9.py; nao reroda nenhum instalador anterior.
"""
import collections, os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import passway as PW, route14 as R14
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, map_json, register, walkable
from install_cap9b import new_map
from install_cap8 import PW_SIGNS

OD = collections.OrderedDict
FLAGS = [("FLAG_UNUSED_0x26A", "0x26A", "FLAG_HT_R14_ITEM_1", "Route 14: Scope Lens"),
         ("FLAG_UNUSED_0x26B", "0x26B", "FLAG_HT_R14_ITEM_2", "Route 14: Razor Claw"),
         ("FLAG_UNUSED_0x26C", "0x26C", "FLAG_HT_R14_ITEM_3", "Route 14: HP Up")]
ALIASES = [("TRAINER_PALM_ROUTE14_BETO", "TRAINER_SEBASTIAN"), ("TRAINER_PALM_ROUTE14_CLARA", "TRAINER_PAT"),
           ("TRAINER_PALM_ROUTE14_OTTO", "TRAINER_JARED")]
TRAINERS = [(20, 17, "MAN_5", "DOWN", 1, "Palm252_RouteBETO", "TRAINER_PALM_ROUTE14_BETO"),
            (30, 20, "WOMAN_2", "UP", 1, "Palm252_RouteCLARA", "TRAINER_PALM_ROUTE14_CLARA"),
            (12, 9, "HIKER", "UP", 1, "Palm252_RouteOTTO", "TRAINER_PALM_ROUTE14_OTTO")]
PARTIES = {
    "TRAINER_SEBASTIAN": ("BETO", "Pkmn Ranger", "Pokemon Ranger M", "Male", "Cool", [("Herdier", 42), ("Lycanroc", 44)]),
    "TRAINER_PAT": ("CLARA", "Pkmn Breeder", "Pokemon Breeder F", "Female", "Female", [("Lillipup", 41), ("Houndour", 41), ("Herdier", 43)]),
    "TRAINER_JARED": ("OTTO", "Hiker", "Hiker", "Male", "Hiker", [("Rockruff", 42), ("Houndoom", 44)]),
}
ITEMS = [(9, 6, "ITEM_SCOPE_LENS", "FLAG_HT_R14_ITEM_1"), (17, 25, "ITEM_RAZOR_CLAW", "FLAG_HT_R14_ITEM_2"),
         (5, 18, "ITEM_HP_UP", "FLAG_HT_R14_ITEM_3")]
SIGNS = [(37, 17, "Palm252_SignEast"), (10, 6, "Palm252_SignLookout")]
LAND = [("SPECIES_LILLIPUP", 41, 43), ("SPECIES_HOUNDOUR", 41, 43), ("SPECIES_ROCKRUFF", 41, 43), ("SPECIES_HERDIER", 42, 44),
        ("SPECIES_LILLIPUP", 42, 44), ("SPECIES_HOUNDOUR", 42, 44), ("SPECIES_ROCKRUFF", 42, 44), ("SPECIES_HERDIER", 43, 45),
        ("SPECIES_HOUNDOUR", 43, 45), ("SPECIES_STOUTLAND", 44, 45), ("SPECIES_ABSOL", 42, 44), ("SPECIES_ABSOL", 43, 45)]
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
    if "TRAINER_PALM_ROUTE14_BETO" not in t:
        anchor = "// Pillarton: admin Lela"
        assert anchor in t
        block = "// Route 14 (Atlas Lookout, opcional)\n" + "".join(f"#define {a:<27} {b}\n" for a, b in ALIASES)
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

    # ---------------- Passway: rua principal ate a borda oeste (so o map.bin, mesmo tamanho) + conexao
    c5 = PW.compose()
    for (x, y, _) in PW_SIGNS:
        if (x, y) != (14, 8):                           # o mural e a propria parede de rocha (como no install_cap8)
            c5.put(x, y, 3, collision=1)
    bl5 = PW.flatten(c5.build())
    lp = f"{ROOT}/data/layouts/PalmPassway/map.bin"
    old = open(lp, "rb").read()
    new = struct.pack(f"<{len(bl5)}H", *bl5)
    assert len(old) == len(new)
    open(lp, "wb").write(new)
    p5 = f"{ROOT}/data/maps/PalmPassway/map.json"
    j5 = jload(p5)
    j5["connections"] = [cn for cn in j5["connections"] if cn["map"] != "MAP_PALM_ROUTE14"] + \
                        [OD([("map", "MAP_PALM_ROUTE14"), ("offset", R14.OFFSET_PASSWAY), ("direction", "left")])]
    jsave(p5, j5)

    # ---------------- Route 14
    new_map("PalmRoute14")
    c = R14.compose()
    for (x, y, _) in SIGNS:
        c.put(x, y, 3, collision=1)
    bl = R14.flatten(c.build())
    register("PalmRoute14", "LAYOUT_PALM_ROUTE14", c, bl)
    for y in R14.EAST:                                  # a estrada chega andavel nas duas bordas
        assert walkable(bl, c.w, c.w - 1, y) and walkable(bl5, c5.w, 0, y + R14.OFFSET_PASSWAY), y
    j = map_json("MAP_PALM_ROUTE14", "PalmRoute14", "LAYOUT_PALM_ROUTE14", "MUS_ROUTE111", "MAPSEC_ROUTE_114", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_PASSWAY"), ("offset", -R14.OFFSET_PASSWAY), ("direction", "right")])])
    for (x, y, gfx, d, sight, script, _) in TRAINERS:
        assert walkable(bl, c.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute14/map.json", j)
    sc = ["PalmRoute14_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in TRAINERS:
        k = script.replace("Palm252_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm252_Text{k}Intro, Palm252_Text{k}Loss\n"
                  f"\tmsgbox Palm252_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s) in SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute14/scripts.inc", "w").write("\n".join(sc))

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE14"]
    entry = OD([("map", "MAP_PALM_ROUTE14"), ("base_label", "gPalmRoute14"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", mons(LAND))]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE08") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/route14.txt"], check=True)
    print("Route 14 instalada:", c.w, "x", c.h)


if __name__ == "__main__":
    main()
