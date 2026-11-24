# Prova CP-DS-03A — terreno 3D gerado

Não é conteúdo de Lunia: só a prova de que o pipeline gera e integra terreno próprio (modelo 3D, alturas, colisão)
num bloco de mapa e que ele funciona no jogo.

- `land.json`: o bloco 57 (metade sul da Route 39, ligada a pé ao corredor norte de Breezeport) é gerado por
  `tools/hollowtide_ds/mapa_teste.py` — campina, caminho, mato alto, flores, árvores, platô com penhasco e rampa,
  placa (construção) com colisão.
- `0900-r39-sul-sem-eventos.patch`: tira os NPCs e placas da Route 39 que ficavam nesse bloco.

Build: `tools/hollowtide_ds/build.sh ROM HG_ENGINE hollowtide_ds/patches/content hollowtide_ds/provas/qa_forte hollowtide_ds/provas/cp03a`;
QA: `tools/hollowtide_ds/qa_cp03a.py`.
