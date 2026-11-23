#!/usr/bin/env python3
"""Catalogo dos mapas de HGSS (caminho A: a geometria que Lunia vai reaproveitar).

Le a tabela de map headers do arm9 (0x020F6BE0, 24 bytes por mapa: area, matriz em +4, scripts, textos, musicas,
eventos, mapsec...), as matrizes (a/0/4/1) e os nomes de asm/include/maps.inc. Para cada mapa: a matriz, as celulas
(blocos 32x32) que ocupa, o retangulo, quantos NPCs/warps/placas tem (a/0/3/2) e se tem tabela de encontro.
Saida: docs/hollowtide/ds/hgss_maps.json + resumo em Markdown (docs/hollowtide/ds/HGSS_MAPAS.md).
Uso: hgss_catalog.py HG_ENGINE ROM
"""
import json, os, re, struct, sys
import ndspy.narc, ndspy.rom
sys.path.insert(0, os.path.dirname(__file__))
from matrix import Matrix

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HDR = 0x020F6BE0


def main(hg, rom_path):
    names = {}
    for k, v in re.findall(r"\.equ\s+(MAP_\w+)\s*,\s*(\d+)", open(os.path.join(hg, "asm/include/maps.inc")).read()):
        names[int(v)] = k
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    arm9 = rom.loadArm9()
    sec = next(s for s in arm9.sections if s.ramAddress <= HDR < s.ramAddress + len(s.data))
    base = HDR - sec.ramAddress
    n_maps = max(names) + 1
    mats = ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files
    evs = ndspy.narc.NARC(rom.getFileByName("a/0/3/2")).files
    maps = {}
    for m in range(n_maps):
        wild, area, unk2, matrix, scripts, lvl, msg, mday, mnight, events = struct.unpack_from("<BBHHHHHHHH", sec.data, base + 24 * m)
        mapsec = sec.data[base + 24 * m + 20] if False else struct.unpack_from("<H", sec.data, base + 24 * m + 18)[0] & 0xFF
        e = evs[events] if events < len(evs) else b""
        cnt = {}
        try:
            p = 0
            for kind, size in (("placas", 0x14), ("npcs", 0x20), ("warps", 0x0C), ("gatilhos", 0x10)):
                k = struct.unpack_from("<I", e, p)[0]; cnt[kind] = k; p += 4 + k * size
        except struct.error:
            cnt = {}
        maps[m] = {"id": m, "name": names.get(m, f"MAP_{m}"), "matrix": matrix, "events": events, "wild": wild,
                   "music_day": mday, "mapsec": mapsec, **cnt}
    # celulas de cada header nas matrizes que tem headers
    for mi, data in enumerate(mats):
        mt = Matrix(data)
        if mt.headers is None:
            continue
        for y in range(mt.h):
            for x in range(mt.w):
                h = mt.headers[y * mt.w + x]
                if h in maps and mt.land[y * mt.w + x] not in (0xFFFF,):
                    maps[h].setdefault("cells", []).append((mi, x, y))
    for m in maps.values():
        c = m.get("cells", [])
        if c:
            xs, ys = [x for _, x, _ in c], [y for _, _, y in c]
            m["rect"] = [min(xs), min(ys), max(xs), max(ys)]
            m["n_cells"] = len(c)
            m["world_matrix"] = c[0][0]
    out = os.path.join(REPO, "docs/hollowtide/ds/hgss_maps.json")
    json.dump(list(maps.values()), open(out, "w"), indent=0)
    # resumo: mapas externos da matriz 0 (o mundo de Johto/Kanto)
    rows = sorted((m for m in maps.values() if m.get("world_matrix") == 0), key=lambda m: (m["rect"][1], m["rect"][0]))
    md = ["# Mapas externos de HGSS na matriz do mundo (matriz 0)", "",
          "Gerado por `tools/hollowtide_ds/hgss_catalog.py`. Blocos de 32×32 tiles; retângulo em células da matriz 0.", "",
          "| Mapa | id | Blocos | Retângulo (x0,y0–x1,y1) | NPCs | Warps | Placas | Encontros |", "|---|---|---|---|---|---|---|---|"]
    for m in rows:
        r = m["rect"]
        md.append(f"| `{m['name']}` | {m['id']} | {m['n_cells']} | {r[0]},{r[1]}–{r[2]},{r[3]} | {m.get('npcs','?')} | "
                  f"{m.get('warps','?')} | {m.get('placas','?')} | {'sim' if m['wild'] != 0xFF else '—'} |")
    open(os.path.join(REPO, "docs/hollowtide/ds/HGSS_MAPAS.md"), "w").write("\n".join(md) + "\n")
    print(f"{len(maps)} mapas; externos na matriz 0: {len(rows)}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
