#!/usr/bin/env python3
"""Gera blocos de mapa a partir de uma grade ASCII de terrenos usando o autotile aprendido.
Legenda: . grama  , mato alto  T arvore  D mata densa  s areia  x poca  p lago  ~ mar  = agua rasa
         v ladeira sul  < ladeira oeste  > ladeira leste  f flores
"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
from autotile import Autotiler

LEGEND = {".": "grass", ",": "tall", "T": "tree", "D": "dense", "s": "sand", "x": "puddle", "p": "pond",
          "~": "sea", "=": "shallow", "v": "ledge_s", "<": "ledge_w", ">": "ledge_e", "f": "flower"}
_AT = None


def autotiler():
    global _AT
    if _AT is None:
        _AT = Autotiler()
    return _AT


def ascii_to_blocks(rows, elevation=3):
    grid = [[LEGEND[c] for c in r] for r in rows]
    at = autotiler()
    out, stats = [], [0] * 10
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            m, lvl = at.tile(grid, x, y)
            stats[lvl] += 1
            out.append(m | (elevation << 12))
    return out, stats


def write_bin(path, blocks):
    open(path, "wb").write(struct.pack(f"<{len(blocks)}H", *blocks))
