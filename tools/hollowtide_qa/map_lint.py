#!/usr/bin/env python3
"""Linter de mapas Hollowtide.

Verifica em cada mapa:
  - metatile vazio (8 entradas zeradas) ou fora do tileset  -> ERRO
  - colisao divergente do padrao aprendido nos mapas oficiais do Emerald (upstream):
      * metatile quase sempre BLOQUEADO aparecendo passavel   -> "anda em parede/penhasco/arvore"
      * metatile quase sempre PASSAVEL aparecendo bloqueado    -> "parede invisivel"
  - warps/gatilhos/NPCs fora do mapa ou sobre tile bloqueado (exceto portas/NPC parado)
Uso: map_lint.py [MAPA ...]   (sem argumentos: todos os mapas tocados pelo Hollowtide)
"""
import collections, json, os, struct, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UPSTREAM = "99044bce"  # expansion sem Hollowtide: referencia de colisao
sys.path.insert(0, os.path.dirname(__file__))
from render_map import TILESETS  # noqa: E402

lay = {l["id"]: l for l in json.load(open(f"{ROOT}/data/layouts/layouts.json"))["layouts"] if "id" in l}


def blocks(L, data=None):
    data = data or open(f"{ROOT}/{L['blockdata_filepath']}", "rb").read()
    return [struct.unpack_from("<H", data, 2 * i)[0] for i in range(L["width"] * L["height"])]


def metatile_table(ts):
    b = open(TILESETS[ts]["metatiles"], "rb").read()
    return [struct.unpack_from("<8H", b, i * 16) for i in range(len(b) // 16)]


def learn_reference():
    """(tileset, metatile) -> Counter(colisao) nos layouts do upstream."""
    ref = collections.defaultdict(collections.Counter)
    up_layouts = json.loads(subprocess.check_output(["git", "-C", ROOT, "show", f"{UPSTREAM}:data/layouts/layouts.json"]))
    for L in up_layouts["layouts"]:
        if "id" not in L:
            continue
        try:
            data = subprocess.check_output(["git", "-C", ROOT, "show", f"{UPSTREAM}:{L['blockdata_filepath']}"], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            continue
        for v in blocks(L, data):
            mt = v & 0x3FF
            ts = L["primary_tileset"] if mt < 512 else L["secondary_tileset"]
            ref[(ts, mt)][(v >> 10) & 3 != 0] += 1
    return ref


def hollowtide_maps():
    out = subprocess.check_output(["git", "-C", ROOT, "diff", "--name-only", UPSTREAM, "--", "data/maps"]).decode().split()
    return sorted({p.split("/")[2] for p in out if p.endswith("map.json")})


def lint(name, ref, mtcache):
    j = json.load(open(f"{ROOT}/data/maps/{name}/map.json"))
    L = lay[j["layout"]]
    w, h = L["width"], L["height"]
    bl = blocks(L)
    issues = []
    for ts in (L["primary_tileset"], L["secondary_tileset"]):
        mtcache.setdefault(ts, metatile_table(ts))
    for i, v in enumerate(bl):
        x, y = i % w, i // w
        mt, col = v & 0x3FF, (v >> 10) & 3 != 0
        ts = L["primary_tileset"] if mt < 512 else L["secondary_tileset"]
        tab = mtcache[ts]
        idx = mt if mt < 512 else mt - 512
        if idx >= len(tab):
            issues.append(("ERRO", x, y, f"metatile {mt} fora do tileset {ts}"))
            continue
        if not any(tab[idx]):
            issues.append(("ERRO", x, y, f"metatile {mt} vazio"))
            continue
        c = ref.get((ts, mt)) if j["layout"].startswith("LAYOUT_PALM") else None   # layouts vanilla sao a propria referencia
        if c and sum(c.values()) >= 8:
            blocked_ratio = c[True] / sum(c.values())
            if blocked_ratio >= 0.95 and not col:
                issues.append(("AVISO", x, y, f"metatile {mt} passavel (bloqueado em {blocked_ratio:.0%} dos mapas oficiais)"))
            elif blocked_ratio <= 0.05 and col:
                issues.append(("AVISO", x, y, f"metatile {mt} bloqueado (passavel em {1 - blocked_ratio:.0%} dos mapas oficiais)"))
    def blocked(x, y):
        return (bl[y * w + x] >> 10) & 3 != 0
    # degrau impossivel: dois tiles andaveis vizinhos com elevacoes diferentes (sem 0/15 de transicao nem agua 1).
    # So nos mapas gerados (Palm*): os mapas vanilla reaproveitados tem tiles de elevacao 4 em cantos inalcancaveis.
    for y in (range(h) if name.startswith("Palm") else ()):
        for x in range(w):
            e = bl[y * w + x] >> 12
            if blocked(x, y) or e in (0, 1, 15):
                continue
            for dx, dy in ((1, 0), (0, 1)):
                X, Y = x + dx, y + dy
                if X < w and Y < h and not blocked(X, Y):
                    e2 = bl[Y * w + X] >> 12
                    if e2 not in (0, 1, 15) and e2 != e:
                        issues.append(("ERRO", x, y, f"degrau impossivel: elevacao {e} ao lado de {e2} em ({X},{Y})"))
    for kind in ("coord_events", "bg_events"):
        for e in j.get(kind, []):
            if not (0 <= e["x"] < w and 0 <= e["y"] < h):
                issues.append(("ERRO", e["x"], e["y"], f"{kind} fora do mapa"))
            elif kind == "coord_events" and blocked(e["x"], e["y"]):
                issues.append(("ERRO", e["x"], e["y"], f"gatilho {e.get('script')} em tile bloqueado"))
    for wv in j.get("warp_events", []):
        if not (0 <= wv["x"] < w and 0 <= wv["y"] < h):
            issues.append(("ERRO", wv["x"], wv["y"], f"warp para {wv['dest_map']} fora do mapa"))
    for o in j.get("object_events", []):
        if not (0 <= o["x"] < w and 0 <= o["y"] < h):
            issues.append(("ERRO", o["x"], o["y"], f"NPC {o.get('local_id') or o['graphics_id']} fora do mapa"))
    return issues


def main(names):
    ref = learn_reference()
    mtcache = {}
    total = collections.Counter()
    for n in names or hollowtide_maps():
        iss = lint(n, ref, mtcache)
        cnt = collections.Counter(i[0] for i in iss)
        total.update(cnt)
        print(f"== {n}: {cnt.get('ERRO', 0)} erros, {cnt.get('AVISO', 0)} avisos")
        groups = collections.defaultdict(list)
        for sev, x, y, msg in iss:
            groups[(sev, msg)].append((x, y))
        for (sev, msg), pts in sorted(groups.items()):
            print(f"   {sev}: {msg} em {len(pts)} tile(s): {pts[:8]}{' ...' if len(pts) > 8 else ''}")
    print(f"TOTAL: {total.get('ERRO', 0)} erros, {total.get('AVISO', 0)} avisos")
    return 1 if total.get("ERRO") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
