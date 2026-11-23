#!/usr/bin/env python3
"""Troca mensagens de textos de HGSS (data/text/custom/NNN.txt) a partir de um JSON, como patch de conteudo.

Fonte: hollowtide_ds/data/texts.json  {"190": {"0": "Prof. Alex: ...", "1": "..."}, ...}
(indices de mensagem; escapes \\n \\r \\f como no msgenc). As copias originais saem byte a byte da ROM (msg_dump.py).
Saida: hollowtide_ds/patches/content/0500-texts.patch. Uso: text_patch.py HG_ENGINE
"""
import json, os, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(REPO, "hollowtide_ds/data/texts.json")
PATCH = os.path.join(REPO, "hollowtide_ds/patches/content/0500-texts.patch")


def main(hg):
    data = json.load(open(SRC, encoding="utf-8"))
    out = ""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "msg_dump.py"), hg, os.path.join(hg, "rom.nds"), tmp],
                       check=True, capture_output=True)
        for arc in sorted(data, key=int):
            name = f"{int(arc):03d}.txt"
            orig = open(os.path.join(tmp, name), encoding="utf-8", newline="").read()
            msgs = orig.split("\r\n")
            for i, t in data[arc].items():
                if i.startswith("_"):
                    continue
                msgs[int(i)] = t
            a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
            open(a, "w", encoding="utf-8", newline="").write(orig)
            open(b, "w", encoding="utf-8", newline="").write("\r\n".join(msgs))
            out += subprocess.run(["diff", "-u", "--label", f"a/data/text/custom/{name}", "--label", f"b/data/text/custom/{name}", a, b],
                                  capture_output=True).stdout.decode("utf-8")
    open(PATCH, "w", encoding="utf-8", newline="").write(out)
    print(f"{sum(len([k for k in v if not k.startswith('_')]) for v in data.values())} mensagem(ns) em {len(data)} texto(s) -> {PATCH}")


if __name__ == "__main__":
    main(sys.argv[1])
