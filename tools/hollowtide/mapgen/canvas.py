#!/usr/bin/env python3
"""Canvas de composicao de mapas: terrenos com autotile aprendido + carimbos de predios dos mapas oficiais.

    c = Canvas(72, 56, "gTileset_General", "gTileset_Lilycove")
    c.fill("grass"); c.rect(0, 44, 71, 55, "sea"); c.ascii(10, 5, ["ss..", ...])
    c.stamp("lily_dept_store", 40, 30)
    c.save("PalmBreezeport")       # data/layouts/PalmBreezeport/map.bin (+ border.bin)
"""
import json, os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
from autotile import Autotiler, SECONDARY_CLASSES
import corpus as C

ROOT = C.ROOT
LEGEND = {"^": "high", ".": "grass", ",": "tall", "T": "tree", "D": "dense", "s": "sand", "x": "puddle", "p": "pond",
          "~": "sea", "=": "shallow", "v": "ledge_s", "<": "ledge_w", ">": "ledge_e", "f": "flower", "c": "cobble"}

# Carimbos: (layout de origem, x, y, largura, altura). Coordenadas levantadas com render_map --grid.
STAMPS = {
    "lily_dept_store": ("LAYOUT_LILYCOVE_CITY", 23, 0, 6, 7),
    "lily_contest_hall": ("LAYOUT_LILYCOVE_CITY", 20, 18, 7, 7),
    "lily_museum": ("LAYOUT_LILYCOVE_CITY", 7, 0, 10, 9),
    "lily_house_blue": ("LAYOUT_LILYCOVE_CITY", 11, 11, 4, 4),
    "lily_pokecenter": ("LAYOUT_LILYCOVE_CITY", 23, 11, 4, 4),
    "lily_motel": ("LAYOUT_LILYCOVE_CITY", 36, 20, 6, 5),
    "lily_harbor": ("LAYOUT_LILYCOVE_CITY", 9, 27, 7, 6),
    "lily_lamp": ("LAYOUT_LILYCOVE_CITY", 61, 33, 1, 2),
    "gen_mart": ("LAYOUT_PETALBURG_CITY", 24, 10, 4, 3),
    "gen_pokecenter": ("LAYOUT_PETALBURG_CITY", 19, 13, 4, 4),
}

_AT = {}
_REF = None


def _autotiler(primary, secondary):
    key = (primary, secondary)
    if key not in _AT:
        _AT[key] = Autotiler(primary, secondary=secondary, extra_classes=SECONDARY_CLASSES.get(secondary, {}))
    return _AT[key]


def _reference():
    global _REF
    if _REF is None:
        sys.path.insert(0, os.path.join(ROOT, "tools", "hollowtide_qa"))
        import fix_collision
        _REF = fix_collision.learn()
    return _REF


def extract(name):
    lay_id, x0, y0, w, h = STAMPS[name]
    L = next(l for l in C.layouts() if l["id"] == lay_id)
    return [[L["bl"][(y0 + y) * L["w"] + x0 + x] for x in range(w)] for y in range(h)], L["sec"]


class Canvas:
    def __init__(self, w, h, primary="gTileset_General", secondary="gTileset_Lilycove"):
        self.w, self.h, self.primary, self.secondary = w, h, primary, secondary
        self.terrain = [["grass"] * w for _ in range(h)]
        self.level = [[3] * w for _ in range(h)]  # 3 = chao, 5 = plato (independente do tipo de terreno)
        self.fixed = {}  # (x,y) -> valor de bloco completo (carimbos, pecas manuais)
        self.stair_cols = []  # (x, y_borda_sul_do_plato)

    def fill(self, cls):
        self.rect(0, 0, self.w - 1, self.h - 1, cls)

    def rect(self, x0, y0, x1, y1, cls, level=None):
        """cls "high" sobe um patamar (ou vai ao nivel indicado); demais classes so mudam o terreno."""
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                if cls == "high":
                    self.level[y][x] = level or 5
                    self.terrain[y][x] = "grass"
                else:
                    self.terrain[y][x] = cls

    def ascii(self, x0, y0, rows):
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch != " " and 0 <= x0 + dx < self.w and 0 <= y0 + dy < self.h:
                    if LEGEND[ch] == "high":
                        self.level[y0 + dy][x0 + dx] = 5
                        self.terrain[y0 + dy][x0 + dx] = "grass"
                    else:
                        self.terrain[y0 + dy][x0 + dx] = LEGEND[ch]

    def levels(self, x0, y0, rows):
        """Desenho de alturas: digitos 5/7/9 sobem o patamar (grama); ' ' ou '.' mantem."""
        for dy, r in enumerate(rows):
            for dx, ch in enumerate(r):
                if ch.isdigit() and 0 <= x0 + dx < self.w and 0 <= y0 + dy < self.h:
                    self.level[y0 + dy][x0 + dx] = int(ch)
                    if self.terrain[y0 + dy][x0 + dx] in ("grass", "dense", "tree"):
                        pass

    def stamp(self, name, x0, y0):
        blocks, sec = extract(name)
        assert sec == self.secondary or all((v & 0x3FF) < 512 for r in blocks for v in r), f"{name}: secundario {sec}"
        for dy, row in enumerate(blocks):
            for dx, v in enumerate(row):
                self.fixed[(x0 + dx, y0 + dy)] = v
                self.terrain[y0 + dy][x0 + dx] = "other"
        return (x0, y0, len(blocks[0]), len(blocks))

    def stairs(self, x, y_edge, width=1):
        """Escada atravessando a borda sul do plato (linha y_edge) e a parede dupla abaixo dela."""
        for dx in range(width):
            self.stair_cols.append((x + dx, y_edge))

    def fence_h(self, x0, x1, y):
        """Cerca horizontal do secundario Lilycove (592 ponta esq., 593 meio, 594 ponta dir.)."""
        for x in range(x0, x1 + 1):
            self.put(x, y, 592 if x == x0 else 594 if x == x1 else 593, collision=1)

    def lamp(self, x, y, floor="cobble", lit=True):
        """Poste composto (globo em cima, base embaixo) sobre o piso do lugar: cobble ou grass."""
        ids = json.load(open(os.path.join(os.path.dirname(__file__), "custom_ids.json")))["lilycove"]
        self.put(x, y, ids[f"lamp_top_{floor}_{'lit' if lit else 'unlit'}"], collision=0)
        self.put(x, y + 1, ids[f"lamp_base_{floor}"], collision=1, elevation=0)
        self.terrain[y][x] = self.terrain[y + 1][x] = floor  # vizinhos enxergam o piso, nao "outro"
        return ids

    def dept_store(self, x, y):
        """Loja de departamentos com cobertura (na Lilycove o telhado fica fora do mapa e nao existe no tileset):
        platibanda montada com o beiral do salao de concursos (mesma paleta)."""
        for dx, m in enumerate([704, 705, 705, 705, 705, 706]):
            self.put(x + dx, y, m, collision=1, elevation=0)
        for dx, m in enumerate([712, 713, 713, 713, 713, 714]):
            self.put(x + dx, y + 1, m, collision=1, elevation=0)
        return self.stamp("lily_dept_store", x, y + 2)

    def check_cohesion(self):
        """Arvores (desenhadas sobre grama) nao podem encostar em piso que nao seja vegetacao."""
        ok_nb = {"grass", "tree", "tall", "flower", "dense", "high", "cliff"}
        tree_mt = {468, 469, 476, 477}
        bad = []
        for (x, y), v in self.fixed.items():
            if v & 0x3FF in tree_mt:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h and (nx, ny) not in self.fixed and self.terrain[ny][nx] not in ok_nb:
                        bad.append((x, y, self.terrain[ny][nx]))
        return bad

    def small_tree(self, x, y):
        """Arvore de rua: arvore 2x2 padrao (468 469 / 476 477), solida."""
        for dy, row in enumerate(((468, 469), (476, 477))):
            for dx, m in enumerate(row):
                self.put(x + dx, y + dy, m, collision=1, elevation=0)

    def put(self, x, y, metatile, collision=None, elevation=3):
        self.fixed[(x, y)] = metatile | ((collision or 0) << 10) | (elevation << 12)
        self.terrain[y][x] = "other"

    def build(self):
        at = _autotiler(self.primary, self.secondary)
        col_ref, elev_ref = _reference()
        import fix_collision as FC
        grid = [[c if c != "other" else "grass" for c in row] for row in self.terrain]
        # patamares: grama acima do chao vira "high"; a borda de um patamar (vizinha de nivel menor) vira rocha
        lv = self.level
        for y in range(self.h):
            for x in range(self.w):
                if lv[y][x] > 3 and grid[y][x] == "grass":
                    grid[y][x] = "high"
        def lower(x, y, ref):
            return 0 <= x < self.w and 0 <= y < self.h and lv[y][x] < ref
        edge = [(x, y) for y in range(self.h) for x in range(self.w) if lv[y][x] > 3 and (x, y) not in self.fixed
                and any(lower(x + dx, y + dy, lv[y][x]) for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
        for x, y in edge:
            grid[y][x] = "cliff"
        # parede sul com 2 fileiras (leitura de altura do Emerald)
        for x, y in edge:
            if lower(x, y + 1, lv[y][x]) and (x, y + 1) not in self.fixed:
                grid[y + 1][x] = "cliff"
        stair_cells = set()
        for x, y in self.stair_cols:
            for yy in (y, y + 1):
                if 0 <= yy < self.h:
                    stair_cells.add((x, yy))
        out = []
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in self.fixed:
                    out.append(self.fixed[(x, y)])
                    continue
                if (x, y) in stair_cells:
                    out.append(175 | (0 << 10) | (0 << 12))  # escada: elevacao 0 liga os niveis 3 e 5
                    continue
                if grid[y][x] == "tree":  # arvore 2x2 alinhada a grade par (padrao das rotas classicas)
                    m = ((468, 469), (476, 477))[y & 1][x & 1]
                else:
                    m, _ = at.tile(grid, x, y)
                ts = self.primary if m < 512 else self.secondary
                c = FC.dominant(col_ref[(ts, m)])
                e = FC.dominant(elev_ref[(ts, m)])
                if grid[y][x] == "high":
                    c, e = 0, lv[y][x]
                elif lv[y][x] > 3 and grid[y][x] != "cliff" and e is not None and e == 3:
                    e = lv[y][x]  # terreno sobre o patamar herda a elevacao
                out.append(m | ((c or 0) << 10) | ((e if e is not None else 3) << 12))
        return out

    def save(self, folder, border=(1, 1, 1, 1)):
        d = f"{ROOT}/data/layouts/{folder}"
        os.makedirs(d, exist_ok=True)
        bl = self.build()
        open(f"{d}/map.bin", "wb").write(struct.pack(f"<{len(bl)}H", *bl))
        open(f"{d}/border.bin", "wb").write(struct.pack("<4H", *[b | (3 << 12) for b in border]))
        return bl
