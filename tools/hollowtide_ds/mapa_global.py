#!/usr/bin/env python3
"""Desenho global de varios blocos (CP-DS-03B): gera a malha do desenho inteiro com mapa_grade.py, reparte por bloco
de 32x32 e monta tudo na matriz do mundo.

- A malha e gerada uma vez sobre o desenho inteiro (margens, bordas de caminho e cercas enxergam os vizinhos atraves
  das divisas de bloco); cada quad vai para o bloco que contem o seu centro e e transladado para as coordenadas
  locais. O chao nunca atravessa divisa (mapa_grade.rects).
- Colisao, alturas (BDHC) e objetos sao recortados por bloco.
- Os blocos sao ACRESCENTADOS ao NARC a/0/6/5 (os 676 originais ficam intactos) e as celulas da matriz recebem o
  bloco novo e o header do mapa que ocupa a maior parte de cada bloco (retangulos do relatorio do gba2grade.py).
Entrada no land.json: {"global": "lunia_cap1.txt", "matriz": 0, "celula": [21, 13], "base": 0,
                       "headers": {"Dawnmere": 60, "Route1": 33, "Harvestvale": 67}, "padrao": 60,
                       "modelos_area": {"lista": 0, "acrescentar": [314, 311], "remover": [21]}}
  (modelos_area: construcoes de outras areas acrescentadas a lista a/0/4/3 que a area dos headers usa; formato da lista:
   u16 quantidade + u16 modelos)
  "doadores_por_header": {"77": [58, 59, ...]}: celulas cujo header e de outra area (Breezeport = Olivine, area 7) usam
  doadores dessa area; "substituir": {"flower02": "flower01", "fence_b": null} para materiais que ela nao tem.
"""
import json, os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
import mapa_grade as mg
from land_data import Land
from nsbmd import compose
from matrix import Matrix


SEAM = 1 / 16
SEAM_MATS = {"grass01", "road01", "egrass", "sea_un", "sea_on", "flower01", "flower02", "flower03"}


def subgrid(g, bx, by):
    return {"tiles": [r[bx * 32:bx * 32 + 32] for r in g["tiles"][by * 32:by * 32 + 32]],
            "alturas": [r[bx * 32:bx * 32 + 32] for r in g["alturas"][by * 32:by * 32 + 32]],
            "doadores": g["doadores"], "tamanho": (32, 32),
            "objetos": [(m, x - bx * 32, z - by * 32, dy) for m, x, z, dy in g["objetos"]
                        if bx * 32 <= x < bx * 32 + 32 and by * 32 <= z < by * 32 + 32]}


def gerar_blocos(path, base_block, blocos, doadores_bloco=None, substituir=None, barreira=False):
    """{(bx, by): bytes do bloco} para todo o desenho.
    doadores_bloco: {(bx, by): [blocos doadores]} para blocos de outra area (os materiais ligam pelo nome as texturas
    da area do header da celula); substituir: {material: outro} para o que a area nao tem (None = nao desenha)."""
    g = mg.load(path)
    mesh, H, ramps = mg.build_mesh(g)
    W, HH = g["tamanho"]
    nbx, nby = W // 32, HH // 32
    parts = {}
    for mat, quads in mesh.quads.items():
        for verts, n in quads:
            cx = sum(v[0] for v in verts) / 4; cz = sum(v[2] for v in verts) / 4
            bx, by = min(nbx - 1, max(0, int(cx // 32))), min(nby - 1, max(0, int(cz // 32)))
            local = [(x - bx * 32, y, z - by * 32, u, v) for x, y, z, u, v in verts]
            if mat in SEAM_MATS:                         # chao na divisa avanca 1/16 de tile: fecha a fresta preta entre
                ext = lambda a: a - SEAM if a == 0 else (a + SEAM if a == 32 else a)    # blocos vizinhos (DeSmuME)
                local = [(ext(x), y, ext(z), u, v) for x, y, z, u, v in local]
            parts.setdefault((bx, by), mg.Mesh()).quad(mat, local, n)
    donor_bytes = lambda ids: [Land(blocos[d]).rest[:Land(blocos[d]).sizes[2]] for d in ids]
    donors = donor_bytes(g["doadores"])
    base = Land(blocos[base_block])
    # alturas no desenho inteiro (uma rampa pode terminar na divisa de bloco, com o vizinho no bloco seguinte);
    # cada bloco recebe o seu recorte e as rampas cortadas nas divisas, com a altura interpolada no corte
    Hg, rg = H, ramps
    out = {}
    for by in range(nby):
        for bx in range(nbx):
            sub = subgrid(g, bx, by)
            mg.set_size(sub)
            Hs = [r[bx * 32:bx * 32 + 32] for r in Hg[by * 32:by * 32 + 32]]
            rs = []
            for x, z0, z1, hn, hs in rg:
                if not bx * 32 <= x < bx * 32 + 32:
                    continue
                c0, c1 = max(z0, by * 32), min(z1, by * 32 + 32)
                if c0 >= c1:
                    continue
                at = lambda zz: hn + (hs - hn) * (zz - z0) / (z1 - z0)
                rs.append((x - bx * 32, c0 - by * 32, c1 - by * 32, at(c0), at(c1)))
            m = parts.get((bx, by), mg.Mesh())
            dn = donors
            sub_mats = {}
            if doadores_bloco and (bx, by) in doadores_bloco:
                dn = donor_bytes(doadores_bloco[(bx, by)])
                sub_mats = substituir or {}
            mm = mg.Mesh()
            for name, quads in m.quads.items():           # materiais que a area da celula nao tem
                to = sub_mats.get(name, name)
                if to is None:
                    continue
                for verts, n in quads:
                    mm.quad(to, verts, n)
            layers = [(name, mm.dl(name)) for name in mg.ORDER if name in mm.quads]
            ld = Land(blocos[base_block])
            model = compose(base.rest[:base.sizes[2]], dn, layers)
            hb = mg.build_bdhc(sub, Hs, rs).pack()
            ld.perms = mg.perms(sub)
            if barreira:                                 # borda externa do desenho: ninguem anda/surfa para fora
                for t in range(32):
                    for (x, z) in ((t, 0), (t, 31), (0, t), (31, t)):
                        edge = (z == 0 and by == 0) or (z == 31 and by == nby - 1) or (x == 0 and bx == 0) or \
                               (x == 31 and bx == nbx - 1)
                        if edge:
                            ld.perms[z * 32 + x] |= 0x8000
            ld.objs = [Land.obj(mdl, x, z, Hs[int(z)][int(x)] + dy) for mdl, x, z, dy in sub["objetos"]]
            ld.sizes[2], ld.sizes[3] = len(model), len(hb)
            ld.rest = model + hb
            out[(bx, by)] = ld.pack()
    mg.set_size(g)
    return out, (nbx, nby)


def owners(report_path, nbx, nby, headers, padrao):
    """Header de cada bloco: o mapa cujo retangulo cobre mais tiles do bloco."""
    rep = json.load(open(report_path))
    res = {}
    for by in range(nby):
        for bx in range(nbx):
            best, area = padrao, 0
            for key, r in rep.items():
                (gx, gy), (w, h) = r["origem"], r["tam"]
                ix = max(0, min(gx + w, bx * 32 + 32) - max(gx, bx * 32))
                iy = max(0, min(gy + h, by * 32 + 32) - max(gy, by * 32))
                if ix * iy > area and key in headers:
                    best, area = headers[key], ix * iy
            res[(bx, by)] = best
    return res


def apply_global(rom, narc, entry, base_dir):
    path = os.path.join(base_dir, entry["global"])
    g0 = mg.load(path)
    nbx0, nby0 = g0["tamanho"][0] // 32, g0["tamanho"][1] // 32
    hdr = owners(path + ".json", nbx0, nby0, entry["headers"], entry.get("padrao", 0))
    for k, h in entry.get("headers_celula", {}).items():  # celula (bx,by do desenho) com header escolhido a mao
        bx, by = map(int, k.split(","))
        hdr[(bx, by)] = h
    por_header = {int(k): v for k, v in entry.get("doadores_por_header", {}).items()}   # blocos de outra area
    doadores_bloco = {c: por_header[h] for c, h in hdr.items() if h in por_header}
    blocks, (nbx, nby) = gerar_blocos(path, entry.get("base", 0), [bytes(f) for f in narc.files], doadores_bloco,
                                      entry.get("substituir"), entry.get("barreira", False))
    import ndspy.narc
    mid = rom.filenames.idOf("a/0/4/1")
    mnarc = ndspy.narc.NARC(rom.files[mid])
    mt = Matrix(mnarc.files[entry["matriz"]])
    cx0, cy0 = entry["celula"]
    ids = {}
    for by in range(nby):
        for bx in range(nbx):
            ids[(bx, by)] = len(narc.files)
            narc.files.append(blocks[(bx, by)])
            mt.set(cx0 + bx, cy0 + by, land=ids[(bx, by)], header=hdr[(bx, by)],
                   altura=0 if mt.alts is not None else None)    # altitude da celula: o desenho ja traz as alturas;
                                                                 # um resto da celula antiga vira degrau na divisa
    mnarc.files[entry["matriz"]] = mt.pack()
    if "modelos_area" in entry:                          # modelos de construcao de outras areas: entram na lista da area
        lst, novos = entry["modelos_area"]["lista"], entry["modelos_area"]["acrescentar"]
        fora = set(entry["modelos_area"].get("remover", []))
        aid = rom.filenames.idOf("a/0/4/3")
        anarc = ndspy.narc.NARC(rom.files[aid])
        f = anarc.files[lst]
        cur = list(struct.unpack_from("<%dH" % (len(f) // 2), f))
        ids_m = [m for m in cur[1:1 + cur[0]] if m not in fora] + [m for m in novos if m not in cur[1:1 + cur[0]]]
        anarc.files[lst] = struct.pack("<%dH" % (len(ids_m) + 1), len(ids_m), *ids_m)
        rom.files[aid] = anarc.save()
        print(f"lista de construcoes {lst}: {cur[0]} -> {len(ids_m)} modelos")
    rom.files[mid] = mnarc.save()
    print(f"desenho global {entry['global']}: {nbx}x{nby} blocos novos ({min(ids.values())}-{max(ids.values())}) "
          f"nas celulas ({cx0},{cy0})-({cx0 + nbx - 1},{cy0 + nby - 1}); headers {sorted(set(hdr.values()))}")
    return nbx * nby
