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
Construcoes (CONSTRUCOES): cada planta do GBA recebe um modelo do HGSS com a porta no tile do warp (ou o mais perto que
o modelo deixa); o tile da porta vira D (bloqueado com comportamento 0x69, como no HGSS).
Uso: gba2grade.py SAIDA.txt   |   gba2grade.py --folha MAPA PNG
"""
import collections, json, os, re, struct, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools", "hollowtide_qa"))

# --- tabela metatile -> letra (General = primario, 0x000-0x1FF; secundarios a partir de 0x200) -----------------------
GENERAL = {
    0x001: ".", 0x00F: "e", 0x003: "S", 0x01B: "S", 0x004: "f", 0x288: "f", 0x289: "f",
    0x00E: "T", 0x016: "T", 0x017: "T", 0x01D: "T", 0x01E: "T", 0x01F: "T", 0x026: "T", 0x027: "T", 0x1D6: "T", 0x1D7: "T",
    0x1DE: "T", 0x1DF: "T", 0x23B: "T",
    0x1CE: ".", 0x1CF: ".", 0x1D0: ".", 0x1D1: ".", 0x1D2: ".", 0x1D8: ".", 0x1D9: ".", 0x1DA: ".", 0x1E0: ".",
    0x1E1: ".", 0x1E2: ".", 0x103: ".", 0x105: ".", 0x10B: ".", 0x10D: ".", 0x113: ".", 0x115: ".",
    0x056: "c", 0x055: "#", 0x057: "#", 0x05D: "#", 0x05E: "=", 0x05F: "#", 0x065: "#", 0x067: "#",   # 05E = tabuado da ponte
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
GENERAL.update({0x1DC: "T", 0x1DD: "T",                            # metade de baixo das arvores grandes (Route 2)
                0x070: "#", 0x072: "#", 0x074: "#", 0x078: "#", 0x079: "#", 0x07A: "#", 0x07C: "#",
                0x087: "v", 0x089: "#", 0x091: "#", 0x0D5: "v", 0x0D6: "v"})       # muro do cercado e ressaltos
GENERAL.update({0x071: "#", 0x073: "#", 0x075: "#", 0x07B: "#", 0x0E2: "#",          # montanha e pedra (Breezeport)
                0x175: "#", 0x176: "#", 0x17A: "#", 0x17B: "#", 0x17C: "#", 0x17D: "#", 0x17E: "#",
                0x182: "#", 0x184: "#", 0x194: "#",                        # rochas na agua
                0x1D3: "T", 0x1DB: "T"})                                   # arbustos
GENERAL.update({0x1D4: "T", 0x1D5: "T", 0x1E4: "T", 0x1E5: "T", 0x1E6: "T", 0x1E7: "T",      # arvores grandes (Harvestvale)
                0x10C: "=", 0x104: "=", 0x114: "=", 0x124: "="})   # terra arada da plantacao e areias
PRIMARY_BUILDINGS = [range(0x028, 0x064), range(0x1AA, 0x1CE)]   # Mart/PC e ginasio do tileset General
for i in range(0x008, 0x023):
    if i not in (0x00D, 0x00E, 0x00F, 0x016, 0x017, 0x01B, 0x01D, 0x01E, 0x01F):
        GENERAL.setdefault(i, "B")          # casa de telhado vermelho do tileset General
# Metatiles a partir de 0x200 sao do tileset SECUNDARIO, que muda de mapa para mapa: as entradas >= 0x200 da tabela
# acima foram conferidas nos tilesets da Route 1 (EverGrande) e de Dawnmere (Petalburg) e so valem para eles.
SECONDARY_TABLE_TILESETS = {"gTileset_EverGrande", "gTileset_Petalburg"}
SECONDARY_BUILDINGS = range(0x200, 0x400)   # nos secundarios destes mapas, metatiles bloqueados = construcoes

# --- construcoes: modelo do HGSS sobre a planta do GBA -----------------------------------------------------------------
# Modelos com textura propria (NARC a/0/4/0); caixa (x0, x1, z0) em tiles a partir do ponto do objeto; porta = modelo da
# porta e deslocamento (dx, dz, dy) medidos nos mapas do HGSS; dtile = tile D (porta de verdade) a partir do objeto.
MODELOS = {
    0x13A: dict(nome="mst_okl (laboratorio de Pallet)", x0=-3.375, x1=3.875, z0=-2.125, porta=(0x137, 0.625, 1.219, 0.16), dtile=(0, 1.5)),
    0x139: dict(nome="mst_rdh (casa de Pallet)", x0=-2.875, x1=3.125, z0=-2.375, porta=(0x136, -0.375, 1.219, 0.16), dtile=(-1, 1.5)),
    0x14: dict(nome="wk_hhouse (casa de New Bark)", x0=-2.875, x1=3.125, z0=-2.375, porta=(0x18, -0.375, 1.089, 0.0), dtile=(-1, 1.5)),
    0x16: dict(nome="wk_h01 (casa de New Bark)", x0=-2.25, x1=2.5, z0=-1.625, porta=(0x19, 0.126, 0.739, 0.07), dtile=(-0.5, 0.875)),
    0x25: dict(nome="yo_h01 (casa de Cherrygrove)", x0=-2.188, x1=2.5, z0=-1.625, porta=(0x32, 0.125, 0.731, 0.04), dtile=(-0.5, 1.0)),
    0x26: dict(nome="yo_h02 (casa de Cherrygrove)", x0=-2.188, x1=2.5, z0=-1.625, porta=(0x32, 0.12, 0.719, 0.04), dtile=(-0.5, 1.0)),
    0x29: dict(nome="kn_h01 (casa de Kanto)", x0=-2.188, x1=2.5, z0=-1.625, porta=(0x18, 0.113, 0.763, 0.062), dtile=(-0.5, 1.0)),
    0x27: dict(nome="fs (Poke Mart)", x0=-2.125, x1=3.633, z0=-1.812, porta=(0x0F, -0.558, 0.757, 0.0), dtile=(-0.5, 1.0)),
    0x28: dict(nome="pc (Centro Pokemon)", x0=-2.625, x1=3.0, z0=-2.0, porta=(0x0F, 0.0, 1.608, 0.0), dtile=(0, 1.5)),
    0xF5: dict(nome="ta_gym (ginasio de Celadon, tipo Planta como o do Nevard)", x0=-3.479, x1=3.865, z0=-2.587,
               porta=(0x10, 0.0, 1.405, 0.0), dtile=(0, 1.5)),
}
# Por mapa: retangulo da construcao no GBA (x0, y0, x1, y1, inclusivo, coordenadas do mapa do GBA), modelo, tile da porta
# no DS (= warp do GBA, salvo quando o modelo nao deixa) e se a porta e de verdade (warp) ou decorativa; "ajustes" sao
# tiles trocados para acompanhar a porta (letra, altura). A colisao e a uniao da planta do GBA com a do modelo.
CONSTRUCOES = {
    "Dawnmere": [
        dict(rect=(10, 4, 16, 8), modelo=0x13A, porta=(13, 8), warp=True, altura=2,
             nota="laboratorio do Prof. Alex: o unico laboratorio do HGSS que cabe na planta do GBA (colunas 10-16) tem a "
                  "porta no centro, 1 tile a oeste do warp do GBA (14,8); a escada vai junto (14,9 -> 13,9)",
             ajustes=[((13, 9), "=", "r"), ((14, 9), "=", "2"), ((15, 9), "S", "2")]),
        dict(rect=(19, 12, 23, 16), modelo=0x14, porta=(20, 16), warp=True, altura=1, nota="casa do warp MAYS_HOUSE"),
        dict(rect=(1, 7, 4, 9), modelo=0x16, porta=(2, 9), warp=True, altura=1, nota="casa do warp BRENDANS_HOUSE"),
        dict(rect=(6, 19, 10, 23), modelo=0x25, porta=(8, 23), warp=False, altura=1, nota="casa sem porta no GBA"),
        dict(rect=(18, 19, 22, 23), modelo=0x26, porta=(20, 23), warp=False, altura=1, nota="casa sem porta no GBA"),
    ],
    "Harvestvale": [
        dict(rect=(2, 17, 7, 21), modelo=0xF5, porta=(5, 21), warp=True, altura=1, nota="ginasio do Nevard (warp do GBA)"),
        dict(rect=(11, 18, 14, 21), modelo=0x28, porta=(12, 21), warp=True, altura=1, nota="Centro Pokemon"),
        dict(rect=(22, 29, 25, 31), modelo=0x27, porta=(23, 31), warp=True, altura=1, nota="Poke Mart"),
        dict(rect=(15, 9, 20, 11), modelo=0x14, porta=(17, 11), warp=True, altura=1, nota="casa (OLDALE_TOWN_HOUSE1)"),
        dict(rect=(20, 15, 23, 18), modelo=0x29, porta=(21, 18), warp=True, altura=1, nota="casa (OLDALE_TOWN_HOUSE2)"),
    ],
    "Route2": [
        dict(rect=(13, 33, 16, 36), modelo=0x25, porta=(14, 36), warp=False, altura=1,
             nota="casa de porta trancada (Palm280_DoorLocked na porta)"),
    ],
    "Route1": [
        dict(rect=(4, 17, 10, 20), modelo=0x14, porta=(5, 20), warp=False, altura=1,
             nota="casa da horta (porta decorativa no GBA, sem warp); a casa de Pallet (mst_rdh), de telhado vermelho, "
                  "ficou sem textura: a lista de construcoes da area so tem VRAM para mais dois modelos"),
    ],
}
# lista de construcoes 0 (area 2: os headers de Dawnmere, Route 1 e Harvestvale), pelo land.json: entram o laboratorio
# de Pallet, o ginasio de Celadon e as portas deles; sai o wk_labo de New Bark (sem uso com Dawnmere original). A VRAM
# das texturas da lista tem limite: 53 248 bytes funcionaram, ~55 600 nao (o ultimo modelo ficou sem textura).
MODELOS_NOVOS_NA_AREA = [0x13A, 0x137, 0xF5, 0x10]
MODELOS_FORA_DA_AREA = [0x15]


def construcoes(key, gx, gy, grid, alt):
    """Carimba as construcoes do mapa no desenho global; devolve as linhas de [objetos] e o relatorio."""
    objs, rel = [], []
    for c in CONSTRUCOES.get(key, []):
        M = MODELOS[c["modelo"]]
        px, pz = c["porta"]
        ox = px + 0.5 - M["dtile"][0]                    # ponto do objeto (coordenadas de borda de tile, mapa do GBA)
        oz = pz + 0.5 - M["dtile"][1]
        x0, y0, x1, y1 = c["rect"]
        cells = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
        cells |= {(x, y) for x in range(int(ox + M["x0"]) - 1, int(ox + M["x1"]) + 2)
                  for y in range(int(oz + M["z0"]) - 1, pz + 1)
                  if ox + M["x0"] + 0.25 <= x + 0.5 <= ox + M["x1"] - 0.25 and y + 0.5 >= oz + M["z0"] - 0.25}
        h = str(c["altura"])
        for x, y in cells:
            grid[gy + y][gx + x] = "B"; alt[gy + y][gx + x] = h
        grid[gy + pz][gx + px] = "D" if c["warp"] else "B"
        for (x, y), ch, a in c.get("ajustes", []):
            grid[gy + y][gx + x] = ch; alt[gy + y][gx + x] = a
        X, Z = gx + ox - 0.5, gy + oz - 0.5             # [objetos] usa indice de tile (o Land.obj soma 0,5)
        dm, ddx, ddz, ddy = M["porta"]
        objs.append(f"{c['modelo']} {X:g} {Z:g} 0")
        objs.append(f"{dm} {X + ddx:g} {Z + ddz:g} {ddy:g}")
        rel.append({"modelo": M["nome"], "porta_ds": (gx + px, gy + pz), "warp": c["warp"], "nota": c["nota"]})
    return objs, rel


MAPS = {"Dawnmere": ("LittlerootTown", 0, 0), "Route1": ("Route101", 34, 17), "Harvestvale": ("OldaleTown", 35, 70),
        "Route2": ("PalmRoute02", 35, 107)}        # ligacoes do GBA: Route 2 abaixo de Harvestvale (deslocamento 0)
ESCADAS = {0x0AF}                           # escada do GBA: rampa no DS (entre os vizinhos norte e sul)
# Deslocamento do desenho dentro da area de blocos. Cada celula de 32x32 tem UM header (zona de eventos, encontros,
# musica): com (30, 21), quase toda celula fica com um mapa so: Dawnmere na coluna de blocos 1, a Route 1 nas colunas
# 2-3 (linhas 1-2), Harvestvale na linha 3, a Route 2 nas linhas 4-5. Sobram as 5 primeiras linhas de Harvestvale
# (arvores e caminho) numa celula da Route 1: a chegada e o fazendeiro descem 3 linhas (eventos_gba.py).
MARGIN = (30, 21)


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
    jump_s = mb["MB_JUMP_SOUTH"]
    shallow = {mb[k] for k in mb if k in ("MB_SHALLOW_WATER",)}
    water = {mb[k] for k in mb if any(t in k for t in ("POND_WATER", "DEEP_WATER", "OCEAN_WATER", "SEMI_DEEP", "INTERIOR_DEEP", "PUDDLE"))}
    tiles, elev, unknown = [], [], collections.Counter()
    for i, v in enumerate(vals):
        mt, col, el = v & 0x3FF, (v >> 10) & 3, v >> 12
        b = prim[mt] if mt < 0x200 else sec[mt - 0x200]
        if b in tall:
            c = "e"
        elif b == jump_s:
            c = "v"                                      # ressalto: pulo para o sul
        elif b in shallow:
            c = "="                                      # poca rasa (andavel): chao de terra no DS
        elif b in water:
            c = "~"
        elif mt in GENERAL and (mt < 0x200 or L["secondary_tileset"] in SECONDARY_TABLE_TILESETS):
            c = GENERAL[mt]
        elif any(mt in r for r in PRIMARY_BUILDINGS):
            c = "B" if col else "="                      # parede/telhado de construcao; calcada na frente
        elif mt in SECONDARY_BUILDINGS and col:
            c = "B"
        elif mt in SECONDARY_BUILDINGS:
            c = "="                                      # chao de construcao andavel (calcada, degrau)
        else:
            c = "#" if col else "."
            unknown[mt] += 1
        if c in "#c" and not col:
            c = "="                                      # fidelidade: sem colisao no GBA, o tile e andavel no DS
        tiles.append(c); elev.append(el)
    return j, w, h, tiles, elev, unknown


def heights(w, h, elev):
    H = [1 if e in (3, 1, 0) else 2 for e in elev]          # 4 e 5 (chao elevado) = altura 2
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
    W, H = 128, 192
    grid = [["T"] * W for _ in range(H)]
    alt = [["1"] * W for _ in range(H)]
    owner = [[None] * W for _ in range(H)]
    report, objetos = {}, []
    for key, (name, ox, oy) in MAPS.items():
        j, w, h, tiles, elev, unknown = convert(name)
        hh = heights(w, h, elev)
        _, _, _, _, vals = load_map(name)
        for i, v in enumerate(vals):                     # escadas: rampa (so as que nao foram ajustadas a mao)
            if v & 0x3FF in ESCADAS and key != "Dawnmere":
                hh[i] = "r"
        gx, gy = ox + MARGIN[0], oy + MARGIN[1]
        for y in range(h):
            for x in range(w):
                grid[gy + y][gx + x] = tiles[y * w + x]
                alt[gy + y][gx + x] = str(hh[y * w + x])
                owner[gy + y][gx + x] = key
        objs, rel = construcoes(key, gx, gy, grid, alt)
        objetos += objs
        for b in j.get("bg_events", []):                 # placas do GBA: modelo de placa do HGSS (board_b) no tile
            if b.get("type") == "sign":                  # as tres celulas sao da area 2 (board_b na lista 0)
                objetos.append(f"30 {gx + b['x']} {gy + b['y']} 0")
        report[key] = {"gba": name, "origem": (gx, gy), "tam": (w, h), "desconhecidos": dict(unknown),
                       "warps": [(wv["x"] + gx, wv["y"] + gy, wv["dest_map"]) for wv in j.get("warp_events", [])],
                       "construcoes": rel}
    return grid, alt, owner, report, objetos


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
    grid, alt, owner, report, objetos = build_global()
    for k, r in report.items():
        print(k, r["gba"], "origem", r["origem"], "tam", r["tam"], "metatiles sem tabela:", r["desconhecidos"])
    out = ["; desenho global de Dawnmere + Route 1 + Harvestvale, convertido do GBA por gba2grade.py (nao editar a mao)",
           "[doadores]", "2 0 5 4", "[tamanho]", f"{len(grid[0])} {len(grid)}", "[tiles]"] + ["".join(r) for r in grid] + ["[alturas]"] + ["".join(r) for r in alt] + ["[objetos]"] + objetos
    open(sys.argv[1], "w").write("\n".join(out) + "\n")
    json.dump(report, open(sys.argv[1] + ".json", "w"), indent=1)
