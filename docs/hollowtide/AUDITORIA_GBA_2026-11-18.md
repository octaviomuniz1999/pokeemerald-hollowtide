# Auditoria GBA — Pokémon Hollowtide (corte 18/11/2026)

Fonte desta auditoria: pacote `HOLLOWTIDE_CLAUDE_INICIO_RAPIDO_2026-11-18.zip` + este repositório.
Tudo abaixo foi **verificado por comando** salvo quando marcado como "relato".

## 1. Base real do repositório

| Item | Resultado |
|---|---|
| Motor | `pokeemerald-expansion` **1.17.3** (`include/constants/expansion.h`) |
| Commit base | `99044bce` (upstream, 2026-11-18) — repositório limpo, **sem nenhum mapa `Palm*`** |
| Toolchain | `arm-none-eabi-gcc 13.2.1` (Ubuntu `gcc-arm-none-eabi`), build `modern` |
| Build | `make -j4` → exit 0, 2m48s, ROM 32 MB (uso 79,72%) |
| SHA-256 ROM base (vanilla expansion) | `d6a0d08ef664ba16cd36b92dee7b5585b17a90b10a6594e872234ac3fdf0b290` |
| SHA-256 ROM com iniciais Hollowtide | `b7553e5b51fc4cb2606350ab45d113bf6d2f17cd13b8f423c19bbf397a58dd19` |

ROMs **não** são versionadas (`*.gba` está no `.gitignore`).

## 2. Lacuna crítica: o snapshot Alpha 02 não veio no pacote

O `manifesto_arquivos.csv` lista, mas o ZIP "início rápido" **não contém**:

- `03_CODIGO_GBA/Pokemon_Palm_Alpha_02_Fonte_Completa_Colheita.zip` (56,4 MB, sha256 `0eedceae…c1`)
- `03_CODIGO_GBA/MAPAS_AUTORAIS/LittlerootTown.rar`, `rota_101.rar`, `oldale_colheita.rar`
- `03_CODIGO_GBA/PATCH_ALPHA02_ROTA02_SEM_ROM/*` (payload.zip, instalador, manifestos)
- zips de `04_MAPAS_CONCEITOS` estão presentes; `07_` e `99_` não.

Consequência: não é possível auditar `PalmBrisa`, `PalmFerralia`, `PalmRoute02/03`, etc.,
nem preservar a geometria autoral do Porymap. Pela regra 6 do pacote, **nenhum mapa foi inventado**.

## 3. Disponibilidade técnica do cânone (verificado em `include/constants/species.h`)

Todas as espécies/formas dos times de líderes, Elite, Doge, Cynthia, Tavinho e Team Palm existem
nesta versão, incluindo `SPECIES_CHARIZARD_MEGA_X`, `SPECIES_LATIOS_MEGA`, `SPECIES_GARCHOMP_MEGA`,
`SPECIES_KYOGRE_PRIMAL`, `SPECIES_NINETALES_ALOLA`, `SPECIES_ZOROARK_HISUI`,
`SPECIES_URSHIFU_RAPID_STRIKE`, Meowscarada, Kingambit. Mega/Primal em batalha ainda não testados.

## 4. Inventário GBA vs GDD

Legenda: **OK** implementado e testado · **NT** presente, não testado in-game · **—** não presente · **P** planejado

| Localidade / sistema | Estado neste repo | Observação |
|---|---|---|
| Iniciais Snivy/Fennekin/Mudkip | **NT** | `src/starter_choose.c`; compila; não jogado em emulador |
| Professor Alex / introdução | — | Emerald vanilla (Birch) |
| Vila Inicial | — | depende de `LittlerootTown.rar` (ausente) |
| Rota 01 | — | depende de `rota_101.rar` (ausente) |
| Vila da Colheita + ginásio Nevard | — | depende de `oldale_colheita.rar` / Alpha 02 |
| Nevard (Shroomish 12 / Treecko 14) | — | espécies disponíveis |
| Rota 02 | — | patch Alpha 02 ausente |
| Cidade da Brisa / Jay | — | P; layout GBA próprio, não a matriz DS |
| Rota 03 / Ferrália / Vessel | — | P |
| Team Palm, Elite, Doge, pós-Liga | — | P; espécies disponíveis |
| Rival | divergente | rival Emerald ainda usa Treecko/Torchic/Mudkip nos times vanilla |

## 5. Testes feitos e não feitos

- Feitos: build limpo da base; rebuild com iniciais; validação JSON do cânone.
- Não feitos: execução em mGBA (nenhum emulador de jogo instalado no container), save/load,
  batalhas Mega/Primal, `.xdelta` (sem ROM-base oficial declarada pelo usuário).

## 6. Próximas mudanças de maior impacto

1. **Receber o Alpha 02 + os três `.rar`** → importar como `baseline-import`, diff contra upstream 1.17.3,
   compilar e listar o que quebrou na migração de versão.
2. Trazer Vila Inicial / Rota 01 / Colheita autorais para o Porymap desta base, com warps e colisões.
3. Professor Alex + times de rival coerentes com os novos iniciais; Nevard (trainer + ginásio placeholder).
