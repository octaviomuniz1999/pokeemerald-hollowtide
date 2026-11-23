#!/usr/bin/env python3
"""Nomes de lugar de Lunia nos mapas de HGSS que os hospedam (texto 279: um nome por MAPSEC, no indice do MAPSEC).

O nome que aparece ao entrar no mapa, no menu e no Pokegear vem do MAPSEC do header do mapa. Fonte:
hollowtide_ds/data/place_names.json ({"MAPSEC_NEW_BARK_TOWN": "Dawnmere Village", ...}).
Saida: hollowtide_ds/patches/content/0400-place-names.patch (data/text/custom/279.txt).
Uso: place_names.py HG_ENGINE
"""
import json, os, re, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(REPO, "hollowtide_ds/data/place_names.json")
PATCH = os.path.join(REPO, "hollowtide_ds/patches/content/0400-place-names.patch")


def main(hg):
    sec = {k: int(v) for k, v in re.findall(r"\.equ\s+(MAPSEC_\w+)\s*,\s*(\d+)", open(os.path.join(hg, "asm/include/map_sections.inc")).read())}
    names = json.load(open(SRC))
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "msg_dump.py"), hg, os.path.join(hg, "rom.nds"), tmp],
                       check=True, capture_output=True)
        orig = open(os.path.join(tmp, "279.txt"), encoding="utf-8", newline="").read()
        msgs = orig.split("\r\n")
        for k, v in names.items():
            if len(v) > 20:
                raise ValueError(f"nome longo demais para a placa do mapa: {v}")
            msgs[sec[k]] = v
        a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
        open(a, "w", encoding="utf-8", newline="").write(orig)
        open(b, "w", encoding="utf-8", newline="").write("\r\n".join(msgs))
        p = subprocess.run(["diff", "-u", "--label", "a/data/text/custom/279.txt", "--label", "b/data/text/custom/279.txt", a, b],
                           capture_output=True).stdout.decode("utf-8")
    open(PATCH, "w", encoding="utf-8", newline="").write(p)
    print(f"{len(names)} nome(s) de lugar -> {PATCH}")


if __name__ == "__main__":
    main(sys.argv[1])
