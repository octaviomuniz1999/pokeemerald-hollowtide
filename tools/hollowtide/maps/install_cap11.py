#!/usr/bin/env python3
"""Capitulo 11 (parte 1): Route 11 (MAP_PALM_ROUTE11, "Caminho da Liga") e a chegada a ilha da Liga.

- Tidemouth ganha a saida oeste (linhas 28-29) com conexao continua para a Route 11 (Tidemouth y = Route 11
  y + 8); um guarda confere as 8 insignias na entrada da rota;
- Route 11: praia sob as falesias, dois patamares e a boca do tunel na parede da serra; Vincent, Leroy e
  Felix (treinadores de elite) com visao; 3 itens; encontros de caverna/vitoria do Cap. 11;
- o tunel sai na parte alta de Ever Grande (a ilha da Liga, reaproveitada) — a parte baixa e o Victory Road
  originais ficam fora do caminho; os guardas da Liga conferem a 8a insignia.
As salas da Elite e do campeao entram na parte 2. Rodar depois de install_nami_gym.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route11 as R11, tidemouth as TD
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable
from install_cap7 import seam_check

OD = collections.OrderedDict
R11_TRAINERS = [(36, 18, "MAN_4", "DOWN", 2, "Palm210_RouteVINCENT", "TRAINER_PALM_ROUTE11_VINCENT"),
                (24, 12, "WOMAN_4", "UP", 1, "Palm210_RouteFELIX", "TRAINER_PALM_ROUTE11_FELIX"),
                (14, 9, "MAN_4", "DOWN", 1, "Palm210_RouteLEROY", "TRAINER_PALM_ROUTE11_LEROY")]
R11_ITEMS = [(4, 22, "ITEM_FULL_RESTORE", "FLAG_ITEM_ROUTE_111_HP_UP"),
             (38, 4, "ITEM_MAX_REVIVE", "FLAG_ITEM_ROUTE_112_NUGGET"),
             (21, 27, "ITEM_PP_MAX", "FLAG_ITEM_ROUTE_113_MAX_ETHER")]
R11_SIGNS = [(44, 19, "Palm210_SignEast"), (11, 8, "Palm210_SignCave")]
R11_WILD = [("SPECIES_GOLBAT", 52, 54), ("SPECIES_LAIRON", 52, 54), ("SPECIES_HAWLUCHA", 52, 54), ("SPECIES_DRUDDIGON", 53, 55),
            ("SPECIES_GOLBAT", 53, 55), ("SPECIES_LAIRON", 53, 55), ("SPECIES_HAWLUCHA", 53, 55), ("SPECIES_SNEASEL", 52, 54),
            ("SPECIES_DRUDDIGON", 54, 56), ("SPECIES_SNEASEL", 53, 55), ("SPECIES_GABITE", 54, 56), ("SPECIES_JANGMO_O", 52, 54)]


def main():
    # ---------------- Tidemouth: saida oeste
    tp = f"{ROOT}/data/maps/PalmTidemouth/map.json"
    tj = jload(tp)
    tj["connections"] = [cn for cn in tj["connections"] if cn["map"] != "MAP_PALM_ROUTE11"] + \
                        [OD([("map", "MAP_PALM_ROUTE11"), ("offset", R11.OFFSET_TIDEMOUTH), ("direction", "left")])]
    jsave(tp, tj)

    # ---------------- Route 11
    c = R11.compose()
    for (x, y, _) in R11_SIGNS:
        c.put(x, y, 3, collision=1)
    bl = R11.flatten(c.build())
    register("PalmRoute11", "LAYOUT_PALM_ROUTE11", c, bl)
    j = map_json("MAP_PALM_ROUTE11", "PalmRoute11", "LAYOUT_PALM_ROUTE11", "MUS_VICTORY_ROAD", "MAPSEC_VICTORY_ROAD", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_TIDEMOUTH"), ("offset", -R11.OFFSET_TIDEMOUTH), ("direction", "right")])])
    for (x, y, gfx, d, sight, script, _) in R11_TRAINERS:
        assert walkable(bl, c.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in R11_ITEMS:
        assert walkable(bl, c.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["warp_events"] = [OD([("x", R11.CAVE[0]), ("y", R11.CAVE[1]), ("elevation", 0), ("dest_map", "MAP_EVER_GRANDE_CITY"), ("dest_warp_id", "3")])]
    j["coord_events"] = [coord(R11.W - 2, y, "Palm210_BadgeGate") for y in R11.EAST]
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in R11_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute11/map.json", j)
    sc = ["PalmRoute11_MapScripts::\n\t.byte 0\n",
          "Palm210_BadgeGate::\n\tgoto_if_set FLAG_BADGE08_GET, Palm210_Ok\n\tlockall\n\tmsgbox Palm210_TextBadgeGate, MSGBOX_DEFAULT\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm210_StepBackEast\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm210_Ok::\n\tend\n", "Palm210_StepBackEast:\n\twalk_right\n\tstep_end\n"]
    for (_, _, _, _, _, script, tid) in R11_TRAINERS:
        k = script.replace("Palm210_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm210_Text{k}Intro, Palm210_Text{k}Loss\n"
                  f"\tmsgbox Palm210_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s_) in R11_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute11/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Ever Grande (ilha da Liga): o tunel sai na parte alta; sem a conexao com a Route 128
    ep = f"{ROOT}/data/maps/EverGrandeCity/map.json"
    e = jload(ep)
    e["connections"] = []
    for w in e["warp_events"]:
        if w["x"] == 18 and w["y"] == 27:
            w["dest_map"], w["dest_warp_id"] = "MAP_PALM_ROUTE11", "0"
    jsave(ep, e)
    # guardas da Liga: 8a insignia (no original, a 6a era a unica que dava para pular)
    lp = f"{ROOT}/data/maps/EverGrandeCity_PokemonLeague_1F/scripts.inc"
    t = open(lp).read()
    t = t.replace("goto_if_unset FLAG_BADGE06_GET, EverGrandeCity_PokemonLeague_1F_EventScript_NotAllBadges",
                  "goto_if_unset FLAG_BADGE08_GET, EverGrandeCity_PokemonLeague_1F_EventScript_NotAllBadges")
    open(lp, "w").write(t)

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [x for x in grp["encounters"] if x.get("map") != "MAP_PALM_ROUTE11"]
    entry = OD([("map", "MAP_PALM_ROUTE11"), ("base_label", "gPalmRoute11"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s_)])
                                                                    for (s_, a, b) in R11_WILD])]))])
    idx = next(i for i, x in enumerate(grp["encounters"]) if x.get("map") == "MAP_PALM_ROUTE10") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch11.txt"], check=True)
    print("Cap. 11 (parte 1) instalado: Route 11", c.w, "x", c.h, "| tunel", R11.CAVE)


if __name__ == "__main__":
    main()
