#!/usr/bin/env python3
"""QA do CP-DS-03A: o bloco de terreno gerado (mapa_teste.py) no lugar da metade sul da Route 39 (mapa 43, celula
(8,6): mundo x 256-287, z 192-223), a partir do estado salvo pelo qa_cap2.py na saida norte de Breezeport, ou do estado do quarto (ds_intro.py) usando o
atalho de QA da build de prova (o PC do quarto leva ao corredor norte de Breezeport, logo abaixo da divisa).

Passos (captura e mapa/posicao/altura em cada um; altura = y da posicao 3D do objeto (+0x74), conferida ao subir a rampa):
1. chega pela emenda sul (caminho, colunas 21-25);  2. caminho ao norte e a oeste ate o pe da rampa;
3. sobe a rampa ate o plato (altura muda);  4. colisao: placa (construcao) e penhasco visto de cima;
5. desce, colisao do penhasco visto de baixo e de uma arvore;  6. volta a Breezeport pela emenda e entra de novo.
Uso: qa_cp03a.py ROM ESTADO_ROUTE3 PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import goto, face

TEST, BREEZEPORT = 43, 77
X0, Z0 = 256, 192
CELLS = [(8, 6)]
BZ_CELLS = [(8, 7), (9, 7), (8, 8), (9, 8)]


def W(x, z):
    return (X0 + x, Z0 + z)


def height(d):
    obj = d.u32(d.avatar + 0x30)                        # posicao 3D do objeto (fx32 x, y, z em +0x70); y em tiles
    return d.emu.memory.signed.read_long(obj + 0x74) / 4096 / 16


def main(rom, state, out):
    os.makedirs(out, exist_ok=True)
    ok, log = {}, []
    d = DS(rom); d.load(state); d.wait(30)
    def step(tag):
        w = d.where(); h = round(height(d), 2) if w else None
        if os.environ.get("QA_DUMP_OBJ") and w:      # memoria do objeto do jogador (para achar o campo de altura)
            obj = d.u32(d.avatar + 0x30)
            open(f"{out}/{tag}.obj", "wb").write(bytes(d.emu.memory.unsigned[obj:obj + 0x140]))
        log.append((tag, w, h)); d.shot(f"{out}/{tag}.png")
        return w, h
    if d.where() and d.where()[0] == 64:                # estado do quarto (ds_intro): atalho de QA no PC (provas/cp03a)
        d.press("UP", 16, 24); d.press("UP", 4, 20); d.press("A", 4, 30)
        for _ in range(20):
            d.wait(30)
            if d.where() and d.where()[0] == BREEZEPORT:
                break
        d.wait(120); step("0_atalho_breezeport")
    for _ in range(6):                                  # corredor norte de Breezeport -> divisa
        if d.where() and d.where()[0] == TEST:
            break
        d.press("UP", 16, 24)
    d.wait(60)
    ok["entrada"] = step("1_entrada")
    go = lambda goal, tag: goto(d, rom, W(*goal), CELLS, TEST, out, tag, fight_ok=True)
    go((23, 19), "c"); step("2a_caminho_norte")
    go((15, 19), "c"); step("2b_caminho_oeste")
    go((15, 15), "c"); ok["pe_rampa"] = step("2c_pe_da_rampa")
    go((15, 13), "c"); step("3a_meio_da_rampa")
    go((15, 10), "c"); ok["plato"] = step("3b_plato")
    go((18, 8), "c"); face(d, "RIGHT")
    for _ in range(3):
        d.press("RIGHT", 16, 24)
    ok["placa"] = step("4a_contra_a_placa")
    go((10, 11), "c")
    for _ in range(3):
        d.press("DOWN", 16, 24)
    ok["penhasco_de_cima"] = step("4b_penhasco_de_cima")
    go((15, 10), "c"); go((15, 16), "c"); go((10, 13), "c")
    for _ in range(3):
        d.press("UP", 16, 24)
    ok["penhasco_de_baixo"] = step("5a_penhasco_de_baixo")
    go((4, 13), "c")
    for _ in range(3):
        d.press("LEFT", 16, 24)
    ok["arvore"] = step("5b_contra_a_arvore")
    go((23, 31), "c")
    for _ in range(3):
        d.press("DOWN", 16, 24)
    d.wait(60); ok["voltou_breezeport"] = step("6a_voltou_breezeport")
    for _ in range(4):
        d.press("UP", 16, 24)
    d.wait(60); ok["entrou_de_novo"] = step("6b_entrou_de_novo")
    for t, w, h in log:
        print(f"{t:24} {w} altura {h}")
    g = lambda k: ok[k][0]
    good = (g("entrada") and g("entrada")[0] == TEST and ok["pe_rampa"][1] == 1.0 and ok["plato"][1] == 2.0
            and g("placa")[1:] == W(18, 8) and g("penhasco_de_cima")[1:] == W(10, 11)
            and g("penhasco_de_baixo")[1:] == W(10, 13) and g("arvore")[1:] == W(4, 13)
            and g("voltou_breezeport")[0] == BREEZEPORT and g("entrou_de_novo")[0] == TEST)
    print("RESULTADO CP-DS-03A:", "ok" if good else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
