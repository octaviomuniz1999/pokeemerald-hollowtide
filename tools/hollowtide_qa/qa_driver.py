#!/usr/bin/env python3
"""Hollowtide QA: dirige o mgba_runner com rotas calculadas por BFS sobre a colisao real dos mapas.

Uso como biblioteca (ver roteiros em tools/hollowtide_qa/):
    q = QA(rom, runner, workdir); q.load("estado.ss"); q.goto("MAP_ROUTE101", 9, 52)
Cada passo salva/carrega savestate, entao a execucao pode ser retomada.
"""
import collections, glob, json, os, re, struct, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _load_maps():
    lay = {l["id"]: l for l in json.load(open(f"{ROOT}/data/layouts/layouts.json"))["layouts"] if "id" in l}
    groups = json.load(open(f"{ROOT}/data/maps/map_groups.json"))
    byid, bynum = {}, {}
    for gi, g in enumerate(groups["group_order"]):
        for ni, name in enumerate(groups[g]):
            j = json.load(open(f"{ROOT}/data/maps/{name}/map.json"))
            L = lay[j["layout"]]
            info = dict(name=name, id=j["id"], json=j, w=L["width"], h=L["height"],
                        bin=open(f"{ROOT}/{L['blockdata_filepath']}", "rb").read(), num=(gi, ni))
            byid[j["id"]] = info
            bynum[(gi, ni)] = info
    return byid, bynum


MAPS, MAPNUM = _load_maps()
SYMS = {}
for line in open(f"{ROOT}/pokeemerald.map"):
    parts = line.split()
    if len(parts) == 2 and parts[0].startswith("0x0") and parts[1] in ("gSaveBlock1Ptr", "gParties", "gObjectEvents", "gTasks"):
        SYMS.setdefault(parts[1], int(parts[0], 16))
    if len(parts) == 2 and parts[1] == "gBackupMapLayout" and parts[0].startswith("0x03"):
        SYMS.setdefault("gBackupMapLayout", int(parts[0], 16))
    if len(parts) == 2 and parts[1] == "gMain" and parts[0].startswith("0x03"):
        SYMS.setdefault("gMain", int(parts[0], 16))
SB1 = "%08x" % SYMS["gSaveBlock1Ptr"]
try:
    _nm = subprocess.check_output(["arm-none-eabi-nm", f"{ROOT}/pokeemerald.elf"]).decode()
    SYMS["BattleMainCB2"] = int(next(l.split()[0] for l in _nm.splitlines() if l.endswith(" BattleMainCB2")), 16)
except Exception:
    SYMS["BattleMainCB2"] = None


def block(m, x, y):
    if "rt" in m:  # grade lida da RAM (inclui setmetatile feitos por scripts)
        v = m["rt"][y * m["w"] + x]
    else:
        v = struct.unpack_from("<H", m["bin"], 2 * (y * m["w"] + x))[0]
    return v & 0x3FF, (v >> 10) & 3, v >> 12


def bfs(m, start, goal, avoid=()):
    """Caminho em tiles respeitando colisao e elevacao (0 e 15 conectam com qualquer elevacao)."""
    blocked = {(o["x"], o["y"]) for o in m["json"].get("object_events", [])} | set(avoid)
    blocked.discard(goal)
    prev = {start: None}
    dq = collections.deque([start])
    while dq:
        c = dq.popleft()
        if c == goal:
            break
        _, _, ec = block(m, *c)
        for d, (dx, dy) in (("UP", (0, -1)), ("DOWN", (0, 1)), ("LEFT", (-1, 0)), ("RIGHT", (1, 0))):
            n = (c[0] + dx, c[1] + dy)
            if not (0 <= n[0] < m["w"] and 0 <= n[1] < m["h"]) or n in prev or n in blocked:
                continue
            _, col, en = block(m, *n)
            if col:
                continue
            if ec not in (0, 15) and en not in (0, 15) and ec != en:
                continue
            prev[n] = (c, d)
            dq.append(n)
    if goal not in prev:
        return None
    path, c = [], goal
    while prev[c]:
        c, d = prev[c]
        path.append(d)
    return path[::-1]


class QA:
    def __init__(self, rom, runner, work):
        self.rom, self.runner, self.work = rom, runner, work
        self.state = None
        self.n = 0
        self.log = []

    def run(self, lines, tag="step"):
        self.n += 1
        out_state = f"{self.work}/s{self.n:03d}.ss"
        script = ([f"loadstate {self.state}", "wait 1"] if self.state else []) + lines + ["pos", f"savestate {out_state}"]
        sp = f"{self.work}/script.txt"
        open(sp, "w").write("\n".join(script) + "\n")
        r = subprocess.run([self.runner, self.rom, sp, "-", SB1], capture_output=True, text=True, cwd=self.work)
        if r.returncode not in (0, 2):
            raise RuntimeError(r.stderr + r.stdout)
        self.state = out_state
        pos = re.findall(r"mapa (-?\d+)\.(-?\d+) pos (-?\d+),(-?\d+)", r.stdout)[-1]
        self.where = tuple(map(int, pos))
        self.log.append((tag, self.where))
        if r.returncode == 2:
            raise AssertionError(r.stdout)
        return self.where

    def load(self, st):
        self.state = st

    def mapname(self):
        return MAPNUM[self.where[:2]]["id"]

    def goto(self, mapid, x, y, tries=40):
        stuck = 0
        self.battles = getattr(self, "battles", 0)
        for _ in range(tries):
            g, n, cx, cy = self.where if hasattr(self, "where") else self.run([])
            m = MAPNUM[(g, n)]
            if m["id"] != mapid:
                raise AssertionError(f"esperado {mapid}, estou em {m['id']} ({cx},{cy})")
            if (cx, cy) == (x, y):
                return True
            path = bfs(self.runtime_map(m), (cx, cy), (x, y))
            if path is None:
                raise AssertionError(f"sem caminho em {mapid} de {(cx, cy)} para {(x, y)}")
            before = self.where
            self.run([f"walk {d} 1" for d in path[:8]], f"goto {mapid} {x},{y}")
            if MAPNUM[self.where[:2]]["id"] != mapid:
                return True  # trocou de mapa (warp no destino)
            if self.where == before:
                # parado: dialogo, treinador ou batalha selvagem. Avanca com A (FIGHT -> 1o golpe).
                stuck += 1
                self.battles += 1
                seq = [f"shot stuck_{self.n:03d}.png"]
                if not self.in_battle():
                    # fora de batalha: fecha dialogos com B (A falaria com o seguidor/NPC e reabriria conversa)
                    self.run(seq + ["mash B 25"], "desbloqueio-dialogo")
                    if stuck > 8:
                        raise AssertionError(f"travado em {mapid} {self.where[2:]} (ver stuck_*.png)")
                    continue
                for _ in range(10):
                    # 1) tenta fugir (Run fica embaixo a direita); em batalha de treinador so mostra aviso
                    seq += ["press B 4 10", "press DOWN 4 6", "press RIGHT 4 6", "press A 4 30", "mash A 3"]
                    # 2) poe o cursor em FIGHT/Battle e usa o 1o golpe
                    seq += ["press B 4 10", "press UP 4 6", "press LEFT 4 6", "press A 4 20", "press A 4 20", "mash A 3"]
                self.run(seq, "desbloqueio")
                if stuck > 8:
                    raise AssertionError(f"travado em {mapid} {self.where[2:]} (ver stuck_*.png)")
            else:
                stuck = 0
        raise AssertionError(f"nao chegou a {mapid} {(x, y)}; em {self.where}")

    def no_wild(self, flags_vars_off="139C", party_addr=None, level_off=0x54):
        """Somente QA de mapas: Repel ativo + nivel 100 no lider do time => nenhum encontro selvagem.
        O nivel e so o campo em RAM (nao altera exp/estatisticas) e e refeito a cada chamada."""
        # Usa as flags de QA da build (FLAG_HT_QA_NO_ENCOUNTERS 0x31 e FLAG_HT_QA_NO_TRAINER_SEE 0x30).
        return self.run(["setflag 1270 31", "setflag 1270 30"], "no_wild")

    def peek32(self, addr):
        import re as _re
        out = subprocess.run([self.runner, self.rom, self._peek_script("%08x" % addr, 1), "-", SB1], capture_output=True, text=True, cwd=self.work).stdout
        return int(_re.findall(r"peek \w+: (\w+)", out)[-1], 16)

    def runtime_map(self, m):
        """Copia de m com a grade real da RAM (gBackupMapLayout, borda MAP_OFFSET=7)."""
        import re as _re
        lay = SYMS["gBackupMapLayout"]
        w = self.peek32(lay); ptr = self.peek32(lay + 8)
        words = (w * (m["h"] + 14) + 1) // 2
        out = subprocess.run([self.runner, self.rom, self._peek_script("%08x" % ptr, words), "-", SB1], capture_output=True, text=True, cwd=self.work).stdout
        vals = []
        for x in _re.findall(r"peek \w+: (.*)", out)[-1].split():
            v = int(x, 16); vals += [v & 0xFFFF, v >> 16]
        grid = [vals[(y + 7) * w + (x + 7)] for y in range(m["h"]) for x in range(m["w"])]
        mm = dict(m); mm["rt"] = grid
        return mm

    def in_battle(self):
        return SYMS.get("BattleMainCB2") is not None and (self.peek32(SYMS["gMain"] + 4) & ~1) == (SYMS["BattleMainCB2"] & ~1)

    def flag(self, n, flags_off=0x1270):
        """Le uma flag do SaveBlock1 no estado atual."""
        import re as _re
        out = subprocess.run([self.runner, self.rom, self._peek_script(SB1, 1), "-", SB1], capture_output=True, text=True, cwd=self.work).stdout
        sb1 = int(_re.findall(r"peek \w+: (\w+)", out)[-1], 16)
        addr = sb1 + flags_off + n // 8
        out = subprocess.run([self.runner, self.rom, self._peek_script("%08x" % (addr & ~3), 1), "-", SB1], capture_output=True, text=True, cwd=self.work).stdout
        word = int(_re.findall(r"peek \w+: (\w+)", out)[-1], 16)
        return bool((word >> (8 * (addr & 3) + n % 8)) & 1)

    def _peek_script(self, addr, n):
        sp = f"{self.work}/peek.txt"
        open(sp, "w").write(f"loadstate {self.state}\nwait 1\npeek {addr} {n}\n")
        return sp

    def strong(self):
        """Somente QA de eventos: liga FLAG_HT_QA_BOOST_PARTY (0x33); o gancho de QA do jogo (build
        nao-release) eleva o time a nivel 100 pela via oficial no proximo frame do overworld."""
        return self.run(["setflag 1270 33", "wait 5"], "strong")

    def step(self, d, n=1, extra=None):
        return self.run([f"walk {d} {n}"] + (extra or []), f"walk {d} {n}")

    def shot(self, name):
        return self.run([f"shot {name}"], f"shot {name}")
