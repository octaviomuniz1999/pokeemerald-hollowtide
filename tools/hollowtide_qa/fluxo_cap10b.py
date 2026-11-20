#!/usr/bin/env python3
"""QA do Capitulo 10 (parte 2): Tidemouth -> barco da Nami -> Complexo Oceanico (3 recrutas com visao) -> sala de
controle: Abelf -> sistema central desligado (a Palm se dissolve, o monitor mostra a montanha) -> barco de volta ->
ginasio da Nami destrancado.
Uso: fluxo_cap10b.py ROM RUNNER WORKDIR ESTADO_EM_TIDEMOUTH
"""
import shutil, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap8 import battle
from fluxo_cap7 import interact_until
from fluxo_cap2_eventos import battle as battle_all      # alterna os 4 golpes (Thunderbolt contra os aquaticos)

TF = 0x500
TD, C1, CC = "MAP_PALM_TIDEMOUTH", "MAP_PALM_OCEAN_COMPLEX_1F", "MAP_PALM_OCEAN_COMPLEX_CORE"
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def ride(q, target, first):
    """Aceita o barco (texto longo + SIM marcado) ate o mapa mudar."""
    q.run(first)
    for _ in range(14):
        if q.mapname() == target:
            break
        q.run(["press A 4 45", "wait 20"])
    q.run(["wait 120"])


def sighted(q, mapa, ax, ay, walk, nome, tid, avoid=()):
    q.strong()
    q.goto(mapa, ax, ay, avoid=avoid)
    if q.flag(TF + tid):
        ok(True, f"{nome} desafiou (no caminho)"); ok(True, f"Venceu {nome}")
        return
    q.run([walk, "wait 60"])
    seen = False
    for _ in range(60):
        if q.in_battle():
            seen = True
            break
        q.run(["press A 4 30"])
    ok(seen, f"{nome} avistou o jogador e desafiou")
    ok(battle(q, TF + tid), f"Venceu {nome}")
    q.run(["mash B 16"])


MOVED_G = set()


def sighted_g(q, mapa, ax, ay, walk, nome, tid):
    q.strong()
    q.goto(mapa, ax, ay, avoid=MOVED_G)
    if q.flag(TF + tid):
        ok(True, f"{nome} desafiou (no caminho)"); ok(True, f"Venceu {nome}")
        return
    q.run([walk, "wait 60"])
    seen = False
    for _ in range(40):
        if q.in_battle():
            seen = True
            break
        q.run(["press A 4 30"])
    ok(seen, f"{nome} avistou o jogador e desafiou")
    ok(battle_all(q, TF + tid), f"Venceu {nome}")
    q.run(["mash B 16"])


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"]); q.strong()
    q.goto(TD, 33, 38, avoid={(35, 38)}); ride(q, C1, ["press UP 18 0", "wait 30"]); q.run(["shot cap10_complexo.png"])
    ok(q.mapname() == C1, "Barco da Nami: Tidemouth -> Complexo Oceanico")
    sighted(q, C1, 4, 24, "walk UP 2", "Recruta do complexo 1", 5)
    sighted(q, C1, 11, 9, "walk RIGHT 2", "Recruta do complexo 2", 27, avoid={(4, 21)})
    sighted(q, C1, 21, 8, "walk RIGHT 2", "Recruta do complexo 3", 28, avoid={(4, 21), (13, 10)})
    q.goto(C1, 22, 2, avoid={(4, 21), (13, 10), (23, 7)}); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == CC, "Escada -> sala de controle")
    q.goto(CC, 14, 17); q.run(["press RIGHT 10 10", "press A 4 40", "mash B 40"])
    sighted(q, CC, 13, 18, "walk DOWN 2", "ABELF", 34, avoid={(15, 18)})
    q.run(["mash B 60", "shot cap10_abelf.png"])
    interact_until(q, CC, 12, 22, "LEFT", 0x55, presses=24, avoid={(13, 21), (15, 18)})
    q.run(["mash A 20", "mash B 40", "shot cap10_montanha.png"])
    ok(q.flag(0x55), "Sistema central desligado: a Team Palm se dissolve")
    for _ in range(10):
        if q.flag(0x270):
            break
        q.run(["mash A 10", "mash B 10"])
    ok(q.flag(0x270), "Nami entrega a HM03 SURF (chegou no WAILORD)")
    q.goto(CC, 13, 2, avoid={(15, 18), (13, 21)}); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == C1, "Sala de controle -> 1F")
    q.goto(C1, 10, 26, avoid={(4, 21), (13, 10), (23, 7)}); ride(q, TD, ["press LEFT 10 10", "press A 4 40"])
    ok(q.mapname() == TD, "Barco de volta a Tidemouth")
    q.strong()
    q.goto(TD, 39, 22); q.run(["press RIGHT 8 10", "press A 4 40", "mash A 6", "wait 120", "mash B 6",
                               "press RIGHT 16 0", "wait 30", "shot cap10_surf.png"])
    ok(q.mapname() == TD and q.where[2] >= 40, "Surf no canal de Tidemouth (uso de campo)")
    q.run(["press LEFT 30 0", "wait 30", "mash B 6"])
    q.goto(TD, 18, 26, avoid={(16, 28)}); q.run(["press UP 18 0", "wait 60", "mash B 10"])
    ok(q.mapname() != TD or q.where[3] <= 25, "Ginasio da Nami destrancado depois do complexo")
    shutil.copy(q.state, f"{work}/c10complexo.ss")
    # ginasio da Nami: 3 eclusas em ordem, 3 nadadores, Nami
    G = "MAP_PALM_NAMI_GYM"
    q.run(["press UP 30 0", "wait 120", "shot cap10_ginasio.png"])
    ok(q.mapname() == G, "Porta do pavilhao -> arena das eclusas")
    q.strong()
    def lever(x, y, face):
        q.goto(G, x, y, avoid=MOVED_G); q.run([f"press {face} 10 10"] + ["press A 4 45"] * 6 + ["mash B 20"])
    global MOVED_G
    lever(4, 34, "UP")
    sighted_g(q, G, 12, 27, "walk UP 2", "Nadadora das eclusas 1", 455)
    ok(tuple(q.where[2:]) in ((12, 25), (12, 26), (12, 27)), "Eclusa 1 drenou a primeira piscina")
    MOVED_G |= {(13, 25)}
    lever(19, 24, "UP")
    sighted_g(q, G, 12, 17, "walk UP 2", "Nadador das eclusas", 453)
    ok(q.where[3] <= 17, "Eclusa 2 drenou a segunda piscina")
    MOVED_G |= {(11, 15)}
    lever(4, 13, "DOWN")
    sighted_g(q, G, 12, 9, "walk UP 2", "Nadadora das eclusas 2", 595)
    ok(q.where[3] <= 9, "Eclusa 3 drenou a terceira piscina")
    MOVED_G |= {(13, 7)}
    q.strong()
    q.goto(G, 11, 4, avoid=MOVED_G); q.run(["press UP 10 10", "press A 4 40"])
    for _ in range(60):
        if q.in_battle():
            break
        q.run(["press A 4 30"])
    ok(battle_all(q, TF + 271), "Venceu NAMI")
    for _ in range(12):
        q.run(["mash A 8", "mash B 6"])
        if q.flag(0x860 + 14):
            break
    q.run(["mash B 90", "wait 30", "mash B 30", "shot cap10_insignia.png"])
    ok(q.flag(0x860 + 14), "Insignia Mare recebida (8 insignias)")
    q.goto(G, 11, 39, avoid=MOVED_G); q.run(["wait 120"])
    ok(q.mapname() == TD, "Saiu da arena para Tidemouth")
    shutil.copy(q.state, f"{work}/c10nami.ss")
    print("\nRESUMO CAPITULO 10 (parte 2)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
