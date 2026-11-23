#!/usr/bin/env python3
"""Leva um jogo novo do HeartGold (hg-engine) ate o quarto do jogador e salva o estado base do QA de DS.
Sequencia levantada em 23/11/2026: tutorial de toque (botao "Touch" em 210,165 da tela de baixo, alternando com A),
pergunta "Do you understand everything so far?" -> YES (200,70), menu de topicos -> NO INFO NEEDED (128,151), depois A
ate o campo (nome e genero padrao). Uso: ds_intro.py ROM SAIDA.dst
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS


def main(rom, out):
    d = DS(rom)
    d.wait(60 * 20)
    for i in range(400):
        if i % 3:
            d.press("A", 4, 40)
        else:
            d.touch(210, 165, 6, 40)
    d.touch(200, 70, 6, 60)
    for i in range(300):
        d.press("A", 4, 40)
        if i % 10 == 9:
            d.touch(200, 70, 6, 40)
        if d.emu.screenshot().getpixel((128, 343))[2] > 180:      # botoes azuis do menu de topicos
            break
    d.touch(128, 151, 6, 90)
    for _ in range(250):
        d.press("A", 4, 40)
        if d.where():
            break
    d.press("B", 4, 30)
    w = d.where()
    if not w:
        raise SystemExit("nao chegou ao campo")
    d.save(out)
    print("estado base salvo:", out, "mapa/x/y =", w)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
