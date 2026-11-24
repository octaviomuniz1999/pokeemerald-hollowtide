# Prova CP-DS-03B — rascunho da Route 1, setor N

Não é conteúdo definitivo. É o rascunho do setor N da Route 1 desenhado em grade (`rota1_n.txt`, gerado por
`tools/hollowtide_ds/mapa_grade.py` com materiais da área 2), posto na célula (22,12) da matriz 0: a 1ª da Route 27,
vizinha leste de Dawnmere e livre no protótipo. A célula definitiva depende da decisão do diretor.
- `land.json`: bloco 11 = setor N (grade).
- `0910`: tira o gatilho de chão da Route 27 que ficava nessa célula.
- `0911`: atalho de QA no PC do quarto, que leva à entrada oeste do setor (712, 390). Não combinar com `provas/cp03a`,
  que usa o mesmo PC.
Build: `build.sh ROM HG hollowtide_ds/patches/content hollowtide_ds/provas/cp03b`; QA: `tools/hollowtide_ds/qa_cp03b.py`.
