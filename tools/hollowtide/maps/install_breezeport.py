#!/usr/bin/env python3
"""Instala a Breezeport gerada no jogo (mapa MAP_PALM_BRISA), de forma reproduzivel.

- salva o layout LAYOUT_PALM_BREEZEPORT (72x56, General + Lilycove) e aponta o mapa para ele;
- gera warps a partir das portas detectadas e religa os interiores (saidas apontando de volta);
- porta os eventos da Brisa: postes do festival (3 postes apagados), Teatro trancado ate religar a luz,
  entrada norte (Route 2), saida oeste pela praia (Route 3, travada ate a Jay), placas e anfitria;
- atualiza o ponto de cura (HEAL_LOCATION_DEWFORD_TOWN passa a ser a Breezeport).
"""
import collections, json, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import breezeport as BZ
from canvas import ROOT

OD = collections.OrderedDict
# (porta) -> interior; a ordem define o indice do warp (Teatro precisa ser 0: PalmTeatro sai para o warp 0)
DOORS = [
    ((47, 27), "MAP_PALM_TEATRO", "PalmTeatro"),
    ((23, 16), "MAP_DEWFORD_TOWN_POKEMON_CENTER_1F", "DewfordTown_PokemonCenter_1F"),
    ((14, 16), "MAP_SLATEPORT_CITY_MART", "SlateportCity_Mart"),
    ((56, 33), "MAP_LILYCOVE_CITY_DEPARTMENT_STORE_1F", "LilycoveCity_DepartmentStore_1F"),
    ((4, 24), "MAP_LILYCOVE_CITY_HOUSE1", "LilycoveCity_House1"),
    ((15, 24), "MAP_LILYCOVE_CITY_HOUSE2", "LilycoveCity_House2"),
    ((4, 30), "MAP_LILYCOVE_CITY_HOUSE3", "LilycoveCity_House3"),
    ((15, 30), "MAP_LILYCOVE_CITY_HOUSE4", "LilycoveCity_House4"),
    ((55, 24), "MAP_DEWFORD_TOWN_HOUSE1", "DewfordTown_House1"),
    ((64, 24), "MAP_DEWFORD_TOWN_HOUSE2", "DewfordTown_House2"),
    ((64, 30), "MAP_LILYCOVE_CITY_MOVE_DELETERS_HOUSE", "LilycoveCity_MoveDeletersHouse"),
]
LAMPS = [(12, 20), (33, 21), (60, 34)]   # topo dos 3 postes do festival (base logo abaixo)
THEATER_DOOR = (47, 27)


def coord(x, y, script):
    return OD([("type", "trigger"), ("x", x), ("y", y), ("elevation", 3), ("var", "VAR_TEMP_0"), ("var_value", "0"), ("script", script)])


def sign(x, y, script):
    return OD([("type", "sign"), ("x", x), ("y", y), ("elevation", 0), ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", script)])


def main():
    c = BZ.compose()
    # postes do festival: comecam apagados (584); a base (674) e solida
    for (x, y) in LAMPS:
        c.put(x, y, 584, collision=0)
        c.put(x, y + 1, 674, collision=1, elevation=0)
    bl = c.save("PalmBreezeport")
    w = c.w
    lay = json.load(open(f"{ROOT}/data/layouts/layouts.json"), object_pairs_hook=OD)
    entry = OD([("id", "LAYOUT_PALM_BREEZEPORT"), ("name", "PalmBreezeport_Layout"), ("width", c.w), ("height", c.h),
                ("primary_tileset", c.primary), ("secondary_tileset", c.secondary),
                ("border_filepath", "data/layouts/PalmBreezeport/border.bin"),
                ("blockdata_filepath", "data/layouts/PalmBreezeport/map.bin"), ("layout_version", "emerald")])
    lay["layouts"] = [l for l in lay["layouts"] if l.get("id") != "LAYOUT_PALM_BREEZEPORT"] + [entry]
    open(f"{ROOT}/data/layouts/layouts.json", "w").write(json.dumps(lay, indent=2, ensure_ascii=False) + "\n")

    # porta do Teatro (para trancar/destrancar via script)
    door_mt = bl[THEATER_DOOR[1] * w + THEATER_DOOR[0]] & 0x3FF
    wall_mt = bl[THEATER_DOOR[1] * w + THEATER_DOOR[0] - 1] & 0x3FF

    p = f"{ROOT}/data/maps/PalmBrisa/map.json"
    j = json.load(open(p), object_pairs_hook=OD)
    j["layout"] = "LAYOUT_PALM_BREEZEPORT"
    j["music"] = "MUS_SLATEPORT"
    j["object_events"] = [OD([("graphics_id", "OBJ_EVENT_GFX_WOMAN_2"), ("x", 45), ("y", 29), ("elevation", 3),
                              ("movement_type", "MOVEMENT_TYPE_FACE_DOWN"), ("movement_range_x", 0), ("movement_range_y", 0),
                              ("trainer_type", "TRAINER_TYPE_NONE"), ("trainer_sight_or_berry_tree_id", "0"),
                              ("script", "Palm080_BrisaHost"), ("flag", "0")])]
    j["warp_events"] = [OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]) for (x, y), dm, _ in DOORS]
    j["coord_events"] = [coord(x, 0, "Palm080_ReturnRoute") for x in range(18, 22)] + \
                        [coord(0, y, "Palm090_ToRoute03") for y in range(38, 45)]
    j["bg_events"] = [sign(22, 3, "Palm080_BrisaSign"), sign(50, 28, "Palm090_TheaterSign"), sign(27, 21, "Palm090_PalmPoster"),
                      sign(2, 37, "Palm090_EastSign"), sign(62, 43, "Palm092_KeeperHouse")] + \
                     [sign(x, y + 1, f"Palm090_CityLamp{i + 1}") for i, (x, y) in enumerate(LAMPS)]
    open(p, "w").write(json.dumps(j, indent=2, ensure_ascii=False) + "\n")

    # interiores: saidas apontam para a Breezeport
    for idx, (_, dm, folder) in enumerate(DOORS):
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = json.load(open(q), object_pairs_hook=OD)
        for wv in k["warp_events"]:
            if wv["dest_map"].startswith(("MAP_DEWFORD_TOWN", "MAP_SLATEPORT_CITY", "MAP_LILYCOVE_CITY", "MAP_PALM_BRISA")) and \
               not any(s in wv["dest_map"] for s in ("_2F", "_ELEVATOR", "_POKEMON_CENTER")):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_BRISA", str(idx)
        open(q, "w").write(json.dumps(k, indent=2, ensure_ascii=False) + "\n")

    # ponto de cura
    hp = f"{ROOT}/src/data/heal_locations.json"
    h = json.load(open(hp), object_pairs_hook=OD)
    for e in h["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_DEWFORD_TOWN":
            e["map"], e["x"], e["y"] = "MAP_PALM_BRISA", 23, 17
    open(hp, "w").write(json.dumps(h, indent=2, ensure_ascii=False) + "\n")

    # scripts: coordenadas novas de postes, Teatro e chegadas
    sp = f"{ROOT}/data/maps/PalmBrisa/scripts.inc"
    s = open(sp).read()
    for i, (x, y) in enumerate(LAMPS, 1):
        s = re.sub(rf"(Palm090_DrawLamp{i}::\n\tsetmetatile )\d+, \d+, \d+, (TRUE|FALSE)", rf"\g<1>{x}, {y}, 576, FALSE", s)
    s = re.sub(r"(Palm090_OpenTheater::\n\tsetmetatile )\d+, \d+, \d+, TRUE", rf"\g<1>{THEATER_DOOR[0]}, {THEATER_DOOR[1]}, {door_mt}, TRUE", s)
    if "Palm090_LockTheater::" not in s:
        s = s.replace("\tcall_if_set FLAG_PALM_BRISA_LIGHTS, Palm090_OpenTheater\n",
                      "\tcall_if_set FLAG_PALM_BRISA_LIGHTS, Palm090_OpenTheater\n\tcall_if_unset FLAG_PALM_BRISA_LIGHTS, Palm090_LockTheater\n")
        s += f"\nPalm090_LockTheater::\n\tsetmetatile {THEATER_DOOR[0]}, {THEATER_DOOR[1]}, {wall_mt}, TRUE\n\treturn\n"
    if "Palm092_KeeperHouse::" not in s:
        s += "\nPalm092_KeeperHouse::\n\tmsgbox Palm092_TextKeeperHouse, MSGBOX_SIGN\n\tend\n\nPalm092_TextKeeperHouse:\n\t.string \"LIGHTHOUSE KEEPER'S HOUSE$\"\n"
    open(sp, "w").write(s)
    for f, old, new in [("PalmRoute02", r"warp MAP_PALM_BRISA, \d+, \d+", "warp MAP_PALM_BRISA, 19, 2"),
                        ("PalmRoute03", r"warp MAP_PALM_BRISA, \d+, \d+", "warp MAP_PALM_BRISA, 2, 41")]:
        q = f"{ROOT}/data/maps/{f}/scripts.inc"
        txt = re.sub(old, new, open(q).read())  # le antes de abrir para escrita
        open(q, "w").write(txt)
    print("Breezeport instalada:", c.w, "x", c.h, "| porta do teatro", door_mt, "-> parede", wall_mt)


if __name__ == "__main__":
    main()
