#!/usr/bin/env python3
"""Alturas do terreno do HeartGold (BDHC, dentro do land_data) — leitura, regravacao e geracao.

Formato conferido nos blocos da ROM:
  "BDHC", 6 u16: pontos, normais, distancias, placas, faixas, lista de acesso
  pontos:     (fx32 x, fx32 z)            — cantos das placas, a partir do centro do bloco (1 tile = 16 unidades)
  normais:    (fx32 nx, ny, nz)
  distancias: fx32 d                      — plano da placa: nx*x + ny*y + nz*z + d = 0  ->  y = -(nx*x + nz*z + d) / ny
  placas:     (u16 ponto_min, u16 ponto_max, u16 normal, u16 distancia) — retangulo alinhado aos eixos
  faixas:     (fx32 z_limite, u16 quantidade, u16 inicio) — placas que tocam a faixa de z ate z_limite (ordem crescente)
  acesso:     u16 indices de placa, referidos pelas faixas
Gerador: placas em tiles do bloco (0..32), planas ou rampas em z ou x (altura em tiles).
"""
import math, struct

FX = 4096
TILE = 16 * FX                       # 1 tile em fx32 de mundo


class Bdhc:
    def __init__(self, data=None):
        self.points, self.normals, self.dists, self.plates, self.strips, self.access = [], [], [], [], [], []
        if data is None:
            return
        assert data[:4] == b"BDHC"
        n = struct.unpack_from("<6H", data, 4)
        p = 16
        def take(fmt, count):
            nonlocal p
            sz = struct.calcsize(fmt)
            out = [struct.unpack_from(fmt, data, p + sz * i) for i in range(count)]
            p += sz * count
            return out
        self.points = take("<ii", n[0]); self.normals = take("<iii", n[1]); self.dists = [d[0] for d in take("<i", n[2])]
        self.plates = take("<4H", n[3]); self.strips = take("<iHH", n[4]); self.access = [a[0] for a in take("<H", n[5])]
        assert p == len(data), "tamanho de BDHC inesperado"

    def pack(self):
        out = b"BDHC" + struct.pack("<6H", len(self.points), len(self.normals), len(self.dists), len(self.plates),
                                    len(self.strips), len(self.access))
        out += b"".join(struct.pack("<ii", *p) for p in self.points)
        out += b"".join(struct.pack("<iii", *n) for n in self.normals)
        out += b"".join(struct.pack("<i", d) for d in self.dists)
        out += b"".join(struct.pack("<4H", *p) for p in self.plates)
        out += b"".join(struct.pack("<iHH", *s) for s in self.strips)
        out += b"".join(struct.pack("<H", a) for a in self.access)
        return out

    def height(self, tx, tz):
        """Altura (tiles) no ponto (tx, tz) em tiles do bloco, pela primeira placa que o contem."""
        x, z = (tx - 16) * TILE, (tz - 16) * TILE
        for a, b, ni, di in self.plates:
            (x0, z0), (x1, z1) = self.points[a], self.points[b]
            if x0 <= x <= x1 and z0 <= z <= z1:
                nx, ny, nz = self.normals[ni]
                return -((nx * x + nz * z) / FX + self.dists[di]) / (ny / FX) / TILE
        return None


def build(plates):
    """plates: [(tx0, tz0, tx1, tz1, h0, h1, eixo)] em tiles; eixo 'z' ou 'x' para rampa (h0 no lado menor), None plano."""
    b = Bdhc()
    pidx, nidx, didx = {}, {}, {}
    def idx(table, lst, key):
        if key not in table:
            table[key] = len(lst); lst.append(key)
        return table[key]
    rects = []
    for tx0, tz0, tx1, tz1, h0, h1, axis in plates:
        x0, z0, x1, z1 = (int(round((t - 16) * TILE)) for t in (tx0, tz0, tx1, tz1))
        if axis is None or h0 == h1:
            n = (0, FX, 0)
            d = int(round(-h0 * TILE))
        else:
            span = (tz1 - tz0) if axis == "z" else (tx1 - tx0)
            k = (h1 - h0) / span                          # tiles de altura por tile
            ny, nh = 1 / math.sqrt(1 + k * k), -k / math.sqrt(1 + k * k)
            n = (0, round(ny * FX), round(nh * FX)) if axis == "z" else (round(nh * FX), round(ny * FX), 0)
            c0 = z0 if axis == "z" else x0
            # ny*y + nh*c + d = 0 no ponto (c0, h0)
            d = -round((n[1] * h0 * TILE + (n[2] if axis == "z" else n[0]) * c0) / FX)
        a = idx(pidx, b.points, (x0, z0)); c = idx(pidx, b.points, (x1, z1))
        b.plates.append((a, c, idx(nidx, b.normals, n), idx(didx, b.dists, d)))
        rects.append((z0, z1))
    # faixas: limites de z de todas as placas, em ordem; cada faixa lista as placas que a cruzam
    bounds = sorted({z for r in rects for z in r})
    lo = bounds[0]
    for z in bounds[1:]:
        members = [i for i, (z0, z1) in enumerate(rects) if z0 < z and z1 > lo]
        b.strips.append((z, len(members), len(b.access)))
        b.access += members
        lo = z
    return b
