#!/usr/bin/env python3
"""CP-DS-02B: SAVE/CONTINUE nativo entre execucoes independentes do emulador (sem savestate em nenhum passo).

Fase 1 (processo 1): liga o console com a ROM, jogo novo ate o quarto, desce, a mae entrega o medalhao, SALVA pelo
menu do jogo na casa (mapa 63), sai para Dawnmere (mapa 60) SEM salvar e fecha o emulador (desmume_close).
Fase 2 (processo 2, emulador novo): liga a mesma ROM, CONTINUE -> o jogo tem de voltar a casa (63), nao a Dawnmere.
O save nativo e o arquivo .dsv do DeSmuME (~/.config/desmume/<nome da ROM>.dsv); o script mostra tamanho e hash
antes e depois de cada passo. Uso: qa_save.py ROM PASTA [TIPO_DE_SAVE]   (tipo 0 = autodetectar; 6 = FLASH 4 Mbit)
"""
import hashlib, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from ds_intro import new_game
from qa_cap1 import walk, advance

DSV_DIR = os.path.expanduser("~/.config/desmume")


def dsv(rom):
    p = os.path.join(DSV_DIR, os.path.splitext(os.path.basename(rom))[0] + ".dsv")
    if not os.path.exists(p):
        return p, "nao existe"
    b = open(p, "rb").read()
    return p, f"{len(b)} bytes sha1 {hashlib.sha1(b).hexdigest()[:12]} mtime {time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(p)))}"


def save_menu(d, out, tag):
    d.touch(124, 76, 8, 120); d.shot(f"{out}/{tag}_a_menu.png")
    for k in range(6):
        d.press("A", 4, 150)
        if k == 1:
            d.shot(f"{out}/{tag}_b_pergunta.png")
    for _ in range(25):
        d.wait(30)
    d.shot(f"{out}/{tag}_c_salvou.png"); advance(d, 4)


def fase1(rom, out, savetype):
    d = DS(rom, savetype)
    print("dsv no inicio:", dsv(rom)[1])
    print("quarto:", new_game(d))
    walk(d, ["UP", "UP", "LEFT", "LEFT", "LEFT", "UP", "LEFT", "LEFT"]); d.wait(200)
    advance(d, 45); d.wait(60)
    casa = d.where(); print("casa:", casa)
    save_menu(d, out, "s1")
    print("dsv depois de salvar:", dsv(rom)[1])
    d.wait(120); advance(d, 6)
    walk(d, ["DOWN"] * 8); d.wait(200); advance(d, 6)
    print("depois (sem salvar):", d.where()); d.shot(f"{out}/s1_d_fora_sem_salvar.png")
    d.emu.close()
    print("dsv depois de fechar:", dsv(rom)[1])
    print("FASE1", casa)


def fase2(rom, out, savetype):
    d = DS(rom, savetype)
    print("dsv ao abrir:", dsv(rom)[1])
    for i in range(200):
        d.wait(60)
        d.press("START" if i % 2 else "A", 4, 30)
        if i in (15, 30):
            d.shot(f"{out}/s2_titulo_{i}.png")
        if i > 10 and d.top_is_field():
            break
    d.wait(200); advance(d, 3); d.shot(f"{out}/s2_a_continue.png")
    d.press("DOWN", 16, 30); d.press("UP", 16, 30)      # o gancho do avatar so dispara quando o jogador anda
    d.shot(f"{out}/s2_b_carregado.png")
    print("FASE2", d.where())


def main(rom, out, savetype="0"):
    os.makedirs(out, exist_ok=True)
    p = dsv(rom)[0]
    if os.path.exists(p):
        os.remove(p)                                   # comeca sem save
    env = dict(os.environ)
    r1 = subprocess.run([sys.executable, __file__, "--fase1", rom, out, savetype], capture_output=True, text=True, env=env)
    r2 = subprocess.run([sys.executable, __file__, "--fase2", rom, out, savetype], capture_output=True, text=True, env=env)
    keep = lambda t: "\n".join(l for l in t.splitlines() if l.split(":")[0] in ("dsv no inicio", "quarto", "casa", "dsv depois de salvar",
                                                                               "depois (sem salvar)", "dsv depois de fechar", "dsv ao abrir")
                                or l.startswith(("FASE", "Traceback", "  File")) or "Error" in l)
    print(keep(r1.stdout + r1.stderr)); print(keep(r2.stdout + r2.stderr))
    f1 = [l for l in r1.stdout.splitlines() if l.startswith("FASE1")]
    f2 = [l for l in r2.stdout.splitlines() if l.startswith("FASE2")]
    ok = f1 and f2 and f1[-1].split(" ", 1)[1] == f2[-1].split(" ", 1)[1] and "None" not in f2[-1]
    print("RESULTADO CP-DS-02B:", "ok" if ok else "FALHOU")


if __name__ == "__main__":
    if sys.argv[1] == "--fase1":
        fase1(*sys.argv[2:4], int(sys.argv[4]))
    elif sys.argv[1] == "--fase2":
        fase2(*sys.argv[2:4], int(sys.argv[4]))
    else:
        main(*sys.argv[1:4])
