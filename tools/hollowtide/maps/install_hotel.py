#!/usr/bin/env python3
"""Grand Hotel de Tidemouth (pendência do Cap. 10).

- a porta do hotel (44,16), que nao tinha destino, leva ao saguao (layout do 1F da loja de departamentos da
  Lilycove — o mesmo predio de fora; mapa proprio, porque a Breezeport ja usa o mapa da loja);
- fechado durante a crise (antes de FLAG_HT_TIDEMOUTH_COMPLEX_DONE): a entrada faz recuar, a placa e o recepcionista
  da calcada dizem; depois o recepcionista da calcada some, a placa reabre e o saguao funciona: recepcao com
  pernoite (cura) por conta da casa para quem salvou a cidade, concierge, hospedes; elevador e escada com funcionarios.
Rodar depois de install_pavilion.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave, obj, coord, map_json
from install_cap9b import new_map

OD = collections.OrderedDict
DOOR = (44, 16)


def main():
    tp = f"{ROOT}/data/maps/PalmTidemouth/map.json"
    t = jload(tp)
    t["warp_events"] = [w for w in t["warp_events"] if w["dest_map"] != "MAP_PALM_GRAND_HOTEL"]
    widx = len(t["warp_events"])
    t["warp_events"].append(OD([("x", DOOR[0]), ("y", DOOR[1]), ("elevation", 0), ("dest_map", "MAP_PALM_GRAND_HOTEL"), ("dest_warp_id", "0")]))
    t["coord_events"] = [e for e in t["coord_events"] if e["script"] != "Palm270_HotelClosed"] + \
                        [coord(DOOR[0], DOOR[1] + 1, "Palm270_HotelClosed")]
    for o in t["object_events"]:
        if o.get("script") == "Palm201_HotelClerk":
            o["flag"] = "FLAG_HT_TIDEMOUTH_COMPLEX_DONE"          # o recepcionista da calcada some quando o hotel reabre
    for b in t["bg_events"]:
        if b.get("script") == "Palm201_HotelSign":
            b["script"] = "Palm270_HotelSign"
    jsave(tp, t)
    ts = f"{ROOT}/data/maps/PalmTidemouth/scripts.inc"
    s = open(ts).read()
    if "Palm270_HotelClosed::" not in s:
        s += """
Palm270_HotelClosed::
	goto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm270_End
	lockall
	msgbox Palm201_HotelClerk_Text, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, Palm270_StepBack
	waitmovement 0
	releaseall
	end

Palm270_StepBack:
	walk_down
	step_end

Palm270_HotelSign::
	goto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm270_HotelSignOpen
	msgbox Palm201_HotelSign_Text, MSGBOX_SIGN
	end

Palm270_HotelSignOpen::
	msgbox Palm270_TextSignOpen, MSGBOX_SIGN
	end

Palm270_End::
	end
"""
        open(ts, "w").write(s)

    new_map("PalmGrandHotel")
    j = map_json("MAP_PALM_GRAND_HOTEL", "PalmGrandHotel", "LAYOUT_LILYCOVE_CITY_DEPARTMENT_STORE_1F", "MUS_LILYCOVE",
                 "MAPSEC_LILYCOVE_CITY", "MAP_TYPE_INDOOR", [])
    j["show_map_name"] = False
    j["allow_cycling"] = j["allow_running"] = False
    j["warp_events"] = [OD([("x", x), ("y", 7), ("elevation", 0), ("dest_map", "MAP_PALM_TIDEMOUTH"), ("dest_warp_id", str(widx))]) for x in (8, 9)]
    j["object_events"] = [obj("BEAUTY", 8, 2, "MOVEMENT_TYPE_FACE_DOWN", "Palm271_Reception"),
                          obj("GENTLEMAN", 10, 2, "MOVEMENT_TYPE_FACE_DOWN", "Palm271_Concierge"),
                          obj("OBJ_EVENT_GFX_MAN_3", 16, 1, "MOVEMENT_TYPE_FACE_DOWN", "Palm271_Staff"),
                          obj("OBJ_EVENT_GFX_MAN_3", 2, 1, "MOVEMENT_TYPE_FACE_DOWN", "Palm271_Elevator"),
                          obj("POKEFAN_F", 14, 5, "MOVEMENT_TYPE_FACE_LEFT", "Palm271_Guest1"),
                          obj("LITTLE_GIRL", 4, 4, "MOVEMENT_TYPE_WANDER_AROUND", "Palm271_Guest2", rng=1),
                          obj("POKEFAN_M", 3, 6, "MOVEMENT_TYPE_FACE_RIGHT", "Palm271_Guest3"),
                          obj("OBJ_EVENT_GFX_SPECIES(AZUMARILL)", 13, 6, "MOVEMENT_TYPE_FACE_LEFT", "Palm271_Wailmer")]
    jsave(f"{ROOT}/data/maps/PalmGrandHotel/map.json", j)
    open(f"{ROOT}/data/maps/PalmGrandHotel/scripts.inc", "w").write("""PalmGrandHotel_MapScripts::
	.byte 0

Palm271_Reception::
	lock
	faceplayer
	msgbox Palm271_TextReception, MSGBOX_DEFAULT
	msgbox Palm271_TextRest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm271_NoRest
	closemessage
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	special HealPlayerParty
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox Palm271_TextMorning, MSGBOX_DEFAULT
	release
	end

Palm271_NoRest::
	msgbox Palm271_TextNoRest, MSGBOX_DEFAULT
	release
	end

Palm271_Concierge::
	msgbox Palm271_TextConcierge, MSGBOX_NPC
	end

Palm271_Staff::
	msgbox Palm271_TextStaff, MSGBOX_NPC
	end

Palm271_Elevator::
	msgbox Palm271_TextElevator, MSGBOX_NPC
	end

Palm271_Guest1::
	msgbox Palm271_TextGuest1, MSGBOX_NPC
	end

Palm271_Guest2::
	msgbox Palm271_TextGuest2, MSGBOX_NPC
	end

Palm271_Guest3::
	msgbox Palm271_TextGuest3, MSGBOX_NPC
	end

Palm271_Wailmer::
	lock
	playmoncry SPECIES_AZUMARILL, CRY_MODE_NORMAL
	msgbox Palm271_TextWailmer, MSGBOX_DEFAULT
	waitmoncry
	release
	end
""")
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/hotel.txt"], check=True)
    print("Grand Hotel instalado")


if __name__ == "__main__":
    main()
