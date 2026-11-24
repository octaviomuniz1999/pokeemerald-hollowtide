#!/usr/bin/env python3
"""Blocos de mapa do HeartGold (land_data, NARC a/0/6/5) — leitura e edicao: objetos 3D e colisao.

Formato de cada bloco (32x32 tiles), conferido nos arquivos da ROM:
  4 u32: tamanhos das secoes (permissoes = 2048, construcoes, modelo do terreno .nsbmd, alturas .bdhc)
  u16 0x1234, u16 N, N bytes (secao extra de HGSS)
  permissoes: 32x32 u16 (byte baixo = comportamento do tile; bit 0x8000 = bloqueado)
  construcoes: entradas de 48 bytes — u32 modelo (NARC a/0/4/0, precisa estar na lista da area em a/0/4/3),
     x, y, z em ponto fixo 16.16 (u16 fracao + s16 inteiro, em tiles, a partir do centro do bloco), 3 u32 rotacao,
     3 u32 escala (0x1000 = 1,0), 2 u32 zerados. Um objeto de 1 tile no tile (tx, ty) fica em x = tx-16+0,5, z = ty-16+0,5.
  terreno .nsbmd, depois alturas .bdhc (nao mexidos aqui).
O hg-engine nao cobre mapas; as edicoes do Hollowtide ficam em `land.json` na pasta de patches e sao gravadas na ROM
pronta pelo build.sh, como a matriz:
  [{"land": 0, "nota": "...",
    "objetos": [{"modelo": 27, "tile": [20, 14], "y": 1}],         (acrescenta construcoes)
    "remover": [3],                                                 (indices de construcoes originais a tirar)
    "colisao": [{"tiles": [[20, 14]], "bloqueado": true}]}]         (liga/desliga o bit 0x8000; "comportamento": N opcional)
  ou {"land": 57, "gerador": "mapa_teste"}: o modulo (tools/hollowtide_ds/) gera o bloco inteiro — modelo 3D, alturas e
  colisao — a partir do bloco original (de onde so aproveita os materiais);
  ou {"land": 57, "grade": "arquivo.txt"}: setor desenhado em grade de texto (mapa_grade.py; caminho relativo ao land.json);
  ou {"global": "arquivo.txt", "matriz": 0, "celula": [x, y], "headers": {...}}: desenho de varios blocos (mapa_global.py).
Uso: land_data.py ROM.nds land.json [land.json ...]   (grava na propria ROM)
     land_data.py ROM.nds --show LAND                 (objetos e colisao de um bloco)
"""
import json, struct, sys
import ndspy.narc, ndspy.rom

ENTRY = 48


class Land:
    def __init__(self, data):
        self.sizes = list(struct.unpack_from("<4I", data, 0))
        magic, n = struct.unpack_from("<HH", data, 16)
        assert magic == 0x1234, "bloco sem a secao extra de HGSS"
        self.head = bytes(data[:20 + n])
        p = 20 + n
        self.perms = list(struct.unpack_from("<1024H", data, p)); p += self.sizes[0]
        nb = self.sizes[1] // ENTRY
        self.objs = [bytes(data[p + ENTRY * k:p + ENTRY * (k + 1)]) for k in range(nb)]; p += self.sizes[1]
        self.rest = bytes(data[p:])                     # terreno + alturas, intactos
        assert len(self.rest) == self.sizes[2] + self.sizes[3], "tamanhos de secao nao batem"

    @staticmethod
    def obj(model, tx, ty, y=1.0):
        fx = lambda v: struct.pack("<i", int(round(v * 65536)))
        return (struct.pack("<I", model) + fx(tx - 16 + 0.5) + fx(y) + fx(ty - 16 + 0.5) + b"\0" * 12
                + struct.pack("<3I", 0x1000, 0x1000, 0x1000) + b"\0" * 8)

    @staticmethod
    def describe(o):
        model = struct.unpack_from("<I", o, 0)[0]
        x, y, z = (struct.unpack_from("<i", o, 4 + 4 * i)[0] / 65536 for i in range(3))
        return model, x + 16, y, z + 16

    def pack(self):
        self.sizes[1] = ENTRY * len(self.objs)
        head = struct.pack("<4I", *self.sizes) + self.head[16:]
        return head + struct.pack("<1024H", *self.perms) + b"".join(self.objs) + self.rest


def apply(rom_path, json_paths):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    fid = rom.filenames.idOf("a/0/6/5")
    narc = ndspy.narc.NARC(rom.files[fid])
    count = 0
    for jp in json_paths:
        for e in json.load(open(jp)):
            if "global" in e:                          # desenho de varios blocos: blocos novos + matriz (mapa_global.py)
                import os, mapa_global
                count += mapa_global.apply_global(rom, narc, e, os.path.dirname(os.path.abspath(jp)))
                continue
            if "grade" in e:                           # setor desenhado em grade de texto (mapa_grade.py)
                import os, mapa_grade
                path = os.path.join(os.path.dirname(os.path.abspath(jp)), e["grade"])
                narc.files[e["land"]] = mapa_grade.gerar(bytes(narc.files[e["land"]]), [bytes(f) for f in narc.files], path)
                count += 1
                continue
            if "gerador" in e:                         # bloco inteiro gerado (modelo, alturas, colisao): ver mapa_teste.py
                import importlib
                gen = importlib.import_module(e["gerador"])
                narc.files[e["land"]] = gen.gerar(bytes(narc.files[e["land"]]), [bytes(f) for f in narc.files])
                count += 1
                continue
            ld = Land(narc.files[e["land"]])
            for k in sorted(e.get("remover", []), reverse=True):
                del ld.objs[k]
            for o in e.get("objetos", []):
                ld.objs.append(Land.obj(o["modelo"], *o["tile"], o.get("y", 1.0)))
            for c in e.get("colisao", []):
                for tx, ty in c["tiles"]:
                    v = ld.perms[ty * 32 + tx]
                    if "comportamento" in c:
                        v = (v & 0xFF00) | c["comportamento"]
                    v = (v | 0x8000) if c.get("bloqueado") else (v & ~0x8000 if c.get("bloqueado") is False else v)
                    ld.perms[ty * 32 + tx] = v
            narc.files[e["land"]] = ld.pack()
            count += 1
    rom.files[fid] = narc.save()
    rom.saveToFile(rom_path)
    print(f"land_data: {count} bloco(s) editado(s) em {rom_path}")


def show(rom_path, land):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    ld = Land(ndspy.narc.NARC(rom.getFileByName("a/0/6/5")).files[land])
    print(f"bloco {land}: secoes {ld.sizes}; {len(ld.objs)} construcoes")
    for k, o in enumerate(ld.objs):
        m, x, y, z = Land.describe(o)
        print(f"  {k:2} modelo {m:3} (0x{m:x})  tile x={x:6.2f} z={z:6.2f}  y={y:.2f}")
    print("    " + "".join(str(i % 10) for i in range(32)))
    for ty in range(32):
        row = ""
        for tx in range(32):
            v = ld.perms[ty * 32 + tx]
            row += "#" if v & 0x8000 else ("~" if 0x10 <= (v & 0xFF) < 0x1A else ".")
        print(f"{ty:3} " + row)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--show":
        show(sys.argv[1], int(sys.argv[3]))
    else:
        apply(sys.argv[1], sys.argv[2:])
