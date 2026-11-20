#!/usr/bin/env python3
"""Capitulo 11 (parte 3): depois dos creditos.

O jogador acorda no quarto, em Dawnmere (casa 2F de Littleroot, conforme o genero). Na primeira vez depois do
Hall da Fama o PC do quarto apita: chegam os dados de Hoc, Riven e Jade, que apontam o cume da montanha acima
da Passway, e em seguida a convocacao do Doge. A convocacao liga FLAG_HT_POSTGAME_DATA, e e ela (nao mais so os
creditos) que abre a escadaria do cume na Passway, como pede o roteiro.
Rodar depois de install_cap11b.py.
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT

FLAG_LINE = "#define FLAG_HT_POSTGAME_DATA                0x68  // depois dos creditos: dados de Hoc/Riven/Jade e a convocacao do Doge\n"

EVENT = """
PalmPost_Arm::
	call_if_unset FLAG_HT_POSTGAME_DATA, PalmPost_SetTemp
	return

PalmPost_SetTemp::
	setvar VAR_TEMP_9, 1
	return

PalmPost_Data::
	lockall
	setvar VAR_TEMP_9, 2
	delay 40
	playse SE_PC_ON
	msgbox PalmPost_TextBeep, MSGBOX_DEFAULT
	msgbox PalmPost_TextHoc, MSGBOX_DEFAULT
	msgbox PalmPost_TextRiven, MSGBOX_DEFAULT
	msgbox PalmPost_TextJade, MSGBOX_DEFAULT
	playse SE_PIN
	msgbox PalmPost_TextDoge, MSGBOX_DEFAULT
	closemessage
	playse SE_PC_OFF
	setflag FLAG_HT_POSTGAME_DATA
	releaseall
	end

PalmPost_TextBeep:
	.string "x$"

PalmPost_TextHoc:
	.string "x$"

PalmPost_TextRiven:
	.string "x$"

PalmPost_TextJade:
	.string "x$"

PalmPost_TextDoge:
	.string "x$"
"""


def patch_house(folder, with_event):
    p = f"{ROOT}/data/maps/{folder}/scripts.inc"
    t = open(p).read()
    if "PalmPost_Arm" in t and "OnFrame" in t:
        return
    hdr = f"{folder}_MapScripts::\n"
    t = t.replace(hdr, hdr + f"\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, {folder}_OnFrame\n", 1)
    tr = f"{folder}_OnTransition:\n"
    assert tr in t, folder
    t = t.replace(tr, tr + "\tcall_if_set FLAG_SYS_GAME_CLEAR, PalmPost_Arm\n", 1)
    t += f"\n{folder}_OnFrame:\n\tmap_script_2 VAR_TEMP_9, 1, PalmPost_Data\n\t.2byte 0\n"
    if with_event:
        t += EVENT
    open(p, "w").write(t)


def main():
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    if "FLAG_HT_POSTGAME_DATA" not in t:
        t = re.sub(r"#define FLAG_UNUSED_0x068\s+0x68[^\n]*\n", FLAG_LINE, t, count=1)
        assert "FLAG_HT_POSTGAME_DATA" in t
        open(fp, "w").write(t)
    patch_house("LittlerootTown_BrendansHouse_2F", True)
    patch_house("LittlerootTown_MaysHouse_2F", False)
    # escadaria do cume: abre com a convocacao do Doge
    for p in [f"{ROOT}/data/maps/PalmPassway/scripts.inc", f"{ROOT}/tools/hollowtide/maps/install_cap8.py"]:
        s = open(p).read()
        s = s.replace("goto_if_set FLAG_SYS_GAME_CLEAR, Palm181_Ok", "goto_if_set FLAG_HT_POSTGAME_DATA, Palm181_Ok")
        open(p, "w").write(s)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch11c.txt"], check=True)
    print("Cap. 11 (parte 3) instalado: dados pos-creditos e convocacao do Doge")


if __name__ == "__main__":
    main()
