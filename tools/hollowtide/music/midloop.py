"""Corta um MIDI no fim do loop e marca '[' e ']' (meta de texto) para o mid2agb. Uso: midloop.py IN OUT BAR_INI BAR_FIM"""
import sys, struct
def vlq(d, p):
    v = 0
    while True:
        b = d[p]; p += 1; v = (v << 7) | (b & 0x7F)
        if not b & 0x80: return v, p
def wvlq(v):
    out = [v & 0x7F]; v >>= 7
    while v: out.append(0x80 | (v & 0x7F)); v >>= 7
    return bytes(reversed(out))
src, dst, b0, b1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
d = open(src, 'rb').read(); fmt, ntr, div = struct.unpack('>HHH', d[8:14]); bar = div*4
L0, L1 = b0*bar, b1*bar
p = 14; tracks = []
for t in range(ntr):
    ln = struct.unpack('>I', d[p+4:p+8])[0]; q = p+8; end = q+ln; p = end; tick = 0; run = 0; ev = []; on = {}
    while q < end:
        dt, q = vlq(d, q); tick += dt; st = d[q]
        if st == 0xFF:
            ty = d[q+1]; l, q2 = vlq(d, q+2); raw = d[q:q2+l]; q = q2+l
            if ty == 0x2F: continue
            if tick <= L1: ev.append((tick, 0, raw))
            continue
        if st in (0xF0, 0xF7):
            l, q2 = vlq(d, q+1); q = q2+l; continue
        if st & 0x80: run = st; q += 1
        ty = run >> 4; ch = run & 15
        n = 1 if ty in (0xC, 0xD) else 2
        data = d[q:q+n]; q += n
        msg = bytes([run]) + data
        if ty == 9 and data[1] > 0:
            if tick >= L1: continue
            on[(ch, data[0])] = on.get((ch, data[0]), 0) + 1
        elif ty == 8 or (ty == 9 and data[1] == 0):
            k = (ch, data[0])
            if not on.get(k): continue
            on[k] -= 1
            if tick > L1: tick_off = L1; ev.append((L1, 1, bytes([0x80 | ch, data[0], 0]))); continue
        elif tick >= L1: continue
        ev.append((tick, 1, msg))
    for (ch, note), c in on.items():
        for _ in range(c): ev.append((L1, 1, bytes([0x80 | ch, note, 0])))
    if t == 0:
        ev.append((L0, -1, b'\xff\x06\x01['))
        ev.append((L1, 2, b'\xff\x06\x01]'))
    ev.sort(key=lambda e: (e[0], e[1]))
    out = bytearray(); last = 0
    for tk, _, raw in ev:
        out += wvlq(tk - last) + raw; last = tk
    out += wvlq(max(0, L1 - last)) + b'\xff\x2f\x00'
    tracks.append(bytes(out))
o = bytearray(b'MThd' + struct.pack('>IHHH', 6, 1, ntr, div))
for tr in tracks: o += b'MTrk' + struct.pack('>I', len(tr)) + tr
open(dst, 'wb').write(o)
print("ok", dst, "loop", L0, L1)
