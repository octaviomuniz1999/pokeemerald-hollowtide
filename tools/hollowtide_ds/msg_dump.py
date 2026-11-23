#!/usr/bin/env python3
"""Extrai os textos do HeartGold (NARC a/0/2/7) em .txt editaveis que voltam ao ROM byte a byte.

O `msgenc -d` do hg-engine escreve as quebras dentro das mensagens (\\n, \\r = rolar, \\f = limpar) como caracteres
crus, e o `msgenc -e` le os mesmos caracteres como separadores de mensagem: o texto despejado por `make dump_scripts`
nao volta igual ao ROM. Aqui o decodificador usa um charmap com marcadores para esses tres codigos e troca os
marcadores pelas sequencias de escape (\\n, \\r, \\f), que o charmap normal codifica de volta. Arquivos sempre lidos
e gravados com newline="" (o separador de mensagens e \\r\\n).

Uso: msg_dump.py HG_ENGINE ROM SAIDA [--check]
  --check: recodifica cada arquivo e compara com o ROM (23/11/2026: 829/829 iguais).
Saida: SAIDA/NNN.txt e SAIDA/keys.csv (chave de cada arquivo, para o `msgenc -e -k`).
"""
import os, re, subprocess, sys, tempfile
import ndspy.narc, ndspy.rom

MARK = {"": "\\n", "": "\\r", "": "\\f"}


def decode_charmap(hg, out):
    cm = open(os.path.join(hg, "charmap.txt"), encoding="utf-8").read()
    for line, mark in (("E000=\\n", ""), ("25BC=\\r", ""), ("25BD=\\f", "")):
        assert line in cm, line
        cm = cm.replace(line, line.split("=")[0] + "=" + mark)
    open(out, "w", encoding="utf-8").write(cm)


def main(hg, rom_path, out, check):
    msgenc = os.path.join(hg, "tools", "msgenc")
    os.makedirs(out, exist_ok=True)
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    narc = ndspy.narc.NARC(rom.getFileByName("a/0/2/7"))
    bad, keys = [], []
    with tempfile.TemporaryDirectory() as tmp:
        cm = os.path.join(tmp, "charmap_dec.txt")
        decode_charmap(hg, cm)
        b, r = os.path.join(tmp, "m.bin"), os.path.join(tmp, "r.bin")
        for i, data in enumerate(narc.files):
            open(b, "wb").write(data)
            t = os.path.join(out, f"{i:03d}.txt")
            res = subprocess.run([msgenc, "-d", "-c", cm, t, b], check=True, capture_output=True, text=True).stdout
            key = "0x" + re.search(r"Key: ([0-9a-fA-F]+)", res).group(1)
            keys.append(f"{i:03d},{key}")
            s = open(t, encoding="utf-8", newline="").read()
            for k, v in MARK.items():
                s = s.replace(k, v)
            open(t, "w", encoding="utf-8", newline="").write(s)
            if check:
                p = subprocess.run([msgenc, "-e", "-k", key, "-c", os.path.join(hg, "charmap.txt"), t, r],
                                   capture_output=True)
                if p.returncode or open(r, "rb").read() != data:
                    bad.append(i)
    open(os.path.join(out, "keys.csv"), "w").write("\n".join(keys) + "\n")
    print(f"{len(narc.files)} arquivos em {out}" + (f"; diferentes do ROM: {len(bad)} {bad[:20]}" if check else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) != 3:
        raise SystemExit(__doc__)
    sys.exit(main(*a, check="--check" in sys.argv))
