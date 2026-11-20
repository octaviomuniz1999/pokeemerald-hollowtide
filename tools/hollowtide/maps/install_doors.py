#!/usr/bin/env python3
"""Portas sem destino (varredura de 20/11): ultimo passo da instalacao — rodar DEPOIS de todos os outros instaladores
(os que regravam map.bin desfariam a colisao).

- Ferralia (29,12): segunda folha da porta da sede da ferrovia ganha o warp para o saguao da estacao;
- terminal de balsas de Tidemouth (33,36) e casa do faroleiro da Breezeport (63,43): eram andaveis e nao levavam
  a lugar nenhum; ficam solidas, com recado proprio;
- as demais portas trancadas (ja solidas) dos predios sem interior respondem "trancada" quando o jogador olha para elas.
"""
import collections, os, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave, sign

OD = collections.OrderedDict
LOCKED = {"PalmFerralia": [(64, 8), (20, 10), (46, 25), (53, 25), (6, 36), (12, 36), (6, 47), (22, 47), (32, 47), (54, 47), (63, 47)],
          "PalmPillarton": [(47, 7), (4, 28), (35, 34), (46, 34)], "PalmRoute02": [(14, 36)], "PalmRoute03": [(19, 61)],
          "PalmRoute04": [(7, 15)], "PalmTradepost": [(35, 7), (15, 28)], "PalmVoltara": [(25, 6), (36, 6), (4, 38)]}
SPECIAL = {"PalmTidemouth": [((33, 36), "Palm280_Terminal")], "PalmBrisa": [((63, 43), "Palm280_KeeperHouse")]}


def solidify(folder, pts):
    j = jload(f"{ROOT}/data/maps/{folder}/map.json")
    lay = next(l for l in jload(f"{ROOT}/data/layouts/layouts.json")["layouts"] if l.get("id") == j["layout"])
    p = f"{ROOT}/{lay['blockdata_filepath']}"
    d = bytearray(open(p, "rb").read())
    for (x, y) in pts:
        i = 2 * (y * lay["width"] + x)
        v = struct.unpack_from("<H", d, i)[0]
        struct.pack_into("<H", d, i, v | (1 << 10))
    open(p, "wb").write(bytes(d))


def add_signs(folder, items):
    mp = f"{ROOT}/data/maps/{folder}/map.json"
    j = jload(mp)
    have = {(b["x"], b["y"]) for b in j["bg_events"]}
    for (x, y), script in items:
        if (x, y) not in have:
            b = sign(x, y, script)
            b["player_facing_dir"] = "BG_EVENT_PLAYER_FACING_NORTH"
            j["bg_events"].append(b)
    jsave(mp, j)


def main():
    # Ferralia: a segunda folha da porta da estacao
    fp = f"{ROOT}/data/maps/PalmFerralia/map.json"
    f = jload(fp)
    if not any(w["x"] == 29 and w["y"] == 12 for w in f["warp_events"]):
        f["warp_events"].append(OD([("x", 29), ("y", 12), ("elevation", 0), ("dest_map", "MAP_PALM_STATION_FERRALIA"), ("dest_warp_id", "1")]))
        jsave(fp, f)
    for folder, pts in LOCKED.items():
        add_signs(folder, [(p, "Palm280_DoorLocked") for p in pts])
    for folder, items in SPECIAL.items():
        solidify(folder, [p for p, _ in items])
        add_signs(folder, items)
    # os scripts ficam na Ferralia (rotulos globais)
    sp = f"{ROOT}/data/maps/PalmFerralia/scripts.inc"
    s = open(sp).read()
    if "Palm280_DoorLocked::" not in s:
        s += """
Palm280_DoorLocked::
	msgbox Palm280_TextDoorLocked, MSGBOX_SIGN
	end

Palm280_Terminal::
	msgbox Palm280_TextTerminal, MSGBOX_SIGN
	end

Palm280_KeeperHouse::
	msgbox Palm280_TextKeeperHouse, MSGBOX_SIGN
	end
"""
        open(sp, "w").write(s)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/doors.txt"], check=True)
    print("Portas: 1 warp novo, 2 portas solidas com recado, 21 portas trancadas com resposta")


if __name__ == "__main__":
    main()
