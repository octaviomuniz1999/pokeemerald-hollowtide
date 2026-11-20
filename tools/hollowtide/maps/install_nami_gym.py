#!/usr/bin/env python3
"""Ginasio da Nami ("As Eclusas") — mapa novo MAP_PALM_NAMI_GYM (arena aquatica, ver namigym.py).

O mapa salvo tem os tres canais secos; ate cada eclusa abrir, o ON_LOAD enche o canal por setmetatile (agua
bloqueada: setmetatile nao muda a elevacao). Alavanca k so funciona com VAR_HT_NAMI_GYM == k-1 e, de qualquer
forma, so e alcancavel depois da anterior. 3 nadadores; Nami (Pelipper 47, Ludicolo 48, Wailord 49, Milotic 50,
Gyarados 52) -> Insignia Mare (FLAG_BADGE08_GET) + HM07 Waterfall (o TM proposto vira o HM existente). Entrada pela porta do pavilhao de Tidemouth.
Rodar depois de install_cap10b.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import namigym as NG, tidemouth as TD
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register

OD = collections.OrderedDict
TRAINERS = [(15, 25, "SWIMMER_F", "LEFT", 4, "Palm205_TrainerA", "TRAINER_PALM_NAMI_GYM_A"),
            (8, 15, "SWIMMER_M", "RIGHT", 4, "Palm205_TrainerB", "TRAINER_PALM_NAMI_GYM_B"),
            (15, 7, "SWIMMER_F", "LEFT", 4, "Palm205_TrainerC", "TRAINER_PALM_NAMI_GYM_C")]
NAMI = (11, 3)
ARRIVE = [(11, 38), (12, 38)]


def main():
    vp = f"{ROOT}/include/constants/vars.h"
    t = open(vp).read()
    if "VAR_HT_NAMI_GYM" not in t:
        t = t.replace("#define VAR_UNUSED_0x4091                                0x4091 // Unused Var",
                      "#define VAR_HT_NAMI_GYM                                  0x4091 // Hollowtide: eclusas abertas no ginasio da Nami (0-3)")
    open(vp, "w").write(t)

    c = NG.compose((True, True, True))
    bl = c.build()
    floods = []
    for k in range(3):
        st = [True, True, True]; st[k] = False
        blf = NG.compose(tuple(st)).build()
        floods.append([(i % c.w, i // c.w, blf[i]) for i in range(len(bl)) if (bl[i] & 0xFFF) != (blf[i] & 0xFFF)])
    register("PalmNamiGym", "LAYOUT_PALM_NAMI_GYM", c, bl)

    # Tidemouth: porta do pavilhao vira warp para a arena
    tp = f"{ROOT}/data/maps/PalmTidemouth/map.json"
    tj = jload(tp)
    gx, gy = TD.door("gym")
    tj["warp_events"] = [w for w in tj["warp_events"] if w["dest_map"] != "MAP_PALM_NAMI_GYM"]
    gym_idx = len(tj["warp_events"])
    tj["warp_events"] += [OD([("x", gx), ("y", gy), ("elevation", 0), ("dest_map", "MAP_PALM_NAMI_GYM"), ("dest_warp_id", "0")]),
                          OD([("x", gx + 1), ("y", gy), ("elevation", 0), ("dest_map", "MAP_PALM_NAMI_GYM"), ("dest_warp_id", "1")])]
    jsave(tp, tj)

    j = map_json("MAP_PALM_NAMI_GYM", "PalmNamiGym", "LAYOUT_PALM_NAMI_GYM", "MUS_GYM", "MAPSEC_MOSSDEEP_CITY", "MAP_TYPE_INDOOR", [])
    j.update({"weather": "WEATHER_SUNNY", "allow_cycling": False, "allow_running": True, "show_map_name": False,
              "battle_scene": "MAP_BATTLE_SCENE_GYM"})
    j["warp_events"] = [OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", "MAP_PALM_TIDEMOUTH"), ("dest_warp_id", str(gym_idx + i))])
                        for i, (x, y) in enumerate(ARRIVE)]
    j["object_events"] = [obj("BEAUTY", NAMI[0], NAMI[1], "MOVEMENT_TYPE_FACE_DOWN", "Palm205_Nami"),
                          obj("OBJ_EVENT_GFX_SPECIES(WAILMER)", 14, 3,
                              "MOVEMENT_TYPE_FACE_DOWN", "Palm205_Wailmer"),
                          obj("MAN_2", 14, 36, "MOVEMENT_TYPE_FACE_LEFT", "Palm205_Guide")]
    for (x, y, gfx, d, sight, script, _) in TRAINERS:
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    j["coord_events"] = [coord(x, NG.H - 1, "Palm205_Exit") for x in NG.ENTRANCE]
    j["bg_events"] = [sign(x, y, f"Palm205_Lever{i + 1}") for i, (x, y) in enumerate(NG.LEVERS)] + [sign(9, 36, "Palm205_Board")]
    os.makedirs(f"{ROOT}/data/maps/PalmNamiGym", exist_ok=True)
    jsave(f"{ROOT}/data/maps/PalmNamiGym/map.json", j)

    def cmds(lst):
        return "".join(f"\tsetmetatile {x}, {y}, {v & 0x3FF}, {'TRUE' if (v >> 10) & 3 or (v >> 12) == 1 else 'FALSE'}\n" for (x, y, v) in lst)
    def dry(k):
        return "".join(f"\tsetmetatile {x}, {y}, {bl[y * c.w + x] & 0x3FF}, {'TRUE' if (bl[y * c.w + x] >> 10) & 3 else 'FALSE'}\n"
                       for (x, y, _) in floods[k])
    load = "Palm205_Load::\n"
    for k in range(3):
        load += f"\tgoto_if_ge VAR_HT_NAMI_GYM, {k + 1}, Palm205_Load{k + 2}\n" + cmds(floods[k]) + f"Palm205_Load{k + 2}::\n"
    load += "\tend\n"
    sc = ["PalmNamiGym_MapScripts::\n\tmap_script MAP_SCRIPT_ON_LOAD, Palm205_Load\n\t.byte 0\n", load]
    for k in range(3):
        sc.append(f"Palm205_Lever{k + 1}::\n\tlockall\n\tgoto_if_ge VAR_HT_NAMI_GYM, {k + 1}, Palm205_LeverDone\n"
                  f"\tmsgbox Palm205_TextLever, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, Palm205_Release\n\tplayse SE_SWITCH\n\twaitse\n"
                  "\tplayse SE_M_WATERFALL\n" + dry(k) + "\tspecial DrawWholeMapView\n"
                  f"\tsetvar VAR_HT_NAMI_GYM, {k + 1}\n\tmsgbox Palm205_TextDrained{k + 1}, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc += ["Palm205_LeverDone::\n\tmsgbox Palm205_TextLeverDone, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
           "Palm205_Release::\n\treleaseall\n\tend\n",
           f"Palm205_Exit::\n\twarp MAP_PALM_TIDEMOUTH, {gx}, {gy + 1}\n\twaitstate\n\tend\n",
           "Palm205_Nami::\n\ttrainerbattle_single TRAINER_PALM_NAMI, Palm205_TextNamiIntro, Palm205_TextNamiDefeat, Palm205_NamiDefeated, NO_MUSIC\n"
           "\tmsgbox Palm205_TextNamiAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
           "Palm205_NamiDefeated::\n\tmessage Palm205_TextBadge\n\twaitmessage\n\tcall Common_EventScript_PlayGymBadgeFanfare\n"
           "\tmsgbox Palm205_TextBadgeExplain, MSGBOX_DEFAULT\n\tsetflag FLAG_BADGE08_GET\n\tsetflag FLAG_DEFEATED_SOOTOPOLIS_GYM\n"
           "\tgiveitem ITEM_HM_WATERFALL\n\tmsgbox Palm205_TextTM, MSGBOX_DEFAULT\n\trelease\n\tend\n",
           "Palm205_Wailmer::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_WAILMER, CRY_MODE_NORMAL\n\tmsgbox Palm205_TextWailmer, MSGBOX_DEFAULT\n"
           "\twaitmoncry\n\trelease\n\tend\n",
           "Palm205_Guide::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_BADGE08_GET, Palm205_GuideAfter\n\tmsgbox Palm205_TextGuide, MSGBOX_DEFAULT\n"
           "\trelease\n\tend\n",
           "Palm205_GuideAfter::\n\tmsgbox Palm205_TextGuideAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
           "Palm205_Board::\n\tmsgbox Palm205_TextBoard, MSGBOX_SIGN\n\tend\n"]
    for (_, _, _, _, _, script, tid) in TRAINERS:
        k = script[-1]
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm205_Text{k}Intro, Palm205_Text{k}Defeat\n"
                  f"\tmsgbox Palm205_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    open(f"{ROOT}/data/maps/PalmNamiGym/scripts.inc", "w").write("\n".join(sc))
    es = f"{ROOT}/data/event_scripts.s"
    t = open(es).read()
    inc = '\t.include "data/maps/PalmNamiGym/scripts.inc"\n'
    if inc not in t:
        anchor = '\t.include "data/maps/PalmFerralia/scripts.inc"\n'
        t = t.replace(anchor, anchor + inc)
        open(es, "w").write(t)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch10_gym.txt"], check=True)
    print("Ginasio da Nami instalado | porta em Tidemouth", (gx, gy), "warps", gym_idx, gym_idx + 1,
          "| canais", [len(f) for f in floods])


if __name__ == "__main__":
    main()
