#!/usr/bin/env python3
"""Prova de ponta a ponta da Fase 0 (HeartGold/hg-engine) no quarto do jogador (mapa 64, T20R0202).

A build de prova (hg-engine com BUILD_DUMPED_SCR_SEQ e BUILD_DUMPED_EVENTDATA) muda, so a partir do codigo-fonte:
- texto 546, mensagem 2 (o Wii em (8,4)): "Hollowtide: text edit OK!";
- script 0846 (T20R0202): depois da fala do Wii, give_mon Mudkip Lv10 e trainer_battle com o Joey;
- treinador 8 (Joey) em data/Trainers.c: Fennekin Lv5 e fala de entrada "Hollowtide: trainer edit OK!";
- evento 061: a escada do quarto leva ao MAP_T20R0401 (mapa 66) em vez do andar de baixo.
Uso: prova_fase0.py ROM ESTADO_BASE PASTA_CAPTURAS  (ESTADO_BASE de ds_intro.py na mesma ROM: boot limpo).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS


def main(rom, base, outdir):
    os.makedirs(outdir, exist_ok=True)
    d = DS(rom)
    d.load(base); d.wait(30)
    print("inicio", d.where())
    # Wii: fica em (8,5) olhando para cima
    for k in ["RIGHT", "RIGHT", "UP", "UP"]:
        d.press(k, 16, 24)
    print("diante do Wii", d.where())
    d.press("A", 4, 90); d.shot(f"{outdir}/1_texto.png")
    for i in range(40):                      # fala, Mudkip, entrada da batalha
        d.press("A", 4, 45)
        if i in (3, 12, 25, 39):
            d.shot(f"{outdir}/2_seq_{i:02d}.png")
    d.save(f"{outdir}/batalha.dst")
    print("depois da sequencia", d.where())


if __name__ == "__main__":
    main(*sys.argv[1:4])
