#!/usr/bin/env python3
"""Encontros de Lunia (GBA 23ap) -> data/Encounters.c do hg-engine (patch de conteudo do Hollowtide DS).

Cada tabela do GBA vai para a tabela ENCDATA do mapa de HGSS que hospeda aquele lugar de Lunia (caminho A),
definido em hollowtide_ds/data/map_bindings.json ({"MAP_PALM_ROUTE02": {"encdata": "ENCDATA_..."}}; a Fase 2
preenche). Sem ligacao, a tabela e so validada (constantes de especie) e fica de fora do patch.

Conversao (23/11/2026):
- Grama: as 12 vagas tem as mesmas chances no GBA e no DS (20/20/10/10/10/10/5/5/4/4/1/1); o DS tem um nivel por
  vaga -> meio da faixa do GBA, arredondado para cima. Manha, dia e noite iguais (o GBA nao tem horario; nada
  e inventado).
- Surf: 5 vagas com as mesmas chances (60/30/5/4/1), faixa de nivel igual.
- Pesca: Old Rod do GBA (70/30) nas 5 vagas do DS (60/30/5/4/1) -> 0,1,0,0,0 = 70/30 exato; Super Rod (40/40/15/4/1)
  igual nos dois; Good Rod (60/20/20) nao cabe nas vagas do DS (40/40/15/4/1) -> 0,1,2,0,0 = 45/40/15.
- Taxas (rateWalk, rateSurf, varas) copiadas do GBA; varas sem tabela ficam 0.
Uso: convert_encounters.py HG_ENGINE [LIGACOES.json PATCH_DE_SAIDA]  (os dois opcionais servem as provas)
"""
import json, os, re, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BIND = os.path.join(REPO, "hollowtide_ds/data/map_bindings.json")
PATCH = os.path.join(REPO, "hollowtide_ds/patches/content/0200-encounters.patch")
OLD_MAP, GOOD_MAP, SUPER_MAP = [0, 1, 0, 0, 0], [2, 3, 4, 2, 2], [5, 6, 7, 8, 9]   # indices nas 10 vagas de pesca do GBA


def species_c(valid, s):
    k = s
    for a, b in (("_HISUI", "_HISUIAN"), ("_ALOLA", "_ALOLAN"), ("_GALAR", "_GALARIAN"), ("_PALDEA", "_PALDEAN")):
        if k.endswith(a):
            k = k[: -len(a)] + b
    if k not in valid:
        raise KeyError(f"especie sem constante no hg-engine: {s}")
    return k


def entry(valid, enc, encdata):
    land = enc.get("land_mons", {}).get("mons", [])
    water = enc.get("water_mons", {}).get("mons", [])
    fish = enc.get("fishing_mons", {}).get("mons", [])
    rate = lambda k: enc.get(k, {}).get("encounter_rate", 0)
    o = [f"    [{encdata}] = {{  // Hollowtide: {enc['map']}",
         f"        .rateWalk = {rate('land_mons') if land else 0},",
         f"        .rateSurf = {rate('water_mons') if water else 0},",
         "        .rateRockSmash = 0,"]
    fr = rate("fishing_mons") if fish else 0
    o += [f"        .rateOldRod = {fr},", f"        .rateGoodRod = {fr},", f"        .rateSuperRod = {fr},"]
    lv = [(m["min_level"] + m["max_level"] + 1) // 2 for m in land] or [0] * 12
    sp = [species_c(valid, m["species"]) for m in land] or ["SPECIES_NONE"] * 12
    o += ["        .landSlots = {", "            .levels = {", "                " + ", ".join(map(str, lv)), "            },"]
    for t in ("speciesMorning", "speciesDay", "speciesNight"):
        o += [f"            .{t} = {{"] + [f"                {s}," for s in sp] + ["            },"]
    o.append("        },")
    o += ["        .hoennSoundSpecies = { SPECIES_NONE, SPECIES_NONE },",
          "        .sinnohSoundSpecies = { SPECIES_NONE, SPECIES_NONE },"]

    def slots(name, mons, idx):
        rows = []
        for i in idx:
            if mons:
                m = mons[i]
                rows.append(f"            {{ {m['min_level']}, {m['max_level']}, {species_c(valid, m['species'])} }},")
            else:
                rows.append("            { 0, 0, SPECIES_NONE },")
        return [f"        .{name} = {{"] + rows + ["        },"]
    o += slots("surfSlots", water, range(5))
    o += ["        .rockSmashSlots = {", "            { 0, 0, SPECIES_NONE },", "            { 0, 0, SPECIES_NONE },", "        },"]
    o += slots("oldRodSlots", fish, OLD_MAP) + slots("goodRodSlots", fish, GOOD_MAP) + slots("superRodSlots", fish, SUPER_MAP)
    o += ["        .landSwarm = SPECIES_NONE,", "        .surfSwarm = SPECIES_NONE,", "        .nightFish = SPECIES_NONE,",
          "        .fishSwarm = SPECIES_NONE,", "    },"]
    return "\n".join(o) + "\n"


def main(hg, bind_path=BIND, patch_path=PATCH):
    valid = set(re.findall(r"#define\s+(SPECIES_[A-Z0-9_]+)\b", open(os.path.join(hg, "include/constants/species.h")).read()))
    inv = json.load(open(os.path.join(REPO, "docs/hollowtide/ds/lunia_inventory.json")))
    bind = json.load(open(bind_path)) if os.path.exists(bind_path) else {}
    orig = subprocess.run(["git", "-C", hg, "show", "HEAD:data/Encounters.c"], capture_output=True, text=True, check=True).stdout
    new, done, unbound = orig, [], []
    for enc in inv["encounters"]:
        text = entry(valid, enc, "X")                      # valida mesmo sem ligacao
        b = bind.get(enc["map"], {}).get("encdata")
        if not b:
            unbound.append(enc["map"]); continue
        m = re.search(r"\n    \[%s\] = \{\n.*?\n    \},\n" % re.escape(b), new, re.S)
        if not m:
            raise KeyError(f"{b} nao existe em data/Encounters.c")
        new = new[:m.start() + 1] + entry(valid, enc, b) + new[m.end():]
        done.append(enc["map"])
    if done:
        with tempfile.TemporaryDirectory() as tmp:
            a, c = os.path.join(tmp, "a"), os.path.join(tmp, "b")
            open(a, "w").write(orig); open(c, "w").write(new)
            p = subprocess.run(["diff", "-u", "--label", "a/data/Encounters.c", "--label", "b/data/Encounters.c", a, c],
                               capture_output=True, text=True).stdout
        open(patch_path, "w").write(p)
    elif os.path.exists(patch_path):
        os.remove(patch_path)
    print(f"tabelas validadas: {len(inv['encounters'])}; no patch: {len(done)}; sem mapa de HGSS ainda: {len(unbound)}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
