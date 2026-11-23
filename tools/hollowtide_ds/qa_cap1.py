#!/usr/bin/env python3
"""QA do Cap. 1 no DS: do quarto ate a Route 1, com a ROM do conteudo (build.sh sem pastas de prova).

Passos (cada um imprime mapa/posicao e salva uma captura em PASTA):
1. quarto -> escada -> a mae e o Medalhao de Atlas (avanca com B);
2. sai de casa (Dawnmere): sem a cena da Lyra; tenta a saida oeste sem Pokemon -> fala do GBA e um passo de volta;
3. laboratorio: Prof. Alex -> escolha (bola da frente) -> Pokedex, Poke Balls, Potions, missao;
4. volta e sai pelo oeste -> Route 1 (mapa 33);
5. atravessa a Route 1 pelo caminho mais curto, lutando (Kai, Min, selvagens), ate Harvestvale.
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


def route_path(rom_path, start, goal, cells):
    """Caminho mais curto a pe entre dois tiles pela colisao dos blocos (matriz 0, celulas dadas)."""
    import collections
    import ndspy.narc, ndspy.rom
    from matrix import Matrix
    from hgss_seams import perms
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    lds = ndspy.narc.NARC(rom.getFileByName("a/0/6/5")).files
    mt = Matrix(ndspy.narc.NARC(rom.getFileByName("a/0/4/1")).files[0])
    free = set()
    for bx, by in cells:
        pm = perms(lds[mt.land[by * mt.w + bx]])
        for ty in range(32):
            for tx in range(32):
                v = pm[ty * 32 + tx]
                if not v & 0x8000 and (v & 0xFF) not in range(0x10, 0x1A):
                    free.add((bx * 32 + tx, by * 32 + ty))
    prev = {start: None}; q = collections.deque([start])
    while q:
        c = q.popleft()
        if c == goal:
            break
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if n in free and n not in prev:
                prev[n] = c; q.append(n)
    path, c = [], goal
    while c:
        path.append(c); c = prev[c]
    return path[::-1]


MOVES = [(64, 48), (192, 48), (64, 120), (192, 120)]      # os 4 botoes de golpe na tela de baixo


def fight(d, max_turns=25):
    """Luta alternando os 4 golpes (um deles pode nao causar dano) ate voltar ao campo."""
    for t in range(max_turns):
        for _ in range(6):
            d.press("B", 4, 30)
        if d.top_is_field():
            return True
        d.touch(128, 90, 6, 60); d.touch(*MOVES[t % 4], 6, 60)
        for _ in range(10):
            d.press("B", 4, 40)
        if d.top_is_field():
            return True
    return False


GYM = 395                                                # MAP_T07GYM0101 (interior do ginasio do Nevard), asm/include/maps.inc
HARVESTVALE = 67                                         # MAP_T21 (Cherrygrove), asm/include/maps.inc


def goto(d, rom, goal, cells, map_id, out, tag, fight_ok=True, max_steps=400):
    """Anda ate goal pelo caminho mais curto (colisao dos blocos), lutando se uma batalha comecar.
    Devolve (batalhas, posicao final)."""
    battles = 0
    w = d.where()
    path = route_path(rom, (w[1], w[2]), goal, cells)
    i, steps, last, still = 1, 0, None, 0
    while steps < max_steps:
        steps += 1
        w = d.where()
        if not d.top_is_field():
            if not fight_ok:
                break
            d.shot(f"{out}/{tag}_batalha_{battles}.png"); battles += 1
            fight(d); advance(d, 6); continue
        if not w or w[0] != map_id:
            break
        cur = (w[1], w[2])
        if cur == goal:
            break
        still = still + 1 if cur == last else 0
        last = cur
        if still in (8, 30):
            d.shot(f"{out}/{tag}_parado_{cur[0]}_{cur[1]}.png"); advance(d, 6)
        if still > 40:
            break
        if cur in path:
            i = path.index(cur) + 1
        if i >= len(path):
            break
        nx = path[i]
        key = {(1, 0): "RIGHT", (-1, 0): "LEFT", (0, 1): "DOWN", (0, -1): "UP"}.get((nx[0] - cur[0], nx[1] - cur[1]))
        if key is None:
            path = route_path(rom, cur, goal, cells); i = 1; continue
        d.press(key, 16, 24)
    return battles, d.where()


def face(d, key):
    """Vira para um lado sem andar (toque curto)."""
    d.press(key, 3, 20)


HV_CELLS = [(16, 12), (17, 12)]


def harvestvale(d, rom, out, ok):
    """Harvestvale: chegada, porta do ginasio fechada, recruta, valvula, ginasio aberto, saida norte fechada."""
    d.shot(f"{out}/8_chegada.png"); advance(d, 20)
    ok["hv_chegada"] = d.where()
    # porta do ginasio (558,401) ainda fechada: tenta entrar e deve voltar
    goto(d, rom, (558, 403), HV_CELLS, HARVESTVALE, out, "hv")
    d.press("UP", 16, 24); d.wait(30); d.shot(f"{out}/9_ginasio_fechado.png"); advance(d, 10)
    ok["hv_ginasio_fechado"] = d.where()
    # recruta no quiosque (538,403), virado para a direita: fala de (539,403)
    goto(d, rom, (539, 403), HV_CELLS, HARVESTVALE, out, "hv")
    face(d, "LEFT"); d.press("A", 4, 60); advance(d, 8, "A")
    d.wait(200); d.shot(f"{out}/10_recruta.png")
    if not d.top_is_field():
        fight(d)
    advance(d, 12)
    ok["hv_recruta"] = d.where()
    # valvula (537,396): fala de (538,396) olhando para a esquerda
    goto(d, rom, (538, 396), HV_CELLS, HARVESTVALE, out, "hv")
    face(d, "LEFT"); d.press("A", 4, 60); d.shot(f"{out}/11_valvula.png"); advance(d, 12)
    # saida norte (547,385) fechada ate o Nevard
    goto(d, rom, (547, 387), HV_CELLS, HARVESTVALE, out, "hv")
    d.press("UP", 16, 24); d.press("UP", 16, 24); d.wait(30); d.shot(f"{out}/12_saida_norte.png"); advance(d, 10)
    ok["hv_saida_norte"] = d.where()
    # ginasio aberto
    goto(d, rom, (558, 402), HV_CELLS, HARVESTVALE, out, "hv")
    d.press("UP", 16, 24); d.wait(200); d.shot(f"{out}/13_ginasio.png")
    ok["hv_ginasio"] = d.where()


def cross_route1(d, rom, out, n0):
    """Atravessa a Route 1 (mapa 33) para o oeste pelo caminho mais curto; devolve (batalhas, posicao final)."""
    battles = 0
    start = d.where()[1:]
    path = route_path(rom, start, (576, 399), [(18, 12), (19, 12), (20, 12)])
    i, steps, last, still = 1, 0, None, 0
    while i < len(path) and steps < 600:
        steps += 1
        w = d.where()
        if not d.top_is_field():
            d.shot(f"{out}/6_batalha_{n0 + battles}.png"); battles += 1
            fight(d); advance(d, 6); continue
        if w and w[0] != 33:
            return battles, w
        cur = (w[1], w[2])
        still = still + 1 if cur == last else 0
        last = cur
        if still in (8, 30):                             # parado: algo na frente (mensagem, NPC) -> registra e tenta B
            d.shot(f"{out}/6_parado_{cur[0]}_{cur[1]}.png"); advance(d, 6)
        if still > 40:
            break
        if cur in path:
            i = path.index(cur) + 1
            if i >= len(path):
                break
        nx = path[i]
        key = {(1, 0): "RIGHT", (-1, 0): "LEFT", (0, 1): "DOWN", (0, -1): "UP"}.get((nx[0] - cur[0], nx[1] - cur[1]))
        if key is None:
            break
        d.press(key, 16, 24)
    walk(d, ["LEFT"] * 4, stop_map=None); d.wait(200)
    return battles, d.where()


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
    # Route 1 a pe ate Harvestvale, lutando o que aparecer (Kai e Min veem o jogador; mato alto tem selvagens).
    # Se perder, o jogo leva para casa (a mae cura): sai de novo e tenta outra vez, como um jogador faria.
    battles, tries = 0, 0
    while tries < 4:
        tries += 1
        w = d.where()
        if w and w[0] == 63:                              # derrota: de volta ao terreo de casa
            advance(d, 70)                               # a fala da mae depois da derrota e longa
            x, y = d.where()[1:]
            walk(d, ["LEFT"] * max(0, x - 3) + ["DOWN"] * 6, stop_map=60); d.wait(200)
            walk(d, ["DOWN"] + ["LEFT"] * 30, stop_map=33); d.wait(200)
        w = d.where()
        if not w or w[0] != 33:
            break
        b, w = cross_route1(d, rom, out, battles)
        battles += b
        if w and w[0] == HARVESTVALE:
            break
    ok["tentativas"] = tries
    ok["batalhas"] = battles
    ok["harvestvale"] = d.where(); d.shot(f"{out}/7_harvestvale.png")
    if ok["harvestvale"] and ok["harvestvale"][0] == HARVESTVALE:
        harvestvale(d, rom, out, ok)
    for k, v in ok.items():
        print(f"{k:10} {v}")
    good = ok["barrado"] and ok["barrado"][0] == 60 and ok["route1"] and ok["route1"][0] == 33 and ok["harvestvale"] and ok["harvestvale"][0] == HARVESTVALE
    hv = good and ok.get("hv_ginasio_fechado", (0,))[0] == HARVESTVALE and ok.get("hv_saida_norte", (0,))[0] == HARVESTVALE \
        and ok.get("hv_ginasio", (0,))[0] == GYM
    print("RESULTADO:", "ok" if good else "FALHOU", "| Harvestvale:", "ok" if hv else "FALHOU")


if __name__ == "__main__":
    main(*sys.argv[1:4])
