#!/usr/bin/env python3
"""Folha de referencia de metatiles: tileset_sheet.py PRIMARIO SECUNDARIO saida.png [inicio fim]
Desenha cada metatile com seu numero, para escolher pecas ao montar mapas."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from render_map import TilesetPair
from PIL import Image, ImageDraw
p, s, out = sys.argv[1:4]
a, b = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1024)
ts = TilesetPair(p, s)
ids = [i for i in range(a, b) if i < len(ts.metatiles) and any(ts.metatiles[i])]
cols = 16; S = 3
im = Image.new("RGB", (cols * 16 * S, ((len(ids) + cols - 1) // cols) * (16 * S + 10)), (40, 40, 40))
d = ImageDraw.Draw(im)
for k, mt in enumerate(ids):
    x, y = (k % cols) * 16 * S, (k // cols) * (16 * S + 10)
    im.paste(ts.metatile(mt).resize((16 * S, 16 * S), Image.NEAREST), (x, y + 10))
    d.text((x + 2, y), str(mt), fill=(255, 255, 0))
im.save(out); print(out, len(ids), "metatiles")
