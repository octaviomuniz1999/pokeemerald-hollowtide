#!/usr/bin/env python3
"""Ginasio do Hoc ("O Circuito") — mapa novo MAP_PALM_HOC_GYM sobre uma copia do layout do ginasio de Mauville.

Todos os feixes comecam LIGADOS. Os quatro botoes de piso sao os consoles de energia; cada um corta o feixe
que guarda o proximo, entao a ordem e imposta pelo proprio salao ("a rota de montagem da corrente"):
  console 1 (0,15)  -> desliga o feixe baixo (4-5, 13-14): abre a ala leste do meio;
  console 2 (4,12)  -> desliga o feixe direito (7-8, 10-11): abre a sala direita;
  console 3 (8,9)   -> desliga o feixe central (4-5, 10-11): abre a sala esquerda;
  console 4 (3,9)   -> desliga o feixe do topo (4-5, 6-7): abre o palco do Hoc.
O feixe esquerdo (1-2, 10-11), o vertical vermelho (3, 11-13) e o vertical verde (6, 8-10) ficam ligados.
Hoc: Jolteon 44, Luxray 45, Ampharos 46, Rotom 47 -> Insignia Circuito (FLAG_BADGE07_GET) + TM55 Volt Switch.
Rodar depois de install_cap9b.py.
"""
import collections, json, os, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import voltara as VT
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register

OD = collections.OrderedDict
C = 1 << 10          # colisao
# feixes horizontais: (x, y_topo) -> cor; o topo do feixe e passavel, a linha de baixo bloqueia
GREEN_ON, GREEN_OFF = (0x220, 0x221, 0x228, 0x229), (0x230, 0x231, 0x238, 0x239)
RED_ON, RED_OFF = (0x222, 0x223, 0x22A, 0x22B), (0x232, 0x233, 0x23A, 0x23B)
BEAMS = {"low": ((4, 13), "green"), "right": ((7, 10), "red"), "mid": ((4, 10), "red"), "top": ((4, 6), "green"),
         "left": ((1, 10), "green")}
CONSOLES = [((0, 15), "low"), ((4, 12), "right"), ((8, 9), "mid"), ((3, 9), "top")]
SWITCH_UP, SWITCH_DOWN = 0x205, 0x206
TRAINERS = [(9, 12, "MAN_5", "LEFT", 2, "Palm194_TrainerA", "TRAINER_PALM_HOC_GYM_A"),
            (7, 8, "EXPERT_M", "DOWN", 2, "Palm194_TrainerB", "TRAINER_PALM_HOC_GYM_B"),
            (0, 10, "EXPERT_M", "RIGHT", 3, "Palm194_TrainerC", "TRAINER_PALM_HOC_GYM_C")]


class Lay:
    w, h, primary, secondary = 10, 21, None, None


def beam_cells(name, on):
    (x, y), color = BEAMS[name]
    mts = (GREEN_ON if on else GREEN_OFF) if color == "green" else (RED_ON if on else RED_OFF)
    return [(x, y, mts[0], False), (x + 1, y, mts[1], False), (x, y + 1, mts[2], on), (x + 1, y + 1, mts[3], on)]


def main():
    L = {l["id"]: l for l in jload(f"{ROOT}/data/layouts/layouts.json")["layouts"] if "id" in l}
    e = L["LAYOUT_MAUVILLE_CITY_GYM"]
    src = list(struct.unpack(f"<{e['width'] * e['height']}H", open(f"{ROOT}/{e['blockdata_filepath']}", "rb").read()))
    lay = Lay(); lay.primary, lay.secondary = e["primary_tileset"], e["secondary_tileset"]
    bl = src[:]
    def put(x, y, m, coll):
        bl[y * 10 + x] = (bl[y * 10 + x] & 0xF000) | (C if coll else 0) | m
    for name in BEAMS:                                   # tudo ligado
        for (x, y, m, coll) in beam_cells(name, True):
            put(x, y, m, coll)
    put(3, 11, 0x241, True); put(3, 12, 0x249, True); put(3, 13, 0x250, True)      # vertical vermelho ligado
    for ((x, y), _) in CONSOLES:
        put(x, y, SWITCH_UP, False)
    register("PalmHocGym", "LAYOUT_PALM_HOC_GYM", lay, bl)
    open(f"{ROOT}/data/layouts/PalmHocGym/border.bin", "wb").write(open(f"{ROOT}/{e['border_filepath']}", "rb").read())

    # ---------------- Voltara: porta do ginasio abre com a energia de volta
    vp = f"{ROOT}/data/maps/PalmVoltara/map.json"
    v = jload(vp)
    gx, gy = VT.door("gym")
    v["warp_events"] = [w for w in v["warp_events"] if w["dest_map"] != "MAP_PALM_HOC_GYM"]
    gym_idx = len(v["warp_events"])
    v["warp_events"].append(OD([("x", gx), ("y", gy), ("elevation", 0), ("dest_map", "MAP_PALM_HOC_GYM"), ("dest_warp_id", "0")]))
    for o in v["object_events"]:
        if o["script"] == "Palm191_Hoc":
            o["graphics_id"] = "OBJ_EVENT_GFX_NORMAN"
    jsave(vp, v)
    vs = f"{ROOT}/data/maps/PalmVoltara/scripts.inc"
    t = open(vs).read()
    old = "Palm191_Load::\n\tsetmetatile"
    if old in t:
        t = t.replace(old, "Palm191_Load::\n\tgoto_if_set FLAG_HT_VOLTARA_DONE, Palm191_Ok\n\tsetmetatile", 1)
    open(vs, "w").write(t)

    # ---------------- mapa do ginasio
    j = map_json("MAP_PALM_HOC_GYM", "PalmHocGym", "LAYOUT_PALM_HOC_GYM", "MUS_GYM", "MAPSEC_FORTREE_CITY", "MAP_TYPE_INDOOR", [])
    j.update({"weather": "WEATHER_NONE", "allow_cycling": False, "allow_running": False, "show_map_name": False,
              "battle_scene": "MAP_BATTLE_SCENE_GYM"})
    j["warp_events"] = [OD([("x", 4), ("y", 20), ("elevation", 0), ("dest_map", "MAP_PALM_VOLTARA"), ("dest_warp_id", str(gym_idx))]),
                        OD([("x", 5), ("y", 20), ("elevation", 0), ("dest_map", "MAP_PALM_VOLTARA"), ("dest_warp_id", str(gym_idx))])]
    j["object_events"] = [obj("NORMAN", 5, 2, "MOVEMENT_TYPE_FACE_DOWN", "Palm194_Hoc"),
                          obj("OBJ_EVENT_GFX_SPECIES(ROTOM)", 6, 3, "MOVEMENT_TYPE_FACE_DOWN", "Palm194_Rotom"),
                          obj("MAN_2", 7, 19, "MOVEMENT_TYPE_FACE_LEFT", "Palm194_Guide")]
    for (x, y, gfx, d, sight, script, _) in TRAINERS:
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    j["coord_events"] = [coord(x, y, f"Palm194_Console{i + 1}") for i, ((x, y), _) in enumerate(CONSOLES)]
    j["bg_events"] = [sign(3, 18, "Palm194_Statue"), sign(6, 18, "Palm194_Statue"), sign(2, 17, "Palm194_Diagram")]
    os.makedirs(f"{ROOT}/data/maps/PalmHocGym", exist_ok=True)
    jsave(f"{ROOT}/data/maps/PalmHocGym/map.json", j)

    def set_beam(name, on):
        return "".join(f"\tsetmetatile {x}, {y}, {m}, {'TRUE' if c else 'FALSE'}\n" for (x, y, m, c) in beam_cells(name, on))
    sc = ["PalmHocGym_MapScripts::\n\tmap_script MAP_SCRIPT_ON_LOAD, Palm194_Load\n\t.byte 0\n"]
    load = "Palm194_Load::\n"
    for i, ((x, y), beam) in enumerate(CONSOLES, 1):
        load += f"\tgoto_if_lt VAR_HT_HOC_GYM, {i}, Palm194_LoadEnd\n" + set_beam(beam, False) + f"\tsetmetatile {x}, {y}, {SWITCH_DOWN}, FALSE\n"
    load += "Palm194_LoadEnd::\n\tend\n"
    sc.append(load)
    for i, ((x, y), beam) in enumerate(CONSOLES, 1):
        sc.append(f"Palm194_Console{i}::\n\tgoto_if_ge VAR_HT_HOC_GYM, {i}, Palm194_End\n\tlockall\n\tplayse SE_SWITCH\n"
                  f"\tsetmetatile {x}, {y}, {SWITCH_DOWN}, FALSE\n" + set_beam(beam, False)
                  + f"\tspecial DrawWholeMapView\n\tplayse SE_UNLOCK\n\tsetvar VAR_HT_HOC_GYM, {i}\n"
                  f"\tmsgbox Palm194_TextConsole{i}, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc += ["Palm194_End::\n\tend\n",
           "Palm194_Hoc::\n\ttrainerbattle_single TRAINER_PALM_HOC, Palm194_TextHocIntro, Palm194_TextHocDefeat, Palm194_HocDefeated, NO_MUSIC\n"
           "\tmsgbox Palm194_TextHocAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
           "Palm194_HocDefeated::\n\tmessage Palm194_TextBadge\n\twaitmessage\n\tcall Common_EventScript_PlayGymBadgeFanfare\n"
           "\tmsgbox Palm194_TextBadgeExplain, MSGBOX_DEFAULT\n\tsetflag FLAG_BADGE07_GET\n\tsetflag FLAG_DEFEATED_LAVARIDGE_GYM\n"
           "\tgiveitem ITEM_TM_VOLT_SWITCH\n\tmsgbox Palm194_TextTM, MSGBOX_DEFAULT\n\tmsgbox Palm194_TextRiven, MSGBOX_DEFAULT\n\trelease\n\tend\n",
           "Palm194_Rotom::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_ROTOM, CRY_MODE_NORMAL\n\tmsgbox Palm194_TextRotom, MSGBOX_DEFAULT\n"
           "\twaitmoncry\n\trelease\n\tend\n",
           "Palm194_Guide::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_BADGE07_GET, Palm194_GuideAfter\n\tmsgbox Palm194_TextGuide, MSGBOX_DEFAULT\n"
           "\trelease\n\tend\n",
           "Palm194_GuideAfter::\n\tmsgbox Palm194_TextGuideAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
           "Palm194_Statue::\n\tlockall\n\tgoto_if_set FLAG_BADGE07_GET, Palm194_StatueWon\n\tmsgbox Palm194_TextStatue, MSGBOX_DEFAULT\n"
           "\treleaseall\n\tend\n",
           "Palm194_StatueWon::\n\tmsgbox Palm194_TextStatueWon, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
           "Palm194_Diagram::\n\tmsgbox Palm194_TextDiagram, MSGBOX_SIGN\n\tend\n"]
    for (_, _, _, _, _, script, tid) in TRAINERS:
        k = script[-1]
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm194_Text{k}Intro, Palm194_Text{k}Defeat\n"
                  f"\tmsgbox Palm194_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    open(f"{ROOT}/data/maps/PalmHocGym/scripts.inc", "w").write("\n".join(sc))
    es = f"{ROOT}/data/event_scripts.s"
    t = open(es).read()
    inc = '\t.include "data/maps/PalmHocGym/scripts.inc"\n'
    if inc not in t:
        anchor = '\t.include "data/maps/PalmFerralia/scripts.inc"\n'
        t = t.replace(anchor, anchor + inc)
        open(es, "w").write(t)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch9_gym.txt"], check=True)
    print("Ginasio do Hoc instalado | porta em Voltara", (gx, gy), "warp", gym_idx)


if __name__ == "__main__":
    main()
