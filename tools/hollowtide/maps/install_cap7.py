#!/usr/bin/env python3
"""Capitulo 7 (parte 1): Route 7 (MAP_PALM_ROUTE07), Horizon City (MAP_PALM_HORIZON) e a estacao sob o lago
(MAP_PALM_LAKE_STATION, layout do esconderijo da Aqua B2F: tanques e maquinas).

- Serenia ganha a saida norte (trava ate a Insignia da Serenidade) e conexao continua com a Route 7, que
  conecta com a Horizon City (as faixas de emenda so usam o primario — conferido aqui);
- Route 7 ("Caminho dos Espelhos"): Henry, Connie, Celia, Colin; 3 itens; encontros do Cap. 7;
- Horizon ("As Aguas do Horizonte"): o lago sobe sem chuva e alagou o jardim da orla. Chelsia e o Piplup
  estao na orla; o Piplup aponta a estacao de controle do lago. Na estacao: 3 recrutas da Team Palm, 3
  amplificadores (desligar), 3 Pokemon presos em redes (soltar) e o terminal com o registro
  "EXTERNAL SOURCE / NORTH / IRREGULAR SIGNAL". Ao terminar, a agua baixa (o jardim volta ao normal).
  Ginasio da Chelsia fechado nesta etapa; saida norte (Route 8) fechada ate a 6a insignia.
Rodar depois de install_jade_gym.py.
"""
import collections, json, os, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route7 as R7, horizon as HZ, serenia as SE
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable

OD = collections.OrderedDict
R7_TRAINERS = [(15, 22, "FISHERMAN", "RIGHT", 1, "Palm160_RouteHENRY", "TRAINER_PALM_ROUTE07_HENRY"),
               (19, 30, "BEAUTY", "LEFT", 2, "Palm160_RouteCONNIE", "TRAINER_PALM_ROUTE07_CONNIE"),
               (26, 45, "PICNICKER", "LEFT", 5, "Palm160_RouteCELIA", "TRAINER_PALM_ROUTE07_CELIA"),
               (30, 15, "MAN_5", "LEFT", 3, "Palm160_RouteCOLIN", "TRAINER_PALM_ROUTE07_COLIN")]
R7_ITEMS = [(29, 11, "ITEM_MOON_STONE", "FLAG_ITEM_ROUTE_119_ZINC"),            # no meio do Circulo da Lua
            (4, 47, "ITEM_MYSTIC_WATER", "FLAG_ITEM_ROUTE_119_ELIXIR_1"),       # margem sul do lago
            (32, 30, "ITEM_PIXIE_PLATE", "FLAG_ITEM_ROUTE_119_LEAF_STONE")]     # mato alto leste
R7_SIGNS = [(22, 52, "Palm160_SignSouth"), (18, 3, "Palm160_SignNorth"), (25, 15, "Palm160_SignCircle")]
R7_WILD = [("SPECIES_CLEFAIRY", 36, 38), ("SPECIES_SWABLU", 36, 38), ("SPECIES_FLABEBE", 36, 38), ("SPECIES_SPRITZEE", 36, 38),
           ("SPECIES_SWIRLIX", 36, 38), ("SPECIES_SWABLU", 37, 39), ("SPECIES_CLEFAIRY", 37, 39), ("SPECIES_FLABEBE", 37, 39),
           ("SPECIES_SPRITZEE", 37, 39), ("SPECIES_SWIRLIX", 37, 39), ("SPECIES_TOGEPI", 36, 38), ("SPECIES_TOGEPI", 38, 39)]
R7_WATER = [("SPECIES_PSYDUCK", 35, 38), ("SPECIES_MARILL", 35, 38), ("SPECIES_GOLDEEN", 35, 38), ("SPECIES_AZUMARILL", 38, 40),
            ("SPECIES_GOLDUCK", 38, 40)]
R7_FISH = [("SPECIES_MAGIKARP", 10, 15), ("SPECIES_GOLDEEN", 10, 15), ("SPECIES_GOLDEEN", 25, 30), ("SPECIES_MAGIKARP", 25, 30),
           ("SPECIES_FEEBAS", 25, 30), ("SPECIES_GOLDEEN", 35, 38), ("SPECIES_SEAKING", 36, 40), ("SPECIES_FEEBAS", 30, 35),
           ("SPECIES_GOLDEEN", 35, 40), ("SPECIES_SEAKING", 38, 42)]

HZ_INTERIORS = [("pc", "MAP_MOSSDEEP_CITY_POKEMON_CENTER_1F", "MossdeepCity_PokemonCenter_1F", "MAP_MOSSDEEP_CITY"),
                ("mart", "MAP_MOSSDEEP_CITY_MART", "MossdeepCity_Mart", "MAP_MOSSDEEP_CITY"),
                ("house_1", "MAP_MOSSDEEP_CITY_HOUSE1", "MossdeepCity_House1", "MAP_MOSSDEEP_CITY"),
                ("house_2", "MAP_MOSSDEEP_CITY_HOUSE3", "MossdeepCity_House3", "MAP_MOSSDEEP_CITY"),   # pescador da Super Rod
                ("house_3", "MAP_MOSSDEEP_CITY_HOUSE4", "MossdeepCity_House4", "MAP_MOSSDEEP_CITY"),
                ("station", "MAP_PALM_LAKE_STATION", "PalmLakeStation", None)]
# moradores dos interiores emprestados: script original -> script novo (o resto do mapa fica igual)
INTERIOR_NPCS = {
    "MossdeepCity_PokemonCenter_1F_EventScript_Woman": "Palm171_PcWoman",
    "MossdeepCity_PokemonCenter_1F_EventScript_Girl": "Palm171_PcGirl",
    "MossdeepCity_Mart_EventScript_Woman": "Palm171_MartWoman",
    "MossdeepCity_Mart_EventScript_Boy": "Palm171_MartBoy",
    "MossdeepCity_Mart_EventScript_Sailor": "Palm171_MartSailor",
    "MossdeepCity_House1_EventScript_BlackBelt": "Palm171_House1Man",
    "MossdeepCity_House1_EventScript_Woman": "Palm171_House1Woman",
    "MossdeepCity_House4_EventScript_Woman": "Palm171_House3Woman",
    "MossdeepCity_House4_EventScript_NinjaBoy": "Palm171_House3Boy",
    "MossdeepCity_House4_EventScript_Skitty": "Palm171_House3Skitty",
}
HZ_NPCS = [  # (x, y, grafico, movimento, script, flag de sumir)
    (24, 20, "ANABEL", "MOVEMENT_TYPE_FACE_UP", "Palm170_Chelsia", "FLAG_HT_HORIZON_CHELSIA_MET"),
    (25, 20, "OBJ_EVENT_GFX_SPECIES(PIPLUP)", "MOVEMENT_TYPE_FACE_UP", "Palm170_Piplup", "FLAG_HT_HORIZON_CHELSIA_MET"),
    (8, 21, "OLD_MAN", "MOVEMENT_TYPE_FACE_UP", "Palm170_OldMan", "0"),
    (40, 21, "FISHERMAN", "MOVEMENT_TYPE_FACE_UP", "Palm170_Fisher", "0"),
    (47, 15, "SCIENTIST_1", "MOVEMENT_TYPE_FACE_DOWN", "Palm170_Astronomer", "0"),
    (17, 31, "LITTLE_GIRL", "MOVEMENT_TYPE_WANDER_AROUND", "Palm170_Girl", "0"),
    (6, 19, "WORKER_M", "MOVEMENT_TYPE_FACE_DOWN", "Palm170_Worker", "0"),
    (40, 31, "MAN_2", "MOVEMENT_TYPE_FACE_UP", "Palm170_GymGuard", "0"),
    (20, 38, "WOMAN_2", "MOVEMENT_TYPE_FACE_LEFT", "Palm170_Woman", "0"),
]
HZ_SIGNS = [(24, 41, "Palm170_TownSign"), (7, 19, "Palm170_StationSign"), (45, 13, "Palm170_PavilionSign"),
            (38, 31, "Palm170_GymSign")]

ST_GRUNTS = [(15, 6, "AQUA_MEMBER_M", "RIGHT", 4, "Palm172_Grunt1", "TRAINER_PALM_STATION_GRUNT_1"),
             (24, 6, "AQUA_MEMBER_F", "LEFT", 2, "Palm172_Grunt2", "TRAINER_PALM_STATION_GRUNT_2"),
             (17, 11, "AQUA_MEMBER_M", "DOWN", 2, "Palm172_Grunt3", "TRAINER_PALM_STATION_GRUNT_3")]
ST_MONS = [(16, 13, "MARILL", "FLAG_HT_HORIZON_PKMN_1"), (19, 12, "PSYDUCK", "FLAG_HT_HORIZON_PKMN_2"),
           (20, 13, "LOTAD", "FLAG_HT_HORIZON_PKMN_3")]
ST_AMPS = [((21, 5), "FLAG_HT_HORIZON_AMP_1"), ((27, 5), "FLAG_HT_HORIZON_AMP_2"), ((17, 8), "FLAG_HT_HORIZON_AMP_3")]
ST_TERMINAL = (20, 8)
ST_ENTRY = (18, 1)


def seam_check(bl, w, h, rows, cols=None):
    """As faixas que o mapa vizinho enxerga (desenhadas com os tilesets do vizinho) so podem usar o primario."""
    bad = [(x, y, bl[y * w + x] & 0x3FF) for y in rows for x in (cols or range(w)) if (bl[y * w + x] & 0x3FF) >= 512]
    assert not bad, f"emenda com secundario: {bad[:8]}"


def main():
    # ---------------- flags
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    names = [("FLAG_HT_HORIZON_CHELSIA_MET", 0x42, "Chelsia e o Piplup mostraram a estacao do lago"),
             ("FLAG_HT_HORIZON_AMP_1", 0x43, "amplificador 1 desligado"), ("FLAG_HT_HORIZON_AMP_2", 0x44, "amplificador 2 desligado"),
             ("FLAG_HT_HORIZON_AMP_3", 0x45, "amplificador 3 desligado"), ("FLAG_HT_HORIZON_PKMN_1", 0x46, "Marill solto"),
             ("FLAG_HT_HORIZON_PKMN_2", 0x47, "Psyduck solto"), ("FLAG_HT_HORIZON_PKMN_3", 0x48, "Lotad solto"),
             ("FLAG_HT_HORIZON_DONE", 0x49, "registro recuperado: o lago baixa")]
    for (n, v, cm) in names:
        old = f"#define FLAG_UNUSED_0x{v:03X}    0x{v:X} // Unused Flag"
        new = f"#define {n:<27} 0x{v:X} // {cm}"
        if n not in t:
            assert old in t, old
            t = t.replace(old, new)
    open(fp, "w").write(t)

    # ---------------- Serenia: saida norte + conexao + trava ate a 5a insignia
    sp = f"{ROOT}/data/maps/PalmSerenia/map.json"
    s = jload(sp)
    s["connections"] = [cn for cn in s["connections"] if cn["map"] != "MAP_PALM_ROUTE07"] + \
                       [OD([("map", "MAP_PALM_ROUTE07"), ("offset", R7.OFFSET_SERENIA), ("direction", "up")])]
    s["coord_events"] = [e for e in s["coord_events"] if e["script"] != "Palm141_NorthGate"] + \
                        [coord(x, 1, "Palm141_NorthGate") for x in SE.NORTH]
    jsave(sp, s)
    ss = f"{ROOT}/data/maps/PalmSerenia/scripts.inc"
    t = open(ss).read()
    if "Palm141_NorthGate::" not in t:
        t = t.rstrip("\n") + ("\n\nPalm141_NorthGate::\n\tgoto_if_set FLAG_BADGE05_GET, Palm141_NorthGateOk\n\tlockall\n"
                              "\tmsgbox Palm141_TextNorthGate, MSGBOX_DEFAULT\n\tapplymovement OBJ_EVENT_ID_PLAYER, Palm141_StepBackSouth\n"
                              "\twaitmovement 0\n\treleaseall\n\tend\n\nPalm141_NorthGateOk::\n\tend\n\n"
                              "Palm141_StepBackSouth:\n\twalk_down\n\tstep_end\n")
        open(ss, "w").write(t)

    # ---------------- Route 7
    c7 = R7.compose()
    for (x, y, _) in R7_SIGNS:
        c7.put(x, y, 3, collision=1)
    bl7 = R7.flatten(c7.build())
    seam_check(bl7, c7.w, c7.h, range(0, 7))
    register("PalmRoute07", "LAYOUT_PALM_ROUTE07", c7, bl7)
    j = map_json("MAP_PALM_ROUTE07", "PalmRoute07", "LAYOUT_PALM_ROUTE07", "MUS_ROUTE119", "MAPSEC_ROUTE_107", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_SERENIA"), ("offset", -R7.OFFSET_SERENIA), ("direction", "down")]),
                  OD([("map", "MAP_PALM_HORIZON"), ("offset", -HZ.OFFSET_ROUTE7), ("direction", "up")])])
    for (x, y, gfx, d, sight, script, _) in R7_TRAINERS:
        assert walkable(bl7, c7.w, x, y) and c7.terrain[y][x] != "pond", (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in R7_ITEMS:
        assert walkable(bl7, c7.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in R7_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute07/map.json", j)
    sc = ["PalmRoute07_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in R7_TRAINERS:
        k = script.replace("Palm160_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm160_Text{k}Intro, Palm160_Text{k}Loss\n"
                  f"\tmsgbox Palm160_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s_) in R7_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute07/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Horizon City (o mapa salvo e o "depois"; o alagamento entra por setmetatile ate o evento)
    ch = HZ.compose(flooded=False)
    for (x, y, _) in HZ_SIGNS:
        ch.put(x, y, 3, collision=1)
    blh = ch.build()
    cf = HZ.compose(flooded=True)
    for (x, y, _) in HZ_SIGNS:
        cf.put(x, y, 3, collision=1)
    blf = cf.build()
    flood = [(i % ch.w, i // ch.w, blf[i]) for i in range(len(blh)) if (blh[i] & 0xFFF) != (blf[i] & 0xFFF)]
    assert all(y < HZ.PROM[0] + 1 for (_, y, _) in flood), "alagamento fora da orla"
    seam_check(blh, ch.w, ch.h, range(ch.h - 7, ch.h))
    register("PalmHorizon", "LAYOUT_PALM_HORIZON", ch, blh)
    j = map_json("MAP_PALM_HORIZON", "PalmHorizon", "LAYOUT_PALM_HORIZON", "MUS_LILYCOVE", "MAPSEC_LILYCOVE_CITY", "MAP_TYPE_CITY",
                 [OD([("map", "MAP_PALM_ROUTE07"), ("offset", HZ.OFFSET_ROUTE7), ("direction", "down")])])
    for (x, y, gfx, mv, script, flag) in HZ_NPCS:
        assert walkable(blh, ch.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, mv, script, flag=flag, rng=1 if "WANDER" in mv else 0))
    for (label, dm, _, _) in HZ_INTERIORS:
        x, y = HZ.door(label)
        j["warp_events"].append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]))
    sx, sy = HZ.door("station")
    j["coord_events"] = [coord(sx, sy + 1, "Palm170_StationLock")] + [coord(x, 1, "Palm170_NorthGate") for x in HZ.NORTH]
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in HZ_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmHorizon/map.json", j)
    for idx, (_, _, folder, old) in enumerate(HZ_INTERIORS):
        if old is None:
            continue
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = jload(q)
        for wv in k["warp_events"]:
            if wv["dest_map"] in (old, "MAP_PALM_HORIZON"):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_HORIZON", str(idx)
        for o in k["object_events"]:
            if o["script"] in INTERIOR_NPCS:
                o["script"] = INTERIOR_NPCS[o["script"]]
        jsave(q, k)
    hp = f"{ROOT}/src/data/heal_locations.json"
    h = jload(hp)
    for e in h["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_MOSSDEEP_CITY":
            e["map"], e["x"], e["y"] = "MAP_PALM_HORIZON", HZ.door("pc")[0], HZ.door("pc")[1] + 1
    jsave(hp, h)
    gx, gy = HZ.door("gym")
    wall_mt = blh[gy * ch.w + gx - 1] & 0x3FF
    # setmetatile mantem a elevacao do mapa salvo (jardim, 3): agua do alagamento precisa entrar como bloqueada
    flood_cmds = "".join(f"\tsetmetatile {x}, {y}, {v & 0x3FF}, {'TRUE' if (v >> 10) & 3 or (v >> 12) == 1 else 'FALSE'}\n" for (x, y, v) in flood)
    sc = ["PalmHorizon_MapScripts::\n\tmap_script MAP_SCRIPT_ON_LOAD, Palm170_Load\n\t.byte 0\n",
          "Palm170_Load::\n\tgoto_if_set FLAG_HT_HORIZON_DONE, Palm170_LoadDone\n"   # ate o lago baixar:
          f"\tsetmetatile {gx}, {gy}, {wall_mt}, TRUE\n" + flood_cmds + "\tend\n",       # ginasio fechado e jardim alagado
          "Palm170_LoadDone::\n\tend\n",
          "Palm170_Chelsia::\n\tlockall\n\tapplymovement 1, Common_Movement_FacePlayer\n\twaitmovement 0\n"
          "\tmsgbox Palm170_TextChelsia1, MSGBOX_DEFAULT\n"
          "\tapplymovement 2, Palm170_PiplupPoint\n\twaitmovement 0\n\tplaymoncry SPECIES_PIPLUP, CRY_MODE_NORMAL\n"
          "\tmsgbox Palm170_TextPiplupPoints, MSGBOX_DEFAULT\n\twaitmoncry\n\tmsgbox Palm170_TextChelsia2, MSGBOX_DEFAULT\n"
          "\tsetflag FLAG_HT_HORIZON_CHELSIA_MET\n\tfadescreen FADE_TO_BLACK\n\tremoveobject 1\n\tremoveobject 2\n"
          "\tfadescreen FADE_FROM_BLACK\n\treleaseall\n\tend\n",
          "Palm170_PiplupPoint:\n\tface_left\n\tdelay_16\n\tjump_in_place_left\n\tstep_end\n",
          "Palm170_Piplup::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_PIPLUP, CRY_MODE_NORMAL\n\tmsgbox Palm170_TextPiplup, MSGBOX_DEFAULT\n"
          "\twaitmoncry\n\trelease\n\tend\n",
          "Palm170_StationLock::\n\tgoto_if_set FLAG_HT_HORIZON_CHELSIA_MET, Palm170_StationOk\n\tlockall\n"
          "\tmsgbox Palm170_TextStationLocked, MSGBOX_DEFAULT\n\tapplymovement OBJ_EVENT_ID_PLAYER, Palm170_StepBackSouth\n"
          "\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm170_StationOk::\n\tend\n",
          "Palm170_NorthGate::\n\tgoto_if_set FLAG_BADGE06_GET, Palm170_StationOk\n\tlockall\n"
          "\tmsgbox Palm170_TextNorthGate, MSGBOX_DEFAULT\n\tapplymovement OBJ_EVENT_ID_PLAYER, Palm170_StepBackSouth\n"
          "\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm170_StepBackSouth:\n\twalk_down\n\tstep_end\n",
          "Palm170_OldMan::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_HORIZON_DONE, Palm170_OldManDone\n"
          "\tmsgbox Palm170_OldMan_Text, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm170_OldManDone::\n\tmsgbox Palm170_OldMan_TextDone, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm170_GymGuard::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_HORIZON_DONE, Palm170_GymGuardDone\n"
          "\tmsgbox Palm170_GymGuard_Text, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm170_GymGuardDone::\n\tmsgbox Palm170_GymGuard_TextDone, MSGBOX_DEFAULT\n\trelease\n\tend\n"]
    for script in ("Palm170_Fisher", "Palm170_Astronomer", "Palm170_Girl", "Palm170_Worker", "Palm170_Woman"):
        sc.append(f"{script}::\n\tmsgbox {script}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s_) in HZ_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    for new in INTERIOR_NPCS.values():
        if new == "Palm171_House3Skitty":
            sc.append(f"{new}::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_SKITTY, CRY_MODE_NORMAL\n\tmsgbox {new}_Text, MSGBOX_DEFAULT\n"
                      "\twaitmoncry\n\trelease\n\tend\n")
        else:
            sc.append(f"{new}::\n\tmsgbox {new}_Text, MSGBOX_NPC\n\tend\n")
    open(f"{ROOT}/data/maps/PalmHorizon/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Estacao sob o lago (mapa novo sobre o layout do esconderijo da Aqua B2F)
    name = "PalmLakeStation"
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
    L = {l["id"]: l for l in jload(f"{ROOT}/data/layouts/layouts.json")["layouts"] if "id" in l}
    e = L["LAYOUT_AQUA_HIDEOUT_B2F"]
    stw = e["width"]
    stb = struct.unpack(f"<{stw * e['height']}H", open(f"{ROOT}/{e['blockdata_filepath']}", "rb").read())
    j = map_json("MAP_PALM_LAKE_STATION", name, "LAYOUT_AQUA_HIDEOUT_B2F", "MUS_AQUA_MAGMA_HIDEOUT", "MAPSEC_LILYCOVE_CITY",
                 "MAP_TYPE_INDOOR", [])
    j.update({"weather": "WEATHER_NONE", "allow_cycling": False, "allow_running": True, "show_map_name": False})
    station_idx = [i for i, (l, _, _, _) in enumerate(HZ_INTERIORS) if l == "station"][0]
    j["warp_events"] = [OD([("x", ST_ENTRY[0]), ("y", ST_ENTRY[1]), ("elevation", 0), ("dest_map", "MAP_PALM_HORIZON"),
                            ("dest_warp_id", str(station_idx))])]
    j["object_events"] = [obj("ANABEL", 19, 3, "MOVEMENT_TYPE_FACE_DOWN", "Palm172_Chelsia", flag="FLAG_HT_HORIZON_DONE"),
                          obj("OBJ_EVENT_GFX_SPECIES(PIPLUP)", 20, 3, "MOVEMENT_TYPE_FACE_DOWN", "Palm172_Piplup", flag="FLAG_HT_HORIZON_DONE")]
    for (x, y, gfx, d, sight, script, _) in ST_GRUNTS:
        assert walkable(stb, stw, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, sp_, flag) in ST_MONS:
        assert walkable(stb, stw, x, y), (sp_, x, y)
        j["object_events"].append(obj(f"OBJ_EVENT_GFX_SPECIES({sp_})", x, y, "MOVEMENT_TYPE_FACE_DOWN", f"Palm172_Free{sp_}", flag=flag))
    local = {o["script"]: i + 1 for i, o in enumerate(j["object_events"])}
    j["bg_events"] = [sign(x, y, f"Palm172_Amp{i + 1}") for i, ((x, y), _) in enumerate(ST_AMPS)] + \
                     [sign(ST_TERMINAL[0], ST_TERMINAL[1], "Palm172_Terminal")]
    jsave(f"{ROOT}/data/maps/{name}/map.json", j)
    all_flags = [f for (_, f) in ST_AMPS] + [f for (_, _, _, f) in ST_MONS]
    sc = [f"{name}_MapScripts::\n\t.byte 0\n",
          "Palm172_Chelsia::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_HORIZON_DONE, Palm172_ChelsiaDone\n"
          "\tmsgbox Palm172_TextChelsia, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm172_ChelsiaDone::\n\tmsgbox Palm172_TextChelsiaDone, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm172_Piplup::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_PIPLUP, CRY_MODE_NORMAL\n\tmsgbox Palm170_TextPiplup, MSGBOX_DEFAULT\n"
          "\twaitmoncry\n\trelease\n\tend\n"]
    for (_, _, _, _, _, script, tid) in ST_GRUNTS:
        k = script.replace("Palm172_", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm172_Text{k}Intro, Palm172_Text{k}Loss\n"
                  f"\tmsgbox Palm172_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for i, (_, flag) in enumerate(ST_AMPS, 1):
        sc.append(f"Palm172_Amp{i}::\n\tlockall\n\tgoto_if_set {flag}, Palm172_AmpOff\n\tmsgbox Palm172_TextAmp, MSGBOX_YESNO\n"
                  f"\tgoto_if_eq VAR_RESULT, NO, Palm172_Release\n\tsetflag {flag}\n\tplayse SE_PC_OFF\n\twaitse\n"
                  "\tmsgbox Palm172_TextAmpDown, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc.append("Palm172_AmpOff::\n\tmsgbox Palm172_TextAmpIsOff, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc.append("Palm172_Release::\n\treleaseall\n\tend\n")
    for (_, _, sp_, flag) in ST_MONS:
        sc.append(f"Palm172_Free{sp_}::\n\tlockall\n\tplaymoncry SPECIES_{sp_}, CRY_MODE_NORMAL\n\tmsgbox Palm172_TextNet{sp_}, MSGBOX_DEFAULT\n"
                  f"\twaitmoncry\n\tsetflag {flag}\n\tplayse SE_BALL_OPEN\n\tremoveobject {local[f'Palm172_Free{sp_}']}\n"
                  f"\tmsgbox Palm172_TextFreed{sp_}, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc.append("Palm172_Terminal::\n\tlockall\n\tgoto_if_set FLAG_HT_HORIZON_DONE, Palm172_TerminalDone\n"
              + "".join(f"\tgoto_if_unset {f}, Palm172_TerminalBusy\n" for f in all_flags)
              + "\tmsgbox Palm172_TextTerminal, MSGBOX_DEFAULT\n\tplayse SE_PC_LOGIN\n\twaitse\n"
              "\tmsgbox Palm172_TextRecord, MSGBOX_DEFAULT\n\tsetflag FLAG_HT_HORIZON_DONE\n"
              "\tapplymovement 1, Common_Movement_FacePlayer\n\twaitmovement 0\n\tmsgbox Palm172_TextChelsiaRecord, MSGBOX_DEFAULT\n"
              "\treleaseall\n\tend\n")
    sc.append("Palm172_TerminalBusy::\n\tmsgbox Palm172_TextTerminalBusy, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc.append("Palm172_TerminalDone::\n\tmsgbox Palm172_TextRecord, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    open(f"{ROOT}/data/maps/{name}/scripts.inc", "w").write("\n".join(sc))

    # ---------------- encontros da Route 7
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE07"]
    mons = lambda L_: [OD([("min_level", a), ("max_level", b), ("species", s_)]) for (s_, a, b) in L_]
    entry = OD([("map", "MAP_PALM_ROUTE07"), ("base_label", "gPalmRoute07"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", mons(R7_WILD))])),
                ("water_mons", OD([("encounter_rate", 4), ("mons", mons(R7_WATER))])),
                ("fishing_mons", OD([("encounter_rate", 30), ("mons", mons(R7_FISH))]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE06") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    for f in ("ch7.txt",):
        subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/{f}"], check=True)
    print("Cap. 7 instalado: Route 7", c7.w, "x", c7.h, "| Horizon", ch.w, "x", ch.h, "| alagamento", len(flood), "tiles",
          "| portas", [(l, HZ.door(l)) for (l, _, _, _) in HZ_INTERIORS])


if __name__ == "__main__":
    main()
