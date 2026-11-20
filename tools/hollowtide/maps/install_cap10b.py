#!/usr/bin/env python3
"""Capitulo 10 (parte 2): o Complexo Oceanico da Team Palm (MAP_PALM_OCEAN_COMPLEX_1F sobre o layout do
esconderijo da Aqua 1F — turbinas, reservatorios, doca; MAP_PALM_OCEAN_COMPLEX_CORE sobre o salao nao usado do
Ruby — sala de controle) e o confronto com o Abelf.

- Tidemouth: depois de falar com a Nami, o marinheiro do porto leva o jogador ao complexo (barco da Nami);
- 1F: 3 recrutas, turbinas e reservatorios; a escada sobe para a sala de controle;
- sala de controle: Nami chega junto; Abelf (Krookodile 49, Magnezone 50, Kingambit 51, Gyarados 52) com as
  falas do canone; vencido, o jogador desliga o sistema central: a Team Palm se dissolve, a mare comeca a
  baixar, mas num monitor, por menos de um segundo, surge o contorno de uma montanha (sem citar Kyogre/orbe);
- de volta a Tidemouth a chuva para e o ginasio da Nami abre (o ginasio entra na parte 3).
Rodar depois de install_cap10.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import tidemouth as TD
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, map_json
from install_cap9b import new_map

OD = collections.OrderedDict
C1, CC = "PalmOceanComplex1F", "PalmOceanComplexCore"
DOCK = (10, 26)                      # chegada do barco no 1F
C1_GRUNTS = [(4, 19, "AQUA_MEMBER_M", "DOWN", 3, "Palm203_Grunt1", "TRAINER_PALM_COMPLEX_GRUNT_1"),
             (13, 11, "AQUA_MEMBER_F", "UP", 2, "Palm203_Grunt2", "TRAINER_PALM_COMPLEX_GRUNT_2"),
             (23, 6, "AQUA_MEMBER_M", "DOWN", 3, "Palm203_Grunt3", "TRAINER_PALM_COMPLEX_GRUNT_3")]
C1_SIGNS = [(2, 15, "Palm203_Turbine"), (25, 22, "Palm203_Turbine"), (10, 6, "Palm203_Tank")]
ABELF = (13, 22)
CORE_CONSOLE = (11, 22)              # parede a esquerda do palco; o jogador examina de (12, 22)


def main():
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    old = "#define FLAG_UNUSED_0x055                    0x55  // Unused Flag"
    if "FLAG_HT_TIDEMOUTH_COMPLEX_DONE" not in t:
        assert old in t, old
        t = t.replace(old, "#define FLAG_HT_TIDEMOUTH_COMPLEX_DONE       0x55  // Abelf derrotado e sistema desligado: a Palm se dissolve")
    open(fp, "w").write(t)

    for name in (C1, CC):
        new_map(name)
    # ---------------- 1F
    j = map_json("MAP_PALM_OCEAN_COMPLEX_1F", C1, "LAYOUT_AQUA_HIDEOUT_1F", "MUS_AQUA_MAGMA_HIDEOUT", "MAPSEC_MOSSDEEP_CITY",
                 "MAP_TYPE_INDOOR", [])
    j.update({"weather": "WEATHER_NONE", "allow_cycling": False, "show_map_name": False})
    j["warp_events"] = [OD([("x", 22), ("y", 1), ("elevation", 0), ("dest_map", "MAP_PALM_OCEAN_COMPLEX_CORE"), ("dest_warp_id", "0")])]
    j["object_events"] = [obj("SAILOR", DOCK[0] - 1, DOCK[1], "MOVEMENT_TYPE_FACE_RIGHT", "Palm203_Boat")]
    for (x, y, gfx, d, sight, script, _) in C1_GRUNTS:
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in C1_SIGNS]
    jsave(f"{ROOT}/data/maps/{C1}/map.json", j)
    sc = [f"{C1}_MapScripts::\n\t.byte 0\n",
          "Palm203_Boat::\n\tlock\n\tfaceplayer\n\tmsgbox Palm203_TextBoat, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, Palm203_BoatNo\n"
          "\twarp MAP_PALM_TIDEMOUTH, 33, 38\n\twaitstate\n\trelease\n\tend\n",
          "Palm203_BoatNo::\n\trelease\n\tend\n"]
    for (_, _, _, _, _, script, tid) in C1_GRUNTS:
        k = script.replace("Palm203_", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm203_Text{k}Intro, Palm203_Text{k}Loss\n"
                  f"\tmsgbox Palm203_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for s_ in sorted({s for (_, _, s) in C1_SIGNS}):
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/{C1}/scripts.inc", "w").write("\n".join(sc))

    # ---------------- sala de controle
    j = map_json("MAP_PALM_OCEAN_COMPLEX_CORE", CC, "LAYOUT_AQUA_HIDEOUT_UNUSED_RUBY_MAP1", "MUS_AQUA_MAGMA_HIDEOUT",
                 "MAPSEC_MOSSDEEP_CITY", "MAP_TYPE_INDOOR", [])
    j.update({"weather": "WEATHER_NONE", "allow_cycling": False, "show_map_name": False})
    j["warp_events"] = [OD([("x", 13), ("y", 1), ("elevation", 0), ("dest_map", "MAP_PALM_OCEAN_COMPLEX_1F"), ("dest_warp_id", "0")])]
    j["object_events"] = [obj("ARCHIE", ABELF[0], ABELF[1], "MOVEMENT_TYPE_FACE_UP", "Palm204_Abelf",
                              "TRAINER_TYPE_NORMAL", 2, flag="FLAG_HT_TIDEMOUTH_COMPLEX_DONE"),
                          obj("WOMAN_5", 15, 18, "MOVEMENT_TYPE_FACE_DOWN", "Palm204_Nami")]
    j["bg_events"] = [sign(CORE_CONSOLE[0], CORE_CONSOLE[1], "Palm204_Console"), sign(16, 22, "Palm204_Monitor")]
    jsave(f"{ROOT}/data/maps/{CC}/map.json", j)
    sc = [f"{CC}_MapScripts::\n\t.byte 0\n",
          "Palm204_Abelf::\n\ttrainerbattle_single TRAINER_PALM_ABELF, Palm204_TextAbelfIntro, Palm204_TextAbelfLoss, Palm204_AbelfDefeated\n"
          "\tmsgbox Palm204_TextAbelfAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm204_AbelfDefeated::\n\tmsgbox Palm204_TextAbelfAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm204_Nami::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm204_NamiDone\n"
          "\tgoto_if_defeated TRAINER_PALM_ABELF, Palm204_NamiConsole\n\tmsgbox Palm204_TextNami, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm204_NamiConsole::\n\tmsgbox Palm204_TextNamiConsole, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm204_NamiDone::\n\tmsgbox Palm204_TextNamiDone, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm204_Console::\n\tlockall\n\tgoto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm204_ConsoleOff\n"
          "\tgoto_if_not_defeated TRAINER_PALM_ABELF, Palm204_ConsoleGuarded\n\tmsgbox Palm204_TextConsole, MSGBOX_YESNO\n"
          "\tgoto_if_eq VAR_RESULT, NO, Palm204_Release\n\tplayse SE_PC_OFF\n\twaitse\n\tmsgbox Palm204_TextShutdown, MSGBOX_DEFAULT\n"
          "\tsetflag FLAG_HT_TIDEMOUTH_COMPLEX_DONE\n\tplayse SE_PIN\n\tmsgbox Palm204_TextMountain, MSGBOX_DEFAULT\n"
          "\tmsgbox Palm204_TextNamiDone, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
          "Palm204_ConsoleOff::\n\tmsgbox Palm204_TextConsoleOff, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
          "Palm204_ConsoleGuarded::\n\tmsgbox Palm204_TextConsoleGuarded, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
          "Palm204_Monitor::\n\tmsgbox Palm204_TextMonitor, MSGBOX_SIGN\n\tend\n",
          "Palm204_Release::\n\treleaseall\n\tend\n"]
    open(f"{ROOT}/data/maps/{CC}/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Tidemouth: barco da Nami no porto; depois do complexo a chuva para e o ginasio abre
    tp = f"{ROOT}/data/maps/PalmTidemouth/map.json"
    tj = jload(tp)
    tj["warp_events"] = [w for w in tj["warp_events"] if w["dest_map"] != "MAP_PALM_OCEAN_COMPLEX_1F"]
    jsave(tp, tj)
    ts = f"{ROOT}/data/maps/PalmTidemouth/scripts.inc"
    t = open(ts).read()
    t = t.replace("PalmTidemouth_MapScripts::\n\t.byte 0\n",
                  "PalmTidemouth_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, Palm201_Transition\n\t.byte 0\n", 1)
    if "Palm201_Transition::" not in t:
        t += ("\nPalm201_Transition::\n\tgoto_if_unset FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm201_TransEnd\n\tsetweather WEATHER_SUNNY\n"
              "Palm201_TransEnd::\n\tend\n")
    t = t.replace("Palm201_PortLock::\n\tlockall\n", "Palm201_PortLock::\n\tlockall\n\tgoto_if_set FLAG_HT_TIDEMOUTH_NAMI_MET, Palm201_Boat\n", 1)
    t = t.replace("Palm201_GymLock::\n\tlockall\n", "Palm201_GymLock::\n\tgoto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm201_TransEnd\n\tlockall\n", 1)
    if "Palm201_Boat::" not in t:
        t += ("\nPalm201_Boat::\n\tmsgbox Palm201_TextBoat, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, Palm201_BoatNo\n"
              f"\twarp MAP_PALM_OCEAN_COMPLEX_1F, {DOCK[0]}, {DOCK[1]}\n\twaitstate\n\treleaseall\n\tend\n"
              "Palm201_BoatNo::\n\tapplymovement OBJ_EVENT_ID_PLAYER, Palm201_StepBackSouth\n\twaitmovement 0\n\treleaseall\n\tend\n")
    open(ts, "w").write(t)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch10b.txt"], check=True)
    print("Cap. 10 (parte 2) instalado: Complexo Oceanico 1F + sala de controle")


if __name__ == "__main__":
    main()
