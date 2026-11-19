#!/usr/bin/env python3
"""Autotile aprendido dos mapas oficiais.

Cada classe de terreno e um conjunto de metatiles. O corpus (mapas upstream com o mesmo tileset primario) e
rotulado por classe; para cada bloco registramos chaves de vizinhanca cada vez mais grosseiras e o metatile
usado. Para gerar, consultamos da chave mais especifica para a mais grosseira.
"""
import collections, os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
import corpus as C

N8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
N4 = [(0, -1), (-1, 0), (1, 0), (0, 1)]

# Classes do tileset General (primario). Conjuntos levantados por comportamento + folha de metatiles.
SECONDARY_CLASSES = {
    "gTileset_Lilycove": {"cobble": {554, 555, 556, 562, 563, 564, 570, 571, 572}},
    # Rustboro: piso de praca bege e avenidas de 2 tiles (bordas superior/inferior, laterais, cruzamento 94)
    "gTileset_Rustboro": {"plaza": {699}, "road": {760, 761, 762, 776, 777, 778, 768, 770, 94}},
}

GENERAL_CLASSES = {
    "grass": {1},
    "tall": {13},
    "tree": {468, 469, 476, 477, 484, 485, 486, 487, 492, 493, 500, 501, 508, 509},
    "dense": {198, 199, 206},
    "sand": {280, 281, 282, 288, 289, 290, 296, 297, 298, 292},
    "puddle": {200, 201, 202, 208, 209, 210, 216, 217, 218},
    "pond": {152, 153, 154, 161, 176, 177, 178, 184, 186, 192, 194, 195, 196, 203, 204},
    "sea": {44, 52, 53, 60, 84, 193, 283, 285, 291, 293, 299, 300, 301, 325, 326, 368, 369, 370, 372, 376, 377,
            384, 385, 392, 393, 394, 400, 402, 403, 408, 409, 410, 419, 420, 429, 431, 437, 439, 445, 446},
    "shallow": {315, 316, 323, 324, 343, 350, 351, 358, 359, 366, 367, 389, 390, 397, 398, 405, 406, 407, 411,
                412, 413, 414, 415, 421, 422, 423, 430, 506, 507},
    "ledge_s": {135, 143, 151, 213, 214, 221, 222, 229, 230},
    "ledge_w": {133, 149, 165, 254, 262, 270, 278, 286, 294},
    "ledge_e": {134, 150, 166, 255, 263, 271, 279, 287, 295},
    "flower": {4},
    # faces de rocha entre grama baixa (elev. 3) e plato (elev. 5), descobertas no corpus
    "cliff": {104, 106, 110, 111, 112, 114, 115, 116, 117, 120, 121, 122, 123, 124, 125, 136, 137, 145},
    "high": set(),  # grama de plato: metatile 1 com elevacao 5 (rotulada pelo valor completo)
}


class Autotiler:
    def __init__(self, primary="gTileset_General", classes=GENERAL_CLASSES, secondary=None, extra_classes=None):
        classes = dict(classes)
        classes.update(extra_classes or {})
        self.classes = classes
        self.secondary = secondary
        self.cls_of = {}
        for c, s in classes.items():
            for m in s:
                self.cls_of[m] = c
        self.tables = [collections.defaultdict(collections.Counter) for _ in range(5)]
        for L in C.maps_with(primary):
            self._learn(L)

    def _cls(self, m, sec=None):
        if (m & 0x3FF) == 1 and (m >> 12) == 5:
            return "high"
        m &= 0x3FF
        if m >= 512 and (self.secondary is None or sec != self.secondary):
            return "other"
        return self.cls_of.get(m, "other")

    def _keys(self, get, x, y):
        c = get(x, y)
        n8 = tuple(get(x + dx, y + dy) for dx, dy in N8)
        n4 = tuple(get(x + dx, y + dy) for dx, dy in N4)
        b8 = tuple(v == c for v in n8)
        b4 = tuple(v == c for v in n4)
        par = (x & 1, y & 1)
        return [(c, n8, par), (c, n8), (c, n4), (c, b8), (c, b4)]

    def _learn(self, L):
        w, h, b = L["w"], L["h"], L["bl"]
        cls = [self._cls(v, L["sec"]) for v in b]
        def get(x, y):
            return cls[y * w + x] if 0 <= x < w and 0 <= y < h else None
        for y in range(h):
            for x in range(w):
                if cls[y * w + x] == "other":
                    continue
                m = b[y * w + x] & 0x3FF
                for t, k in zip(self.tables, self._keys(get, x, y)):
                    t[k][m] += 1

    def tile(self, grid, x, y):
        """grid: lista de linhas de classes (strings de nomes). Retorna (metatile, nivel_de_chave_usado)."""
        h, w = len(grid), len(grid[0])
        def get(xx, yy):
            if 0 <= xx < w and 0 <= yy < h:
                return grid[yy][xx]
            return grid[min(max(yy, 0), h - 1)][min(max(xx, 0), w - 1)]  # borda: estende o terreno
        for lvl, (t, k) in enumerate(zip(self.tables, self._keys(get, x, y))):
            if k in t:
                return t[k].most_common(1)[0][0], lvl
        c = grid[y][x]
        return (1 if c == "high" else min(self.classes[c])), 9


if __name__ == "__main__":
    a = Autotiler()
    print({i: len(t) for i, t in enumerate(a.tables)})
