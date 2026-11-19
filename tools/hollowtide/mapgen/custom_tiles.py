#!/usr/bin/env python3
"""Metatiles compostos (Hollowtide) acrescentados ao FIM de tilesets secundarios, a partir do original do upstream.

Cada peca e montada com tiles 8x8 que ja existem (camada de baixo de um piso + camada de cima de um objeto) ou com
tiles derivados por recoloracao de indices de paleta (sem desenho novo). Rodar de novo regenera tudo do zero,
preservando os IDs na ordem de CUSTOM. Escreve custom_ids.json para o Canvas consultar.

Uso: custom_tiles.py
"""
import json, os, struct, subprocess, sys, io
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
UPSTREAM = "99044bce"


def _git_bytes(path):
    return subprocess.check_output(["git", "-C", ROOT, "show", f"{UPSTREAM}:{path}"])


def _mt(bin_, i):
    return list(struct.unpack_from("<8H", bin_, i * 16))


# definicoes por tileset secundario. Fontes: ("mt", id) usa as 4 entradas de baixo ou de cima de um metatile;
# ("recolor", id, {idx_origem: idx_destino}) copia a camada de cima recolorindo indices (gera tiles novos).
CUSTOM = {
    "lilycove": [
        # nome, camada de baixo, camada de cima, atributos copiados de
        ("lamp_top_cobble_lit", ("mt", 571, "bottom"), ("mt", 576, "top"), 576),
        ("lamp_top_cobble_unlit", ("mt", 571, "bottom"), ("recolor", 576, {9: 3, 10: 6}), 576),
        ("lamp_base_cobble", ("mt", 571, "bottom"), ("mt", 674, "top"), 674),
        ("lamp_top_grass_lit", ("mt", 1, "bottom"), ("mt", 576, "top"), 576),
        ("lamp_top_grass_unlit", ("mt", 1, "bottom"), ("recolor", 576, {9: 3, 10: 6}), 576),
        ("lamp_base_grass", ("mt", 1, "bottom"), ("mt", 674, "top"), 674),
    ],
}


def build(tsname):
    d = f"data/tilesets/secondary/{tsname}"
    mts = bytearray(_git_bytes(f"{d}/metatiles.bin"))
    attrs = bytearray(_git_bytes(f"{d}/metatile_attributes.bin"))
    tiles = Image.open(io.BytesIO(_git_bytes(f"{d}/tiles.png")))
    tiles.load()
    tw = tiles.size[0] // 8
    tile_list = []
    px = tiles.load()
    for ty in range(tiles.size[1] // 8):
        for tx in range(tw):
            tile_list.append([[px[tx * 8 + x, ty * 8 + y] for x in range(8)] for y in range(8)])
    prim = _git_bytes("data/tilesets/primary/general/metatiles.bin")
    n_base_mt = len(mts) // 16
    ids = {}
    for name, bot, top, attr_from in CUSTOM[tsname]:
        entries = []
        for layer, src in (("bottom", bot), ("top", top)):
            if src[0] == "mt":
                m = _mt(mts, src[1] - 512) if src[1] >= 512 else _mt(prim, src[1])
                part = m[:4] if src[2] == "bottom" else m[4:]
            else:  # recolor: camada de cima do metatile, tiles secundarios recoloridos
                m = _mt(mts, src[1] - 512)
                part = []
                for e in m[4:]:
                    ti = e & 0x3FF
                    if ti >= 512:
                        t = [[src[2].get(v, v) for v in row] for row in tile_list[ti - 512]]
                        if t != tile_list[ti - 512]:
                            tile_list.append(t)
                            e = (e & ~0x3FF) | (512 + len(tile_list) - 1)
                    part.append(e)
            entries += part
        mts += struct.pack("<8H", *entries)
        attrs += attrs[(attr_from - 512) * 2:(attr_from - 512) * 2 + 2]
        ids[name] = 512 + n_base_mt + len(ids)
    assert len(mts) // 16 <= 512 and len(tile_list) <= 512, "limite do tileset secundario"
    # grava tiles.png com as linhas extras (mesma paleta/modo indexado)
    rows = (len(tile_list) + tw - 1) // tw
    out = Image.new("P", (tw * 8, rows * 8), 0)
    out.putpalette(tiles.getpalette())
    po = out.load()
    for i, t in enumerate(tile_list):
        for y in range(8):
            for x in range(8):
                po[(i % tw) * 8 + x, (i // tw) * 8 + y] = t[y][x]
    out.save(f"{ROOT}/{d}/tiles.png")
    open(f"{ROOT}/{d}/metatiles.bin", "wb").write(mts)
    open(f"{ROOT}/{d}/metatile_attributes.bin", "wb").write(attrs)
    return ids, len(tile_list)


def main():
    all_ids = {}
    for ts in CUSTOM:
        ids, nt = build(ts)
        all_ids[ts] = ids
        print(ts, ids, "tiles:", nt)
    json.dump(all_ids, open(os.path.join(HERE, "custom_ids.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
