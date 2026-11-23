#!/usr/bin/env python3
"""Lacunas de sprites do hg-engine para as especies que Lunia usa (inventario de lunia_inventory.py).

No hg-engine, especie sem arte usa a do Bulbasaur como substituta (mesmo arquivo, byte a byte): batalha
(`male/front.png`, ou `female/front.png` nas especies so femeas, cujo `male/front.png` vem vazio), seguidor
(`overworld.png`) e icone (`icon.png`). Tambem confere as Megas e a Reversao Primal implicadas pelos itens dos times.
Uso: sprite_gaps.py HG_ENGINE INVENTARIO.json [SAIDA.md]
"""
import hashlib, json, os, re, sys, unicodedata

FORM_ALIAS = {"_HISUI": "_HISUIAN", "_ALOLA": "_ALOLAN", "_GALAR": "_GALARIAN", "_PALDEA": "_PALDEAN"}
SPECIAL = {"NIDORAN_F": "nidoran_f", "NIDORAN_M": "nidoran_m"}


def key(name):
    n = name[8:] if name.startswith("SPECIES_") else name
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode()
    n = n.replace("♀", "_F").replace("♂", "_M")
    n = re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_").upper()
    for a, b in FORM_ALIAS.items():
        if n.endswith(a):
            n = n[: -len(a)] + b
    return n


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None


def mega_of(species, item):
    it = key(item)
    if species == "KYOGRE" and it == "BLUE_ORB":
        return "kyogre_primal"
    if species == "GROUDON" and it == "RED_ORB":
        return "groudon_primal"
    m = re.match(r"([A-Z]+)ITE(_([XYZ]))?$", it)
    if m and it not in ("EVIOLITE", "WHITE_HERB") and it.startswith(species[:4]):
        return "mega_" + species.lower() + ("_" + m.group(3).lower() if m.group(3) else "")
    return None


def main(hg, inv_path, out=None):
    sp = os.path.join(hg, "data/graphics/sprites")
    base = {f: md5(os.path.join(sp, "bulbasaur", f)) for f in ("male/front.png", "overworld.png", "icon.png")}
    inv = json.load(open(inv_path))
    need = {}                                   # pasta -> de onde vem
    for s in inv["species"]:
        k = key(s)
        need.setdefault(SPECIAL.get(k, k.lower()), set()).add("dex")
    for t, v in inv["trainers"].items():
        for m in v["party"]:
            head = m["head"]
            if "@" in head:
                mg = mega_of(key(m["species"]), head.split("@", 1)[1].strip())
                if mg:
                    need.setdefault(mg, set()).add(t)
    rows = []
    for folder in sorted(need):
        d = os.path.join(sp, folder)
        if not os.path.isdir(d):
            rows.append((folder, "SEM PASTA", "-", "-")); continue
        front = os.path.join(d, "male/front.png")
        if os.path.getsize(front) == 0:
            front = os.path.join(d, "female/front.png")
        isbulba = folder == "bulbasaur"
        f_ok = "ok" if isbulba or md5(front) != base["male/front.png"] else "FALTA"
        o_ok = "ok" if isbulba or md5(os.path.join(d, "overworld.png")) not in (None, base["overworld.png"]) else "FALTA"
        if folder.startswith(("mega_", "kyogre_primal", "groudon_primal")):
            o_ok = "n/a"                         # forma de batalha: o seguidor usa a forma base
        i_ok = "ok" if isbulba or md5(os.path.join(d, "icon.png")) not in (None, base["icon.png"]) else "FALTA"
        rows.append((folder, f_ok, o_ok, i_ok))
    bad = [r for r in rows if "FALTA" in r or r[1] == "SEM PASTA"]
    lines = [f"# Lacunas de sprites do hg-engine para Lunia", "",
             f"Especies e formas conferidas: {len(rows)}; com alguma lacuna: {len(bad)}.", "",
             "| Pasta | Batalha | Seguidor | Ícone |", "|---|---|---|---|"]
    lines += [f"| `{a}` | {b} | {c} | {d} |" for a, b, c, d in bad]
    txt = "\n".join(lines) + "\n"
    if out:
        open(out, "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main(*sys.argv[1:4])
