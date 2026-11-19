#!/usr/bin/env python3
"""Capitulo 5 (parte 1): instala a Route 5 (MAP_PALM_ROUTE05) e abre a saida norte do Tradepost.

- Route 5: mapa novo (General + Rustboro), conexao continua com o Tradepost (offset 6; o canal vira o rio);
- Tradepost: conexao para cima + trava ate "O Preco da Troca" (recua um passo); o operario da enchente sai;
- treinadores Tiago, Odair, Lia e Dudu (opcional), 3 itens, placas, encontros do Cap. 5;
- norte: Pillarton ainda nao existe — a trilha termina na mata, placa de obras na barragem.
Rodar depois de install_cap4.py.
"""
import collections, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route5 as R5, tradepost as TP
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable

OD = collections.OrderedDict
TRAINERS = [(19, 45, "FISHERMAN", "RIGHT", 2, "Palm120_RouteTIAGO", "TRAINER_PALM_ROUTE05_TIAGO"),
            (13, 27, "HIKER", "RIGHT", 1, "Palm120_RouteODAIR", "TRAINER_PALM_ROUTE05_ODAIR"),
            (19, 5, "PICNICKER", "LEFT", 2, "Palm120_RouteLIA", "TRAINER_PALM_ROUTE05_LIA"),
            (35, 26, "HIKER", "UP", 3, "Palm120_RouteDUDU", "TRAINER_PALM_ROUTE05_DUDU")]
ITEMS = [(13, 32, "ITEM_SUPER_POTION", "FLAG_ITEM_ROUTE_120_NEST_BALL"),
         (37, 22, "ITEM_SOFT_SAND", "FLAG_ITEM_ROUTE_120_REVIVE"),
         (6, 11, "ITEM_ETHER", "FLAG_ITEM_ROUTE_123_RARE_CANDY")]
SIGNS = [(19, 48, "Palm120_SignSouth"), (18, 8, "Palm120_SignNorth")]
WILD = [("SPECIES_SANDSHREW", 24, 26), ("SPECIES_PHANPY", 24, 26), ("SPECIES_CUBONE", 24, 26), ("SPECIES_WOOPER", 24, 26),
        ("SPECIES_MARILL", 24, 26), ("SPECIES_LOTAD", 24, 26), ("SPECIES_SANDSHREW", 25, 27), ("SPECIES_PHANPY", 25, 27),
        ("SPECIES_CUBONE", 25, 27), ("SPECIES_WOOPER", 25, 27), ("SPECIES_LARVITAR", 25, 27), ("SPECIES_LARVITAR", 25, 27)]


def main(north_open=False):
    c = R5.compose(north_open=north_open)
    for (x, y, _) in SIGNS:
        c.put(x, y, 3, collision=1)
    bl = c.build()
    register("PalmRoute05", "LAYOUT_PALM_ROUTE05", c, bl)
    j = map_json("MAP_PALM_ROUTE05", "PalmRoute05", "LAYOUT_PALM_ROUTE05", "MUS_ROUTE119", "MAPSEC_ROUTE_105", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_TRADEPOST"), ("offset", -R5.OFFSET_TRADEPOST), ("direction", "down")])])
    for (x, y, gfx, d, sight, script, _) in TRAINERS:
        assert walkable(bl, c.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute05/map.json", j)
    sc = ["PalmRoute05_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in TRAINERS:
        k = script.replace("Palm120_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm120_Text{k}Intro, Palm120_Text{k}Loss\n"
                  f"\tmsgbox Palm120_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s) in SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute05/scripts.inc", "w").write("\n".join(sc))

    # Tradepost: saida norte + trava ate o evento; operario da enchente some depois
    tp = f"{ROOT}/data/maps/PalmTradepost/map.json"
    t = jload(tp)
    t["connections"] = [cn for cn in t["connections"] if cn["map"] != "MAP_PALM_ROUTE05"] + \
                       [OD([("map", "MAP_PALM_ROUTE05"), ("offset", R5.OFFSET_TRADEPOST), ("direction", "up")])]
    t["coord_events"] = [e for e in t["coord_events"] if e["script"] != "Palm121_NorthGate"] + \
                        [coord(x, 1, "Palm121_NorthGate") for x in range(TP.NORTH_EXIT[0], TP.NORTH_EXIT[1] + 1)]
    for o in t["object_events"]:
        if o["script"] == "Palm111_NorthWorker":
            o["flag"] = "FLAG_HT_TRADEPOST_DONE"
    jsave(tp, t)
    ts = f"{ROOT}/data/maps/PalmTradepost/scripts.inc"
    s = open(ts).read()
    if "Palm121_NorthGate::" not in s:
        s = s.rstrip("\n") + ("\n\nPalm121_NorthGate::\n\tgoto_if_set FLAG_HT_TRADEPOST_DONE, Palm121_NorthGateOk\n\tlockall\n"
                              "\tmsgbox Palm121_TextNorthGate, MSGBOX_DEFAULT\n\tapplymovement OBJ_EVENT_ID_PLAYER, Palm121_StepBackSouth\n"
                              "\twaitmovement 0\n\treleaseall\n\tend\n\nPalm121_NorthGateOk::\n\tend\n\n"
                              "Palm121_StepBackSouth:\n\twalk_down\n\tstep_end\n")
        open(ts, "w").write(s)

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE05"]
    entry = OD([("map", "MAP_PALM_ROUTE05"), ("base_label", "gPalmRoute05"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s)])
                                                                    for (s, a, b) in WILD])]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE04") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch5.txt"], check=True)
    print("Route 5 instalada:", c.w, "x", c.h)


if __name__ == "__main__":
    main()
