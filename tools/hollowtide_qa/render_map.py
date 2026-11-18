#!/usr/bin/env python3
"""Renderiza um mapa (map.bin + tilesets) em PNG para revisao artistica e de colisao, sem emulador.

Uso:
  render_map.py MAP_NAME_OU_PASTA saida.png [--events] [--collision] [--grid] [--scale N]
Ex.: render_map.py OldaleTown /tmp/harvestvale.png --events --grid

Camadas: os 8 tiles de cada metatile (camada de baixo + de cima) com as paletas reais do tileset.
--collision pinta de vermelho os tiles bloqueados; --events marca warps (azul), gatilhos (amarelo),
placas (ciano) e NPCs (magenta, com local_id).
"""
import argparse, json, os, re, struct
from functools import lru_cache
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NUM_TILES_PRIMARY, NUM_METATILES_PRIMARY, NUM_PALS_PRIMARY = 512, 512, 6


def _tileset_paths():
    hdr = open(f"{ROOT}/src/data/tilesets/headers.h").read()
    gfx = open(f"{ROOT}/src/data/tilesets/graphics.h").read() + open(f"{ROOT}/src/graphics.c").read()
    mts = open(f"{ROOT}/src/data/tilesets/metatiles.h").read()
    tiles_src = dict(re.findall(r'const u32 (gTilesetTiles_\w+)\[\] = INCGFX_U32\("([^"]+)"', gfx))
    mt_src = dict(re.findall(r'const u16 (gMetatiles_\w+)\[\] = INCBIN_U16\("([^"]+)"', mts))
    attr_src = dict(re.findall(r'const u16 (gMetatileAttributes_\w+)\[\] = INCBIN_U16\("([^"]+)"', mts))
    out = {}
    for name, body in re.findall(r'const struct Tileset (gTileset_\w+) =\s*\{(.*?)\};', hdr, re.S):
        f = dict(re.findall(r'\.(\w+) = (\w+),', body))
        if f.get("tiles") in tiles_src:
            t = tiles_src[f["tiles"]]
            out[name] = dict(tiles=f"{ROOT}/{t}", pal=f"{ROOT}/{os.path.dirname(t)}/palettes",
                             metatiles=f"{ROOT}/{mt_src[f['metatiles']]}",
                             attrs=f"{ROOT}/{attr_src[f['metatileAttributes']]}")
    return out


TILESETS = _tileset_paths()


def _read_pal(path):
    lines = open(path).read().split("\n")[3:19]
    return [tuple(int(v) for v in l.split()[:3]) for l in lines if l.strip()]


def _read_tiles(path):
    im = Image.open(path)
    w, h = im.size
    px = im.load()
    tiles = []
    for ty in range(h // 8):
        for tx in range(w // 8):
            tiles.append([[px[tx * 8 + x, ty * 8 + y] & 0xF for x in range(8)] for y in range(8)])
    return tiles


class TilesetPair:
    def __init__(self, primary, secondary):
        p, s = TILESETS[primary], TILESETS[secondary]
        self.tiles = _read_tiles(p["tiles"])[:NUM_TILES_PRIMARY]
        self.tiles += [[[0] * 8] * 8] * (NUM_TILES_PRIMARY - len(self.tiles))
        self.tiles += _read_tiles(s["tiles"])
        self.pals = [_read_pal(f"{p['pal']}/{i:02d}.pal") for i in range(NUM_PALS_PRIMARY)]
        self.pals += [_read_pal(f"{s['pal']}/{i:02d}.pal") for i in range(NUM_PALS_PRIMARY, 16)]
        mp = open(p["metatiles"], "rb").read()
        ms = open(s["metatiles"], "rb").read()
        self.metatiles = [struct.unpack_from("<8H", mp, i * 16) for i in range(len(mp) // 16)]
        self.metatiles += [(0,) * 8] * (NUM_METATILES_PRIMARY - len(self.metatiles))
        self.metatiles += [struct.unpack_from("<8H", ms, i * 16) for i in range(len(ms) // 16)]
        self.cache = {}

    def metatile(self, mt):
        if mt in self.cache:
            return self.cache[mt]
        im = Image.new("RGB", (16, 16), self.pals[0][0])
        px = im.load()
        ent = self.metatiles[mt] if mt < len(self.metatiles) else (0,) * 8
        for layer in range(2):
            for q in range(4):
                e = ent[layer * 4 + q]
                ti, hf, vf, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
                tile = self.tiles[ti] if ti < len(self.tiles) else [[0] * 8] * 8
                ox, oy = (q % 2) * 8, (q // 2) * 8
                for y in range(8):
                    for x in range(8):
                        c = tile[7 - y if vf else y][7 - x if hf else x]
                        if c == 0 and layer == 1:
                            continue
                        px[ox + x, oy + y] = self.pals[pal][c] if c else self.pals[0][0]
        self.cache[mt] = im
        return im


@lru_cache(None)
def _maps():
    lay = {l["id"]: l for l in json.load(open(f"{ROOT}/data/layouts/layouts.json"))["layouts"] if "id" in l}
    return lay


def render(map_name, out, events=False, collision=False, grid=False, scale=1):
    j = json.load(open(f"{ROOT}/data/maps/{map_name}/map.json"))
    L = _maps()[j["layout"]]
    w, h = L["width"], L["height"]
    data = open(f"{ROOT}/{L['blockdata_filepath']}", "rb").read()
    ts = TilesetPair(L["primary_tileset"], L["secondary_tileset"])
    im = Image.new("RGB", (w * 16, h * 16))
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(h):
        for x in range(w):
            v = struct.unpack_from("<H", data, 2 * (y * w + x))[0]
            im.paste(ts.metatile(v & 0x3FF), (x * 16, y * 16))
            if collision and (v >> 10) & 3:
                d.rectangle([x * 16, y * 16, x * 16 + 15, y * 16 + 15], fill=(255, 0, 0, 70))
    if grid:
        for x in range(0, w * 16, 16):
            d.line([x, 0, x, h * 16], fill=(0, 0, 0, 40))
        for y in range(0, h * 16, 16):
            d.line([0, y, w * 16, y], fill=(0, 0, 0, 40))
        for x in range(0, w, 5):
            for y in range(0, h, 5):
                d.text((x * 16 + 1, y * 16), f"{x},{y}", fill=(255, 255, 255, 200))
    if events:
        for wv in j.get("warp_events", []):
            d.rectangle([wv["x"] * 16 + 2, wv["y"] * 16 + 2, wv["x"] * 16 + 13, wv["y"] * 16 + 13], outline=(0, 90, 255, 255), width=2)
        for c in j.get("coord_events", []):
            d.rectangle([c["x"] * 16 + 4, c["y"] * 16 + 4, c["x"] * 16 + 11, c["y"] * 16 + 11], fill=(255, 220, 0, 180))
        for b in j.get("bg_events", []):
            d.ellipse([b["x"] * 16 + 4, b["y"] * 16 + 4, b["x"] * 16 + 11, b["y"] * 16 + 11], fill=(0, 230, 230, 200))
        for i, o in enumerate(j.get("object_events", []), 1):
            d.ellipse([o["x"] * 16 + 2, o["y"] * 16 + 2, o["x"] * 16 + 13, o["y"] * 16 + 13], outline=(255, 0, 255, 255), width=2)
            d.text((o["x"] * 16 + 4, o["y"] * 16 + 3), str(i), fill=(255, 0, 255, 255))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("map")
    ap.add_argument("out")
    ap.add_argument("--events", action="store_true")
    ap.add_argument("--collision", action="store_true")
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--scale", type=int, default=1)
    a = ap.parse_args()
    print(render(a.map, a.out, a.events, a.collision, a.grid, a.scale))
