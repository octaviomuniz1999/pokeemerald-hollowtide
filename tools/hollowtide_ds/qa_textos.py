#!/usr/bin/env python3
"""CP-DS-02: teste dirigido dos dois textos decididos pelo diretor em 24/11 (o percurso dos QAs nao passa por eles).
1. livro do laboratorio (estante 11-12,10; script T20R0101_008, texto 543/96), a partir do estado do quarto;
2. menino da loja em Breezeport (objeto em 286,259; script T26_011, texto 604/10), a partir do estado de Breezeport.
Cada pagina de fala vira captura (QA_FALAS). Uso: qa_textos.py ROM ESTADO_QUARTO ESTADO_BREEZEPORT PASTA
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
from qa_cap1 import walk, advance, goto, face
from qa_cap2 import bz


def main(rom, room, breeze, out):
    """Duas execucoes do Python (o DeSmuME nao abre dois emuladores no mesmo processo)."""
    import subprocess
    for part in ("--livro", "--loja"):
        r = subprocess.run([sys.executable, __file__, part, rom, room, breeze, out], capture_output=True, text=True)
        print("\n".join(l for l in r.stdout.splitlines() if l.split(":")[0] in ("laboratorio", "livro lido em", "menino da loja")))


def livro(rom, room, breeze, out):
    os.environ.setdefault("QA_FALAS", os.path.join(out, "falas"))
    os.makedirs(out, exist_ok=True)
    d = DS(rom); d.load(room); d.wait(30)
    walk(d, ["UP", "UP", "LEFT", "LEFT", "LEFT", "UP", "LEFT", "LEFT"]); d.wait(200)
    advance(d, 45); d.wait(60)
    walk(d, ["DOWN"] * 8); d.wait(200); advance(d, 10)
    walk(d, ["DOWN"] + ["LEFT"] * 20, stop_map=33); d.wait(60); advance(d, 8); d.wait(60)
    x = d.where()[1]
    walk(d, ["RIGHT"] * (684 - x) + ["UP"] * 6, stop_map=61); d.wait(200)
    print("laboratorio:", d.where())
    goto(d, rom, (11, 11), [(0, 0)], 61, out, "lab", avoid={(6, 5), (9, 12)}, matrix=100)
    face(d, "UP"); d.press("A", 4, 90); d.shot(f"{out}/1_livro.png"); advance(d, 6)
    print("livro lido em:", d.where())


def loja(rom, room, breeze, out):
    os.makedirs(out, exist_ok=True)
    d = DS(rom); d.load(breeze); d.wait(30)
    bz(d, rom, out, (286, 260), "bz")
    face(d, "UP"); d.press("A", 4, 90); d.shot(f"{out}/2_menino_da_loja.png"); advance(d, 6)
    print("menino da loja:", d.where())


if __name__ == "__main__":
    if sys.argv[1] in ("--livro", "--loja"):
        os.environ.setdefault("QA_FALAS", os.path.join(sys.argv[5], "falas"))
        (livro if sys.argv[1] == "--livro" else loja)(*sys.argv[2:6])
    else:
        main(*sys.argv[1:5])
