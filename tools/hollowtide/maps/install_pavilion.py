#!/usr/bin/env python3
"""Pavilhao das Estrelas de Horizon (pendência do Cap. 7; roteiro: "pavilhoes de constelacoes").

- as duas folhas da porta do pavilhao (46,9)/(47,9) levam ao interior (layout do 1F do museu da Lilycove, o
  mesmo predio do lado de fora); enquanto o lago esta alto (antes de FLAG_HT_HORIZON_DONE) a entrada fica fechada
  e a placa diz isso; depois a placa convida;
- dentro: as constelacoes de LUNIA nos quadros, a maquete do telescopio, a tabua dos primeiros moradores e
  visitantes; a escada do mirante (noturno) fica com um atendente.
Rodar depois de install_polish.py.
"""
import collections, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, coord, map_json
from install_cap9b import new_map

OD = collections.OrderedDict
DOORS = [(46, 9), (47, 9)]
EXHIBITS = {(1, 1): "Lantern", (2, 1): "Lantern", (5, 1): "Crown", (6, 1): "Crown", (9, 1): "Piplup", (11, 1): "Piplup",
            (2, 6): "Mirror", (3, 6): "Mirror", (6, 6): "Wayfarer", (15, 12): "Telescope", (16, 9): "Tablet",
            (17, 9): "Tablet", (18, 9): "Tablet", (18, 11): "MoonStone", (19, 1): "Twins", (20, 1): "Twins"}


def flatten_steps():
    """O carimbo do museu traz a escadaria com elevacao 5 (como na Lilycove, onde a praca e mais alta); em Horizon a
    rua e elevacao 3 e a escada ficava inalcancavel: os degraus andaveis do carimbo (x 42-51, y 9-12) viram 3."""
    import struct
    lp = f"{ROOT}/data/layouts/PalmHorizon/map.bin"
    d = bytearray(open(lp, "rb").read())
    w = jload(f"{ROOT}/data/layouts/layouts.json")
    W = next(l for l in w["layouts"] if l.get("id") == "LAYOUT_PALM_HORIZON")["width"]
    for y in range(9, 13):
        for x in range(42, 52):
            i = 2 * (y * W + x)
            v = struct.unpack_from("<H", d, i)[0]
            if (v >> 12) == 5 and (v >> 10) & 3 == 0:
                struct.pack_into("<H", d, i, (v & 0x0FFF) | (3 << 12))
    for y in range(4, 6):                       # telhado de cima do carimbo: estava andavel (elevacao 5); vira solido
        for x in range(42, 52):
            i = 2 * (y * W + x)
            v = struct.unpack_from("<H", d, i)[0]
            if (v >> 12) == 5 and (v >> 10) & 3 == 0:
                struct.pack_into("<H", d, i, v | (1 << 10))
    open(lp, "wb").write(bytes(d))


def main():
    flatten_steps()
    hp = f"{ROOT}/data/maps/PalmHorizon/map.json"
    h = jload(hp)
    h["warp_events"] = [w for w in h["warp_events"] if w["dest_map"] != "MAP_PALM_STAR_PAVILION"]
    first = len(h["warp_events"])
    h["warp_events"] += [OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", "MAP_PALM_STAR_PAVILION"), ("dest_warp_id", str(i))])
                         for i, (x, y) in enumerate(DOORS)]
    h["coord_events"] = [e for e in h["coord_events"] if e["script"] != "Palm260_PavilionClosed"] + \
                        [coord(x, y + 1, "Palm260_PavilionClosed") for (x, y) in DOORS]
    for b in h["bg_events"]:
        if b.get("script") == "Palm170_PavilionSign":
            b["script"] = "Palm260_PavilionSign"
    jsave(hp, h)
    hs = f"{ROOT}/data/maps/PalmHorizon/scripts.inc"
    t = open(hs).read()
    if "Palm260_PavilionClosed::" not in t:
        t += """
Palm260_PavilionClosed::
	goto_if_set FLAG_HT_HORIZON_DONE, Palm260_End
	lockall
	msgbox Palm260_TextClosed, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, Palm260_StepBack
	waitmovement 0
	releaseall
	end

Palm260_StepBack:
	walk_down
	step_end

Palm260_PavilionSign::
	goto_if_set FLAG_HT_HORIZON_DONE, Palm260_PavilionSignOpen
	msgbox Palm170_PavilionSign_Text, MSGBOX_SIGN
	end

Palm260_PavilionSignOpen::
	msgbox Palm260_TextSignOpen, MSGBOX_SIGN
	end

Palm260_End::
	end
"""
        open(hs, "w").write(t)

    new_map("PalmStarPavilion")
    j = map_json("MAP_PALM_STAR_PAVILION", "PalmStarPavilion", "LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_1F", "MUS_LILYCOVE_MUSEUM",
                 "MAPSEC_MOSSDEEP_CITY", "MAP_TYPE_INDOOR", [])
    j["show_map_name"] = False
    j["allow_cycling"] = j["allow_running"] = False
    j["warp_events"] = [OD([("x", x), ("y", 13), ("elevation", 0), ("dest_map", "MAP_PALM_HORIZON"), ("dest_warp_id", str(first + i))])
                        for i, x in enumerate((9, 10))]
    j["object_events"] = [obj("GENTLEMAN", 16, 2, "MOVEMENT_TYPE_FACE_DOWN", "Palm261_Attendant"),
                          obj("BEAUTY", 5, 12, "MOVEMENT_TYPE_FACE_RIGHT", "Palm261_Guide"),
                          obj("PSYCHIC_M", 6, 2, "MOVEMENT_TYPE_FACE_UP", "Palm261_Stargazer"),
                          obj("SCHOOL_KID_M", 13, 7, "MOVEMENT_TYPE_WANDER_AROUND", "Palm261_Kid", rng=1),
                          obj("WOMAN_4", 3, 8, "MOVEMENT_TYPE_FACE_UP", "Palm261_Visitor")]
    j["bg_events"] = [sign(x, y, f"Palm261_Ex{name}") for (x, y), name in EXHIBITS.items()]
    jsave(f"{ROOT}/data/maps/PalmStarPavilion/map.json", j)
    sc = ["PalmStarPavilion_MapScripts::\n\t.byte 0\n"]
    for lab in ("Attendant", "Guide", "Stargazer", "Kid", "Visitor"):
        sc.append(f"Palm261_{lab}::\n\tmsgbox Palm261_Text{lab}, MSGBOX_NPC\n\tend\n")
    for name in sorted(set(EXHIBITS.values())):
        sc.append(f"Palm261_Ex{name}::\n\tmsgbox Palm261_TextEx{name}, MSGBOX_SIGN\n\tend\n")
    open(f"{ROOT}/data/maps/PalmStarPavilion/scripts.inc", "w").write("\n".join(sc))
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/pavilion.txt"], check=True)
    print("Pavilhao das Estrelas instalado")


if __name__ == "__main__":
    main()
