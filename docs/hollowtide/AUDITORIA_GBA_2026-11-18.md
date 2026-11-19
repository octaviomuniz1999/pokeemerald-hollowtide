# Auditoria GBA — Pokémon Hollowtide (corte 18/11/2026, revisão 2)

Fontes: pacote completo `Pokemon_Hollowtide_Transferencia.part01-09.rar` (74/74 arquivos conferidos
contra o SHA-256 do `manifesto_arquivos.csv`) + este repositório.
**Testado** = executado em emulador (libmgba 0.10.2, headless, `tools/hollowtide_qa`). **Inspecionado** = só leitura de código/dados.

## 1. Base e importação

| Item | Resultado |
|---|---|
| Snapshot Alpha 02 | `pokeemerald-expansion` 1.17.3 = upstream `c460a866` + 113 arquivos Palm (42 novos, 71 alterados) |
| Importação | branch `hollowtide/baseline-import-alpha02` (commit `d4d5b55b`, sem edições; só perdas de permissão do zip descartadas) |
| Merge com upstream atual (`99044bce`) | 1 conflito trivial (`starter_choose.c`, mesma troca nos dois lados) |
| Build do snapshot original | `make` exit 0 (2m48s) — compila como veio |
| Build atual do branch | `make` exit 0, **0 avisos** de redefinição |
| Patch `PATCH_ALPHA02_ROTA02_SEM_ROM` | **Não aplicar**: 3 dos 4 arquivos já estão no snapshot; o 4º (`PalmRoute02/scripts.inc`) é mais antigo que o do snapshot (11:24 vs 19:15 de 06/11). O instalador recusaria (hash de base diverge). |
| `.rar` autorais | `rota_101` e `oldale_colheita` = mesma geometria do Alpha 02 (40×53 e 39×37), que tem ajustes posteriores (12 e 6 metatiles + elevação/colisão). `LittlerootTown.rar` não tem `map.bin` (só `map.json`/scripts vanilla) — a geometria da Vila está só no Alpha 02. |

## 2. Correções feitas nesta rodada

1. **Respawn fora do mundo (bug grave, testado)**: a intro Palm pula o caminhão, que era quem chamava
   `setrespawn`. Perder uma batalha antes do primeiro Centro Pokémon levava a **Petalburg City** (vanilla,
   sem ligação com o mundo Hollowtide). Corrigido em `src/new_game.c`; agora o jogador volta para casa
   e a mãe cura o time (validado em emulador perdendo para o recruta da Team Palm).
2. **LOCALIDs conflitantes** entre as casas de Littleroot (2/3/4 vs 3/4/5): reordenados os objetos da casa da May; elimina 168 avisos.

## 3. Resultado do QA em emulador

| Verificação | Resultado |
|---|---|
| Boot, título, novo jogo, apresentação do PROF. ALEX, nome, gênero | **OK** (sprite ainda é o Birch — placeholder documentado) |
| Início direto na casa (sem caminhão) | **OK** — o bug histórico "preso no caminhão" não ocorre |
| Lab: Alex oferece Snivy → Fennekin → Mudkip; Snivy recebido + 5 Poké Balls + 2 Potions | **OK** (Snivy Lv5 confirmado em batalha) |
| Vila Inicial → Rota 01 → Vila da Colheita (com batalhas selvagens/treinadores) | **OK** |
| Portas da Colheita (Centro, Mart, Casa 1, Casa 2) | **OK** |
| Porta do ginásio trancada até a irrigação ser restaurada | **OK** (intencional: `Palm071_LoadDoor`) |
| Recruta da Team Palm (quiosque) → batalha | **OK** (interage; Poochyena Lv9) |
| Saída Colheita → Rota 02 bloqueada antes do Nevard | **OK** |
| Saída leste da Brisa bloqueada antes da Jay | **OK** |
| Colheita ⇄ Rota 02 ⇄ Brisa ⇄ Rota 03 ⇄ Ferrália, ida e volta, até a Vila Inicial | **OK 13/13** (travas liberadas por injeção de flag) |
| Entrar no ginásio com irrigação restaurada | **OK** |
| Puzzle de comportas, Nevard, insígnia, TM Bullet Seed | **não testado** (exige vencer batalhas) |
| Teatro/Jay, Ferrália (interior/ginásio) | **não testado** |
| Salvar/carregar pelo menu | **não testado** |

Para as passagens além do Nevard o teste **injeta** `FLAG_DEFEATED_RUSTBORO_GYM`, `FLAG_PALM_JAY_WON` e
`FLAG_PALM_IRRIGATION_RESTORED` e desliga encontros selvagens via Repel em RAM. Isso valida mapas e
warps, não as batalhas nem os eventos.

## 4. Defeitos e divergências encontrados (abertos)

| # | Achado | Tipo |
|---|---|---|
| 1 | Emenda Rota 03 → Ferrália: corredor da Rota 03 ocupa as linhas 9–13, Ferrália só libera 9–11 (parede nas linhas 12–13) | defeito de mapa |
| 2 | Popups/menu mostram nomes do Emerald: Brisa = DEWFORD TOWN, Rota 02 = ROUTE 104, Rota 03 = ROUTE 116, Ferrália = RUSTBORO CITY | divergência (nomes finais a decidir) |
| 3 | Diálogos Palm (Alex, placas, Colheita) estão em **português**; cânone pede inglês no jogo | divergência |
| 4 | Balanceamento: recruta Lv9 logo após a Rota 01 (Snivy chega Lv6); não venci com o script | balanceamento |
| 5 | Brisa 20×20 (base Dewford) e Ferrália 26×20 — placeholders muito menores que o cânone (cidade grande / metrópole) | divergência de escopo |
| 6 | Saída da Brisa para a Rota 03 é a **leste**; cânone atual: oeste/noroeste pela praia | divergência |
| 7 | Rota 03 é um corredor reto 48×20; cânone pede serra, desníveis e bifurcações | divergência de escopo |
| 8 | Transições entre áreas são feitas por gatilhos com `warp` (com fade), não por conexões de mapa — funciona, mas não é a travessia contínua do Emerald | observação |
| 9 | Times de rival continuam os do Emerald | divergência |

## 5. Próximas mudanças de maior impacto

1. Corrigir a emenda Rota 03/Ferrália e dar nomes Hollowtide às seções de mapa (decisão de nomes pendente).
2. Passagem de balanceamento do início (níveis da Rota 01/recruta/ginásio) e teste do puzzle do Nevard até a insígnia.
3. Reconstruir a Brisa em escala de cidade costeira, com saída oeste para a Rota 03 (o esqueleto atual vira placeholder).

## 6. Capítulo 1 — estado em 18/11/2026 (noite)

| Item | Estado |
|---|---|
| Colisão de Dawnmere, Route 1, Harvestvale | corrigida (linter 0/0) |
| Texto do capítulo | 100% inglês, validado por largura de glifo (`tools/hollowtide/texts.py`) |
| Medalhão de Atlas | item-chave novo; a mãe entrega na porta de casa — **testado** |
| Escolha do inicial | tela das 3 Poké Balls (sem batalha do Zigzagoon) — **testado** |
| Recruta → válvula → ginásio → comportas → Josh → Tommy → Nevard → insígnia → Route 2 | **10/10 testado no emulador** (time de QA nível 100) |
| Comportas do ginásio | progresso persistente (antes zerava ao sair do mapa) |
| Team Palm | classe "TEAM PALM"; Grunts com paleta verde-oliva dedicada; retratos recoloridos sem o símbolo da Aqua |
| Nevard | níveis do cânone (12/14); moveset sem Stun Spore/Mega Drain; sem Potion; sprite **placeholder oficial (Camper)** — o sprite gerado do Alpha 02 fica no repositório, fora de uso |
| Balanceamento | inicial solo, sem itens: vence recruta, Josh e Tommy; contra o Nevard a luta é apertada (Treecko termina com ~1/3 de HP). Pendente: teste com Potions e um 2º Pokémon |

## 7. Capítulo 2 — 19/11/2026 (madrugada)

| Item | Estado |
|---|---|
| Breezeport | layout novo 72×56 (General + Lilycove) gerado pelo `mapgen` e instalado por script; linter 0/0 |
| Saídas | norte → Route 2; **oeste pela praia → Route 3** (cânone; antes era leste) |
| Interiores | Centro Pokémon, Mart, loja de departamentos, 7 casas e o Teatro religados; ponto de cura atualizado |
| Festival | anfitriã → 3 postes apagados em bairros diferentes → Teatro abre — **testado** |
| Teatro / Jay | holofotes E-D-E → Jay (Shuppet 18 / Misdreavus 21) → Insígnia Eco → Route 3 — **testado** (time de QA) |
| Texto | 100% inglês; interiores reaproveitados sem citações a Hoenn |
| Jay | placeholder oficial (Phoebe) no campo e na batalha; sprite gerado do Alpha 02 preservado fora de uso |
| Pendente | farol, polimento artístico, Route 2 (revisão), NPCs urbanos, balanceamento da Jay |
