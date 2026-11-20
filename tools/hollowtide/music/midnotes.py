import sys, struct, collections
def vlq(d, p):
    v = 0
    while True:
        b = d[p]; p += 1; v = (v << 7) | (b & 0x7F)
        if not b & 0x80: return v, p
def notes(path):
    d = open(path, 'rb').read(); fmt, ntr, div = struct.unpack('>HHH', d[8:14]); p = 14; out = []
    for t in range(ntr):
        ln = struct.unpack('>I', d[p+4:p+8])[0]; q = p+8; end = q+ln; p = end; tick = 0; run = 0; on = {}
        while q < end:
            dt, q = vlq(d, q); tick += dt; st = d[q]
            if st == 0xFF:
                l, q2 = vlq(d, q+2); q = q2+l; continue
            if st in (0xF0, 0xF7):
                l, q2 = vlq(d, q+1); q = q2+l; continue
            if st & 0x80: run = st; q += 1
            ch = run & 15; ty = run >> 4
            if ty in (0xC, 0xD): q += 1; continue
            a, b = d[q], d[q+1]; q += 2
            if ty == 9 and b > 0: on[(ch, a)] = (tick, b)
            elif ty == 8 or (ty == 9 and b == 0):
                if (ch, a) in on: s, v = on.pop((ch, a)); out.append((s, tick, ch, a, v))
    return div, sorted(out)
if __name__ == '__main__':
    div, ns = notes(sys.argv[1])
    ev = []
    for s, e, ch, a, v in ns: ev += [(s, 1, ch), (e, -1, ch)]
    ev.sort(key=lambda x: (x[0], x[1]))
    cur = collections.Counter(); mx = collections.Counter(); tot = 0; mt = 0; hist = collections.Counter(); last = 0
    for t, dlt, ch in ev:
        hist[tot] += t - last; last = t
        cur[ch] += dlt; tot += dlt; mx[ch] = max(mx[ch], cur[ch]); mt = max(mt, tot)
    print("max poly per ch", dict(mx), "max total", mt)
    T = sum(hist.values()); print("time share by total poly", {k: round(v/T*100,1) for k, v in sorted(hist.items())})
    bar = div*4; S = set((s, ch, a) for s, e, ch, a, v in ns); end = max(e for s, e, *_ in ns)
    best = []
    for k in range(4, int(end/bar)):
        sh = k*bar; m = sum(1 for (s, ch, a) in S if (s+sh, ch, a) in S); best.append((m, k))
    best.sort(reverse=True); print("end bars", end/bar, "best shifts (matches, bars)", best[:6], "total", len(S))
