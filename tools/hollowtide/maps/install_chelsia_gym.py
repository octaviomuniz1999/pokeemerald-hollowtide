#!/usr/bin/env python3
"""Ginasio da Chelsia ("O Lago das Estrelas") — reaproveita os mapas do ginasio de Sootopolis (1F e B1F).

1F: tres campos de gelo = tres constelacoes. Cada placa de gelo e uma estrela: pisar uma vez a acende (a
placa racha); com todas as estrelas de um campo acesas, a escada para o campo seguinte aparece. Pisar de
novo numa estrela acesa quebra o gelo e o jogador cai no B1F ("o lago embaixo"), onde ficam 3 treinadoras
e a escada de volta a entrada. O mecanismo e o do ginasio de Sootopolis (callback de passo + VAR_ICE_STEP_COUNT).
Chelsia (Clefable 40, Azumarill 41, Sylveon 43) -> Insignia do Horizonte (FLAG_BADGE06_GET) + TM54 Dazzling Gleam.
A porta do ginasio na Horizon abre quando o lago baixa (FLAG_HT_HORIZON_DONE). Rodar depois de install_cap7.py.
"""
import collections, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import horizon as HZ
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign

OD = collections.OrderedDict
G1, GB = "SootopolisCity_Gym_1F", "SootopolisCity_Gym_B1F"
B1F_KEEP = {  # (x, y) do treinador original -> (script novo, treinador, grafico)
    (7, 17): ("Palm173_TrainerA", "TRAINER_PALM_CHELSIA_GYM_A", "LASS"),
    (6, 13): ("Palm173_TrainerB", "TRAINER_PALM_CHELSIA_GYM_B", "WOMAN_2"),
    (11, 9): ("Palm173_TrainerC", "TRAINER_PALM_CHELSIA_GYM_C", "BEAUTY"),
}


def main():
    # ---------------- Horizon: porta do ginasio vira warp e abre com o lago calmo
    hp = f"{ROOT}/data/maps/PalmHorizon/map.json"
    h = jload(hp)
    gx, gy = HZ.door("gym")
    h["warp_events"] = [w for w in h["warp_events"] if w["dest_map"] != "MAP_SOOTOPOLIS_CITY_GYM_1F"]
    gym_idx = len(h["warp_events"])
    h["warp_events"].append(OD([("x", gx), ("y", gy), ("elevation", 0), ("dest_map", "MAP_SOOTOPOLIS_CITY_GYM_1F"), ("dest_warp_id", "0")]))
    jsave(hp, h)
    hs = f"{ROOT}/data/maps/PalmHorizon/scripts.inc"
    t = open(hs).read()
    marker = "Palm170_Load::\n"
    i = t.index(marker) + len(marker)
    if not t[i:].startswith("\tgoto_if_set FLAG_HT_HORIZON_DONE, Palm170_LoadDone\n"):
        # ginasio fechado e jardim alagado so ate o fim do evento
        body_end = t.index("\tend\n", i)
        body = t[i:body_end].replace("\tgoto_if_set FLAG_HT_HORIZON_DONE, Palm170_LoadDone\n", "")
        t = t[:i] + "\tgoto_if_set FLAG_HT_HORIZON_DONE, Palm170_LoadDone\n" + body + t[body_end:]
        open(hs, "w").write(t)

    # ---------------- 1F
    p = f"{ROOT}/data/maps/{G1}/map.json"
    j = jload(p)
    for w in j["warp_events"]:
        if w["dest_map"] in ("MAP_SOOTOPOLIS_CITY", "MAP_PALM_HORIZON"):
            w["dest_map"], w["dest_warp_id"] = "MAP_PALM_HORIZON", str(gym_idx)
    objs = []
    for o in j["object_events"]:
        if o["script"].endswith("EventScript_Juan") or o["script"] == "Palm173_Chelsia":
            o["graphics_id"], o["script"] = "OBJ_EVENT_GFX_ANABEL", "Palm173_Chelsia"
            objs.append(o)
        elif o["script"].endswith("EventScript_GymGuide") or o["script"] == "Palm173_Guide":
            o["script"] = "Palm173_Guide"
            objs.append(o)
    objs.append(obj("OBJ_EVENT_GFX_SPECIES(PIPLUP)", 9, 2, "MOVEMENT_TYPE_FACE_DOWN", "Palm173_Piplup"))
    j["object_events"] = objs
    for b in j["bg_events"]:
        b["script"] = "Palm173_Statue"
    j["region_map_section"] = "MAPSEC_LILYCOVE_CITY"
    jsave(p, j)
    s = f"{ROOT}/data/maps/{G1}/scripts.inc"
    t = open(s).read()
    cut = t.find("\n@ ---- Hollowtide: ginasio da Chelsia")
    if cut >= 0:
        t = t[:cut]
    t = t.rstrip("\n") + "\n\n@ ---- Hollowtide: ginasio da Chelsia\n" + "\n".join([
        "Palm173_Chelsia::\n\ttrainerbattle_single TRAINER_PALM_CHELSIA, Palm173_TextChelsiaIntro, Palm173_TextChelsiaDefeat, "
        "Palm173_ChelsiaDefeated, NO_MUSIC\n\tmsgbox Palm173_TextChelsiaAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
        "Palm173_ChelsiaDefeated::\n\tmessage Palm173_TextBadge\n\twaitmessage\n\tcall Common_EventScript_PlayGymBadgeFanfare\n"
        "\tmsgbox Palm173_TextBadgeExplain, MSGBOX_DEFAULT\n\tsetflag FLAG_BADGE06_GET\n\tsetflag FLAG_DEFEATED_SOOTOPOLIS_GYM\n"
        "\tgiveitem ITEM_TM_DAZZLING_GLEAM\n\tmsgbox Palm173_TextTM, MSGBOX_DEFAULT\n\trelease\n\tend\n",
        "Palm173_Piplup::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_PIPLUP, CRY_MODE_NORMAL\n\tmsgbox Palm173_TextPiplup, MSGBOX_DEFAULT\n"
        "\twaitmoncry\n\trelease\n\tend\n",
        "Palm173_Guide::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_BADGE06_GET, Palm173_GuideAfter\n"
        "\tmsgbox Palm173_TextGuide, MSGBOX_DEFAULT\n\trelease\n\tend\n",
        "Palm173_GuideAfter::\n\tmsgbox Palm173_TextGuideAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
        "Palm173_Statue::\n\tlockall\n\tgoto_if_set FLAG_BADGE06_GET, Palm173_StatueWon\n\tmsgbox Palm173_TextStatue, MSGBOX_DEFAULT\n"
        "\treleaseall\n\tend\n",
        "Palm173_StatueWon::\n\tmsgbox Palm173_TextStatueWon, MSGBOX_DEFAULT\n\treleaseall\n\tend\n"]) + "\n"
    open(s, "w").write(t)

    # ---------------- B1F: 3 treinadoras (as outras saem)
    p = f"{ROOT}/data/maps/{GB}/map.json"
    j = jload(p)
    keep = []
    for o in j["object_events"]:
        k = (o["x"], o["y"])
        if k in B1F_KEEP:
            script, _, gfx = B1F_KEEP[k]
            o["script"], o["graphics_id"] = script, f"OBJ_EVENT_GFX_{gfx}"
            keep.append(o)
    assert len(keep) == 3, keep
    j["object_events"] = keep
    j["region_map_section"] = "MAPSEC_LILYCOVE_CITY"
    jsave(p, j)
    s = f"{ROOT}/data/maps/{GB}/scripts.inc"
    t = open(s).read()
    cut = t.find("\n@ ---- Hollowtide: ginasio da Chelsia")
    if cut >= 0:
        t = t[:cut]
    t = t.rstrip("\n") + "\n\n@ ---- Hollowtide: ginasio da Chelsia\n"
    for (script, tid, _) in B1F_KEEP.values():
        k = script[-1]
        t += (f"{script}::\n\ttrainerbattle_single {tid}, Palm173_Text{k}Intro, Palm173_Text{k}Defeat\n"
              f"\tmsgbox Palm173_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n\n")
    open(s, "w").write(t)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch7_gym.txt"], check=True)
    print("Ginasio da Chelsia instalado | porta na Horizon", (gx, gy), "warp", gym_idx)


if __name__ == "__main__":
    main()
