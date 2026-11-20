#!/usr/bin/env python3
"""Capitulo 9 (parte 2): Voltara (MAP_PALM_VOLTARA) e o Centro de Dados da Team Palm
(MAP_PALM_DATA_CENTER_1F/2F, sobre os layouts do Space Center de Mossdeep).

- o portao leste da Route 9 abre (Voltara existe): conexao continua Route 9 <-> Voltara (offset 0);
- Voltara sem energia: Hoc recebe o jogador na frente da estacao (as falas do cânone; Riven achou um padrao
  nos registros, "alguma coisa esta respondendo de muito longe"); o Centro de Dados so abre depois;
- Centro de Dados: 2 recrutas no saguao (1F); no 2F, o admin Vega (Magneton 43, Porygon2 44, Eelektrik 45)
  defende 3 retransmissores; com o Vega derrotado e os 3 desligados, a energia volta, a ferrovia
  Ferralia-Tradepost-Voltara pode voltar a funcionar e o Hoc abre o ginasio (o ginasio entra na parte 3);
- Centro Pokemon, Mart e casas (interiores de Mauville com moradores novos); saida sul fechada ate a 7a
  insignia. Rodar depois de install_cap9.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import voltara as VT, route9 as R9
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable
from install_cap7 import seam_check

OD = collections.OrderedDict
VT_INTERIORS = [("pc", "MAP_MAUVILLE_CITY_POKEMON_CENTER_1F", "MauvilleCity_PokemonCenter_1F", "MAP_MAUVILLE_CITY"),
                ("mart", "MAP_MAUVILLE_CITY_MART", "MauvilleCity_Mart", "MAP_MAUVILLE_CITY"),
                ("house_1", "MAP_MAUVILLE_CITY_HOUSE1", "MauvilleCity_House1", "MAP_MAUVILLE_CITY"),
                ("house_2", "MAP_MAUVILLE_CITY_HOUSE2", "MauvilleCity_House2", "MAP_MAUVILLE_CITY"),
                ("datacenter", "MAP_PALM_DATA_CENTER_1F", "PalmDataCenter1F", None)]
INTERIOR_NPCS = {
    "MauvilleCity_PokemonCenter_1F_EventScript_Woman1": "Palm192_PcWoman1",
    "MauvilleCity_PokemonCenter_1F_EventScript_Woman2": "Palm192_PcWoman2",
    "MauvilleCity_PokemonCenter_1F_EventScript_Youngster": "Palm192_PcBoy",
    "MauvilleCity_Mart_EventScript_ExpertM": "Palm192_MartExpert",
    "MauvilleCity_Mart_EventScript_Man": "Palm192_MartMan",
    "MauvilleCity_House1_EventScript_RockSmashDude": "Palm192_House1Man",
    "MauvilleCity_House2_EventScript_Woman": "Palm192_House2Woman",
}
DROP_NPCS = {"MauvilleCity_PokemonCenter_1F_EventScript_MauvilleOldMan"}
VT_NPCS = [  # (x, y, grafico, movimento, script, flag de sumir)
    (27, 18, "MAN_4", "MOVEMENT_TYPE_FACE_DOWN", "Palm191_Hoc", "FLAG_HT_VOLTARA_DONE"),
    (12, 20, "WORKER_M", "MOVEMENT_TYPE_FACE_UP", "Palm191_Worker", "0"),
    (40, 20, "SCIENTIST_1", "MOVEMENT_TYPE_FACE_UP", "Palm191_Scientist", "0"),
    (20, 26, "LITTLE_GIRL", "MOVEMENT_TYPE_WANDER_AROUND", "Palm191_Girl", "0"),
    (49, 17, "AQUA_MEMBER_M", "MOVEMENT_TYPE_FACE_DOWN", "Palm191_DoorGrunt", "FLAG_HT_VOLTARA_HOC_MET"),
    (32, 40, "MAN_2", "MOVEMENT_TYPE_FACE_UP", "Palm191_SouthGuard", "0"),
    (50, 37, "OLD_MAN", "MOVEMENT_TYPE_FACE_DOWN", "Palm191_OldMan", "0"),
]
VT_SIGNS = [(3, 17, "Palm191_TownSign"), (31, 17, "Palm191_StationSign"), (52, 17, "Palm191_DataSign"), (36, 30, "Palm191_GymSign")]
DC1_GRUNTS = [(8, 4, "AQUA_MEMBER_M", "DOWN", 4, "Palm193_Grunt1", "TRAINER_PALM_DATA_GRUNT_1"),
              (13, 4, "AQUA_MEMBER_F", "UP", 2, "Palm193_Grunt2", "TRAINER_PALM_DATA_GRUNT_2")]
DC2_VEGA = (12, 5)
RELAYS = [((2, 7), "FLAG_HT_VOLTARA_RELAY_1"), ((5, 7), "FLAG_HT_VOLTARA_RELAY_2"), ((8, 7), "FLAG_HT_VOLTARA_RELAY_3")]


def new_map(name):
    os.makedirs(f"{ROOT}/data/maps/{name}", exist_ok=True)
    mg = jload(f"{ROOT}/data/maps/map_groups.json")
    if name not in mg["gMapGroup_TownsAndRoutes"]:
        mg["gMapGroup_TownsAndRoutes"].append(name)
        jsave(f"{ROOT}/data/maps/map_groups.json", mg)
    es = f"{ROOT}/data/event_scripts.s"
    t = open(es).read()
    inc = f'\t.include "data/maps/{name}/scripts.inc"\n'
    if inc not in t:
        anchor = '\t.include "data/maps/PalmFerralia/scripts.inc"\n'
        t = t.replace(anchor, anchor + inc)
        open(es, "w").write(t)


def main():
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    for (n, v, cm) in [("FLAG_HT_VOLTARA_HOC_MET", 0x4B, "Hoc recebeu o jogador na estacao"),
                       ("FLAG_HT_VOLTARA_RELAY_1", 0x4C, "retransmissor 1 desligado"),
                       ("FLAG_HT_VOLTARA_RELAY_2", 0x4D, "retransmissor 2 desligado"),
                       ("FLAG_HT_VOLTARA_RELAY_3", 0x4E, "retransmissor 3 desligado"),
                       ("FLAG_HT_VOLTARA_DONE", 0x4F, "Vega derrotado e retransmissores desligados: energia de volta")]:
        old = f"#define FLAG_UNUSED_0x{v:03X}    0x{v:X} // Unused Flag"
        if n not in t:
            assert old in t, old
            t = t.replace(old, f"#define {n:<27} 0x{v:X} // {cm}")
    open(fp, "w").write(t)

    # ---------------- Route 9: portao leste abre, conexao com Voltara
    rp = f"{ROOT}/data/maps/PalmRoute09/map.json"
    r = jload(rp)
    r["coord_events"] = [e for e in r["coord_events"] if e["script"] != "Palm190_EastGate"]
    r["connections"] = [cn for cn in r["connections"] if cn["map"] != "MAP_PALM_VOLTARA"] + \
                       [OD([("map", "MAP_PALM_VOLTARA"), ("offset", 0), ("direction", "right")])]
    jsave(rp, r)

    # ---------------- Voltara
    cv = VT.compose()
    for (x, y, _) in VT_SIGNS:
        cv.put(x, y, 3, collision=1)
    blv = cv.build()
    register("PalmVoltara", "LAYOUT_PALM_VOLTARA", cv, blv)
    j = map_json("MAP_PALM_VOLTARA", "PalmVoltara", "LAYOUT_PALM_VOLTARA", "MUS_VERDANTURF", "MAPSEC_FORTREE_CITY", "MAP_TYPE_CITY",
                 [OD([("map", "MAP_PALM_ROUTE09"), ("offset", 0), ("direction", "left")])])
    j["weather"] = "WEATHER_SHADE"
    for (x, y, gfx, mv, script, flag) in VT_NPCS:
        assert walkable(blv, cv.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, mv, script, flag=flag, rng=1 if "WANDER" in mv else 0))
    for (label, dm, _, _) in VT_INTERIORS:
        x, y = VT.door(label)
        j["warp_events"].append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]))
    dx, dy = VT.door("datacenter")
    j["coord_events"] = [coord(dx, dy + 1, "Palm191_DataLock")] + [coord(x, VT.H - 3, "Palm191_SouthGate") for x in VT.SOUTH]
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in VT_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmVoltara/map.json", j)
    for idx, (_, _, folder, old) in enumerate(VT_INTERIORS):
        if old is None:
            continue
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = jload(q)
        for wv in k["warp_events"]:
            if wv["dest_map"] in (old, "MAP_PALM_VOLTARA"):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_VOLTARA", str(idx)
        k["object_events"] = [o for o in k["object_events"] if o["script"] not in DROP_NPCS]
        for o in k["object_events"]:
            if o["script"] in INTERIOR_NPCS:
                o["script"] = INTERIOR_NPCS[o["script"]]
        jsave(q, k)
    hl = f"{ROOT}/src/data/heal_locations.json"
    hj = jload(hl)
    for e in hj["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_MAUVILLE_CITY":
            e["map"], e["x"], e["y"] = "MAP_PALM_VOLTARA", VT.door("pc")[0], VT.door("pc")[1] + 1
    jsave(hl, hj)
    gx, gy = VT.door("gym")
    wall_mt = blv[gy * cv.w + gx - 1] & 0x3FF
    sc = ["PalmVoltara_MapScripts::\n\tmap_script MAP_SCRIPT_ON_LOAD, Palm191_Load\n\t.byte 0\n",
          f"Palm191_Load::\n\tsetmetatile {gx}, {gy}, {wall_mt}, TRUE\n\tend\n",              # ginasio do Hoc: parte 3
          "Palm191_Hoc::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_VOLTARA_HOC_MET, Palm191_HocAgain\n"
          "\tmsgbox Palm191_TextHoc, MSGBOX_DEFAULT\n\tsetflag FLAG_HT_VOLTARA_HOC_MET\n\trelease\n\tend\n",
          "Palm191_HocAgain::\n\tmsgbox Palm191_TextHocAgain, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm191_DataLock::\n\tgoto_if_set FLAG_HT_VOLTARA_HOC_MET, Palm191_Ok\n\tlockall\n\tmsgbox Palm191_TextDataLock, MSGBOX_DEFAULT\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm191_StepBackSouth\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm191_SouthGate::\n\tgoto_if_set FLAG_BADGE07_GET, Palm191_Ok\n\tlockall\n\tmsgbox Palm191_TextSouthGate, MSGBOX_DEFAULT\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm191_StepBackNorth\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm191_Ok::\n\tend\n", "Palm191_StepBackSouth:\n\twalk_down\n\tstep_end\n", "Palm191_StepBackNorth:\n\twalk_up\n\tstep_end\n",
          "Palm191_Worker::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_VOLTARA_DONE, Palm191_WorkerDone\n"
          "\tmsgbox Palm191_Worker_Text, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm191_WorkerDone::\n\tmsgbox Palm191_Worker_TextDone, MSGBOX_DEFAULT\n\trelease\n\tend\n"]
    for script in ("Palm191_Scientist", "Palm191_Girl", "Palm191_DoorGrunt", "Palm191_SouthGuard", "Palm191_OldMan"):
        sc.append(f"{script}::\n\tmsgbox {script}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s_) in VT_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    for new in INTERIOR_NPCS.values():
        sc.append(f"{new}::\n\tmsgbox {new}_Text, MSGBOX_NPC\n\tend\n")
    open(f"{ROOT}/data/maps/PalmVoltara/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Centro de Dados (1F saguao, 2F servidores)
    for name in ("PalmDataCenter1F", "PalmDataCenter2F"):
        new_map(name)
    dc_idx = [i for i, (l, _, _, _) in enumerate(VT_INTERIORS) if l == "datacenter"][0]
    j1 = map_json("MAP_PALM_DATA_CENTER_1F", "PalmDataCenter1F", "LAYOUT_MOSSDEEP_CITY_SPACE_CENTER_1F", "MUS_AQUA_MAGMA_HIDEOUT",
                  "MAPSEC_FORTREE_CITY", "MAP_TYPE_INDOOR", [])
    j1.update({"weather": "WEATHER_NONE", "allow_cycling": False, "show_map_name": False})
    j1["warp_events"] = [OD([("x", 7), ("y", 9), ("elevation", 0), ("dest_map", "MAP_PALM_VOLTARA"), ("dest_warp_id", str(dc_idx))]),
                         OD([("x", 8), ("y", 9), ("elevation", 0), ("dest_map", "MAP_PALM_VOLTARA"), ("dest_warp_id", str(dc_idx))]),
                         OD([("x", 13), ("y", 1), ("elevation", 0), ("dest_map", "MAP_PALM_DATA_CENTER_2F"), ("dest_warp_id", "0")])]
    for (x, y, gfx, d, sight, script, _) in DC1_GRUNTS:
        j1["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    j1["bg_events"] = [sign(3, 6, "Palm193_Screen"), sign(11, 8, "Palm193_Screen")]
    jsave(f"{ROOT}/data/maps/PalmDataCenter1F/map.json", j1)
    j2 = map_json("MAP_PALM_DATA_CENTER_2F", "PalmDataCenter2F", "LAYOUT_MOSSDEEP_CITY_SPACE_CENTER_2F", "MUS_AQUA_MAGMA_HIDEOUT",
                  "MAPSEC_FORTREE_CITY", "MAP_TYPE_INDOOR", [])
    j2.update({"weather": "WEATHER_NONE", "allow_cycling": False, "show_map_name": False})
    j2["warp_events"] = [OD([("x", 13), ("y", 1), ("elevation", 0), ("dest_map", "MAP_PALM_DATA_CENTER_1F"), ("dest_warp_id", "2")])]
    j2["object_events"] = [obj("AQUA_MEMBER_M", DC2_VEGA[0], DC2_VEGA[1], "MOVEMENT_TYPE_FACE_RIGHT", "Palm193_Vega",
                               "TRAINER_TYPE_NORMAL", 1)]
    j2["bg_events"] = [sign(x, y, f"Palm193_Relay{i + 1}") for i, ((x, y), _) in enumerate(RELAYS)] + [sign(11, 7, "Palm193_Log")]
    jsave(f"{ROOT}/data/maps/PalmDataCenter2F/map.json", j2)
    sc1 = ["PalmDataCenter1F_MapScripts::\n\t.byte 0\n",
           "Palm193_Screen::\n\tmsgbox Palm193_TextScreen, MSGBOX_SIGN\n\tend\n"]
    for (_, _, _, _, _, script, tid) in DC1_GRUNTS:
        k = script.replace("Palm193_", "")
        sc1.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm193_Text{k}Intro, Palm193_Text{k}Loss\n"
                   f"\tmsgbox Palm193_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    open(f"{ROOT}/data/maps/PalmDataCenter1F/scripts.inc", "w").write("\n".join(sc1))
    relay_flags = [f for (_, f) in RELAYS]
    sc2 = ["PalmDataCenter2F_MapScripts::\n\t.byte 0\n",
           "Palm193_Vega::\n\ttrainerbattle_single TRAINER_PALM_VEGA, Palm193_TextVegaIntro, Palm193_TextVegaLoss\n"
           "\tmsgbox Palm193_TextVegaAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
           "Palm193_Log::\n\tmsgbox Palm193_TextLog, MSGBOX_SIGN\n\tend\n"]
    for i, (_, flag) in enumerate(RELAYS, 1):
        sc2.append(f"Palm193_Relay{i}::\n\tlockall\n\tgoto_if_set {flag}, Palm193_RelayOff\n"
                   "\tgoto_if_not_defeated TRAINER_PALM_VEGA, Palm193_RelayGuarded\n"
                   f"\tmsgbox Palm193_TextRelay, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, Palm193_Release\n\tsetflag {flag}\n"
                   "\tplayse SE_PC_OFF\n\twaitse\n\tmsgbox Palm193_TextRelayDown, MSGBOX_DEFAULT\n\tgoto Palm193_CheckDone\n")
    sc2.append("Palm193_CheckDone::\n" + "".join(f"\tgoto_if_unset {f}, Palm193_Release\n" for f in relay_flags)
               + "\tsetflag FLAG_HT_VOLTARA_DONE\n\tplayse SE_SUCCESS\n\tmsgbox Palm193_TextPowerBack, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc2.append("Palm193_RelayOff::\n\tmsgbox Palm193_TextRelayIsOff, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc2.append("Palm193_RelayGuarded::\n\tmsgbox Palm193_TextRelayGuarded, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc2.append("Palm193_Release::\n\treleaseall\n\tend\n")
    open(f"{ROOT}/data/maps/PalmDataCenter2F/scripts.inc", "w").write("\n".join(sc2))
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch9b.txt"], check=True)
    print("Cap. 9 (parte 2) instalado: Voltara", cv.w, "x", cv.h, "| portas", [(l, VT.door(l)) for (l, _, _, _) in VT_INTERIORS])


if __name__ == "__main__":
    main()
