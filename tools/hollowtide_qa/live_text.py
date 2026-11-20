#!/usr/bin/env python3
"""Textos vivos: a partir das entradas reais de cada mapa alcancavel (NPCs, placas, gatilhos, scripts do mapa),
segue os scripts que podem rodar e lista os textos que casam com o padrao. Uso: live_text.py REGEX (rodar na raiz)."""
import re, glob, os, json, sys
files=glob.glob('data/maps/*/scripts.inc')+glob.glob('data/scripts/*.inc')+['data/event_scripts.s']+glob.glob('data/text/*.inc')
body={}; strings={}
for f in files:
    cur=None
    for ln in open(f, errors='ignore'):
        m=re.match(r"^(\w+)::?\s*(@.*)?$",ln.rstrip())
        if m: cur=m.group(1); body.setdefault(cur,[]); continue
        if cur:
            body[cur].append(ln)
            if '.string' in ln: strings.setdefault(cur,[]).append(ln.strip())
maps={os.path.basename(os.path.dirname(p)):json.load(open(p)) for p in glob.glob('data/maps/*/map.json')}
byid={j['id']:k for k,j in maps.items()}
reach=set(k for k in maps if k.startswith('Palm'))|{'LittlerootTown','LittlerootTown_BrendansHouse_1F','LittlerootTown_BrendansHouse_2F','LittlerootTown_MaysHouse_1F','LittlerootTown_MaysHouse_2F','LittlerootTown_ProfessorBirchsLab'}
fr=list(reach)
while fr:
    k=fr.pop(); j=maps.get(k)
    if not j: continue
    for w in j.get('warp_events',[]):
        d=byid.get(w['dest_map'])
        if d and d not in reach: reach.add(d); fr.append(d)
    for c in j.get('connections',[]) or []:
        d=byid.get(c['map'])
        if d and d not in reach: reach.add(d); fr.append(d)
pat=re.compile(sys.argv[1])
tok=re.compile(r"\b[A-Za-z_]\w+\b")
for k in sorted(reach):
    j=maps[k]; start=set()
    for o in j.get('object_events',[]): start.add(o.get('script',''))
    for e in j.get('coord_events',[])+j.get('bg_events',[]): start.add(e.get('script',''))
    start.add(f"{k}_MapScripts")
    seen=set(); st=[s for s in start if s in body]
    while st:
        s=st.pop()
        if s in seen: continue
        seen.add(s)
        for ln in body.get(s,[]):
            if '.string' in ln: continue
            for t in tok.findall(ln):
                if t in body and t not in seen and not t.startswith(('Common_','EventScript_','Std_','gText_')) : st.append(t)
    bad=[(s,l) for s in seen for l in strings.get(s,[]) if pat.search(l)]
    if bad: print(k, len(bad), sorted(set(s for s,_ in bad))[:5])
