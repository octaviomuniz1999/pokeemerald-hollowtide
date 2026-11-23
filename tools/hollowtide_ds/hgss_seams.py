#!/usr/bin/env python3
"""Emendas andaveis entre os mapas externos de HGSS (matriz 0), lidas da colisao de cada bloco (a/0/6/5).

land_data de HGSS: 4 u32 (tamanho das permissoes = 2048, construcoes, modelo, BDHC), u16 0x1234, u16 N, N bytes,
depois 32x32 u16 de permissao (byte baixo = comportamento do tile, bit 0x8000 = bloqueado).
Para cada par de mapas vizinhos: quantos tiles atravessam a divisa a pe (os dois lados livres e sem agua) — 0 quer
dizer que a ligacao do HGSS ali e por caverna, portao, surf ou nao existe. Sem objetos (arvores de Cut, pedras):
eles sao eventos e somem quando os eventos forem trocados pelos de Lunia.
Saida: docs/hollowtide/ds/HGSS_EMENDAS.md. Uso: hgss_seams.py ROM
"""
import collections, json, os, struct, sys
import ndspy.narc, ndspy.rom
sys.path.insert(0, os.path.dirname(__file__))
from matrix import Matrix

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WATER = set(range(0x10, 0x1A)) | {0x22, 0x2A}          # agua, mar, cachoeira, agua rasa nao conta como chao


def perms(ld):
    p = 20 + struct.unpack_from("<H", ld, 18)[0] if struct.unpack_from("<H", ld, 16)[0] == 0x1234 else 16
    return struct.unpack_from("<1024H", ld, p)


def main(rom_path):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    lds = ndspy.narc.NARC(rom.getFileByName("a/0/6/5")).files
    mt = Matrix(ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files[0])
    names = {m["id"]: m["name"][4:] for m in json.load(open(os.path.join(REPO, "docs/hollowtide/ds/hgss_maps.json")))}
    W, H = mt.w * 32, mt.h * 32
    free = bytearray(W * H)
    owner = [0] * (W * H)
    for by in range(mt.h):
        for bx in range(mt.w):
            i = by * mt.w + bx
            land, hdr = mt.land[i], mt.headers[i]
            if land == 0xFFFF or land >= len(lds):
                continue
            pm = perms(lds[land])
            for ty in range(32):
                for tx in range(32):
                    v = pm[ty * 32 + tx]
                    g = (by * 32 + ty) * W + bx * 32 + tx
                    owner[g] = hdr
                    free[g] = 0 if (v & 0x8000) or (v & 0xFF) in WATER else 1
    cross = collections.Counter()
    for y in range(H):
        for x in range(W):
            g = y * W + x
            if not free[g]:
                continue
            for dx, dy in ((1, 0), (0, 1)):
                if x + dx < W and y + dy < H:
                    h = (y + dy) * W + x + dx
                    if free[h] and owner[h] != owner[g] and owner[g] and owner[h]:
                        cross[tuple(sorted((names[owner[g]], names[owner[h]])))] += 1
    md = ["# Emendas andáveis entre mapas externos de HGSS", "",
          "Gerado por `tools/hollowtide_ds/hgss_seams.py`: tiles que atravessam a divisa a pé (colisão dos blocos, sem água",
          "e sem objetos). Pares vizinhos na matriz que não aparecem aqui não se ligam a pé.", "",
          "| Mapa A | Mapa B | Tiles na divisa |", "|---|---|---|"]
    for (a, b), n in sorted(cross.items()):
        md.append(f"| `{a}` | `{b}` | {n} |")
    open(os.path.join(REPO, "docs/hollowtide/ds/HGSS_EMENDAS.md"), "w").write("\n".join(md) + "\n")
    print(len(cross), "emendas andaveis")
    return cross


if __name__ == "__main__":
    c = main(sys.argv[1])
    for (a, b), n in sorted(c.items()):
        if a[0] in "TR" and b[0] in "TR":
            print(a, b, n)
