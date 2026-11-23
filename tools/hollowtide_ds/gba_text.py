#!/usr/bin/env python3
"""Textos do GBA (labels .string dos scripts) no formato de texto do DS (msgenc / data/text).

- Codigos: \\n fica \\n; \\l (rolar uma linha) -> \\r; \\p (novo paragrafo) -> \\f; $ final sai.
- {PLAYER} -> {STRVAR_1 3, 0, 0}; ' -> ’ (o charmap do DS nao tem o apostrofo reto) (buffer 0: o script chama buffer_players_name 0 antes).
- Caixa: o GBA escreve nomes em maiusculas (MOM, PROF. ALEX, POKéMON); o DS usa caixa mista. So os nomes da lista
  abaixo mudam — e so a grafia, o texto e o mesmo.
Uso como modulo: text_of(label) -> str. Linha de comando: gba_text.py LABEL [LABEL...]
"""
import glob, os, re, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CASE = [
    ("POKéMON", "Pokémon"), ("POKéDEX", "Pokédex"), ("POKé BALLS", "Poké Balls"), ("POKé BALL", "Poké Ball"),
    ("PROF. ALEX", "Prof. Alex"), ("MOM", "Mom"), ("ATLAS", "Atlas"), ("DAWNMERE", "Dawnmere"),
    ("HARVESTVALE", "Harvestvale"), ("NEVARD", "Nevard"), ("ROUTE", "Route"), ("GYM", "Gym"), ("LAB", "Lab"),
    ("BAG", "Bag"), ("B BUTTON", "B Button"), ("TEAM PALM", "Team Palm"),
    # cabecalhos de placa, todos em maiusculas no GBA
    ("VILLAGE", "Village"), ("VILLAGER", "Villager"), ("LEADER", "Leader"), ("BADGE", "Badge"),
    ("HARVEST", "Harvest"), ("BREEZEPORT", "Breezeport"), ("CITY", "City"), ("BULLET", "Bullet"), ("SEED", "Seed"), ("COFFEE FIELDS", "Coffee Fields"),
    ("WATER KIOSK", "Water Kiosk"), ("DRYING YARD", "Drying Yard"), ("IRRIGATION SCHEDULE", "Irrigation Schedule"),
    ("WATER UNDER CONTRACT", "Water Under Contract"), ("THE NEIGHBORS", "The Neighbors"), ("HOUSE", "House"),
]
_cache = None


def _all_scripts():
    global _cache
    if _cache is None:
        files = glob.glob(os.path.join(REPO, "data/maps/*/scripts.inc")) + glob.glob(os.path.join(REPO, "data/scripts/*.inc"))
        _cache = "\n".join(open(f, encoding="utf-8").read() for f in files)
    return _cache


def raw(label):
    m = re.search(r"^%s::?\s*\n((?:\s*\.string\s+\"(?:[^\"\\]|\\.)*\"\s*\n?)+)" % re.escape(label), _all_scripts(), re.M)
    if not m:
        raise KeyError(f"label de texto do GBA nao encontrado: {label}")
    return "".join(re.findall(r"\.string\s+\"((?:[^\"\\]|\\.)*)\"", m.group(1)))


def convert(s):
    s = s.rstrip("$")
    s = s.replace("\\l", "\\r").replace("\\p", "\\f")
    s = s.replace("{PLAYER}", "{STRVAR_1 3, 0, 0}")
    s = s.replace("'", "’")                       # o charmap do DS so tem o apostrofo tipografico
    esc = {"\\n": "\x01", "\\r": "\x02", "\\f": "\x03"}   # para "\\nPROF" nao contar o n como letra
    for k, v in esc.items():
        s = s.replace(k, v)
    for a, b in CASE:
        s = re.sub(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(a), b, s)
    for k, v in esc.items():
        s = s.replace(v, k)
    s = re.sub(r"(?<=[a-z])’S\b", "’s", s)             # "Prof. Alex’S" -> "Prof. Alex’s"
    if re.search(r"\{(?!STRVAR_1 3, 0, 0\})", s):
        raise ValueError(f"codigo de texto do GBA sem equivalente: {s}")
    return s


def text_of(label):
    return convert(raw(label))


if __name__ == "__main__":
    for lab in sys.argv[1:]:
        print(lab, "=>", text_of(lab))
