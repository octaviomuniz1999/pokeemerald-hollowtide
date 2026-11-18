#!/usr/bin/env python3
"""Gera graphics/title_screen/emerald_version.png com o texto HOLLOWTIDE no estilo do original
(letras brancas grossas, contorno escuro de 2 px, leve sombreamento), mantendo a paleta original."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
path = f"{ROOT}/graphics/title_screen/emerald_version.png"
orig = Image.open(path)
pal = orig.getpalette()
W, H = orig.size
font = ImageFont.truetype(sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/inter/Inter-Black.otf", 19)
text = "HOLLOWTIDE"
# texto em alta resolucao sem antialias, ajustado para caber em W-6 px
mask = Image.new("L", (W * 2, H * 2), 0)
d = ImageDraw.Draw(mask)
d.text((0, 0), text, font=font, fill=255)
bb = mask.getbbox()
glyph = mask.crop(bb).point(lambda v: 255 if v > 110 else 0)
scale = min((W - 8) / glyph.width, (H - 8) / glyph.height)
glyph = glyph.resize((max(1, int(glyph.width * scale)), max(1, int(glyph.height * scale))), Image.NEAREST)
gx, gy = (W - glyph.width) // 2, (H - glyph.height) // 2
fill = Image.new("L", (W, H), 0); fill.paste(glyph, (gx, gy))
outline = fill.filter(ImageFilter.MaxFilter(5))  # contorno de 2 px
out = Image.new("P", (W, H), 0); out.putpalette(pal)
po, pf, pl = out.load(), fill.load(), outline.load()
top, bot = gy, gy + glyph.height
for y in range(H):
    for x in range(W):
        if pf[x, y]:
            t = (y - top) / max(1, bot - top)
            po[x, y] = 15 if t < 0.55 else (6 if t < 0.8 else 3)  # branco -> cinza claro embaixo
        elif pl[x, y]:
            po[x, y] = 4
out.save(path)
print("logo gerado", glyph.size, "em", path)
