#!/usr/bin/env python3
"""Lista textos que citam nomes de Hoenn/Emerald que não existem em Lunia. Uso: find_hoenn.py ARQUIVOS..."""
import re, sys
H = re.compile(r"\b(HOENN|BIRCH|LITTLEROOT|OLDALE|PETALBURG|RUSTBORO|DEWFORD|SLATEPORT|MAUVILLE|VERDANTURF|FALLARBOR|LAVARIDGE|FORTREE|LILYCOVE|MOSSDEEP|SOOTOPOLIS|EVER GRANDE|ROXANNE|NORMAN|MAY|BRENDAN|WALLY|STEVEN|DEVON|AQUA|MAGMA|ROUTE 10[1-9]|ROUTE 11[0-9]|ROUTE 12[0-9]|ROUTE 13[0-4])\b")
for f in sys.argv[1:]:
    label, buf = None, []
    def flush():
        if label and buf:
            t = " ".join(buf)
            m = H.findall(t)
            if m: print(f"{f}: {label}: {sorted(set(m))}: {t[:80]}")
    for line in open(f, encoding="utf-8"):
        mm = re.match(r"^(\w+)::?\s*$", line)
        if mm:
            flush(); label, buf = mm.group(1), []
        s = re.match(r'\s*\.string "(.*)"', line)
        if s: buf.append(s.group(1))
    flush()
