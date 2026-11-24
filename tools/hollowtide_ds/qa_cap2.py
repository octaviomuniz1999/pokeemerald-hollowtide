#!/usr/bin/env python3
"""QA do Cap. 2 no DS: Breezeport (Olivine) e o Teatro da Jay, a partir do estado salvo pelo qa_cap1.py na chegada.

1. Teatro fechado antes do festival (porta do ginasio de Olivine, 269,238);
2. a artista (270,240) comeca o festival; os 3 lampioes: casas do oeste (266,250), praca (277,262), cais (279,272);
3. Teatro aberto; refletores ESQUERDA (4,20), DIREITA (8,20), ESQUERDA; Jay (6,5) -> Echo Badge;
4. saida norte (Route 3 = Route 39) liberada.
Uso: qa_cap2.py ROM ESTADO_BREEZEPORT PASTA   (ROM do build com provas/qa_forte, a mesma do estado)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import goto, face, fight, advance, walk

BREEZEPORT, TEATRO, ROUTE3 = 77, 138, 43                  # MAP_T26, MAP_T26GYM0101, MAP_R39
BZ_CELLS = [(8, 7), (9, 7), (8, 8), (9, 8)]
BZ_NPCS = {(270, 240), (266, 259), (280, 262), (279, 237), (262, 266), (279, 275), (273, 242), (299, 265), (289, 243),
           (286, 259), (284, 264)}
TE_CELLS, TE_MATRIX = [(0, 0)], 91
TE_NPCS = {(6, 5), (4, 15), (8, 15)}


def bz(d, rom, out, goal, tag):
    return goto(d, rom, goal, BZ_CELLS, BREEZEPORT, out, tag, avoid=BZ_NPCS)


def te(d, rom, out, goal, tag):
    return goto(d, rom, goal, TE_CELLS, TEATRO, out, tag, avoid=TE_NPCS, matrix=TE_MATRIX)


def use(d, key, out, name, n=10):
    face(d, key); d.press("A", 4, 60); d.shot(f"{out}/{name}.png"); advance(d, n)


def main(rom, state, out):
    os.makedirs(out, exist_ok=True)
    ok = {}
    d = DS(rom)
    d.load(state); d.wait(30)
    ok["inicio"] = d.where()
    # 1. Teatro fechado
    bz(d, rom, out, (269, 240), "bz")
    d.press("UP", 16, 24); d.press("UP", 16, 24); d.wait(30); d.shot(f"{out}/1_teatro_fechado.png"); advance(d, 8)
    ok["teatro_fechado"] = d.where()
    # 2. artista e lampioes
    bz(d, rom, out, (270, 241), "bz"); use(d, "UP", out, "2_artista", 14)
    bz(d, rom, out, (267, 250), "bz"); use(d, "LEFT", out, "3_lampiao1")
    bz(d, rom, out, (278, 262), "bz"); use(d, "LEFT", out, "4_lampiao2")
    bz(d, rom, out, (279, 271), "bz"); use(d, "DOWN", out, "5_lampiao3", 12)
    # 3. Teatro
    bz(d, rom, out, (269, 239), "bz"); d.press("UP", 16, 24); d.wait(200)
    ok["teatro"] = d.where(); d.shot(f"{out}/6_teatro.png")
    if ok["teatro"] and ok["teatro"][0] == TEATRO:
        te(d, rom, out, (5, 20), "te"); use(d, "LEFT", out, "7_esquerda")
        te(d, rom, out, (7, 20), "te"); use(d, "RIGHT", out, "8_direita")
        te(d, rom, out, (5, 20), "te"); use(d, "LEFT", out, "9_esquerda")
        b, w = te(d, rom, out, (6, 6), "te")
        face(d, "UP"); d.press("A", 4, 60)
        for _ in range(10):
            d.press("A", 4, 45)
            if not d.top_is_field():
                break
        d.wait(200); d.shot(f"{out}/10_jay.png")
        if not d.top_is_field():
            fight(d, 40)
        for i in range(14):
            d.press("B", 4, 45)
            if i in (4, 9):
                d.shot(f"{out}/11_insignia_{i}.png")
        ok["jay"] = d.where()
        te(d, rom, out, (6, 27), "te"); d.press("DOWN", 16, 24); d.wait(200)
        ok["saiu_teatro"] = d.where()
        # 4. saida norte
        bz(d, rom, out, (279, 235), "bz")
        for _ in range(6):
            d.press("UP", 16, 24)
        d.wait(200)
        ok["route3"] = d.where(); d.shot(f"{out}/12_route3.png")
    for k, v in ok.items():
        print(f"{k:14} {v}")
    good = ok.get("teatro_fechado", (0,))[0] == BREEZEPORT and ok.get("teatro", (0,))[0] == TEATRO and ok.get("route3", (0,))[0] == ROUTE3
    print("RESULTADO Breezeport:", "ok" if good else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
