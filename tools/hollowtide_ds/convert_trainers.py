#!/usr/bin/env python3
"""Times de Lunia (GBA 23ap) -> data/Trainers.c do hg-engine, como patch de conteudo do Hollowtide DS.

Entrada: docs/hollowtide/ds/lunia_inventory.json (lunia_inventory.py) e os scripts dos mapas do GBA (falas).
Saida:
- hollowtide_ds/patches/content/0100-trainers.patch: entradas de data/Trainers.c substituidas (slots de HGSS
  reaproveitados) e o novo data/scr_seq/include/hollowtide_trainers.inc (.equ TRAINER_HT_<SLOT_DO_GBA>, indice);
- hollowtide_ds/data/trainer_slots.json: slot do GBA -> indice no DS. So cresce: um treinador nunca muda de indice
  (os flags de "treinador vencido" e os scripts dependem dele).

Regras (Fase 1, 23/11/2026):
- Indices a partir de FIRST_SLOT (400): sobrescreve treinadores de HGSS (o mundo de Johto/Kanto sai na Fase 2;
  usar indices novos passaria da faixa fixa de flags de treinador).
- Classe (sprite e titulo na batalha): a do campo Class do GBA quando ha equivalente (Leader/Elite Four/Champion ->
  classe de lider/Elite/campeao de HGSS, titulo certo), senao pelo Pic; sprites sao placeholders oficiais ate a arte.
- IVs iguais nos 6 -> campo .ivs (0-255); diferentes -> IV_EV_SET. Habilidade: se for a 1, 2 ou oculta da especie,
  so o slot; senao TRAINER_DATA_TYPE_ABILITY (e a 1a habilidade nos outros do time).
- IA: lideres, Elite, campeoes e chefes da Team Palm com IA de especialista (DECISOES: "IA inteligente nos lideres").
Uso: convert_trainers.py HG_ENGINE
"""
import json, os, re, subprocess, sys, tempfile, unicodedata

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIRST_SLOT = 400
SLOTS = os.path.join(REPO, "hollowtide_ds/data/trainer_slots.json")
PATCH = os.path.join(REPO, "hollowtide_ds/patches/content/0100-trainers.patch")
INC = "data/scr_seq/include/hollowtide_trainers.inc"

PIC_CLASS = {
    "Cooltrainer F": "ACE_TRAINER_F", "Cooltrainer M": "ACE_TRAINER_M", "Aqua Grunt M": "TEAM_ROCKET",
    "Aqua Grunt F": "TEAM_ROCKET_F", "Beauty": "BEAUTY", "Hiker": "HIKER", "Youngster": "YOUNGSTER", "Lass": "LASS",
    "Guitarist": "GUITARIST", "Picnicker": "PICNICKER", "Fisherman": "FISHERMAN", "Camper": "CAMPER",
    "Psychic M": "PSYCHIC_M", "Psychic F": "PSYCHIC_F", "Ruin Maniac": "RUIN_MANIAC", "Swimmer F": "SWIMMER_F",
    "Swimmer M": "SWIMMER_M", "Pokefan F": "POKEFAN", "Pokefan M": "POKEFAN_M", "Lady": "LADY", "Expert M": "VETERAN",
    "Hex Maniac": "MEDIUM", "Black Belt": "BLACK_BELT", "Battle Girl": "BATTLE_GIRL", "Sailor": "SAILOR",
    "Bug Catcher": "BUG_CATCHER", "Aroma Lady": "AROMA_LADY", "Bird Keeper": "BIRD_KEEPER", "Tuber F": "TUBER_F",
    "Pokemon Ranger M": "PKMN_RANGER_M", "Pokemon Ranger F": "PKMN_RANGER_F", "Pokemon Breeder F": "PKMN_BREEDER_F",
    "Aqua Admin F": "EXECUTIVE_ARIANA", "Aqua Admin M": "EXECUTIVE_ARCHER", "Aqua Leader Archie": "ROCKET_BOSS",
    "Champion Cynthia": "CHAMPION_CYNTHIA", "Red": "PKMN_TRAINER_RED",
}
# titulo certo na batalha para lideres/Elite/campeao: classe de HGSS do mesmo papel, sprite mais proximo do tipo
NAME_CLASS = {
    "NEVARD": "LEADER_BUGSY", "JAY": "LEADER_FANTINA", "VESSEL": "LEADER_BYRON", "TCHUM": "LEADER_BROCK",
    "JADE": "LEADER_SABRINA", "CHELSIA": "LEADER_WHITNEY", "HOC": "LEADER_LT_SURGE", "NAMI": "LEADER_MISTY",
    "PKAS": "ELITE_FOUR_BRUNO", "ANGELIC": "ELITE_FOUR_KOGA", "RIVEN": "ELITE_FOUR_WILL", "DU": "ELITE_FOUR_BRUNO",
    "DOGE": "CHAMPION",
}
EXPERT_CLASSES = {"Leader", "Elite Four", "Champion", "Aqua Leader", "Aqua Admin"}
AI = {"Basic Trainer": "F_PRIORITIZE_SUPER_EFFECTIVE | F_EVALUATE_ATTACKS",
      "Check Bad Move": "F_PRIORITIZE_SUPER_EFFECTIVE | F_EVALUATE_ATTACKS"}
STATS = ["HP", "Atk", "Def", "Spe", "SpA", "SpD"]           # ordem do TrainerPokemonEVIV
EVIV_FIELDS = ["hp", "attack", "defense", "speed", "spAttack", "spDefense"]


def ckey(name):
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    n = n.replace("♀", "_F").replace("♂", "_M")
    return re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_").upper()


class Consts:
    def __init__(self, hg):
        def grab(path, prefix):
            return set(re.findall(r"#define\s+(%s[A-Z0-9_]+)\b" % prefix, open(os.path.join(hg, path)).read()))
        self.species = grab("include/constants/species.h", "SPECIES_")
        self.moves = grab("include/constants/moves.h", "MOVE_")
        self.items = grab("include/constants/item.h", "ITEM_")
        self.abilities = grab("include/constants/ability.h", "ABILITY_")
        self.classes = set(re.findall(r"(TRAINERCLASS_[A-Z0-9_]+)", open(os.path.join(hg, "include/constants/trainerclass.h")).read()))
        sp = open(os.path.join(hg, "data/Species.c"), encoding="utf-8").read()
        self.abil = {}
        for m in re.finditer(r"\[(SPECIES_[A-Z0-9_]+)\s*\]\s*=\s*\{(.*?)\n    \},", sp, re.S):
            a = re.search(r"\.abilities\s*=\s*\{\s*(\w+)\s*,\s*(\w+)\s*\}", m.group(2))
            if a:
                self.abil[m.group(1)] = [a.group(1), a.group(2)]
        ha = open(os.path.join(hg, "data/HiddenAbilityTable.c"), encoding="utf-8").read()
        self.hidden = dict(re.findall(r"\[(SPECIES_[A-Z0-9_]+)\s*\]\s*=\s*(ABILITY_\w+)", ha))

    def species_c(self, name):
        k = ckey(name)
        for a, b in (("_HISUI", "_HISUIAN"), ("_ALOLA", "_ALOLAN"), ("_GALAR", "_GALARIAN"), ("_PALDEA", "_PALDEAN")):
            if k.endswith(a):
                k = k[: -len(a)] + b
        c = "SPECIES_" + k
        if c not in self.species:
            raise KeyError(f"especie sem constante no hg-engine: {name} ({c})")
        return c

    def one(self, kind, prefix, name):
        c = prefix + ckey(name)
        if c not in getattr(self, kind):
            raise KeyError(f"{kind}: {name} ({c})")
        return c


PLAYER_TEXTS = []


def gba_text(maps_txt, label):
    m = re.search(r"^%s::?\s*\n((?:\s*\.string\s+\"(?:[^\"\\]|\\.)*\"\s*\n?)+)" % re.escape(label), maps_txt, re.M)
    if not m:
        return None
    s = "".join(re.findall(r"\.string\s+\"((?:[^\"\\]|\\.)*)\"", m.group(1)))
    s = s.rstrip("$")
    if "{PLAYER}" in s:                 # buffer 0 = nome do jogador (o script precisa de buffer_players_name 0)
        PLAYER_TEXTS.append(label)
        s = s.replace("{PLAYER}", "{STRVAR_1 3, 0, 0}")
    if re.search(r"\{(?!STRVAR_1 3, 0, 0\})", s):
        raise ValueError(f"codigo de texto do GBA sem equivalente ainda: {label}: {s}")
    s = s.replace("\\n", "\\\\n").replace("\\l", "\\\\r").replace("\\p", "\\\\f").replace('"', '\\"')
    return s


def battle_texts(inv_tr, scripts):
    """trainerbattle_single T, Intro, Defeat [+ msgbox After logo depois]; trainerbattle_no_intro T, Defeat."""
    out = {}
    for src, txt in scripts.items():
        lines = txt.splitlines()
        for i, l in enumerate(lines):
            m = re.match(r"\s*trainerbattle_(single|no_intro)\s+(TRAINER_\w+)\s*,\s*(\w+)(?:\s*,\s*(\w+))?", l)
            if not m or m.group(2) not in inv_tr:
                continue
            kind, t = m.group(1), m.group(2)
            intro, defeat = (m.group(3), m.group(4)) if kind == "single" else (None, m.group(3))
            after = None
            if i + 1 < len(lines):
                a = re.match(r"\s*msgbox\s+(\w+)", lines[i + 1])
                after = a.group(1) if a else None
            out.setdefault(t, {"intro": gba_text(txt, intro) if intro else None,
                               "defeat": gba_text(txt, defeat) if defeat else None,
                               "after": gba_text(txt, after) if after else None})
    return out


def mon_entry(C, mon):
    sp = C.species_c(mon["species"])
    d = {"species": sp, "moves": [], "item": "ITEM_NONE", "ability": None, "ivs": None, "level": None}
    if "@" in mon["head"]:
        d["item"] = C.one("items", "ITEM_", mon["head"].split("@", 1)[1].strip())
    for l in mon["lines"]:
        if l.startswith("- "):
            d["moves"].append(C.one("moves", "MOVE_", l[2:].strip()))
        elif l.startswith("Level:"):
            d["level"] = int(l.split(":")[1])
        elif l.startswith("Ability:"):
            d["ability"] = C.one("abilities", "ABILITY_", l.split(":", 1)[1].strip())
        elif l.startswith("IVs:"):
            iv = {s: 31 for s in STATS}
            for part in l.split(":", 1)[1].split("/"):
                v, s = part.split()
                iv[s] = int(v)
            d["ivs"] = [iv[s] for s in STATS]
        else:
            raise ValueError(f"linha do time nao tratada: {l}")
    return d


def build_entry(C, idx, gba_slot, tr, texts):
    f = tr["fields"]
    mons = [mon_entry(C, m) for m in tr["party"]]
    flags = ["TRAINER_DATA_TYPE_MOVES"] if any(m["moves"] for m in mons) else []
    if any(m["item"] != "ITEM_NONE" for m in mons):
        flags.append("TRAINER_DATA_TYPE_ITEMS")
    need_iv = any(m["ivs"] and len(set(m["ivs"])) > 1 for m in mons)
    if need_iv:
        flags.append("TRAINER_DATA_TYPE_IV_EV_SET")
    for m in mons:                                       # habilidade pelo slot quando possivel
        m["slot"] = "TRAINER_POKEMON_ABILITY_1"
        if m["ability"]:
            two = C.abil.get(m["species"], [])
            if two and m["ability"] == two[0]:
                m["ability"] = None
            elif len(two) > 1 and m["ability"] == two[1] and two[1] != "ABILITY_NONE":
                m["slot"], m["ability"] = "TRAINER_POKEMON_ABILITY_2", None
            elif C.hidden.get(m["species"]) == m["ability"]:
                m["slot"], m["ability"] = "TRAINER_POKEMON_ABILITY_HIDDEN", None
    if any(m["ability"] for m in mons):
        flags.append("TRAINER_DATA_TYPE_ABILITY")
        for m in mons:
            if not m["ability"]:
                m["ability"] = C.abil[m["species"]][0]
    cls = NAME_CLASS.get(f["Name"]) if f["Class"] in ("Leader", "Elite Four", "Champion") else None
    cls = "TRAINERCLASS_" + (cls or PIC_CLASS[f["Pic"]])
    assert cls in C.classes, cls
    ai = "F_TRAINER_EXPERT_AI" if f["Class"] in EXPERT_CLASSES else AI.get(f.get("AI", "Basic Trainer"), AI["Basic Trainer"])
    if "Try To Faint" in f.get("AI", ""):
        ai = "F_TRAINER_EXPERT_AI"
    items = [C.one("items", "ITEM_", x.strip()) for x in f.get("Items", "").split("/") if x.strip()][:4]
    items += ["ITEM_NONE"] * (4 - len(items))
    battle = "DOUBLE_BATTLE" if f.get("Double Battle", "No") == "Yes" else "SINGLE_BATTLE"
    name = f["Name"].title() if f["Name"].isupper() else f["Name"]
    o = [f"    [{idx}] = {{  // Hollowtide: {gba_slot}",
         f'        .name = "{name}",', "        .data = {",
         f"            .trainerType = {' | '.join(flags) if flags else 'TRAINER_DATA_TYPE_NOTHING'},",
         f"            .trainerClass = {cls},", f"            .items = {{ {', '.join(items)} }},",
         f"            .aiFlags = {ai},", f"            .battleType = {battle},", "        },", "        .party = {"]
    for m in mons:
        ivs = m["ivs"] or [0] * 6
        o += ["            {", f"                .ivs = {round(max(ivs) * 255 / 31) if not need_iv else 0},",
              f"                .abilitySlot = {m['slot']},", f"                .level = {m['level']},",
              f"                .species = {m['species']},"]
        if "TRAINER_DATA_TYPE_ITEMS" in flags:
            o.append(f"                .item = {m['item']},")
        if "TRAINER_DATA_TYPE_MOVES" in flags:
            mv = (m["moves"] + ["MOVE_NONE"] * 4)[:4]
            o.append(f"                .moves = {{ {', '.join(mv)} }},")
        if "TRAINER_DATA_TYPE_ABILITY" in flags:
            o.append(f"                .ability = {m['ability']},")
        if need_iv:
            o.append("                .setIvs = { " + ", ".join(f".{k} = {v}" for k, v in zip(EVIV_FIELDS, ivs)) + " },")
            o.append("                .setEvs = { 0, 0, 0, 0, 0, 0 },")
        o += ["                .ballSeal = 0,", "            },"]
    o.append("        },")
    t = texts.get(gba_slot) or {}
    msgs = [("TRMSG_INTRO", t.get("intro"), "\\\\r"), ("TRMSG_LOSE", t.get("defeat"), "\\\\n"),
            ("TRMSG_AFTER", t.get("after"), "\\\\n")]
    msgs = [(k, v + end) for k, v, end in msgs if v]
    if msgs:
        o.append("        .text = {")
        for k, v in msgs:
            o += ["            {", f"                .type = {k},", f'                .text = "{v}",', "            },"]
        o.append("        },")
    o.append("    },")
    return "\n".join(o) + "\n"


def main(hg):
    C = Consts(hg)
    inv = json.load(open(os.path.join(REPO, "docs/hollowtide/ds/lunia_inventory.json")))
    by_slot = {}
    for name, tr in sorted(inv["trainers"].items()):
        by_slot.setdefault(tr["slot"], (name, tr))
    slots = json.load(open(SLOTS)) if os.path.exists(SLOTS) else {}
    nxt = max(list(slots.values()) + [FIRST_SLOT - 1]) + 1
    for s in sorted(by_slot):
        if s not in slots:
            slots[s] = nxt
            nxt += 1
    scripts = {}
    for mid in inv["maps"]:
        d = [p for p in os.listdir(os.path.join(REPO, "data/maps")) if os.path.exists(os.path.join(REPO, "data/maps", p, "map.json"))
             and json.load(open(os.path.join(REPO, "data/maps", p, "map.json")))["id"] == mid]
        if d and os.path.exists(os.path.join(REPO, "data/maps", d[0], "scripts.inc")):
            scripts[mid] = open(os.path.join(REPO, "data/maps", d[0], "scripts.inc")).read()
    alias_to_slot = {n: tr["slot"] for n, tr in inv["trainers"].items()}
    texts_by_name = battle_texts(set(inv["trainers"]), scripts)
    texts = {}
    for n, t in texts_by_name.items():
        texts.setdefault(alias_to_slot[n], t)
    orig = subprocess.run(["git", "-C", hg, "cat-file", "--filters", "HEAD:data/Trainers.c"], capture_output=True, text=True, check=True).stdout
    new = orig
    for s, (name, tr) in sorted(by_slot.items(), key=lambda x: slots[x[0]]):
        idx = slots[s]
        a = new.index(f"\n    [{idx}] = {{")
        b = new.index(f"\n    [{idx + 1}] = {{", a)
        new = new[:a + 1] + build_entry(C, idx, s, tr, texts) + new[b:]
    inc = ["// gerado por tools/hollowtide_ds/convert_trainers.py — indices dos treinadores de Lunia no DS", ""]
    inc += [f".equ TRAINER_HT_{s[len('TRAINER_'):]}, {slots[s]}" for s in sorted(by_slot)]
    al = sorted(n for n in inv["trainers"] if n not in by_slot)
    inc += [f".equ TRAINER_HT_{n[len('TRAINER_'):]}, {slots[alias_to_slot[n]]}  // = {alias_to_slot[n]}" for n in al]
    with tempfile.TemporaryDirectory() as tmp:
        a, b = os.path.join(tmp, "a.c"), os.path.join(tmp, "b.c")
        open(a, "w").write(orig); open(b, "w").write(new)
        p1 = subprocess.run(["diff", "-u", "--label", "a/data/Trainers.c", "--label", "b/data/Trainers.c", a, b],
                            capture_output=True, text=True).stdout
        bi = os.path.join(tmp, "inc")
        open(bi, "w").write("\n".join(inc) + "\n")
        p2 = subprocess.run(["diff", "-u", "--label", "/dev/null", "--label", "b/" + INC, "/dev/null", bi],
                            capture_output=True, text=True).stdout
    os.makedirs(os.path.dirname(PATCH), exist_ok=True)
    open(PATCH, "w").write(p1 + p2)
    os.makedirs(os.path.dirname(SLOTS), exist_ok=True)
    json.dump(dict(sorted(slots.items(), key=lambda x: x[1])), open(SLOTS, "w"), indent=1)
    missing = [s for s in by_slot if s not in texts]
    print(f"treinadores: {len(by_slot)} (indices {min(slots.values())}-{max(slots.values())}); com falas: "
          f"{len(by_slot) - len(missing)}; sem falas nos scripts: {missing}")
    print("falas com o nome do jogador (conferir no jogo; o script chama buffer_players_name 0):", sorted(set(PLAYER_TEXTS)))


if __name__ == "__main__":
    main(sys.argv[1])
