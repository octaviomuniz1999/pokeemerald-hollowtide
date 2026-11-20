#!/usr/bin/env python3
"""Ferrovia Voltara–Ferrália–Tradepost (pendência do Cap. 9; roteiro sec. 14: com os terminais da Palm desligados,
a ferrovia volta a funcionar).

- as portas das estacoes, que estavam fechadas, levam a saguoes (layout do 1F da Devon: balcao de bilhetes) —
  Voltara (estacao, porta 26,17), Tradepost (estacao, 14,7) e Ferralia (sede da ferrovia, 28,12);
- a bilheteira oferece os dois outros destinos (pergunta um de cada vez); antes do Vega (FLAG_HT_VOLTARA_DONE)
  os trens estao suspensos; a viagem e uma transicao com o som do trem;
- a escada do saguao da Devon fica fechada por um funcionario (so plataforma).
Rodar depois de install_cap12c.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave, obj, map_json
from install_cap9b import new_map

OD = collections.OrderedDict
# (pasta do saguao, mapa da cidade, porta na cidade, nome no texto, rotulo)
STATIONS = [("PalmStationVoltara", "PalmVoltara", "MAP_PALM_VOLTARA", (26, 17), "VOLTARA", "Volt"),
            ("PalmStationFerralia", "PalmFerralia", "MAP_PALM_FERRALIA", (28, 12), "FERRALIA", "Ferr"),
            ("PalmStationTradepost", "PalmTradepost", "MAP_PALM_TRADEPOST", (14, 7), "TRADEPOST", "Trad")]
MAPID = {s[0]: "MAP_" + "PALM_STATION_" + s[4] for s in STATIONS}
ARRIVE = (5, 7)


def main():
    texts = ["## file: data/maps/PalmStationVoltara/scripts.inc"]
    for (folder, city, city_id, door, name, lab) in STATIONS:
        # porta da cidade -> saguao
        cp = f"{ROOT}/data/maps/{city}/map.json"
        cj = jload(cp)
        cj["warp_events"] = [w for w in cj["warp_events"] if w["dest_map"] != MAPID[folder]] + \
                            [OD([("x", door[0]), ("y", door[1]), ("elevation", 0), ("dest_map", MAPID[folder]), ("dest_warp_id", "0")])]
        widx = len(cj["warp_events"]) - 1
        jsave(cp, cj)
        # saguao
        new_map(folder)
        j = map_json(MAPID[folder], folder, "LAYOUT_RUSTBORO_CITY_DEVON_CORP_1F", "MUS_POKE_CENTER", "MAPSEC_NONE", "MAP_TYPE_INDOOR", [])
        j["region_map_section"] = {"PalmVoltara": "MAPSEC_MAUVILLE_CITY", "PalmFerralia": "MAPSEC_RUSTBORO_CITY",
                                   "PalmTradepost": "MAPSEC_VERDANTURF_TOWN"}[city]
        j["show_map_name"] = False
        j["allow_cycling"] = j["allow_running"] = False
        j["warp_events"] = [OD([("x", x), ("y", 8), ("elevation", 0), ("dest_map", city_id), ("dest_warp_id", str(widx))]) for x in (5, 6)]
        j["object_events"] = [obj("WOMAN_3", 5, 3, "MOVEMENT_TYPE_FACE_DOWN", f"Palm250_{lab}Clerk"),
                              obj("OBJ_EVENT_GFX_DEVON_EMPLOYEE", 14, 1, "MOVEMENT_TYPE_FACE_DOWN", "Palm250_Staff"),
                              obj("MAN_1", 2, 6, "MOVEMENT_TYPE_WANDER_AROUND", f"Palm250_{lab}Traveler", rng=1),
                              obj("WOMAN_2", 15, 5, "MOVEMENT_TYPE_FACE_LEFT", f"Palm250_{lab}Traveler2")]
        jsave(f"{ROOT}/data/maps/{folder}/map.json", j)
        others = [s for s in STATIONS if s[0] != folder]
        sc = [f"{folder}_MapScripts::\n\t.byte 0\n",
              f"Palm250_{lab}Clerk::\n\tlock\n\tfaceplayer\n\tgoto_if_unset FLAG_HT_VOLTARA_DONE, Palm250_Suspended\n"
              f"\tmsgbox Palm250_TextWelcome, MSGBOX_DEFAULT\n"]
        for (f2, _, _, _, n2, l2) in others:
            sc[-1] += (f"\tmsgbox Palm250_TextAsk{l2}, MSGBOX_YESNO\n"
                       f"\tgoto_if_eq VAR_RESULT, YES, Palm250_Go{l2}\n")
        sc[-1] += "\tmsgbox Palm250_TextComeAgain, MSGBOX_DEFAULT\n\trelease\n\tend\n"
        sc.append(f"Palm250_{lab}Traveler::\n\tmsgbox Palm250_Text{lab}Traveler, MSGBOX_NPC\n\tend\n")
        sc.append(f"Palm250_{lab}Traveler2::\n\tmsgbox Palm250_Text{lab}Traveler2, MSGBOX_NPC\n\tend\n")
        if folder == "PalmStationVoltara":
            sc.append("Palm250_Suspended::\n\tmsgbox Palm250_TextSuspended, MSGBOX_DEFAULT\n\trelease\n\tend\n")
            sc.append("Palm250_Staff::\n\tmsgbox Palm250_TextStaff, MSGBOX_NPC\n\tend\n")
            sc.append("Palm250_TextAllAboard::\n\tmsgbox Palm250_TextBoard, MSGBOX_DEFAULT\n\tcloseMessage\n"
                      "\tfadescreen FADE_TO_BLACK\n\tplayse SE_TRUCK_MOVE\n\tdelay 60\n\tplayse SE_DING_DONG\n\twaitse\n\tdelay 40\n\treturn\n")
            for (f2, _, _, _, n2, l2) in STATIONS:
                sc.append(f"Palm250_Go{l2}::\n\tcall Palm250_TextAllAboard\n\twarpsilent {MAPID[f2]}, {ARRIVE[0]}, {ARRIVE[1]}\n"
                          "\twaitstate\n\trelease\n\tend\n")
        open(f"{ROOT}/data/maps/{folder}/scripts.inc", "w").write("\n".join(sc).replace("closeMessage", "closemessage"))
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/train.txt"], check=True)
    print("Ferrovia instalada: Voltara, Ferralia, Tradepost")


if __name__ == "__main__":
    main()
