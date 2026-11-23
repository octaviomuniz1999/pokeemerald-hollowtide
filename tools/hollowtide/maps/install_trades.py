#!/usr/bin/env python3
"""Trocas tematicas do Tradepost (POKEDEX_LUNIA, Cap. 4): Kadabra, Machoke, Graveler e Haunter — as quatro especies
que evoluem por troca. Nesta expansion a troca com NPC tenta a evolucao por troca (trade.c, STATE_TRY_EVOLUTION),
entao o jogador recebe e ve a evolucao (Alakazam, Machamp, Golem, Gengar). Os pedidos sao especies locais da Route 4.
4 IDs novos no fim de InGameTradeID (sem mexer nas trocas de Hoenn/FRLG), flags 0x275-0x278, 4 NPCs na praca do
mercado, scripts em data/scripts/hollowtide_trades.inc. Idempotente.
"""
import collections, json, os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave, obj, walkable

# (chave, trade id, oferece, apelido, pede, OT, sexo OT, otId, IVs, gfx, x, y, flag)
TRADES = [("Kadabra", "INGAME_TRADE_HT_KADABRA", "KADABRA", "KADA", "MEOWTH", "RAFA", "MALE", 51203, "PSYCHIC_M", 14, 18, "0x275"),
          ("Machoke", "INGAME_TRADE_HT_MACHOKE", "MACHOKE", "MUSCLE", "TIMBURR", "CIDA", "FEMALE", 30711, "BLACK_BELT", 16, 22, "0x276"),
          ("Graveler", "INGAME_TRADE_HT_GRAVELER", "GRAVELER", "PEBBLES", "ROGGENROLA", "TONI", "MALE", 44190, "HIKER", 28, 17, "0x277"),
          ("Haunter", "INGAME_TRADE_HT_HAUNTER", "HAUNTER", "BOO", "TRUBBISH", "DANI", "FEMALE", 12876, "HEX_MANIAC", 11, 18, "0x278")]


def main():
    # enum
    p = f"{ROOT}/include/constants/trade.h"
    t = open(p).read()
    if "INGAME_TRADE_HT_KADABRA" not in t:
        t = t.replace("    INGAME_TRADE_SEEL,\n};", "    INGAME_TRADE_SEEL,\n    // Hollowtide: trocas do Tradepost\n" +
                      "".join(f"    {tr[1]},\n" for tr in TRADES) + "};", 1)
        assert "INGAME_TRADE_HT_KADABRA" in t
        open(p, "w").write(t)
    # dados
    p = f"{ROOT}/src/data/trade.h"
    t = open(p).read()
    if "[INGAME_TRADE_HT_KADABRA]" not in t:
        entries = "".join(f"""    [{tid}] =
    {{
        .nickname = _("{nick}"),
        .species = SPECIES_{sp},
        .ivs = {{20, 20, 20, 20, 20, 20}},
        .abilityNum = 0,
        .otId = {otid},
        .conditions = {{5, 5, 5, 5, 5}},
        .personality = 0x{otid * 7 & 0xFFFF:04x},
        .heldItem = ITEM_NONE,
        .mailNum = MAIL_NONE,
        .otName = _("{ot}"),
        .otGender = {sex},
        .sheen = 10,
        .requestedSpecies = SPECIES_{req}
    }},
""" for (_, tid, sp, nick, req, ot, sex, otid, *_r) in TRADES)
        i = t.index("[INGAME_TRADE_MR_MIME]")
        t = t[:i] + entries.lstrip() + "    " + t[i:]
        open(p, "w").write(t)
    # flags
    p = f"{ROOT}/include/constants/flags.h"
    t = open(p).read()
    for (k, *_r, val) in TRADES:
        name = f"FLAG_HT_TRADE_{k.upper()}"
        if name not in t:
            t, n = re.subn(r"#define FLAG_UNUSED_%s\s+%s[^\n]*\n" % (val, val), f"#define {name:<36} {val} // troca do Tradepost: {k}\n", t, count=1)
            assert n == 1, val
    open(p, "w").write(t)
    # scripts
    body = ["@ Hollowtide: trocas do Tradepost (install_trades.py)\n"]
    for (k, tid, *_r) in TRADES:
        f = f"FLAG_HT_TRADE_{k.upper()}"
        body.append(f"""
Palm261_Trade{k}::
	lock
	faceplayer
	goto_if_set {f}, Palm261_{k}Done
	ingame_trade {tid}, Palm261_Text{k}Want, Palm261_{k}Decline, Palm261_{k}Wrong, Palm261_Text{k}Thanks
	setflag {f}
	release
	end

Palm261_{k}Decline::
	msgbox Palm261_Text{k}Decline, MSGBOX_DEFAULT
	release
	end

Palm261_{k}Wrong::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox Palm261_TextTradeWrong, MSGBOX_DEFAULT
	release
	end

Palm261_{k}Done::
	msgbox Palm261_Text{k}Done, MSGBOX_DEFAULT
	release
	end

Palm261_Text{k}Want:
	.string "x$"
Palm261_Text{k}Thanks:
	.string "x$"
Palm261_Text{k}Decline:
	.string "x$"
Palm261_Text{k}Done:
	.string "x$"
""")
    body.append("\nPalm261_TextTradeWrong:\n\t.string \"x$\"\n")
    open(f"{ROOT}/data/scripts/hollowtide_trades.inc", "w").write("".join(body))
    es = f"{ROOT}/data/event_scripts.s"
    s = open(es).read()
    inc = '\t.include "data/scripts/hollowtide_trades.inc"\n'
    if inc not in s:
        anchor = '\t.include "data/scripts/hollowtide_gifts.inc"\n'
        assert anchor in s
        s = s.replace(anchor, anchor + inc)
        open(es, "w").write(s)
    # NPCs
    mp = f"{ROOT}/data/maps/PalmTradepost/map.json"
    j = jload(mp)
    lay = {l["id"]: l for l in jload(f"{ROOT}/data/layouts/layouts.json")["layouts"] if "id" in l}[j["layout"]]
    w = lay["width"]; bl = struct.unpack(f"<{w * lay['height']}H", open(f"{ROOT}/{lay['blockdata_filepath']}", "rb").read())
    j["object_events"] = [o for o in j["object_events"] if not o["script"].startswith("Palm261_Trade")]
    for (k, tid, sp, nick, req, ot, sex, otid, gfx, x, y, val) in TRADES:
        assert walkable(bl, w, x, y) and walkable(bl, w, x, y + 1), (k, x, y)
        j["object_events"].append(obj(gfx, x, y, "MOVEMENT_TYPE_FACE_DOWN", f"Palm261_Trade{k}"))
    jsave(mp, j)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/trades.txt"], check=True)
    print("Trocas do Tradepost instaladas")


if __name__ == "__main__":
    main()
