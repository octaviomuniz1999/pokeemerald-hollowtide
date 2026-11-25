#!/usr/bin/env python3
"""Teste dirigido da Route 3 original (25/11), na ROM de conteudo + provas/visual (o PC do quarto da um Tyranitar e
faz o warp que o qa_visual troca na RAM).

Casos: escadas dos patamares (praia -> meio, meio -> alto), batalha com o Tomas (visao no caminho da escada), as tres
placas (praia, platô, porta trancada da casa), a Great Ball no chao, e a praia ate Breezeport a pe.
Uso: qa_route3.py ROM ESTADO_DO_QUARTO PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_visual import Visita
from qa_cap1 import walk, advance
import lunia_mundo as L


def batalha(d, limite=600):
    """Treinador que viu o jogador: a fala de desafio, a batalha e a fala depois. Aperta A enquanto houver caixa de texto
    ou tela de batalha. Devolve True se houve batalha (tela de baixo fora do campo)."""
    houve, calmo = False, 0
    for _ in range(limite):
        campo = d.top_is_field()
        if campo and not d.box_visible():
            # entre o fim da fala e o comeco da batalha ha quadros sem caixa e com o campo na tela: so termina depois de
            # uns 90 quadros seguidos de campo calmo
            calmo += 1
            if calmo >= 6:
                break
            d.wait(15)
            continue
        calmo = 0
        houve |= not campo
        d.press("A", 4, 20)
    d.wait(120)                                          # volta da batalha: o fade engole a proxima tecla
    return houve


CASOS = [
    # nome, inicio no GBA da Route 3, passos, fim esperado (mapa, x, y) ou None, ler (lado) ou None, batalha esperada
    ("escada_praia_para_o_meio", (40, 51), ["UP"] * 9, ("Route3", 40, 43), None, True),    # 1o UP so vira; Tomas ve o caminho
    ("escada_meio_para_o_alto", (14, 33), ["UP"] * 5, ("Route3", 14, 28), None, False),
    ("placa_da_praia", (42, 55), [], ("Route3", 42, 55), "UP", False),
    ("porta_trancada", (19, 62), [], ("Route3", 19, 62), "UP", False),
    ("great_ball", (18, 30), [], ("Route3", 18, 30), "UP", False),
    ("placa_do_plato", (28, 4), [], ("Route3", 28, 4), "UP", False),
    ("praia_ate_breezeport", (52, 56), ["RIGHT"] * 5, None, None, False),
]


def main(rom, estado, pasta):
    os.makedirs(pasta, exist_ok=True)
    v = Visita(rom, estado, pasta)
    d = v.d
    ok_total = True
    for nome, (x, y), passos, fim, ler, quer_batalha in CASOS:
        wx, wz = L.gba("Route3", x, y)
        v.ir(wx, wz, espera=40)
        advance(d, 3); d.wait(20)
        houve = False
        for p in passos:
            antes = d.where()
            walk(d, [p])
            parado = d.where() == antes                  # preso: um treinador viu o jogador
            # o "!" e a caminhada do treinador levam uns 170 quadros, e outra tecla de direcao nesse meio tempo cancela a
            # abordagem: espera depois de cada passo
            for _ in range(20 if parado else 13):
                if d.box_visible() or not d.top_is_field():
                    houve |= batalha(d)
                    break
                d.wait(15)
        d.wait(30)
        texto = ""
        if ler:
            d.press(ler, 4, 20); d.press("A", 4, 60); d.wait(40)
            texto = "caixa de texto aberta" if d.box_visible() else "SEM caixa de texto"
        v.foto(f"{pasta}/{nome}.png")
        if ler:
            advance(d, 8); d.wait(30)
        w = d.where()
        if fim and nome == "escada_praia_para_o_meio":
            # a batalha engole um numero variavel de teclas (o fade da volta): basta ter passado do topo da escada (y 43)
            # na mesma coluna
            fx, fz = L.gba(*fim)
            ok = w is not None and w[1] == fx and w[2] <= fz
        elif fim:
            ok = w is not None and (w[1], w[2]) == L.gba(*fim)
        else:                                            # praia -> Breezeport: chegou ao header de Breezeport (77)
            ok = w is not None and w[0] == 77
        if ler:
            ok &= texto == "caixa de texto aberta"
        if quer_batalha:
            ok &= houve
        ok_total &= ok
        gw = (w[0], w[1] - L.ORIGENS["Route3"][0], w[2] - L.ORIGENS["Route3"][1]) if w else None
        print(f"{nome:26} chegou (mapa, GBA da Route 3) {gw} esperado {fim} {texto} "
              f"{'batalha' if houve else ''} {'ok' if ok else 'FALHOU'}")
    print("RESULTADO Route 3:", "ok" if ok_total else "FALHOU")
    return ok_total


if __name__ == "__main__":
    import shutil
    if "FAKETIME" not in os.environ and shutil.which("faketime"):
        os.execvp("faketime", ["faketime", "-f", "@2026-11-25 13:00:00", sys.executable] + sys.argv)
    sys.exit(0 if main(*sys.argv[1:4]) else 1)
