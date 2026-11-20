#!/usr/bin/env python3
"""QA do Capitulo 12 (partes 2 e 3): crista (posto da Joy, cura) -> Cynthia na ultima escadaria (aceitar voltar ->
recua; insistir duas vezes -> luta) -> cume: Tavinho (Primal Kyogre) -> medalhao, Doge, epilogo na Caverna Marinha
-> de volta ao cume sem tempestade -> tela final.
As duas lutas finais usam FLAG_HT_QA_GODMODE (so build nao-release): o QA confere os scripts, nao o balanceamento.
Uso: fluxo_cap12b.py ROM RUNNER WORKDIR ESTADO_TRILHA (c12trilha.ss)
"""
import os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from qa_driver import QA, SB1
from fluxo_cap11b import enemy_species, NAV

TF = 0x500
ST, SR, CB, SM, MC = ("MAP_PALM_STORM_TRAIL", "MAP_PALM_STORM_RIDGE", "MAP_PALM_STORM_CABIN", "MAP_PALM_STORM_SUMMIT",
                      "MAP_PALM_MARINE_EPILOGUE")
CYNTHIA_DONE, SUMMIT_DONE, GODMODE = 0x1AB, 0x1DA, 0x1DF
VAR_EPILOGUE = 0x409B
IDS = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define (TRAINER_\w+)\s+(\d+)",
       open(os.path.join(os.path.dirname(__file__), "..", "..", "include", "constants", "opponents.h")).read())}
# golpes do Mewtwo de QA: 0 Surf, 1 Aura Sphere, 2 Thunderbolt, 3 Psystrike
BEST = {442: 2, 407: 3, 468: 2, 448: 1, 350: 2, 445: 3, 947: 3,           # Cynthia
        279: 2, 260: 3, 212: 2, 1230: 3, 382: 2, 954: 2}                    # Tavinho
res = []


def ok(cond, label):
    res.append(("OK" if cond else "FALHA", label))
    print("OK   " if cond else "FALHA", label, flush=True)
    if not cond:
        raise SystemExit(1)


def var(q, v):
    out = subprocess.run([q.runner, q.rom, q._peek_script(SB1, 1), "-", SB1], capture_output=True, text=True, cwd=q.work).stdout
    sb1 = int(re.findall(r"peek \w+: (\w+)", out)[-1], 16)
    addr = sb1 + 0x139C + (v - 0x4000) * 2
    out = subprocess.run([q.runner, q.rom, q._peek_script("%08x" % (addr & ~3), 1), "-", SB1], capture_output=True, text=True, cwd=q.work).stdout
    word = int(re.findall(r"peek \w+: (\w+)", out)[-1], 16)
    return (word >> (8 * (addr & 3))) & 0xFFFF


def battle(q, flag, tries=500):
    for i in range(tries):
        if q.flag(flag) and not q.in_battle():
            return True
        if q.in_battle():
            slot = BEST.get(enemy_species(q), 3)
            if i % 5 == 4:                 # o golpe certo pode ficar sem PP numa luta longa (Full Restores): varia
                slot = (i // 5) % 4
            q.run(["press B 4 8", "press UP 4 6", "press LEFT 4 6", "press A 4 20", "press UP 4 6", "press LEFT 4 6"]
                  + NAV[slot] + ["press A 4 20", "wait 150", "mash B 4"])
        else:
            q.run(["mash B 6", "press A 4 30"])
    return q.flag(flag)


def until_battle(q, keys, n=60):
    for _ in range(n):
        if q.in_battle():
            return True
        q.run(keys)
    return False


def main(rom, runner, work, pre):
    q = QA(rom, runner, work)
    q.load(pre); q.no_wild(); q.run(["mash B 10", "setflag 1270 31", "setflag 1270 30"]); q.strong()
    q.goto(ST, 8, 0); q.run(["press UP 30 0", "wait 60", "shot cap12b_crista.png"])
    ok(q.mapname() == SR and q.where[2] == 8 and q.where[3] >= 43, "Trilha -> crista (conexao continua)")
    q.goto(SR, 13, 38); q.run(["press UP 30 0", "wait 120"])
    ok(q.mapname() == CB, "Crista -> cabana do posto da Joy")
    q.goto(CB, 2, 4); q.run(["press UP 10 10", "press A 4 40", "mash A 30", "wait 200", "mash A 10", "mash B 10", "shot cap12b_joy.png"])
    ok(q.mapname() == CB, "Joy cura o time (posto da Liga)")
    q.goto(CB, 3, 6); q.run(["press DOWN 30 0", "wait 120"])
    ok(q.mapname() == SR and tuple(q.where[2:]) == (13, 38), "Cabana -> crista (porta certa)")
    # Cynthia: aceitar voltar (A no SIM) -> recua
    q.goto(SR, 17, 15); q.run(["press UP 8 0", "wait 30", "mash A 40", "wait 60"])
    ok(not q.flag(CYNTHIA_DONE) and q.where[3] >= 15, "Cynthia: aceitar voltar faz o jogador recuar")
    # insistir (B = NAO nas duas perguntas) -> luta
    q.strong(); q.run([f"setflag 1270 {GODMODE:X}"])
    q.goto(SR, 17, 15); q.run(["press UP 8 0", "wait 30"])
    ok(until_battle(q, ["press B 4 30"]), "Cynthia: insistir duas vezes -> luta")
    ok(battle(q, TF + IDS["TRAINER_STEVEN"]), "Venceu CYNTHIA (Mega Garchomp por ultimo)")
    for _ in range(40):
        if q.flag(CYNTHIA_DONE):
            break
        q.run(["mash A 6", "wait 30"])
    q.run(["mash B 10", "shot cap12b_cynthia.png"])
    ok(q.flag(CYNTHIA_DONE), "Joy cura depois da luta e a Cynthia sai da frente")
    q.goto(SR, 17, 0); q.run(["press UP 30 0", "wait 60", "shot cap12b_cume.png"])
    ok(q.mapname() == SM and q.where[2] == 11 and q.where[3] >= 19, "Ultima escadaria -> cume")
    q.strong(); q.run([f"setflag 1270 {GODMODE:X}"])
    q.goto(SM, 11, 10); q.run(["press UP 8 0", "wait 30"])
    ok(until_battle(q, ["press A 4 30"]), "Tavinho desafia o jogador no cume")
    ok(battle(q, TF + IDS["TRAINER_MAXIE_MOSSDEEP"]), "Venceu TAVINHO (Primal Kyogre por ultimo)")
    seen_hoenn = False
    for _ in range(80):
        q.run(["mash A 6", "wait 40"])
        if q.mapname() == MC:
            seen_hoenn = True
            q.run(["shot cap12b_hoenn.png"])
        if q.mapname() == SM and var(q, VAR_EPILOGUE) == 3:
            break
    ok(q.flag(SUMMIT_DONE), "Medalhao, Doge e as falas finais")
    ok(seen_hoenn, "Epilogo: Doge sela o Kyogre na Caverna Marinha")
    q.run(["mash A 20", "wait 120", "shot cap12b_fim.png"])
    ok(q.mapname() == SM and var(q, VAR_EPILOGUE) == 3, "De volta ao cume, tempestade passou, tela final")
    q.run([f"clearflag 1270 {GODMODE:X}"])
    shutil.copy(q.state, f"{work}/c12fim.ss")
    q.goto(SM, 11, 21); q.run(["press DOWN 30 0", "wait 60"])
    ok(q.mapname() == SR, "Cume -> crista (volta livre)")
    print("\nRESUMO CAPITULO 12 (partes 2 e 3)")
    for r in res:
        print(" ", r[0], r[1])


if __name__ == "__main__":
    main(*sys.argv[1:5])
