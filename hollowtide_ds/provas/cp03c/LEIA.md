# Prova CP-DS-03B — atalho de QA para a Dawnmere original

Desde a etapa 6 do CP-DS-03B, Dawnmere, a Route 1 e Harvestvale convertidos do GBA estão na pasta de conteúdo:
- `patches/content/land.json`: o desenho global;
- `0700`–`0704`: os eventos nas posições do GBA (`tools/hollowtide_ds/eventos_gba.py`);
- `0705`: a ponte provisória para a Route 2 do protótipo (`tools/hollowtide_ds/ponte_route2.py`).

Esta pasta guarda só o atalho de QA:

`bash tools/hollowtide_ds/build.sh ROM HG_ENGINE hollowtide_ds/patches/content hollowtide_ds/provas/cp03c`

- `0921`: o PC do quarto leva a um caminho de Dawnmere (desenho 16,20; células a partir de (0,0)). É o que `qa_cp03c.py` usa.

Para o Cap. 1 inteiro, pelo fluxo do jogo, use a build de conteúdo com `provas/qa_forte` (o Tyranitar de QA) e
`qa_cp03d.py ROM ESTADO PASTA --cap1`.
