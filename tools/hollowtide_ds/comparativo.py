#!/usr/bin/env python3
"""Capturas comparativas ANTES/DEPOIS a partir de duas varreduras do qa_visual.py (mesmas coordenadas).

Uso: comparativo.py PASTA_ANTES PASTA_DEPOIS SAIDA MAPA:X_Y:legenda [...]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def main(antes, depois, saida, pares):
    os.makedirs(saida, exist_ok=True)
    f = ImageFont.truetype(FONTE, 16) if os.path.exists(FONTE) else ImageFont.load_default()
    fb = ImageFont.truetype(FONTE.replace("Sans.", "Sans-Bold."), 15) if os.path.exists(FONTE) else f
    for k, par in enumerate(pares):
        m, n, txt = par.split(":", 2)
        a = Image.open(f"{antes}/{m}/{n}.png").resize((512, 384), Image.NEAREST)
        b = Image.open(f"{depois}/{m}/{n}.png").resize((512, 384), Image.NEAREST)
        im = Image.new("RGB", (1040, 448), (24, 24, 28))
        d = ImageDraw.Draw(im)
        d.text((8, 8), f"{k + 1}. {m} (GBA {n.replace('_', ',')}): {txt}", fill=(255, 230, 120), font=f)
        d.text((8, 36), "ANTES", fill=(255, 130, 130), font=fb)
        d.text((536, 36), "DEPOIS", fill=(130, 255, 150), font=fb)
        im.paste(a, (0, 60)); im.paste(b, (528, 60))
        p = f"{saida}/{k + 1:02d}_{m}_{n}.png"
        im.save(p); print(p)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
