#!/usr/bin/env python3
"""Teste dirigido da auditoria de acabamento (25/11): anda nas areas corrigidas, na ROM de conteudo + provas/visual.

Cada caso: warp para perto (qa_visual.Visita), uma sequencia de passos, posicao final esperada e captura.
- rampa da lagoa cercada de Dawnmere (entrada que virou rampa);
- costura Dawnmere -> Route 1 na saida leste (a coluna de grama que virou caminho);
- escadas da montanha de Breezeport ate o cume e o cercado elevado da Route 2;
- lampiao (bloqueado, com modelo) e placa de lampiao (le a fala);
- rocha solta da praia (bloqueada);
- cerca viva de arbustos em volta da torre de Harvestvale (bloqueada).
Uso: qa_acabamento.py ROM ESTADO_DO_QUARTO PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_visual import Visita
from qa_cap1 import walk, advance
import lunia_mundo as L

CASOS = [
    # nome, mapa do GBA, inicio (x, y), passos, posicao final esperada no GBA (x, y) ou None, ler placa
    ("rampa_lagoa_dawnmere", "Dawnmere", (25, 11), ["UP"] * 4, (25, 8), False),
    ("costura_route1_dawnmere", "Route1", (3, 4), ["LEFT"] * 3, (0, 4), False),   # a trava de Dawnmere fica em (33,21)
    ("escada_montanha_breezeport", "Brisa", (44, 17), ["UP"] * 12, (44, 5), False),   # cume: (44,4) e rocha
    ("cercado_route2", "Route2", (8, 33), ["UP"] * 5, (8, 28), False),
    ("lampiao_bloqueia", "Brisa", (12, 36), ["UP"] * 2, (12, 36), False),
    ("placa_do_lampiao", "Brisa", (12, 22), [], (12, 22), True),
    ("rocha_da_praia", "Brisa", (29, 44), ["UP"] * 2, (29, 44), False),
    ("arbustos_da_torre", "Harvestvale", (15, 26), ["DOWN"] * 2, (15, 26), False),
]


def main(rom, estado, pasta):
    os.makedirs(pasta, exist_ok=True)
    v = Visita(rom, estado, pasta)
    d = v.d
    ok_total = True
    for nome, mapa, (x, y), passos, fim, ler in CASOS:
        wx, wz = L.gba(mapa, x, y)
        v.ir(wx, wz, espera=40)
        advance(d, 3); d.wait(20)
        walk(d, passos)
        d.wait(40)
        w = d.where()
        texto = ""
        if ler:
            d.press("UP", 4, 20); d.press("A", 4, 60); d.wait(40)
            texto = "caixa de texto aberta" if d.box_visible() else "SEM caixa de texto"
        v.foto(f"{pasta}/{nome}.png")
        if ler:
            advance(d, 6)
        esperado = L.gba(mapa, *fim)
        ok = w is not None and (w[1], w[2]) == esperado and (not ler or texto == "caixa de texto aberta")
        ok_total &= ok
        gw = (w[1] - L.ORIGENS[mapa][0], w[2] - L.ORIGENS[mapa][1]) if w else None
        print(f"{nome:28} chegou GBA {gw} esperado {fim} {texto:22} {'ok' if ok else 'FALHOU'}")
    print("RESULTADO acabamento:", "ok" if ok_total else "FALHOU")
    return ok_total


if __name__ == "__main__":
    import shutil
    if "FAKETIME" not in os.environ and shutil.which("faketime"):
        os.execvp("faketime", ["faketime", "-f", "@2026-11-25 13:00:00", sys.executable] + sys.argv)
    sys.exit(0 if main(*sys.argv[1:4]) else 1)
