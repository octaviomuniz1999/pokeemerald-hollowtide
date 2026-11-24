# CP-DS-02B — SAVE/CONTINUE nativo entre execuções independentes (24/11/2026) — **passou**

## Teste definitivo (pedido pelo diretor), sem savestate em nenhum passo

`tools/hollowtide_ds/qa_save.py ROM PASTA` executa duas vezes o Python, em dois processos separados:

| Passo | Processo | Resultado |
|---|---|---|
| apagar o save da ROM (`~/.config/desmume/<nome>.dsv`) | — | começa sem save |
| abrir o emulador, carregar a ROM, jogo novo até o quarto | 1 | (64, 6, 6) |
| descer; a mãe entrega o medalhão (agora o menu tem SAVE) | 1 | casa (63, 3, 3) |
| **salvar pelo menu do jogo** (SAVE → Yes → "You saved…") | 1 | `.dsv` gravado na hora: 524 410 bytes, sha1 `0af31465db16` |
| sair de casa **sem salvar** | 1 | Dawnmere (60, 695, 397) |
| encerrar o emulador (`desmume_close`) e o processo | 1 | `.dsv` igual (nada pendente) |
| abrir outro emulador num processo novo, carregar a mesma ROM, CONTINUE | 2 | **casa (63, 3, 3)**, o ponto salvo e não o último visitado |
| **RESULTADO** | | **ok** |

## Diagnóstico (o que a ordem pediu para investigar)

| Item | Achado |
|---|---|
| Tipo de save | detectado automaticamente pelo DeSmuME como FLASH 4 Mbit (rodapé do `.dsv`: tipo 6, 512 KiB), que é o do HeartGold. `ds_driver.DS(rom, savetype)` permite fixá-lo; não foi preciso |
| Diretório e arquivo nativo | `~/.config/desmume/<nome da ROM sem extensão>.dsv` (512 KiB + rodapé DeSmuME). Associação ROM ↔ save pelo **nome do arquivo** da ROM |
| Escrita | o DeSmuME grava o `.dsv` no momento do save do jogo (mtime e hash mudam logo depois de "You saved…"); fechar o emulador não muda o arquivo. Permissões de escrita: ok |
| Por que o teste do CP-DS-01 falhou num processo novo | aquele fluxo **partia de um savestate** (estado da intro). O `.dsv` gravado depois de carregar um savestate não foi reconhecido por um emulador novo (caiu em NEW GAME); sem savestate, é reconhecido. O 1º campo do rodapé difere (0x80000 contra 0x40001). Regra: teste de save nativo nunca usa savestate |
| Reset × savestate × save normal | o reset do mesmo console mantém a memória do save (teste positivo, mas insuficiente); o savestate guarda RAM e o chip de save congelados e não substitui o save nativo; o save normal persiste no `.dsv` e volta num processo novo (este teste) |
| Leitura de posição depois do CONTINUE | nenhum script roda, então o gancho de `FieldSystem_FlagCheck` não dispara. `ds_driver` passou a achar o FieldSystem pelo ponteiro do avatar (FieldSystem + 0x40), conferido num estado com os dois ganchos |

Para o jogador (DeSmuME/melonDS no Windows): o save é o arquivo `.dsv`/`.sav` ao lado da ROM ou na pasta de saves
do emulador, com o mesmo nome da ROM. Trocar o nome da ROM "perde" o save, porque o emulador procura outro arquivo.
