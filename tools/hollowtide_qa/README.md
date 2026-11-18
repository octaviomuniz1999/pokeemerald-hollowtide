# Hollowtide QA — testes in-game headless

Roda a ROM no núcleo do mGBA sem interface, aperta botões por roteiro, lê a posição do jogador na RAM
e salva capturas. Serve para validar mapas, warps e travas a cada build.

```sh
sudo apt-get install -y libmgba-dev libpng-dev
gcc -O2 -o mgba_runner tools/hollowtide_qa/mgba_runner.c -lmgba -lpng
make -j$(nproc)
W=$(mktemp -d)
# 1) novo jogo ate a casa
{ cat tools/hollowtide_qa/roteiros/01_intro_ate_casa.txt; echo "savestate $W/casa.ss"; } > $W/r.txt
./mgba_runner pokeemerald.gba $W/r.txt
# 2) casa -> lab (Snivy) -> Rota 01 -> Colheita
python3 tools/hollowtide_qa/fluxo_inicial.py pokeemerald.gba ./mgba_runner $W $W/casa.ss
# 3) transicoes ida e volta ate Ferralia (injeta flags de historia)
python3 tools/hollowtide_qa/fluxo_transicoes.py pokeemerald.gba ./mgba_runner $W $W/e2e_colheita.ss
```

- `mgba_runner.c`: comandos `wait`, `press`, `walk`, `mash`, `shot`, `pos`, `expect_map`, `expect_pos`,
  `peek`, `setflag`, `setvar`, `poke8`, `savestate`, `loadstate` (ver cabeçalho do arquivo).
- `qa_driver.py`: rotas por BFS sobre a colisão/elevação reais dos `map.bin`, replanejando a cada trecho;
  trata diálogos e batalhas (tenta fugir, senão usa o 1º golpe). Endereços vêm do `pokeemerald.map`.
- Offsets usados (`SaveBlock1.flags` = 0x1270, `vars` = 0x139C, `struct Pokemon.level` = 0x54) valem
  para a build atual; recalcule se `struct SaveBlock1`/`struct Pokemon` mudarem.
- Savestates e capturas são gerados fora do repositório. Não versionar ROMs nem saves.
