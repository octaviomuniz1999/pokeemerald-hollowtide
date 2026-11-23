#!/usr/bin/env python3
"""Trocas com NPC de Lunia (GBA 23ap, src/data/trade.h, INGAME_TRADE_HT_*) -> trocas do HeartGold.

HGSS tem 13 trocas fixas: dados no NARC a/1/1/2 (0x54 bytes cada: especie dada, 6 IVs, habilidade, OT id, 5
condicoes, PID, item, genero do OT, brilho, idioma, especie pedida, 0) e nomes no texto 200 (apelido no indice da
troca, nome do OT em indice + 13). As de Lunia ocupam as primeiras vagas (0, 1, ...).

convert HG_ENGINE  -> hollowtide_ds/patches/content/trades.json + 0300-trades-text.patch (texto 200) +
                      data/scr_seq/include/hollowtide_trades.inc (.equ NPC_TRADE_HT_<NOME>, vaga) no mesmo patch
apply ROM.nds trades.json [...]  -> grava as vagas no NARC a/1/1/2 (o build.sh chama depois do make)
Apelidos e OT em caixa mista, como no DS ("KADA" -> "Kada"). A troca do GBA faz o Pokemon evoluir (Kadabra etc.);
no DS isso ainda precisa ser conferido no jogo.
"""
import json, os, re, struct, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT_JSON = os.path.join(REPO, "hollowtide_ds/patches/content/trades.json")
OUT_PATCH = os.path.join(REPO, "hollowtide_ds/patches/content/0300-trades-text.patch")
INC = "data/scr_seq/include/hollowtide_trades.inc"
NPC_TRADE_MAX = 13
FIELDS = ["give", "hpIv", "atkIv", "defIv", "speedIv", "spAtkIv", "spDefIv", "ability", "otId", "cool", "beauty",
          "cute", "smart", "tough", "pid", "item", "gender", "sheen", "language", "ask", "unk50"]


def numeric(hg, path, prefix):
    out, txt = {}, open(os.path.join(hg, path)).read()
    for k, v in re.findall(r"#define\s+(%s[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)\b" % prefix, txt):
        out[k] = int(v, 0)
    return out


def gba_trades():
    txt = open(os.path.join(REPO, "src/data/trade.h"), encoding="utf-8").read()
    res = []
    for name, body in re.findall(r"\[INGAME_TRADE_HT_(\w+)\]\s*=\s*\{(.*?)\n    \}", txt, re.S):
        g = lambda k: re.search(r"\.%s\s*=\s*([^,\n]+)" % k, body).group(1).strip()
        res.append({"name": name, "nickname": re.search(r'_\("([^"]*)"\)', g("nickname")).group(1),
                    "species": g("species"), "ivs": [int(x) for x in re.search(r"\{([^}]*)\}", body[body.index(".ivs"):]).group(1).split(",")],
                    "abilityNum": int(g("abilityNum")), "otId": int(g("otId")),
                    "conditions": [int(x) for x in re.search(r"\.conditions\s*=\s*\{([^}]*)\}", body).group(1).split(",")],
                    "personality": int(g("personality"), 0), "heldItem": g("heldItem"),
                    "otName": re.search(r'_\("([^"]*)"\)', g("otName")).group(1), "otGender": g("otGender"),
                    "sheen": int(g("sheen")), "requestedSpecies": g("requestedSpecies")})
    return res


def convert(hg):
    sp = numeric(hg, "include/constants/species.h", "SPECIES_")
    it = numeric(hg, "include/constants/item.h", "ITEM_")
    ab = numeric(hg, "include/constants/ability.h", "ABILITY_")
    species_c = open(os.path.join(hg, "data/Species.c"), encoding="utf-8").read()
    trades, names = [], {}
    for slot, t in enumerate(gba_trades()):
        m = re.search(r"\[%s\s*\]\s*=\s*\{.*?\.abilities\s*=\s*\{\s*(\w+)\s*,\s*(\w+)\s*\}" % t["species"], species_c, re.S)
        ability = ab[m.group(1 + min(t["abilityNum"], 1))]
        rec = {"slot": slot, "name": t["name"], "give": sp[t["species"]], "hpIv": t["ivs"][0], "atkIv": t["ivs"][1],
               "defIv": t["ivs"][2], "speedIv": t["ivs"][3], "spAtkIv": t["ivs"][4], "spDefIv": t["ivs"][5],
               "ability": ability, "otId": t["otId"], "cool": t["conditions"][0], "beauty": t["conditions"][1],
               "cute": t["conditions"][2], "smart": t["conditions"][3], "tough": t["conditions"][4],
               "pid": t["personality"], "item": it[t["heldItem"]], "gender": 1 if t["otGender"] == "FEMALE" else 0,
               "sheen": t["sheen"], "language": 2, "ask": sp[t["requestedSpecies"]], "unk50": 0,
               "_comment": f"{t['species']} '{t['nickname']}' (OT {t['otName']}) por {t['requestedSpecies']}"}
        trades.append(rec)
        names[slot] = t["nickname"].title()
        names[slot + NPC_TRADE_MAX] = t["otName"].title()
    json.dump(trades, open(OUT_JSON, "w"), indent=1)
    # texto 200: a copia byte a byte da ROM (msg_dump.py) com os nomes trocados
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "msg_dump.py"), hg,
                        os.path.join(hg, "rom.nds"), tmp], check=True, capture_output=True)
        orig = open(os.path.join(tmp, "200.txt"), encoding="utf-8", newline="").read()
        msgs = orig.split("\r\n")
        for i, n in names.items():
            msgs[i] = n
        new = "\r\n".join(msgs)
        a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
        open(a, "w", encoding="utf-8", newline="").write(orig)
        open(b, "w", encoding="utf-8", newline="").write(new)
        p1 = subprocess.run(["diff", "-u", "--label", "a/data/text/custom/200.txt", "--label",
                             "b/data/text/custom/200.txt", a, b], capture_output=True).stdout.decode("utf-8")
        inc = ["// gerado por tools/hollowtide_ds/npc_trades.py — vagas das trocas de Lunia (load_npc_trade N)", ""]
        inc += [f".equ NPC_TRADE_HT_{t['name']}, {t['slot']}" for t in trades]
        c = os.path.join(tmp, "inc")
        open(c, "w").write("\n".join(inc) + "\n")
        p2 = subprocess.run(["diff", "-u", "--label", "/dev/null", "--label", "b/" + INC, "/dev/null", c],
                            capture_output=True, text=True).stdout
    open(OUT_PATCH, "w", encoding="utf-8", newline="").write(p1 + p2)
    for t in trades:
        print(t["slot"], t["_comment"])


def apply(rom_path, jsons):
    import ndspy.narc, ndspy.rom
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    fid = rom.filenames.idOf("a/1/1/2")
    narc = ndspy.narc.NARC(rom.files[fid])
    n = 0
    for jp in jsons:
        for t in json.load(open(jp)):
            narc.files[t["slot"]] = struct.pack("<21i", *[t[k] for k in FIELDS])
            n += 1
    rom.files[fid] = narc.save()
    rom.saveToFile(rom_path)
    print(f"trocas: {n} vaga(s) em {rom_path}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "convert":
        convert(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "apply":
        apply(sys.argv[2], sys.argv[3:])
    else:
        raise SystemExit(__doc__)
