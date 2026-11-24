#!/usr/bin/env python3
"""Onde o desenho global de Lunia fica na matriz 0 (CP-DS-03B): lido do land.json da pasta de conteudo, para que
eventos, ponte, atalho de QA e robos de QA usem a mesma origem. Coordenada de mundo = origem + tile do desenho."""
import json, os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_E = next(e for e in json.load(open(os.path.join(REPO, "hollowtide_ds/patches/content/land.json"))) if "global" in e)
CELULA = tuple(_E["celula"])
X0, Z0 = CELULA[0] * 32, CELULA[1] * 32
_G = os.path.normpath(os.path.join(REPO, "hollowtide_ds/patches/content", _E["global"]))
_L = open(_G).read().split("\n")
W, H = map(int, _L[_L.index("[tamanho]") + 1].split())
CELLS = [(CELULA[0] + bx, CELULA[1] + by) for bx in range(W // 32) for by in range(H // 32)]
GRADE = _G


def g(x, z):
    """Tile do desenho global -> coordenada de mundo."""
    return (X0 + x, Z0 + z)


ORIGENS = {k: tuple(v["origem"]) for k, v in json.load(open(_G + ".json")).items()}   # mapa do GBA -> canto no desenho


def gba(mapa, x, y):
    """Tile (x, y) do mapa do GBA (Dawnmere, Route1, Harvestvale, Route2) -> coordenada de mundo."""
    ox, oy = ORIGENS[mapa]
    return (X0 + ox + x, Z0 + oy + y)


def D(x, y): return gba("Dawnmere", x, y)
def R1(x, y): return gba("Route1", x, y)
def HV(x, y): return gba("Harvestvale", x, y)
def R2(x, y): return gba("Route2", x, y)
