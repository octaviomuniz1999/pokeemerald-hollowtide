#!/usr/bin/env python3
"""Modelos 3D de mapa do HeartGold (.nsbmd dentro do land_data) — leitura e regravacao das formas (geometria).

Estrutura conferida nos blocos da ROM (um modelo, um no; materiais = texturas do conjunto da area, a/0/4/4):
  BMD0 (cabecalho) > MDL0 (dicionario de modelos) > modelo: tamanho, ofs dos comandos de render (SBC), dos materiais,
  das formas e das matrizes de envelope; info (escala de posicao, contagens, caixa); nos; SBC; materiais; formas.
  Formas: dicionario + cabecalhos de 16 bytes (tag, tamanho, flags, ofs da lista de desenho, tamanho) e as listas de
  desenho (comandos GX empacotados) no fim do modelo. Os comandos de render desenham "MAT m, SHP s" em pares.
O que este modulo faz: decodifica as listas de desenho em poligonos (vertices, UV, normal/cor) e regrava o modelo com
listas novas, mantendo cabecalho, nos, materiais, texturas e comandos de render byte a byte (so tamanhos, offsets,
contagens e caixa mudam). Ida e volta (decodificar -> codificar) confere byte a byte.
"""
import struct

CMD_PARAMS = {0x00: 0, 0x10: 1, 0x11: 0, 0x12: 1, 0x13: 1, 0x14: 1, 0x15: 0, 0x16: 16, 0x17: 12, 0x18: 16, 0x19: 12,
              0x1A: 9, 0x1B: 3, 0x1C: 3, 0x20: 1, 0x21: 1, 0x22: 1, 0x23: 2, 0x24: 1, 0x25: 1, 0x26: 1, 0x27: 1,
              0x28: 1, 0x29: 1, 0x2A: 1, 0x2B: 1, 0x30: 1, 0x31: 1, 0x32: 1, 0x33: 1, 0x34: 32, 0x40: 1, 0x41: 0,
              0x50: 1, 0x60: 1, 0x70: 3, 0x71: 2, 0x72: 1}


def s(v, bits):
    v &= (1 << bits) - 1
    return v - (1 << bits) if v & (1 << (bits - 1)) else v


def read_dict(b, base):
    rev, n, size = struct.unpack_from("<BBH", b, base)
    ofs_entry = struct.unpack_from("<H", b, base + 6)[0]
    e = base + ofs_entry
    unit, esize = struct.unpack_from("<HH", b, e)
    data = [bytes(b[e + 4 + unit * i:e + 4 + unit * (i + 1)]) for i in range(n)]
    names = [bytes(b[e + esize + 16 * i:e + esize + 16 * (i + 1)]).rstrip(b"\0").decode() for i in range(n)]
    return names, data, e


def decode_dl(dl):
    """Lista de desenho -> [(cmd, [params])] na ordem."""
    out, p = [], 0
    while p + 4 <= len(dl):
        ids = list(dl[p:p + 4]); p += 4
        for c in ids:
            n = CMD_PARAMS[c]
            params = list(struct.unpack_from(f"<{n}I", dl, p)); p += 4 * n
            out.append((c, params))
    return out


def encode_dl(cmds):
    """[(cmd, params)] -> bytes, em pacotes de 4 comandos (NOP no fim), como o conversor da Nintendo."""
    out = bytearray()
    for i in range(0, len(cmds), 4):
        grp = cmds[i:i + 4]
        ids = [c for c, _ in grp] + [0] * (4 - len(grp))
        out += bytes(ids)
        for _, params in grp:
            out += struct.pack(f"<{len(params)}I", *params)
    return bytes(out)


def polygons(cmds):
    """Vertices de cada BEGIN..END: [{'prim': tipo, 'v': [(x,y,z,u,v,cor_ou_normal)]}] em unidades do modelo (fx 12 bits)."""
    polys, cur, pos, uv, extra = [], None, [0, 0, 0], (0, 0), None
    for c, p in cmds:
        if c == 0x40:
            cur = {"prim": p[0] & 3, "v": []}
        elif c == 0x41:
            if cur:
                polys.append(cur)
            cur = None
        elif c == 0x22:
            uv = (s(p[0], 16), s(p[0] >> 16, 16))
        elif c in (0x20, 0x21):
            extra = (c, p[0])
        elif c in (0x23, 0x24, 0x25, 0x26, 0x27, 0x28):
            if c == 0x23:
                pos = [s(p[0], 16), s(p[0] >> 16, 16), s(p[1], 16)]
            elif c == 0x24:
                pos = [s(p[0], 10) << 6, s(p[0] >> 10, 10) << 6, s(p[0] >> 20, 10) << 6]
            elif c == 0x25:
                pos = [s(p[0], 16), s(p[0] >> 16, 16), pos[2]]
            elif c == 0x26:
                pos = [s(p[0], 16), pos[1], s(p[0] >> 16, 16)]
            elif c == 0x27:
                pos = [pos[0], s(p[0], 16), s(p[0] >> 16, 16)]
            else:
                pos = [pos[0] + s(p[0], 10), pos[1] + s(p[0] >> 10, 10), pos[2] + s(p[0] >> 20, 10)]
            if cur is not None:
                cur["v"].append((pos[0], pos[1], pos[2], uv[0], uv[1], extra))
    return polys


class Model:
    def __init__(self, data):
        self.b = bytearray(data)
        assert self.b[:4] == b"BMD0"
        nb = struct.unpack_from("<H", self.b, 14)[0]
        assert nb == 1, "modelo com texturas embutidas (nao e modelo de mapa)"
        self.mdl0 = struct.unpack_from("<I", self.b, 16)[0]
        names, data_, _ = read_dict(self.b, self.mdl0 + 8)
        assert len(names) == 1
        self.name = names[0]
        self.m = self.mdl0 + struct.unpack_from("<I", data_[0])[0]
        self.size, self.ofs_sbc, self.ofs_mat, self.ofs_shp, self.ofs_evp = struct.unpack_from("<5I", self.b, self.m)
        assert self.ofs_evp == self.size, "modelo com matrizes de envelope"
        info = self.m + 20
        self.n_mat, self.n_shp = self.b[info + 4], self.b[info + 5]
        self.pos_scale = struct.unpack_from("<i", self.b, info + 8)[0] / 4096
        self.box = struct.unpack_from("<6h", self.b, info + 24)
        mb = self.m + self.ofs_mat
        self.materials, _, _ = read_dict(self.b, mb + 4)
        sb = self.m + self.ofs_shp
        self.shape_names, sdata, _ = read_dict(self.b, sb)
        self.shape_hdr = [sb + struct.unpack_from("<I", d)[0] for d in sdata]
        self.dls = []
        for h in self.shape_hdr:
            tag, size, flag, ofs, n = struct.unpack_from("<HHII I".replace(" ", ""), self.b, h)
            self.dls.append(bytes(self.b[h + ofs:h + ofs + n]))
        self.dl_start = self.shape_hdr[0] + struct.unpack_from("<I", self.b, self.shape_hdr[0] + 8)[0]
        assert self.dl_start + sum(len(x) for x in self.dls) == self.m + self.size, "listas de desenho fora do fim do modelo"
        sbc = self.b[self.m + self.ofs_sbc:self.m + self.ofs_mat]
        self.draws = []                                # (material, forma) na ordem dos comandos de render
        i = 0
        while i < len(sbc):
            op = sbc[i] & 0x1F
            if op == 0x04:
                mat = sbc[i + 1]; i += 2
                if sbc[i] & 0x1F == 0x05:
                    self.draws.append((mat, sbc[i + 1])); i += 2
                continue
            i += {0x00: 1, 0x01: 1, 0x02: 3, 0x03: 2, 0x05: 2, 0x06: 4, 0x0B: 1}.get(op, 1)

    def shape_material(self):
        return {s_: self.materials[m] for m, s_ in self.draws}

    def pack(self, new_dls=None, box=None, counts=None):
        """Modelo com as listas de desenho trocadas (mesma quantidade de formas)."""
        dls = new_dls if new_dls is not None else self.dls
        assert len(dls) == len(self.dls)
        head = bytearray(self.b[:self.dl_start])
        pos = self.dl_start
        for h, dl in zip(self.shape_hdr, dls):
            struct.pack_into("<II", head, h + 8, pos - h, len(dl))
            pos += len(dl)
        size = pos - self.m
        struct.pack_into("<I", head, self.m, size)
        struct.pack_into("<I", head, self.m + 16, size)          # ofs das matrizes de envelope = fim (nao ha)
        info = self.m + 20
        if counts:
            struct.pack_into("<4H", head, info + 16, *counts)
        if box:
            struct.pack_into("<6h", head, info + 24, *box)
        out = bytes(head) + b"".join(dls)
        out = bytearray(out)
        struct.pack_into("<I", out, self.mdl0 + 4, len(out) - self.mdl0)   # tamanho do bloco MDL0
        struct.pack_into("<I", out, 8, len(out))                            # tamanho do arquivo
        return bytes(out)


# --- secao de materiais (para juntar materiais de varios blocos doadores da mesma area) -------------------------------
def read_materials(b, mb):
    """Bloco de materiais em b[mb:]: (materiais [(nome, dados)], texturas [(nome, [indices], flag)], paletas idem).
    Layout conferido nos 676 modelos: u16 ofs_tex, u16 ofs_pal, dicionario de materiais (u32 ofs dos dados),
    dicionario de texturas e de paletas (u16 ofs da lista, u8 quantidade, u8 flag), listas de indices (u8),
    alinhamento a 4, dados dos materiais (tamanho no 2o u16 de cada um)."""
    import g3d_dict as g
    ot, op = struct.unpack_from("<HH", b, mb)
    mnames, mdata, _ = g.read(b, mb + 4)
    mats = []
    for n, d in zip(mnames, mdata):
        o = mb + struct.unpack_from("<I", d)[0]
        size = struct.unpack_from("<H", b, o + 2)[0]
        mats.append((n, bytes(b[o:o + size])))
    def binds(base):
        names, data, _ = g.read(b, mb + base)
        out = []
        for n, d in zip(names, data):
            ofs, cnt, flag = struct.unpack_from("<HBB", d)
            out.append((n, list(b[mb + ofs:mb + ofs + cnt]), flag))
        return out
    return mats, binds(ot), binds(op)


def material_orders(b, mb):
    """Ordens de insercao dos 3 dicionarios do bloco de materiais (para remontar byte a byte)."""
    import g3d_dict as g
    ot, op = struct.unpack_from("<HH", b, mb)
    return g.read_order(b, mb + 4), g.read_order(b, mb + ot), g.read_order(b, mb + op)


def build_materials(mats, tex, pal, orders=(None, None, None)):
    """Bloco de materiais (inverso de read_materials). orders: ordens de insercao dos dicionarios (None = padrao)."""
    import g3d_dict as g
    md_size = len(g.build([n for n, _ in mats], [b"\0" * 4] * len(mats), 4))
    td_size = len(g.build([n for n, _, _ in tex], [b"\0" * 4] * len(tex), 4))
    pd_size = len(g.build([n for n, _, _ in pal], [b"\0" * 4] * len(pal), 4))
    ot = 4 + md_size
    op = ot + td_size
    lists_at = op + pd_size
    lists, tdata, pdata = b"", [], []
    for group, out in ((tex, tdata), (pal, pdata)):
        for n, idx, flag in group:
            out.append(struct.pack("<HBB", lists_at + len(lists), len(idx), flag))
            lists += bytes(idx)
    mat_at = lists_at + len(lists)
    pad = (-mat_at) % 4
    mat_at += pad
    mdata, pos = [], mat_at
    for n, d in mats:
        mdata.append(struct.pack("<I", pos)); pos += len(d)
    return (struct.pack("<HH", ot, op) + g.build([n for n, _ in mats], mdata, 4, orders[0])
            + g.build([n for n, _, _ in tex], tdata, 4, orders[1]) + g.build([n for n, _, _ in pal], pdata, 4, orders[2])
            + lists + b"\0" * pad + b"".join(d for _, d in mats))


SBC_PRE = bytes.fromhex("26000000000200010b")       # NODEDESC 0, NODE 0 visivel, POSSCALE  (669 dos 676 modelos)
SBC_SUF = bytes.fromhex("2b0100")                   # POSSCALE inverso, RET


def model_parts(md):
    """Partes de um modelo de mapa: dict com cabecalho/info/nos (opacos), comandos de render (prefixo, pares,
    sufixo), materiais, formas [(nome, flag, lista de desenho)] e as ordens de insercao dos dicionarios."""
    import g3d_dict as g
    m = Model(md)
    sbc = bytes(md[m.m + m.ofs_sbc:m.m + m.ofs_mat])
    k = sbc.find(b"\x04")
    i = k
    while i + 3 < len(sbc) and sbc[i] == 4 and sbc[i + 2] == 5:
        i += 4
    draws = [(sbc[j + 1], sbc[j + 3]) for j in range(k, i, 4)]
    mb = m.m + m.ofs_mat
    sb = m.m + m.ofs_shp
    names, data, _ = g.read(md, sb)
    shapes = []
    for n, d, dl in zip(names, data, m.dls):
        h = sb + struct.unpack_from("<I", d)[0]
        shapes.append((n, struct.unpack_from("<I", md, h + 4)[0], dl))
    return {"head": bytes(md[:m.m]), "info": bytes(md[m.m + 20:m.m + m.ofs_sbc]), "sbc": (sbc[:k], draws, sbc[i:]),
            "materials": read_materials(md, mb), "mat_orders": material_orders(md, mb), "shapes": shapes,
            "shape_order": g.read_order(md, sb), "mdl0": m.mdl0, "m": m.m}


def build_model(p, counts=None):
    """Modelo a partir das partes (inverso de model_parts); numero de materiais/formas livre."""
    import g3d_dict as g
    pre, draws, suf = p["sbc"]
    sbc = pre + b"".join(bytes([4, a, 5, b]) for a, b in draws) + suf
    sbc += b"\0" * ((-(20 + len(p["info"]) + len(sbc))) % 4)
    mats, tex, pal = p["materials"]
    matb = build_materials(mats, tex, pal, p.get("mat_orders", (None, None, None)))
    shapes = p["shapes"]
    dsize = len(g.build([n for n, _, _ in shapes], [b"\0" * 4] * len(shapes), 4))
    hdr_at = dsize
    dl_at = hdr_at + 16 * len(shapes)
    sdata, hdrs, pos = [], b"", dl_at
    for k, (n, flag, dl) in enumerate(shapes):
        h = hdr_at + 16 * k
        sdata.append(struct.pack("<I", h))
        hdrs += struct.pack("<HHIII", 0, 16, flag, pos - h, len(dl))
        pos += len(dl)
    shpb = g.build([n for n, _, _ in shapes], sdata, 4, p.get("shape_order")) + hdrs + b"".join(dl for _, _, dl in shapes)
    info = bytearray(p["info"])
    info[4], info[5] = len(mats), len(shapes)
    if counts:
        struct.pack_into("<4H", info, 16, *counts)
    ofs_sbc = 20 + len(info)
    ofs_mat = ofs_sbc + len(sbc)
    ofs_shp = ofs_mat + len(matb)
    size = ofs_shp + len(shpb)
    model = struct.pack("<5I", size, ofs_sbc, ofs_mat, ofs_shp, size) + bytes(info) + sbc + matb + shpb
    out = bytearray(p["head"] + model)
    struct.pack_into("<I", out, p["mdl0"] + 4, len(out) - p["mdl0"])
    struct.pack_into("<I", out, 8, len(out))
    return bytes(out)


def compose(base, donors, layers):
    """Modelo novo com materiais de varios blocos doadores da mesma area.
    base: bytes do modelo que da cabecalho, info e no; donors: lista de bytes de modelos (procurados em ordem);
    layers: [(nome_do_material, lista_de_desenho)] na ordem de desenho. Cada material leva os dados, a ligacao de
    textura e paleta e o flag da forma do doador onde foi achado."""
    p = model_parts(base)
    dparts = [model_parts(d) for d in donors]
    mats, texmap, palmap, shapes = [], {}, {}, []
    for k, (name, dl) in enumerate(layers):
        # prefere o doador que DESENHA o material (alguns blocos listam materiais da area sem usa-los)
        found = None
        for dp in dparts:
            names = [n for n, _ in dp["materials"][0]]
            if name in names:
                i = names.index(name)
                drawn = any(m_ == i for m_, _ in dp["sbc"][1])
                if drawn or found is None:
                    found = (dp, names, i, drawn)
                if drawn:
                    break
        if found is None:
            raise KeyError(f"material {name} em nenhum doador")
        dp, names, i, drawn = found
        mats.append((name, dp["materials"][0][i][1]))
        for src, dst in ((dp["materials"][1], texmap), (dp["materials"][2], palmap)):
            for tn, idx, flag in src:
                if i in idx:
                    dst.setdefault(tn, ([], flag))[0].append(k)
        flag = dp["shapes"][next(s for m_, s in dp["sbc"][1] if m_ == i)][1] if drawn else 5   # 5 = normal + textura
        shapes.append((f"polygon{k}", flag, dl))
    p["materials"] = (mats, [(n, v[0], v[1]) for n, v in texmap.items()], [(n, v[0], v[1]) for n, v in palmap.items()])
    p["mat_orders"] = (None, None, None)
    p["shapes"] = shapes
    p["shape_order"] = None
    p["sbc"] = (SBC_PRE, [(k, k) for k in range(len(layers))], SBC_SUF)
    return build_model(p)
