#!/usr/bin/env python3
"""Corpus dos mapas oficiais (upstream) para aprender padroes de tiles."""
import json, os, struct, subprocess, functools
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
UPSTREAM = "99044bce"

@functools.lru_cache(None)
def layouts():
    up = json.loads(subprocess.check_output(["git", "-C", ROOT, "show", f"{UPSTREAM}:data/layouts/layouts.json"]))
    out = []
    for L in up["layouts"]:
        if "id" not in L:
            continue
        try:
            data = subprocess.check_output(["git", "-C", ROOT, "show", f"{UPSTREAM}:{L['blockdata_filepath']}"], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            continue
        w, h = L["width"], L["height"]
        bl = [struct.unpack_from("<H", data, 2 * i)[0] for i in range(w * h)]
        out.append(dict(id=L["id"], w=w, h=h, prim=L["primary_tileset"], sec=L["secondary_tileset"], bl=bl))
    return out

def maps_with(primary=None, secondary=None):
    return [L for L in layouts() if (primary is None or L["prim"] == primary) and (secondary is None or L["sec"] == secondary)]
