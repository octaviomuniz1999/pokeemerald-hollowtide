#!/usr/bin/env python3
"""Revisao de colisao dos mapas convertidos (auditoria de acabamento, 25/11): compara, tile a tile, a colisao do GBA
com a do DS na ROM pronta (blocos a/0/6/5 nas celulas da matriz 0).

- GBA bloqueado e DS andavel = passagem nova (erro, salvo agua: no DS a agua e surfavel, 0x15, como no GBA);
- GBA andavel e DS bloqueado = bloqueio novo (erro, salvo as excecoes documentadas: base de lampiao com modelo,
  rocha solta 'R', arbusto/arvore sobre tile andavel do GBA nao existe).
Mostra a lista e um resumo por mapa. Uso: check_colisao.py ROM  (codigo 1 se houver divergencia nao explicada)
A conversao bloqueia de proposito a planta inteira das construcoes e as copas das arvores (andaveis no GBA, por tras):
essas divergencias sao antigas. Para conferir o que uma rodada MUDOU: check_colisao.py ROM --antes ROM_ANTERIOR
(lista cada tile cuja colisao mudou entre as duas ROMs, com a letra da grade).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import ndspy.rom, ndspy.narc
from matrix import Matrix
from land_data import Land
import lunia_mundo as L
import gba2grade as G
import mapa_grade as M
from qa_visual import TAM


def main(rom_path):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    m = Matrix(ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files[0])
    lands = ndspy.narc.NARC(rom.getFileByName("a/0/6/5")).files
    cache = {}

    def perm(x, z):
        c = (x // 32, z // 32)
        if c not in cache:
            cache[c] = Land(lands[m.land[c[1] * m.w + c[0]]]).perms
        return cache[c][(z % 32) * 32 + x % 32]
    g = M.load(L.GRADE)
    total = 0
    for key, (name, _, _) in G.MAPS.items():
        j, Ly, w, h, vals = G.load_map(name)
        ox, oy = L.ORIGENS[key]
        novos_bloq, novas_pass = [], []
        for i, v in enumerate(vals):
            x, y = i % w, i // w
            col = (v >> 10) & 3 != 0
            p = perm(ox + x, oy + y)
            ds_bloq = bool(p & 0x8000)
            agua = (p & 0xFF) == 0x15
            t = g["tiles"][oy + y][ox + x]
            if col and not ds_bloq and not agua:
                novas_pass.append((x, y, t))
            elif not col and ds_bloq and t not in "SR":
                novos_bloq.append((x, y, t))
        print(f"{key}: {len(novas_pass)} passagem(ns) nova(s), {len(novos_bloq)} bloqueio(s) novo(s)")
        for x, y, t in novas_pass[:20]:
            print(f"   passagem nova em ({x},{y}) tile DS '{t}'")
        for x, y, t in novos_bloq[:20]:
            print(f"   bloqueio novo em ({x},{y}) tile DS '{t}'")
        total += len(novas_pass) + len(novos_bloq)
    print("RESULTADO colisao:", "ok" if not total else f"{total} divergencia(s)")
    return total


def diff(rom_path, antes_path):
    def perms(path):
        rom = ndspy.rom.NintendoDSRom.fromFile(path)
        m = Matrix(ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files[0])
        lands = ndspy.narc.NARC(rom.getFileByName("a/0/6/5")).files
        out = {}
        for c in L.CELLS:
            p = Land(lands[m.land[c[1] * m.w + c[0]]]).perms
            for k in range(1024):
                out[(c[0] * 32 + k % 32, c[1] * 32 + k // 32)] = p[k]
        return out
    a, b = perms(antes_path), perms(rom_path)
    g = M.load(L.GRADE)
    mud = [(xz, a[xz], b[xz]) for xz in sorted(b, key=lambda t: (t[1], t[0])) if a[xz] != b[xz]]
    def onde(x, z):
        for key, (ox, oy) in L.ORIGENS.items():
            w, h = TAM[key]
            if ox <= x < ox + w and oy <= z < oy + h:
                return f"{key} ({x - ox},{z - oy})"
        return f"fora dos mapas ({x},{z})"
    for (x, z), pa, pb in mud:
        print(f"{onde(x, z):28} {pa:#06x} -> {pb:#06x}  tile '{g['tiles'][z][x]}'")
    print(f"RESULTADO colisao mudada: {len(mud)} tile(s)")
    return mud


if __name__ == "__main__":
    if "--antes" in sys.argv:
        diff(sys.argv[1], sys.argv[sys.argv.index("--antes") + 1]); sys.exit(0)
    sys.exit(1 if main(sys.argv[1]) else 0)
