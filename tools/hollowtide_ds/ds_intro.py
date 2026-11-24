#!/usr/bin/env python3
"""Leva um jogo novo do HeartGold (hg-engine) ate o quarto do jogador e salva o estado base do QA de DS.
Sequencia levantada em 23/11/2026: tutorial de toque (botao "Touch" em 210,165 da tela de baixo, alternando com A),
pergunta "Do you understand everything so far?" -> YES (200,70), menu de topicos -> NO INFO NEEDED (128,151), depois A
ate o campo (nome "A" pelo teclado de toque, genero padrao). Uso: ds_intro.py ROM SAIDA.dst
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS


def topic_menu(d):
    """Os tres botoes azul-esverdeados (CONTROL INFO, ADVENTURE INFO, NO INFO NEEDED) na tela de baixo."""
    im = d.emu.screenshot()
    return all(im.getpixel((70, y))[:3] == (24, 184, 192) for y in (232, 287, 343))


def name_screen(d):
    """Teclado do nome: botao OK lilas (215,263), teclas rosa (150,330), borda salmao (20,300)."""
    im = d.emu.screenshot()
    return (im.getpixel((215, 263))[:3] == (200, 144, 248) and im.getpixel((150, 330))[:3] == (248, 200, 184)
            and im.getpixel((20, 300))[:3] == (240, 128, 112))


def new_game(d):
    """Do console ligado ate o jogador aparecer no quarto (jogo novo). Devolve (mapa, x, y) ou None."""
    d.wait(60 * 20)
    for i in range(400):
        if i % 3:
            d.press("A", 4, 40)
        else:
            d.touch(210, 165, 6, 40)
    d.touch(200, 70, 6, 60)
    # um laco so: o tempo de cada fala varia entre execucoes (relogio do DS), entao em vez de uma sequencia fixa
    # responde ao que estiver na tela ate o jogador aparecer no mapa
    menu_seen = False
    for i in range(900):
        if d.where():
            break
        if topic_menu(d):                      # menu de topicos: toca NO INFO NEEDED enquanto ele estiver na tela
            d.touch(128, 151, 10, 90)
            menu_seen = True
            continue
        if name_screen(d):                     # nome: tecla A (36,101) e OK (215,71) na tela de baixo
            d.wait(60)                         # a tela entra com fade; toque antes disso se perde
            d.touch(36, 101, 10, 40)
            d.touch(215, 71, 10, 90)
            continue
        d.press("A", 4, 40)
        if not menu_seen and i % 10 == 9:
            d.touch(200, 70, 6, 40)            # YES da pergunta, se ela voltar
    d.press("B", 4, 30)
    return d.where()


def main(rom, out):
    d = DS(rom)
    w = new_game(d)
    if not w:
        d.shot(out + ".falhou.png")
        raise SystemExit("nao chegou ao campo (tela em %s.falhou.png)" % out)
    d.save(out)
    print("estado base salvo:", out, "mapa/x/y =", w)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
