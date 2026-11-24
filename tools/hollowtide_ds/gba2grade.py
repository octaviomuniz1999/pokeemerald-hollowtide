#!/usr/bin/env python3
"""Conversao fiel dos mapas do GBA (23ap) para a grade do gerador do DS (CP-DS-03B; decisao do diretor: "siga a risca
o que fez no GBA").

Para cada tile do map.bin do GBA:
  - comportamento do metatile (metatile_attributes.bin): mato alto -> e; agua (lagoa, mar, canal) -> ~;
  - tabela explicita METATILES (id do metatile -> letra), feita conferindo a imagem de cada metatile usado
    (folhas de contato geradas por este script com --folha);
  - elevacao (bits 12-15): 3 = chao (altura 1 no DS), 4 = chao elevado (altura 2), 1 = agua, 0 = bloqueado
    (fica com a altura dos vizinhos).
Os mapas sao postos num desenho GLOBAL nas posicoes que fazem as ligacoes do GBA virarem divisas naturais
(CP-DS-03B_PLANO_SETORES.md par. 6) e o desenho e salvo no formato do mapa_grade.py (secao [tamanho] W H).
Construcoes: componentes de tiles B com um warp do GBA na borda de baixo recebem o modelo da area com a porta no
tile do warp (PORTAS); o tile do warp vira D (porta: bloqueado com comportamento 0x69, como no HGSS).
Uso: gba2grade.py SAIDA.txt   |   gba2grade.py --folha MAPA PNG
"""
import collections, json, os, re, struct, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools", "hollowtide_qa"))

# --- tabela metatile -> letra (General = primario, 0x000-0x1FF; secundarios a partir de 0x200) -----------------------
GENERAL = {
    0x001: ".", 0x00F: "e", 0x003: "S", 0x01B: "S", 0x004: "f", 0x288: "f", 0x289: "f",
    0x00E: "T", 0x016: "T", 0x01D: "T", 0x01E: "T", 0x01F: "T", 0x026: "T", 0x027: "T", 0x1D6: "T", 0x1D7: "T",
    0x1DE: "T", 0x1DF: "T", 0x23B: "T",
    0x1CE: ".", 0x1CF: ".", 0x1D0: ".", 0x1D1: ".", 0x1D2: ".", 0x1D8: ".", 0x1D9: ".", 0x1DA: ".", 0x1E0: ".",
    0x1E1: ".", 0x1E2: ".", 0x103: ".", 0x105: ".", 0x10B: ".", 0x10D: ".", 0x113: ".", 0x115: ".",
    0x056: "c", 0x055: "#", 0x057: "#", 0x05D: "#", 0x05E: "#", 0x05F: "#", 0x065: "#", 0x067: "#",
    0x068: "#", 0x06A: "#", 0x070: "#", 0x072: "#", 0x078: "#", 0x079: "#", 0x07A: "#",
    0x0AF: "=",
    0x100: "=", 0x102: "=", 0x109: "=", 0x10A: "=", 0x110: "=", 0x112: "=",
    0x118: "=", 0x119: "=", 0x11A: "=", 0x120: "=", 0x121: "=", 0x122: "=", 0x128: "=", 0x129: "=", 0x12A: "=",
    0x138: "c", 0x13A: "c", 0x140: "c", 0x142: "c", 0x148: "c", 0x149: "c", 0x14A: "c",
    0x248: "=", 0x249: "=", 0x24A: "=", 0x24B: "=", 0x24C: "=", 0x250: "=", 0x251: "=", 0x252: "=", 0x253: "=",
    0x254: "=", 0x258: "=", 0x259: "=", 0x25A: "=", 0x25B: "=", 0x25C: "=",
    0x260: "#", 0x264: "#", 0x268: "#", 0x26C: "#",
    0x265: "=", 0x266: "=", 0x267: "=", 0x26D: "=", 0x26E: "=", 0x26F: "=",
}
for i in range(0x008, 0x023):
    if i not in (0x00D, 0x00E, 0x00F, 0x016, 0x01B, 0x01D, 0x01E, 0x01F):
        GENERAL.setdefault(i, "B")          # casa de telhado vermelho do tileset General
SECONDARY_BUILDINGS = range(0x200, 0x300)   # nos secundarios destes mapas, metatiles bloqueados = construcoes

MAPS = {"Dawnmere": ("LittlerootTown", 0, 0), "Route1": ("Route101", 34, 17), "Harvestvale": ("OldaleTown", 35, 70)}
MARGIN = (2, 2)                             # deslocamento do desenho dentro da area de blocos


def behaviors(tileset_name):
    """Comportamento (byte baixo do atributo) de cada metatile do tileset."""
    import render_map as rm
    raw = open(rm.TILESETS[tileset_name]["attrs"], "rb").read()
    return [struct.unpack_from("<H", raw, 2 * i)[0] & 0xFF for i in range(len(raw) // 2)]


def mb_values():
    names = re.findall(r"^\s*(MB_\w+)", open(os.path.join(REPO, "include/constants/metatile_behaviors.h")).read(), re.M)
    return {n: i for i, n in enumerate(names)}


def load_map(name):
    import render_map as rm
    j = json.load(open(os.path.join(REPO, f"data/maps/{name}/map.json")))
    L = rm._maps()[j["layout"]]
    w, h = L["width"], L["height"]
    data = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
    vals = [struct.unpack_from("<H", data, 2 * i)[0] for i in range(w * h)]
    return j, L, w, h, vals


def convert(name):
    j, L, w, h, vals = load_map(name)
    mb = mb_values()
    prim, sec = behaviors(L["primary_tileset"]), behaviors(L["secondary_tileset"])
    tall = {mb[k] for k in mb if "TALL_GRASS" in k or "LONG_GRASS" in k}
    water = {mb[k] for k in mb if any(t in k for t in ("POND_WATER", "DEEP_WATER", "OCEAN_WATER", "SEMI_DEEP", "INTERIOR_DEEP", "PUDDLE"))}
    tiles, elev, unknown = [], [], collections.Counter()
    for i, v in enumerate(vals):
        mt, col, el = v & 0x3FF, (v >> 10) & 3, v >> 12
        b = prim[mt] if mt < 0x200 else sec[mt - 0x200]
        if b in tall:
            c = "e"
        elif b in water:
            c = "~"
        elif mt in GENERAL:
            c = GENERAL[mt]
        elif mt in SECONDARY_BUILDINGS and col:
            c = "B"
        elif mt in SECONDARY_BUILDINGS:
            c = "="                                      # chao de construcao andavel (calcada, degrau)
        else:
            c = "#" if col else "."
            unknown[mt] += 1
        tiles.append(c); elev.append(el)
    return j, w, h, tiles, elev, unknown


def heights(w, h, elev):
    H = [1 if e in (3, 1, 0) else 2 for e in elev]
    for _ in range(2):                                   # tiles de elevacao 0 (bloqueados) herdam dos vizinhos
        for i, e in enumerate(elev):
            if e == 0:
                x, y = i % w, i // w
                nb = [H[(y + dy) * w + x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if 0 <= x + dx < w and 0 <= y + dy < h and elev[(y + dy) * w + x + dx] != 0]
                if nb:
                    H[i] = max(set(nb), key=nb.count)
    return H


def build_global():
    W = H = 128
    grid = [["T"] * W for _ in range(H)]
    alt = [["1"] * W for _ in range(H)]
    owner = [[None] * W for _ in range(H)]
    report = {}
    for key, (name, ox, oy) in MAPS.items():
        j, w, h, tiles, elev, unknown = convert(name)
        hh = heights(w, h, elev)
        gx, gy = ox + MARGIN[0], oy + MARGIN[1]
        for y in range(h):
            for x in range(w):
                grid[gy + y][gx + x] = tiles[y * w + x]
                alt[gy + y][gx + x] = str(hh[y * w + x])
                owner[gy + y][gx + x] = key
        report[key] = {"gba": name, "origem": (gx, gy), "tam": (w, h), "desconhecidos": dict(unknown),
                       "warps": [(wv["x"] + gx, wv["y"] + gy, wv["dest_map"]) for wv in j.get("warp_events", [])]}
    return grid, alt, owner, report


def folha(name, out):
    import render_map as rm
    from PIL import Image, ImageDraw
    j, L, w, h, vals = load_map(name)
    ts = rm.TilesetPair(L["primary_tileset"], L["secondary_tileset"])
    ids = sorted({v & 0x3FF for v in vals})
    cols, cell = 12, 40
    im = Image.new("RGB", (cols * cell, ((len(ids) + cols - 1) // cols) * (cell + 10)), (40, 40, 40)); d = ImageDraw.Draw(im)
    for k, mt in enumerate(ids):
        x, y = (k % cols) * cell, (k // cols) * (cell + 10)
        im.paste(ts.metatile(mt).resize((32, 32), Image.NEAREST), (x + 4, y + 2))
        d.text((x + 2, y + 34), f"{mt:03x}", fill=(255, 255, 0))
    im.save(out)


if __name__ == "__main__":
    if sys.argv[1] == "--folha":
        folha(sys.argv[2], sys.argv[3]); sys.exit()
    grid, alt, owner, report = build_global()
    for k, r in report.items():
        print(k, r["gba"], "origem", r["origem"], "tam", r["tam"], "metatiles sem tabela:", r["desconhecidos"])
    out = ["; desenho global de Dawnmere + Route 1 + Harvestvale, convertido do GBA por gba2grade.py (nao editar a mao)",
           "[doadores]", "2 0 5 4", "[tamanho]", "128 128", "[tiles]"] + ["".join(r) for r in grid] + ["[alturas]"] + ["".join(r) for r in alt]
    open(sys.argv[1], "w").write("\n".join(out) + "\n")
    json.dump(report, open(sys.argv[1] + ".json", "w"), indent=1)
