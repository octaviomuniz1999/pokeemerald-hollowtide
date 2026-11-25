# Prova — varredura visual dos mapas convertidos

Só para QA (nunca na build de entrega): o PC do quarto espera 20 quadros e faz `warp MAP_T20, 0, 1111, 2222`.
`tools/hollowtide_ds/qa_visual.py` troca na RAM, durante a espera, o mapa e as coordenadas do warp, e assim visita
qualquer ponto do mundo com o mapa carregado de verdade (blocos 3D, colisão, NPCs).

`bash tools/hollowtide_ds/build.sh ROM HG_ENGINE hollowtide_ds/patches/content hollowtide_ds/provas/visual`
