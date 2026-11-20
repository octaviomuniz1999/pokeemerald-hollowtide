#!/usr/bin/env python3
"""QA do Capitulo 7 (parte 1) jogado de verdade: trava norte da Serenia (antes/depois da Insignia da
Serenidade) -> Route 7 (Celia, Connie, Henry, Colin com visao; 3 itens) -> Horizon City (conexao): estacao
fechada antes da Chelsia -> Chelsia e Piplup -> estacao sob o lago: 3 recrutas, 3 amplificadores, 3 Pokemon
presos, terminal com o registro -> agua baixou (jardim andavel) -> saida norte fechada -> Centro Pokemon.
Uso: fluxo_cap7.py ROM RUNNER WORKDIR ESTADO_POS_JADE
"""
import shutil, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA
from fluxo_cap2_eventos import battle
import json, struct

TF = 0x500
S, R7, HZ, LS = "MAP_PALM_SERENIA", "MAP_PALM_ROUTE07", "MAP_PALM_HORIZON", "MAP_PALM_LAKE_STATION"
G1, GB = "MAP_SOOTOPOLIS_CITY_GYM_1F", "MAP_SOOTOPOLIS_CITY_GYM_B1F"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ICE_FIELDS = [((17, 19), (8, 19), (8, 17)), ((12, 14), (8, 14), (8, 12)), ((6, 9), (8, 9), (8, 6))]


def ice_path(rows, start, end):
    """Caminho que pisa cada placa de gelo do campo uma unica vez (do pe da escada ate o pe da proxima)."""
    L = {l["id"]: l for l in json.load(open(f"{ROOT}/data/layouts/layouts.json"))["layouts"] if "id" in l}
    e = L["LAYOUT_SOOTOPOLIS_CITY_GYM_1F"]; w, h = e["width"], e["height"]
    b = struct.unpack(f"<{w * h}H", open(f"{ROOT}/{e['blockdata_filepath']}", "rb").read())
    cells = {(x, y) for y in range(rows[0], rows[1] + 1) for x in range(w)
             if not (b[y * w + x] >> 10) & 3 and (b[y * w + x] & 0x3FF) in (0x20D, 0x215, 0x216)}
    path, seen = [start], {start}
    def nb(c):
        x, y = c
        return [p for p in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)) if p in cells and p not in seen]
    def dfs(c):
        if len(path) == len(cells):
            return c == end
        if c == end:
            return False
        for p in sorted(nb(c), key=lambda p: len(nb(p))):
            seen.add(p); path.append(p)
            if dfs(p):
                return True
            seen.discard(p); path.pop()
        return False
    assert dfs(start), rows
    return path


def walk_cells(q, cur, cells):
    cmds = []
    for (x, y) in cells:
        d = {(0, -1): "UP", (0, 1): "DOWN", (1, 0): "RIGHT", (-1, 0): "LEFT"}[(x - cur[0], y - cur[1])]
        cmds.append(f"walk {d} 1"); cur = (x, y)
    q.run(cmds + ["wait 30"])
    return cur
BADGE5 = 0x860 + 11
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


GONE = {(20, 16), (21, 16), (20, 13), (21, 13), (20, 10), (21, 10), (21, 8), (24, 19), (25, 19)}   # Serenia: ja removidos


MOVED = {(28, 14), (30, 14), (29, 14)}   # Colin para ao lado do jogador depois de avistar (perto de (28, 14))


def talk(q, mapa, x, y, face, extra=("mash B 20",)):
    q.goto(mapa, x, y, ignore=GONE, avoid=MOVED if mapa == R7 else ())
    q.run([f"press {face} 10 10", "press A 4 40"] + list(extra))


def interact_until(q, mapa, x, y, face, flag, presses=16, avoid=()):
    """Fala/examina e vai apertando A ate a flag ligar (textos longos e SIM/NAO com SIM marcado)."""
    q.goto(mapa, x, y, ignore=GONE, avoid=set(avoid) | (MOVED if mapa == R7 else set()))
    q.run([f"press {face} 10 10"])
    for _ in range(presses):
        q.run(["press A 4 45"])
        if q.flag(flag):
            break
    q.run(["press A 4 45", "press A 4 45", "mash B 10"])


def sighted(q, mapa, ax, ay, walk, nome, tid):
    q.goto(mapa, ax, ay, ignore=GONE)
    if q.flag(TF + tid):
        ok(True, f"{nome} desafiou (no caminho)"); ok(True, f"Venceu {nome}")
        return
    q.run([walk, "wait 60"])
    seen = False
    for _ in range(25):
        if q.in_battle():
            seen = True
            break
        q.run(["press A 4 30"])
    ok(seen, f"{nome} avistou o jogador e desafiou")
    ok(battle(q, TF + tid, tries=140), f"Venceu {nome}")
    q.run(["mash B 16"])


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "clearflag 1270 30", f"clearflag 1270 {BADGE5:X}"])
    q.goto(S, 38, 2, ignore=GONE); q.run(["press UP 18 0", "wait 60", "mash A 24", "mash B 6", "wait 60"])
    ok(q.mapname() == S and tuple(q.where[2:]) == (38, 2), "Serenia: saida norte fechada antes da insignia (recua)")
    q.run([f"setflag 1270 {BADGE5:X}"]); q.strong()
    q.goto(S, 38, 0, ignore=GONE); q.run(["press UP 30 0", "wait 90", "shot cap7_rota7.png"])
    ok(q.mapname() == R7, "Serenia -> Route 7 (conexao, apos a insignia)")
    sighted(q, R7, 21, 47, "walk UP 2", "CELIA", 743)
    sighted(q, R7, 17, 32, "walk UP 2", "CONNIE", 128)
    sighted(q, R7, 16, 24, "walk UP 2", "HENRY", 668)
    sighted(q, R7, 27, 18, "walk UP 4", "COLIN", 405)
    for (x, y, face, flag, nome) in [(29, 12, "UP", 0x401, "Moon Stone do Circulo da Lua"), (5, 47, "LEFT", 0x402, "Mystic Water"),
                                     (32, 31, "UP", 0x403, "Pixie Plate")]:
        talk(q, R7, x, y, face, ("mash B 12",))
        ok(q.flag(flag), f"Route 7: {nome} coletado")
    q.goto(R7, 16, 0); q.run(["press UP 30 0", "wait 90", "shot cap7_horizon.png"])
    ok(q.mapname() == HZ, "Route 7 -> Horizon City (conexao)")
    q.goto(HZ, 5, 17); q.run(["press UP 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == HZ and tuple(q.where[2:]) == (5, 17), "Estacao do lago fechada antes da Chelsia (recua)")
    q.goto(HZ, 20, 20); q.run(["press UP 30 0", "wait 30"])
    ok(tuple(q.where[2:]) == (20, 20), "Jardim alagado: nao da para andar na agua da orla")
    talk(q, HZ, 24, 21, "UP", ("mash B 60", "wait 60", "mash B 30"))
    q.run(["shot cap7_chelsia.png"])
    ok(q.flag(0x42), "Chelsia e Piplup mostraram a estacao")
    q.goto(HZ, 5, 16, ignore={(24, 20), (25, 20)}); q.run(["press UP 30 0", "wait 120", "shot cap7_estacao.png"])
    ok(q.mapname() == LS, "Horizon -> estacao sob o lago")
    q.strong()
    sighted(q, LS, 18, 4, "walk DOWN 2", "Recruta 1", 2)
    sighted(q, LS, 21, 6, "walk RIGHT 1", "Recruta 2", 3)
    sighted(q, LS, 18, 12, "walk LEFT 1", "Recruta 3", 4)
    for (x, y, fl, n) in [(21, 6, 0x43, 1), (27, 6, 0x44, 2), (17, 9, 0x45, 3)]:
        interact_until(q, LS, x, y, "UP", fl)
        ok(q.flag(fl), f"Amplificador {n} desligado")
    for (x, y, face, fl, nome) in [(15, 13, "RIGHT", 0x46, "Marill"), (19, 11, "DOWN", 0x47, "Psyduck"), (21, 13, "LEFT", 0x48, "Lotad")]:
        interact_until(q, LS, x, y, face, fl)
        ok(q.flag(fl), f"{nome} solto da rede")
    interact_until(q, LS, 20, 9, "UP", 0x49, presses=24); q.run(["mash A 20", "shot cap7_registro.png", "mash B 20"])
    ok(q.flag(0x49), "Terminal: registro FONTE EXTERNA / NORTE / SINAL IRREGULAR")
    q.goto(LS, 18, 2, ignore={(16, 13), (19, 12), (20, 13)}); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == HZ and tuple(q.where[2:]) in ((5, 15), (5, 16)), "Estacao -> Horizon (porta certa)")
    q.goto(HZ, 20, 19, ignore={(24, 20), (25, 20)}); q.run(["wait 20", "shot cap7_jardim.png"])
    ok(q.mapname() == HZ and tuple(q.where[2:]) == (20, 19), "A agua baixou: o jardim da orla e andavel")
    q.goto(HZ, 52, 2, ignore={(24, 20), (25, 20)}); q.run(["press UP 18 0", "wait 60", "mash A 20", "mash B 6", "wait 40"])
    ok(q.mapname() == HZ and tuple(q.where[2:]) == (52, 2), "Saida norte fechada ate a 6a insignia (recua)")
    q.goto(HZ, 7, 29, ignore={(24, 20), (25, 20)}); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == "MAP_MOSSDEEP_CITY_POKEMON_CENTER_1F", "Horizon -> Centro Pokemon")
    q.goto("MAP_MOSSDEEP_CITY_POKEMON_CENTER_1F", 7, 8); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == HZ and tuple(q.where[2:]) in ((7, 28), (7, 29)), "Centro Pokemon -> Horizon (porta certa)")
    shutil.copy(q.state, f"{work}/c7lago.ss")
    # ginasio da Chelsia: tres campos de gelo (acender cada estrela uma vez), Chelsia, saida caindo no B1F
    q.goto(HZ, 39, 30, ignore={(24, 20), (25, 20)}); q.run(["press UP 30 0", "wait 120", "shot cap7_ginasio.png"])
    ok(q.mapname() == G1, "Ginasio da Chelsia aberto depois do lago baixar")
    q.strong()
    q.goto(G1, 8, 20)
    cur = (8, 20)
    for n, (rows, start, end) in enumerate(ICE_FIELDS, 1):
        cur = walk_cells(q, cur, ice_path(rows, start, end))
        q.run(["wait 100"])
        cur = walk_cells(q, cur, [(8, end[1] - 1), (8, end[1] - 2)])
        ok(q.mapname() == G1 and tuple(q.where[2:]) == (8, end[1] - 2), f"Constelacao {n} acesa: escada aberta")
    q.run(["shot cap7_estrelas.png"])
    q.run(["walk UP 1", "press UP 10 10", "press A 4 40"])
    ok(battle(q, TF + 272, tries=140), "Venceu CHELSIA")
    for _ in range(10):
        q.run(["mash A 8", "mash B 6"])
        if q.flag(0x860 + 12):
            break
    q.run(["mash B 90", "wait 30", "mash B 30", "shot cap7_insignia.png"])
    ok(q.flag(0x860 + 12), "Insignia do Horizonte recebida")
    q.run(["walk DOWN 1", "walk DOWN 1", "walk DOWN 1", "walk DOWN 1", "wait 200"])
    ok(q.mapname() == GB, "Gelo aceso quebra: caiu no andar de baixo")
    q.goto(GB, 11, 22); q.run(["wait 120"])
    ok(q.mapname() == G1, "Escada do B1F volta a entrada")
    q.goto(G1, 8, 25); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == HZ and tuple(q.where[2:]) in ((39, 29), (39, 30)), "Saiu do ginasio na porta certa")
    shutil.copy(q.state, f"{work}/c7chelsia.ss")
    q.goto(HZ, 26, 43, ignore={(24, 20), (25, 20)}); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == R7, "Horizon -> Route 7 (conexao)")
    q.goto(R7, 20, 55); q.run(["press DOWN 30 0", "wait 90"])
    ok(q.mapname() == S, "Route 7 -> Serenia (conexao)")
    print("\nRESUMO CAPITULO 7")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
