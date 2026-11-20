#!/usr/bin/env python3
"""Capitulo 9 (parte 1): Route 9 (MAP_PALM_ROUTE09), o "Corredor de Ferro", mapa novo.

- a estrada leste da Passway (o deslizamento foi limpo) tem conexao continua com a Route 9 (offset 0);
  a faixa da Passway que a rota enxerga so tem primario e a faixa da rota que a Passway enxerga tambem
  (os trilhos comecam num para-choque depois dela) — conferido aqui;
- Route 9: estrada ao lado da ferrovia que vem de Voltara, subestacao, mato alto; Joseph, Fabian, Drew e
  Heidi com visao; 3 itens; encontros eletricos do Cap. 9;
- a saida leste (Voltara) fica fechada nesta etapa: a cidade esta sem energia e o portao nao abre.
Rodar depois de install_cap8.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route9 as R9, passway as PW
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable
from install_cap7 import seam_check

OD = collections.OrderedDict
R9_TRAINERS = [(8, 17, "MAN_3", "DOWN", 2, "Palm190_RouteJOSEPH", "TRAINER_PALM_ROUTE09_JOSEPH"),
               (16, 15, "CAMPER", "LEFT", 1, "Palm190_RouteDREW", "TRAINER_PALM_ROUTE09_DREW"),
               (30, 14, "PICNICKER", "UP", 1, "Palm190_RouteHEIDI", "TRAINER_PALM_ROUTE09_HEIDI"),
               (42, 16, "MAN_3", "LEFT", 1, "Palm190_RouteFABIAN", "TRAINER_PALM_ROUTE09_FABIAN")]
R9_ITEMS = [(5, 22, "ITEM_MAGNET", "FLAG_ITEM_ROUTE_116_X_SPECIAL"),                  # mato alto oeste
            (33, 16, "ITEM_THUNDER_STONE", "FLAG_ITEM_ROUTE_117_REVIVE"),             # mato alto ao lado da ferrovia
            (36, 26, "ITEM_ELECTRIC_SEED", "FLAG_ITEM_ROUTE_119_HYPER_POTION_2")]     # patio da subestacao
R9_SIGNS = [(3, 17, "Palm190_SignWest"), (44, 17, "Palm190_SignEast"), (35, 26, "Palm190_SignStation")]
R9_WILD = [("SPECIES_ELECTRIKE", 42, 44), ("SPECIES_BLITZLE", 42, 44), ("SPECIES_SHINX", 42, 44), ("SPECIES_JOLTIK", 42, 44),
           ("SPECIES_HELIOPTILE", 42, 44), ("SPECIES_ELECTRIKE", 43, 45), ("SPECIES_BLITZLE", 43, 45), ("SPECIES_SHINX", 43, 45),
           ("SPECIES_JOLTIK", 43, 45), ("SPECIES_HELIOPTILE", 43, 45), ("SPECIES_LUXIO", 44, 45), ("SPECIES_ELEKID", 42, 44)]


def main():
    # ---------------- Passway: estrada leste aberta (sem a trava) + conexao
    pp = f"{ROOT}/data/maps/PalmPassway/map.json"
    p = jload(pp)
    pbl_l = {l["id"]: l for l in jload(f"{ROOT}/data/layouts/layouts.json")["layouts"] if "id" in l}["LAYOUT_PALM_PASSWAY"]
    import struct
    pbl = struct.unpack(f"<{pbl_l['width'] * pbl_l['height']}H", open(f"{ROOT}/{pbl_l['blockdata_filepath']}", "rb").read())
    seam_check(pbl, PW.W, PW.H, range(10, 28), range(PW.W - 8, PW.W))
    p["coord_events"] = [e for e in p["coord_events"] if e["script"] != "Palm181_EastGate"]
    p["connections"] = [cn for cn in p["connections"] if cn["map"] != "MAP_PALM_ROUTE09"] + \
                       [OD([("map", "MAP_PALM_ROUTE09"), ("offset", 0), ("direction", "right")])]
    jsave(pp, p)

    # ---------------- Route 9
    c9 = R9.compose()
    for (x, y, _) in R9_SIGNS:
        c9.put(x, y, 3, collision=1)
    bl9 = R9.flatten(c9.build())
    seam_check(bl9, c9.w, c9.h, range(c9.h), range(0, 8))
    register("PalmRoute09", "LAYOUT_PALM_ROUTE09", c9, bl9)
    j = map_json("MAP_PALM_ROUTE09", "PalmRoute09", "LAYOUT_PALM_ROUTE09", "MUS_ROUTE110", "MAPSEC_ROUTE_109", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_PASSWAY"), ("offset", 0), ("direction", "left")])])
    for (x, y, gfx, d, sight, script, _) in R9_TRAINERS:
        assert walkable(bl9, c9.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in R9_ITEMS:
        assert walkable(bl9, c9.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s_) for (x, y, s_) in R9_SIGNS]
    j["coord_events"] = [coord(R9.W - 2, y, "Palm190_EastGate") for y in R9.EAST]
    jsave(f"{ROOT}/data/maps/PalmRoute09/map.json", j)
    sc = ["PalmRoute09_MapScripts::\n\t.byte 0\n",
          "Palm190_EastGate::\n\tgoto_if_set FLAG_HT_PASSWAY_EAST_OPEN, Palm190_Ok\n\tlockall\n\tmsgbox Palm190_TextEastGate, MSGBOX_DEFAULT\n"
          "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm190_StepBackWest\n\twaitmovement 0\n\treleaseall\n\tend\n",
          "Palm190_Ok::\n\tend\n", "Palm190_StepBackWest:\n\twalk_left\n\tstep_end\n"]
    for (_, _, _, _, _, script, tid) in R9_TRAINERS:
        k = script.replace("Palm190_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm190_Text{k}Intro, Palm190_Text{k}Loss\n"
                  f"\tmsgbox Palm190_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s_) in R9_SIGNS:
        sc.append(f"{s_}::\n\tmsgbox {s_}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute09/scripts.inc", "w").write("\n".join(sc))

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE09"]
    entry = OD([("map", "MAP_PALM_ROUTE09"), ("base_label", "gPalmRoute09"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s_)])
                                                                    for (s_, a, b) in R9_WILD])]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE08") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch9.txt"], check=True)
    print("Cap. 9 (parte 1) instalado: Route 9", c9.w, "x", c9.h)


if __name__ == "__main__":
    main()
