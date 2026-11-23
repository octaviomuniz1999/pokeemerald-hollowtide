#!/usr/bin/env python3
"""Flags de historia de Lunia no DS, reaproveitando flags de eventos de Kanto que Lunia nao tem.

As flags do HGSS estao todas em uso ate 2911 (1360-2097 sao as de "treinador vencido"). Como o mundo de HGSS sai,
Lunia reaproveita flags de eventos que so aparecem num unico script de mapa de Kanto (ex.: "ganhou o TM19 da
Erika") e em nenhum codigo C do hg-engine — conferido a cada execucao. Sem MAPTEMP (zera ao trocar de mapa), sem
FLAG_UNK/SYS/HIDE.
Fonte: hollowtide_ds/data/flags.json {"FLAG_HT_NOME": "FLAG_DO_HGSS", ...} — so cresce; nomes novos pedidos na
linha de comando ganham a proxima flag livre.
Saida: hollowtide_ds/patches/content/0070-flags.patch (cria data/scr_seq/include/hollowtide_flags.inc).
Uso: flags.py HG_ENGINE [FLAG_HT_NOVA ...]
"""
import collections, glob, json, os, re, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(REPO, "hollowtide_ds/data/flags.json")
PATCH = os.path.join(REPO, "hollowtide_ds/patches/content/0070-flags.patch")
INC = "data/scr_seq/include/hollowtide_flags.inc"
KANTO = re.compile(r"_(T0[1-9]|T1[01]|R0[1-9]|R1[0-9]|R2[0-8]|D0[1-9])")


def pool(hg):
    flags = {k: int(v) for k, v in re.findall(r"\.equ\s+(FLAG_\w+)\s*,\s*(\d+)\b", open(os.path.join(hg, "asm/include/flags.inc")).read())}
    uses = collections.defaultdict(set)
    for f in glob.glob(os.path.join(hg, "data/scr_seq/*.s")) + glob.glob(os.path.join(hg, "data/eventdata/zone_event/*.json")):
        for m in set(re.findall(r"\bFLAG_\w+", open(f, errors="ignore").read())):
            uses[m].add(os.path.basename(f))
    ccode = "".join(open(f, errors="ignore").read() for f in glob.glob(os.path.join(hg, "src/**/*.c"), recursive=True)
                    + glob.glob(os.path.join(hg, "include/**/*.h"), recursive=True))
    out = []
    for k, v in flags.items():
        if k.startswith(("FLAG_UNK", "FLAG_TEMP", "FLAG_SYS", "FLAG_HIDE", "FLAG_MAPTEMP")) or k in ccode or v >= 1360:
            continue
        u = uses.get(k, set())
        if len(u) == 1 and KANTO.search(next(iter(u))):
            out.append((v, k, next(iter(u))))
    return sorted(out), flags


def main(hg, new_names):
    cands, flags = pool(hg)
    ok = {k for _, k, _ in cands}
    alloc = json.load(open(SRC)) if os.path.exists(SRC) else {}
    for name, hg_flag in alloc.items():
        if hg_flag not in ok:
            raise SystemExit(f"{name}: {hg_flag} deixou de ser exclusiva de um script de Kanto — rever")
    used = set(alloc.values())
    free = [k for _, k, _ in cands if k not in used]
    for n in new_names:
        if n not in alloc:
            alloc[n] = free.pop(0)
    json.dump(alloc, open(SRC, "w"), indent=1)
    where = {k: f for _, k, f in cands}
    inc = ["// gerado por tools/hollowtide_ds/flags.py — flags de Lunia em flags de eventos de Kanto que saem do jogo", ""]
    inc += [f".equ {n}, {flags[h]}  // {h} ({where[h]})" for n, h in alloc.items()]
    with tempfile.TemporaryDirectory() as tmp:
        c = os.path.join(tmp, "inc")
        open(c, "w").write("\n".join(inc) + "\n")
        p = subprocess.run(["diff", "-u", "--label", "/dev/null", "--label", "b/" + INC, "/dev/null", c], capture_output=True, text=True).stdout
    open(PATCH, "w").write(p)
    print(f"{len(alloc)} flag(s) de Lunia; livres no conjunto: {len(free)}")
    for n, h in alloc.items():
        print(f"  {n} = {h} ({flags[h]})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
