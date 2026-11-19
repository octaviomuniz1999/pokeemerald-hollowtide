#!/usr/bin/env python3
"""Instala a Route 3 gerada (MAP_PALM_ROUTE03) e a conexao continua Breezeport <-> Route 3.

- layout LAYOUT_PALM_ROUTE03 (56x80, General + Lilycove), patamares achatados para elevacao 3 (ver route3.py);
- conexao: Route 3 (direita, offset 20) <-> Breezeport (esquerda, offset -20). A trava antes da Jay continua na
  borda oeste da Breezeport (gatilho que faz o jogador recuar um passo) — gravada por install_breezeport.py;
- norte: conexao continua com a Ferralia (offset -16; a emenda do lado da cidade e o parque, so primario);
- 5 treinadores com visao (slots de Hoenn sem acesso em Lunia), 3 itens, 2 placas, encontros do Cap. 3.
Rodar depois de install_breezeport.py.
"""
import collections, json, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route3 as R3
from canvas import ROOT

OD = collections.OrderedDict
SIGN_GRASS = 3
# (x, y, grafico, direcao, visao, script)
TRAINERS = [
    (36, 62, "FISHERMAN", "LEFT", 4, "Palm100_RouteRUI"),          # praia, perto da casa
    (43, 44, "BUG_CATCHER", "LEFT", 3, "Palm100_RouteTOMAS"),      # encosta, de olho na trilha logo acima da escada
    (12, 26, "HIKER", "RIGHT", 3, "Palm100_RouteBENTO"),           # trilha alternativa da mata
    (33, 30, "PICNICKER", "LEFT", 2, "Palm100_RouteIARA"),         # serra, trilha principal
    (30, 8, "CAMPER", "DOWN", 2, "Palm100_RouteDAVI"),             # planalto, beira da estrada
]
TRAINER_IDS = {"RUI": "TRAINER_PALM_ROUTE03_RUI", "TOMAS": "TRAINER_PALM_ROUTE03_TOMAS", "BENTO": "TRAINER_PALM_ROUTE03_BENTO",
               "IARA": "TRAINER_PALM_ROUTE03_IARA", "DAVI": "TRAINER_PALM_ROUTE03_DAVI"}
# flags de itens de mapas de Hoenn sem acesso em Lunia
ITEMS = [(3, 74, "ITEM_BIG_PEARL", "FLAG_ITEM_ROUTE_123_CALCIUM"),          # ponta de areia escondida (oeste)
         (18, 29, "ITEM_GREAT_BALL", "FLAG_ITEM_ROUTE_123_ULTRA_BALL"),     # clareira da trilha alternativa
         (8, 9, "ITEM_REVIVE", "FLAG_ITEM_ROUTE_123_ELIXIR")]              # planalto, junto ao mato alto
SIGNS = [(42, 54, "Palm100_SignBeach"), (28, 3, "Palm100_SignPlateau")]
FERRALIA_ARRIVAL = (1, 10)
ROUTE3_FROM_FERRALIA = (25, 2)
WILD = [("SPECIES_WINGULL", 17, 19), ("SPECIES_PIKIPEK", 17, 19), ("SPECIES_AIPOM", 18, 20), ("SPECIES_COMBEE", 17, 19),
        ("SPECIES_VENIPEDE", 17, 19), ("SPECIES_HOPPIP", 18, 20), ("SPECIES_MAREEP", 18, 20), ("SPECIES_LILLIPUP", 18, 20),
        ("SPECIES_SANDYGAST", 18, 20), ("SPECIES_SKIDDO", 19, 21), ("SPECIES_NINCADA", 19, 21), ("SPECIES_PANSAGE", 19, 21)]


def jload(p):
    return json.load(open(p), object_pairs_hook=OD)


def jsave(p, j):
    open(p, "w").write(json.dumps(j, indent=2, ensure_ascii=False) + "\n")


def obj(gfx, x, y, mv, ttype, sight, script, flag="0"):
    return OD([("graphics_id", gfx), ("x", x), ("y", y), ("elevation", 3), ("movement_type", mv),
               ("movement_range_x", 0), ("movement_range_y", 0), ("trainer_type", ttype),
               ("trainer_sight_or_berry_tree_id", str(sight)), ("script", script), ("flag", flag)])


def coord(x, y, script):
    return OD([("type", "trigger"), ("x", x), ("y", y), ("elevation", 3), ("var", "VAR_TEMP_0"), ("var_value", "0"), ("script", script)])


def main():
    c = R3.compose()
    for (x, y, _) in SIGNS:
        c.put(x, y, SIGN_GRASS, 1, 3)
    bl = R3.flatten(c.build())
    w = c.w
    d = f"{ROOT}/data/layouts/PalmRoute03"
    open(f"{d}/map.bin", "wb").write(struct.pack(f"<{len(bl)}H", *bl))
    open(f"{d}/border.bin", "wb").write(struct.pack("<4H", *[m | (3 << 12) for m in (468, 469, 476, 477)]))
    lay = jload(f"{ROOT}/data/layouts/layouts.json")
    for l in lay["layouts"]:
        if l.get("id") == "LAYOUT_PALM_ROUTE03":
            l["width"], l["height"] = c.w, c.h
            l["primary_tileset"], l["secondary_tileset"] = c.primary, c.secondary
    jsave(f"{ROOT}/data/layouts/layouts.json", lay)

    def walkable(x, y):
        v = bl[y * w + x]
        return (v >> 10) & 3 == 0

    p = f"{ROOT}/data/maps/PalmRoute03/map.json"
    j = jload(p)
    j["music"] = "MUS_ROUTE110"
    j["region_map_section"] = "MAPSEC_ROUTE_103"
    j["connections"] = [OD([("map", "MAP_PALM_BRISA"), ("offset", R3.OFFSET_BREEZEPORT), ("direction", "right")]),
                        OD([("map", "MAP_PALM_FERRALIA"), ("offset", -16), ("direction", "up")])]   # ver ferralia.py
    j["object_events"] = []
    for (x, y, gfx, dr, sight, script) in TRAINERS:
        assert walkable(x, y), f"treinador {script} em tile bloqueado {(x, y)}"
        j["object_events"].append(obj(f"OBJ_EVENT_GFX_{gfx}", x, y, f"MOVEMENT_TYPE_FACE_{dr}", "TRAINER_TYPE_NORMAL", sight, script))
    for (x, y, item, flag) in ITEMS:
        assert walkable(x, y), f"item {item} em tile bloqueado {(x, y)}"
        j["object_events"].append(obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN", "TRAINER_TYPE_NONE", item,
                                      "Common_EventScript_FindItem", flag))
    j["warp_events"] = []
    j["coord_events"] = []
    j["bg_events"] = [OD([("type", "sign"), ("x", x), ("y", y), ("elevation", 0),
                          ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", s)]) for (x, y, s) in SIGNS]
    jsave(p, j)

    # scripts (texto em tools/hollowtide/text/ch3.txt, aplicado por texts.py)
    sc = ["PalmRoute03_MapScripts::\n\t.byte 0\n",
          "Palm100_SignBeach::\n\tmsgbox Palm100_TextSignBeach, MSGBOX_SIGN\n\tend\n",
          "Palm100_SignPlateau::\n\tmsgbox Palm100_TextSignPlateau, MSGBOX_SIGN\n\tend\n"]
    for k, tid in TRAINER_IDS.items():
        sc.append(f"Palm100_Route{k}::\n\ttrainerbattle_single {tid}, Palm100_Text{k}Intro, Palm100_Text{k}Loss\n"
                  f"\tmsgbox Palm100_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    open(f"{ROOT}/data/maps/PalmRoute03/scripts.inc", "w").write("\n".join(sc))

    # encontros
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_ROUTE03"]
    entry = OD([("map", "MAP_PALM_ROUTE03"), ("base_label", "gPalmRoute03"),
                ("land_mons", OD([("encounter_rate", 20), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s)])
                                                                    for (s, a, b) in WILD])]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE02") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    # textos (o scripts.inc acabou de ser reescrito sem eles)
    import subprocess
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch3.txt"], check=True)
    print("Route 3 instalada:", c.w, "x", c.h)


if __name__ == "__main__":
    main()
