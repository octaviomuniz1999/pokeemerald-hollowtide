#!/usr/bin/env python3
"""Capitulo 5 (parte 2): instala Pillarton (MAP_PALM_PILLARTON, mapa novo) e abre o fim norte da Route 5.

- conexao continua Route 5 (cima, offset -4) <-> Pillarton (baixo, offset 4); a emenda do lado da cidade e o
  parque (so primario nas linhas que a rota enxerga);
- "A Cidade das Aguas Presas": dois recrutas na crista da barragem, tres valvulas (pecas desenhadas,
  fechada/aberta), Lela no patio da usina (so luta depois das tres valvulas) -> agua de volta;
- Tchum recebe o jogador na entrada; ginasio fechado nesta etapa (interior de Fortree na proxima rodada);
- Centro Pokemon, Mart e casa (interiores de Lavaridge), ponto de cura, moradores e placas.
Rodar depois de install_cap5.py.
"""
import collections, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import pillarton as PL, route5 as R5
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json, register, walkable

OD = collections.OrderedDict
DOOR_OFF = {"rb_house_grey": (2, 4), "rb_office_long": (4, 5), "rb_office_small": (2, 4), "rb_pokecenter": (1, 3),
            "rb_mart": (1, 3), "rb_apartment": (2, 8), "rb_gym": (3, 4)}
INTERIORS = [("pc", "MAP_LAVARIDGE_TOWN_POKEMON_CENTER_1F", "LavaridgeTown_PokemonCenter_1F", "MAP_LAVARIDGE_TOWN"),
             ("mart", "MAP_LAVARIDGE_TOWN_MART", "LavaridgeTown_Mart", "MAP_LAVARIDGE_TOWN"),
             ("house_w", "MAP_LAVARIDGE_TOWN_HOUSE", "LavaridgeTown_House", "MAP_LAVARIDGE_TOWN")]
NPCS = [  # (x, y, grafico, movimento, script, flag de sumir)
    (23, 36, "BRAWLY", "MOVEMENT_TYPE_FACE_DOWN", "Palm130_Tchum", "0"),
    (48, 8, "AQUA_MEMBER_F", "MOVEMENT_TYPE_FACE_LEFT", "Palm131_Lela", "FLAG_HT_PILLARTON_WATER"),
    (18, 21, "OLD_MAN", "MOVEMENT_TYPE_FACE_RIGHT", "Palm130_OldCanal", "0"),
    (34, 26, "WOMAN_2", "MOVEMENT_TYPE_FACE_UP", "Palm130_GardenLady", "0"),
    (13, 19, "LITTLE_GIRL", "MOVEMENT_TYPE_WANDER_AROUND", "Palm130_Kid", "0"),
    (48, 21, "MAN_1", "MOVEMENT_TYPE_FACE_DOWN", "Palm130_GymFan", "0"),
]
GRUNTS = [(22, 7, "AQUA_MEMBER_M", "LEFT", 3, "Palm131_DamGrunt1", "TRAINER_PALM_DAM_GRUNT_1"),
          (33, 8, "AQUA_MEMBER_F", "LEFT", 3, "Palm131_DamGrunt2", "TRAINER_PALM_DAM_GRUNT_2")]
SIGNS = [(18, 37, "Palm130_CitySign"), (39, 17, "Palm130_GymSign"), (41, 6, "Palm130_PlantSign"), (12, 11, "Palm130_DamSign")]
VALVE_FLAGS = ["FLAG_HT_PILLARTON_VALVE_1", "FLAG_HT_PILLARTON_VALVE_2", "FLAG_HT_PILLARTON_VALVE_3"]


def main():
    # Route 5: fim norte aberto, conexao com Pillarton
    import install_cap5
    install_cap5.main(north_open=True)
    rp = f"{ROOT}/data/maps/PalmRoute05/map.json"
    r = jload(rp)
    r["connections"] = [cn for cn in r["connections"] if cn["map"] != "MAP_PALM_PILLARTON"] + \
                       [OD([("map", "MAP_PALM_PILLARTON"), ("offset", -PL.OFFSET_ROUTE5), ("direction", "up")])]
    jsave(rp, r)

    ids = json.load(open(os.path.join(HERE, "..", "mapgen", "custom_ids.json")))["rustboro"]
    c = PL.compose()
    for (x, y, _) in SIGNS:
        c.put(x, y, 3, collision=1)
    bl = PL.flatten(c.build())
    register("PalmPillarton", "LAYOUT_PALM_PILLARTON", c, bl)
    j = map_json("MAP_PALM_PILLARTON", "PalmPillarton", "LAYOUT_PALM_PILLARTON", "MUS_FORTREE", "MAPSEC_MAUVILLE_CITY", "MAP_TYPE_CITY",
                 [OD([("map", "MAP_PALM_ROUTE05"), ("offset", PL.OFFSET_ROUTE5), ("direction", "down")])])
    for (x, y, gfx, mv, script, flag) in NPCS:
        assert walkable(bl, c.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, mv, script, flag=flag, rng=1 if "WANDER" in mv else 0))
    for (x, y, gfx, d, sight, script, _) in GRUNTS:
        assert walkable(bl, c.w, x, y), (script, x, y)
        j["object_events"].append(obj(gfx, x, y, f"MOVEMENT_TYPE_FACE_{d}", script, "TRAINER_TYPE_NORMAL", sight))
    local = {e["script"]: i + 1 for i, e in enumerate(j["object_events"])}
    pos = {label: (name, x, y) for (name, x, y, label) in PL.BUILDINGS}
    def door(label):
        name, x, y = pos[label]
        dx, dy = DOOR_OFF[name]
        return x + dx, y + dy
    for (label, dm, _, _) in INTERIORS:
        x, y = door(label)
        j["warp_events"].append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dm), ("dest_warp_id", "0")]))
    pcx, pcy = pos["pc"][1:]; mx, my = pos["mart"][1:]
    j["bg_events"] = [sign(x, y, s) for (x, y, s) in SIGNS] + \
        [sign(vx, vy, f"Palm131_Valve{i + 1}") for i, (vx, vy) in enumerate(PL.VALVES)] + \
        [sign(pcx + 2, pcy + 3, "Common_EventScript_ShowPokemonCenterSign"), sign(pcx + 3, pcy + 3, "Common_EventScript_ShowPokemonCenterSign"),
         sign(mx + 2, my + 3, "Common_EventScript_ShowPokemartSign"), sign(mx + 3, my + 3, "Common_EventScript_ShowPokemartSign")]
    jsave(f"{ROOT}/data/maps/PalmPillarton/map.json", j)
    for idx, (_, _, folder, old) in enumerate(INTERIORS):
        q = f"{ROOT}/data/maps/{folder}/map.json"
        k = jload(q)
        for wv in k["warp_events"]:
            if wv["dest_map"] in (old, "MAP_PALM_PILLARTON"):
                wv["dest_map"], wv["dest_warp_id"] = "MAP_PALM_PILLARTON", str(idx)
        jsave(q, k)
    hp = f"{ROOT}/src/data/heal_locations.json"
    h = jload(hp)
    for e in h["heal_locations"]:
        if e["id"] == "HEAL_LOCATION_LAVARIDGE_TOWN":
            e["map"], e["x"], e["y"] = "MAP_PALM_PILLARTON", door("pc")[0], door("pc")[1] + 1
    jsave(hp, h)

    gx, gy = door("gym")
    door_mt, wall_mt = bl[gy * c.w + gx] & 0x3FF, bl[gy * c.w + gx - 1] & 0x3FF
    lela = local["Palm131_Lela"]
    sc = ["PalmPillarton_MapScripts::\n\tmap_script MAP_SCRIPT_ON_LOAD, Palm131_Load\n\t.byte 0\n",
          "Palm131_Load::\n" + "".join(f"\tcall_if_set {fl}, Palm131_DrawValve{i + 1}\n" for i, fl in enumerate(VALVE_FLAGS))
          + f"\tsetmetatile {gx}, {gy}, {wall_mt}, TRUE\n\tend\n"]   # ginasio fechado nesta etapa
    for i, ((vx, vy), fl) in enumerate(zip(PL.VALVES, VALVE_FLAGS), 1):
        sc.append(f"Palm131_DrawValve{i}::\n\tsetmetatile {vx}, {vy}, {ids['valve_open']}, TRUE\n\treturn\n")
        sc.append(f"Palm131_Valve{i}::\n\tlockall\n\tgoto_if_set {fl}, Palm131_ValveIsOpen\n"
                  f"\tmsgbox Palm131_TextValveTurn, MSGBOX_DEFAULT\n\tsetflag {fl}\n\tcall Palm131_DrawValve{i}\n"
                  f"\tspecial DrawWholeMapView\n\tplayse SE_UNLOCK\n\tgoto Palm131_ValveCount\n")
    sc.append("Palm131_ValveIsOpen::\n\tmsgbox Palm131_TextValveOpen, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc.append("Palm131_ValveCount::\n" + "".join(f"\tgoto_if_unset {fl}, Palm131_ValveMore\n" for fl in VALVE_FLAGS)
              + "\tmsgbox Palm131_TextValvesAll, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc.append("Palm131_ValveMore::\n\tmsgbox Palm131_TextValveMore, MSGBOX_DEFAULT\n\treleaseall\n\tend\n")
    sc.append("Palm131_Lela::\n\tlock\n\tfaceplayer\n" + "".join(f"\tgoto_if_unset {fl}, Palm131_LelaTaunt\n" for fl in VALVE_FLAGS)
              + "\ttrainerbattle_single TRAINER_PALM_LELA, Palm131_TextLelaIntro, Palm131_TextLelaDefeat, Palm131_LelaDefeated\n"
              "\trelease\n\tend\n")
    sc.append("Palm131_LelaTaunt::\n\tmsgbox Palm131_TextLelaTaunt, MSGBOX_DEFAULT\n\trelease\n\tend\n")
    sc.append(f"Palm131_LelaDefeated::\n\tmsgbox Palm131_TextLelaAfter, MSGBOX_DEFAULT\n\tclosemessage\n\tfadescreen FADE_TO_BLACK\n"
              f"\tsetflag FLAG_HT_PILLARTON_WATER\n\tremoveobject {lela}\n\tfadescreen FADE_FROM_BLACK\n"
              "\tmsgbox Palm131_TextWaterBack, MSGBOX_DEFAULT\n\trelease\n\tend\n")
    for (_, _, _, _, _, script, tid) in GRUNTS:
        k = script.replace("Palm131_", "")
        sc.append(f"{script}::\n\ttrainerbattle_single {tid}, Palm131_Text{k}Intro, Palm131_Text{k}Defeat\n"
                  f"\tmsgbox Palm131_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    sc.append("Palm130_Tchum::\n\tgoto_if_set FLAG_HT_PILLARTON_WATER, Palm130_TchumAfter\n\tmsgbox Palm130_Tchum_Text, MSGBOX_NPC\n\tend\n")
    sc.append("Palm130_TchumAfter::\n\tmsgbox Palm130_TchumAfter_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, _, _, script, _) in NPCS:
        if script.startswith("Palm130_") and script != "Palm130_Tchum":
            sc.append(f"{script}::\n\tmsgbox {script}_Text, MSGBOX_NPC\n\tend\n")
    for (_, _, s) in SIGNS:
        sc.append(f"{s}::\n\tmsgbox {s}_Text, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmPillarton/scripts.inc", "w").write("\n".join(sc))
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch5_pillarton.txt"], check=True)
    print("Pillarton instalada:", c.w, "x", c.h, "| portas", [(l, door(l)) for (l, _, _, _) in INTERIORS], "| ginasio", (gx, gy))


if __name__ == "__main__":
    main()
