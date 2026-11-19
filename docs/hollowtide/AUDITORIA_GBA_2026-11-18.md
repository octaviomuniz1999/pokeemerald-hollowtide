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

## 8. Route 2 e travessia contínua — 19/11/2026 (manhã)

| Item | Estado |
|---|---|
| Route 2 | refeita pelo `mapgen` (40×48, General + Lilycove): campo com trilha sinuosa e manchas de mato de contorno irregular, bosques escalonados, ladeiras de mão única, mirante em platô com escada, enseada com casa do pescador, calçamento e poste na chegada à cidade; linter 0/0. Instalada por `tools/hollowtide/maps/install_route2.py` |
| Conexões | Harvestvale ⇄ Route 2 ⇄ Breezeport agora são **conexões de mapa** (sem fade, como no Emerald); defeito nº 8 da seção 4 resolvido nesse trecho (Route 3 ainda usa warp, será refeita no Cap. 3) |
| Trava antes do Nevard | gatilho na calçada sul da Harvestvale: mensagem + jogador recua um passo — **testado** nos dois estados |
| Emenda de tilesets | o GBA desenha o mapa vizinho com o tileset do mapa atual; as 4 linhas finais da Harvestvale visíveis da Route 2 viraram estrada de terra do primário (o calçamento Slateport aparecia preto). Regra nova: **toda emenda de conexão só pode mostrar metatiles do primário ou do secundário comum aos dois mapas** |
| Treinadores | Liang, Mei-Lan e Qin com linha de visão (desafiam ao avistar), posicionados ao lado da trilha; falas de derrota em inglês — **testado** (`fluxo_rota2.py`) |
| Recompensa | Super Potion no mirante (flag de item de Hoenn sem uso em Lunia) — **testado** |
| Gerador | correção: terreno sem elevação de referência (flores) sobre platô herda a altura do platô — o mirante era inalcançável; na Breezeport corrigiu a trilha do morro |
| QA | regressão completa 48/48 (`qa_completo.sh`: intro, Cap. 1, transições 17, Cap. 2, Route 2) |

## 9. Breezeport: morro e orla — 19/11/2026 (manhã)

| Item | Estado |
|---|---|
| Morro | refeito: mata de árvores 2×2 em contorno orgânico (grade par), patamar (elev. 5) com árvores e flores, cume-mirante (elev. 7); escadaria da avenida ao cume; acabou a leitura de "zigurate" dos anéis concêntricos |
| Orla | faixa de água rasa entre areia e mar, com laguna mais larga e banco de areia; pedras na areia e na água rasa; rochedo no mar; **rochedo do antigo farol** (3×4) e **farol provisório** (poste composto sobre areia) na ponta do pontal |
| Narrativa | faroleiro aponta o rochedo onde ficava o farol e o poste que guia os barcos até a reconstrução; montanhista do cume descreve a baía |
| Route 2 | a enseada que sumia na borda oeste virou poça de maré rasa cercada de areia (bordas completas) |
| Ferramenta | `install_route2.py` idempotente (a emenda de terra da Harvestvale não muda ao reinstalar); peças compostas de poste sobre areia |
| QA | caminhada no emulador até o cume, patamar, pontal e laguna; regressão 48/48 |

## 10. Capítulo 3 — Route 3 — 19/11/2026 (tarde)

| Item | Estado |
|---|---|
| Route 3 | refeita pelo `mapgen` (56×80, General + Lilycove), seguindo a progressão do cânone: calçadão da Breezeport → praia natural (casa de praia, pedras, ponta de areia escondida) → restinga → encosta (patamar 5) → serra/mata atlântica (7) → planalto (9) → saída norte. Duas trilhas (escadas principais e trilha da mata) que se reencontram na serra |
| Conexão | Breezeport ⇄ Route 3 contínua (offset 20); trava antes da Jay em toda a borda oeste da Breezeport (calçadão, areia e água rasa), recuando um passo — **testada** |
| Emendas | patamares só visuais: piso andável achatado para elevação 3 (rocha bloqueia, escadas em 0), deixando as emendas no mesmo nível; borda reta em volta das escadas (degrau diagonal virava quina de rocha e trancava a subida — corrigido) |
| Bordas | Breezeport 72×60 e Route 3 76→80 linhas: 4+ linhas de mar fundo depois da última água rasa (antes dava para ver além da borda a partir da água rasa); moldura sem frestas (mata fechada onde a 2×2 não cabe) |
| Treinadores | Rui (Fisherman), Tomás (Bug Catcher), Bento (Hiker), Iara (Picnicker), Davi (Camper), Lv 19–22, em slots de Hoenn sem acesso em Lunia (`TRAINER_PALM_ROUTE03_*`) — **todos testados com visão ligada** |
| Itens | Big Pearl (ponta de areia), Great Ball (clareira), Revive (planalto) — **testados** |
| Encontros | Wingull, Pikipek, Aipom, Combee, Venipede, Hoppip, Mareep, Lillipup, Sandygast, Skiddo, Nincada, Pansage (Lv 17–21) |
| Ferralia | ainda é o mapa provisório do Alpha 02; ligação temporária por warp nos dois sentidos (conexão desalinhada removida). Próximo passo: metrópole |
| QA | `fluxo_rota3.py`; `goto` do driver alterna golpes em batalhas encontradas no caminho; regressão completa **63/63** |

## 11. Capítulo 3 — Ferralia — 19/11/2026 (tarde)

| Item | Estado |
|---|---|
| Ferralia | refeita pelo `mapgen` (72×64, General + **Rustboro**): avenidas de 2 tiles (norte, "Paulista", três N-S), bairro residencial, sede FERRALIA RAIL & STEEL (prédio Devon), ginásio do Vessel com torres, praça da fonte com jardim, Centro Pokémon e Mart, torres de escritório na Paulista, escritórios ao sul, **pátio de carga cercado com duas linhas de trem** e parque ao sul; 23 prédios conferidos contra sobreposição; linter 0/0 |
| Ferrovia | trilho e para-choque **desenhados** (lastro, dormentes, trilhos; paleta 9 da Rustboro) em slots de tile livres do secundário, fora dos slots animados (água 128–159, fonte 448–451) |
| Emenda | Route 3 ⇄ Ferralia contínua (offset 16); as 6 linhas do parque visíveis da rota e as linhas do planalto visíveis da cidade usam só o primário — conferido por script |
| Interiores | Centro Pokémon, Mart, 3 casas e 2 prédios residenciais da Rustboro religados; textos sem Hoenn (Roxanne→Vessel, Devon→Ferralia Rail & Steel) |
| Narrativa | ginásio fechado: o líder foi ao pátio de carga por um carregamento que não chegou; operário: a Team Palm só descarrega à noite; linha leste (Route 4) fechada "para inspeção" — ganchos de "Carga Desviada" |
| Encontros | parque: Pidove, Trubbish, Rattata, Lillipup, Grimer, Magnemite, Klink (R), Aron (R), Lv 20–23 |
| QA | transições 21/21 (Route 3 ⇄ Ferralia, Centro Pokémon); regressão completa 67/67; `qa_completo.sh` agora mostra o resumo inteiro das transições |

## 12. Capítulo 3 — "Carga Desviada" e ginásio do Vessel — 19/11/2026 (tarde)

| Item | Estado |
|---|---|
| Evento | ginásio trancado ao chegar; Vessel no pátio de carga pede ajuda; 2 recrutas da Team Palm (visão ligada) desviando os canos de aço para secar as nascentes da costa e revender a água; Vessel agradece, some do pátio e o ginásio destranca na hora — **testado** |
| Ginásio | interior do ginásio de Mauville (chaves que alternam barreiras = "passarelas ressonantes"); 5 treinadores de Aço (Klink, Magnemite, Aron, Ferroseed, Pawniard, Mawile, Bronzor; Lv 21–22); Vessel Magnemite 22 / Mawile 24 / Aron 26 (cânone), placeholder oficial (Wattson); efeitos colaterais de Hoenn removidos (museu de Slateport, Scott, Petalburg, Match Call, TM Shock Wave) — **testado** até a insígnia |
| Textos | 100% EN; guia, estátuas e treinadores reescritos; insígnia "RESONANCE BADGE" |
| Pendente | TM Flash Cannon (exige trocar a lista de TMs — fazer junto com Bullet Seed/Hex dos ginásios 1–2); interior do ginásio com arte própria |
| QA | `fluxo_cap3_eventos.py` (13/13); `goto` aceita células a evitar (chaves do quebra-cabeça); regressão completa: 80 verificações, 0 falhas |

## 13. Capítulo 4 — Route 4 e Tradepost — 19/11/2026 (tarde)

| Item | Estado |
|---|---|
| Base | pacote conceitual `etapa9_entreposto` (dimensões 52×32 e 40×32, pontos de interesse, treinadores, encontros, evento) |
| Route 4 | mapa novo (General + Rustboro): ferrovia ao norte continuando o pátio de Ferralia (leito fechado: trilhos com colisão, cerca viva; a linha só abre no capítulo do Hoc), estrada das caravanas, antigo abrigo de carga, canal com a única ponte (tabuado da Route 104), desvio norte (Super Potion), desvio sul (2 Oran Berries), mirante NE; Yue (Meowth 22/Koffing 23), Qiao (Timburr 23/Electrike 24), Mara opcional (Nincada 22/Dwebble 24); encontros do pacote |
| Tradepost | mapa novo: estação no fim da linha (para-choque leste desenhado), Centro Pokémon e Mart (interiores de Verdanturf), casa e casa do Relembrador de Golpes (Fallarbor), praça do mercado com fonte e canteiros, Associação de Mercadores, canal com ponte para o cais leste e o quiosque da Team Palm; ponto de cura |
| Emendas | os três mapas usam General + Rustboro: Ferralia ⇄ Route 4 (offset 24) ⇄ Tradepost (offset 0) contínuas e corretas dos dois lados; Ferralia: leito ferroviário vedado na emenda para não haver atalho |
| Travas | borda leste da Ferralia fecha até a Insígnia da Ressonância (recua um passo); saída norte do Tradepost (Route 5) fechada pela enchente até o Cap. 5 |
| Evento | "O Preço da Troca" (sem batalha): Mestre Wen pede a autorização original de carga → operador da estação entrega → Wen desmonta a cobrança em PALM Coin, a mensageira da Palm vai embora, a vendedora recupera as caixas, Amulet Coin. Kyogre/Orbe/Tavinho não são citados |
| Textos | 100% EN; interiores de Verdanturf sem Hoenn |
| QA | `fluxo_cap4.py` 20/20 (trava antes/depois, 3 treinadores com visão, 4 itens, evento completo, Centro Pokémon, conexões ida e volta); regressão completa sem falhas (100 verificações) |
| Pendente | bancas de feira desenhadas (hoje: canteiros e moradores), interior da Associação, Route 5 |
