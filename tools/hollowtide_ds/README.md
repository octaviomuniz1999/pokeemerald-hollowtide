# Ferramentas da versão DS (Hollowtide em HeartGold / hg-engine)

## Build

- `build.sh ROM_HEARTGOLD PASTA_HG_ENGINE [PASTAS_DE_PATCHES...]`: hg-engine no commit de
  `hollowtide_ds/hg-engine.commit` + ROM HeartGold EUA (IPKE) + `hollowtide_ds/patches/0001-hg-engine-base.patch` +
  os patches de conteúdo (padrão `hollowtide_ds/patches/content`). Extrai da ROM, a cada build, os scripts, eventos e
  textos originais (`make dump_scripts`), aplica os patches e compila → `PASTA_HG_ENGINE/test.nds`. ~1–3 min.
- `matrix.py ROM matrix.json…` / `matrix.py ROM --show N X0 Y0 X1 Y1`: matrizes de mapa (a/0/4/1); o `build.sh`
  aplica o `matrix.json` de cada pasta de patches depois do `make`.
- `land_data.py ROM land.json…` / `land_data.py ROM --show BLOCO`: blocos de mapa (a/0/6/5): objetos 3D (construções)
  e colisão/comportamento de tile; ida e volta byte a byte nos 676 blocos. O `build.sh` aplica o `land.json` de cada
  pasta de patches depois da matriz. Coordenadas: tile (tx, ty) do bloco ↔ objeto em x = tx−16+0,5, z = ty−16+0,5;
  mundo = célula da matriz × 32 + tile.
- `text_patch.py HG_ENGINE`: `hollowtide_ds/data/texts.json` → `0500-texts.patch`. **Rodar depois de editar o
  `texts.json`**: a build usa o patch, não o JSON.
- `msg_dump.py HG_ENGINE ROM SAIDA [--check]`: textos (a/0/2/7) em `.txt` que voltam ao ROM byte a byte (829/829); o
  despejo de texto do próprio hg-engine perde as quebras de linha e não serve para recompilar.

## QA

- `ds_driver.py`: DeSmuME sem tela (`py-desmume`, `SDL_VIDEODRIVER=dummy`): botões, toque, capturas das duas telas,
  savestates (com os ponteiros do jogo ao lado, em `.ptr`) e leitura de mapa/posição do jogador pelos ganchos
  `FieldSystem_FlagCheck` e `PlayerAvatar_GetXCoord` (endereços do `rom.ld` do hg-engine).
- `ds_intro.py ROM SAIDA.dst`: jogo novo até o quarto do jogador (estado base dos testes; ~1m45).
- `prova_fase0.py ROM ESTADO_BASE CAPTURAS`: a prova de edição da Fase 0 (texto, script, presente, batalha vencida pelo
  toque, warp para a Route 29, encontro selvagem).

- `qa_cap1.py`, `qa_cap2.py`: Cap. 1 (quarto → Nevard → Breezeport) e Cap. 2 (Breezeport → Jay → saída norte).
- `qa_cp01.py ROM ESTADO_BASE PASTA`: prova de edição de mapa do CP-DS-01 (placa nova em Dawnmere: modelo, colisão
  dos dois lados, leitura, divisa com a Route 1 nos dois sentidos, salvar pelo menu, reiniciar, CONTINUE).
- `audit_dialogos.py HG_ENGINE ROM SAIDA.md`: auditoria das mensagens chamadas pelos scripts dos mapas jogáveis
  (referência, largura em pixels pela fonte do DS, linhas por caixa, nomes de Johto/Kanto, português, falas iguais às
  do HGSS), separando o que é alcançável do código morto.

**Estados salvos valem só para a ROM em que foram feitos.** O savestate guarda o mapa já carregado (e a tabela de
arquivos do cartucho); para testar uma edição, gere o estado base com `ds_intro.py` na ROM nova.

Ambiente: `python3 -m venv dsqa && dsqa/bin/pip install py-desmume ndspy`. A ROM nunca entra no repositório.
