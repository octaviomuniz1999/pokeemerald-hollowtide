#!/usr/bin/env python3
"""QA dos eventos de Dawnmere e da Route 1 nas posicoes do GBA (provas/cp03c, 0922-0924), pelo fluxo do jogo, sem atalho:
quarto -> mae -> porta da casa do jogador (GBA 2,9) -> placa da casa -> saida leste sem Pokemon (trava, um passo para
oeste) -> placa do laboratorio -> porta do laboratorio -> Prof. Alex e o inicial -> volta pela porta -> guia ->
saida leste com Pokemon -> Route 1 (header 33): placa norte, andarilho, Potion, Kai e Min (visao do GBA), placa sul.
Capturas em cada passo (as batalhas tambem, em kai_batalha_N / min_batalha_N).
Uso: qa_cp03d.py ROM ESTADO_QUARTO PASTA [--cap1]   (ESTADO_QUARTO de ds_intro.py na mesma ROM; build com provas/cp03c e
     provas/qa_forte, que da um Tyranitar junto com o Medalhao: o inicial de nivel 5 perde para o Kai com o robo)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import walk, goto, face, advance, starter_screen, fight, route2, GYM_CELLS, GYM_NPCS, GYM_MATRIX, BREEZEPORT
CAP1 = "--cap1" in sys.argv                              # build de conteudo: segue pelo Nevard, a ponte e a Route 2

from lunia_mundo import X0, Z0, CELLS, D, R1, HV, R2
DAWNMERE, ROUTE1, LAB, HARVESTVALE, GYM = 60, 33, 61, 67, 395
NPCS = {D(23, 18), D(11, 24), D(23, 10),              # guia, vizinho, mirante (fora da colisao dos blocos)
        R1(12, 6), R1(22, 25), R1(17, 39), R1(13, 24),  # andarilho, Kai, Min, Potion (Route 1)
        R1(21, 25), R1(18, 39),                          # Kai e Min depois de virem ate o jogador
        HV(11, 6), HV(7, 32),                            # fazendeiro e recruta (Harvestvale)
        R2(26, 13), R2(16, 27), R2(21, 35), R2(7, 26),   # Liang, Mei Lan, Qin, Super Potion (Route 2)
        R2(24, 13), R2(18, 27), R2(19, 35)}              # Liang, Mei Lan e Qin depois de virem ate o jogador




def main(rom, state, out):
    os.makedirs(out, exist_ok=True)
    d = DS(rom); d.load(state); d.wait(30)
    log = []

    def step(tag, extra=""):
        w = d.where(); log.append((tag, w, extra)); d.shot(f"{out}/{tag}.png"); print(tag, w, flush=True); return w

    def go(goal, tag, fight_ok=False):
        try:
            return goto(d, rom, goal, CELLS, (DAWNMERE, ROUTE1, HARVESTVALE, 34, 35), out, tag, fight_ok=fight_ok,
                        avoid=NPCS)[0]
        except KeyError:                                  # alvo inalcancavel de onde o robo esta: registra e segue
            print("sem caminho de", d.where(), "ate", goal)
        return 0

    def ler(tag, lado="UP"):
        face(d, lado); d.press("A", 4, 60); d.wait(40); step(tag); advance(d, 8); d.wait(30)

    walk(d, ["UP", "UP", "LEFT", "LEFT", "LEFT", "UP", "LEFT", "LEFT"]); d.wait(200)
    advance(d, 45); d.wait(60)
    walk(d, ["DOWN"] * 8, stop_map=DAWNMERE); d.wait(200); advance(d, 6)
    step("1_porta_da_casa", "esperado desenho (4, 12): um passo abaixo da porta do GBA (2,9)")
    go(D(11, 20), "c"); ler("2_placa_da_casa")
    go(D(32, 21), "c"); d.press("RIGHT", 16, 24); d.wait(40)
    step("3_trava_leste")
    advance(d, 25); d.wait(90)
    step("4_depois_da_trava", "esperado GBA x 32 (um passo para oeste da saida 33)")
    go(D(15, 10), "c"); ler("5_placa_do_lab")
    go(D(13, 10), "c")
    walk(d, ["UP"] * 4, stop_map=LAB); d.wait(200)
    step("6_lab")
    walk(d, ["UP"] * 8 + ["RIGHT"] * 2 + ["UP"])
    d.press("A", 4, 60)
    for _ in range(60):
        if starter_screen(d):
            break
        d.press("A", 4, 50)
    for _ in range(6):
        if not starter_screen(d):
            break
        d.wait(300); d.press("A", 4, 120)
        d.touch(128, 110, 8, 150); d.touch(128, 110, 8, 150)
        for _ in range(10):
            d.wait(30)
    for _ in range(40):
        d.wait(30)
    advance(d, 70); step("7_inicial")
    walk(d, ["LEFT", "LEFT"] + ["DOWN"] * 9, stop_map=DAWNMERE); d.wait(200); advance(d, 4)
    step("8_saida_do_lab", "esperado desenho (15, 11): abaixo da porta do laboratorio")
    go(D(23, 19), "c"); ler("9_guia")
    go(D(32, 21), "c")
    for _ in range(5):
        d.press("RIGHT", 16, 24)
    d.wait(60); step("10_route1")
    # Route 1 (etapa 4): eventos nas posicoes do Route101 do GBA (origem (36,19) no desenho)
    go(R1(7, 22), "c"); ler("11_placa_norte")
    go(R1(11, 6), "c"); ler("12_andarilho", "RIGHT")
    go(R1(13, 25), "c"); ler("13_potion")
    def visao(goal, tag):
        """Anda ate o tile na visao do treinador; a batalha comeca depois que o treinador vem ate o jogador."""
        n = go(goal, tag, fight_ok=True)
        for _ in range(12):
            d.wait(60)
            if not d.top_is_field():
                d.shot(f"{out}/{tag}_batalha_{n}.png"); fight(d); advance(d, 10); n += 1
                break
            d.press("B", 4, 20)
        return n
    nk = visao(R1(20, 25), "kai"); d.wait(60); step("14_kai", f"batalhas: {nk}")
    nm = visao(R1(19, 39), "min"); d.wait(60); step("15_min", f"batalhas: {nm}")
    go(R1(6, 49), "c", fight_ok=True); ler("16_placa_sul")
    # Harvestvale (etapa 5, so o mapa e as construcoes; os eventos ainda estao nas posicoes do prototipo)
    # Harvestvale (etapa 5): eventos nas posicoes do OldaleTown do GBA (origem (37,72) no desenho)
    go(HV(9, 4), "c", fight_ok=True); d.wait(60)
    d.press("DOWN", 16, 24); d.wait(60)                 # linha 5 (GBA 2, descida 3): o fazendeiro chama (Palm072_Arrival)
    step("17_harvestvale_chegada"); advance(d, 12); d.wait(40)
    go(HV(12, 12), "c"); ler("18_placa_boas_vindas")
    go(HV(5, 23), "c"); d.press("UP", 16, 24); d.wait(40)
    step("19_ginasio_fechado"); advance(d, 12); d.wait(60)
    step("20_depois_do_ginasio", "esperado desenho (42, 95): um passo para baixo")
    go(HV(7, 33), "c"); face(d, "UP"); d.press("A", 4, 60)
    nr = 0
    for _ in range(30):                                  # recruta: fala, batalha (treinador 483), volta ao campo
        d.wait(40)
        if not d.top_is_field():
            d.shot(f"{out}/recruta_batalha.png"); fight(d); advance(d, 12); nr += 1
            break
        d.press("A", 4, 30)
    d.wait(60); step("21_recruta", f"batalhas: {nr}"); advance(d, 6)
    go(HV(26, 23), "c"); ler("22_valvula", "RIGHT"); advance(d, 10)
    go(HV(18, 34), "c"); d.press("DOWN", 16, 24); d.wait(40)
    step("23_saida_sul_fechada"); advance(d, 12); d.wait(60)
    step("24_depois_da_saida_sul", "esperado desenho (55, 106): um passo para cima")
    go(HV(5, 23), "c")
    walk(d, ["UP"] * 3, stop_map=GYM); d.wait(200)
    step("25_ginasio_aberto")
    if CAP1:                                              # build de conteudo (etapa 6): Nevard, ponte e Route 2
        b, _ = goto(d, rom, (7, 4), GYM_CELLS, GYM, out, "gym", avoid=GYM_NPCS, matrix=GYM_MATRIX, max_steps=600)
        face(d, "UP"); d.press("A", 4, 60)
        for _ in range(12):
            d.press("A", 4, 45)
            if not d.top_is_field():
                break
        d.wait(200); step("26_nevard", f"batalhas no caminho: {b}")
        if not d.top_is_field():
            fight(d, 40)
        advance(d, 36)
        step("27_depois_do_nevard")
        goto(d, rom, (7, 46), GYM_CELLS, GYM, out, "gym", avoid=GYM_NPCS, matrix=GYM_MATRIX, max_steps=600)
        d.press("DOWN", 16, 24); d.wait(200)
        step("28_saida_do_ginasio", "esperado desenho (42, 94): abaixo da porta do GBA")
        d.wait(30); d.save(f"{out}/depois_do_nevard.dst")      # ponto de partida para testar so a Route 2
        # Route 2 original (PalmRoute02): Harvestvale -> Route 2 a pe, sem warp
        go(HV(18, 34), "c")
        for _ in range(3):
            d.press("DOWN", 16, 24)
        d.wait(80); step("29_route2_entrada", "esperado header 34 (R30) na Route 2 original")
        go(R2(16, 4), "r2", fight_ok=True); ler("30_placa_norte_r2")
        nl = visao(R2(23, 13), "liang"); step("31_liang", f"batalhas: {nl}")
        go(R2(7, 27), "r2", fight_ok=True); ler("32_super_potion")
        nm2 = visao(R2(19, 27), "meilan"); step("33_mei_lan", f"batalhas: {nm2}")
        go(R2(14, 37), "r2", fight_ok=True); ler("34_porta_trancada")
        nq = visao(R2(18, 35), "qin"); step("35_qin", f"batalhas: {nq}")
        go(R2(17, 41), "r2", fight_ok=True); ler("36_placa_sul_r2")
        go(R2(19, 46), "r2", fight_ok=True)
        d.press("DOWN", 16, 24); d.wait(250); step("37_guarita", "esperado a guarita do prototipo (ponte provisoria)")
        for _ in range(24):
            w = d.where()
            if w and w[0] == BREEZEPORT:
                break
            d.press("LEFT", 16, 24); d.wait(60)
        d.wait(200); step("38_breezeport")
    for t, w, e in log:
        print(f"{t:20} {w}  {e}")
    r = {t: w for t, w, _ in log}
    checks = {"porta da casa": r["1_porta_da_casa"] == (DAWNMERE, *D(2, 10)),
              "trava": r["4_depois_da_trava"] and r["4_depois_da_trava"][1] == D(32, 21)[0],
              "porta do lab": r["6_lab"] and r["6_lab"][0] == LAB,
              "volta do lab": r["8_saida_do_lab"] == (DAWNMERE, *D(13, 9)),
              "route 1": r["10_route1"] and r["10_route1"][0] == ROUTE1,
              "batalha Kai": nk >= 1, "batalha Min": nm >= 1,
              "placa sul": r["16_placa_sul"] and r["16_placa_sul"][1:] == R1(6, 49),
              "harvestvale": r["17_harvestvale_chegada"] and r["17_harvestvale_chegada"][0] == HARVESTVALE,
              "ginasio fechado": r["20_depois_do_ginasio"] == (HARVESTVALE, *HV(5, 23)),
              "recruta": nr >= 1,
              "saida sul fechada": r["24_depois_da_saida_sul"] == (HARVESTVALE, *HV(18, 34)),
              "ginasio aberto": r["25_ginasio_aberto"] and r["25_ginasio_aberto"][0] == GYM}
    if CAP1:
        checks.update({"Nevard": r["27_depois_do_nevard"] and r["27_depois_do_nevard"][0] == GYM,
                       "volta do ginasio": r["28_saida_do_ginasio"] == (HARVESTVALE, *HV(5, 22)),
                       "Route 2 a pe": r["29_route2_entrada"] and r["29_route2_entrada"][0] == 34,
                       "Liang": nl >= 1, "Mei Lan": nm2 >= 1, "Qin": nq >= 1,
                       "guarita": r["37_guarita"] and r["37_guarita"][0] == 97,
                       "Breezeport": r["38_breezeport"] and r["38_breezeport"][0] == BREEZEPORT})
    for k, v in checks.items():
        print(f"  {k:14} {'ok' if v else 'FALHOU'}")
    print("RESULTADO CP-DS-03B eventos de Dawnmere:", "ok" if all(checks.values()) else "FALHOU")


if __name__ == "__main__":
    main(*[a for a in sys.argv[1:] if a != "--cap1"][:3])
