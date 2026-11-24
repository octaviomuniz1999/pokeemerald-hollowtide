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
  0710-breezeport-eventos-gba.patch (zone_event/074_T26.json: Breezeport, mais o fim da Route 2 na linha dividida)
  0711-breezeport-scripts.patch     (scr_seq_0911_T26.s: placa e porta da Route 2, saida oeste e ponte para a Route 39)
  0712-route39-volta-breezeport.patch (Route 39: descendo, volta a borda oeste de Breezeport)
Uso: eventos_gba.py HG_ENGINE PASTA_SAIDA
"""
import difflib, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from lunia_mundo import X0, Z0, ORIGENS, gba   # canto do desenho na matriz 0 e de cada mapa do GBA no desenho
HG = None
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
    # Breezeport (PalmBrisa), header de Olivine (T26). A linha de blocos 5 e dividida com o fim da Route 2 e fica com
    # o header de Breezeport: Qin, a placa sul e a porta trancada da Route 2 entram nesta zona (novos_*)
    "074_T26": dict(
        origem=ORIGENS["Brisa"],
        objetos={"1": ((45, 29), "baixo"),        # artista, anfitria do festival (Palm080_BrisaHost)
                 "2": ((21, 8), "esquerda"),      # Palm093_Greeter
                 "5": ((30, 25), None),           # Palm093_PlazaGirl
                 "6": ((47, 7), "esquerda"),      # Palm093_LookoutHiker
                 "7": ((20, 41), None),           # Palm093_BeachWoman
                 "8": ((36, 44), "baixo"),        # Palm093_Fisherman
                 "9": ((50, 36), None),           # Palm093_JayFan
                 "10": ((64, 46), "baixo"),       # Palm093_KeeperOldMan
                 "11": ((12, 31), None),          # Palm093_PumpWife
                 "12": ((36, 19), None),          # Palm093_StoreKid (fala do Poke Mart)
                 "14": ((49, 30), "baixo")},      # Palm093_FestivalBeauty
        placas={"15": (22, 3),                    # Palm080_BrisaSign
                "16": (50, 28),                   # Palm090_TheaterSign
                "17": (27, 21),                   # Palm090_PalmPoster
                "18": (2, 37),                    # Palm090_EastSign (Route 3)
                "19": [(62, 43), (63, 43)],       # Palm092/Palm280_KeeperHouse
                "20": (12, 21), "21": (33, 22), "22": (60, 35)},   # lampioes do festival (Palm090_CityLamp1-3)
        tirar_placas=set(),
        warps={"MAP_T26GYM0101": (47, 27),        # Teatro (ginasio da Jay)
               "MAP_T26PC0101": (23, 16), "MAP_T26FS0101": (14, 16),
               "MAP_T26R0301": (4, 24), "MAP_T26R0501": (15, 24), "MAP_T26R0601": (4, 30),
               "MAP_R31R0101": (56, 33)},         # guarita do prototipo: sem uso (porta decorativa da loja, bloqueada)
        coord={"23": ("gba", 47, 28, 1, 1),       # porta do Teatro fechada ate as luzes: o tile abaixo da porta
               "24": ("gba", 0, 32, 1, 28)},      # saida para a Route 3: a borda oeste do GBA (Palm090_ToRoute03)
        novos_bg=[{"script": "3", "type": 1, "mapa": "Route2", "gba": (17, 40), "player_facing_dir": 4},   # placa sul
                  {"script": "4", "type": 1, "mapa": "Route2", "gba": (14, 36), "player_facing_dir": 4}],  # porta trancada
        novos_obj=[{"de": "032_R31", "script": "490 - 1 + _std_npc_trainer", "mapa": "Route2", "gba": (21, 35),
                    "lado": "esquerda"}],   # Qin
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
    usados = {}
    for b in j["bg_events"]:
        if b["script"] in z["placas"]:
            pos = z["placas"][b["script"]]
            if isinstance(pos, list):                    # o mesmo script em varias placas: na ordem do arquivo
                k = usados.get(b["script"], 0); usados[b["script"]] = k + 1
                pos = pos[min(k, len(pos) - 1)]
            b["x"], b["z"] = w(*pos)
    for wp in j["warp_events"]:
        if wp["dest_header_id"] in z["warps"]:
            wp["x"], wp["z"] = w(*z["warps"][wp["dest_header_id"]])
    for o in z.get("novos_obj", []):
        src = json.load(open(os.path.join(HG, f"data/eventdata/zone_event/{o['de']}.json")))
        n = dict(next(e for e in src["object_events"] if e["script"] == o["script"]))
        n["id"] = len(j["object_events"])               # id numerico (um nome obj_* precisaria de simbolo no hg-engine)
        n["x"], n["z"] = gba(o["mapa"], *o["gba"])
        n["movement_type"], n["initial_dir"] = OLHA[o["lado"]]
        n["movement_range_x"] = n["movement_range_z"] = 0
        j["object_events"].append(n)
    for b in z.get("novos_bg", []):
        x, zz = gba(b["mapa"], *b["gba"]) if "mapa" in b else w(*b["gba"])
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
    global HG
    HG = hg
    zona(hg, out, "057_T20", "0700-dawnmere-eventos-gba.patch")
    zona(hg, out, "030_R29", "0702-route1-eventos-gba.patch")
    zona(hg, out, "064_T21", "0703-harvestvale-eventos-gba.patch")
    zona(hg, out, "031_R30", "0706-route2-r30-eventos-gba.patch")
    zona(hg, out, "074_T26", "0710-breezeport-eventos-gba.patch")
    # Breezeport: placa sul e porta trancada da Route 2 (zona de Breezeport); a saida para a Route 3 e a borda oeste
    # (passo de volta para leste) e, depois da Jay, a ponte provisoria para a Route 39 (a Route 3 do prototipo)
    rel = "data/scr_seq/scr_seq_0911_T26.s"
    old = open(os.path.join(hg, rel)).read()
    a = "scr_seq_T26_002:\nscr_seq_T26_003:\nscr_seq_T26_012:\n"
    assert a in old
    new = old.replace(a, "scr_seq_T26_012:\n")
    sign = lambda lab, msg, nota: (f"// {nota}\n{lab}:\n\tplay_se SEQ_SE_DP_SELECT\n\tlockall\n\tnpc_msg {msg}\n"
                                   "\twait_button\n\tclosemsg\n\treleaseall\n\tend\n\n")
    new = new.replace("// gatilhos de quadro e carga do HGSS (rival, Jasmine): nada\n",
                      sign("scr_seq_T26_002", 20, "placa sul da Route 2 (a linha de blocos 5 e de Breezeport)") +
                      sign("scr_seq_T26_003", 21, "porta trancada da Route 2 (Palm280_DoorLocked)") +
                      "// gatilhos de quadro e carga do HGSS (rival, Jasmine): nada\n", 1)
    new = new.replace("// saida norte (Route 3): fechada ate vencer a Jay",
                      "// saida para a Route 3: a borda oeste, como no GBA (Palm090_ToRoute03); fechada ate vencer a Jay")
    a = new.index("scr_seq_T26_023:"); b = new.index("_HT_NorthOpen:", a)
    new = new[:a] + new[a:b].replace("_HT_StepDown", "_HT_StepRight") + new[b:]
    r39 = gba("Brisa", 1, 33)
    new = new.replace("_HT_NorthOpen:\n\tsetvar VAR_UNK_4078, 2\n\treleaseall\n\tend\n",
                      "_HT_NorthOpen:\n\tsetvar VAR_UNK_4078, 2\n"
                      "\t// ponte provisoria: a Route 3 original ainda nao existe; vai para a do prototipo (Route 39)\n"
                      "\twarp MAP_R39, 0, 279, 222, DIR_NORTH\n\treleaseall\n\tend\n")
    new = new.rstrip("\n") + "\n_HT_StepRight:\n\tstep MOVEMENT_STEP_RIGHT, 1\n\tstep_end\n\t.balign 4\n"
    assert new.count("_HT_StepRight") == 2 and "warp MAP_R39" in new
    open(os.path.join(out, "0711-breezeport-scripts.patch"), "w").write(diff(rel, old, new))
    # Route 39: descendo para Olivine (celulas antigas, sem eventos), volta a borda oeste de Breezeport
    parts = []
    rel = "data/scr_seq/scr_seq_0249_R39.s"
    old = open(os.path.join(hg, rel)).read()
    new = old.replace("scrdef scr_seq_R39_007\nscrdef_end", "scrdef scr_seq_R39_007\nscrdef scr_seq_R39_008\nscrdef_end")
    new = new.rstrip("\n") + ("\n\n// Hollowtide: ponte provisoria, a Route 39 (Route 3 do prototipo) volta para a borda oeste de\n"
                               f"// Breezeport nos mapas originais\nscr_seq_R39_008:\n\tlockall\n\twarp MAP_T26, 0, {r39[0]}, {r39[1]}, DIR_EAST\n"
                               "\treleaseall\n\tend\n")
    assert new != old
    parts.append(diff(rel, old, new))
    rel = "data/scr_seq/include/event_R39.inc"
    old = open(os.path.join(hg, rel)).read()
    new = old.replace(".equ _EV_scr_seq_R39_007, 7\n", ".equ _EV_scr_seq_R39_007, 7\n.equ _EV_scr_seq_R39_008, 8\n")
    assert new != old
    parts.append(diff(rel, old, new))
    rel = "data/eventdata/zone_event/040_R39.json"
    old = open(os.path.join(hg, rel)).read()
    jj = json.loads(old)
    jj.setdefault("coord_events", []).append({"script": "_EV_scr_seq_R39_008 + 1", "x": 277, "z": 223, "width": 5,
                                              "length": 1, "y": 0, "value": 0, "var": "VAR_TEMP_x4001"})
    parts.append(diff(rel, old, json.dumps(jj, indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")))
    open(os.path.join(out, "0712-route39-volta-breezeport.patch"), "w").write("".join(parts))
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
