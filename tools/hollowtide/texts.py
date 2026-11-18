#!/usr/bin/env python3
"""Aplica textos do jogo a partir de arquivos legíveis, validando a largura real de cada linha.

Formato do arquivo de texto (UTF-8):
    ## file: data/maps/OldaleTown/scripts.inc
    == Palm060_TextWelcome
    HARVESTVALE
    North: ROUTE 1

    Fields of coffee and quiet canals.
    ==+ Palm099_NewText          (com "+": cria o rótulo no fim do arquivo se não existir)
    ...
Dentro de um bloco: linhas consecutivas formam uma caixa (1ª linha, \\n na 2ª, \\l nas seguintes);
linha em branco = nova caixa (\\p). O texto termina com $.

Uso: texts.py ARQUIVO.txt [--check]   (--check só valida, não escreve)
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAX_PX = 208  # largura útil da caixa de diálogo padrão (26 tiles)
PLACEHOLDER_PX = {"PLAYER": 42, "RIVAL": 42, "STR_VAR_1": 60, "STR_VAR_2": 60, "STR_VAR_3": 60, "KUN": 0}


def _widths():
    src = open(f"{ROOT}/src/fonts.c").read()
    m = re.search(r"gFontNormalLatinGlyphWidths\[\] = \{(.*?)\};", src, re.S)
    w = [int(v) for v in re.findall(r"\d+", m.group(1))]
    cmap = {}
    for line in open(f"{ROOT}/charmap.txt", encoding="utf-8"):
        mm = re.match(r"^'(\\?.)'\s*=\s*([0-9A-F]{2})\s*$", line)
        if mm:
            ch = mm.group(1)
            if ch.startswith("\\"):
                if ch[1] not in "'\"\\":
                    continue  # \l \p \n sao controles, nao glifos
                ch = ch[1]
            cmap[ch] = int(mm.group(2), 16)
    return w, cmap


WIDTHS, CMAP = _widths()


def line_px(line):
    px, i = 0, 0
    while i < len(line):
        if line[i] == "{":
            j = line.index("}", i)
            px += PLACEHOLDER_PX.get(line[i + 1:j], 48)
            i = j + 1
            continue
        if line.startswith("POKé", i):  # glifo comum, contado normalmente
            pass
        ch = line[i]
        if ch not in CMAP:
            raise ValueError(f"caractere sem glifo no charmap: {ch!r} em {line!r}")
        px += WIDTHS[CMAP[ch]]
        i += 1
    return px


def to_strings(paragraphs):
    out = []
    for pi, para in enumerate(paragraphs):
        for li, line in enumerate(para):
            sep = "" if li == len(para) - 1 else ("\\n" if li == 0 else "\\l")
            end = sep if li < len(para) - 1 else ("\\p" if pi < len(paragraphs) - 1 else "$")
            out.append(f'\t.string "{line}{end}"')
    return out


def parse(path):
    files, cur_file, cur = {}, None, None
    for raw in open(path, encoding="utf-8").read().split("\n"):
        if raw.startswith("## file:"):
            cur_file = raw.split(":", 1)[1].strip()
            files.setdefault(cur_file, [])
            continue
        m = re.match(r"^==(\+?)\s*(\w+)\s*$", raw)
        if m:
            cur = {"label": m.group(2), "create": bool(m.group(1)), "paras": [[]]}
            files[cur_file].append(cur)
            continue
        if cur is None or raw.startswith("#"):
            continue
        if raw.strip() == "":
            if cur["paras"][-1]:
                cur["paras"].append([])
        else:
            cur["paras"][-1].append(raw.rstrip())
    for f in files.values():
        for b in f:
            b["paras"] = [p for p in b["paras"] if p]
    return files


def validate(files):
    errs = []
    for f, blocks in files.items():
        for b in blocks:
            for p in b["paras"]:
                for line in p:
                    try:
                        px = line_px(line)
                    except ValueError as e:
                        errs.append(f"{b['label']}: {e}")
                        continue
                    if px > MAX_PX:
                        errs.append(f"{b['label']}: linha com {px}px (> {MAX_PX}): {line!r}")
    return errs


def apply(files):
    for f, blocks in files.items():
        path = f"{ROOT}/{f}"
        lines = open(path, encoding="utf-8").read().split("\n")
        for b in blocks:
            idx = next((i for i, l in enumerate(lines) if re.match(rf"^{b['label']}::?\s*$", l)), None)
            new = to_strings(b["paras"])
            if idx is None:
                if not b["create"]:
                    raise SystemExit(f"rótulo não encontrado: {b['label']} em {f}")
                lines += ["", f"{b['label']}:"] + new
                continue
            j = idx + 1
            while j < len(lines) and lines[j].strip().startswith(".string"):
                j += 1
            lines[idx + 1:j] = new
        open(path, "w", encoding="utf-8").write("\n".join(lines))


if __name__ == "__main__":
    files = parse(sys.argv[1])
    errs = validate(files)
    for e in errs:
        print("ERRO:", e)
    n = sum(len(v) for v in files.values())
    if errs:
        sys.exit(1)
    if "--check" not in sys.argv:
        apply(files)
    print(f"{n} textos {'validados' if '--check' in sys.argv else 'aplicados'} em {len(files)} arquivo(s)")
