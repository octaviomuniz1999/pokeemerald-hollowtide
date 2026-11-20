#!/usr/bin/env python3
"""Field moves sem HM obrigatoria (decisoes do diretor, 20/11):

- SURF: a Nami entrega a HM03 Surf no fim do Complexo Oceanico, logo depois de desligar o sistema (ela chegou
  montada no WAILORD; levou o jogador de barco ate ali — agora ele atravessa a agua sozinho). Se a mochila estiver
  cheia, falar com a Nami na sala de controle entrega de novo (FLAG_HT_RECEIVED_SURF, 0x270).
- HMs podem ser esquecidas (P_CAN_FORGET_HIDDEN_MOVE): a HM07 Waterfall continua sendo HM (trocar por TM renumeraria
  as HMs dos saves existentes), mas deixa de prender o golpe no Pokemon.
Rodar por ultimo (depois de install_doors.py); idempotente.
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT


def main():
    fp = f"{ROOT}/include/constants/flags.h"
    t = open(fp).read()
    if "FLAG_HT_RECEIVED_SURF" not in t:
        t, n = re.subn(r"#define FLAG_UNUSED_0x270\s+0x270[^\n]*\n",
                       "#define FLAG_HT_RECEIVED_SURF                0x270 // Nami entregou a HM03 Surf (fim do Complexo Oceanico)\n", t, count=1)
        assert n == 1
        open(fp, "w").write(t)
    cp = f"{ROOT}/include/config/pokemon.h"
    t = open(cp).read()
    t2 = re.sub(r"#define P_CAN_FORGET_HIDDEN_MOVE\s+FALSE", "#define P_CAN_FORGET_HIDDEN_MOVE         TRUE ", t)
    assert "P_CAN_FORGET_HIDDEN_MOVE         TRUE" in t2
    open(cp, "w").write(t2)
    sp = f"{ROOT}/data/maps/PalmOceanComplexCore/scripts.inc"
    s = open(sp).read()
    if "Palm204_GiveSurf::" not in s:
        a = "\tmsgbox Palm204_TextNamiDone, MSGBOX_DEFAULT\n\treleaseall\n\tend\n"
        assert s.count(a) == 1
        s = s.replace(a, "\tmsgbox Palm204_TextNamiDone, MSGBOX_DEFAULT\n\tcall Palm204_GiveSurf\n\treleaseall\n\tend\n")
        b = "Palm204_NamiDone::\n\tmsgbox Palm204_TextNamiDone, MSGBOX_DEFAULT\n\trelease\n\tend\n"
        assert b in s
        s = s.replace(b, "Palm204_NamiDone::\n\tmsgbox Palm204_TextNamiDone, MSGBOX_DEFAULT\n\tcall Palm204_GiveSurf\n\trelease\n\tend\n")
        s = s.rstrip("\n") + ("\n\nPalm204_GiveSurf::\n\tgoto_if_set FLAG_HT_RECEIVED_SURF, Palm204_GiveSurfEnd\n"
                              "\tmsgbox Palm204_TextNamiSurf, MSGBOX_DEFAULT\n\tgiveitem ITEM_HM_SURF\n"
                              "\tgoto_if_eq VAR_RESULT, FALSE, Palm204_GiveSurfEnd\n\tsetflag FLAG_HT_RECEIVED_SURF\n"
                              "\tmsgbox Palm204_TextNamiSurfHint, MSGBOX_DEFAULT\nPalm204_GiveSurfEnd::\n\treturn\n")
        open(sp, "w").write(s)
    # o marinheiro do porto: depois da crise o mar esta calmo (e a Nami continua na sala de controle)
    tp = f"{ROOT}/data/maps/PalmTidemouth/scripts.inc"
    s = open(tp).read()
    if "Palm201_BoatCalm" not in s:
        a = "Palm201_Boat::\n\tmsgbox Palm201_TextBoat, MSGBOX_YESNO\n"
        assert a in s
        s = s.replace(a, "Palm201_Boat::\n\tgoto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm201_BoatCalm\n\tmsgbox Palm201_TextBoat, MSGBOX_YESNO\n"
                         "Palm201_BoatGo::\n")
        s = s.replace("Palm201_BoatGo::\n\tgoto_if_eq VAR_RESULT, NO, Palm201_BoatNo\n",
                      "Palm201_BoatGo::\n\tgoto_if_eq VAR_RESULT, NO, Palm201_BoatNo\n")
        s = s.rstrip("\n") + "\n\nPalm201_BoatCalm::\n\tmsgbox Palm201_TextBoatCalm, MSGBOX_YESNO\n\tgoto Palm201_BoatGo\n"
        open(tp, "w").write(s)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/surf.txt"], check=True)
    print("Surf da Nami instalado; HMs esqueciveis")


if __name__ == "__main__":
    main()
