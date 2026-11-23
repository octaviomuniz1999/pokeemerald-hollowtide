# Hollowtide DS (HeartGold + hg-engine)

O jogo DS é o hg-engine (dependência externa, commit fixo em `hg-engine.commit`) mais o que está aqui. Nada da
Nintendo entra no git: os scripts, eventos e textos originais saem da ROM do diretor a cada build e o conteúdo do
Hollowtide fica em patches sobre esse despejo e sobre o hg-engine.

| Pasta | Conteúdo |
|---|---|
| `patches/0001-hg-engine-base.patch` | ajustes no hg-engine: compilar os scripts e eventos despejados (`BUILD_DUMPED_SCR_SEQ`, `BUILD_DUMPED_EVENTDATA`) e a correção da ordem dos argumentos do `msgenc` no despejo |
| `patches/content/` | o conteúdo do jogo (Lunia), aplicado em ordem alfabética: `data/scr_seq/*.s` (scripts), `data/eventdata/zone_event/*.json` (NPCs, warps, gatilhos, placas), `data/text/custom/NNN.txt` (textos), `data/Trainers.c`, `data/Encounters.c`… |
| `patches/content/matrix.json` | edições da matriz de mapas (o hg-engine não cobre mapas), aplicadas na ROM pronta por `tools/hollowtide_ds/matrix.py` |
| `provas/fase0/`, `provas/fase0_matriz/` | as provas de edição da Fase 0 (não são conteúdo do jogo) |

Build: `tools/hollowtide_ds/build.sh ROM_HEARTGOLD PASTA_HG_ENGINE` (ver `tools/hollowtide_ds/README.md`).
Créditos e licença do hg-engine: uso sem fins lucrativos, nada atrás de paywall, créditos do `CREDITS.md` na entrega.
