#!/usr/bin/env python3
"""QA do Cap. 1 no DS: do quarto ate a Route 1, com a ROM do conteudo (build.sh sem pastas de prova).

Passos (cada um imprime mapa/posicao e salva uma captura em PASTA):
1. quarto -> escada -> a mae e o Medalhao de Atlas (avanca com B);
2. sai de casa (Dawnmere): sem a cena da Lyra; tenta a saida oeste sem Pokemon -> fala do GBA e um passo de volta;
3. laboratorio: Prof. Alex -> escolha (bola da frente) -> Pokedex, Poke Balls, Potions, missao;
4. volta e sai pelo oeste -> Route 1 (mapa 33).
Uso: qa_cap1.py ROM ESTADO_BASE PASTA  (ESTADO_BASE de ds_intro.py na mesma ROM)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS


def walk(d, keys, stop_map=None):
    for k in keys:
        d.press(k, 16, 24)
        w = d.where()
        if stop_map is not None and w and w[0] == stop_map:
            break
    return d.where()


def starter_screen(d):
    """Tela das Poke Balls (choose_starter): fundo cinza em cima e no meio."""
    im = d.emu.screenshot()
    return im.getpixel((5, 5))[:3] == (64, 64, 72) and im.getpixel((128, 250))[:3] == (88, 88, 96)


def advance(d, n=40, key="B"):
    for _ in range(n):
        d.press(key, 4, 40)


def main(rom, base, out):
    os.makedirs(out, exist_ok=True)
    ok = {}
    d = DS(rom)
    d.load(base); d.wait(30)
    walk(d, ["UP", "UP", "LEFT", "LEFT", "LEFT", "UP", "LEFT", "LEFT"]); d.wait(200)
    d.shot(f"{out}/1_mae.png"); advance(d, 45); d.wait(60)
    ok["casa"] = d.where()
    walk(d, ["DOWN"] * 8); d.wait(200)
    advance(d, 10)
    ok["dawnmere"] = d.where(); d.shot(f"{out}/2_dawnmere.png")
    # saida oeste sem Pokemon: linha y=398 ate x=676
    w = walk(d, ["DOWN"] + ["LEFT"] * 20, stop_map=33)
    d.wait(60); d.shot(f"{out}/3_saida_sem_pokemon.png")
    advance(d, 8); d.wait(60)
    ok["barrado"] = d.where()
    # laboratorio: porta em (684,393)
    x = d.where()[1]
    walk(d, ["RIGHT"] * (684 - x) + ["UP"] * 6, stop_map=61); d.wait(200)
    ok["lab"] = d.where()
    walk(d, ["UP"] * 8 + ["RIGHT"] * 2 + ["UP"])
    d.press("A", 4, 60)
    for _ in range(60):                                  # falas ate a tela das bolas
        if starter_screen(d):
            break
        d.press("A", 4, 50)
    for _ in range(6):                                   # sequencia conferida: espera, A (mostra a bola da frente),
        if not starter_screen(d):                        # toque na bola da frente (pergunta) e de novo (escolhe)
            break
        d.wait(300); d.press("A", 4, 120)
        d.touch(128, 110, 8, 150); d.touch(128, 110, 8, 150)
        for _ in range(10):
            d.wait(30)
    for _ in range(40):
        d.wait(30)
    advance(d, 60); d.shot(f"{out}/4_lab.png")   # so B: o A fala de novo com o professor
    advance(d, 10)
    ok["inicial"] = d.where()
    walk(d, ["LEFT", "LEFT"] + ["DOWN"] * 9, stop_map=60); d.wait(200)
    walk(d, ["DOWN"] * 4 + ["LEFT"] * 30, stop_map=33); d.wait(200)   # linha y=398 (a vizinha fica em 683,399)
    ok["route1"] = d.where(); d.shot(f"{out}/5_route1.png")
    for k, v in ok.items():
        print(f"{k:10} {v}")
    print("RESULTADO:", "ok" if ok["barrado"] and ok["barrado"][0] == 60 and ok["route1"] and ok["route1"][0] == 33 else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
