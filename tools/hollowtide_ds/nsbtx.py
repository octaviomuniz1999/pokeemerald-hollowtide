#!/usr/bin/env python3
"""Conjuntos de textura das construcoes por area (NARC a/0/7/0, um NSBTX por lista de construcoes de a/0/4/3).

Descoberta (25/11/2026): as construcoes do HGSS nao usam as texturas embutidas no proprio modelo (a/0/4/0); usam o
conjunto da lista da area, procurado pelo NOME da textura. Um modelo trazido de outra area ficava branco (ginasio,
galpao, bancos) ou so com as texturas de nome igual ao de Johto (o laboratorio de Pallet, com as janelas h_mado).
merge() acrescenta ao conjunto da area as texturas e paletas que um modelo usa e que o conjunto ainda nao tem.

Formato do bloco TEX0 (conferido byte a byte nos 104 arquivos de a/0/7/0):
  0x0C u16 tamanho dos dados de textura >> 3   0x0E u16 dicionario de texturas   0x14 u32 dados de textura
  0x1C u16 tamanho 4x4 >> 3 (0 aqui)           0x1E u16 dicionario 4x4           0x24/0x28 u32 dados/indices 4x4
  0x30 u32 tamanho das paletas >> 3 (+ flag no bit 31)  0x34 u32 dicionario de paletas  0x38 u32 dados das paletas
  textura: u32 params (offset >> 3 nos 16 bits baixos; largura, altura, formato) + u32 extra
  paleta: u16 offset >> 3 + u16 0
"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import g3d_dict

BPP = {1: 8, 2: 2, 3: 4, 4: 8, 5: 2, 6: 8, 7: 16}


def tex_size(params):
    w, h = 8 << ((params >> 20) & 7), 8 << ((params >> 23) & 7)
    return w * h * BPP[(params >> 26) & 7] // 8


class Tex0:
    def __init__(self, b, t):
        self.head = bytes(b[t:t + 0x3C])
        texsize = struct.unpack_from("<H", b, t + 0x0C)[0] << 3
        texinfo = struct.unpack_from("<H", b, t + 0x0E)[0]
        texdata = struct.unpack_from("<I", b, t + 0x14)[0]
        assert struct.unpack_from("<H", b, t + 0x1C)[0] == 0, "textura 4x4 (nao tratada)"
        palword = struct.unpack_from("<I", b, t + 0x30)[0]
        self.palflag = palword & 0xFFFF0000
        palsize = (palword & 0xFFFF) << 3
        paldict = struct.unpack_from("<I", b, t + 0x34)[0]
        paldata = struct.unpack_from("<I", b, t + 0x38)[0]
        tn, td, _ = g3d_dict.read(b, t + texinfo)
        self.tex_order = g3d_dict.read_order(b, t + texinfo)
        pn, pd, _ = g3d_dict.read(b, t + paldict)
        self.pal_order = g3d_dict.read_order(b, t + paldict)
        self.texraw = bytes(b[t + texdata:t + texdata + texsize])
        self.palraw = bytes(b[t + paldata:t + paldata + palsize])
        self.tex = [(n, struct.unpack("<II", d)) for n, d in zip(tn, td)]
        self.pal = [(n, struct.unpack("<HH", d)) for n, d in zip(pn, pd)]

    def tex_bytes(self, name):
        params, extra = dict(self.tex)[name]
        off = (params & 0xFFFF) << 3
        return params, extra, self.texraw[off:off + tex_size(params)]

    def pal_bytes(self, name):
        offs = sorted({o << 3 for _, (o, _) in self.pal})
        o = dict(self.pal)[name][0] << 3
        nxt = next((x for x in offs if x > o), len(self.palraw))
        return self.palraw[o:nxt]

    def build(self):
        """Bloco TEX0 com o mesmo leiaute do original (cabecalho, dicionario de texturas, de paletas, dados)."""
        texdict = g3d_dict.build([n for n, _ in self.tex], [struct.pack("<II", *v) for _, v in self.tex], 8,
                                 self.tex_order if len(self.tex_order) == len(self.tex) else None)
        paldict = g3d_dict.build([n for n, _ in self.pal], [struct.pack("<HH", *v) for _, v in self.pal], 4,
                                 self.pal_order if len(self.pal_order) == len(self.pal) else None)
        texinfo = 0x3C
        pd_off = texinfo + len(texdict)
        td_off = pd_off + len(paldict)
        pal_off = td_off + len(self.texraw)
        size = pal_off + len(self.palraw)
        h = bytearray(self.head)
        struct.pack_into("<4sI", h, 0, b"TEX0", size)
        struct.pack_into("<HH", h, 0x0C, len(self.texraw) >> 3, texinfo)
        struct.pack_into("<I", h, 0x14, td_off)
        struct.pack_into("<HH", h, 0x1C, 0, texinfo)
        struct.pack_into("<II", h, 0x24, pal_off, pal_off)
        struct.pack_into("<III", h, 0x30, self.palflag | (len(self.palraw) >> 3), pd_off, pal_off)
        return bytes(h) + texdict + paldict + self.texraw + self.palraw


def parse_file(b):
    """NSBTX (BTX0) ou modelo com TEX0 (BMD0): (bytes antes do TEX0, Tex0)."""
    nblocks = struct.unpack_from("<H", b, 14)[0]
    for k in range(nblocks):
        off = struct.unpack_from("<I", b, 16 + 4 * k)[0]
        if b[off:off + 4] == b"TEX0":
            return off, Tex0(b, off)
    raise ValueError("sem bloco TEX0")


def build_btx0(t0):
    blk = t0.build()
    head = struct.pack("<4sHHIHHI", b"BTX0", 0xFEFF, 1, 0x14 + len(blk), 0x10, 1, 0x14)
    return head + blk


def names_of(model):
    _, t = parse_file(model)
    return {n for n, _ in t.tex} | {n for n, _ in t.pal}


def prune(area, keep):
    """Tira do conjunto as texturas e paletas cujo nome nenhum modelo mantido usa (dados reempacotados)."""
    texraw, palraw, tex, pal = bytearray(), bytearray(), [], []
    for n, (params, extra) in area.tex:
        if n not in keep:
            continue
        data = area.tex_bytes(n)[2]
        while len(texraw) % 8:
            texraw.append(0)
        tex.append((n, ((params & ~0xFFFF) | (len(texraw) >> 3), extra)))
        texraw += data
    for n, (o, z) in area.pal:
        if n not in keep:
            continue
        data = area.pal_bytes(n)
        while len(palraw) % 8:
            palraw.append(0)
        pal.append((n, (len(palraw) >> 3, z)))
        palraw += data
    area.tex, area.pal, area.texraw, area.palraw = tex, pal, bytes(texraw), bytes(palraw)
    area.tex_order, area.pal_order = [], []


def merge(btx, models, keep_models=None):
    """btx: bytes do NSBTX da area; models: bytes de modelos (BMD0 com TEX0) a acrescentar; keep_models: se dado, os
    modelos que ficam na lista: as texturas que so os outros usavam saem antes (o conjunto tem teto de memoria: com
    tudo somado a ROM travou ao carregar o mapa). Devolve (novo NSBTX, nomes novos)."""
    _, area = parse_file(btx)
    if keep_models is not None:
        prune(area, set().union(*[names_of(m) for m in keep_models + models]))
    have_t = {n for n, _ in area.tex}
    have_p = {n for n, _ in area.pal}
    novos = []
    texraw, palraw = bytearray(area.texraw), bytearray(area.palraw)
    for mb in models:
        _, m = parse_file(mb)
        for n, _ in m.tex:
            if n in have_t:
                continue
            params, extra, data = m.tex_bytes(n)
            while len(texraw) % 8:
                texraw.append(0)
            params = (params & ~0xFFFF) | (len(texraw) >> 3)
            texraw += data
            area.tex.append((n, (params, extra)))
            have_t.add(n); novos.append(n)
        for n, (o, z) in m.pal:
            if n in have_p:
                continue
            data = m.pal_bytes(n)
            while len(palraw) % 8:
                palraw.append(0)
            area.pal.append((n, (len(palraw) >> 3, z)))
            palraw += data
            have_p.add(n); novos.append(n)
    area.texraw, area.palraw = bytes(texraw), bytes(palraw)
    area.tex_order, area.pal_order = [], []         # nomes novos: ordem de insercao padrao
    return build_btx0(area), novos


if __name__ == "__main__":                            # conferencia: remonta os 104 conjuntos byte a byte
    import ndspy.rom, ndspy.narc
    rom = ndspy.rom.NintendoDSRom.fromFile(sys.argv[1])
    A = ndspy.narc.NARC(rom.getFileByName("a/0/7/0"))
    ok = 0
    for i, f in enumerate(A.files):
        try:
            _, t = parse_file(f)
            ok += build_btx0(t) == bytes(f)
        except Exception as e:
            print(i, "erro", e)
    print(f"{ok}/{len(A.files)} conjuntos remontados byte a byte")
