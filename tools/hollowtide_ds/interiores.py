#!/usr/bin/env python3
"""Interiores de Lunia: coesao das falas (diretor, 25/11: "outros nao apresentam coesao").

audit_dialogos.py acha as falas originais do HGSS alcancaveis nos interiores. As que contam coisas que nao existem em
Lunia mudam assim:
  - falas soltas: a mensagem do DS recebe a fala do NPC correspondente no interior do GBA (texts.json);
  - NPCs de mecanicas do HGSS que Lunia nao tem (Seals, Ball Capsule): saem da sala (hidden_flag com uma flag que ja
    esta ligada desde o comeco, FLAG_GOT_TRAINER_CARD, posta na cena da mae).
Gera 0713-interiores-coesao.patch sobre o hg-engine montado com a pasta de conteudo (sem este patch).
Uso: interiores.py HG_ENGINE PASTA_SAIDA
"""
import difflib, json, os, sys

ESCONDER = {   # zona -> scripts dos NPCs que saem
    "212_T26PC0101": ["_EV_scr_seq_T26PC0101_004 + 1"],   # Ball Capsule (Centro de Breezeport)
    "215_T26R0501": ["_EV_scr_seq_T26R0501_002 + 1"],     # Seals (casa de Breezeport)
}
FLAG = "FLAG_GOT_TRAINER_CARD"


def diff(rel, old, new):
    out = []
    for line in difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + rel, "b/" + rel):
        out.append(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n")
    return "".join(out)


def main(hg, out):
    parts = []
    for zona, scripts in ESCONDER.items():
        rel = f"data/eventdata/zone_event/{zona}.json"
        old = open(os.path.join(hg, rel)).read()
        j = json.loads(old)
        n = 0
        for o in j["object_events"]:
            if o["script"] in scripts:
                o["hidden_flag"] = FLAG; n += 1
        assert n == len(scripts), (zona, n)
        parts.append(diff(rel, old, json.dumps(j, indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")))
    open(os.path.join(out, "0713-interiores-coesao.patch"), "w").write("".join(parts))
    print("0713-interiores-coesao.patch gerado")


if __name__ == "__main__":
    main(*sys.argv[1:3])
