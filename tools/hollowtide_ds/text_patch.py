#!/usr/bin/env python3
"""Troca mensagens de textos de HGSS (data/text/custom/NNN.txt) a partir de um JSON, como patch de conteudo.

Fonte: hollowtide_ds/data/texts.json  {"190": {"0": "Prof. Alex: ...", "1": "..."}, ...}
(indices de mensagem; escapes \\n \\r \\f como no msgenc; ou {"gba": "LabelDoGBA"} para trazer o texto do
GBA convertido por gba_text.py, com "replace"; ou {"hgss_replace": [[trecho, novo]]} para manter a fala do HGSS
num placeholder trocando so um nome de Johto/Kanto; e "engine:NNN": {"replace_all": [[trecho, novo]]} para os textos do
proprio hg-engine em data/text/NNN.txt: [[trecho, novo], ...] para adaptacoes registradas). As copias originais saem byte a byte da ROM (msg_dump.py).
Saida: hollowtide_ds/patches/content/0500-texts.patch. Uso: text_patch.py HG_ENGINE
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import gba_text

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(REPO, "hollowtide_ds/data/texts.json")
PATCH = os.path.join(REPO, "hollowtide_ds/patches/content/0500-texts.patch")


def main(hg):
    data = json.load(open(SRC, encoding="utf-8"))
    out = ""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "msg_dump.py"), hg, os.path.join(hg, "rom.nds"), tmp],
                       check=True, capture_output=True)
        for arc in sorted((a for a in data if not a.startswith("engine:")), key=int):
            name = f"{int(arc):03d}.txt"
            orig = open(os.path.join(tmp, name), encoding="utf-8", newline="").read()
            msgs = orig.split("\r\n")
            for i, t in data[arc].items():
                if i.startswith("_"):
                    continue
                if isinstance(t, dict) and "hgss_replace" in t:    # fala original do HGSS, so com nomes trocados
                    txt = msgs[int(i)]
                    for old, new in t["hgss_replace"]:
                        if old not in txt:
                            raise ValueError(f"{arc}/{i}: trecho do HGSS nao encontrado: {old!r}")
                        txt = txt.replace(old, new)
                    msgs[int(i)] = txt
                elif isinstance(t, dict):
                    labs = t["gba"] if isinstance(t["gba"], list) else [t["gba"]]   # varios labels: juntados com \\f
                    txt = "\\f".join(gba_text.text_of(l) for l in labs)
                    for old, new in t.get("replace", []):          # adaptacoes registradas (ex.: direcoes no mapa do DS)
                        if old not in txt:
                            raise ValueError(f"{arc}/{i}: trecho para trocar nao encontrado: {old!r}")
                        txt = txt.replace(old, new)
                    msgs += [""] * (int(i) + 1 - len(msgs))     # mensagens novas alem do fim do arquivo
                    msgs[int(i)] = txt
                else:
                    msgs += [""] * (int(i) + 1 - len(msgs))
                    msgs[int(i)] = t
            a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
            open(a, "w", encoding="utf-8", newline="").write(orig)
            open(b, "w", encoding="utf-8", newline="").write("\r\n".join(msgs))
            out += subprocess.run(["diff", "-u", "--label", f"a/data/text/custom/{name}", "--label", f"b/data/text/custom/{name}", a, b],
                                  capture_output=True).stdout.decode("utf-8")
        # textos do proprio hg-engine (data/text/NNN.txt): so trocas registradas de trechos
        for arc in sorted(a for a in data if a.startswith("engine:")):
            name = f"data/text/{int(arc[7:]):03d}.txt"
            orig = subprocess.run(["git", "-C", hg, "cat-file", "--filters", f"HEAD:{name}"], capture_output=True, check=True).stdout.decode("utf-8")
            new = orig
            if "linhas" in data[arc]:                      # linhas inteiras por indice (0 = primeira)
                ls = new.split("\n")
                for k, v in data[arc]["linhas"].items():
                    end = "\r" if ls[int(k)].endswith("\r") else ""
                    ls[int(k)] = v + end
                new = "\n".join(ls)
            for old, rep in data[arc].get("replace_all", []):
                if old not in new:
                    raise ValueError(f"{arc}: trecho nao encontrado: {old!r}")
                new = new.replace(old, rep)
            a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
            open(a, "w", encoding="utf-8", newline="").write(orig)
            open(b, "w", encoding="utf-8", newline="").write(new)
            out += subprocess.run(["diff", "-u", "--label", f"a/{name}", "--label", f"b/{name}", a, b], capture_output=True).stdout.decode("utf-8")
    open(PATCH, "w", encoding="utf-8", newline="").write(out)
    print(f"{len(data)} texto(s) -> {PATCH}")


if __name__ == "__main__":
    main(sys.argv[1])
