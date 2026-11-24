#!/usr/bin/env python3
"""Teste rapido: grava um bloco gerado NO LUGAR do bloco original numa ROM pronta (mesmo tamanho de arquivo, com
enchimento), para reaproveitar savestates feitos nessa ROM (a tabela de arquivos nao muda). So para QA.
Uso: inplace_block.py ROM_ENTRADA ROM_SAIDA BLOCO MODULO_GERADOR   (a ROM de entrada ja tem o bloco gerado ou o original)
"""
import importlib, struct, sys
import ndspy.narc, ndspy.rom
src, dst, blk, mod = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
rom = ndspy.rom.NintendoDSRom.fromFile(src)
fid = rom.filenames.idOf("a/0/6/5")
narc = ndspy.narc.NARC(rom.files[fid])
orig_len = len(narc.files[blk])
allb = ndspy.narc.NARC(ndspy.rom.NintendoDSRom.fromFile("/home/user/blurosie/hg-engine/rom.nds").getFileByName("a/0/6/5")).files
new = importlib.import_module(mod).gerar(bytes(allb[blk]), [bytes(f) for f in allb])
assert len(new) <= orig_len, (len(new), orig_len)
narc.files[blk] = new + b"\0" * (orig_len - len(new))
data = narc.save()
raw = bytearray(open(src, "rb").read())
fat = struct.unpack_from("<I", raw, 0x48)[0]
a, b = struct.unpack_from("<II", raw, fat + 8 * fid)
assert b - a == len(data)
raw[a:b] = data
open(dst, "wb").write(raw)
print(f"bloco {blk}: {len(new)} bytes (vaga de {orig_len}) gravado no lugar em {dst}")
