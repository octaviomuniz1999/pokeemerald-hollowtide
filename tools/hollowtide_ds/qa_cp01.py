#!/usr/bin/env python3
"""QA do CP-DS-01 (prova de edicao de mapa): a placa da Route 1 na saida oeste de Dawnmere (bloco 0, tile 5,12 =
mundo 677,396), acrescentada por land.json (modelo 3D 30 + colisao) e 0621 (placa legivel, texto 542/8).

1. do quarto ate a Route 1 com o inicial (qa_cap1.ate_route1): sai de Dawnmere pela divisa oeste;
2. volta a pe pela divisa para Dawnmere (mapa 60) e para embaixo da placa (677,397) -> captura;
3. colisao: UP contra a placa (posicao nao muda); de (678,396) LEFT contra a placa (nao muda);
4. leitura: de (677,397) olhando para cima, A -> caixa "Route 1 / ← Harvestvale";
5. sai de novo para a Route 1 e volta (os dois sentidos da divisa);
6. salva o jogo pelo menu (SAVE), reinicia o console (a memoria do save fica) e da CONTINUE; andar para cima contra
   a placa abre a mesma caixa de antes (comparacao pixel a pixel) -> mesmo lugar, placa e colisao no lugar.
   (Um DeSmuME novo, em outro processo, nao reconhece o .dsv gravado e cai em NEW GAME: limite do emulador.)
Uso: qa_cp01.py ROM ESTADO_BASE PASTA   (ESTADO_BASE de ds_intro.py na mesma ROM)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import ate_route1, goto, face, advance, walk

DAWNMERE, ROUTE1 = 60, 33
CELLS = [(21, 12)]
SIGN, BELOW, RIGHT_OF = (677, 396), (677, 397), (678, 396)
HG = "/home/user/blurosie/hg-engine"


def npcs():
    ev = json.load(open(os.path.join(HG, "data/eventdata/zone_event/057_T20.json")))
    return {(o["x"], o["z"]) for o in ev["object_events"]}


def main(rom, base, out):
    os.makedirs(out, exist_ok=True)
    ok = {}
    d = DS(rom)
    d.load(base); d.wait(30)
    ate_route1(d, out, ok)
    # 2. volta para Dawnmere pela divisa
    walk(d, ["RIGHT"] * 6, stop_map=DAWNMERE); d.wait(120)
    ok["volta_dawnmere"] = d.where()
    goto(d, rom, BELOW, CELLS, DAWNMERE, out, "dm", avoid=npcs())
    face(d, "UP"); d.wait(30)
    ok["embaixo_da_placa"] = d.where(); d.shot(f"{out}/cp01_1_placa.png")
    # 3. colisao
    for _ in range(3):
        d.press("UP", 16, 24)
    ok["colisao_de_baixo"] = d.where(); d.shot(f"{out}/cp01_2_colisao_baixo.png")
    goto(d, rom, RIGHT_OF, CELLS, DAWNMERE, out, "dm", avoid=npcs())
    for _ in range(3):
        d.press("LEFT", 16, 24)
    ok["colisao_do_lado"] = d.where(); d.shot(f"{out}/cp01_3_colisao_lado.png")
    # 4. leitura
    goto(d, rom, BELOW, CELLS, DAWNMERE, out, "dm", avoid=npcs())
    face(d, "UP"); d.press("A", 4, 90)
    d.shot(f"{out}/cp01_4_leitura.png"); advance(d, 4)
    ok["leu"] = d.where()
    # 5. divisa nos dois sentidos de novo
    w = walk(d, ["DOWN"] + ["LEFT"] * 8, stop_map=ROUTE1); d.wait(120)
    ok["saiu_route1"] = d.where(); d.shot(f"{out}/cp01_5_route1.png")
    walk(d, ["RIGHT"] * 4, stop_map=DAWNMERE); d.wait(120)
    ok["voltou_dawnmere"] = d.where()
    goto(d, rom, BELOW, CELLS, DAWNMERE, out, "dm", avoid=npcs()); advance(d, 4)   # sem virar para a placa (andar
    ok["antes_de_salvar"] = d.where()                                               # contra ela abre a leitura)
    d.save(f"{out}/antes_de_salvar.dst")
    # 6. salvar pelo menu do campo (botao SAVE da tela de baixo), reiniciar, CONTINUE
    d.touch(124, 76, 8, 120); d.shot(f"{out}/cp01_6a_menu_save.png")
    for k in range(6):
        d.press("A", 4, 150)
        if k == 1:
            d.shot(f"{out}/cp01_6b_pergunta.png")
    for _ in range(25):
        d.wait(30)
    d.shot(f"{out}/cp01_6_salvou.png"); advance(d, 4)
    # reinicia o console (a memoria do save fica, como desligar e ligar) e da CONTINUE pela abertura
    d.reset()
    for i in range(200):
        d.wait(60)
        d.press("START" if i % 2 else "A", 4, 30)
        if i > 10 and d.top_is_field():                 # menu verde do campo: o CONTINUE carregou
            break
    d.wait(200); advance(d, 3)
    d.shot(f"{out}/cp01_7a_continue.png")
    # prova da posicao: andar para cima contra a placa abre a mesma caixa da leitura de antes de salvar
    d.press("UP", 16, 90); d.shot(f"{out}/cp01_7_carregado.png")
    from PIL import Image, ImageChops
    box = (10, 150, 234, 186)                          # interior da caixa de texto
    a_, b_ = Image.open(f"{out}/cp01_4_leitura.png").crop(box), Image.open(f"{out}/cp01_7_carregado.png").crop(box)
    ok["placa_depois_de_carregar"] = ImageChops.difference(a_.convert("RGB"), b_.convert("RGB")).getbbox() is None
    advance(d, 4)
    for k, v in ok.items():
        print(f"{k:20} {v}")
    good = (ok["embaixo_da_placa"] and ok["embaixo_da_placa"][1:] == BELOW
            and ok["colisao_de_baixo"][1:] == BELOW and ok["colisao_do_lado"][1:] == RIGHT_OF
            and ok["saiu_route1"][0] == ROUTE1 and ok["voltou_dawnmere"][0] == DAWNMERE
            and ok["placa_depois_de_carregar"])
    print("RESULTADO CP-DS-01:", "ok" if good else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
