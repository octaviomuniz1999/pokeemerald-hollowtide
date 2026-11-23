#!/usr/bin/env python3
"""Prova de ponta a ponta da Fase 0 (HeartGold/hg-engine), patches em hollowtide_ds/provas/fase0.

A build de prova muda, so a partir do codigo-fonte:
- texto 546, mensagem 2 (o Wii do quarto, em (8,4)): "Hollowtide: text edit OK!";
- script 0846 (T20R0202): depois da fala do Wii, give_mon Mudkip Lv10 e trainer_battle com o Joey;
- treinador 8 (Joey) em data/Trainers.c: Fennekin Lv5;
- evento 061: a escada do quarto leva a Route 29 (porta da guarita) em vez do andar de baixo;
- encontros da Route 29 em data/Encounters.c: so Sprigatito (Gen 9), taxa 60.
Uso: prova_fase0.py ROM ESTADO_BASE PASTA_CAPTURAS  (ESTADO_BASE de ds_intro.py na mesma ROM: boot limpo).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS

FIGHT = (128, 90)        # tela de baixo
MOVE_2 = (192, 48)       # golpe do canto superior direito (Water Gun no Mudkip Lv10)


def battle(d, outdir, tag, turns=12):
    """Vence a batalha com o golpe 2; para quando o mapa volta a responder."""
    for t in range(turns):
        for _ in range(8):
            d.press("B", 4, 30)
        d.touch(*FIGHT, 6, 60)
        d.touch(*MOVE_2, 6, 60)
        if t == 0:
            d.shot(f"{outdir}/{tag}_turno.png")
        for _ in range(12):
            d.press("B", 4, 40)
        if d.top_is_field():
            return True
    return False


def main(rom, base, outdir):
    os.makedirs(outdir, exist_ok=True)
    d = DS(rom)
    d.load(base); d.wait(30)
    print("inicio", d.where())
    for k in ["RIGHT", "RIGHT", "UP", "UP"]:          # Wii: (8,5) olhando para cima
        d.press(k, 16, 24)
    d.press("A", 4, 90); d.shot(f"{outdir}/1_texto.png")
    for i in range(20):                                 # fala, Mudkip, entrada da batalha
        d.press("A", 4, 45)
    d.wait(240); d.shot(f"{outdir}/2_batalha.png")
    print("batalha com o Joey vencida:", battle(d, outdir, "2"))
    d.wait(120)
    for k in ["DOWN", "LEFT", "LEFT", "LEFT", "LEFT", "UP", "UP", "LEFT", "LEFT"]:   # escada em (3,4)
        d.press(k, 16, 24)
    d.wait(240)
    print("depois da escada", d.where()); d.shot(f"{outdir}/3_warp.png")
    d.save(f"{outdir}/rota29.dst")
    # mato alto a sudeste da guarita (ate (630,396)), depois anda de um lado para o outro
    for k in ["DOWN"] * 5 + ["RIGHT"] * 2 + ["DOWN", "DOWN"] + ["RIGHT"] * 3:
        d.press(k, 16, 24)
    for i in range(120):
        if not d.top_is_field():
            d.wait(400); d.shot(f"{outdir}/4_encontro.png")
            print("encontro selvagem no passo", i, d.where())
            break
        d.press(["LEFT", "RIGHT"][i % 2], 16, 24)
    else:
        print("sem encontro", d.where())


if __name__ == "__main__":
    main(*sys.argv[1:4])
