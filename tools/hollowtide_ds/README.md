# QA de DS (Hollowtide em HeartGold / hg-engine)

- `ds_driver.py`: DeSmuME sem tela (`py-desmume`, `SDL_VIDEODRIVER=dummy`): botões, toque, capturas das duas telas,
  savestates (com os ponteiros do jogo ao lado, em `.ptr`) e leitura de mapa/posição do jogador pelos ganchos
  `FieldSystem_FlagCheck` e `PlayerAvatar_GetXCoord` (endereços do `rom.ld` do hg-engine).
- `ds_intro.py ROM SAIDA.dst`: jogo novo até o quarto do jogador (estado base dos testes).

Ambiente: `python3 -m venv dsqa && dsqa/bin/pip install py-desmume ndspy`. A ROM nunca entra no repositório.
