#!/usr/bin/env python3
"""Capitulo 12 (parte 3): o cume — Tavinho, Primal Kyogre e o epilogo.

- MAP_PALM_STORM_SUMMIT continua a ultima escadaria da crista (cume x = crista x - 6);
- Tavinho (slot TRAINER_MAXIE_MOSSDEEP, sem uso; sprite/retrato provisorios Red) no meio do pico: falas do
  roteiro (sec. 17), luta: Pelipper 87 (Drizzle), Swampert 88, Scizor 89, Garchomp 90, Urshifu Golpe Fluido 91 e
  Kyogre @ Blue Orb 94 por ultimo (Reversao Primal na entrada, Primordial Sea);
- depois: o medalhao, o Doge chega, as falas finais; epilogo: Tavinho entrega a bola do Kyogre e a Orbe Azul ao
  Doge, que voa no Mega Latios ate a Caverna Marinha de Hoenn (layout de Marine Cave End) e sela o Kyogre; de volta
  ao cume, a tempestade passou (trilha, crista e cume ensolarados) e a tela final;
- VAR_HT_EPILOGUE (0x409B): 1 indo a Hoenn, 2 de volta ao cume, 3 fim; FLAG_HT_SUMMIT_DONE (0x1DA) Tavinho vencido;
  FLAG_HT_HIDE_SUMMIT_DOGE (0x1DE) esconde o Doge ate ele chegar.
Rodar depois de install_cap12b.py.
"""
import collections, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import storm_summit as SM
from canvas import ROOT
from install_cap4 import jload, jsave, obj, coord, map_json, register, walkable
from install_cap9b import new_map
from install_cap11b import mon, header

OD = collections.OrderedDict
FLAGS = [("FLAG_UNUSED_0x1DA", "0x1DA", "FLAG_HT_SUMMIT_DONE", "Tavinho vencido no cume da Storm Mountain"),
         ("FLAG_UNUSED_0x1DE", "0x1DE", "FLAG_HT_HIDE_SUMMIT_DOGE", "esconde o Doge no cume ate ele chegar")]
VAR = ("VAR_UNUSED_0x409B", "0x409B", "VAR_HT_EPILOGUE", "epilogo: 1 indo a Hoenn, 2 de volta ao cume, 3 fim")
TAVINHO_PARTY = header("TRAINER_MAXIE_MOSSDEEP", "TAVINHO", "Champion", "Red", "Male", "Male",
                       ["Full Restore"] * 4, "Check Bad Move / Try To Faint", "Blue") + "\n".join([
    mon("Pelipper", 87, ["Hurricane", "Hydro Pump", "Ice Beam", "U-turn"], 31, ability="Drizzle"),
    mon("Swampert", 88, ["Waterfall", "Earthquake", "Ice Punch", "Stone Edge"], 31),
    mon("Scizor", 89, ["Bullet Punch", "X-Scissor", "Close Combat", "Swords Dance"], 31, ability="Technician"),
    mon("Garchomp", 90, ["Earthquake", "Dragon Claw", "Stone Edge", "Fire Fang"], 31),
    mon("Urshifu-Rapid-Strike", 91, ["Surging Strikes", "Close Combat", "Aqua Jet", "U-turn"], 31),
    mon("Kyogre", 94, ["Origin Pulse", "Ice Beam", "Thunder", "Water Spout"], 31, "Blue Orb")])


def define(path, old, val, new, why):
    t = open(path).read()
    if new not in t:
        t, n = re.subn(r"#define %s\s+%s[^\n]*\n" % (old, val), f"#define {new:<36} {val} // {why}\n", t, count=1)
        assert n == 1, old
        open(path, "w").write(t)


def sunny_on_transition(folder, label):
    """Trilha e crista: depois do epilogo a tempestade passou."""
    p = f"{ROOT}/data/maps/{folder}/scripts.inc"
    t = open(p).read()
    if "Palm24x_Sunny" in t:
        return
    hdr = f"{folder}_MapScripts::\n"
    if f"MAP_SCRIPT_ON_TRANSITION, {label}" not in t:
        t = t.replace(hdr, hdr + f"\tmap_script MAP_SCRIPT_ON_TRANSITION, {label}\n", 1)
        t += f"\n{label}:\n\tcall_if_ge VAR_HT_EPILOGUE, 2, Palm24x_Sunny\n\tend\n"
    else:
        t = t.replace(f"{label}:\n", f"{label}:\n\tcall_if_ge VAR_HT_EPILOGUE, 2, Palm24x_Sunny\n", 1)
    t += "\n@ Palm24x_Sunny (definido no cume)\n"
    open(p, "w").write(t)


def main():
    for f in FLAGS:
        define(f"{ROOT}/include/constants/flags.h", *f)
    define(f"{ROOT}/include/constants/vars.h", *VAR)
    pp = f"{ROOT}/src/data/trainers.party"
    pt = open(pp).read()
    pat = re.compile(r"=== TRAINER_MAXIE_MOSSDEEP ===\n.*?(?=\n=== )", re.S)
    assert len(pat.findall(pt)) == 1
    open(pp, "w").write(pat.sub(lambda _m: TAVINHO_PARTY.rstrip("\n") + "\n", pt))
    # a luta multi da Mossdeep (inalcancavel) usava o slot: troca por um trainerbattle de Maxie de outro slot
    ms = f"{ROOT}/data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc"
    open(ms, "w").write(open(ms).read().replace("multi_2_vs_2 TRAINER_MAXIE_MOSSDEEP,", "multi_2_vs_2 TRAINER_MAXIE_MAGMA_HIDEOUT,"))

    # ---------------- crista -> cume
    rp = f"{ROOT}/data/maps/PalmStormRidge/map.json"
    rj = jload(rp)
    rj["connections"] = [cn for cn in rj["connections"] if cn["map"] != "MAP_PALM_STORM_SUMMIT"] + \
                        [OD([("map", "MAP_PALM_STORM_SUMMIT"), ("offset", SM.OFFSET_RIDGE), ("direction", "up")])]
    jsave(rp, rj)

    # ---------------- o cume
    c = SM.compose()
    bl = SM.flatten(c.build())
    register("PalmStormSummit", "LAYOUT_PALM_STORM_SUMMIT", c, bl)
    j = map_json("MAP_PALM_STORM_SUMMIT", "PalmStormSummit", "LAYOUT_PALM_STORM_SUMMIT", "MUS_ROUTE120", "MAPSEC_MT_CHIMNEY",
                 "MAP_TYPE_ROUTE", [OD([("map", "MAP_PALM_STORM_RIDGE"), ("offset", -SM.OFFSET_RIDGE), ("direction", "down")])])
    j["weather"] = "WEATHER_RAIN_THUNDERSTORM"
    tx, ty = SM.TAVINHO
    dx, dy = SM.DOGE_IN
    for (x, y) in [(tx, ty), (dx, dy), (tx + 1, ty + 2)]:
        assert walkable(bl, c.w, x, y), (x, y)
    tav = OD([("local_id", "LOCALID_SUMMIT_TAVINHO")] + list(obj("RED", tx, ty, "MOVEMENT_TYPE_FACE_DOWN", "Palm240_Tavinho").items()))
    dog = OD([("local_id", "LOCALID_SUMMIT_DOGE")] + list(obj("WALLACE", dx, dy, "MOVEMENT_TYPE_FACE_UP", "Palm240_Doge",
                                                                flag="FLAG_HT_HIDE_SUMMIT_DOGE").items()))
    j["object_events"] = [tav, dog]
    j["coord_events"] = [coord(x, ty + 3, "Palm240_Scene") for x in SM.SOUTH]
    jsave(f"{ROOT}/data/maps/PalmStormSummit/map.json", j)
    sc = f"""PalmStormSummit_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Palm240_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Palm240_OnFrame
	.byte 0

Palm240_OnTransition:
	call_if_lt VAR_HT_EPILOGUE, 2, Palm240_HideDoge
	call_if_ge VAR_HT_EPILOGUE, 2, Palm240_DogeHere
	call_if_ge VAR_HT_EPILOGUE, 2, Palm24x_Sunny
	end

Palm240_HideDoge::
	setflag FLAG_HT_HIDE_SUMMIT_DOGE
	return

Palm240_DogeHere::
	clearflag FLAG_HT_HIDE_SUMMIT_DOGE
	setobjectxyperm LOCALID_SUMMIT_DOGE, {tx + 1}, {ty + 1}
	setobjectmovementtype LOCALID_SUMMIT_DOGE, MOVEMENT_TYPE_FACE_DOWN
	return

Palm24x_Sunny::
	setweather WEATHER_SUNNY
	return

Palm240_OnFrame:
	map_script_2 VAR_HT_EPILOGUE, 2, Palm240_Ending
	.2byte 0

Palm240_Scene::
	goto_if_set FLAG_HT_SUMMIT_DONE, Palm240_End
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Palm240_TextIntro, MSGBOX_DEFAULT
	playmoncry SPECIES_KYOGRE, CRY_MODE_NORMAL
	waitmoncry
	msgbox Palm240_TextBattle, MSGBOX_DEFAULT
	playbgm MUS_VS_KYOGRE_GROUDON, FALSE
	trainerbattle_no_intro TRAINER_MAXIE_MOSSDEEP, Palm240_TextDefeat
	setflag FLAG_HT_SUMMIT_DONE
	msgbox Palm240_TextMedallion, MSGBOX_DEFAULT
	msgbox Palm240_TextTavinho1, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HT_HIDE_SUMMIT_DOGE
	addobject LOCALID_SUMMIT_DOGE
	applymovement LOCALID_SUMMIT_DOGE, Palm240_DogeArrives
	waitmovement 0
	msgbox Palm240_TextDoge1, MSGBOX_DEFAULT
	msgbox Palm240_TextTavinho2, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	msgbox Palm240_TextHandOver, MSGBOX_DEFAULT
	closemessage
	setvar VAR_HT_EPILOGUE, 1
	warpsilent MAP_PALM_MARINE_EPILOGUE, 12, 26
	waitstate
	releaseall
	end

Palm240_DogeArrives:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_up
	walk_in_place_faster_up
	step_end

Palm240_Ending::
	lockall
	setvar VAR_HT_EPILOGUE, 3
	delay 30
	msgbox Palm240_TextReturn, MSGBOX_DEFAULT
	msgbox Palm240_TextDoge2, MSGBOX_DEFAULT
	closemessage
	delay 30
	fadescreen FADE_TO_BLACK
	msgbox Palm240_TextFinal, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_FROM_BLACK
	releaseall
	end

Palm240_Tavinho::
	lock
	faceplayer
	goto_if_set FLAG_HT_SUMMIT_DONE, Palm240_TavinhoAfter
	release
	end

Palm240_TavinhoAfter::
	msgbox Palm240_TextTavinhoAfter, MSGBOX_DEFAULT
	release
	end

Palm240_Doge::
	lock
	faceplayer
	msgbox Palm240_TextDogeAfter, MSGBOX_DEFAULT
	release
	end

Palm240_End::
	end

Palm240_TextIntro:
	.string "x$"
Palm240_TextBattle:
	.string "x$"
Palm240_TextDefeat:
	.string "x$"
Palm240_TextMedallion:
	.string "x$"
Palm240_TextTavinho1:
	.string "x$"
Palm240_TextDoge1:
	.string "x$"
Palm240_TextTavinho2:
	.string "x$"
Palm240_TextHandOver:
	.string "x$"
Palm240_TextReturn:
	.string "x$"
Palm240_TextDoge2:
	.string "x$"
Palm240_TextFinal:
	.string "x$"
Palm240_TextTavinhoAfter:
	.string "x$"
Palm240_TextDogeAfter:
	.string "x$"
"""
    open(f"{ROOT}/data/maps/PalmStormSummit/scripts.inc", "w").write(sc)
    sunny_on_transition("PalmStormTrail", "PalmStormTrail_OnTransition")
    sunny_on_transition("PalmStormRidge", "Palm230_OnTransition")

    # ---------------- epilogo: a Caverna Marinha de Hoenn
    new_map("PalmMarineEpilogue")
    m = map_json("MAP_PALM_MARINE_EPILOGUE", "PalmMarineEpilogue", "LAYOUT_MARINE_CAVE_END", "MUS_ABNORMAL_WEATHER",
                 "MAPSEC_MARINE_CAVE", "MAP_TYPE_UNDERGROUND", [])
    m["show_map_name"] = False
    m["allow_cycling"] = m["allow_running"] = False
    kyo = OD([("local_id", "LOCALID_EPILOGUE_KYOGRE")] + list(obj("KYOGRE_FRONT", 9, 22, "MOVEMENT_TYPE_FACE_DOWN", "0x0").items()))
    dg = OD([("local_id", "LOCALID_EPILOGUE_DOGE")] + list(obj("WALLACE", 9, 27, "MOVEMENT_TYPE_FACE_UP", "0x0").items()))
    m["object_events"] = [kyo, dg]
    jsave(f"{ROOT}/data/maps/PalmMarineEpilogue/map.json", m)
    open(f"{ROOT}/data/maps/PalmMarineEpilogue/scripts.inc", "w").write(f"""PalmMarineEpilogue_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Palm241_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Palm241_OnFrame
	.byte 0

Palm241_OnTransition:
	setflag FLAG_HIDE_MAP_NAME_POPUP
	end

Palm241_OnFrame:
	map_script_2 VAR_HT_EPILOGUE, 1, Palm241_Scene
	.2byte 0

Palm241_Scene::
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Palm241_Hide
	waitmovement 0
	msgbox Palm241_TextHoenn, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_EPILOGUE_DOGE, Palm241_DogeWalk
	waitmovement 0
	playmoncry SPECIES_KYOGRE, CRY_MODE_NORMAL
	waitmoncry
	msgbox Palm241_TextDoge, MSGBOX_DEFAULT
	closemessage
	playse SE_ORB
	fadescreen FADE_TO_WHITE
	removeobject LOCALID_EPILOGUE_KYOGRE
	fadescreen FADE_FROM_WHITE
	msgbox Palm241_TextSealed, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	setvar VAR_HT_EPILOGUE, 2
	fadescreen FADE_TO_BLACK
	warpsilent MAP_PALM_STORM_SUMMIT, {tx}, {ty + 2}
	waitstate
	releaseall
	end

Palm241_Hide:
	set_invisible
	step_end

Palm241_DogeWalk:
	walk_up
	walk_in_place_faster_up
	step_end

Palm241_TextHoenn:
	.string "x$"
Palm241_TextDoge:
	.string "x$"
Palm241_TextSealed:
	.string "x$"
""")
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch12c.txt"], check=True)
    print("Cap. 12 (parte 3) instalado: cume, Tavinho, epilogo")


if __name__ == "__main__":
    main()
