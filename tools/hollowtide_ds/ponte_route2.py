#!/usr/bin/env python3
"""Ponte provisoria Harvestvale <-> Route 2 do prototipo (CP-DS-03B, etapa 6).

Com Dawnmere, Route 1 e Harvestvale nos mapas originais (celulas (21,13)-(24,16)), a saida sul de Harvestvale (GBA,
Palm080_LeaveColheita) ainda nao tem a Route 2 original do outro lado: a Route 2 do prototipo (Route 30 do HGSS)
continua ao norte das celulas antigas da Cherrygrove. Ate a Route 2 ser convertida, uma ponte de dois scripts:
  - Harvestvale, saida sul depois do Nevard (_HT_ExitOk do scr_seq_T21_002): warp para o comeco da Route 2 do prototipo
    (548, 382), olhando para o norte; o gatilho da saida passa a valer tambem com VAR_SCENE_CHERRYGROVE_CITY_OW = 3
    (o ginasio poe 3 ao vencer o Nevard);
  - Route 2, ultima linha antes das celulas antigas (z 383, x 547-550): warp para a saida sul de Harvestvale (727, 522),
    olhando para o norte (scr_seq_R30_002, que estava sem uso).
Sai quando a Route 2 for convertida do GBA. Gera 0705-ponte-provisoria-route2.patch sobre o hg-engine montado com a
pasta de conteudo ate o 0704 (sem o 0705: reverta-o com patch -R antes de regenerar).
Uso: ponte_route2.py HG_ENGINE PASTA_SAIDA
"""
import difflib, json, os, sys

R2 = (548, 382)                  # comeco da Route 2 do prototipo (Route 30), logo acima das celulas antigas
HV = (727, 522)                  # saida sul de Harvestvale no desenho global (GBA 18,34)


def diff(rel, old, new):
    """Diff unificado aplicavel pelo patch(1), com a marca de arquivo sem quebra de linha no fim."""
    out = []
    for line in difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + rel, "b/" + rel):
        out.append(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n")
    return "".join(out)


def main(hg, out):
    parts = []
    rel = "data/scr_seq/scr_seq_0850_T21.s"
    old = open(os.path.join(hg, rel)).read()
    a = "_HT_ExitOk:\n\tsetvar VAR_SCENE_CHERRYGROVE_CITY_OW, 3\n\treleaseall\n\tend\n"
    assert a in old
    new = old.replace(a, "_HT_ExitOk:\n\tsetvar VAR_SCENE_CHERRYGROVE_CITY_OW, 3\n"
                         "\t// ponte provisoria (ponte_route2.py): a Route 2 original ainda nao existe; vai para a do prototipo\n"
                         f"\twarp MAP_R30, 0, {R2[0]}, {R2[1]}, DIR_NORTH\n\treleaseall\n\tend\n")
    parts.append(diff(rel, old, new))

    rel = "data/eventdata/zone_event/064_T21.json"
    old = open(os.path.join(hg, rel)).read()
    j = json.loads(old)
    saida = [c for c in j["coord_events"] if c["script"] == "_EV_scr_seq_T21_002 + 1"]
    assert saida and all(c["value"] != 3 for c in saida)
    j["coord_events"].append(dict(saida[0], value=3))
    new = json.dumps(j, indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")
    parts.append(diff(rel, old, new))

    rel = "data/scr_seq/scr_seq_0227_R30.s"
    old = open(os.path.join(hg, rel)).read()
    a = "scr_seq_R30_001:\nscr_seq_R30_002:\n"
    assert a in old
    new = old.replace(a, "scr_seq_R30_001:\n").replace(
        "scr_seq_R30_000:\n", "// ponte provisoria (ponte_route2.py): descendo a Route 2 do prototipo, chega-se a saida sul de\n"
        "// Harvestvale nos mapas originais (as celulas antigas da Cherrygrove ficaram sem eventos)\n"
        f"scr_seq_R30_002:\n\tlockall\n\twarp MAP_T21, 0, {HV[0]}, {HV[1]}, DIR_NORTH\n\treleaseall\n\tend\n\n"
        "scr_seq_R30_000:\n", 1)
    parts.append(diff(rel, old, new))

    rel = "data/eventdata/zone_event/031_R30.json"
    old = open(os.path.join(hg, rel)).read()
    j = json.loads(old)
    assert not j["coord_events"]
    j["coord_events"] = [{"script": "_EV_scr_seq_R30_002 + 1", "x": 547, "z": 383, "width": 4, "length": 1, "y": 0,
                          "value": 0, "var": "VAR_TEMP_x4001"}]
    new = json.dumps(j, indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")
    parts.append(diff(rel, old, new))

    open(os.path.join(out, "0705-ponte-provisoria-route2.patch"), "w").write("".join(parts))
    print("0705-ponte-provisoria-route2.patch gerado em", out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
