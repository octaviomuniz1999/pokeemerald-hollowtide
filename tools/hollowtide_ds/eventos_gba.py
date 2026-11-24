#!/usr/bin/env python3
"""Eventos de Dawnmere nas posicoes do GBA (CP-DS-03B, etapa 3).

Os eventos de Dawnmere ja portados no CP-DS-01/02 (header do New Bark, zona 057_T20) ficam com os mesmos scripts e
textos; so mudam de lugar, para os tiles do LittlerootTown do GBA no desenho global (gba2grade.py):
  mundo = (672 + x_global, 416 + z_global); x_global = x_GBA + 2, z_global = y_GBA + 2 (origem de Dawnmere no desenho).
Gera os patches da build de prova (sobre o estado da pasta de conteudo, ja aplicado no hg-engine pelo build.sh):
  0922-dawnmere-eventos-gba.patch  (zone_event/057_T20.json)
  0923-dawnmere-trava-leste.patch  (scr_seq_0842_T20.s: a saida volta a ser a leste; o passo de volta e para oeste)
Uso: eventos_gba.py HG_ENGINE PASTA_SAIDA
"""
import difflib, json, os, sys

X0, Z0 = 672, 416                # canto da celula (21,13) da matriz 0
OX, OY = 2, 2                    # origem de Dawnmere no desenho global


def w(x, y):
    """Tile do GBA (LittlerootTown) -> coordenada de mundo do DS."""
    return X0 + OX + x, Z0 + OY + y


# script do evento do DS -> tile do GBA (o mesmo texto/papel no LittlerootTown)
OBJETOS = {"_EV_scr_seq_T20_015 + 1": (23, 18),    # guia (Palm040_Guide)
           "_EV_scr_seq_T20_001 + 1": (11, 24),    # vizinho (Palm040_Neighbor)
           "_EV_scr_seq_T20_017 + 1": (23, 10)}    # mirante (Palm051_OverlookNpc)
PLACAS = {"_EV_scr_seq_T20_013 + 1": (15, 9),      # Palm040_LabSign
          "_EV_scr_seq_T20_007 + 1": (11, 19),     # Palm040_HomeSign
          "_EV_scr_seq_T20_016 + 1": (18, 16),     # Palm040_NeighborSign
          "_EV_scr_seq_T20_014 + 1": (17, 19)}     # Palm040_TownSign
# warps por destino; o GBA tem 3 portas. Os dois warps do HGSS sem par ficam nas portas decorativas (tiles bloqueados,
# inalcancaveis), para os interiores continuarem com a volta valida.
WARPS = {"MAP_T20R0201": (2, 9),     # casa do jogador (T20R0201/0202) = BRENDANS_HOUSE (o jogo novo comeca nela)
         "MAP_T20R0101": (13, 8),    # laboratorio (T20R0101): porta do modelo, 1 tile a oeste do warp do GBA (14,8)
         "MAP_T20R0301": (20, 16),   # casa vizinha = MAYS_HOUSE
         "MAP_T20R0401": (8, 23),    # sem par no GBA: porta decorativa (bloqueada)
         "MAP_T20R0102": (20, 23)}   # sem par no GBA: porta decorativa (bloqueada)
TRAVA_X, TRAVA_Z0, TRAVA_Z1 = 31, 2, 29    # coluna global 31 (ultima da celula de Dawnmere), linhas 2-29: a saida leste
SAI = "placa da Route 1 (script 19): sai de Dawnmere, que no GBA nao tem essa placa; volta na Route 1 (etapa 4)"


def novo_json(j):
    for o in j["object_events"]:
        if o["script"] in OBJETOS:
            o["x"], o["z"] = w(*OBJETOS[o["script"]])
    j["bg_events"] = [b for b in j["bg_events"] if b["script"] != "19"]
    for b in j["bg_events"]:
        if b["script"] in PLACAS:
            b["x"], b["z"] = w(*PLACAS[b["script"]])
    for wp in j["warp_events"]:
        wp["x"], wp["z"] = w(*WARPS[wp["dest_header_id"]])
    for c in j["coord_events"]:
        if c["script"] == "_EV_scr_seq_T20_002 + 1":
            c["x"], c["z"] = X0 + TRAVA_X, Z0 + TRAVA_Z0
            c["width"], c["length"] = 1, TRAVA_Z1 - TRAVA_Z0 + 1
    return j


def diff(path_rel, old, new):
    return "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + path_rel, "b/" + path_rel))


def main(hg, out):
    rel = "data/eventdata/zone_event/057_T20.json"
    old = open(os.path.join(hg, rel)).read()
    new = json.dumps(novo_json(json.loads(old)), indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")
    open(os.path.join(out, "0922-dawnmere-eventos-gba.patch"), "w").write(diff(rel, old, new))
    rel = "data/scr_seq/scr_seq_0842_T20.s"
    old = open(os.path.join(hg, rel)).read()
    new = old.replace("// saida oeste (Route 1): sem Pokemon, volta um passo (GBA Palm040_ExitEast)",
                      "// saida leste (Route 1), como no GBA: sem Pokemon, volta um passo para oeste (Palm040_ExitEast)")
    a = new.rindex("_HT_StepBack:")
    new = new[:a] + new[a:].replace("step MOVEMENT_STEP_RIGHT, 1", "step MOVEMENT_STEP_LEFT, 1", 1)
    assert new != old
    open(os.path.join(out, "0923-dawnmere-trava-leste.patch"), "w").write(diff(rel, old, new))
    print("patches de eventos gerados em", out, "|", SAI)


if __name__ == "__main__":
    main(*sys.argv[1:3])
