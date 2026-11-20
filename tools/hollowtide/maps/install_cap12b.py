#!/usr/bin/env python3
"""Capitulo 12 (parte 2): Storm Mountain — a crista: o posto da Joy e a Cynthia na ultima escadaria.

- MAP_PALM_STORM_RIDGE continua a trilha pelo norte (mesmo x); MAP_PALM_STORM_CABIN e a cabana de campanha
  da Liga (layout de casa generico) com a Enfermeira Joy: cura e conta da Cynthia (roteiro, sec. 17);
- a Cynthia (slot TRAINER_STEVEN, sem uso; sprite de PK Black Pearl) para o jogador no pe da ultima escadaria:
  avisa, pergunta se ele volta; se insistir, luta (Spiritomb 79, Roserade 80, Togekiss 81, Lucario 82, Milotic 83,
  Garchomp @ Garchompite 85 por ultimo); depois da vitoria a Joy sobe e cura o time, e a Cynthia sai da frente;
- a escadaria leva ao cume (parte 3).
Rodar depois de install_cap12.py.
"""
import collections, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import storm_ridge as SR
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable
from install_cap9b import new_map
from install_cap11b import mon, header

OD = collections.OrderedDict
FLAG = ("FLAG_UNUSED_0x1AB", "0x1AB", "FLAG_HT_CYNTHIA_DONE", "Cynthia vencida na ultima escadaria da Storm Mountain")
CYNTHIA_PARTY = header("TRAINER_STEVEN", "CYNTHIA", "Champion", "Champion Cynthia", "Female", "Female",
                       ["Full Restore"] * 4, "Check Bad Move / Try To Faint", "Purple") + "\n".join([
    mon("Spiritomb", 79, ["Shadow Ball", "Dark Pulse", "Will-O-Wisp", "Sucker Punch"], 31),
    mon("Roserade", 80, ["Leaf Storm", "Sludge Bomb", "Shadow Ball", "Extrasensory"], 31),
    mon("Togekiss", 81, ["Air Slash", "Dazzling Gleam", "Aura Sphere", "Flamethrower"], 31, ability="Serene Grace"),
    mon("Lucario", 82, ["Aura Sphere", "Flash Cannon", "Dragon Pulse", "Extreme Speed"], 31),
    mon("Milotic", 83, ["Hydro Pump", "Ice Beam", "Dragon Pulse", "Recover"], 31),
    mon("Garchomp", 85, ["Earthquake", "Dragon Claw", "Stone Edge", "Swords Dance"], 31, "Garchompite")])
ITEMS = [(26, 42, "ITEM_PP_MAX", "FLAG_ITEM_ROUTE_114_PROTEIN"), (10, 16, "ITEM_FULL_RESTORE", "FLAG_ITEM_ROUTE_133_BIG_PEARL")]


def main():
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    old, val, new, why = FLAG
    if new not in t:
        t, n = re.subn(r"#define %s\s+%s[^\n]*\n" % (old, val), f"#define {new:<36} {val} // {why}\n", t, count=1)
        assert n == 1
        open(fp, "w").write(t)

    pp = f"{ROOT}/data/trainers.party" if False else f"{ROOT}/src/data/trainers.party"
    pt = open(pp).read()
    pat = re.compile(r"=== TRAINER_STEVEN ===\n.*?(?=\n=== )", re.S)
    assert len(pat.findall(pt)) == 1
    pt = pat.sub(lambda _m: CYNTHIA_PARTY.rstrip("\n") + "\n", pt)
    open(pp, "w").write(pt)

    # ---------------- trilha -> crista
    tp = f"{ROOT}/data/maps/PalmStormTrail/map.json"
    tj = jload(tp)
    tj["connections"] = [cn for cn in tj["connections"] if cn["map"] != "MAP_PALM_STORM_RIDGE"] + \
                        [OD([("map", "MAP_PALM_STORM_RIDGE"), ("offset", -SR.OFFSET_TRAIL), ("direction", "up")])]
    jsave(tp, tj)

    # ---------------- a crista
    c = SR.compose()
    c.put(*SR.SIGN, 3, collision=1)
    bl = SR.flatten(c.build())
    register("PalmStormRidge", "LAYOUT_PALM_STORM_RIDGE", c, bl)
    j = map_json("MAP_PALM_STORM_RIDGE", "PalmStormRidge", "LAYOUT_PALM_STORM_RIDGE", "MUS_ROUTE120", "MAPSEC_MT_CHIMNEY",
                 "MAP_TYPE_ROUTE", [OD([("map", "MAP_PALM_STORM_TRAIL"), ("offset", SR.OFFSET_TRAIL), ("direction", "down")])])
    j["weather"] = "WEATHER_RAIN_THUNDERSTORM"
    cx, cy = SR.CYNTHIA
    assert walkable(bl, c.w, cx, cy) and walkable(bl, c.w, cx + 1, cy)
    cyn = obj("CHAMPION_CYNTHIA", cx, cy, "MOVEMENT_TYPE_FACE_DOWN", "Palm230_Cynthia")
    cyn = OD([("local_id", "LOCALID_STORM_CYNTHIA")] + list(cyn.items()))
    j["object_events"] = [cyn]
    for (x, y, item, flag) in ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    door = (SR.CABIN[0] + 1, SR.CABIN[1] + 3)
    j["warp_events"] = [OD([("x", door[0]), ("y", door[1]), ("elevation", 0), ("dest_map", "MAP_PALM_STORM_CABIN"), ("dest_warp_id", "0")])]
    j["coord_events"] = [coord(x, cy + 1, "Palm230_CynthiaStop") for x in SR.STAIR_X]
    j["bg_events"] = [sign(*SR.SIGN, "Palm230_SignPost")]
    jsave(f"{ROOT}/data/maps/PalmStormRidge/map.json", j)
    sc = ["PalmStormRidge_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, Palm230_OnTransition\n\t.byte 0\n",
          f"Palm230_OnTransition:\n\tcall_if_set FLAG_HT_CYNTHIA_DONE, Palm230_CynthiaAside\n\tend\n",
          f"Palm230_CynthiaAside::\n\tsetobjectxyperm LOCALID_STORM_CYNTHIA, {cx + 1}, {cy}\n"
          "\tsetobjectmovementtype LOCALID_STORM_CYNTHIA, MOVEMENT_TYPE_FACE_LEFT\n\treturn\n",
          "Palm230_CynthiaStop::\n\tgoto_if_set FLAG_HT_CYNTHIA_DONE, Palm230_End\n\tlockall\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterUp\n\twaitmovement 0\n"
          "\tgoto Palm230_CynthiaTalk\n\tend\n",
          "Palm230_Cynthia::\n\tlockall\n\tgoto_if_set FLAG_HT_CYNTHIA_DONE, Palm230_CynthiaAfter\n\tgoto Palm230_CynthiaTalk\n\tend\n",
          "Palm230_CynthiaTalk::\n\tplaybgm MUS_HT_CYNTHIA_ENCOUNTER, FALSE\n\tmsgbox Palm230_TextCynthiaWarn1, MSGBOX_DEFAULT\n"
          "\tmsgbox Palm230_TextCynthiaAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, YES, Palm230_TurnBack\n"
          "\tmsgbox Palm230_TextCynthiaWarn2, MSGBOX_DEFAULT\n"
          "\tmsgbox Palm230_TextCynthiaAsk, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, YES, Palm230_TurnBack\n"
          "\tmsgbox Palm230_TextCynthiaIntro, MSGBOX_DEFAULT\n"
          "\ttrainerbattle_no_intro TRAINER_STEVEN, Palm230_TextCynthiaDefeat\n"
          "\tmsgbox Palm230_TextCynthiaPost, MSGBOX_DEFAULT\n\tcloseMessage\n"
          "\tfadescreen FADE_TO_BLACK\n\tspecial HealPlayerParty\n\tplayfanfare MUS_HEAL\n\twaitfanfare\n\tfadescreen FADE_FROM_BLACK\n"
          "\tmsgbox Palm230_TextJoyHeal, MSGBOX_DEFAULT\n"
          "\tapplymovement LOCALID_STORM_CYNTHIA, Palm230_StepAside\n\twaitmovement 0\n"
          "\tsetflag FLAG_HT_CYNTHIA_DONE\n\tcall Palm230_CynthiaAside\n"
          "\tmsgbox Palm230_TextCynthiaGo, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
          "Palm230_TurnBack::\n\tmsgbox Palm230_TextCynthiaThanks, MSGBOX_DEFAULT\n\tfadedefaultbgm\n\tcloseMessage\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm230_StepBackDown\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm230_CynthiaAfter::\n\tmsgbox Palm230_TextCynthiaGo, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
          "Palm230_End::\n\tend\n",
          "Palm230_StepAside:\n\twalk_right\n\twalk_in_place_faster_left\n\tstep_end\n",
          "Palm230_StepBackDown:\n\twalk_down\n\tstep_end\n",
          "Palm230_SignPost::\n\tmsgbox Palm230_SignPost_Text, MSGBOX_SIGN\n\tend\n"]
    open(f"{ROOT}/data/maps/PalmStormRidge/scripts.inc", "w").write("\n".join(sc).replace("closeMessage", "closemessage"))

    # ---------------- a cabana da Joy (interior generico de casa)
    new_map("PalmStormCabin")
    k = map_json("MAP_PALM_STORM_CABIN", "PalmStormCabin", "LAYOUT_HOUSE3", "MUS_POKE_CENTER", "MAPSEC_MT_CHIMNEY", "MAP_TYPE_INDOOR", [])
    k["show_map_name"] = False
    k["allow_cycling"] = False
    joy = obj("NURSE", 2, 3, "MOVEMENT_TYPE_FACE_DOWN", "Palm231_Joy")
    k["object_events"] = [joy, obj("OBJ_EVENT_GFX_SPECIES(CHANSEY)", 6, 6, "MOVEMENT_TYPE_FACE_LEFT", "Palm231_Chansey")]
    k["warp_events"] = [OD([("x", x), ("y", 7), ("elevation", 0), ("dest_map", "MAP_PALM_STORM_RIDGE"), ("dest_warp_id", "0")]) for x in (3, 4)]
    jsave(f"{ROOT}/data/maps/PalmStormCabin/map.json", k)
    kc = ["PalmStormCabin_MapScripts::\n\t.byte 0\n",
          "Palm231_Joy::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_CYNTHIA_DONE, Palm231_JoyAfter\n"
          "\tmsgbox Palm231_TextJoy, MSGBOX_DEFAULT\n\tgoto Palm231_Heal\n\tend\n",
          "Palm231_JoyAfter::\n\tmsgbox Palm231_TextJoyAfter, MSGBOX_DEFAULT\n\tgoto Palm231_Heal\n\tend\n",
          "Palm231_Heal::\n\tcloseMessage\n\tfadescreen FADE_TO_BLACK\n\tspecial HealPlayerParty\n\tplayfanfare MUS_HEAL\n\twaitfanfare\n"
          "\tfadescreen FADE_FROM_BLACK\n\tmsgbox Palm231_TextHealed, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm231_Chansey::\n\tlock\n\tplaymoncry SPECIES_CHANSEY, CRY_MODE_NORMAL\n\tmsgbox Palm231_TextChansey, MSGBOX_DEFAULT\n"
          "\twaitmoncry\n\trelease\n\tend\n"]
    open(f"{ROOT}/data/maps/PalmStormCabin/scripts.inc", "w").write("\n".join(kc).replace("closeMessage", "closemessage"))

    # ---------------- encontros (os mesmos da trilha, 4 niveis acima)
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [x for x in grp["encounters"] if x.get("map") != "MAP_PALM_STORM_RIDGE"]
    base = next(x for x in grp["encounters"] if x.get("map") == "MAP_PALM_STORM_TRAIL")
    mons = [OD([("min_level", m["min_level"] + 4), ("max_level", m["max_level"] + 4), ("species", m["species"])]) for m in base["land_mons"]["mons"]]
    entry = OD([("map", "MAP_PALM_STORM_RIDGE"), ("base_label", "gPalmStormRidge"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", mons)]))])
    idx = next(i for i, x in enumerate(grp["encounters"]) if x.get("map") == "MAP_PALM_STORM_TRAIL") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch12b.txt"], check=True)
    print("Cap. 12 (parte 2) instalado: crista, posto da Joy e Cynthia", c.w, "x", c.h)


if __name__ == "__main__":
    main()
