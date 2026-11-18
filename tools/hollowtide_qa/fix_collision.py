#!/usr/bin/env python3
"""Aplica colisao/elevacao de referencia (padrao dos mapas oficiais) a um layout, preservando a geometria.

Para cada bloco, se o metatile tem referencia confiavel (>= MIN_SAMPLES ocorrencias no upstream e
>= CONF de concordancia), a colisao e ajustada; a elevacao so e ajustada quando a referencia e agua (1)
ou quando o bloco estava com elevacao 0 (indefinida) e a referencia e confiavel.
Uso: fix_collision.py MAPA [--dry-run]
"""
import collections, json, os, struct, subprocess, sys

sys.path.insert(0, os.path.dirname(__file__))
import map_lint as ML  # noqa: E402

MIN_SAMPLES, CONF = 8, 0.95


def learn():
    col = collections.defaultdict(collections.Counter)
    elev = collections.defaultdict(collections.Counter)
    up = json.loads(subprocess.check_output(["git", "-C", ML.ROOT, "show", f"{ML.UPSTREAM}:data/layouts/layouts.json"]))
    for L in up["layouts"]:
        if "id" not in L:
            continue
        try:
            data = subprocess.check_output(["git", "-C", ML.ROOT, "show", f"{ML.UPSTREAM}:{L['blockdata_filepath']}"], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            continue
        for v in ML.blocks(L, data):
            mt = v & 0x3FF
            ts = L["primary_tileset"] if mt < 512 else L["secondary_tileset"]
            col[(ts, mt)][(v >> 10) & 3] += 1
            elev[(ts, mt)][v >> 12] += 1
    return col, elev


def dominant(counter):
    tot = sum(counter.values())
    if tot < MIN_SAMPLES:
        return None
    val, n = counter.most_common(1)[0]
    return val if n / tot >= CONF else None


def fix(name, dry=False, refs=None):
    col, elev = refs or learn()
    j = json.load(open(f"{ML.ROOT}/data/maps/{name}/map.json"))
    L = ML.lay[j["layout"]]
    path = f"{ML.ROOT}/{L['blockdata_filepath']}"
    bl = ML.blocks(L)
    changed = collections.Counter()
    unknown = collections.Counter()
    for i, v in enumerate(bl):
        mt, c, e = v & 0x3FF, (v >> 10) & 3, v >> 12
        ts = L["primary_tileset"] if mt < 512 else L["secondary_tileset"]
        dc, de = dominant(col[(ts, mt)]), dominant(elev[(ts, mt)])
        if dc is None:
            unknown[mt] += 1
        nc = c if dc is None else dc
        ne = e
        if de is not None and (de == 1 or e == 0):
            ne = de
        if (nc, ne) != (c, e):
            changed[mt] += 1
            bl[i] = mt | (nc << 10) | (ne << 12)
    if not dry:
        open(path, "wb").write(struct.pack(f"<{len(bl)}H", *bl))
    print(f"{name}: {sum(changed.values())} blocos ajustados; metatiles sem referencia confiavel: "
          f"{dict(unknown.most_common(12))}")
    return changed, unknown


if __name__ == "__main__":
    refs = learn()
    dry = "--dry-run" in sys.argv
    for n in [a for a in sys.argv[1:] if not a.startswith("--")]:
        fix(n, dry, refs)
