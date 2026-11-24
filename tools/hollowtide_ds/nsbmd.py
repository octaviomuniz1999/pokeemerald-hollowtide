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
