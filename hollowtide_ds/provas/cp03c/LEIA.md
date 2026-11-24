# Prova CP-DS-03B — Dawnmere e Route 1 convertidas do GBA (build de prova)

`bash tools/hollowtide_ds/build.sh ROM HG_ENGINE hollowtide_ds/patches/content hollowtide_ds/provas/cp03c`

- `land.json`: desenho global `data/mapas/lunia_cap1.txt` (gerado por `gba2grade.py`) em 16 blocos novos nas células
  (21,13)–(24,16) da matriz 0. Também acrescenta o laboratório de Pallet e a porta dele à lista de construções 0.
- `0921`: atalho de QA. O PC do quarto leva a um caminho de Dawnmere, em (688,436).
- `0922`/`0923` (gerados por `tools/hollowtide_ds/eventos_gba.py`): os eventos de Dawnmere vão para as posições do
  GBA (warps, placas, NPCs, trava da saída), e a trava volta a ser a leste.
  - Para regenerar, rode o gerador sobre um hg-engine montado sem estes dois patches (`patch -R` antes).
- QA:
  - `qa_cp03c.py` anda de Dawnmere até a Route 1 pelo atalho;
  - `qa_cp03d.py` testa os eventos pelo fluxo do jogo, do quarto até a Route 1 com o inicial.
