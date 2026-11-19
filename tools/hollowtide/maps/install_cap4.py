#!/usr/bin/env python3
"""Capitulo 4: instala a Route 4 (MAP_PALM_ROUTE04) e o Tradepost (MAP_PALM_TRADEPOST), mapas novos.

- registra os mapas (map_groups.json, layouts.json, include em data/event_scripts.s);
- conexoes continuas Ferralia (direita, offset 24) <-> Route 4 <-> Tradepost (offset 0); os tres usam
  General + Rustboro, entao as emendas ficam corretas dos dois lados;
- trava na borda leste da Ferralia ate a Insignia da Ressonancia (recua um passo);
- treinadores Yue, Qiao e Mara (slots de Hoenn sem uso), itens, placas, encontros;
- Tradepost: Centro Pokemon e Mart (interiores de Verdanturf), casa e casa do Relembrador de Golpes,
  ponto de cura; evento "O Preco da Troca" (sem batalha): Mestre Wen -> operador da estacao entrega a
  autorizacao original de carga -> Wen desmonta a cobranca em PALM Coin -> mensageira da Palm vai embora,
  Amulet Coin. Saida norte (Route 5) segue fechada ate o Capitulo 5.
Rodar depois de install_ferralia.py.
"""
import collections, json, os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route4 as R4, tradepost as TP, ferralia as FE
from canvas import ROOT

OD = collections.OrderedDict
SIGN = 3


def jload(p):
    return json.load(open(p), object_pairs_hook=OD)


def jsave(p, j):
    open(p, "w").write(json.dumps(j, indent=2, ensure_ascii=False) + "\n")


def obj(gfx, x, y, mv, script, ttype="TRAINER_TYPE_NONE", sight=0, flag="0", rng=0):
    return OD([("graphics_id", f"OBJ_EVENT_GFX_{gfx}" if not gfx.startswith("OBJ_") else gfx), ("x", x), ("y", y),
               ("elevation", 3), ("movement_type", mv), ("movement_range_x", rng), ("movement_range_y", rng),
               ("trainer_type", ttype), ("trainer_sight_or_berry_tree_id", str(sight)), ("script", script), ("flag", flag)])


def sign(x, y, script):
    return OD([("type", "sign"), ("x", x), ("y", y), ("elevation", 0), ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", script)])


def coord(x, y, script):
    return OD([("type", "trigger"), ("x", x), ("y", y), ("elevation", 3), ("var", "VAR_TEMP_0"), ("var_value", "0"), ("script", script)])


def map_json(mid, name, layout, music, mapsec, mtype, conns):
    return OD([("id", mid), ("name", name), ("layout", layout), ("music", music), ("region", "REGION_HOENN"),
               ("region_map_section", mapsec), ("requires_flash", False), ("weather", "WEATHER_SUNNY"),
               ("map_type", mtype), ("allow_cycling", True), ("allow_escaping", False), ("allow_running", True),
               ("show_map_name", True), ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", conns),
               ("object_events", []), ("warp_events", []), ("coord_events", []), ("bg_events", [])])


def register(name, layout_id, c, bl):
    d = f"{ROOT}/data/layouts/{name}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/map.bin", "wb").write(struct.pack(f"<{len(bl)}H", *bl))
    open(f"{d}/border.bin", "wb").write(struct.pack("<4H", *[m | (3 << 12) for m in (468, 469, 476, 477)]))
    lay = jload(f"{ROOT}/data/layouts/layouts.json")
    lay["layouts"] = [l for l in lay["layouts"] if l.get("id") != layout_id] + [OD([
        ("id", layout_id), ("name", f"{name}_Layout"), ("width", c.w), ("height", c.h), ("primary_tileset", c.primary),
        ("secondary_tileset", c.secondary), ("border_filepath", f"data/layouts/{name}/border.bin"),
        ("blockdata_filepath", f"data/layouts/{name}/map.bin"), ("layout_version", "emerald")])]
    jsave(f"{ROOT}/data/layouts/layouts.json", lay)
    mg = jload(f"{ROOT}/data/maps/map_groups.json")
    grp = mg["gMapGroup_TownsAndRoutes"]
    if name not in grp:
        grp.append(name)
        jsave(f"{ROOT}/data/maps/map_groups.json", mg)
    es = f"{ROOT}/data/event_scripts.s"
    t = open(es).read()
    inc = f'\t.include "data/maps/{name}/scripts.inc"\n'
    if inc not in t:
        anchor = '\t.include "data/maps/PalmFerralia/scripts.inc"\n'
        t = t.replace(anchor, anchor + inc)
        open(es, "w").write(t)
    os.makedirs(f"{ROOT}/data/maps/{name}", exist_ok=True)


def walkable(bl, w, x, y):
    return (bl[y * w + x] >> 10) & 3 == 0


# ----------------------------------------------------------------------------------------------- Route 4
R4_TRAINERS = [(16, 18, "LASS", "UP", 2, "Palm110_RouteYUE", "TRAINER_PALM_ROUTE04_YUE"),
               (38, 15, "BLACK_BELT", "DOWN", 1, "Palm110_RouteQIAO", "TRAINER_PALM_ROUTE04_QIAO"),
               (48, 13, "POKEFAN_F", "LEFT", 3, "Palm110_RouteMARA", "TRAINER_PALM_ROUTE04_MARA")]
R4_ITEMS = [(19, 12, "ITEM_SUPER_POTION", "FLAG_ITEM_ROUTE_120_NUGGET"),
            (17, 22, "ITEM_ORAN_BERRY", "FLAG_ITEM_ROUTE_120_FULL_HEAL"),
            (17, 23, "ITEM_ORAN_BERRY", "FLAG_ITEM_ROUTE_121_CARBOS")]
R4_SIGNS = [(13, 15, "Palm110_SignWest"), (49, 15, "Palm110_SignEast")]
R4_NPCS = [(8, 18, "MAN_4", "MOVEMENT_TYPE_FACE_UP", "Palm110_Trader")]
R4_WILD = [("SPECIES_MEOWTH", 19, 22), ("SPECIES_ELECTRIKE", 19, 22), ("SPECIES_TIMBURR", 20, 22), ("SPECIES_TIMBURR", 20, 22),
           ("SPECIES_KOFFING", 20, 22), ("SPECIES_NINCADA", 20, 22), ("SPECIES_DWEBBLE", 20, 23), ("SPECIES_DWEBBLE", 20, 23),
           ("SPECIES_TRUBBISH", 21, 23), ("SPECIES_TRUBBISH", 21, 23), ("SPECIES_TRUBBISH", 21, 23), ("SPECIES_TRUBBISH", 21, 23)]

# --------------------------------------------------------------------------------------------- Tradepost
TP_DOOR_OFF = {"rb_house_grey": (2, 4), "rb_office_long": (4, 5), "rb_office_small": (2, 4), "rb_pokecenter": (1, 3),
               "rb_mart": (1, 3)}
TP_INTERIORS = [("pc", "MAP_VERDANTURF_TOWN_POKEMON_CENTER_1F", "VerdanturfTown_PokemonCenter_1F", "MAP_VERDANTURF_TOWN"),
                ("mart", "MAP_VERDANTURF_TOWN_MART", "VerdanturfTown_Mart", "MAP_VERDANTURF_TOWN"),
                ("house_n", "MAP_VERDANTURF_TOWN_HOUSE", "VerdanturfTown_House", "MAP_VERDANTURF_TOWN"),
                ("house_s", "MAP_FALLARBOR_TOWN_MOVE_RELEARNERS_HOUSE", "FallarborTown_MoveRelearnersHouse", "MAP_FALLARBOR_TOWN")]
TP_NPCS = [  # (x, y, grafico, movimento, script, flag de sumir)
    (21, 25, "OLD_MAN", "MOVEMENT_TYPE_FACE_DOWN", "Palm111_Wen", "0"),
    (14, 9, "MAN_2", "MOVEMENT_TYPE_FACE_DOWN", "Palm111_StationOperator", "0"),
    (26, 17, "AQUA_MEMBER_F", "MOVEMENT_TYPE_FACE_LEFT", "Palm111_PalmMessenger", "FLAG_HT_TRADEPOST_DONE"),
    (19, 17, "WOMAN_3", "MOVEMENT_TYPE_FACE_RIGHT", "Palm111_FruitSeller", "0"),
    (8, 22, "MAN_4", "MOVEMENT_TYPE_FACE_DOWN", "Palm111_Porter", "0"),
    (36, 12, "SAILOR", "MOVEMENT_TYPE_FACE_LEFT", "Palm111_DockSailor", "0"),
    (27, 5, "WORKER_M", "MOVEMENT_TYPE_FACE_DOWN", "Palm111_NorthWorker", "0"),
]
TP_SIGNS = [(3, 15, "Palm111_TownSign"), (18, 29, "Palm111_AssociationSign"), (19, 8, "Palm111_StationSign"),
            (25, 8, "Palm111_NorthSign"), (34, 8, "Palm111_KioskSign")]
TP_ITEMS = [(37, 24, "ITEM_GREAT_BALL", "FLAG_ITEM_ROUTE_120_HYPER_POTION")]


def main():
    # ---------------- Route 4
    c4 = R4.compose()
    for (x, y, _) in R4_SIGNS:
        c4.put(x, y, SIGN, collision=1)
    bl4 = c4.build()
    register("PalmRoute04", "LAYOUT_PALM_ROUTE04", c4, bl4)
    j = map_json("MAP_PALM_ROUTE04", "PalmRoute04", "LAYOUT_PALM_ROUTE04", "MUS_ROUTE104", "MAPSEC_ROUTE_104", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_FERRALIA"), ("offset", -R4.OFFSET_FERRALIA), ("direction", "left")]),
                  OD([("map", "MAP_PALM_TRADEPOST"), ("offset", 0), ("direction", "right")])])
    for (x, y, gfx, d, sight, script, _) in R4_TRAINERS:
        assert walkable(bl4, c4.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, gfx, mv, script) in R4_NPCS:
        assert walkable(bl4, c4.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, mv, script))
    for (x, y, item, flag) in R4_ITEMS:
        assert walkable(bl4, c4.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in R4_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute04/map.json", j)
    sc = ["PalmRoute04_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in R4_TRAINERS:
        k = script.replace("Palm110_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm110_Text{k}Intro, Palm110_Text{k}Loss\n"
                  f"\tmsgbox Palm110_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, _, _, script) in R4_NPCS:
        sc.append(f"{script}::\n\tmsgbox {script}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s) in R4_SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute04/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Tradepost
    ct = TP.compose()
    for (x, y, _) in TP_SIGNS:
        ct.put(x, y, SIGN, collision=1)
    blt = ct.build()
    register("PalmTradepost", "LAYOUT_PALM_TRADEPOST", ct, blt)
    j = map_json("MAP_PALM_TRADEPOST", "PalmTradepost", "LAYOUT_PALM_TRADEPOST", "MUS_SLATEPORT", "MAPSEC_SLATEPORT_CITY", "MAP_TYPE_TOWN",
                 [OD([("map", "MAP_PALM_ROUTE04"), ("offset", 0), ("direction", "left")])])
    for (x, y, gfx, mv, script, flag) in TP_NPCS:
        assert walkable(blt, ct.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, mv, script, flag=flag))
    for (x, y, item, flag) in TP_ITEMS:
        assert walkable(blt, ct.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    local = {e["script"]: i + 1 for i, e in enumerate(j["object_events"])}
    pos = {label: (name, x, y) for (name, x, y, label) in TP.BUILDINGS}
    def door(label):
        name, x, y = pos[label]
        dx, dy = TP_DOOR_OFF[name]
        return x + dx, y + dy
    for (label, dm, _, _) in TP_INTERIORS:
        x, y = door(label)
        j["warp_events"].append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]))
    pcx, pcy = pos["pc"][1:]; mx, my = pos["mart"][1:]
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in TP_SIGNS] + \
        [sign(pcx + 2, pcy + 3, "Common_EventScript_ShowPokemonCenterSign"), sign(pcx + 3, pcy + 3, "Common_EventScript_ShowPokemonCenterSign"),
         sign(mx + 2, my + 3, "Common_EventScript_ShowPokemartSign"), sign(mx + 3, my + 3, "Common_EventScript_ShowPokemartSign")]
    jsave(f"{ROOT}/data/maps/PalmTradepost/map.json", j)
    for idx, (_, _, folder, old) in enumerate(TP_INTERIORS):
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = jload(q)
        for wv in k["warp_events"]:
            if wv["dest_map"] in (old, "MAP_PALM_TRADEPOST"):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_TRADEPOST", str(idx)
        jsave(q, k)
    hp = f"{ROOT}/src/data/heal_locations.json"
    h = jload(hp)
    for e in h["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_VERDANTURF_TOWN":
            e["map"], e["x"], e["y"] = "MAP_PALM_TRADEPOST", door("pc")[0], door("pc")[1] + 1
    jsave(hp, h)
    msg = local["Palm111_PalmMessenger"]
    sc = ["PalmTradepost_MapScripts::\n\t.byte 0\n",
          # Mestre Wen: pede a autorizacao; com ela em maos, resolve o impasse
          "Palm111_Wen::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_TRADEPOST_DONE, Palm111_WenDone\n"
          "\tgoto_if_set FLAG_HT_TRADEPOST_PERMIT, Palm111_WenResolve\n"
          "\tmsgbox Palm111_TextWenAsk, MSGBOX_DEFAULT\n\tsetflag FLAG_HT_TRADEPOST_WEN_ASKED\n\trelease\n\tend\n",
          "Palm111_WenResolve::\n\tmsgbox Palm111_TextWenResolve, MSGBOX_DEFAULT\n\tclosemessage\n"
          f"\tapplymovement {msg}, Palm111_MessengerLeaves\n\twaitmovement 0\n\tremoveobject {msg}\n"
          "\tsetflag FLAG_HT_TRADEPOST_DONE\n\tmsgbox Palm111_TextWenReward, MSGBOX_DEFAULT\n"
          "\tgiveitem ITEM_AMULET_COIN\n\trelease\n\tend\n",
          "Palm111_WenDone::\n\tmsgbox Palm111_TextWenDone, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm111_MessengerLeaves:\n\twalk_right\n\twalk_right\n\twalk_up\n\twalk_up\n\twalk_up\n\tstep_end\n",
          # operador da estacao: entrega a autorizacao original depois do pedido do Wen
          "Palm111_StationOperator::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_TRADEPOST_PERMIT, Palm111_OperatorAfter\n"
          "\tgoto_if_unset FLAG_HT_TRADEPOST_WEN_ASKED, Palm111_OperatorIdle\n"
          "\tmsgbox Palm111_TextOperatorGive, MSGBOX_DEFAULT\n\tplayfanfare MUS_OBTAIN_ITEM\n"
          "\tmessage Palm111_TextGotPermit\n\twaitfanfare\n\twaitmessage\n\tsetflag FLAG_HT_TRADEPOST_PERMIT\n"
          "\tmsgbox Palm111_TextOperatorAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm111_OperatorIdle::\n\tmsgbox Palm111_TextOperatorIdle, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm111_OperatorAfter::\n\tmsgbox Palm111_TextOperatorAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm111_FruitSeller::\n\tgoto_if_set FLAG_HT_TRADEPOST_DONE, Palm111_FruitSellerHappy\n"
          "\tmsgbox Palm111_FruitSeller_Text, MSGBOX_NPC\n\tend\n",
          "Palm111_FruitSellerHappy::\n\tmsgbox Palm111_FruitSellerHappy_Text, MSGBOX_NPC\n\tend\n"]
    for (_, _, _, _, script, _) in TP_NPCS:
        if script not in ("Palm111_Wen", "Palm111_StationOperator", "Palm111_FruitSeller"):
            sc.append(f"{script}::\n\tmsgbox {script}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s) in TP_SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmTradepost/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Ferralia: conexao leste + trava ate a Insignia da Ressonancia
    fp = f"{ROOT}/data/maps/PalmFerralia/map.json"
    f = jload(fp)
    f["connections"] = [cn for cn in f["connections"] if cn["map"] != "MAP_PALM_ROUTE04"] + \
                       [OD([("map", "MAP_PALM_ROUTE04"), ("offset", R4.OFFSET_FERRALIA), ("direction", "right")])]
    f["coord_events"] = [e for e in f["coord_events"] if e["script"] != "Palm103_EastGate"] + \
                        [coord(FE.W - 2, y, "Palm103_EastGate") for y in (40, 41)]
    jsave(fp, f)
    fs = f"{ROOT}/data/maps/PalmFerralia/scripts.inc"
    t = open(fs).read()
    if "Palm103_EastGate::" not in t:
        t = t.rstrip("\n") + ("\n\nPalm103_EastGate::\n\tgoto_if_set FLAG_BADGE03_GET, Palm103_EastGateOk\n\tlockall\n"
                              "\tmsgbox Palm103_TextEastGate, MSGBOX_DEFAULT\n\tapplymovement OBJ_EVENT_ID_PLAYER, Palm103_StepBackWest\n"
                              "\twaitmovement 0\n\treleaseall\n\tend\n\nPalm103_EastGateOk::\n\tend\n\n"
                              "Palm103_StepBackWest:\n\twalk_left\n\tstep_end\n")
        open(fs, "w").write(t)

    # ---------------- encontros
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE04"]
    entry = OD([("map", "MAP_PALM_ROUTE04"), ("base_label", "gPalmRoute04"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s)])
                                                                    for (s, a, b) in R4_WILD])]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_FERRALIA") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch4.txt"], check=True)
    print("Cap. 4 instalado: Route 4", c4.w, "x", c4.h, "| Tradepost", ct.w, "x", ct.h,
          "| portas", [(l, door(l)) for (l, _, _, _) in TP_INTERIORS])


if __name__ == "__main__":
    main()
