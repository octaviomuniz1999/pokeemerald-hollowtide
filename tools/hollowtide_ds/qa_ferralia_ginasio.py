#!/usr/bin/env python3
"""Teste dirigido do patio de cargas e do ginasio de Ferralia (25/11), na ROM de conteudo + provas/visual (o PC do
quarto da um Tyranitar e faz o warp que o qa_visual troca na RAM).

Sequencia numa sessao so (as flags valem de um passo para o outro):
  1. porta do ginasio fechada antes do patio (gatilho em 49,13: fala e volta um passo);
  2. Vessel no patio pede ajuda;
  3. batalha com os dois recrutas (visao);
  4. Vessel agradece e os tres somem;
  5. a porta do ginasio abre (entra no interior 137, MAP_T25GYM0101).
Depois, warp direto para dentro do ginasio: o guia fala e Vessel luta e da a insignia.
Uso: qa_ferralia_ginasio.py ROM ESTADO_DO_QUARTO PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_visual import Visita
from qa_cap1 import walk, advance, goto
from qa_route3 import batalha
import lunia_mundo as L

FERRALIA, GINASIO = 76, 137


def andar(d, passos):
    houve = False
    for p in passos:
        antes = d.where()
        walk(d, [p])
        parado = d.where() == antes
        for _ in range(20 if parado else 13):
            if d.box_visible() or not d.top_is_field():
                houve |= batalha(d)
                break
            d.wait(15)
    return houve


def encontro(d, quadros=300):
    """Espera ate `quadros` pela caixa de texto ou pela batalha (o "!" e a caminhada do treinador, ou a fala que demora a
    abrir) e resolve; devolve True se houve batalha."""
    for _ in range(quadros // 15):
        if d.box_visible() or not d.top_is_field():
            return batalha(d, 900)
        d.wait(15)
    return False


def falar(d, lado="UP"):
    d.press(lado, 4, 20); d.press("A", 4, 60); d.wait(40)
    return d.box_visible()


def main(rom_path, estado, pasta):
    global rom
    rom = rom_path
    os.makedirs(pasta, exist_ok=True)
    v = Visita(rom_path, estado, pasta)
    d = v.d
    log = []

    def passo(nome, ok, extra=""):
        v.foto(f"{pasta}/{nome}.png")
        w = d.where()
        log.append((nome, ok)); print(f"{nome:28} {w} {extra} {'ok' if ok else 'FALHOU'}")
    F = lambda x, y: L.gba("Ferralia", x, y)
    # 1. porta fechada
    v.ir(*F(49, 15), espera=40); advance(d, 3)
    walk(d, ["UP"] * 3); d.wait(60)
    caixa = d.box_visible(); advance(d, 8); d.wait(60)
    w = d.where()
    passo("1_ginasio_fechado", caixa and w[0] == FERRALIA and w[2] >= F(49, 13)[1])
    # 2. Vessel pede ajuda (Vessel em 63,29 olhando para a esquerda: falar de 62,29)
    d2 = F(62, 29)
    walk(d, ["DOWN"] * 1)
    v.ir(*d2, espera=40)                                  # warp de novo: as flags da sessao sao do estado salvo
    advance(d, 3)
    passo("2_vessel_pede_ajuda", falar(d, "RIGHT")); advance(d, 12); d.wait(40)
    # 3. recrutas: o 1 em 67,28 olha para a esquerda (visao 2); o 2 em 66,35 olha para cima (visao 2)
    npcs = [F(63, 29), F(67, 28), F(66, 35)]
    vai = lambda alvo, tag: goto(d, rom, alvo, L.CELLS, (FERRALIA,), pasta, tag, fight_ok=True, avoid=npcs)
    b1, _ = vai(F(65, 28), "recruta1")
    b1 = b1 or encontro(d)
    passo("3a_recruta_1", b1 > 0 if isinstance(b1, int) else bool(b1))
    # o recruta 1 para ao lado do jogador; de frente para ele a tela de baixo mostra "TALK" e nao o menu, que o robo le
    # como fora do campo: um passo para baixo antes de seguir
    advance(d, 4); walk(d, ["DOWN", "DOWN"])
    b2, _ = vai(F(66, 33), "recruta2")
    b2 = b2 or encontro(d)
    passo("3b_recruta_2", b2 > 0 if isinstance(b2, int) else bool(b2))
    # 4. Vessel agradece (falar de 62,29, olhando para a direita)
    vai(F(62, 29), "vessel")
    ok4 = falar(d, "RIGHT"); advance(d, 16); d.wait(90)
    passo("4_vessel_agradece", ok4)
    # 5. a porta do ginasio abre: anda ate a frente da porta (o gatilho de 49,13 agora so termina) e entra
    goto(d, rom, F(49, 14), L.CELLS, (FERRALIA,), pasta, "porta", fight_ok=False)
    walk(d, ["UP"] * 3); d.wait(200)
    w = d.where()
    passo("5_ginasio_aberto", w is not None and w[0] == GINASIO)
    # 6. dentro do ginasio: guia e Vessel (warp direto)
    v.ir(7, 24, espera=40, mapa=GINASIO); advance(d, 3)
    passo("6a_guia", falar(d, "UP")); advance(d, 12); d.wait(40)
    v.ir(13, 5, espera=40, mapa=GINASIO); advance(d, 3)
    d.press("UP", 4, 20); d.press("A", 4, 30)
    houve = encontro(d)
    advance(d, 20); d.wait(60)
    passo("6b_vessel_lider", houve, "(batalha e insignia)")
    ok = all(o for _, o in log)
    print("RESULTADO Ferralia patio/ginasio:", "ok" if ok else "FALHOU")
    return ok


if __name__ == "__main__":
    import shutil
    if "FAKETIME" not in os.environ and shutil.which("faketime"):
        os.execvp("faketime", ["faketime", "-f", "@2026-11-25 13:00:00", sys.executable] + sys.argv)
    sys.exit(0 if main(*sys.argv[1:4]) else 1)
