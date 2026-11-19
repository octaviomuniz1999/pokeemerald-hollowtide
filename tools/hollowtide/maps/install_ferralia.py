#!/usr/bin/env python3
"""Instala a Ferralia gerada (MAP_PALM_FERRALIA, 72x64, General + Rustboro) e a conexao continua com a Route 3.

- conexao: Ferralia (baixo, offset 16) <-> Route 3 (cima, offset -16); remove a ligacao provisoria por warp;
- portas dos predios calculadas a partir do carimbo (offset da porta no mapa da Rustboro); interiores da Rustboro
  religados (Centro Pokemon, Mart, 3 casas, 2 predios residenciais); demais portas ficam fechadas;
- ginasio do Vessel fechado nesta etapa (placa: o lider esta no patio de carga) — gancho de "Carga Desviada";
- placas, moradores com falas de ambiente, ponto de cura e encontros do parque.
Rodar depois de install_route3.py.
"""
import collections, json, os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import ferralia as FE
from canvas import ROOT

OD = collections.OrderedDict
DOOR_OFF = {"rb_gym": [(3, 4)], "rb_house_grey": [(2, 4)], "rb_devon": [(4, 8), (5, 8)], "rb_office_long": [(4, 5)],
            "rb_office_small": [(2, 4)], "rb_office_mid": [(3, 4)], "rb_office_six": [(2, 4)], "rb_apartment": [(2, 8)],
            "rb_pokecenter": [(1, 3)], "rb_mart": [(1, 3)]}
# rotulo do predio -> (mapa interior, pasta). A ordem define o indice do warp.
INTERIORS = [("pc", "MAP_RUSTBORO_CITY_POKEMON_CENTER_1F", "RustboroCity_PokemonCenter_1F"),
             ("mart", "MAP_RUSTBORO_CITY_MART", "RustboroCity_Mart"),
             ("house_nw", "MAP_RUSTBORO_CITY_HOUSE1", "RustboroCity_House1"),
             ("house_n", "MAP_RUSTBORO_CITY_HOUSE2", "RustboroCity_House2"),
             ("house_s", "MAP_RUSTBORO_CITY_HOUSE3", "RustboroCity_House3"),
             ("flat_nw", "MAP_RUSTBORO_CITY_FLAT2_1F", "RustboroCity_Flat2_1F"),
             ("school", "MAP_RUSTBORO_CITY_FLAT1_1F", "RustboroCity_Flat1_1F")]
# moradores (x, y, grafico, movimento, rotulo); falas em tools/hollowtide/text/ch3.txt (rotulo + "_Text")
NPCS = [
    (41, 47, "MAN_3", "MOVEMENT_TYPE_FACE_DOWN", "Palm101_Greeter"),
    (64, 29, "WORKER_M", "MOVEMENT_TYPE_FACE_LEFT", "Palm101_YardWorker"),
    (50, 15, "GENTLEMAN", "MOVEMENT_TYPE_FACE_DOWN", "Palm101_GymFan"),
    (28, 36, "LITTLE_BOY", "MOVEMENT_TYPE_WANDER_AROUND", "Palm101_FountainKid"),
    (45, 39, "MAN_1", "MOVEMENT_TYPE_WANDER_AROUND", "Palm101_Commuter"),
    (12, 20, "WOMAN_2", "MOVEMENT_TYPE_WANDER_AROUND", "Palm101_Resident"),
    (29, 15, "SCIENTIST_1", "MOVEMENT_TYPE_FACE_DOWN", "Palm101_HQGuard"),
    (31, 56, "OLD_WOMAN", "MOVEMENT_TYPE_WANDER_AROUND", "Palm101_ParkLady"),
]
SIGNS_EXTRA = [(39, 47, "Palm101_CitySign"), (45, 11, "Palm101_GymSign"), (27, 14, "Palm101_HQSign"),
               (57, 27, "Palm101_YardSign"), (69, 39, "Palm101_Route4Sign")]
WILD = [("SPECIES_PIDOVE", 20, 22), ("SPECIES_TRUBBISH", 20, 22), ("SPECIES_PIDOVE", 20, 22), ("SPECIES_TRUBBISH", 21, 23),
        ("SPECIES_RATTATA", 20, 22), ("SPECIES_LILLIPUP", 20, 22), ("SPECIES_PIDOVE", 21, 23), ("SPECIES_TRUBBISH", 21, 23),
        ("SPECIES_GRIMER", 21, 23), ("SPECIES_MAGNEMITE", 21, 23), ("SPECIES_KLINK", 22, 23), ("SPECIES_ARON", 22, 23)]


def jload(p):
    return json.load(open(p), object_pairs_hook=OD)


def jsave(p, j):
    open(p, "w").write(json.dumps(j, indent=2, ensure_ascii=False) + "\n")


def sign(x, y, script):
    return OD([("type", "sign"), ("x", x), ("y", y), ("elevation", 0), ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", script)])


def main():
    c = FE.compose()
    for (x, y, _) in SIGNS_EXTRA:
        c.put(x, y, 3, collision=1)
    bl = c.build()
    w = c.w
    d = f"{ROOT}/data/layouts/PalmFerralia"
    open(f"{d}/map.bin", "wb").write(struct.pack(f"<{len(bl)}H", *bl))
    open(f"{d}/border.bin", "wb").write(struct.pack("<4H", *[m | (3 << 12) for m in (468, 469, 476, 477)]))
    lay = jload(f"{ROOT}/data/layouts/layouts.json")
    for l in lay["layouts"]:
        if l.get("id") == "LAYOUT_PALM_FERRALIA":
            l["width"], l["height"] = c.w, c.h
            l["primary_tileset"], l["secondary_tileset"] = c.primary, c.secondary
    jsave(f"{ROOT}/data/layouts/layouts.json", lay)

    pos = {label: (name, x, y) for (name, x, y, label) in FE.BUILDINGS}
    def door(label, i=0):
        name, x, y = pos[label]
        dx, dy = DOOR_OFF[name][i]
        return (x + dx, y + dy)

    p = f"{ROOT}/data/maps/PalmFerralia/map.json"
    j = jload(p)
    j["music"] = "MUS_RUSTBORO"
    j["region_map_section"] = "MAPSEC_RUSTBORO_CITY"
    j["map_type"] = "MAP_TYPE_CITY"
    j["connections"] = [OD([("map", "MAP_PALM_ROUTE03"), ("offset", FE.OFFSET_ROUTE3), ("direction", "down")])]
    j["object_events"] = []
    for (x, y, gfx, mv, label) in NPCS:
        v = bl[y * w + x]
        assert (v >> 10) & 3 == 0, f"morador {label} em tile bloqueado {(x, y)}"
        rng = 1 if "WANDER" in mv else 0
        j["object_events"].append(OD([("graphics_id", f"OBJ_EVENT_GFX_{gfx}"), ("x", x), ("y", y), ("elevation", 3),
                                      ("movement_type", mv), ("movement_range_x", rng), ("movement_range_y", rng),
                                      ("trainer_type", "TRAINER_TYPE_NONE"), ("trainer_sight_or_berry_tree_id", "0"),
                                      ("script", label), ("flag", "0")]))
    j["warp_events"] = []
    for (label, dm, _) in INTERIORS:
        x, y = door(label)
        j["warp_events"].append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]))
    j["coord_events"] = []
    pcx, pcy = pos["pc"][1:]; mx, my = pos["mart"][1:]
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in SIGNS_EXTRA] + \
        [sign(pcx + 2, pcy + 3, "Common_EventScript_ShowPokemonCenterSign"), sign(pcx + 3, pcy + 3, "Common_EventScript_ShowPokemonCenterSign"),
         sign(mx + 2, my + 3, "Common_EventScript_ShowPokemartSign"), sign(mx + 3, my + 3, "Common_EventScript_ShowPokemartSign")]
    jsave(p, j)

    # interiores: saidas para a Ferralia
    for idx, (_, _, folder) in enumerate(INTERIORS):
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = jload(q)
        for wv in k["warp_events"]:
            if wv["dest_map"] in ("MAP_RUSTBORO_CITY", "MAP_PALM_FERRALIA"):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_FERRALIA", str(idx)
        jsave(q, k)

    # ponto de cura: na frente do Centro Pokemon
    hp = f"{ROOT}/src/data/heal_locations.json"
    h = jload(hp)
    for e in h["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_RUSTBORO_CITY":
            e["map"], e["x"], e["y"] = "MAP_PALM_FERRALIA", door("pc")[0], door("pc")[1] + 1
    jsave(hp, h)

    # Route 3: a saida norte vira conexao (sai a ligacao provisoria por warp)
    rp = f"{ROOT}/data/maps/PalmRoute03/map.json"
    r = jload(rp)
    r["connections"] = [cn for cn in r["connections"] if cn["map"] != "MAP_PALM_FERRALIA"] + \
                       [OD([("map", "MAP_PALM_FERRALIA"), ("offset", -FE.OFFSET_ROUTE3), ("direction", "up")])]
    r["coord_events"] = [e for e in r["coord_events"] if e["script"] != "Palm100_ToFerralia"]
    jsave(rp, r)

    # scripts da Ferralia (codigo aqui; textos em ch3.txt)
    sc = ["PalmFerralia_MapScripts::\n\t.byte 0\n"]
    for (_, _, _, _, label) in NPCS:
        sc.append(f"{label}::\n\tmsgbox {label}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s) in SIGNS_EXTRA:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmFerralia/scripts.inc", "w").write("\n".join(sc))

    # encontros do parque
    wp = f"{ROOT}/src/data/wild_encounters.json"
    wj = jload(wp)
    grp = wj["wild_encounter_groups"][0]
    grp["encounters"] = [e for e in grp["encounters"] if e.get("map") != "MAP_PALM_FERRALIA"]
    entry = OD([("map", "MAP_PALM_FERRALIA"), ("base_label", "gPalmFerralia"),
                ("land_mons", OD([("encounter_rate", 15), ("mons", [OD([("min_level", a), ("max_level", b), ("species", s)])
                                                                    for (s, a, b) in WILD])]))])
    idx = next(i for i, e in enumerate(grp["encounters"]) if e.get("map") == "MAP_PALM_ROUTE03") + 1
    grp["encounters"].insert(idx, entry)
    jsave(wp, wj)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch3.txt"], check=True)
    print("Ferralia instalada:", c.w, "x", c.h, "| portas:", [(l, door(l)) for (l, _, _) in INTERIORS])


if __name__ == "__main__":
    main()
