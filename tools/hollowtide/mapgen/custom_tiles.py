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
    "rustboro": [
        ("rail_h", ("draw", "rail", 9), None, 699),          # ferrovia do patio de carga de Ferralia
        ("rail_end", ("draw", "rail_end", 9), None, 699),
        ("rail_end_e", ("draw", "rail_end_e", 9), None, 699),   # para-choque do lado leste (fim de linha)
        ("valve_closed", ("mt", 699, "bottom"), ("draw", "valve_closed", 9), 699),   # valvulas da usina (Pillarton)
        ("valve_open", ("mt", 699, "bottom"), ("draw", "valve_open", 9), 699),
    ],
    "lilycove": [
        # nome, camada de baixo, camada de cima, atributos copiados de
        ("lamp_top_cobble_lit", ("mt", 571, "bottom"), ("mt", 576, "top"), 576),
        ("lamp_top_cobble_unlit", ("mt", 571, "bottom"), ("recolor", 576, {9: 3, 10: 6}), 576),
        ("lamp_base_cobble", ("mt", 571, "bottom"), ("mt", 674, "top"), 674),
        ("lamp_top_grass_lit", ("mt", 1, "bottom"), ("mt", 576, "top"), 576),
        ("lamp_top_grass_unlit", ("mt", 1, "bottom"), ("recolor", 576, {9: 3, 10: 6}), 576),
        ("lamp_base_grass", ("mt", 1, "bottom"), ("mt", 674, "top"), 674),
        ("lamp_top_sand_lit", ("mt", 292, "bottom"), ("mt", 576, "top"), 576),      # farol provisorio no pontal
        ("lamp_top_sand_unlit", ("mt", 292, "bottom"), ("recolor", 576, {9: 3, 10: 6}), 576),
        ("lamp_base_sand", ("mt", 292, "bottom"), ("mt", 674, "top"), 674),
    ],
}


def _rail(end=False):
    """Trilho horizontal 16x16 (paleta 9 da Rustboro): lastro bege, dormentes marrons, trilhos de aco.
    end=True: para-choque (fim de linha) do lado esquerdo."""
    g = [[2 if (x * 7 + y * 3) % 5 else 3 for x in range(16)] for y in range(16)]
    for y in (0, 15):
        for x in range(16):
            g[y][x] = 1 if (x + y) % 3 else 2
    for sx in (1, 6, 11):
        for y in range(2, 14):
            g[y][sx] = g[y][sx + 1] = 4
        g[13][sx] = g[13][sx + 1] = 7
    for ry in (4, 10):
        for x in range(16):
            if end and x < 4:
                continue
            g[ry][x], g[ry + 1][x] = 5, 7
    if end:
        for y in range(3, 13):
            for x in range(1, 5):
                g[y][x] = 4 if 1 < x < 4 and 3 < y < 12 else 8
    return g


def _valve(opened):
    """Valvula (camada de cima, fundo transparente; paleta 9 da Rustboro): cano cinza, haste e volante.
    Fechada: volante marrom com raios em +; aberta: volante bege com raios em x."""
    g = [[0] * 16 for _ in range(16)]
    for x in range(1, 15):                      # cano
        g[10][x], g[11][x], g[12][x] = 5, 6, 7
    g[10][0] = g[11][0] = g[12][0] = 7; g[10][15] = g[11][15] = g[12][15] = 7
    for y in range(6, 10):                      # haste
        g[y][7], g[y][8] = 6, 7
    ring = 2 if opened else 4
    for y in range(0, 9):
        for x in range(3, 13):
            d = ((x - 7.5) ** 2 + (y - 4.0) ** 2) ** 0.5
            if 3.2 <= d <= 4.4:
                g[y][x] = ring
            elif d > 4.4 and d <= 4.9:
                g[y][x] = 8
    if opened:
        for k in range(-3, 4):
            for (x, y) in ((int(7.5 + k), int(4 + k)), (int(7.5 + k), int(4 - k))):
                if 0 <= y < 9:
                    g[y][x] = ring
    else:
        for k in range(-3, 4):
            g[4][int(7.5 + k)] = ring
            g[int(4 + k)][7] = ring
    g[4][7] = g[4][8] = 8
    return g


DRAW = {"rail": lambda: _rail(), "rail_end": lambda: _rail(end=True),
        "rail_end_e": lambda: [r[::-1] for r in _rail(end=True)],
        "valve_closed": lambda: _valve(False), "valve_open": lambda: _valve(True)}


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
    # slots de tile livres: em branco e sem uso em nenhum metatile (a Rustboro ja ocupa os 512 do PNG)
    used = {struct.unpack_from("<H", mts, i * 2)[0] & 0x3FF for i in range(len(mts) // 2)}
    free = [i for i, t in enumerate(tile_list) if i > 0 and not any(any(r) for r in t) and 512 + i not in used]

    def add_tile(t):
        if free:
            i = free.pop(0)
            tile_list[i] = t
            return i
        tile_list.append(t)
        return len(tile_list) - 1
    for name, bot, top, attr_from in CUSTOM[tsname]:
        entries = []
        for layer, src in (("bottom", bot), ("top", top)):
            if src is None:
                entries += [0, 0, 0, 0]
                continue
            if src[0] == "draw":
                g = DRAW[src[1]]()
                for (ox, oy) in ((0, 0), (8, 0), (0, 8), (8, 8)):
                    ti = add_tile([[g[oy + y][ox + x] for x in range(8)] for y in range(8)])
                    entries.append((512 + ti) | (src[2] << 12))
                continue
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
                            e = (e & ~0x3FF) | (512 + add_tile(t))
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
