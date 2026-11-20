#!/usr/bin/env python3
"""Capitulo 12 (parte 1): Storm Mountain — a trilha (encosta inferior com o Steven, desfiladeiro com o Leon).

- a escadaria da Passway (aberta pela convocacao do Doge, FLAG_HT_POSTGAME_DATA) continua para o norte numa
  conexao continua com MAP_PALM_STORM_TRAIL (trilha x = Passway x + 2);
- tempestade (chuva com trovoes), encontros do pos-Liga (Bagon, Gible raro, Druddigon, Snorunt, Scyther raro);
- Steven (com o Metagross) na encosta inferior e Leon (com o Charizard) no desfiladeiro: cenas unicas com as
  falas do roteiro (sec. 17), sem batalha obrigatoria (os dois tentaram enfrentar o antigo Campeao e recuaram);
- MAPSEC_MT_CHIMNEY (no mapa da regiao, ao norte da Passway) passa a se chamar STORM MOUNTAIN.
O posto da Joy, a Cynthia e o cume entram nas partes 2 e 3. Rodar depois de install_cap11c.py.
"""
import collections, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import storm_trail as ST
from canvas import ROOT
from install_cap4 import jload, jsave, obj, coord, map_json, register, walkable

OD = collections.OrderedDict
FLAGS = [("FLAG_UNUSED_0x0E9", "0xE9", "FLAG_HT_STEVEN_MET", "Steven conversou com o jogador na encosta da Storm Mountain"),
         ("FLAG_UNUSED_0x1AA", "0x1AA", "FLAG_HT_LEON_MET", "Leon conversou com o jogador no desfiladeiro")]
ITEMS = [(30, 47, "ITEM_MAX_ELIXIR", "FLAG_ITEM_ROUTE_114_RARE_CANDY"),
         (36, 28, "ITEM_FULL_RESTORE", "FLAG_ITEM_ROUTE_133_STAR_PIECE"),
         (14, 3, "ITEM_MAX_REVIVE", "FLAG_ITEM_ROUTE_121_REVIVE")]
WILD = [("SPECIES_BAGON", 68, 70), ("SPECIES_DRUDDIGON", 68, 70), ("SPECIES_SNORUNT", 68, 70), ("SPECIES_BAGON", 69, 71),
        ("SPECIES_DRUDDIGON", 69, 71), ("SPECIES_SNORUNT", 69, 71), ("SPECIES_SHELGON", 70, 72), ("SPECIES_SCYTHER", 70, 72),
        ("SPECIES_DRUDDIGON", 71, 73), ("SPECIES_SNORUNT", 71, 73), ("SPECIES_GIBLE", 70, 72), ("SPECIES_GIBLE", 72, 74)]


def main():
    # ---------------- flags novas (substituem flags sem uso)
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    for old, val, new, why in FLAGS:
        if new not in t:
            t, n = re.subn(r"#define %s\s+%s[^\n]*\n" % (old, val), f"#define {new:<36} {val} // {why}\n", t, count=1)
            assert n == 1, old
    open(fp, "w").write(t)

    # ---------------- nome no mapa da regiao
    rp = f"{ROOT}/src/data/region_map/region_map_sections.json"
    r = jload(rp)
    for s in r["map_sections"]:
        if s["id"] == "MAPSEC_MT_CHIMNEY":
            s["name"] = "STORM MOUNTAIN"
    jsave(rp, r)

    # ---------------- Passway: a escadaria continua para o norte
    pp = f"{ROOT}/data/maps/PalmPassway/map.json"
    pj = jload(pp)
    pj["connections"] = [cn for cn in pj["connections"] if cn["map"] != "MAP_PALM_STORM_TRAIL"] + \
                        [OD([("map", "MAP_PALM_STORM_TRAIL"), ("offset", -ST.OFFSET_PASSWAY), ("direction", "up")])]
    jsave(pp, pj)

    # ---------------- a trilha
    c = ST.compose()
    bl = ST.flatten(c.build())
    register("PalmStormTrail", "LAYOUT_PALM_STORM_TRAIL", c, bl)
    j = map_json("MAP_PALM_STORM_TRAIL", "PalmStormTrail", "LAYOUT_PALM_STORM_TRAIL", "MUS_ROUTE120", "MAPSEC_MT_CHIMNEY",
                 "MAP_TYPE_ROUTE", [OD([("map", "MAP_PALM_PASSWAY"), ("offset", ST.OFFSET_PASSWAY), ("direction", "down")])])
    j["weather"] = "WEATHER_RAIN_THUNDERSTORM"
    sx, sy = ST.STEVEN
    lx, ly = ST.LEON
    for (x, y) in [(sx, sy), (sx + 1, sy), (lx + 1, ly - 1), (lx + 2, ly - 1)]:
        assert walkable(bl, c.w, x, y), (x, y)
    j["object_events"] = [
        obj("STEVEN", sx, sy, "MOVEMENT_TYPE_FACE_LEFT", "Palm220_Steven"),
        obj("OBJ_EVENT_GFX_SPECIES(METAGROSS)", sx + 1, sy, "MOVEMENT_TYPE_FACE_LEFT", "Palm220_Metagross"),
        obj("OBJ_EVENT_GFX_COOLTRAINER_M", lx + 1, ly - 1, "MOVEMENT_TYPE_FACE_DOWN", "Palm220_Leon"),
        obj("OBJ_EVENT_GFX_SPECIES(CHARIZARD)", lx + 2, ly - 1, "MOVEMENT_TYPE_FACE_DOWN", "Palm220_Charizard")]
    for (x, y, item, flag) in ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    # cenas unicas: ao passar pela altura de cada um
    j["coord_events"] = [coord(x, sy, "Palm220_StevenScene") for x in ST.SOUTH] + \
                        [coord(x, ly + 1, "Palm220_LeonScene") for x in range(ST.GORGE[0], ST.GORGE[1] + 1)]
    jsave(f"{ROOT}/data/maps/PalmStormTrail/map.json", j)
    sc = ["PalmStormTrail_MapScripts::\n\t.byte 0\n",
          "Palm220_StevenScene::\n\tgoto_if_set FLAG_HT_STEVEN_MET, Palm220_End\n\tlockall\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterRight\n\twaitmovement 0\n"
          "\tmsgbox Palm220_TextSteven, MSGBOX_DEFAULT\n\tsetflag FLAG_HT_STEVEN_MET\n\treleaseall\n\tend\n",
          "Palm220_LeonScene::\n\tgoto_if_set FLAG_HT_LEON_MET, Palm220_End\n\tlockall\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterUp\n\twaitmovement 0\n"
          "\tplaymoncry SPECIES_CHARIZARD, CRY_MODE_NORMAL\n\twaitmoncry\n"
          "\tmsgbox Palm220_TextLeon, MSGBOX_DEFAULT\n\tsetflag FLAG_HT_LEON_MET\n\treleaseall\n\tend\n",
          "Palm220_End::\n\tend\n",
          "Palm220_Steven::\n\tlock\n\tfaceplayer\n\tmsgbox Palm220_TextStevenAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm220_Leon::\n\tlock\n\tfaceplayer\n\tmsgbox Palm220_TextLeonAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm220_Metagross::\n\tlock\n\tplaymoncry SPECIES_METAGROSS, CRY_MODE_NORMAL\n\tmsgbox Palm220_TextMetagross, MSGBOX_DEFAULT\n"
          "\twaitmoncry\n\trelease\n\tend\n",
          "Palm220_Charizard::\n\tlock\n\tplaymoncry SPECIES_CHARIZARD, CRY_MODE_NORMAL\n\tmsgbox Palm220_TextCharizard, MSGBOX_DEFAULT\n"
          "\twaitmoncry\n\trelease\n\tend\n"]
    open(f"{ROOT}/data/maps/PalmStormTrail/scripts.inc", "w").write("\n".join(sc))

    # ---------------- encontros
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [x for x in grp["encounters"] if x.get("map") != "MAP_PALM_STORM_TRAIL"]
    entry = OD([("map", "MAP_PALM_STORM_TRAIL"), ("base_label", "gPalmStormTrail"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s_)])
                                                                    for (s_, a, b) in WILD])]))])
    idx = next(i for i, x in enumerate(grp["encounters"]) if x.get("map") == "MAP_PALM_ROUTE11") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch12.txt"], check=True)
    print("Cap. 12 (parte 1) instalado: Storm Mountain (trilha)", c.w, "x", c.h)


if __name__ == "__main__":
    main()
