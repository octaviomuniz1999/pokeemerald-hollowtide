#!/usr/bin/env python3
"""Pos-Liga (decisoes do diretor, 20/11): area de treino com selvagens 80+ e a KEY STONE entregue pelo Doge.

- a caverna do pico (MAP_PALM_STORM_HOLLOW, layout da caverna do Steven nas Meteor Falls — uma entrada so) abre na
  parede sul do patamar do cume (7,13); fica fechada pelo vento ate o Tavinho ser vencido (FLAG_HT_SUMMIT_DONE);
- selvagens Lv 80–86: as formas evoluidas das especies da montanha (Shelgon/Salamence, Gabite/Garchomp, Druddigon,
  Glalie/Froslass, Scyther); um montanhista na entrada; 3 itens (Salamencite, Garchompite, Full Restore);
- a Key Stone (ITEM_MEGA_RING) vem do Doge no fim do epilogo (install_cap12c; FLAG_HT_RECEIVED_KEY_STONE).
Rodar depois de install_cap12c.py (e antes de install_doors.py, o ultimo).
"""
import collections, os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import storm_summit as SM
from canvas import ROOT
from install_cap4 import jload, jsave, obj, coord, map_json
from install_cap9b import new_map

OD = collections.OrderedDict
FLAGS = [("FLAG_UNUSED_0x1E0", "0x1E0", "FLAG_HT_RECEIVED_KEY_STONE", "Doge entregou a Key Stone (Mega Ring) no fim do epilogo"),
         ("FLAG_UNUSED_0x1E1", "0x1E1", "FLAG_HT_HOLLOW_ITEM_1", "caverna do pico: Salamencite"),
         ("FLAG_UNUSED_0x1E2", "0x1E2", "FLAG_HT_HOLLOW_ITEM_2", "caverna do pico: Garchompite"),
         ("FLAG_UNUSED_0x1E3", "0x1E3", "FLAG_HT_HOLLOW_ITEM_3", "caverna do pico: Full Restore")]
ITEMS = [(19, 3, "ITEM_SALAMENCITE", "FLAG_HT_HOLLOW_ITEM_1"), (4, 17, "ITEM_GARCHOMPITE", "FLAG_HT_HOLLOW_ITEM_2"),
         (23, 15, "ITEM_FULL_RESTORE", "FLAG_HT_HOLLOW_ITEM_3")]
WILD = [("SPECIES_SHELGON", 80, 82), ("SPECIES_GABITE", 80, 82), ("SPECIES_DRUDDIGON", 80, 83), ("SPECIES_GLALIE", 80, 83),
        ("SPECIES_SHELGON", 81, 83), ("SPECIES_GABITE", 81, 83), ("SPECIES_FROSLASS", 81, 84), ("SPECIES_SCYTHER", 81, 84),
        ("SPECIES_DRUDDIGON", 82, 85), ("SPECIES_GLALIE", 82, 85), ("SPECIES_SALAMENCE", 83, 86), ("SPECIES_GARCHOMP", 83, 86)]


def main():
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    for old, val, new, why in FLAGS:
        if new not in t:
            t, n = re.subn(r"#define %s\s+%s[^\n]*\n" % (old, val), f"#define {new:<36} {val} // {why}\n", t, count=1)
            assert n == 1, old
    open(fp, "w").write(t)

    # ---------------- boca da caverna no cume: so o map.bin (o resto do cume vem do install_cap12c)
    c = SM.compose()
    bl = SM.flatten(c.build())
    lp = f"{ROOT}/data/layouts/PalmStormSummit/map.bin"
    old = open(lp, "rb").read()
    new = struct.pack(f"<{len(bl)}H", *bl)
    assert len(old) == len(new)
    open(lp, "wb").write(new)
    mx, my = SM.HOLLOW_MOUTH
    sp = f"{ROOT}/data/maps/PalmStormSummit/map.json"
    s = jload(sp)
    s["warp_events"] = [w for w in s["warp_events"] if w["dest_map"] != "MAP_PALM_STORM_HOLLOW"]
    widx = len(s["warp_events"])
    s["warp_events"].append(OD([("x", mx), ("y", my), ("elevation", 0), ("dest_map", "MAP_PALM_STORM_HOLLOW"), ("dest_warp_id", "0")]))
    s["coord_events"] = [e for e in s["coord_events"] if e["script"] != "Palm242_HollowWind"] + [coord(mx, my + 1, "Palm242_HollowWind")]
    jsave(sp, s)
    ss = f"{ROOT}/data/maps/PalmStormSummit/scripts.inc"
    st = open(ss).read()
    if "Palm242_HollowWind::" not in st:
        st += """
Palm242_HollowWind::
	goto_if_set FLAG_HT_SUMMIT_DONE, Palm240_End
	lockall
	msgbox Palm242_TextWind, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, Palm242_StepBack
	waitmovement 0
	releaseall
	end

Palm242_StepBack:
	walk_down
	step_end

Palm242_TextWind:
	.string "x$"
"""
        open(ss, "w").write(st)

    # ---------------- a caverna
    new_map("PalmStormHollow")
    j = map_json("MAP_PALM_STORM_HOLLOW", "PalmStormHollow", "LAYOUT_METEOR_FALLS_STEVENS_CAVE", "MUS_CAVE_OF_ORIGIN",
                 "MAPSEC_MT_CHIMNEY", "MAP_TYPE_UNDERGROUND", [])
    j["allow_cycling"] = False
    j["warp_events"] = [OD([("x", 10), ("y", 29), ("elevation", 3), ("dest_map", "MAP_PALM_STORM_SUMMIT"), ("dest_warp_id", str(widx))])]
    j["object_events"] = [obj("HIKER", 11, 27, "MOVEMENT_TYPE_FACE_DOWN", "Palm243_Hiker")]
    for (x, y, item, flag) in ITEMS:
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    jsave(f"{ROOT}/data/maps/PalmStormHollow/map.json", j)
    open(f"{ROOT}/data/maps/PalmStormHollow/scripts.inc", "w").write(
        "PalmStormHollow_MapScripts::\n\t.byte 0\n\nPalm243_Hiker::\n\tmsgbox Palm243_TextHiker, MSGBOX_NPC\n\tend\n\n"
        "Palm243_TextHiker:\n\t.string \"x$\"\n")

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [x for x in grp["encounters"] if x.get("map") != "MAP_PALM_STORM_HOLLOW"]
    entry = OD([("map", "MAP_PALM_STORM_HOLLOW"), ("base_label", "gPalmStormHollow"),
                ("land_mons", OD([("encounter_rate", 10), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s_)])
                                                                    for (s_, a, b) in WILD])]))])
    idx = next(i for i, x in enumerate(grp["encounters"]) if x.get("map") == "MAP_PALM_STORM_RIDGE") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/hollow.txt"], check=True)
    print("Caverna do pico instalada (selvagens 80-86, 3 itens)")


if __name__ == "__main__":
    main()
