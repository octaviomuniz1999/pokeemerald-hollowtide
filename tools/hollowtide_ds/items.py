#!/usr/bin/env python3
"""Itens-chave de Lunia no hg-engine, reaproveitando vagas de itens que Lunia nao usa.

Item novo de verdade no hg-engine exige entrada na tabela de icones gerada (itemgra.mk) e nos arquivos de texto
"custom"; reaproveitar uma vaga existente (com o icone que o GBA ja usava) e mais seguro. Fonte:
hollowtide_ds/data/items.json:
  {"ITEM_RELIC_GOLD": {"alias": "ITEM_ATLAS_MEDALLION", "name": "Atlas Medallion", "plural": "Atlas Medallions",
                       "description": "linha\\nlinha\\nlinha", "key_item": true}}
Muda: data/itemdata/itemdata.c (bolso de itens-chave, nao pode jogar fora, preco 0), data/text/222.txt (nome, no
indice do item), os 4 textos da geracao do item (descricao, nome com artigo, plural, "deu o item"), e cria
data/scr_seq/include/hollowtide_items.inc (.equ ITEM_ATLAS_MEDALLION, 586).
Saida: hollowtide_ds/patches/content/0060-items.patch. Uso: items.py HG_ENGINE
"""
import json, os, re, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(REPO, "hollowtide_ds/data/items.json")
PATCH = os.path.join(REPO, "hollowtide_ds/patches/content/0060-items.patch")
INC = "data/scr_seq/include/hollowtide_items.inc"
GEN_BOUNDS = ["ITEM_ENIGMA_STONE", "ITEM_REVEAL_GLASS", "ITEM_EON_FLUTE", "ITEM_UNKNOWN_1073", "ITEM_LEGEND_PLATE", "ITEM_CANARI_BREAD"]


def git_show(hg, path):
    return subprocess.run(["git", "-C", hg, "cat-file", "--filters", f"HEAD:{path}"], capture_output=True, check=True).stdout.decode("utf-8")


def main(hg):
    consts = {k: int(v) for k, v in re.findall(r"#define\s+(ITEM_\w+)\s+(\d+)\b", git_show(hg, "include/constants/item.h"))}
    items = json.load(open(SRC, encoding="utf-8"))
    files = {}

    def get(p):
        if p not in files:
            files[p] = [git_show(hg, p)]
            files[p].append(files[p][0])
        return files[p][1]

    def put(p, s):
        files[p][1] = s

    def set_line(p, idx, text):
        s = get(p)
        lines = s.split("\r\n") if "\r\n" in s else s.split("\n")
        sep = "\r\n" if "\r\n" in s else "\n"
        lines[idx] = text
        put(p, sep.join(lines))

    inc = ["// gerado por tools/hollowtide_ds/items.py — itens de Lunia nas vagas reaproveitadas", ""]
    for slot, it in items.items():
        iid = consts[slot]
        # dados: bolso de itens-chave
        p = "data/itemdata/itemdata.c"
        s = get(p)
        m = re.search(r"\n\[%s\] =\n\{\n(.*?)\n\},\n" % re.escape(slot), s, re.S)
        body = m.group(1)
        if it.get("key_item"):
            body = re.sub(r"ITEM_PRICE\(\d+\)", "ITEM_PRICE(0)", body)
            body = re.sub(r"\.prevent_toss = \w+", ".prevent_toss = TRUE", body)
            body = re.sub(r"\.fieldPocket = \w+", ".fieldPocket = POCKET_KEY_ITEMS", body)
            body = re.sub(r"\.flingPower = \d+", ".flingPower = 0", body)
        put(p, s[:m.start(1)] + body + s[m.end(1):])
        # textos
        set_line("data/text/222.txt", iid, it["name"])
        gen = next(i for i, b in enumerate(GEN_BOUNDS) if iid <= consts[b])
        base = 830 + gen * 4
        off = iid - (consts[GEN_BOUNDS[gen - 1]] + 1) if gen else iid
        article = "an" if it["name"][0].lower() in "aeiou" else "a"
        set_line(f"data/text/{base}.txt", off, it["description"])
        set_line(f"data/text/{base + 1}.txt", off, f"{article} {{COLOR 255}}{it['name']}{{COLOR 0}}")
        set_line(f"data/text/{base + 2}.txt", off, f"{{COLOR 255}}{it['plural']}{{COLOR 0}}")
        set_line(f"data/text/{base + 3}.txt", off, f"{article} {{COLOR 255}}{it['name']}{{COLOR 0}}")
        inc.append(f".equ {it['alias']}, {iid}  // vaga de {slot}")
    out = ""
    with tempfile.TemporaryDirectory() as tmp:
        for p, (a_txt, b_txt) in sorted(files.items()):
            a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
            open(a, "w", encoding="utf-8", newline="").write(a_txt)
            open(b, "w", encoding="utf-8", newline="").write(b_txt)
            out += subprocess.run(["diff", "-u", "--label", f"a/{p}", "--label", f"b/{p}", a, b], capture_output=True).stdout.decode("utf-8")
        c = os.path.join(tmp, "inc")
        open(c, "w").write("\n".join(inc) + "\n")
        out += subprocess.run(["diff", "-u", "--label", "/dev/null", "--label", "b/" + INC, "/dev/null", c], capture_output=True).stdout.decode("utf-8")
    open(PATCH, "w", encoding="utf-8", newline="").write(out)
    print(f"{len(items)} item(ns) -> {PATCH}")


if __name__ == "__main__":
    main(sys.argv[1])
