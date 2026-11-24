#!/usr/bin/env python3
"""Eventos de Dawnmere e da Route 1 nas posicoes do GBA (CP-DS-03B, etapas 3 e 4).

Os eventos ja portados no CP-DS-01/02 (zonas 057_T20 = Dawnmere e 030_R29 = Route 1) ficam com os mesmos scripts e
textos; so mudam de lugar, para os tiles do mapa do GBA no desenho global (gba2grade.py):
  mundo = (672 + x_global, 416 + z_global); global = tile do GBA + origem do mapa no desenho
  (Dawnmere/LittlerootTown (2, 2); Route 1/Route101 (36, 19)).
Os NPCs ficam parados olhando para o lado do GBA (tipos de movimento do HGSS: 14 cima, 15 baixo, 16 esquerda,
17 direita, conferidos nos eventos originais).
Gera os patches da build de prova, sobre o estado da pasta de conteudo ja aplicado no hg-engine pelo build.sh (sem
estes patches: reverta-os com patch -R antes de regenerar):
  0922-dawnmere-eventos-gba.patch   (zone_event/057_T20.json)
  0923-dawnmere-trava-leste.patch   (scr_seq_0842_T20.s: a saida volta a ser a leste; o passo de volta e para oeste)
  0924-route1-eventos-gba.patch     (zone_event/030_R29.json)
Uso: eventos_gba.py HG_ENGINE PASTA_SAIDA
"""
import difflib, json, os, sys

X0, Z0 = 672, 416                # canto da celula (21,13) da matriz 0
OLHA = {"cima": (14, 0), "baixo": (15, 1), "esquerda": (16, 2), "direita": (17, 3)}

ZONAS = {
    "057_T20": dict(
        origem=(2, 2),
        # script do evento do DS -> (tile do GBA, lado para onde olha) no LittlerootTown
        objetos={"_EV_scr_seq_T20_015 + 1": ((23, 18), "baixo"),     # guia (Palm040_Guide)
                 "_EV_scr_seq_T20_001 + 1": ((11, 24), "baixo"),     # vizinho (Palm040_Neighbor)
                 "_EV_scr_seq_T20_017 + 1": ((23, 10), "baixo")},    # mirante (Palm051_OverlookNpc)
        placas={"_EV_scr_seq_T20_013 + 1": (15, 9),                  # Palm040_LabSign
                "_EV_scr_seq_T20_007 + 1": (11, 19),                 # Palm040_HomeSign
                "_EV_scr_seq_T20_016 + 1": (18, 16),                 # Palm040_NeighborSign
                "_EV_scr_seq_T20_014 + 1": (17, 19)},                # Palm040_TownSign
        # placa da Route 1 do CP-DS-01 (script 19): sai; no GBA a Route 1 tem as placas norte e sul (0924)
        tirar_placas={"19"},
        # warps por destino; o GBA tem 3 portas. Os dois warps do HGSS sem par ficam nas portas decorativas (tiles
        # bloqueados, inalcancaveis), para os interiores continuarem com a volta valida.
        warps={"MAP_T20R0201": (2, 9),     # casa do jogador (T20R0201/0202) = BRENDANS_HOUSE (o jogo novo comeca nela)
               "MAP_T20R0101": (13, 8),    # laboratorio (T20R0101): porta do modelo, 1 tile a oeste do warp do GBA (14,8)
               "MAP_T20R0301": (20, 16),   # casa vizinha = MAYS_HOUSE
               "MAP_T20R0401": (8, 23),    # sem par no GBA: porta decorativa (bloqueada)
               "MAP_T20R0102": (20, 23)},  # sem par no GBA: porta decorativa (bloqueada)
        # trava da saida (Palm040_ExitEast): coluna global 31, a ultima da celula de Dawnmere, linhas 2-29
        coord={"_EV_scr_seq_T20_002 + 1": ("global", 31, 2, 1, 28)},
    ),
    "030_R29": dict(
        origem=(36, 19),
        objetos={"_EV_scr_seq_R29_002 + 1": ((12, 6), "esquerda"),   # andarilho (Palm050_Walker)
                 "485 - 1 + _std_npc_trainer": ((22, 25), "esquerda"),   # Kai (TRAINER_PALM_KAI)
                 "487 - 1 + _std_npc_trainer": ((17, 39), "direita"),    # Min (TRAINER_PALM_MIN)
                 "std_itemball_r29_potion": ((13, 24), None)},           # Potion
        placas={"_EV_scr_seq_R29_005 + 1": (7, 21),                  # Palm050_NorthSign
                "_EV_scr_seq_R29_004 + 1": (6, 48)},                 # Palm050_SouthSign
        tirar_placas=set(), warps={}, coord={},
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
        wp["x"], wp["z"] = w(*z["warps"][wp["dest_header_id"]])
    for c in j["coord_events"]:
        if c["script"] in z["coord"]:
            _, gx, gz, wd, ln = z["coord"][c["script"]]
            c["x"], c["z"], c["width"], c["length"] = X0 + gx, Z0 + gz, wd, ln
    return j


def diff(path_rel, old, new):
    return "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + path_rel, "b/" + path_rel))


def zona(hg, out, nome, arquivo):
    rel = f"data/eventdata/zone_event/{nome}.json"
    old = open(os.path.join(hg, rel)).read()
    new = json.dumps(mover(json.loads(old), ZONAS[nome]), indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")
    open(os.path.join(out, arquivo), "w").write(diff(rel, old, new))


def main(hg, out):
    zona(hg, out, "057_T20", "0922-dawnmere-eventos-gba.patch")
    zona(hg, out, "030_R29", "0924-route1-eventos-gba.patch")
    rel = "data/scr_seq/scr_seq_0842_T20.s"
    old = open(os.path.join(hg, rel)).read()
    new = old.replace("// saida oeste (Route 1): sem Pokemon, volta um passo (GBA Palm040_ExitEast)",
                      "// saida leste (Route 1), como no GBA: sem Pokemon, volta um passo para oeste (Palm040_ExitEast)")
    a = new.rindex("_HT_StepBack:")
    new = new[:a] + new[a:].replace("step MOVEMENT_STEP_RIGHT, 1", "step MOVEMENT_STEP_LEFT, 1", 1)
    assert new != old
    open(os.path.join(out, "0923-dawnmere-trava-leste.patch"), "w").write(diff(rel, old, new))
    print("patches de eventos gerados em", out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
