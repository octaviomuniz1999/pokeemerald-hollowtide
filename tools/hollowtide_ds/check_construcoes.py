#!/usr/bin/env python3
"""Confere se cada construcao do desenho global aparece de onde o jogador a ve (auditoria de acabamento, 25/11).

O HGSS carrega so os modelos da lista de construcoes (a/0/4/3) da area do header em que o jogador esta. Um modelo
que nao esta nessa lista some da tela, mesmo que o bloco dele esteja carregado. Foi o caso da casa da Route 2: o bloco
dela fica numa celula com o header de Breezeport (area de Olivine, lista 6), sem o modelo 0x25, e a casa sumia quando
o jogador chegava perto. Regra conferida aqui: todo modelo de um bloco tem de estar na lista da celula dele e na das
celulas vizinhas onde o jogador pode pisar (8 direcoes; a camera mostra uns 8 tiles alem da celula).

Uso: check_construcoes.py ROM  (sai com codigo 1 se faltar modelo em alguma lista)
"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ndspy.rom, ndspy.narc
from matrix import Matrix
from land_data import Land
import lunia_mundo as L

# header -> lista de construcoes da area (tabela de headers do ARM9: byte 1 = area; a/0/4/2: area -> lista)
LISTA_DO_HEADER = {60: 0, 33: 0, 67: 0, 34: 0, 35: 0, 77: 6}


def main(rom_path):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    m = Matrix(ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files[0])
    lands = ndspy.narc.NARC(rom.getFileByName("a/0/6/5")).files
    listas = ndspy.narc.NARC(rom.getFileByName("a/0/4/3")).files
    lista = {}
    for k in set(LISTA_DO_HEADER.values()):
        f = listas[k]; n = struct.unpack_from("<H", f)[0]
        lista[k] = set(struct.unpack_from(f"<{n}H", f, 2))
    cells = L.CELLS
    hdr = {c: m.headers[c[1] * m.w + c[0]] for c in cells}
    # celulas onde o jogador pode estar: alguma colisao livre (as de floresta pura nao contam)
    pisavel = {c for c in cells if any(not (p & 0x8000) for p in Land(lands[m.land[c[1] * m.w + c[0]]]).perms)}
    erros = 0
    for c in cells:
        ld = Land(lands[m.land[c[1] * m.w + c[0]]])
        for o in ld.objs:
            mdl, x, y, z = Land.describe(o)
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    v = (c[0] + dx, c[1] + dz)
                    if v not in hdr or v not in pisavel:
                        continue
                    lst = LISTA_DO_HEADER.get(hdr[v])
                    if lst is None:
                        print(f"celula {v}: header {hdr[v]} sem lista conhecida"); erros += 1; continue
                    if mdl not in lista[lst]:
                        onde = "na propria celula" if (dx, dz) == (0, 0) else f"vista da celula {v}"
                        print(f"modelo {mdl:#x} do bloco {c} (tile {c[0] * 32 + x:.1f},{c[1] * 32 + z:.1f}) fora da "
                              f"lista {lst} (header {hdr[v]}) {onde}")
                        erros += 1
    print("RESULTADO construcoes:", "ok" if not erros else f"{erros} falta(s)")
    return erros


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
