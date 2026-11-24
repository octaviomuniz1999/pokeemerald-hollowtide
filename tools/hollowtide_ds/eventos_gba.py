#!/usr/bin/env python3
"""Eventos de Dawnmere e da Route 1 nas posicoes do GBA (CP-DS-03B, etapas 3 e 4).

Os eventos ja portados no CP-DS-01/02 (zonas 057_T20 = Dawnmere e 030_R29 = Route 1) ficam com os mesmos scripts e
textos; so mudam de lugar, para os tiles do mapa do GBA no desenho global (gba2grade.py):
  mundo = (X0 + x_global, Z0 + z_global) (lunia_mundo.py); global = tile do GBA + origem do mapa no desenho
  (Dawnmere/LittlerootTown (2, 2); Route 1/Route101 (36, 19)).
Os NPCs ficam parados olhando para o lado do GBA (tipos de movimento do HGSS: 14 cima, 15 baixo, 16 esquerda,
17 direita, conferidos nos eventos originais).
Gera os patches da pasta de conteudo (07xx), sobre o estado da pasta de conteudo ja aplicado no hg-engine pelo build.sh (sem
estes patches: reverta-os com patch -R antes de regenerar):
  0700-dawnmere-eventos-gba.patch   (zone_event/057_T20.json)
  0701-dawnmere-trava-leste.patch   (scr_seq_0842_T20.s: a saida volta a ser a leste; o passo de volta e para oeste)
  0702-route1-eventos-gba.patch     (zone_event/030_R29.json)
  0703-harvestvale-eventos-gba.patch (zone_event/064_T21.json)
  0704-harvestvale-saida-sul.patch  (scr_seq_0850_T21.s: a saida para a Route 2 e a do sul, como no GBA)
  0706-route2-r30-eventos-gba.patch (zone_event/031_R30.json: Route 2, linhas 0-31 do GBA)
  0707-route2-r31-eventos-gba.patch (zone_event/032_R31.json: Route 2, linhas 32-47; porta trancada e saida sul)
  0708-route2-r31-scripts.patch     (scr_seq_0230_R31.s: porta trancada e ponte provisoria para a guarita)
Uso: eventos_gba.py HG_ENGINE PASTA_SAIDA
"""
import difflib, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from lunia_mundo import X0, Z0, ORIGENS   # canto do desenho na matriz 0 e de cada mapa do GBA no desenho
OLHA = {"cima": (14, 0), "baixo": (15, 1), "esquerda": (16, 2), "direita": (17, 3)}

ZONAS = {
    "057_T20": dict(
        origem=ORIGENS["Dawnmere"],
        # script do evento do DS -> (tile do GBA, lado para onde olha) no LittlerootTown
        objetos={"_EV_scr_seq_T20_015 + 1": ((23, 18), "baixo"),     # guia (Palm040_Guide)
                 "_EV_scr_seq_T20_001 + 1": ((11, 24), "baixo"),     # vizinho (Palm040_Neighbor)
                 "_EV_scr_seq_T20_017 + 1": ((23, 10), "baixo")},    # mirante (Palm051_OverlookNpc)
        placas={"_EV_scr_seq_T20_013 + 1": (15, 9),                  # Palm040_LabSign
                "_EV_scr_seq_T20_007 + 1": (11, 19),                 # Palm040_HomeSign
                "_EV_scr_seq_T20_016 + 1": (18, 16),                 # Palm040_NeighborSign
                "_EV_scr_seq_T20_014 + 1": (17, 19)},                # Palm040_TownSign
        # placa da Route 1 do CP-DS-01 (script 19): sai; no GBA a Route 1 tem as placas norte e sul (0702)
        tirar_placas={"19"},
        # warps por destino; o GBA tem 3 portas. Os dois warps do HGSS sem par ficam nas portas decorativas (tiles
        # bloqueados, inalcancaveis), para os interiores continuarem com a volta valida.
        warps={"MAP_T20R0201": (2, 9),     # casa do jogador (T20R0201/0202) = BRENDANS_HOUSE (o jogo novo comeca nela)
               "MAP_T20R0101": (13, 8),    # laboratorio (T20R0101): porta do modelo, 1 tile a oeste do warp do GBA (14,8)
               "MAP_T20R0301": (20, 16),   # casa vizinha = MAYS_HOUSE
               "MAP_T20R0401": (8, 23),    # sem par no GBA: porta decorativa (bloqueada)
               "MAP_T20R0102": (20, 23)},  # sem par no GBA: porta decorativa (bloqueada)
        # trava da saida (Palm040_ExitEast): os tiles do GBA (33, 21-22); Dawnmere inteira fica numa celula so
        coord={"_EV_scr_seq_T20_002 + 1": ("gba", 33, 21, 1, 2)},
    ),
    "030_R29": dict(
        origem=ORIGENS["Route1"],
        objetos={"_EV_scr_seq_R29_002 + 1": ((12, 6), "esquerda"),   # andarilho (Palm050_Walker)
                 "485 - 1 + _std_npc_trainer": ((22, 25), "esquerda"),   # Kai (TRAINER_PALM_KAI)
                 "487 - 1 + _std_npc_trainer": ((17, 39), "direita"),    # Min (TRAINER_PALM_MIN)
                 "std_itemball_r29_potion": ((13, 24), None)},           # Potion
        placas={"_EV_scr_seq_R29_005 + 1": (7, 21),                  # Palm050_NorthSign
                "_EV_scr_seq_R29_004 + 1": (6, 48)},                 # Palm050_SouthSign
        tirar_placas=set(), warps={}, coord={},
    ),
    "064_T21": dict(
        origem=ORIGENS["Harvestvale"],
        # as linhas 0-4 de Harvestvale caem numa celula da Route 1 (um header por celula): o fazendeiro e a chegada
        # descem 3 linhas (GBA (11,3) e linha 2), para ficarem na zona de Harvestvale
        objetos={"_EV_scr_seq_T21_000 + 1": ((11, 6), "esquerda"),   # fazendeiro (Palm060_Farmer / Palm071)
                 "_EV_scr_seq_T21_004 + 1": ((7, 32), "baixo")},     # recruta da Team Palm no quiosque (Palm060_Kiosk)
        placas={"_EV_scr_seq_T21_006 + 1": (12, 11),                 # Palm060_Welcome
                "_EV_scr_seq_T21_005 + 1": (7, 22),                  # Palm060_GymSign
                "_EV_scr_seq_T21_007 + 1": (20, 35),                 # Palm060_ClosedRoad
                "_EV_scr_seq_T21_008 + 1": (10, 32),                 # Palm060_KioskSign
                "_EV_scr_seq_T21_009 + 1": (27, 23),                 # valvula = Palm062_WaterSign
                "12": (26, 19),                                      # Palm062_CoffeeSign
                "13": (16, 34),                                      # Palm064_DryingYard
                "14": (24, 18)},                                     # Palm064_WaterBoard
        tirar_placas=set(),
        warps={"MAP_T21PC0101": (12, 21),     # Centro Pokemon
               "MAP_T21FS0101": (23, 31),     # Poke Mart
               "MAP_T21R0301": (17, 11),      # OLDALE_TOWN_HOUSE1
               "MAP_T07GYM0101": (5, 21),     # ginasio do Nevard
               "MAP_T21R0501": (21, 18)},     # OLDALE_TOWN_HOUSE2
        coord={"_EV_scr_seq_T21_001 + 1": ("gba", 8, 5, 4, 1),       # chegada pelo norte (Palm072_Arrival, GBA linha 2)
               "_EV_scr_seq_T21_002 + 1": ("gba", 17, 35, 3, 1),     # saida sul para a Route 2 (Palm080_LeaveColheita)
               "_EV_scr_seq_T21_003 + 1": ("gba", 5, 22, 1, 1)},     # porta do ginasio fechada: o tile abaixo da porta
    ),
    # Route 2 (PalmRoute02): as linhas 0-31 caem nas celulas de header R30, as 32-47 nas de header R31 (as duas zonas
    # que ja eram a Route 2 do prototipo)
    "031_R30": dict(
        origem=ORIGENS["Route2"],
        objetos={"488 - 1 + _std_npc_trainer": ((26, 13), "esquerda"),   # Liang (Palm080_RouteLIANG)
                 "489 - 1 + _std_npc_trainer": ((16, 27), "direita"),    # Mei Lan (Palm080_RouteMEI_LAN)
                 "std_itemball_r30_potion": ((7, 26), None)},            # Super Potion
        placas={"_EV_scr_seq_R30_005 + 1": (16, 3)},                     # Palm080_RouteSignNorth
        tirar_placas={"_EV_scr_seq_R30_006 + 1"},   # porta trancada: a casa fica nas linhas do R31 (scr_seq_R31_003)
        warps={}, coord={},
    ),
    "032_R31": dict(
        origem=ORIGENS["Route2"],
        objetos={"490 - 1 + _std_npc_trainer": ((21, 35), "esquerda")},  # Qin (Palm080_RouteQIN)
        placas={"_EV_scr_seq_R31_002 + 1": (17, 40)},                    # Palm080_RouteSignSouth
        tirar_placas=set(),
        # chegada de quem sai da guarita (proto) para a Route 2: logo acima da saida sul do GBA (18-21, 47)
        warps={"MAP_R31R0101": (19, 46)},
        coord={},
        novos_bg=[{"script": "_EV_scr_seq_R31_003 + 1", "type": 1, "gba": (14, 36), "player_facing_dir": 4}],   # Palm280_DoorLocked
        novos_coord=[{"script": "_EV_scr_seq_R31_004 + 1", "gba": (18, 47), "width": 4, "length": 1,
                      "value": 0, "var": "VAR_TEMP_x4001"}],   # saida sul: ponte provisoria para a guarita de Breezeport
    ),
}


def mover(j, z):
    ox, oy = z["origem"]
    w = lambda x, y: (X0 + ox + x, Z0 + oy + y)
    for o in j["object_events"]:
        if o["script"] in z["objetos"]:
            (x, y), lado = z["objetos"][o["script"]]
            o["x"], o["z"] = w(x, y)
            if lado:
                o["movement_type"], o["initial_dir"] = OLHA[lado]
                o["movement_range_x"] = o["movement_range_z"] = 0
    j["bg_events"] = [b for b in j["bg_events"] if b["script"] not in z["tirar_placas"]]
    for b in j["bg_events"]:
        if b["script"] in z["placas"]:
            b["x"], b["z"] = w(*z["placas"][b["script"]])
    for wp in j["warp_events"]:
        if wp["dest_header_id"] in z["warps"]:
            wp["x"], wp["z"] = w(*z["warps"][wp["dest_header_id"]])
    for b in z.get("novos_bg", []):
        x, zz = w(*b["gba"])
        j.setdefault("bg_events", []).append({"script": b["script"], "type": b["type"], "x": x, "z": zz, "y": 0,
                                              "player_facing_dir": b["player_facing_dir"]})
    for c in z.get("novos_coord", []):
        x, zz = w(*c["gba"])
        j.setdefault("coord_events", []).append({"script": c["script"], "x": x, "z": zz, "width": c["width"],
                                                 "length": c["length"], "y": 0, "value": c["value"], "var": c["var"]})
    for c in j.get("coord_events", []):
        if c["script"] in z["coord"]:
            ref, cx, cz, wd, ln = z["coord"][c["script"]]
            c["x"], c["z"] = (X0 + cx, Z0 + cz) if ref == "global" else w(cx, cz)
            c["width"], c["length"] = wd, ln
    return j


def diff(rel, old, new):
    """Diff unificado aplicavel pelo patch(1), com a marca de arquivo sem quebra de linha no fim."""
    out = []
    for line in difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + rel, "b/" + rel):
        out.append(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n")
    return "".join(out)


def zona(hg, out, nome, arquivo):
    rel = f"data/eventdata/zone_event/{nome}.json"
    old = open(os.path.join(hg, rel)).read()
    new = json.dumps(mover(json.loads(old), ZONAS[nome]), indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")
    open(os.path.join(out, arquivo), "w").write(diff(rel, old, new))


def main(hg, out):
    zona(hg, out, "057_T20", "0700-dawnmere-eventos-gba.patch")
    zona(hg, out, "030_R29", "0702-route1-eventos-gba.patch")
    zona(hg, out, "064_T21", "0703-harvestvale-eventos-gba.patch")
    zona(hg, out, "031_R30", "0706-route2-r30-eventos-gba.patch")
    zona(hg, out, "032_R31", "0707-route2-r31-eventos-gba.patch")
    rel = "data/scr_seq/scr_seq_0230_R31.s"
    old = open(os.path.join(hg, rel)).read()
    a = "scr_seq_R31_001:\nscr_seq_R31_003:\nscr_seq_R31_004:\n"
    assert a in old, "stubs do R31 mudaram"
    new = old.replace(a, "scr_seq_R31_001:\n").replace(
        "scr_seq_R31_000:\n",
        "// casa de porta trancada da Route 2 (Palm280_DoorLocked; a casa fica nas linhas de header R31)\n"
        "scr_seq_R31_003:\n\tplay_se SEQ_SE_DP_SELECT\n\tlockall\n\tnpc_msg 1\n\twait_button\n\tcloseMsg_PLACEHOLDER\n"
        "\treleaseall\n\tend\n\n"
        "// ponte provisoria: a saida sul da Route 2 (GBA) leva a guarita do prototipo, do lado da Route 2; dali se segue\n"
        "// para Breezeport (Olivine do HGSS) ate Breezeport ser convertida\n"
        "scr_seq_R31_004:\n\tlockall\n\twarp MAP_R31R0101, 0, 9, 7, DIR_WEST\n\treleaseall\n\tend\n\n"
        "scr_seq_R31_000:\n", 1).replace("closeMsg_PLACEHOLDER", "closemsg")
    assert new.count("scr_seq_R31_003:") == 1 and new.count("scr_seq_R31_004:") == 1
    open(os.path.join(out, "0708-route2-r31-scripts.patch"), "w").write(diff(rel, old, new))
    rel = "data/scr_seq/scr_seq_0850_T21.s"
    old = open(os.path.join(hg, rel)).read()
    new = old.replace("// chegada pelo leste (Route 1)", "// chegada pelo norte (Route 1), como no GBA (Palm072_Arrival)")
    new = new.replace("// saida norte (Route 2): fechada ate vencer o Nevard",
                      "// saida sul (Route 2), como no GBA (Palm080_LeaveColheita): fechada ate vencer o Nevard; volta um passo para cima")
    a = new.index("scr_seq_T21_002:"); b = new.index("_HT_ExitOk:", a)
    new = new[:a] + new[a:b].replace("_HT_StepDown", "_HT_StepUp") + new[b:]
    new = new.rstrip("\n") + "\n_HT_StepUp:\n\tstep MOVEMENT_STEP_UP, 1\n\tstep_end\n\t.balign 4\n"
    assert new.count("_HT_StepUp") == 2
    open(os.path.join(out, "0704-harvestvale-saida-sul.patch"), "w").write(diff(rel, old, new))
    rel = "data/scr_seq/scr_seq_0842_T20.s"
    old = open(os.path.join(hg, rel)).read()
    new = old.replace("// saida oeste (Route 1): sem Pokemon, volta um passo (GBA Palm040_ExitEast)",
                      "// saida leste (Route 1), como no GBA: sem Pokemon, volta um passo para oeste (Palm040_ExitEast)")
    a = new.rindex("_HT_StepBack:")
    new = new[:a] + new[a:].replace("step MOVEMENT_STEP_RIGHT, 1", "step MOVEMENT_STEP_LEFT, 1", 1)
    assert new != old
    open(os.path.join(out, "0701-dawnmere-trava-leste.patch"), "w").write(diff(rel, old, new))
    print("patches de eventos gerados em", out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
