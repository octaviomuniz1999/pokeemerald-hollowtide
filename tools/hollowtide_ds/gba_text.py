#!/usr/bin/env python3
"""Textos do GBA (labels .string dos scripts) no formato de texto do DS (msgenc / data/text).

- Codigos: \\n fica \\n; \\l (rolar uma linha) -> \\r; \\p (novo paragrafo) -> \\f; $ final sai.
- {PLAYER} -> {STRVAR_1 3, 0, 0}; {X_ARROW} -> setas do charmap do DS; ' -> ’ (o charmap do DS nao tem o apostrofo reto) (buffer 0: o script chama buffer_players_name 0 antes).
- Caixa: o GBA escreve nomes em maiusculas (MOM, PROF. ALEX, POKéMON); o DS usa caixa mista. So os nomes da lista
  abaixo mudam — e so a grafia, o texto e o mesmo.
Uso como modulo: text_of(label) -> str. Linha de comando: gba_text.py LABEL [LABEL...]
"""
import glob, os, re, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CASE = [
    ("POKéMON", "Pokémon"), ("POKéDEX", "Pokédex"), ("POKé BALLS", "Poké Balls"), ("POKé BALL", "Poké Ball"),
    ("PROF. ALEX", "Prof. Alex"), ("ALEX", "Alex"), ("PROFESSOR", "Professor"), ("MOM", "Mom"), ("ATLAS", "Atlas"), ("DAWNMERE", "Dawnmere"),
    ("HARVESTVALE", "Harvestvale"), ("NEVARD", "Nevard"), ("ROUTE", "Route"), ("GYM", "Gym"), ("LAB", "Lab"),
    ("BAG", "Bag"), ("B BUTTON", "B Button"), ("TEAM PALM", "Team Palm"),
    # cabecalhos de placa, todos em maiusculas no GBA
    ("VILLAGE", "Village"), ("VILLAGER", "Villager"), ("LEADER", "Leader"), ("BADGE", "Badge"),
    ("HARVEST", "Harvest"), ("BREEZEPORT", "Breezeport"), ("CITY", "City"), ("THEATER OF ECHOES", "Theater of Echoes"),
    ("THEATER", "Theater"), ("JAY", "Jay"), ("ECHO", "Echo"), ("FERRALIA", "Ferralia"), ("WEST BEACH TRAIL", "West Beach Trail"),
    ("LIGHTHOUSE KEEPER'S HOUSE", "Lighthouse Keeper's House"), ("LIGHTHOUSE KEEPER’S HOUSE", "Lighthouse Keeper’s House"), ("BULLET", "Bullet"), ("SEED", "Seed"), ("COFFEE FIELDS", "Coffee Fields"),
    ("WATER KIOSK", "Water Kiosk"), ("DRYING YARD", "Drying Yard"), ("IRRIGATION SCHEDULE", "Irrigation Schedule"),
    ("WATER UNDER CONTRACT", "Water Under Contract"), ("THE NEIGHBORS", "The Neighbors"), ("HOUSE", "House"),
]
KEEP_CAPS = {"TM", "HM", "HP", "PP", "OK", "KO", "TV", "PC", "LEFT", "RIGHT", "HAHAHA", "I"}   # siglas e enfase (refletores da Jay)
SMALL = {"OF", "THE", "AND"}
_cache = None


def _all_scripts():
    global _cache
    if _cache is None:
        files = (glob.glob(os.path.join(REPO, "data/maps/*/scripts.inc")) + glob.glob(os.path.join(REPO, "data/scripts/*.inc"))
                 + glob.glob(os.path.join(REPO, "data/text/*.inc")))
        _cache = "\n".join(open(f, encoding="utf-8").read() for f in files)
    return _cache


def raw(label):
    m = re.search(r"^%s::?\s*\n((?:\s*\.string\s+\"(?:[^\"\\]|\\.)*\"\s*\n?)+)" % re.escape(label), _all_scripts(), re.M)
    if not m:
        raise KeyError(f"label de texto do GBA nao encontrado: {label}")
    return "".join(re.findall(r"\.string\s+\"((?:[^\"\\]|\\.)*)\"", m.group(1)))


def convert(s):
    s = s.rstrip("$")
    # no DS (HGSS), \\r limpa a caixa e comeca pagina nova e \\f rola uma linha (o padrao das falas originais:
    # linha1\\nlinha2\\r...). O GBA usa \\p para pagina nova e \\l para rolar.
    s = s.replace("\\l", "\\f").replace("\\p", "\\r")
    s = s.replace("{PLAYER}", "{STRVAR_1 3, 0, 0}").replace("{KUN}", "")   # {KUN} e vazio no ingles
    s = s.replace("'", "’")                       # o charmap do DS so tem o apostrofo tipografico
    for k, v in (("LEFT", "←"), ("UP", "↑"), ("DOWN", "↓"), ("RIGHT", "→")):   # setas: 011B-011E no charmap do DS
        s = s.replace("{%s_ARROW}" % k, v)
    esc = {"\\n": "\x01", "\\r": "\x02", "\\f": "\x03"}   # para "\\nPROF" nao contar o n como letra
    for k, v in esc.items():
        s = s.replace(k, v)
    for a, b in CASE:
        s = re.sub(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(a), b, s)
    # o resto do que o GBA escreve em maiusculas sao nomes (pessoas, lugares, especies, titulos): caixa mista no DS,
    # menos siglas e enfase de quebra-cabeca; os codigos {...} ficam intactos
    codes = re.findall(r"\{[^}]*\}", s)
    s = re.sub(r"\{[^}]*\}", "\x04", s)
    def word(m):
        w = m.group(0)
        if w in KEEP_CAPS:
            return w
        return w.lower() if w in SMALL and m.start() > 0 else w[0] + w[1:].lower()
    s = re.sub(r"(?<![A-Za-zé])[A-ZÉ][A-ZÉ]+(?![a-zé])", word, s)
    for c in codes:
        s = s.replace("\x04", c, 1)
    for k, v in esc.items():
        s = s.replace(v, k)
    s = re.sub(r"(?<=[a-z])’S\b", "’s", s)             # "Prof. Alex’S" -> "Prof. Alex’s"
    if re.search(r"\{(?!STRVAR_1 3, 0, 0\})", s):
        raise ValueError(f"codigo de texto do GBA sem equivalente: {s}")
    return s


def text_of(label):
    return convert(raw(label))


# --- paginacao para a caixa do DS -----------------------------------------------------------------------------------
# O GBA quebra com \n (linha 2), \l (rola uma linha) e \p (pagina nova). Convertido para o \r do DS, o \l deixava
# linhas soltas, uma por vez, e caixas que pareciam vazias (diretor, 25/11: "textos bugados... sem coesao"). Agora cada
# pagina tem duas linhas inteiras (\n entre elas, \f entre paginas); os paragrafos do GBA (\p) comecam pagina nova.
# Paragrafo de ate 2 linhas que ja cabem (placas, falas curtas) fica com as quebras do GBA.
BOX_W = 215                            # maior linha do HGSS nas caixas de fala (audit_dialogos.py)
FONT = None                            # (larguras, charmap) da fonte do DS: set_font(hg)


def set_font(hg):
    global FONT
    import ndspy.rom
    from audit_dialogos import load_font, load_charmap
    FONT = (load_font(ndspy.rom.NintendoDSRom.fromFile(os.path.join(hg, "rom.nds"))), load_charmap(hg))


def paginar(s):
    if FONT is None:
        raise RuntimeError("paginar() sem fonte: chame set_font(hg)")
    from audit_dialogos import width
    w, cm = FONT
    pages = []
    for par in s.split("\\r"):
        lines = [l for l in re.split(r"\\[nf]", par)]
        if len(lines) <= 2 and all(width(l, cm, w) <= BOX_W for l in lines):
            if par.strip():
                pages.append("\\n".join(lines))
            continue
        words = " ".join(lines).split()

        def wrap(limit):
            out, cur = [], ""
            for word in words:
                cand = (cur + " " + word).strip()
                if not cur or width(cand, cm, w) <= limit:
                    cur = cand
                else:
                    out.append(cur); cur = word
            return out + ([cur] if cur else [])
        out = wrap(BOX_W)
        # equilibra: o mesmo numero de linhas, com largura parecida (sem uma palavra sozinha na ultima linha)
        total = width(" ".join(words), cm, w)
        for limit in range(int(total / len(out)) + 8, BOX_W, 6):
            cand = wrap(limit)
            if len(cand) <= len(out):
                out = cand
                break
        pages += ["\\n".join(out[k:k + 2]) for k in range(0, len(out), 2)]
    return "\\r".join(pages)


if __name__ == "__main__":
    for lab in sys.argv[1:]:
        print(lab, "=>", text_of(lab))
