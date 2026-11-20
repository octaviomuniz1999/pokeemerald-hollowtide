import sys, struct, collections
GM = ["Piano","BrightPiano","ElecGrand","HonkyTonk","EPiano1","EPiano2","Harpsichord","Clavi","Celesta","Glockenspiel","MusicBox","Vibraphone","Marimba","Xylophone","TubularBells","Dulcimer","DrawbarOrgan","PercOrgan","RockOrgan","ChurchOrgan","ReedOrgan","Accordion","Harmonica","TangoAcc","NylonGtr","SteelGtr","JazzGtr","CleanGtr","MutedGtr","OverdriveGtr","DistGtr","GtrHarmonics","AcBass","FingerBass","PickBass","Fretless","SlapBass1","SlapBass2","SynthBass1","SynthBass2","Violin","Viola","Cello","Contrabass","TremoloStr","PizzStr","Harp","Timpani","Strings1","Strings2","SynStr1","SynStr2","ChoirAahs","VoiceOohs","SynthVoice","OrchHit","Trumpet","Trombone","Tuba","MutedTpt","FrenchHorn","Brass","SynBrass1","SynBrass2","SopSax","AltoSax","TenorSax","BariSax","Oboe","EngHorn","Bassoon","Clarinet","Piccolo","Flute","Recorder","PanFlute","Bottle","Shakuhachi","Whistle","Ocarina","SquareLead","SawLead","Calliope","Chiff","Charang","VoiceLead","FifthsLead","BassLead","Pad1","Pad2","Pad3","Pad4","Pad5","Pad6","Pad7","Pad8","FX1","FX2","FX3","FX4","FX5","FX6","FX7","FX8","Sitar","Banjo","Shamisen","Koto","Kalimba","Bagpipe","Fiddle","Shanai","TinkleBell","Agogo","SteelDrums","Woodblock","Taiko","MelodicTom","SynthDrum","RevCymbal","FretNoise","Breath","Seashore","Bird","Phone","Helicopter","Applause","Gunshot"]
def vlq(d, p):
    v = 0
    while True:
        b = d[p]; p += 1; v = (v << 7) | (b & 0x7F)
        if not b & 0x80: return v, p
d = open(sys.argv[1], 'rb').read()
fmt, ntr, div = struct.unpack('>HHH', d[8:14]); print("format", fmt, "tracks", ntr, "division", div)
p = 14
for t in range(ntr):
    assert d[p:p+4] == b'MTrk'; ln = struct.unpack('>I', d[p+4:p+8])[0]; q = p+8; end = q+ln; p = end
    tick = 0; run = 0; notes = collections.Counter(); progs = []; meta = []; ccs = collections.Counter(); rng = {}
    while q < end:
        dt, q = vlq(d, q); tick += dt
        st = d[q]
        if st == 0xFF:
            ty = d[q+1]; l, q2 = vlq(d, q+2); data = d[q2:q2+l]; q = q2+l
            if ty in (1,3,6): meta.append((tick, ty, data.decode('latin1')))
            elif ty == 0x51: meta.append((tick, 'tempo', round(60e6/int.from_bytes(data,'big'),1)))
            elif ty == 0x58: meta.append((tick, 'timesig', tuple(data)))
            continue
        if st in (0xF0, 0xF7):
            l, q2 = vlq(d, q+1); q = q2+l; continue
        if st & 0x80: run = st; q += 1
        ch = run & 15; ty = run >> 4
        if ty in (0xC, 0xD): a = d[q]; q += 1
        else: a, b = d[q], d[q+1]; q += 2
        if ty == 9 and b > 0:
            notes[ch] += 1; lo, hi = rng.get(ch, (127, 0)); rng[ch] = (min(lo, a), max(hi, a))
        elif ty == 0xC: progs.append((tick, ch, a, GM[a]))
        elif ty == 0xB: ccs[(ch, a)] += 1
    print(f"track {t}: end tick {tick}, notes {dict(notes)}, range {rng}")
    for m in meta[:12]: print("   meta", m)
    for pr in progs[:10]: print("   prog", pr)
    if ccs: print("   cc", dict(sorted(ccs.items())[:20]))
