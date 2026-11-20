#!/usr/bin/env python3
"""Capitulo 10 (parte 1): Route 10 (MAP_PALM_ROUTE10, "Costa dos Farois") e Tidemouth (MAP_PALM_TIDEMOUTH).

- a saida sul de Voltara (aberta pela Insignia Circuito) tem conexao continua com a Route 10 (Voltara x = Route
  10 x + 12), e a Route 10 com Tidemouth (Tidemouth x = Route 10 x + 12); faixas de emenda conferidas;
- Route 10: praia entre o mar e as falesias, farois-guia nas pontas de pedra, enseada rasa; Tomas, Rita,
  Jonas, Luana com visao; 3 itens; encontros de terra e de surf do Cap. 10;
- Tidemouth ("A Mare Anormal", inicio): a mare alta ameaca a orla; a Nami coordena a evacuacao na avenida
  (falas do canone); hotel fechado; terminal do porto fechado ate a proxima etapa (Complexo Oceanico da
  Palm); ginasio da Nami fechado (a Nami esta na rua). Centro Pokemon, Mart, motel e casas.
Rodar depois de install_hoc_gym.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route10 as R10, tidemouth as TD, voltara as VT
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable
from install_cap7 import seam_check
from route8 import flatten as R8_flatten

OD = collections.OrderedDict
R10_TRAINERS = [(21, 18, "SAILOR", "LEFT", 2, "Palm200_RouteTOMAS", "TRAINER_PALM_ROUTE10_TOMAS"),
                (13, 26, "TUBER_F", "RIGHT", 3, "Palm200_RouteRITA", "TRAINER_PALM_ROUTE10_RITA"),
                (20, 36, "FISHERMAN", "LEFT", 2, "Palm200_RouteJONAS", "TRAINER_PALM_ROUTE10_JONAS"),
                (22, 48, "SWIMMER_F", "LEFT", 2, "Palm200_RouteLUANA", "TRAINER_PALM_ROUTE10_LUANA")]
R10_ITEMS = [(6, 21, "ITEM_DEEP_SEA_SCALE", "FLAG_ITEM_ROUTE_110_RARE_CANDY"),   # farol norte
             (7, 42, "ITEM_DAMP_ROCK", "FLAG_ITEM_ROUTE_110_DIRE_HIT"),                  # farol sul
             (26, 22, "ITEM_MAX_REPEL", "FLAG_ITEM_ROUTE_111_STARDUST")]                 # restinga
R10_SIGNS = [(20, 4, "Palm200_SignNorth"), (21, 54, "Palm200_SignSouth"), (8, 23, "Palm200_SignBeacon")]
R10_WILD = [("SPECIES_WINGULL", 46, 48), ("SPECIES_LOMBRE", 46, 48), ("SPECIES_PELIPPER", 47, 49), ("SPECIES_WINGULL", 46, 48),
            ("SPECIES_LOMBRE", 47, 49), ("SPECIES_KRABBY", 46, 48), ("SPECIES_KINGLER", 48, 50), ("SPECIES_CORPHISH", 46, 48),
            ("SPECIES_PELIPPER", 48, 50), ("SPECIES_KRABBY", 47, 49), ("SPECIES_LUDICOLO", 49, 50), ("SPECIES_CRAWDAUNT", 49, 50)]
R10_WATER = [("SPECIES_TENTACRUEL", 46, 50), ("SPECIES_WAILMER", 46, 50), ("SPECIES_MANTINE", 47, 50), ("SPECIES_PELIPPER", 47, 50),
             ("SPECIES_LAPRAS", 48, 50)]

TD_INTERIORS = [("pc", "MAP_PACIFIDLOG_TOWN_POKEMON_CENTER_1F", "PacifidlogTown_PokemonCenter_1F", "MAP_PACIFIDLOG_TOWN"),
                ("mart", "MAP_SOOTOPOLIS_CITY_MART", "SootopolisCity_Mart", "MAP_SOOTOPOLIS_CITY"),
                ("motel", "MAP_LILYCOVE_CITY_COVE_LILY_MOTEL_1F", "LilycoveCity_CoveLilyMotel_1F", "MAP_LILYCOVE_CITY"),
                ("house_1", "MAP_SOOTOPOLIS_CITY_HOUSE2", "SootopolisCity_House2", "MAP_SOOTOPOLIS_CITY"),
                ("house_2", "MAP_SOOTOPOLIS_CITY_HOUSE4", "SootopolisCity_House4", "MAP_SOOTOPOLIS_CITY")]
INTERIOR_NPCS = {
    "PacifidlogTown_PokemonCenter_1F_EventScript_OldMan": "Palm202_PcOldMan",
    "PacifidlogTown_PokemonCenter_1F_EventScript_Girl": "Palm202_PcGirl",
    "PacifidlogTown_PokemonCenter_1F_EventScript_Woman": "Palm202_PcWoman",
    "SootopolisCity_Mart_EventScript_FatMan": "Palm202_MartMan",
    "SootopolisCity_Mart_EventScript_Gentleman": "Palm202_MartGent",
    "LilycoveCity_CoveLilyMotel_1F_EventScript_MotelOwner": "Palm202_MotelOwner",
    "SootopolisCity_House2_EventScript_ExpertF": "Palm202_House1Woman",
    "SootopolisCity_House4_EventScript_Man": "Palm202_House2Man",
    "SootopolisCity_House4_EventScript_Woman": "Palm202_House2Woman",
    "SootopolisCity_House4_EventScript_Azumarill": "Palm202_House2Azumarill",
}
TD_NPCS = [  # (x, y, grafico, movimento, script, flag de sumir)
    (31, 18, "WOMAN_5", "MOVEMENT_TYPE_FACE_UP", "Palm201_Nami", "0"),
    (24, 19, "SAILOR", "MOVEMENT_TYPE_FACE_DOWN", "Palm201_Sailor", "0"),
    (10, 18, "WOMAN_2", "MOVEMENT_TYPE_WANDER_AROUND", "Palm201_Tourist", "0"),
    (46, 18, "MAN_3", "MOVEMENT_TYPE_FACE_DOWN", "Palm201_HotelClerk", "0"),
    (35, 38, "SAILOR", "MOVEMENT_TYPE_FACE_LEFT", "Palm201_PortGuard", "0"),
    (16, 28, "MAN_2", "MOVEMENT_TYPE_FACE_UP", "Palm201_GymGuard", "0"),
    (50, 38, "LITTLE_BOY", "MOVEMENT_TYPE_WANDER_AROUND", "Palm201_Kid", "0"),
    (8, 29, "OLD_WOMAN", "MOVEMENT_TYPE_FACE_DOWN", "Palm201_OldWoman", "0"),
]
TD_SIGNS = [(29, 8, "Palm201_TownSign"), (39, 14, "Palm201_HotelSign"), (29, 37, "Palm201_PortSign"), (13, 27, "Palm201_GymSign")]


def main():
    # ---------------- Voltara: faixa sul so primario (refeita no compose) + conexao com a Route 10
    vp = f"{ROOT}/data/maps/PalmVoltara/map.json"
    v = jload(vp)
    v["connections"] = [cn for cn in v["connections"] if cn["map"] != "MAP_PALM_ROUTE10"] + \
                       [OD([("map", "MAP_PALM_ROUTE10"), ("offset", VT.OFFSET_ROUTE10), ("direction", "down")])]
    jsave(vp, v)
    import struct
    L = {l["id"]: l for l in jload(f"{ROOT}/data/layouts/layouts.json")["layouts"] if "id" in l}
    lv = L["LAYOUT_PALM_VOLTARA"]
    vbl = struct.unpack(f"<{lv['width'] * lv['height']}H", open(f"{ROOT}/{lv['blockdata_filepath']}", "rb").read())
    seam_check(vbl, VT.W, VT.H, range(VT.H - 7, VT.H), range(VT.OFFSET_ROUTE10, VT.OFFSET_ROUTE10 + R10.W))

    # ---------------- Route 10
    c = R10.compose()
    for (x, y, _) in R10_SIGNS:
        c.put(x, y, 3, collision=1)
    bl = c.build()
    seam_check(bl, c.w, c.h, range(0, 7))
    register("PalmRoute10", "LAYOUT_PALM_ROUTE10", c, bl)
    j = map_json("MAP_PALM_ROUTE10", "PalmRoute10", "LAYOUT_PALM_ROUTE10", "MUS_ROUTE104", "MAPSEC_ROUTE_110", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_VOLTARA"), ("offset", -VT.OFFSET_ROUTE10), ("direction", "up")]),
                  OD([("map", "MAP_PALM_TIDEMOUTH"), ("offset", TD.OFFSET_ROUTE10), ("direction", "down")])])
    for (x, y, gfx, d, sight, script, _) in R10_TRAINERS:
        assert walkable(bl, c.w, x, y) and c.terrain[y][x] not in ("sea", "shallow"), (script, x, y, c.terrain[y][x])
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in R10_ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in R10_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute10/map.json", j)
    sc = ["PalmRoute10_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in R10_TRAINERS:
        k = script.replace("Palm200_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm200_Text{k}Intro, Palm200_Text{k}Loss\n"
                  f"\tmsgbox Palm200_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s_) in R10_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute10/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Tidemouth
    ct = TD.compose()
    for (x, y, _) in TD_SIGNS:
        ct.put(x, y, 3, collision=1)
    blt = R8_flatten(ct.build())          # o carimbo do pavilhao (ginasio) vem com o patamar da Lilycove: piso andavel no nivel da rua
    register("PalmTidemouth", "LAYOUT_PALM_TIDEMOUTH", ct, blt)
    j = map_json("MAP_PALM_TIDEMOUTH", "PalmTidemouth", "LAYOUT_PALM_TIDEMOUTH", "MUS_SLATEPORT", "MAPSEC_MOSSDEEP_CITY", "MAP_TYPE_CITY",
                 [OD([("map", "MAP_PALM_ROUTE10"), ("offset", -TD.OFFSET_ROUTE10), ("direction", "up")])])
    j["weather"] = "WEATHER_RAIN"
    for (x, y, gfx, mv, script, flag) in TD_NPCS:
        assert walkable(blt, ct.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, mv, script, flag=flag, rng=1 if "WANDER" in mv else 0))
    for (label, dm, _, _) in TD_INTERIORS:
        x, y = TD.door(label)
        j["warp_events"].append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]))
    px, py = TD.door("terminal")
    gx, gy = TD.door("gym")
    j["coord_events"] = [coord(px, py + 1, "Palm201_PortLock"), coord(gx, gy + 1, "Palm201_GymLock")]
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in TD_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmTidemouth/map.json", j)
    for idx, (_, _, folder, old) in enumerate(TD_INTERIORS):
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = jload(q)
        k["warp_events"] = [wv for wv in k["warp_events"] if "MOTEL_2F" not in wv["dest_map"]]      # motel: so o terreo
        for wv in k["warp_events"]:
            if wv["dest_map"] in (old, "MAP_PALM_TIDEMOUTH"):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_TIDEMOUTH", str(idx)
        for o in k["object_events"]:
            if o["script"] in INTERIOR_NPCS:
                o["script"] = INTERIOR_NPCS[o["script"]]
        jsave(q, k)
    hl = f"{ROOT}/src/data/heal_locations.json"
    hj = jload(hl)
    for e in hj["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_PACIFIDLOG_TOWN":
            e["map"], e["x"], e["y"] = "MAP_PALM_TIDEMOUTH", TD.door("pc")[0], TD.door("pc")[1] + 1
    jsave(hl, hj)
    sc = ["PalmTidemouth_MapScripts::\n\t.byte 0\n",
          "Palm201_Nami::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_TIDEMOUTH_NAMI_MET, Palm201_NamiAgain\n"
          "\tmsgbox Palm201_TextNami, MSGBOX_DEFAULT\n\tsetflag FLAG_HT_TIDEMOUTH_NAMI_MET\n\trelease\n\tend\n",
          "Palm201_NamiAgain::\n\tmsgbox Palm201_TextNamiAgain, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm201_PortLock::\n\tlockall\n\tmsgbox Palm201_TextPortLock, MSGBOX_DEFAULT\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm201_StepBackSouth\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm201_GymLock::\n\tlockall\n\tmsgbox Palm201_TextGymLock, MSGBOX_DEFAULT\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm201_StepBackSouth\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm201_StepBackNorth:\n\twalk_up\n\tstep_end\n", "Palm201_StepBackSouth:\n\twalk_down\n\tstep_end\n"]
    for (_, _, _, _, script, _) in TD_NPCS:
        if script != "Palm201_Nami":
            sc.append(f"{script}::\n\tmsgbox {script}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s_) in TD_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    for new in INTERIOR_NPCS.values():
        if new == "Palm202_House2Azumarill":
            sc.append(f"{new}::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_AZUMARILL, CRY_MODE_NORMAL\n\tmsgbox {new}_Text, MSGBOX_DEFAULT\n"
                      "\twaitmoncry\n\trelease\n\tend\n")
        else:
            sc.append(f"{new}::\n\tmsgbox {new}_Text, MSGBOX_NPC\n\tend\n")
    open(f"{ROOT}/data/maps/PalmTidemouth/scripts.inc", "w").write("\n".join(sc))

    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    old = "#define FLAG_UNUSED_0x054                    0x54  // Unused Flag"
    if "FLAG_HT_TIDEMOUTH_NAMI_MET" not in t:
        assert old in t, old
        t = t.replace(old, "#define FLAG_HT_TIDEMOUTH_NAMI_MET           0x54  // Nami recebeu o jogador na evacuacao")
    open(fp, "w").write(t)

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE10"]
    mons = lambda L_: [OD([("min_level", a), ("max_level", b), ("species", s_)]) for (s_, a, b) in L_]
    entry = OD([("map", "MAP_PALM_ROUTE10"), ("base_label", "gPalmRoute10"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", mons(R10_WILD))])),
                ("water_mons", OD([("encounter_rate", 4), ("mons", mons(R10_WATER))]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE09") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch10.txt"], check=True)
    print("Cap. 10 (parte 1) instalado: Route 10", c.w, "x", c.h, "| Tidemouth", ct.w, "x", ct.h,
          "| portas", [(l, TD.door(l)) for (l, _, _, _) in TD_INTERIORS], "| terminal", (px, py), "| ginasio", (gx, gy))


if __name__ == "__main__":
    main()
