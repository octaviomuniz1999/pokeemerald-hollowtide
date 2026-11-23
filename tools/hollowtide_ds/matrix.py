#!/usr/bin/env python3
"""Matrizes de mapa do HeartGold (NARC a/0/4/1) — leitura, edicao e aplicacao por JSON depois do build.

Formato de cada matriz: u8 largura, u8 altura, u8 tem_headers, u8 tem_alturas, u8 tamanho_do_nome, nome; depois
(se houver) largura*altura u16 de map header, largura*altura u8 de altura, e largura*altura u16 de land_data (bloco
32x32 com modelo 3D, colisao e permissoes; a/0/6/5). 0xFFFF / bloco 208 na matriz 0 = vazio.

O hg-engine nao cobre mapas; as edicoes de matriz do Hollowtide ficam em `matrix.json` na pasta de patches:
  [{"matrix": 0, "x": 19, "y": 12, "land": 0, "header": 33, "altura": 0}, ...]   (header e altura opcionais)
Uso: matrix.py ROM.nds matrix.json [matrix.json ...]  (grava na propria ROM)
     matrix.py ROM.nds --show N X0 Y0 X1 Y1         (mostra header/land de um retangulo)
"""
import json, struct, sys
import ndspy.narc, ndspy.rom


class Matrix:
    def __init__(self, data):
        self.w, self.h, hh, ha, nl = data[:5]
        self.name = bytes(data[5:5 + nl])
        p = 5 + nl
        n = self.w * self.h
        self.headers = list(struct.unpack_from(f"<{n}H", data, p)) if hh else None
        p += 2 * n if hh else 0
        self.alts = list(data[p:p + n]) if ha else None
        p += n if ha else 0
        self.land = list(struct.unpack_from(f"<{n}H", data, p))
        assert p + 2 * n == len(data), "formato de matriz inesperado"

    def pack(self):
        n = self.w * self.h
        out = bytearray([self.w, self.h, int(self.headers is not None), int(self.alts is not None), len(self.name)])
        out += self.name
        if self.headers is not None:
            out += struct.pack(f"<{n}H", *self.headers)
        if self.alts is not None:
            out += bytes(self.alts)
        out += struct.pack(f"<{n}H", *self.land)
        return bytes(out)

    def set(self, x, y, land=None, header=None, altura=None):
        i = y * self.w + x
        if land is not None:
            self.land[i] = land
        if header is not None:
            self.headers[i] = header
        if altura is not None:
            self.alts[i] = altura


def apply(rom_path, json_paths):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    fid = rom.filenames.idOf("a/0/4/1")
    narc = ndspy.narc.NARC(rom.files[fid])
    count = 0
    for jp in json_paths:
        for e in json.load(open(jp)):
            m = Matrix(narc.files[e["matrix"]])
            m.set(e["x"], e["y"], e.get("land"), e.get("header"), e.get("altura"))
            narc.files[e["matrix"]] = m.pack()
            count += 1
    rom.files[fid] = narc.save()
    rom.saveToFile(rom_path)
    print(f"matriz: {count} celula(s) em {rom_path}")


def show(rom_path, n, x0, y0, x1, y1):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    m = Matrix(ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files[n])
    print(f"matriz {n}: {m.w}x{m.h} {m.name}")
    for y in range(y0, y1 + 1):
        print(y, [(m.headers[y * m.w + x] if m.headers else None, m.land[y * m.w + x]) for x in range(x0, x1 + 1)])


if __name__ == "__main__":
    if len(sys.argv) >= 8 and sys.argv[2] == "--show":
        show(sys.argv[1], *map(int, sys.argv[3:8]))
    elif len(sys.argv) >= 3:
        apply(sys.argv[1], sys.argv[2:])
    else:
        raise SystemExit(__doc__)
