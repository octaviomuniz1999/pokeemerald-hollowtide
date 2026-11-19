#!/usr/bin/env python3
"""Lista rótulos de texto que ainda parecem estar em português. Uso: find_pt.py ARQUIVOS..."""
import re, sys
PT = re.compile(r"[ãõçáíóúâêô]|\b(voce|você|nao|não|para|com|uma|seu|sua|agua|água|esta|está|ate|até|pelo|pela|mae|aqui|muito|bem-vindo|vamos|minha|meu|essa|esse|depois|ginasio|insignia|treinador|obrigad[oa]|tambem|também|comporta|vila|cidade|rota|quer|siga|leia|ao|nos|das|dos|pronto|um|luzes|tente|esquerda|direita|holofotes?|apagaram|acendeu|sequencia|painel)\b", re.I)
for f in sys.argv[1:]:
    label, buf = None, []
    def flush():
        if label and buf and PT.search(" ".join(buf)):
            print(f"{f}: {label}: {' '.join(buf)[:90]}")
    for line in open(f, encoding="utf-8"):
        m = re.match(r"^(\w+)::?\s*$", line)
        if m:
            flush(); label, buf = m.group(1), []
        s = re.match(r'\s*\.string "(.*)"', line)
        if s: buf.append(s.group(1))
    flush()
