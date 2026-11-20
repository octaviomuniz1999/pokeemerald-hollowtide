#!/usr/bin/env python3
"""Capitulo 8: Route 8 (MAP_PALM_ROUTE08) e Passway Village (MAP_PALM_PASSWAY), mapas novos, sem ginasio.

- a saida norte da Horizon (aberta pela Insignia do Horizonte) tem conexao continua com a Route 8, que conecta
  com a Passway; as faixas de emenda sao conferidas aqui (so primario onde o vizinho enxerga);
- Route 8 ("Encostas Antigas"): Alan, Kiyo, Cora, Auron com visao; 3 itens; mirante sobre o lago; encontros;
- Passway ("A Montanha que Espera"): fonte termal que cura, estalagem, Centro Pokemon, Mart, casa da ancia
  (o guardiao fiel: "um circulo claro como a lua sobre o peito de um cao negro"), mural com a figura do
  Medalhao de Atlas, escadaria do cume interditada pelo guardiao (so depois dos creditos: FLAG_SYS_GAME_CLEAR,
  e na historia ainda depende da convocacao do Doge), saida leste para a Route 9 fechada nesta etapa.
Rodar depois de install_chelsia_gym.py.
"""
import collections, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route8 as R8, passway as PW, horizon as HZ
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable
from install_cap7 import seam_check

OD = collections.OrderedDict
R8_TRAINERS = [(25, 41, "HIKER", "LEFT", 2, "Palm180_RouteALAN", "TRAINER_PALM_ROUTE08_ALAN"),
               (16, 29, "BLACK_BELT", "DOWN", 2, "Palm180_RouteKIYO", "TRAINER_PALM_ROUTE08_KIYO"),
               (18, 17, "EXPERT_F", "DOWN", 2, "Palm180_RouteCORA", "TRAINER_PALM_ROUTE08_CORA"),
               (22, 5, "EXPERT_M", "DOWN", 2, "Palm180_RouteAURON", "TRAINER_PALM_ROUTE08_AURON")]
R8_ITEMS = [(3, 20, "ITEM_NEVER_MELT_ICE", "FLAG_ITEM_ROUTE_119_RARE_CANDY"),          # mirante
            (29, 15, "ITEM_HYPER_POTION", "FLAG_ITEM_ROUTE_119_HYPER_POTION_1"),
            (14, 9, "ITEM_ICE_STONE", "FLAG_ITEM_ROUTE_119_SUPER_REPEL")]
R8_SIGNS = [(18, 44, "Palm180_SignSouth"), (8, 21, "Palm180_SignView"), (20, 2, "Palm180_SignNorth")]
R8_WILD = [("SPECIES_SNORUNT", 40, 42), ("SPECIES_SWINUB", 40, 42), ("SPECIES_TEDDIURSA", 40, 42), ("SPECIES_STANTLER", 40, 42),
           ("SPECIES_SNOVER", 40, 42), ("SPECIES_SNORUNT", 41, 43), ("SPECIES_SWINUB", 41, 43), ("SPECIES_TEDDIURSA", 41, 43),
           ("SPECIES_STANTLER", 41, 43), ("SPECIES_SNOVER", 41, 43), ("SPECIES_SNEASEL", 41, 43), ("SPECIES_RIOLU", 40, 42)]

PW_INTERIORS = [("pc", "MAP_FALLARBOR_TOWN_POKEMON_CENTER_1F", "FallarborTown_PokemonCenter_1F", "MAP_FALLARBOR_TOWN"),
                ("mart", "MAP_FALLARBOR_TOWN_MART", "FallarborTown_Mart", "MAP_FALLARBOR_TOWN"),
                ("inn", "MAP_PACIFIDLOG_TOWN_HOUSE1", "PacifidlogTown_House1", "MAP_PACIFIDLOG_TOWN"),
                ("elder", "MAP_SOOTOPOLIS_CITY_HOUSE7", "SootopolisCity_House7", "MAP_SOOTOPOLIS_CITY"),
                ("house", "MAP_PACIFIDLOG_TOWN_HOUSE4", "PacifidlogTown_House4", "MAP_PACIFIDLOG_TOWN")]
INTERIOR_NPCS = {  # script original -> (script novo, grafico novo ou None)
    "FallarborTown_PokemonCenter_1F_EventScript_Girl": ("Palm182_PcGirl", None),
    "FallarborTown_PokemonCenter_1F_EventScript_ExpertM": ("Palm182_PcExpert", None),
    "FallarborTown_PokemonCenter_1F_EventScript_Lanette": ("Palm182_PcWoman", None),
    "FallarborTown_Mart_EventScript_Woman": ("Palm182_MartWoman", None),
    "FallarborTown_Mart_EventScript_PokefanM": ("Palm182_MartMan", None),
    "FallarborTown_Mart_EventScript_Skitty": ("Palm182_MartSkitty", None),
    "PacifidlogTown_House1_EventScript_Man": ("Palm182_Innkeeper", None),
    "PacifidlogTown_House1_EventScript_Woman": ("Palm182_InnGuest", None),
    "SootopolisCity_House7_EventScript_OldMan": ("Palm182_Elder", "OBJ_EVENT_GFX_OLD_WOMAN"),
    "SootopolisCity_House7_EventScript_PokefanF": ("Palm182_ElderGrandkid", None),
    "PacifidlogTown_House4_EventScript_Woman": ("Palm182_HouseWoman", None),
    "PacifidlogTown_House4_EventScript_LittleGirl": ("Palm182_HouseGirl", None),
    "PacifidlogTown_House4_EventScript_Boy": ("Palm182_HouseBoy", None),
}
PW_NPCS = [  # (x, y, grafico, movimento, script)
    (19, 9, "MAN_4", "MOVEMENT_TYPE_FACE_LEFT", "Palm181_Guardian"),
    (3, 9, "OLD_MAN", "MOVEMENT_TYPE_FACE_UP", "Palm181_Watcher"),
    (21, 19, "CAMPER", "MOVEMENT_TYPE_FACE_DOWN", "Palm181_Traveler"),
    (14, 21, "LITTLE_BOY", "MOVEMENT_TYPE_WANDER_AROUND", "Palm181_Kid"),
    (30, 19, "HIKER", "MOVEMENT_TYPE_FACE_RIGHT", "Palm181_Worker"),
    (29, 10, "WOMAN_2", "MOVEMENT_TYPE_FACE_UP", "Palm181_Bather"),
]
PW_SIGNS = [(15, 20, "Palm181_TownSign"), (14, 8, "Palm181_Mural"), (16, 9, "Palm181_StairSign")]


def main():
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    old = "#define FLAG_UNUSED_0x04A    0x4A // Unused Flag"
    if "FLAG_HT_PASSWAY_EAST_OPEN" not in t:
        assert old in t
        t = t.replace(old, "#define FLAG_HT_PASSWAY_EAST_OPEN   0x4A // estrada leste da Passway liberada (Route 9)")
    open(fp, "w").write(t)

    # ---------------- Horizon: conexao norte
    hp = f"{ROOT}/data/maps/PalmHorizon/map.json"
    h = jload(hp)
    h["connections"] = [cn for cn in h["connections"] if cn["map"] != "MAP_PALM_ROUTE08"] + \
                       [OD([("map", "MAP_PALM_ROUTE08"), ("offset", R8.OFFSET_HORIZON), ("direction", "up")])]
    jsave(hp, h)

    # ---------------- Route 8
    c8 = R8.compose()
    for (x, y, _) in R8_SIGNS:
        c8.put(x, y, 3, collision=1)
    bl8 = R8.flatten(c8.build())
    seam_check(bl8, c8.w, c8.h, range(0, 7)); seam_check(bl8, c8.w, c8.h, range(c8.h - 7, c8.h))
    register("PalmRoute08", "LAYOUT_PALM_ROUTE08", c8, bl8)
    j = map_json("MAP_PALM_ROUTE08", "PalmRoute08", "LAYOUT_PALM_ROUTE08", "MUS_ROUTE113", "MAPSEC_ROUTE_108", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_HORIZON"), ("offset", -R8.OFFSET_HORIZON), ("direction", "down")]),
                  OD([("map", "MAP_PALM_PASSWAY"), ("offset", -PW.OFFSET_ROUTE8), ("direction", "up")])])
    for (x, y, gfx, d, sight, script, _) in R8_TRAINERS:
        assert walkable(bl8, c8.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in R8_ITEMS:
        assert walkable(bl8, c8.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in R8_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute08/map.json", j)
    sc = ["PalmRoute08_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in R8_TRAINERS:
        k = script.replace("Palm180_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm180_Text{k}Intro, Palm180_Text{k}Loss\n"
                  f"\tmsgbox Palm180_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s_) in R8_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute08/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Passway Village
    cp = PW.compose()
    for (x, y, _) in PW_SIGNS:
        if (x, y) != (14, 8):                     # o mural e a propria parede de rocha
            cp.put(x, y, 3, collision=1)
    blp = PW.flatten(cp.build())
    seam_check(blp, cp.w, cp.h, range(cp.h - 7, cp.h))
    register("PalmPassway", "LAYOUT_PALM_PASSWAY", cp, blp)
    j = map_json("MAP_PALM_PASSWAY", "PalmPassway", "LAYOUT_PALM_PASSWAY", "MUS_FALLARBOR", "MAPSEC_VERDANTURF_TOWN", "MAP_TYPE_TOWN",
                 [OD([("map", "MAP_PALM_ROUTE08"), ("offset", PW.OFFSET_ROUTE8), ("direction", "down")])])
    for (x, y, gfx, mv, script) in PW_NPCS:
        assert walkable(blp, cp.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, mv, script, rng=1 if "WANDER" in mv else 0))
    for (label, dm, _, _) in PW_INTERIORS:
        x, y = PW.door(label)
        j["warp_events"].append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]))
    sx, sy = PW.door("spring")
    j["coord_events"] = [coord(x, 9, "Palm181_StairGate") for x in PW.STAIRWAY] + \
                        [coord(PW.W - 2, y, "Palm181_EastGate") for y in PW.EAST]
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in PW_SIGNS] + [sign(sx, sy, "Palm181_Spring"), sign(sx + 1, sy, "Palm181_Spring")]
    jsave(f"{ROOT}/data/maps/PalmPassway/map.json", j)
    for idx, (_, _, folder, old) in enumerate(PW_INTERIORS):
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = jload(q)
        for wv in k["warp_events"]:
            if wv["dest_map"] in (old, "MAP_PALM_PASSWAY"):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_PASSWAY", str(idx)
        for o in k["object_events"]:
            if o["script"] in INTERIOR_NPCS:
                new, gfx = INTERIOR_NPCS[o["script"]]
                o["script"] = new
                if gfx:
                    o["graphics_id"] = gfx
        jsave(q, k)
    hl = f"{ROOT}/src/data/heal_locations.json"
    hj = jload(hl)
    for e in hj["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_FALLARBOR_TOWN":
            e["map"], e["x"], e["y"] = "MAP_PALM_PASSWAY", PW.door("pc")[0], PW.door("pc")[1] + 1
    jsave(hl, hj)
    sc = ["PalmPassway_MapScripts::\n\t.byte 0\n",
          "Palm181_StairGate::\n\tgoto_if_set FLAG_SYS_GAME_CLEAR, Palm181_Ok\n\tlockall\n\tmsgbox Palm181_TextStairGate, MSGBOX_DEFAULT\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm181_StepBackSouth\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm181_EastGate::\n\tgoto_if_set FLAG_HT_PASSWAY_EAST_OPEN, Palm181_Ok\n\tlockall\n\tmsgbox Palm181_TextEastGate, MSGBOX_DEFAULT\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm181_StepBackWest\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm181_Ok::\n\tend\n",
          "Palm181_StepBackSouth:\n\twalk_down\n\tstep_end\n",
          "Palm181_StepBackWest:\n\twalk_left\n\tstep_end\n",
          "Palm181_Spring::\n\tlockall\n\tmsgbox Palm181_TextSpring, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, Palm181_SpringNo\n"
          "\tfadescreen FADE_TO_BLACK\n\tplayfanfare MUS_HEAL\n\twaitfanfare\n\tspecial HealPlayerParty\n\tfadescreen FADE_FROM_BLACK\n"
          "\tmsgbox Palm181_TextSpringDone, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
          "Palm181_SpringNo::\n\treleaseall\n\tend\n"]
    for (_, _, _, _, script) in PW_NPCS:
        sc.append(f"{script}::\n\tmsgbox {script}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s_) in PW_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    for (new, _) in INTERIOR_NPCS.values():
        if new == "Palm182_MartSkitty":
            sc.append(f"{new}::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_SKITTY, CRY_MODE_NORMAL\n\tmsgbox {new}_Text, MSGBOX_DEFAULT\n"
                      "\twaitmoncry\n\trelease\n\tend\n")
        else:
            sc.append(f"{new}::\n\tmsgbox {new}_Text, MSGBOX_NPC\n\tend\n")
    open(f"{ROOT}/data/maps/PalmPassway/scripts.inc", "w").write("\n".join(sc))

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE08"]
    entry = OD([("map", "MAP_PALM_ROUTE08"), ("base_label", "gPalmRoute08"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s_)])
                                                                    for (s_, a, b) in R8_WILD])]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE07") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch8.txt"], check=True)
    print("Cap. 8 instalado: Route 8", c8.w, "x", c8.h, "| Passway", cp.w, "x", cp.h,
          "| portas", [(l, PW.door(l)) for (l, _, _, _) in PW_INTERIORS], "| fonte", (sx, sy))


if __name__ == "__main__":
    main()
