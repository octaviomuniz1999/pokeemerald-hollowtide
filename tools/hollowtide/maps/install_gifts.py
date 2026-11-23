#!/usr/bin/env python3
"""Presentes do canone (POKEDEX_LUNIA) que nao existiam no jogo:
- EEVEE (Serenia, apos o arco de Lau): o jardineiro, depois de FLAG_HT_SERENIA_DONE;
- PORYGON (Ferralia, pos-ginasio, "laboratorio de dados"): o funcionario da sede da ferrovia, depois da 3a insignia;
- ROTOM (Voltara, centro de dados de Vega, apos a libertacao): o proprio Rotom na sala dos servidores, depois do Vega;
- FURFROU (Tradepost, salao de tosa): a moradora da casa do Tradepost, depois de "O Preco da Troca".
Scripts em data/scripts/hollowtide_gifts.inc (padrao do Beldum do Steven: party/PC, apelido). Idempotente.
"""
import collections, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave, obj

FLAGS = [("0x271", "FLAG_HT_GIFT_EEVEE", "jardineiro de Serenia deu o Eevee"),
         ("0x272", "FLAG_HT_GIFT_ROTOM", "Rotom do centro de dados foi com o jogador"),
         ("0x273", "FLAG_HT_GIFT_PORYGON", "sede da ferrovia de Ferralia deu o Porygon"),
         ("0x274", "FLAG_HT_GIFT_FURFROU", "salao de tosa do Tradepost deu o Furfrou")]
# (chave, especie, nivel, flag, condicao, texto "antes", remove o objeto?)
GIFTS = [("Eevee", "SPECIES_EEVEE", 30, "FLAG_HT_GIFT_EEVEE", "FLAG_HT_SERENIA_DONE", "Palm141_Gardener_Text", False),
         ("Porygon", "SPECIES_PORYGON", 24, "FLAG_HT_GIFT_PORYGON", "FLAG_BADGE03_GET", "Palm250_TextStaff", False),
         ("Rotom", "SPECIES_ROTOM", 40, "FLAG_HT_GIFT_ROTOM", "FLAG_HT_VOLTARA_DONE", "Palm260_TextRotomBefore", True),
         ("Furfrou", "SPECIES_FURFROU", 27, "FLAG_HT_GIFT_FURFROU", "FLAG_HT_TRADEPOST_DONE",
          "VerdanturfTown_House_Text_TrainersGatherAtPokemonLeague", False)]


def gift_script(k, sp, lv, flag, cond, before, remove):
    rm = f"\tremoveobject VAR_LAST_TALKED\n" if remove else ""
    return f"""Palm260_Gift{k}::
	lock
	faceplayer
	goto_if_set {flag}, Palm260_{k}After
	goto_if_unset {cond}, Palm260_{k}Before
	msgbox Palm260_Text{k}Offer, MSGBOX_DEFAULT
	setvar VAR_TEMP_TRANSFERRED_SPECIES, {sp}
	givemon {sp}, {lv}
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, Palm260_{k}Party
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, Palm260_{k}PC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

Palm260_{k}Party::
	call Palm260_{k}Fanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_{k}Done
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto Palm260_{k}Done
	end

Palm260_{k}PC::
	call Palm260_{k}Fanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_{k}PCDone
	call Common_EventScript_NameReceivedBoxMon
Palm260_{k}PCDone::
	call Common_EventScript_TransferredToPC
Palm260_{k}Done::
	setflag {flag}
	msgbox Palm260_Text{k}After, MSGBOX_DEFAULT
{rm}	release
	end

Palm260_{k}Fanfare::
	bufferspeciesname STR_VAR_2, {sp}
	playfanfare MUS_OBTAIN_ITEM
	message Palm260_TextObtainedMon
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, {sp}
	return

Palm260_{k}After::
	msgbox Palm260_Text{k}After, MSGBOX_DEFAULT
	release
	end

Palm260_{k}Before::
	msgbox {before}, MSGBOX_DEFAULT
	release
	end

Palm260_Text{k}Offer:
	.string "x$"

Palm260_Text{k}After:
	.string "x$"

"""


def main():
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    for val, name, why in FLAGS:
        if name not in t:
            t, n = re.subn(r"#define FLAG_UNUSED_%s\s+%s[^\n]*\n" % (val, val), f"#define {name:<36} {val} // {why}\n", t, count=1)
            assert n == 1, val
    open(fp, "w").write(t)
    body = "@ Hollowtide: presentes do canone (install_gifts.py)\n\n" + "".join(gift_script(*g) for g in GIFTS) + \
           "Palm260_TextObtainedMon:\n\t.string \"x$\"\n\nPalm260_TextRotomBefore:\n\t.string \"x$\"\n"
    open(f"{ROOT}/data/scripts/hollowtide_gifts.inc", "w").write(body)
    es = f"{ROOT}/data/event_scripts.s"
    s = open(es).read()
    inc = '\t.include "data/scripts/hollowtide_gifts.inc"\n'
    if inc not in s:
        anchor = '\t.include "data/scripts/shared_secret_base.inc"\n'   # fora do bloco .if IS_FRLG
        assert anchor in s
        s = s.replace(anchor, anchor + inc)
        open(es, "w").write(s)
    # objetos
    def retarget(mapdir, old_script, new_script):
        p = f"{ROOT}/data/maps/{mapdir}/map.json"
        j = jload(p)
        hit = [o for o in j["object_events"] if o["script"] in (old_script, new_script)]
        assert len(hit) == 1, (mapdir, old_script, len(hit))
        hit[0]["script"] = new_script
        jsave(p, j)
    retarget("PalmSerenia", "Palm141_Gardener", "Palm260_GiftEevee")
    retarget("VerdanturfTown_House", "VerdanturfTown_House_EventScript_Woman1", "Palm260_GiftFurfrou")
    p = f"{ROOT}/data/maps/PalmStationFerralia/map.json"
    j = jload(p)
    st = [o for o in j["object_events"] if o["graphics_id"] == "OBJ_EVENT_GFX_DEVON_EMPLOYEE"]
    assert len(st) == 1
    st[0]["script"] = "Palm260_GiftPorygon"
    jsave(p, j)
    p = f"{ROOT}/data/maps/PalmDataCenter2F/map.json"
    j = jload(p)
    j["object_events"] = [o for o in j["object_events"] if o["script"] != "Palm260_GiftRotom"]
    o = obj("SPECIES(ROTOM)", 4, 2, "MOVEMENT_TYPE_FACE_DOWN", "Palm260_GiftRotom")
    o["flag"] = "FLAG_HT_GIFT_ROTOM"
    j["object_events"].append(o)
    jsave(p, j)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/gifts.txt"], check=True)
    print("Presentes instalados: Eevee, Porygon, Rotom, Furfrou")


if __name__ == "__main__":
    main()
