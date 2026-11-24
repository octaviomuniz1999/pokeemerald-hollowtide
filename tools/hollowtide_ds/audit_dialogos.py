#!/usr/bin/env python3
"""Auditoria dos dialogos de Lunia na ROM pronta (CP-DS-02): cada mensagem que um script dos mapas jogaveis chama.

Mapas: os externos de Lunia ja montados (ligados a pe pela matriz) e tudo o que se alcanca pelos warps deles; a
Route 39 (Route 3, ainda nao montada) nao e expandida. Para cada `npc_msg`/`simple_npc_msg`/`non_npc_msg`/`gender_msgbox` checa:
  - REF: a mensagem existe no arquivo de texto do mapa (header) e nao esta vazia;
  - LARGURA: cada linha cabe na caixa — largura em pixels pela tabela da fonte do DS (a/0/1/6, arquivo 0; glifo = codigo-1),
    com o nome do jogador contado como 7 letras largas; o limite e a maior linha dos mesmos arquivos no HGSS original;
  - LINHAS: duas quebras \\n seguidas sem \\r/\\f (a terceira linha sai fora da caixa de 2 linhas);
  - HGSS: nomes de Johto/HGSS que nao existem em Lunia (Elm, Lyra, Johto...);
  - PT: palavras em portugues;
  - ORIGINAL: o texto e igual ao do HGSS (fala de Johto que ficou num NPC de Lunia) — so aviso: falas genericas
    (enfermeira, vendedor) sao iguais de proposito.
  - VAZIA: script chamado direto (scrdef) com wait_button e sem mensagem nenhuma (caixa vazia).
Uso: audit_dialogos.py HG_ENGINE ROM_PRONTA SAIDA.md
"""
import collections, glob, json, os, re, struct, subprocess, sys, tempfile
import ndspy.narc, ndspy.rom
sys.path.insert(0, os.path.dirname(__file__))

HDR_NAMES = r"\.equ\s+(MAP_\w+)\s*,\s*(\d+)"
OUTDOOR = [60, 33, 67, 34, 35, 77]          # Dawnmere, Route 1, Harvestvale, Route 2 (R30+R31), Breezeport
STOP = {43}                                # Route 39 (Route 3, ainda nao montada) nao e expandida
HGSS_NAMES = ["Elm", "Lyra", "Ethan", "Kris", "Johto", "Kanto", "Silver", "Kurt", "Falkner", "Bugsy", "Whitney", "Morty",
              "Chuck", "Jasmine", "Pryce", "Clair", "Lance", "New Bark", "Cherrygrove", "Violet", "Azalea", "Goldenrod",
              "Ecruteak", "Olivine", "Cianwood", "Mahogany", "Blackthorn", "Sprout Tower", "Bell Tower", "Ho-Oh", "Lugia",
              "Togepi", "Mr. Pokémon", "Professor Oak", "Prof. Oak", "Amphy", "Radio Tower", "Pokéathlon", "Pokégear",
              "Union Cave", "Ilex", "Whirl Islands", "Mt. Mortar", "Team Rocket", "Rocket", "Sudowoodo", "Ruins of Alph"]
PT_WORDS = re.compile(r"\b(você|voce|não|nao|está|esta|obrigad[oa]|olá|ola|cidade|treinador|ginásio|rota|placa|"
                      r"então|também|porque|aqui|isso|agora|vamos|muito)\b", re.I)
NAME_W = 7


def load_font(rom):
    f = ndspy.narc.NARC(rom.getFileByName("a/0/1/6")).files[0]
    off, n = struct.unpack_from("<II", f, 4)
    return f[off:off + n]


def load_charmap(hg):
    cm = {}
    for line in open(os.path.join(hg, "charmap.txt"), encoding="utf-8"):
        line = line.rstrip("\n").lstrip(" \t")
        if not line or line.startswith("//") or "=" not in line:
            continue
        code, ch = line.split("=", 1)
        if len(ch) == 1:
            cm.setdefault(ch, int(code, 16))
    return cm


def width(line, cm, widths):
    w = 0
    line = re.sub(r"\{STRVAR_1 3, 0, 0\}", "\0" * NAME_W, line)
    line = re.sub(r"\{[^}]*\}", "", line)            # outros codigos (cor, variaveis) sem largura fixa
    for ch in line:
        if ch == "\0":
            w += max(widths[cm[c] - 1] for c in "MW")
            continue
        code = cm.get(ch)
        w += widths[code - 1] if code and code - 1 < len(widths) else 8
    return w


def split_lines(msg):
    """[(linha, separador_que_veio_antes)]"""
    out, sep = [], "\\f"
    for part in re.split(r"(\\[nrf])", msg):
        if part in ("\\n", "\\r", "\\f"):
            sep = part
        else:
            out.append((part, sep))
    return out


def dump_texts(hg, rom_path, tmp):
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "msg_dump.py"), hg, rom_path, tmp],
                   check=True, capture_output=True)
    return lambda a: (open(os.path.join(tmp, f"{a:03d}.txt"), encoding="utf-8", newline="").read().split("\r\n")
                      if os.path.exists(os.path.join(tmp, f"{a:03d}.txt")) else None)


def headers(rom, hg):
    src = open(os.path.join(os.path.dirname(__file__), "hgss_catalog.py")).read()
    hdr = int(re.search(r"HDR\s*=\s*(0x[0-9A-Fa-f]+)", src).group(1), 16)
    arm9 = rom.loadArm9()
    sec = next(s for s in arm9.sections if s.ramAddress <= hdr < s.ramAddress + len(s.data))
    names = {int(v): k for k, v in re.findall(HDR_NAMES, open(os.path.join(hg, "asm/include/maps.inc")).read())}
    out = {}
    for m in names:
        _, _, _, _, scripts, _, msg, _, _, events = struct.unpack_from("<BBHHHHHHHH", sec.data, hdr - sec.ramAddress + 24 * m)
        out[m] = {"name": names[m], "scripts": scripts, "msg": msg, "events": events}
    return out


def region(hg, hdrs):
    by_name = {v["name"]: k for k, v in hdrs.items()}
    ev = {int(os.path.basename(p).split("_")[0]): p for p in glob.glob(os.path.join(hg, "data/eventdata/zone_event/*.json"))}
    seen, q = set(), list(OUTDOOR)
    while q:
        m = q.pop()
        if m in seen:
            continue
        seen.add(m)
        if m in STOP or hdrs[m]["events"] not in ev:
            continue
        for w in json.load(open(ev[hdrs[m]["events"]])).get("warp_events", []):
            dest = w.get("dest_header_id")
            d = by_name.get(dest) if isinstance(dest, str) else dest
            if d is not None and d not in seen:
                q.append(d)
    return sorted(seen), ev


def script_file(hg, n):
    g = glob.glob(os.path.join(hg, f"data/scr_seq/scr_seq_{n:04d}_*.s")) + glob.glob(os.path.join(hg, f"data/scr_seq/scr_seq_{n:04d}.s"))
    return g[0] if g else None


def reachable(path, hg, events_json):
    """Rotulos alcancaveis: scripts chamados pelos eventos do mapa (NPCs, placas, gatilhos) e pelo header do mapa
    (_hdr.s: tabelas de quadro, ao entrar, ao carregar), e o que eles alcancam por goto/call/queda."""
    lines = open(path, encoding="utf-8").read().splitlines()
    defs = [m.group(1) for m in (re.match(r"\s*scrdef\s+(\w+)", l) for l in lines) if m]
    blocks, order, cur = {}, [], None
    for l in lines:
        m = re.match(r"^(\w+):", l)
        if m:
            cur = m.group(1); blocks[cur] = []; order.append(cur); continue
        if cur and l.strip() and not l.strip().startswith("//"):
            blocks[cur].append(l.strip())
    ids = set()
    if events_json:
        ev = json.load(open(events_json))
        for kind in ("object_events", "bg_events", "coord_events"):
            for e in ev.get(kind, []):
                sc = str(e.get("script", ""))
                m = re.match(r"_EV_\w+_(\d+)\s*\+\s*1$", sc)
                if m:
                    ids.add(int(m.group(1)))
                elif sc.isdigit():
                    ids.add(int(sc) - 1)
    hdr = path.replace(".s", "_hdr.s")
    hdr = glob.glob(re.sub(r"scr_seq_\d{4}_", "scr_seq_*_", hdr))
    if hdr:
        t = open(hdr[0], encoding="utf-8").read()
        for a in re.findall(r"\.hword\s+(\d+),\s*0", t):
            ids.add(int(a) - 1)
        for a in re.findall(r"\.hword\s+\w+,\s*\d+,\s*(\d+)", t):
            ids.add(int(a) - 1)
    todo = [defs[i] for i in ids if 0 <= i < len(defs)]
    seen = set()
    while todo:
        b = todo.pop()
        if b in seen or b not in blocks:
            continue
        seen.add(b)
        body = blocks[b]
        for tok in re.findall(r"\b(\w+)\b", " ".join(body)):
            if tok in blocks and tok not in seen:
                todo.append(tok)
        if not body or not re.match(r"(end|goto|return|jump)\b", body[-1]):
            i = order.index(b)
            if i + 1 < len(order):
                todo.append(order[i + 1])
    return seen


def refs(path):
    """[(rotulo, indice)] e blocos com wait_button sem mensagem."""
    lab, out, empty, block_msgs, block_wait = None, [], [], 0, False
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(\w+):", line)
        if m:
            if lab and block_wait and not block_msgs:
                empty.append(lab)
            lab, block_msgs, block_wait = m.group(1), 0, False
            continue
        s = line.strip()
        m = re.match(r"(npc_msg|simple_npc_msg|non_npc_msg)\s+(\d+)\b", s)
        if m:
            out.append((lab, int(m.group(2)))); block_msgs += 1
        m = re.match(r"gender_msgbox\s+(\d+),\s*(\d+)", s)
        if m:
            out += [(lab, int(m.group(1))), (lab, int(m.group(2)))]; block_msgs += 1
        if re.match(r"(msgbox_extern|non_npc_msg_var|npc_msg_var|trainer_message|holdmsg)\b", s):
            block_msgs += 1
        if s.startswith("wait_button"):
            block_wait = True
    if lab and block_wait and not block_msgs:
        empty.append(lab)
    return out, empty


def main(hg, rom_path, out_md):
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    widths, cm = load_font(rom), load_charmap(hg)
    hdrs = headers(rom, hg)
    maps, evfiles = region(hg, hdrs)
    with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
        new = dump_texts(hg, rom_path, t1)
        old = dump_texts(hg, os.path.join(hg, "rom.nds"), t2)
        limit = 0
        for m in maps:                                   # limite: a maior linha do HGSS nos mesmos arquivos
            for msg in old(hdrs[m]["msg"]) or []:
                for ln, _ in split_lines(msg):
                    if re.search(r"[A-Za-z]", ln):           # linhas so de espacos sao enchimento de tela, nao caixa
                        limit = max(limit, width(ln, cm, widths))
        issues = collections.defaultdict(list)
        stats = collections.Counter()
        for m in maps:
            h = hdrs[m]
            sf = script_file(hg, h["scripts"])
            if not sf:
                continue
            msgs, orig = new(h["msg"]) or [], old(h["msg"]) or []
            rs, empty = refs(sf)
            live = reachable(sf, hg, evfiles.get(h["events"]))
            defs = set(re.findall(r"^\s*scrdef\s+(\w+)", open(sf, encoding="utf-8").read(), re.M))
            for lab in (l for l in empty if l in defs):      # rotulos internos sao rabos de goto depois de uma mensagem
                issues[m].append(("VAZIA", lab, "", "wait_button sem mensagem no bloco", lab in live))
            for lab, i in sorted(set(rs), key=lambda r: r[1]):
                stats["mensagens"] += 1
                if i >= len(msgs) or not msgs[i].strip():
                    issues[m].append(("REF", lab, i, "mensagem inexistente ou vazia", lab in live)); continue
                t = msgs[i]
                lines = split_lines(t)
                for ln, _ in lines:
                    w = width(ln, cm, widths)
                    if w > limit:
                        issues[m].append(("LARGURA", lab, i, f"{w}px > {limit}px: {ln!r}", lab in live))
                for (a, sa), (b, sb) in zip(lines, lines[1:]):
                    if sa == "\\n" and sb == "\\n":
                        issues[m].append(("LINHAS", lab, i, f"3 linhas na caixa: {a!r} / {b!r}", lab in live))
                for nm in HGSS_NAMES:
                    if re.search(r"(?<![A-Za-z])%s(?![a-z])" % re.escape(nm), t):
                        issues[m].append(("HGSS", lab, i, f"{nm}: {t[:90]!r}", lab in live))
                if PT_WORDS.search(t):
                    issues[m].append(("PT", lab, i, t[:90], lab in live))
                if i < len(orig) and t == orig[i]:
                    stats["iguais_ao_hgss"] += 1
                    issues[m].append(("ORIGINAL", lab, i, t[:90], lab in live))
    kinds = collections.Counter((k, "alcançável" if r else "código morto") for v in issues.values() for k, _, _, _, r in v)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Auditoria de diálogos (gerada por `tools/hollowtide_ds/audit_dialogos.py`)\n\n")
        f.write(f"ROM: `{os.path.basename(rom_path)}`. Mapas da região jogável (warps a partir do quarto): {len(maps)}. "
                f"Mensagens chamadas por scripts: {stats['mensagens']}. Limite da caixa: {limit}px (maior linha do HGSS "
                f"nos mesmos arquivos).\n\n")
        f.write("| Tipo | Onde | Ocorrências |\n|---|---|---|\n" + "".join(f"| {k} | {r} | {v} |\n" for (k, r), v in sorted(kinds.items())) + "\n")
        f.write("Código morto = script que nenhum evento ou header do mapa chama (cenas do HGSS desligadas); fica listado "
                "só para conferência.\n\n")
        for m in maps:
            if not issues[m]:
                continue
            h = hdrs[m]
            f.write(f"## {h['name']} ({m}) — scripts {h['scripts']}, textos {h['msg']}\n\n")
            for k, lab, i, d, r in sorted(issues[m], key=lambda x: not x[4]):
                f.write(f"- {'**' + k + '**' if r else k + ' (código morto)'} `{lab}` msg {i}: {d}\n")
            f.write("\n")
    print(f"{len(maps)} mapas, {stats['mensagens']} mensagens, limite {limit}px:", {f"{k}/{r}": v for (k, r), v in kinds.items()}, "->", out_md)


if __name__ == "__main__":
    main(*sys.argv[1:4])
