#!/usr/bin/env python3
"""Teste dirigido de Ferralia (25/11), na ROM de conteudo + provas/visual (warp pelo PC do quarto).

Casos: portas de verdade (Centro, Mart, estacao, casa) levam a um interior; a porta do ginasio esta trancada (fala);
placa da cidade e o recepcionista falam; o portao leste devolve o jogador (a Route 4 nao existe); a saida sul leva a
Route 3 a pe.
Uso: qa_ferralia.py ROM ESTADO_DO_QUARTO PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_visual import Visita
from qa_cap1 import walk, advance
import lunia_mundo as L

FERRALIA, ROUTE3 = 76, 43
CASOS = [
    # nome, inicio (GBA de Ferralia), passos, condicao final, ler (lado) ou None
    ("porta_do_centro", (20, 25), ["UP"] * 3, "interior", None),
    ("porta_do_mart", (36, 25), ["UP"] * 3, "interior", None),
    ("porta_da_estacao", (28, 13), ["UP"] * 3, "interior", None),
    ("porta_da_casa", (12, 12), ["UP"] * 3, "interior", None),
    ("ginasio_trancado", (49, 13), ["UP"] * 2, "fica", "UP"),
    ("placa_da_cidade", (39, 48), [], "fica", "UP"),
    ("recepcionista", (41, 48), [], "fica", "UP"),
    ("portao_leste", (67, 40), ["RIGHT"] * 4, "leste_fechado", None),
    ("descida_para_route3", (42, 60), ["DOWN"] * 8, "route3", None),
]


def main(rom, estado, pasta):
    os.makedirs(pasta, exist_ok=True)
    v = Visita(rom, estado, pasta)
    d = v.d
    ok_total = True
    for nome, (x, y), passos, cond, ler in CASOS:
        v.ir(*L.gba("Ferralia", x, y), espera=40)
        advance(d, 3); d.wait(20)
        caixa = False
        for p in passos:
            walk(d, [p])
            if d.box_visible():
                caixa = True
                advance(d, 6); d.wait(40)
        d.wait(60)
        if ler:
            d.press(ler, 4, 20); d.press("A", 4, 60); d.wait(40)
            caixa |= d.box_visible()
        v.foto(f"{pasta}/{nome}.png")
        advance(d, 8); d.wait(30)
        w = d.where()
        mapa = w[0] if w else None
        gx = w[1] - L.ORIGENS["Ferralia"][0] if w else None
        if cond == "interior":
            ok = mapa not in (None, FERRALIA, ROUTE3)
        elif cond == "fica":
            ok = mapa == FERRALIA and caixa
        elif cond == "leste_fechado":
            ok = mapa == FERRALIA and gx is not None and gx <= 69 and caixa
        else:
            ok = mapa == ROUTE3
        ok_total &= ok
        print(f"{nome:22} mapa {mapa} x_gba {gx} {'caixa' if caixa else ''} {'ok' if ok else 'FALHOU'}")
    print("RESULTADO Ferralia:", "ok" if ok_total else "FALHOU")
    return ok_total


if __name__ == "__main__":
    import shutil
    if "FAKETIME" not in os.environ and shutil.which("faketime"):
        os.execvp("faketime", ["faketime", "-f", "@2026-11-25 13:00:00", sys.executable] + sys.argv)
    sys.exit(0 if main(*sys.argv[1:4]) else 1)
