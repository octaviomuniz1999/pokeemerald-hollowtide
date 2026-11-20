#!/usr/bin/env python3
"""Polimento (depois da historia principal), sem decisoes de cânone novas:
- estalagem da Passway: o estalajadeiro oferece pernoite (cura o time) e o hospede acompanha a historia
  (estrada de Voltara aberta -> energia de volta/trens -> depois da Liga, a montanha).
Rodar depois de install_train.py.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT

INN_OLD = "Palm182_Innkeeper::\n\tmsgbox Palm182_Innkeeper_Text, MSGBOX_NPC\n\tend\n"
INN_NEW = """Palm182_Innkeeper::
	lock
	faceplayer
	msgbox Palm182_Innkeeper_Text, MSGBOX_DEFAULT
	msgbox Palm182_InnRest_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm182_InnNo
	closemessage
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	special HealPlayerParty
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox Palm182_InnMorning_Text, MSGBOX_DEFAULT
	release
	end

Palm182_InnNo::
	msgbox Palm182_InnNo_Text, MSGBOX_DEFAULT
	release
	end
"""
GUEST_OLD = "Palm182_InnGuest::\n\tmsgbox Palm182_InnGuest_Text, MSGBOX_NPC\n\tend\n"
GUEST_NEW = """Palm182_InnGuest::
	goto_if_set FLAG_HT_POSTGAME_DATA, Palm182_InnGuestStorm
	goto_if_set FLAG_HT_VOLTARA_DONE, Palm182_InnGuestTrains
	msgbox Palm182_InnGuest_Text, MSGBOX_NPC
	end

Palm182_InnGuestTrains::
	msgbox Palm182_InnGuestTrains_Text, MSGBOX_NPC
	end

Palm182_InnGuestStorm::
	msgbox Palm182_InnGuestStorm_Text, MSGBOX_NPC
	end
"""


def main():
    p = f"{ROOT}/data/maps/PalmPassway/scripts.inc"
    t = open(p).read()
    if "Palm182_InnRest_Text" not in t:
        assert INN_OLD in t and GUEST_OLD in t
        t = t.replace(INN_OLD, INN_NEW).replace(GUEST_OLD, GUEST_NEW)
        open(p, "w").write(t)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/polish.txt"], check=True)
    print("Polimento instalado: estalagem da Passway")


if __name__ == "__main__":
    main()
