#!/usr/bin/env python3
"""QA do Capitulo 11 (parte 2): saguao da Liga -> guardas -> Angelic (sala de gelo) -> Riven (sala roxa) ->
Du (tatame) -> Pkas (sala laranja, Mega Charizard X) -> Doge (Mega Latios) -> Hall da Fama -> fim de jogo.
Uso: fluxo_cap11b.py ROM RUNNER WORKDIR ESTADO_SAGUAO (c11liga.ss)
"""
import os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA, SB1
from fluxo_cap2_eventos import battle as battle_all

NAV = {0: [], 1: ["press RIGHT 4 6"], 2: ["press DOWN 4 6"], 3: ["press DOWN 4 6", "press RIGHT 4 6"]}


def enemy_species(q):
    """Especie do Pokemon adversario em campo: gBattleMons[1].species (struct BattlePokemon de 140 bytes;
    o endereco de gBattleMons vem do pokeemerald.map)."""
    import re as _re
    if not hasattr(enemy_species, "addr"):
        mp = open(os.path.join(os.path.dirname(__file__), "..", "..", "pokeemerald.map")).read()
        enemy_species.addr = int(_re.search(r"0x([0-9a-f]{8})\s+gBattleMons\n", mp).group(1), 16) + 140
    out = subprocess.run([q.runner, q.rom, q._peek_script("%08x" % enemy_species.addr, 1), "-", SB1],
                         capture_output=True, text=True, cwd=q.work).stdout
    return int(_re.findall(r"peek \w+: (\w+)", out)[-1], 16) & 0xFFFF


# golpes do Mewtwo de QA: 0 Surf, 1 Aura Sphere, 2 Thunderbolt, 3 Psystrike
BEST = {1291: 1, 197: 1,            # Meowscarada, Umbreon: Aura Sphere
        38: 3, 134: 2,              # Ninetales: Psystrike; Vaporeon: Thunderbolt
        249: 2, 381: 2, 945: 2}     # Lugia, Latios, Mega Latios: Thunderbolt


def battle_smart(q, flag, tries=500):
    """Como battle_all, mas escolhe o golpe pelo Pokemon adversario em campo (a IA do Doge troca de Pokemon)."""
    for i in range(tries):
        if q.flag(flag) and not q.in_battle():
            q.run(["mash B 20"])
            return True
        if q.in_battle():
            slot = BEST.get(enemy_species(q), 1)
            if i % 5 == 4:                 # o golpe certo pode ficar sem PP numa luta longa (Full Restores): varia
                slot = (i // 5) % 4
            q.run(["press B 4 8", "press UP 4 6", "press LEFT 4 6", "press A 4 20", "press UP 4 6", "press LEFT 4 6"]
                  + NAV[slot] + ["press A 4 20", "wait 150", "mash B 4"])
        else:
            q.run(["mash B 6", "press A 4 30"])
    return q.flag(flag)

TF = 0x500
L1 = "MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F"
H = {i: f"MAP_EVER_GRANDE_CITY_HALL{i}" for i in range(1, 6)}
ROOMS = [("MAP_EVER_GRANDE_CITY_GLACIAS_ROOM", "ANGELIC", 0x4FD, H[1]),
         ("MAP_EVER_GRANDE_CITY_PHOEBES_ROOM", "RIVEN", 0x4FC, H[2]),
         ("MAP_EVER_GRANDE_CITY_SIDNEYS_ROOM", "DU", 0x4FB, H[3]),
         ("MAP_EVER_GRANDE_CITY_DRAKES_ROOM", "PKAS", 0x4FE, H[4])]
CHAMP, HOF = "MAP_EVER_GRANDE_CITY_CHAMPIONS_ROOM", "MAP_EVER_GRANDE_CITY_HALL_OF_FAME"
WALLACE = 335
GAME_CLEAR = 0x864
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def hall_up(q, hall, nxt):
    top = min(y for y in (2,))
    q.goto(hall, 5, top + 1); q.run(["press UP 30 0", "wait 150"])
    ok(q.mapname() == nxt, f"{hall.split('_')[-1]} -> {nxt.split('MAP_EVER_GRANDE_CITY_')[-1]}")


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30"]); q.strong()
    ok(q.mapname() == L1, "Saguao da Liga")
    q.goto(L1, 9, 3); q.run(["press UP 10 10", "press A 4 40"])      # os guardas ficam na frente da porta (9,2)/(10,2)
    for _ in range(12):
        q.run(["wait 120", "press A 4 30"])
        if q.flag(0x107):
            break
    q.run(["mash B 6", "wait 60"])
    ok(q.flag(0x107), "Guardas conferem as 8 insignias e abrem a porta")
    q.goto(L1, 9, 2); q.run(["press UP 30 0", "wait 150"])
    ok(q.mapname() == H[5], "Saguao -> corredor da Elite")
    hall_up(q, H[5], ROOMS[0][0])
    for (room, nome, flag, hall) in ROOMS:
        q.run(["wait 200", "mash B 6"])                 # entra andando e a porta fecha
        q.strong()
        q.run([f"shot cap11b_{nome.lower()}_sala.png", "press UP 10 10", "press A 4 40"])
        seen = False
        for _ in range(40):
            if q.in_battle():
                seen = True
                break
            q.run(["press A 4 30"])
        ok(seen, f"{nome} desafia o jogador")
        ok(battle_all(q, flag, tries=220), f"Venceu {nome}")
        q.run(["mash B 30", "wait 60"])
        x, y = q.where[2:]
        q.goto(room, 6, 3, avoid={(6, 5)}); q.run(["press UP 30 0", "wait 150"])
        ok(q.mapname() == hall, f"Porta aberta: {nome} -> corredor")
        hall_up(q, hall, ROOMS[ROOMS.index((room, nome, flag, hall)) + 1][0] if hall != H[4] else CHAMP)
    q.strong()
    q.run(["setflag 1270 1DF"])          # FLAG_HT_QA_GODMODE (so build nao-release): o QA confere o script do campeao, nao o balanceamento
    seen = False
    for _ in range(60):
        if q.in_battle():
            seen = True
            break
        q.run(["press A 4 30"])
    ok(seen, "DOGE desafia o jogador")
    ok(battle_smart(q, TF + WALLACE), "Venceu DOGE (campeao)")
    for _ in range(40):
        q.run(["mash A 10", "wait 60"])
        if q.mapname() == HOF:
            break
    ok(q.mapname() == HOF, "Doge leva o jogador ao Hall da Fama")
    q.run(["shot cap11b_hof.png"])
    for _ in range(30):
        q.run(["mash A 10", "wait 120"])
        if q.flag(GAME_CLEAR):
            break
    ok(q.flag(GAME_CLEAR), "Hall da Fama registrado (FLAG_SYS_GAME_CLEAR)")
    q.run(["clearflag 1270 1DF"])
    q.run(["wait 600", "shot cap11b_creditos.png"])
    shutil.copy(q.state, f"{work}/c11fim.ss")
    print("\nRESUMO CAPITULO 11 (parte 2)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
