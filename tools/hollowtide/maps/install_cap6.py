#!/usr/bin/env python3
"""Capitulo 6: instala a Route 6 (MAP_PALM_ROUTE06) e Serenia (MAP_PALM_SERENIA), mapas novos.

- conexoes continuas Pillarton (direita) <-> Route 6 <-> Serenia (offset 0); a emenda Pillarton/Route 6 so
  mostra primario (parque leste da Pillarton e lado oeste da rota); Route 6 e Serenia usam General + Lavaridge;
- trava na borda leste da Pillarton ate a Insignia dos Pilares;
- Route 6: Ren, Mika, Sayo e Hana, 3 itens, placas, encontros do Cap. 6;
- Serenia ("O Jardim das Lembrancas"): Jade e o Espeon Lau recebem o jogador; tres ilusoes (pedras que
  fecham as duas faixas da trilha da fonte) se desfazem depois do encontro; o fragmento roubado esta no
  patio; devolvido ao altar da fonte, revela a inscricao ("convocar a mare sobre as montanhas");
  ginasio da Jade fechado nesta etapa. Centro Pokemon, Mart e 3 casas (interiores de Fortree).
Rodar depois de install_pillarton.py.
"""
import collections, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route6 as R6, serenia as SE, pillarton as PL
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable

OD = collections.OrderedDict
R6_TRAINERS = [(24, 13, "PSYCHIC_M", "DOWN", 1, "Palm140_RouteREN", "TRAINER_PALM_ROUTE06_REN"),
               (8, 19, "LASS", "DOWN", 1, "Palm140_RouteMIKA", "TRAINER_PALM_ROUTE06_MIKA"),
               (32, 18, "HEX_MANIAC", "LEFT", 1, "Palm140_RouteSAYO", "TRAINER_PALM_ROUTE06_SAYO"),
               (45, 19, "WOMAN_5", "DOWN", 1, "Palm140_RouteHANA", "TRAINER_PALM_ROUTE06_HANA")]
R6_ITEMS = [(22, 7, "ITEM_TWISTED_SPOON", "FLAG_ITEM_ROUTE_127_ZINC"),
            (50, 4, "ITEM_PP_UP", "FLAG_ITEM_ROUTE_127_CARBOS"),
            (3, 32, "ITEM_REVIVE", "FLAG_ITEM_ROUTE_132_RARE_CANDY")]
R6_SIGNS = [(3, 19, "Palm140_SignWest"), (50, 19, "Palm140_SignEast"), (12, 18, "Palm140_Shrine")]
R6_WILD = [("SPECIES_RALTS", 30, 32), ("SPECIES_CHINGLING", 30, 32), ("SPECIES_NATU", 30, 32), ("SPECIES_ESPURR", 30, 32),
           ("SPECIES_SNUBBULL", 30, 32), ("SPECIES_PETILIL", 30, 32), ("SPECIES_COTTONEE", 31, 33), ("SPECIES_NATU", 31, 33),
           ("SPECIES_ESPURR", 31, 33), ("SPECIES_COTTONEE", 31, 33), ("SPECIES_CHIMECHO", 32, 33), ("SPECIES_RALTS", 32, 33)]

SE_DOOR_OFF = {"lav_pokecenter": (1, 3), "lav_mart": (1, 3), "lav_gym": (3, 4), "lav_house": (1, 3), "lav_house2": (1, 3)}
SE_INTERIORS = [("pc", "MAP_FORTREE_CITY_POKEMON_CENTER_1F", "FortreeCity_PokemonCenter_1F", "MAP_FORTREE_CITY"),
                ("mart", "MAP_FORTREE_CITY_MART", "FortreeCity_Mart", "MAP_FORTREE_CITY"),
                ("house_1", "MAP_FORTREE_CITY_HOUSE1", "FortreeCity_House1", "MAP_FORTREE_CITY"),
                ("house_2", "MAP_FORTREE_CITY_HOUSE2", "FortreeCity_House2", "MAP_FORTREE_CITY"),
                ("house_3", "MAP_FORTREE_CITY_HOUSE3", "FortreeCity_House3", "MAP_FORTREE_CITY")]
SE_NPCS = [  # (x, y, grafico, movimento, script, flag de sumir)
    (22, 19, "LIZA", "MOVEMENT_TYPE_FACE_LEFT", "Palm141_Jade", "0"),
    (23, 19, "OBJ_EVENT_GFX_SPECIES(ESPEON)", "MOVEMENT_TYPE_FACE_LEFT", "Palm141_Lau", "0"),
    (21, 8, "ITEM_BALL", "MOVEMENT_TYPE_FACE_DOWN", "Palm141_Fragment", "FLAG_HT_SERENIA_FRAGMENT"),
    (10, 24, "OLD_WOMAN", "MOVEMENT_TYPE_FACE_DOWN", "Palm141_Elder", "0"),
    (28, 22, "LITTLE_GIRL", "MOVEMENT_TYPE_WANDER_AROUND", "Palm141_Girl", "0"),
    (36, 21, "MAN_2", "MOVEMENT_TYPE_FACE_UP", "Palm141_GymGuard", "0"),
    (13, 33, "GENTLEMAN", "MOVEMENT_TYPE_FACE_UP", "Palm141_Gardener", "0"),
]
SE_SIGNS = [(3, 19, "Palm141_TownSign"), (32, 19, "Palm141_GymSign"), (24, 9, "Palm141_SpringSign")]
ILLUSION_FLAGS = ["FLAG_HT_SERENIA_ILLUSION_1", "FLAG_HT_SERENIA_ILLUSION_2", "FLAG_HT_SERENIA_ILLUSION_3"]


def main():
    # ---------------- Route 6
    c6 = R6.compose()
    for (x, y, _) in R6_SIGNS:
        c6.put(x, y, 3, collision=1)
    bl6 = c6.build()
    register("PalmRoute06", "LAYOUT_PALM_ROUTE06", c6, bl6)
    j = map_json("MAP_PALM_ROUTE06", "PalmRoute06", "LAYOUT_PALM_ROUTE06", "MUS_ROUTE120", "MAPSEC_ROUTE_106", "MAP_TYPE_ROUTE",
                 [OD([("map", "MAP_PALM_PILLARTON"), ("offset", 0), ("direction", "left")]),
                  OD([("map", "MAP_PALM_SERENIA"), ("offset", 0), ("direction", "right")])])
    for (x, y, gfx, d, sight, script, _) in R6_TRAINERS:
        assert walkable(bl6, c6.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    for (x, y, item, flag) in R6_ITEMS:
        assert walkable(bl6, c6.w, x, y), (item, x, y)
        j["object_events"].append(obj("ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "Common_EventScript_FindItem", sight=item, flag=flag))
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in R6_SIGNS]
    jsave(f"{ROOT}/data/maps/PalmRoute06/map.json", j)
    sc = ["PalmRoute06_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, _, script, tid) in R6_TRAINERS:
        k = script.replace("Palm140_Route", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm140_Text{k}Intro, Palm140_Text{k}Loss\n"
                  f"\tmsgbox Palm140_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for (_, _, s) in R6_SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute06/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Serenia
    cs = SE.compose()
    for (x, y, _) in SE_SIGNS:
        cs.put(x, y, 3, collision=1)
    bls = cs.build()
    register("PalmSerenia", "LAYOUT_PALM_SERENIA", cs, bls)
    j = map_json("MAP_PALM_SERENIA", "PalmSerenia", "LAYOUT_PALM_SERENIA", "MUS_LILYCOVE", "MAPSEC_FALLARBOR_TOWN", "MAP_TYPE_TOWN",
                 [OD([("map", "MAP_PALM_ROUTE06"), ("offset", 0), ("direction", "left")])])
    for (x, y, gfx, mv, script, flag) in SE_NPCS:
        assert walkable(bls, cs.w, x, y), (script, x, y)
        g = gfx if gfx.startswith("OBJ_") else gfx
        j["object_events"].append(obj(g, x, y, mv, script, flag=flag, rng=1 if "WANDER" in mv else 0))
    for i, (x, y) in enumerate(SE.ILLUSIONS):
        for dx in (0, 1):
            assert walkable(bls, cs.w, x + dx, y), ("ilusao", x + dx, y)
            j["object_events"].append(obj("PUSHABLE_BOULDER", x + dx, y, "MOVEMENT_TYPE_NONE", f"Palm141_Illusion{i + 1}", flag=ILLUSION_FLAGS[i]))
    local = collections.defaultdict(list)
    for i, e in enumerate(j["object_events"]):
        local[e["script"]].append(i + 1)
    pos = {label: (name, x, y) for (name, x, y, label) in SE.BUILDINGS}
    def door(label):
        name, x, y = pos[label]
        dx, dy = SE_DOOR_OFF[name]
        return x + dx, y + dy
    for (label, dm, _, _) in SE_INTERIORS:
        x, y = door(label)
        j["warp_events"].append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]))
    sx, sy = pos["spring"][1:]
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in SE_SIGNS] + [sign(sx + 2, sy + 4, "Palm141_Altar"), sign(sx + 3, sy + 4, "Palm141_Altar")]
    jsave(f"{ROOT}/data/maps/PalmSerenia/map.json", j)
    for idx, (_, _, folder, old) in enumerate(SE_INTERIORS):
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = jload(q)
        for wv in k["warp_events"]:
            if wv["dest_map"] in (old, "MAP_PALM_SERENIA"):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_SERENIA", str(idx)
        jsave(q, k)
    hp = f"{ROOT}/src/data/heal_locations.json"
    h = jload(hp)
    for e in h["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_FORTREE_CITY":
            e["map"], e["x"], e["y"] = "MAP_PALM_SERENIA", door("pc")[0], door("pc")[1] + 1
    jsave(hp, h)
    gx, gy = door("gym")
    wall_mt = bls[gy * cs.w + gx - 1] & 0x3FF
    sc = ["PalmSerenia_MapScripts::\n\tmap_script MAP_SCRIPT_ON_LOAD, Palm141_Load\n\t.byte 0\n",
          f"Palm141_Load::\n\tsetmetatile {gx}, {gy}, {wall_mt}, TRUE\n\tend\n",       # ginasio da Jade fechado nesta etapa
          "Palm141_Jade::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_HT_SERENIA_DONE, Palm141_JadeDone\n"
          "\tgoto_if_set FLAG_HT_SERENIA_JADE_MET, Palm141_JadeAgain\n\tmsgbox Palm141_TextJadeMeet, MSGBOX_DEFAULT\n"
          "\tsetflag FLAG_HT_SERENIA_JADE_MET\n\trelease\n\tend\n",
          "Palm141_JadeAgain::\n\tmsgbox Palm141_TextJadeAgain, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm141_JadeDone::\n\tmsgbox Palm141_TextJadeDone, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm141_Lau::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_ESPEON, CRY_MODE_NORMAL\n\tmsgbox Palm141_TextLau, MSGBOX_DEFAULT\n"
          "\twaitmoncry\n\trelease\n\tend\n",
          "Palm141_Fragment::\n\tlock\n\tmsgbox Palm141_TextFragment, MSGBOX_DEFAULT\n\tsetflag FLAG_HT_SERENIA_FRAGMENT\n"
          f"\tremoveobject {local['Palm141_Fragment'][0]}\n\trelease\n\tend\n",
          "Palm141_Altar::\n\tlockall\n\tgoto_if_set FLAG_HT_SERENIA_DONE, Palm141_AltarDone\n"
          "\tgoto_if_set FLAG_HT_SERENIA_FRAGMENT, Palm141_AltarPlace\n\tmsgbox Palm141_TextAltarEmpty, MSGBOX_DEFAULT\n\treleaseall\n\tend\n",
          "Palm141_AltarPlace::\n\tmsgbox Palm141_TextAltarPlace, MSGBOX_DEFAULT\n\tplayse SE_M_CONFUSE_RAY\n\twaitse\n"
          "\tmsgbox Palm141_TextInscription, MSGBOX_DEFAULT\n\tsetflag FLAG_HT_SERENIA_DONE\n\treleaseall\n\tend\n",
          "Palm141_AltarDone::\n\tmsgbox Palm141_TextInscription, MSGBOX_DEFAULT\n\treleaseall\n\tend\n"]
    for i, fl in enumerate(ILLUSION_FLAGS, 1):
        ids = local[f"Palm141_Illusion{i}"]
        sc.append(f"Palm141_Illusion{i}::\n\tlockall\n\tgoto_if_unset FLAG_HT_SERENIA_JADE_MET, Palm141_IllusionSolid\n"
                  f"\tmsgbox Palm141_TextIllusion, MSGBOX_DEFAULT\n\tplayse SE_M_TELEPORT\n\tsetflag {fl}\n"
                  + "".join(f"\tremoveobject {k}\n" for k in ids) + "\treleaseall\n\tend\n")
    sc.append("Palm141_IllusionSolid::\n\tmsgbox Palm141_TextIllusionSolid, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    for (_, _, _, _, script, _) in SE_NPCS:
        if script in ("Palm141_Elder", "Palm141_Girl", "Palm141_GymGuard", "Palm141_Gardener"):
            sc.append(f"{script}::\n\tmsgbox {script}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s) in SE_SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmSerenia/scripts.inc", "w").write("\n".join(sc))

    # ---------------- Pillarton: conexao leste + trava ate a Insignia dos Pilares
    pp = f"{ROOT}/data/maps/PalmPillarton/map.json"
    p = jload(pp)
    p["connections"] = [cn for cn in p["connections"] if cn["map"] != "MAP_PALM_ROUTE06"] + \
                       [OD([("map", "MAP_PALM_ROUTE06"), ("offset", 0), ("direction", "right")])]
    p["coord_events"] = [e for e in p["coord_events"] if e["script"] != "Palm142_EastGate"] + \
                        [coord(PL.W - 2, y, "Palm142_EastGate") for y in PL.EAST_ROAD]
    jsave(pp, p)
    ps = f"{ROOT}/data/maps/PalmPillarton/scripts.inc"
    t = open(ps).read()
    if "Palm142_EastGate::" not in t:
        t = t.rstrip("\n") + ("\n\nPalm142_EastGate::\n\tgoto_if_set FLAG_BADGE04_GET, Palm142_EastGateOk\n\tlockall\n"
                              "\tmsgbox Palm142_TextEastGate, MSGBOX_DEFAULT\n\tapplymovement OBJ_EVENT_ID_PLAYER, Palm142_StepBackWest\n"
                              "\twaitmovement 0\n\treleaseall\n\tend\n\nPalm142_EastGateOk::\n\tend\n\n"
                              "Palm142_StepBackWest:\n\twalk_left\n\tstep_end\n")
        open(ps, "w").write(t)

    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE06"]
    entry = OD([("map", "MAP_PALM_ROUTE06"), ("base_label", "gPalmRoute06"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s)])
                                                                    for (s, a, b) in R6_WILD])]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE05") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch6.txt"], check=True)
    print("Cap. 6 instalado: Route 6", c6.w, "x", c6.h, "| Serenia", cs.w, "x", cs.h, "| portas", [(l, door(l)) for (l, _, _, _) in SE_INTERIORS])


if __name__ == "__main__":
    main()
