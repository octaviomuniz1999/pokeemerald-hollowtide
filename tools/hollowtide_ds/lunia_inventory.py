#!/usr/bin/env python3
"""Inventario de Lunia a partir do GBA congelado (23ap): o que a versao DS precisa portar.

O GBA reaproveitou mapas e treinadores de Hoenn, entao "o que e de Lunia" sai de um percurso no grafo do mundo:
comeca no quarto do jogador (Dawnmere) e segue conexoes, warps e warps de script (warp/warpsilent/... MAP_X).
De cada mapa alcancado: treinadores citados nos scripts (trainerbattle*), encontros selvagens e presentes/trocas
(givemon/ingame trade). Saida: JSON (padrao docs/hollowtide/ds/lunia_inventory.json) + resumo no terminal.

Uso: lunia_inventory.py [SAIDA.json]
"""
import glob, json, os, re, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
START = "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F"
# ligacoes de Hoenn que sobraram nos mapas reaproveitados e nao fazem parte de Lunia: a Ever Grande City (fachada da
# Liga, ligada a Route 11) ainda tem a entrada da Victory Road e a conexao com a Route 128 do Emerald; no canone a
# Route 11 leva direto a Liga e nao ha rival (DECISOES: "Sem rival").
EXCLUDE_PREFIX = ("MAP_VICTORY_ROAD", "MAP_ROUTE128")
SHARED_SCRIPTS = ["data/scripts/hollowtide_gifts.inc", "data/scripts/hollowtide_trades.inc"]
RE_WARP = re.compile(r"\b(?:warp|warpsilent|warpdoor|warphole|warpteleport|warpspinenter|setwarp|setdynamicwarp|"
                     r"setescapewarp|setdivewarp|setholewarp|warpmossdeepgym|warpwhitefade)\s+(MAP_[A-Z0-9_]+)")
RE_TRAINER = re.compile(r"\btrainerbattle\w*\s+(TRAINER_[A-Z0-9_]+)")
RE_GIVEMON = re.compile(r"\bgivemon\s+(SPECIES_[A-Z0-9_]+)\s*,\s*(\d+)")


def load_maps():
    maps = {}
    for f in glob.glob(os.path.join(REPO, "data/maps/*/map.json")):
        j = json.load(open(f))
        j["_dir"] = os.path.dirname(f)
        maps[j["id"]] = j
    return maps


def script_text(m):
    p = os.path.join(m["_dir"], "scripts.inc")
    return open(p).read() if os.path.exists(p) else ""


def walk(maps):
    seen, todo = set(), [START]
    while todo:
        mid = todo.pop()
        if mid in seen or mid not in maps or mid.startswith(EXCLUDE_PREFIX):
            continue
        seen.add(mid)
        m = maps[mid]
        nxt = [c["map"] for c in (m.get("connections") or [])]
        nxt += [w["dest_map"] for w in m.get("warp_events", [])]
        nxt += RE_WARP.findall(script_text(m))
        todo += [n for n in nxt if n not in seen and n != "MAP_DYNAMIC"]
    return seen


def parse_party():
    out, cur = {}, None
    for line in open(os.path.join(REPO, "src/data/trainers.party")):
        line = line.rstrip("\n")
        if line.startswith("=== TRAINER_"):
            cur = line.strip("= ").strip()
            out[cur] = {"fields": {}, "party": []}
            mon = None
            continue
        if cur is None:
            continue
        t = out[cur]
        if not line.strip():
            mon = None
            continue
        if mon is None and ":" in line and not t["party"] and not line.startswith("-") and \
                line.split(":")[0] in ("Name", "Class", "Pic", "Gender", "Music", "Items", "Battle Type", "AI",
                                       "Mugshot", "Starting Status", "Double Battle", "Party Size", "Multi Party"):
            k, v = line.split(":", 1)
            t["fields"][k.strip()] = v.strip()
            continue
        if mon is None:
            mon = {"head": line.strip(), "lines": []}
            t["party"].append(mon)
        else:
            mon["lines"].append(line.strip())
    return out


def trainer_aliases():
    """include/constants/opponents.h: #define TRAINER_PALM_X TRAINER_Y (slots de Hoenn reaproveitados)."""
    al = {}
    for line in open(os.path.join(REPO, "include/constants/opponents.h")):
        m = re.match(r"#define\s+(TRAINER_\w+)\s+(TRAINER_[A-Z]\w*)\s*(//.*)?$", line.strip())
        if m:
            al[m.group(1)] = m.group(2)
    return al


def species_of(head):
    """'Nick (Snivy) (M) @ Item' / 'Snivy @ Item' / 'SPECIES_SNIVY' -> nome da especie como escrito."""
    h = head.split("@")[0].strip()
    h = re.sub(r"\s*\((M|F)\)\s*$", "", h)
    m = re.search(r"\(([^()]+)\)\s*$", h)
    return (m.group(1) if m else h).strip()


def main(out):
    maps = load_maps()
    lunia = sorted(walk(maps))
    party = parse_party()
    trainers, gifts = {}, []
    texts = {mid: script_text(maps[mid]) for mid in lunia}
    for p in SHARED_SCRIPTS:
        texts[p] = open(os.path.join(REPO, p)).read()
    for src, txt in texts.items():
        for t in RE_TRAINER.findall(txt):
            trainers.setdefault(t, set()).add(src)
        for sp, lv in RE_GIVEMON.findall(txt):
            gifts.append({"species": sp, "level": int(lv), "where": src})
    # treinadores de objetos com visao (trainer_type) cujo script chama trainerbattle ja entram acima
    w = json.load(open(os.path.join(REPO, "src/data/wild_encounters.json")))
    enc = []
    for g in w["wild_encounter_groups"]:
        for e in g["encounters"]:
            if e.get("map") in lunia:
                row = {"map": e["map"], "base_label": e.get("base_label")}
                for kind in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
                    if kind in e:
                        row[kind] = e[kind]
                enc.append(row)
    tr_out, al = {}, trainer_aliases()
    for t in sorted(trainers):
        slot = t
        while slot in al and slot not in party:
            slot = al[slot]
        p = party.get(slot)
        tr_out[t] = {"slot": slot, "maps": sorted(trainers[t]), "fields": p["fields"] if p else None,
                     "party": [{"species": species_of(m["head"]), "head": m["head"], "lines": m["lines"]}
                               for m in (p["party"] if p else [])]}
    species = set()
    for t in tr_out.values():
        species |= {m["species"] for m in t["party"]}
    for e in enc:
        for kind in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
            species |= {m["species"] for m in e.get(kind, {}).get("mons", [])}
    species |= {g["species"] for g in gifts}
    res = {"start": START, "maps": lunia, "trainers": tr_out, "encounters": enc, "gifts": gifts,
           "species": sorted(species)}
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"mapas {len(lunia)} | treinadores {len(tr_out)} (sem time no .party: "
          f"{sum(1 for t in tr_out.values() if not t['party'])}) | tabelas de encontro {len(enc)} | "
          f"presentes {len(gifts)} | especies (nomes crus) {len(species)} -> {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "docs/hollowtide/ds/lunia_inventory.json"))
