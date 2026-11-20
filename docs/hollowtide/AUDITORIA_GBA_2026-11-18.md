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

## 14. Capítulo 5 — Route 5 — 19/11/2026 (fim da tarde)

| Item | Estado |
|---|---|
| Route 5 | mapa novo (42×52, General + Rustboro): o canal do Tradepost continua como rio (offset 6, grade par alinhada), braço oeste em volta da ilha do meio (mato alto, item) com dois tabuados, tabuado horizontal para a margem leste, leito antigo **seco** (a barragem de Pillarton segura a água) com pedras e poças na várzea; Tiago (Barboach/Wooper), Odair (Sandshrew/Phanpy), Lia (Marill/Lotad), Dudu opcional (Cubone/Larvitar), Lv 25–26; 3 itens (Super Potion, Soft Sand, Ether); encontros Lv 24–27 |
| Tradepost | saída norte aberta após "O Preço da Troca" (trava recua um passo antes); operário da enchente sai; textos do Wen e da placa atualizados |
| Norte | Pillarton ainda não existe: a trilha termina na mata com placa de obras na barragem |
| Gerador | **margem sul de lagos** aprendida (metatile 2/45/211/212 como grama com margem) — os mapas existentes não mudaram; **água funda (pond/sea) com elevação 1** como nos oficiais (surf e colisão por altura) |
| QA | `fluxo_cap5.py` 14/14; **`qa_completo.sh` corrigido**: antes, um fluxo que falhava antes do resumo podia sumir do log (o filtro só mostrava a partir de "RESUMO"); agora mostra toda linha OK/FALHA/erro e para na primeira falha (`pipefail`). Regressão completa sem falhas (~118 verificações) |

## 15. Capítulo 5 — Pillarton e "A Cidade das Águas Presas" — 19/11/2026 (noite)

| Item | Estado |
|---|---|
| Pillarton | mapa novo (56×44, General + Rustboro — o tileset de Mauville não tem pontes): barragem ao norte (patamar com o reservatório e a crista de serviço, escada), usina da Team Palm no pátio leste da crista, rio que sai do pé da barragem e cruza a cidade sob duas pontes até a Route 5 (offset 4), canal antigo seco com pedras, Centro Pokémon, Mart e casa (interiores de Lavaridge, sem Hoenn), ginásio, jardins "de contrato" da Palm, parque ao sul (emenda só com primário, conferida) |
| Evento | Tchum recebe o jogador (piadas de "base sólida"); 2 recrutas na crista (visão ligada); 3 **válvulas desenhadas** (volante marrom fechado / bege aberto, sobre o piso da praça); Lela só luta depois das três (Persian 28, Roselia 29, Lanturn 30 — cânone; placeholder oficial de admin), fala do cânone ("escassez com oportunidade… água em energia, energia em moedas…"), vai embora; água de volta (FLAG_HT_PILLARTON_WATER) |
| Pendente | ginásio do Tchum (interior de Fortree: portões giratórios como comportas; o BFS do QA ainda não modela os portões), rio visualmente mais cheio depois do evento |
| QA | `fluxo_cap5.py` estendido: 28/28 (Route 5 + Pillarton + Centro Pokémon + volta); regressão completa sem falhas (~130 verificações) |

## 16. Capítulo 5 — ginásio do Tchum — 19/11/2026 (noite)

| Item | Estado |
|---|---|
| Ginásio | interior do ginásio de Fortree: os portões giratórios fazem o papel das comportas; abre na hora em que a Lela é derrotada (o Tchum sai da rua e vai ao ginásio); 6 treinadores de Terra (Geodude, Diglett, Cubone, Sandshrew, Trapinch, Wooper, Phanpy, Nosepass, Drilbur, Baltoy, Larvitar; Lv 26–27); Tchum Sandshrew 27 / Phanpy 28 / Marowak 31 (cânone; Marowak por último), placeholder oficial (Brawly) → **Insígnia dos Pilares** (FLAG_BADGE04_GET); efeitos de Hoenn removidos (TM Aerial Ace, Match Call, Scott) |
| Textos | 100% EN, com o "TERrapia" do cânone ("It's time for some TERapy") |
| QA | **resolvedor de portões giratórios**: porta em Python de `rotating_gate.c` (tabelas de rotação, braços, colisão com BUGFIX) + BFS sobre (posição, orientação dos 8 portões); no jogo, 97 passos com a posição conferida a cada 6 passos contra a simulação; volta pelo estado atual dos portões; `fluxo_cap5.py` 34/34; regressão completa sem falhas (~137 verificações) |
| Pendente | arte própria do ginásio (hoje: casa na árvore de Fortree), TM Bulldoze/Flash Cannon/Hex/Bullet Seed na passada de TMs |

## 17. Passada de TMs e robustez do QA — 19/11/2026 (noite)

| Item | Estado |
|---|---|
| TMs | lista de TMs ganhou **Flash Cannon (TM52)** e **Bulldoze (TM53)** depois do Hex (TM51); quem aprende é regenerado no build a partir de `all_learnables.json` (Magnemite → Flash Cannon e Phanpy → Bulldoze conferidos); Vessel e Tchum entregam os TMs depois da insígnia; descrição do TM Hex traduzida (estava em português) |
| QA | o modo forte (só em build não-release) agora também dá golpes de ataque variados (Surf, Ice Beam, Thunderbolt, Body Slam) e é reaplicado (cura) antes de cada líder/admin — o inicial nível 100 com golpes de status perdia para o Marowak do Tchum de vez em quando; regressão completa sem falhas |

## 18. Correção: ginásio da Jay (relato do diretor) — 19/11/2026 (noite)

| Item | Estado |
|---|---|
| Relato | "não dá para ativar a sequência de lâmpadas, não é possível passar do ginásio" |
| Diagnóstico | a mecânica funcionava (VAR_TEMP_8 0→1→2→3 conferido no emulador), mas a ordem só existia numa placa **invisível** (piso comum em (8,11)) que a Jay mandava ler; o painel do meio e qualquer erro apagavam tudo sem dizer por quê — para o jogador, o puzzle parecia não responder |
| Correção | a Jay diz a ordem (ESQUERDA, DIREITA, ESQUERDA); cada holofote diz qual é o próximo; o painel do meio mostra a ordem em vez de apagar; erro apaga com a dica; som de sucesso ao acender o palco |
| QA | `fluxo_cap2_eventos.py` agora simula o jogador confuso (painel do meio e ordem errada antes da ordem certa) e confirma que o ginásio continua vencível; regressão completa sem falhas |
| Builds | a partir da 19l as builds de teste saem **sem RELEASE**, com o menu de debug da expansion (R + START), a pedido do diretor, até o fim do jogo |

## 19. Capítulo 6 — Route 6, Serenia e "O Jardim das Lembranças" — 19/11/2026 (noite)

| Item | Estado |
|---|---|
| Pillarton | borda leste virou parque (só primário nas colunas que a Route 6 enxerga — conferido) com a avenida saindo para leste; trava até a Insígnia dos Pilares |
| Route 6 | mapa novo (54×36, General + Lavaridge): jardim de pedra (areia lisa com pedras dispostas), bosques fechados no lugar do bambu, canal tranquilo com margem completa, santuários de beira de estrada; Ren (Natu/Espurr), Mika (Snubbull/Cottonee), Sayo (Chingling/Ralts), Hana (Petilil/Cottonee), Lv 30–32; Twisted Spoon, PP Up, Revive; encontros da Pokédex do Cap. 6 |
| Serenia | mapa novo (44×40, Lavaridge): fonte sagrada como santuário/altar, trilha de pedras entre moitas até a fonte, Centro Pokémon, Mart e 3 casas (interiores de Fortree, sem Hoenn), ginásio, jardins; ponto de cura |
| Evento | Jade e o **Espeon Lau** (sprite de Pokémon de mapa) com as falas do cânone; 3 ilusões (pedras que fecham as duas faixas e somem depois do encontro); fragmento deixado pela Team Palm; altar revela a inscrição ("a sleeping power may call the tide over the mountains") — Tavinho e Kyogre não são citados |
| Pendente | ginásio da Jade → feito na seção 20 |
| QA | `fluxo_cap6.py` 25/25; driver: `goto(ignore=...)` para objetos já removidos; regressão completa sem falhas (~160 verificações) |

## 20. Capítulo 6 — ginásio da Jade ("Jardim dos Espelhos") — 20/11/2026

| Item | Estado |
|---|---|
| Mapa | `MAP_PALM_JADE_GYM` novo, 9×48, montado com as salas do ginásio de Petalburg (entrada, salas A/B/C, sala da líder); borda com o vazio do próprio tileset (a borda de árvores padrão virava lixo magenta) |
| Puzzle | os 3 espelhos da entrada mostram LUA, ESTRELA, SOL; cada sala tem duas portas com símbolo gravado; a porta certa leva à próxima sala, a errada devolve à entrada; descer pelo piso de baixo de qualquer sala também volta à entrada |
| Portas | as portas de Petalburg não são portas de warp (comportamento `MB_PETALBURG_GYM_DOOR`): viraram sinais como no original — mostram o símbolo, perguntam "Step through the door?" e usam `warpdoor`; metatile da porta já aberta |
| Batalhas | 3 treinadores com visão (Psychic/Hex Maniac) e Jade: Chimecho 34, Gardevoir 36, Espeon (Lau) 38 → Insígnia da Serenidade (5ª) + TM Psychic |
| Serenia | a porta do ginásio abre na hora em que o altar revela a inscrição (som + mensagem); Jade e Lau saem da vila e vão para o ginásio |
| QA | `fluxo_cap6.py` com o ginásio: espelhos, porta certa/errada, vitória, insígnia e saída na porta certa de Serenia |

## 21. Capítulo 7 (parte 1) — Route 7, Horizon City e "As Águas do Horizonte" — 20/11/2026

| Item | Estado |
|---|---|
| Serenia | saída norte nova (trilha nas colunas 38-39, entre a mata) com conexão contínua para a Route 7; trava até a Insígnia da Serenidade |
| Route 7 | mapa novo (36×56, General + Lavaridge): lago-espelho a oeste com contorno em degraus de 2 tiles (degrau de 1 tile não tem quina no autotile), trilha pela margem leste, **Círculo da Lua** (patamar com escada, anel de pedras e flores — Moon Stone no centro), campo de flores, mato alto; Celia (Swirlix/Togepi/Marill), Connie (Spritzee/Flabébé), Henry (Goldeen/Psyduck/Seaking), Colin (Swablu/Altaria), Lv 36–39; Moon Stone, Mystic Water, Pixie Plate; encontros de terra (Clefairy, Togepi, Swablu, Flabébé, Spritzee, Swirlix), surf e pesca (Feebas raro) |
| Horizon City | mapa novo (56×44, General + Lilycove): lago ao norte cercado de mata, orla com passeio calçado e postes, jardim da orla, estação de controle do lago (margem oeste), Pavilhão das Estrelas (margem leste, fechado por enquanto), cúpula do ginásio da Chelsia, Centro Pokémon, Mart e 3 casas (interiores de Mossdeep com moradores novos; o pescador da Super Rod ficou); ponto de cura; faixa sul só com primário (a Route 7 enxerga 7 linhas — o instalador confere as duas emendas) |
| Evento | o lago subiu sem chuva: o mapa salvo é o "depois" e o ON_LOAD alaga o jardim (58 metatiles) até o fim do evento, com colisão; Chelsia e o **Piplup** (sprite de Pokémon) na orla — o Piplup aponta a estação, que só abre depois disso; **estação sob o lago** (mapa novo sobre o layout B2F do esconderijo da Aqua: tanques e máquinas): 3 recrutas da Team Palm, 3 amplificadores para desligar, Marill/Psyduck/Lotad presos em redes, terminal com o registro "SOURCE: EXTERNAL / DIRECTION: NORTH / SIGNAL: IRREGULAR" (só com tudo feito); Kyogre e Tavinho não são citados |
| Ginásio | **"O Lago das Estrelas"** nos mapas do ginásio de Sootopolis (1F/B1F): cada placa de gelo é uma estrela — pisar uma vez acende (racha), com todas acesas a escada do campo seguinte aparece; pisar de novo quebra o gelo e cai no B1F (3 treinadoras: Andrea, Daphne, Bridget) com a escada de volta à entrada; mecanismo original de Sootopolis (callback de passo + VAR_ICE_STEP_COUNT, limites 8/28/67 conferidos com os 7/19/38 ladrilhos); Chelsia (sprite/retrato provisórios: Anabel) com o Piplup ao lado: Clefable 40, Azumarill 41, Sylveon 43 → **Insígnia do Horizonte** + **TM54 Dazzling Gleam** (TM novo); a porta abre quando o lago baixa |
| Cuidado técnico | `setmetatile` não muda a elevação do bloco: água colocada por script sobre chão (elevação 3) ficaria andável — os metatiles de água do alagamento entram como bloqueados; o QA confere que não se anda na água da orla antes do evento |
| QA | `fluxo_cap7.py` 48/48 (trava norte, 4 treinadores com visão, 3 itens, conexões nos dois sentidos, estação fechada antes da Chelsia, água da orla bloqueada, recrutas, amplificadores, Pokémon soltos, registro, jardim andável depois, trava norte, Centro Pokémon, ginásio: 3 constelações, vitória, insígnia, queda no B1F e volta); o fluxo resolve cada campo de gelo com um caminho que pisa cada estrela uma única vez (busca em profundidade sobre o layout); suíte completa sem falhas (~355 verificações nos Cap. 1–6 + 48 no Cap. 7, mesma build) |
| Pendente | interior do Pavilhão das Estrelas; arte própria do ginásio |

## 22. Capítulo 8 — Route 8 e Passway Village — 20/11/2026

| Item | Estado |
|---|---|
| Route 8 | mapa novo (34×48, General + Lilycove — a emenda sul enxerga o Pavilhão das Estrelas da Horizon): encosta em 3 patamares de contorno orgânico com bordas retas em volta de cada escada, trilha em zigue-zague, pinheiros (mata 2×2), pedras, mato alto, mirante oeste sobre o lago; Alan (Swinub/Graveler/Ursaring), Kiyo (Machoke/Riolu), Cora (Meditite/Sneasel), Auron (Glalie/Abomasnow), Lv 40–43; Never-Melt Ice, Hyper Potion, Ice Stone; encontros do Cap. 8 (Lv 40–43) |
| Passway Village | mapa novo (36×32, Lavaridge): patamar da montanha com a escadaria do cume (interditada pelo guardião; abre só com FLAG_SYS_GAME_CLEAR — na história, depois dos créditos e da convocação do Doge), mural na rocha (a figura do Medalhão de Atlas, detalhe opcional), fonte termal que cura o time, estalagem, Centro Pokémon, Mart (o tutor de Metronome ficou), casa da anciã ("um círculo claro como a lua sobre o peito de um cão negro… até os guardiões precisam descansar"), mirante; estrada leste para Voltara fechada por um deslizamento nesta etapa; ponto de cura |
| Emendas | Horizon ⇄ Route 8 (offset 36) e Route 8 ⇄ Passway (offset 2): faixas conferidas no instalador (só primário onde o vizinho enxerga) |
| Cânone | Tavinho e Kyogre não aparecem; o protagonista só observa o céu escurecendo sobre o cume |
| Correções | sprite CRUSH_GIRL é só do modo FRLG (não aparece no Emerald): Cora usa EXPERT_F; o sinal do deslocamento da conexão Route 8 ⇄ Passway estava invertido (o QA pegou na travessia) |
| QA | `fluxo_cap8.py` (trava/conexões nos dois sentidos, 4 treinadores com visão, 3 itens, escadaria e estrada leste recuam, fonte termal, casa da anciã, Centro Pokémon); o combate de QA da montanha usa só Surf/Ice Beam e cura antes de cada treinador; **suíte completa 484/484 (Cap. 1–8) na mesma build** — build 20p |

## 23. Capítulo 9 (parte 1) — Route 9 — 20/11/2026

| Item | Estado |
|---|---|
| Passway | estrada leste aberta (deslizamento limpo); a casa da anciã mudou para o sul da vila: a Route 9 usa o secundário Rustboro e enxerga as colunas 28-35 da Passway, que agora só têm primário (o instalador confere linhas 10-27) |
| Route 9 | mapa novo (48×36, General + Rustboro): estrada ao lado da ferrovia que vem de Voltara (os trilhos terminam num para-choque na coluna 12, depois da faixa que a Passway enxerga), calçada de serviço, subestação com placa de alta tensão, mato alto, bosques; Joseph (Electrike/Voltorb/Manectric), Drew (Shinx/Blitzle), Heidi (Helioptile/Pachirisu), Fabian (Magneton/Galvantula), Lv 42–44; Magnet, Thunder Stone, Electric Seed; encontros (Electrike, Blitzle, Shinx, Joltik, Helioptile, Elekid, Luxio raro); portão de Voltara fechado por falta de energia até a cidade existir |
| QA | `fluxo_cap9.py` (conexão nos dois sentidos, 4 treinadores com visão, 3 itens, portão fechado); a verificação da estrada leste saiu do QA do Cap. 8; **suíte completa 510/510 (Cap. 1–9 parte 1)** — build 20q |

## 24. Capítulo 9 (parte 2) — Voltara e o Centro de Dados — 20/11/2026

| Item | Estado |
|---|---|
| Route 9 | portão leste aberto; conexão contínua com Voltara (offset 0, mesmos tilesets) |
| Voltara | mapa novo (60×44, General + Rustboro): os trilhos da Route 9 entram pela moldura e terminam no para-choque da estação; Centro de Dados da Team Palm (prédio grande), ginásio (fechado até a parte 3), Centro Pokémon, Mart, apartamentos, casas, torre, escritórios, canteiros, árvore só em canteiro (regra de coesão), parque com flores; céu encoberto (cidade sem energia); ponto de cura; interiores de Mauville com moradores novos (o velho de Mauville saiu) |
| Evento | Hoc recebe o jogador na frente da estação (falas do cânone: a rede caiu, o "Du", Riven e "alguma coisa está respondendo de muito longe"); um recruta guarda a porta do Centro de Dados até lá; saguão (layout do Space Center 1F) com 2 recrutas; sala dos servidores (2F) com o **Vega** (Magneton 43, Porygon2 44, Eelektrik 45) e 3 retransmissores — só dá para desligar depois de vencê-lo; com os 3 desligados a energia volta; a fala do Vega sobre "a fonte" e um log "SENSOR FEED: NORTH…" |
| Build | um nome de música inválido (MUS_MAUVILLE) passou pelo filtro de erros do make (erro de link, não de compilação): agora a saída completa do make é conferida |
| QA | `fluxo_cap9b.py` (conexão, porta fechada antes do Hoc, Hoc, recrutas e Vega com visão, 3 retransmissores, energia, saída sul fechada, Centro Pokémon, volta); **suíte completa 552/552** — build 20r |

## 25. Capítulo 9 (parte 3) — ginásio do Hoc e o time de QA — 20/11/2026

| Item | Estado |
|---|---|
| Ginásio | `MAP_PALM_HOC_GYM`, cópia do layout do ginásio de Mauville com todos os feixes ligados no começo; os 4 botões são consoles: (0,15) corta o feixe baixo → (4,12) o leste → (8,9) o central → (3,9) o do palco; o feixe esquerdo e os verticais ficam ligados; a ordem é imposta pelo próprio salão (conferido por BFS etapa a etapa); progresso em VAR_HT_HOC_GYM, refeito no ON_LOAD; 3 treinadores (Marcos, Conor, Paxton); Hoc (sprite/retrato provisórios: Norman) com o Rotom: Jolteon 44, Luxray 45, Ampharos 46, Rotom 47 → **Insígnia Circuito**, **TM55 Volt Switch** (novo) e a mensagem do Riven ("guarde os dados, não pergunte por quê"); a Insígnia abre a saída sul de Voltara |
| Voltara | as duas folhas da porta do Centro de Dados entram; a porta do ginásio abre com a energia de volta |
| Vega | sem Recover/Thunder Wave (paralisia + cura deixavam a luta empatada): Mirror Shot no Magneton, Ice Beam no Porygon2 |
| QA | pedido do diretor: o líder do time de QA vira um **Mewtwo Lv 100 Modest** (IVs 31, 252 EVs em Sp. Atk e Speed; Surf, Psystrike, Thunderbolt, Ice Beam), só no gancho de QA de builds não-release; ele conta como encontrado no Lv 5 (a obediência Gen 8+ usa o nível de encontro — sem isso ele cochilava, "began to nap"); limite de turnos 140 em todos os fluxos; **suíte completa 582/582 (Cap. 1–9)** — build 20s |

## 26. Capítulo 10 (parte 1) — Route 10 e Tidemouth — 20/11/2026

| Item | Estado |
|---|---|
| Voltara | faixa sul (linhas 37-43, colunas 12-49) repintada só com primário: grama, mata e estrada de terra (a Route 10 usa Lilycove); clareira na frente do prédio de apartamentos |
| Route 10 | mapa novo (38×60, General + Lilycove): estrada desce de Voltara e segue pela praia contínua entre o mar e as falésias com mata; faróis-guia (postes compostos sobre areia) em duas pontas de pedra, enseada rasa, restinga com mato alto; Tomas (Pelipper/Machoke), Rita (Marill/Azumarill), Jonas (Remoraid/Qwilfish/Octillery), Luana (Lumineon/Seaking/Starmie), Lv 45–48; Deep Sea Scale, Damp Rock, Max Repel; encontros de terra (Wingull, Lombre, Pelipper, Krabby, Corphish…) e surf (Tentacruel, Wailmer, Mantine, Lapras raro) |
| Tidemouth | mapa novo (64×48, General + Lilycove, chuva): avenida calçada, motel, Grand Hotel (fechado), Centro Pokémon, Mart, casas, canal de água (3 de largura — 2 de água rasa não tem borda boa), parque aquático, porto com o terminal; ginásio da Nami no pavilhão — o carimbo vinha com o patamar da Lilycove (escada em elevação 5), agora o piso andável fica no nível da rua; interiores de Pacifidlog/Sootopolis/Lilycove (motel só térreo) com moradores novos; ponto de cura |
| Evento | Nami coordena a evacuação na avenida ("nobody goes in the water…", "these guys put an entire city at risk"); porto com as balsas suspensas e ginásio trancado com o bilhete da Nami; correção: a trava do porto empurrava o jogador para dentro da porta (agora recua para o sul) |
| QA | `fluxo_cap10.py` (conexões nos dois sentidos, 4 treinadores com visão, 3 itens, Nami, porto e ginásio fechados, Centro Pokémon); o QA desvia dos treinadores parados na estrada; **suíte completa 622/622 (Cap. 1–10 parte 1)** — build 20t |

## 27. Capítulo 10 (partes 2 e 3) — Complexo Oceânico, Abelf e o ginásio da Nami — 20/11/2026

| Item | Estado |
|---|---|
| Complexo | depois da Nami, o marinheiro do porto leva o jogador no barco dela; 1F no layout do esconderijo da Aqua (turbinas, reservatórios, doca) com 3 recrutas posicionados nos únicos corredores; sala de controle no salão não usado do Ruby: Nami chega no Wailord; **Abelf** (Krookodile 49, Magnezone 50, Kingambit 51, Gyarados 52; sprite/retrato provisórios: Archie) com as falas do cânone; vencido, o jogador desliga o sistema central: a Team Palm se dissolve e o monitor mostra por um instante o contorno de uma montanha sob um céu escuro (sem citar Kyogre/orbe) |
| Tidemouth | depois do complexo a chuva para (ON_TRANSITION) e o ginásio destranca |
| Ginásio | **"As Eclusas"**: arena aquática a céu aberto (General + Lilycove), 3 piscinas atravessando a arena; o mapa salvo tem os canais secos e o ON_LOAD enche os que ainda estão fechados (água por setmetatile entra bloqueada); cada alavanca drena o canal da sua piscina e a próxima só fica alcançável depois (conferido por BFS etapa a etapa); 3 nadadores; **Nami** (sprite/retrato provisórios: Beauty) Pelipper 47, Ludicolo 48, Wailord 49, Milotic 50, Gyarados 52 → **Insígnia Maré** (8ª) + **HM07 Waterfall** (o "TM Waterfall" proposto vira o HM que já existe, para não duplicar o golpe na lista de TM/HM) |
| QA | o Mewtwo de QA usa Surf/Aura Sphere/Thunderbolt/Psystrike (Psystrike não acerta os Sombrios do Abelf); os fluxos desviam dos treinadores parados depois da luta (crista da Pillarton, Route 10, Abelf); **suíte completa 676/676 (Cap. 1–10)** — build 20u |

## 28. Capítulo 11 — Route 11, a Liga Pokémon de Lunia e o pós-créditos — 20/11/2026

| Item | Estado |
|---|---|
| Route 11 | mapa novo (48×36, General + Lilycove): saída oeste de Tidemouth (linhas 28-29) com guarda das 8 insígnias; praia sob as falésias, patamares 5 e 7 com escadas, boca do túnel (metatile 0xA7) na parede do patamar alto; Vincent, Felix e Leroy com visão e **golpes definidos** (o Altaria do Felix aprendia Perish Song pelo nível e derrubava o time de QA de um Pokémon só); 3 itens; encontros de caverna |
| Ilha da Liga | o túnel sai na parte alta de Ever Grande (warp 18,27); conexões com a Route 128 removidas; guardas do saguão conferem a **8ª** insígnia |
| Ordem das salas | refeita pelos warps para combinar piso e tipo: Hall5 → sala de gelo (**Angelic**, Gelo) → Hall1 → sala roxa (**Riven**, Normal) → Hall2 → tatame (**Du**, Lutador) → Hall3 → sala laranja (**Pkas**, Solar) → Hall4 → campeão |
| Times | do cânone, com golpes; Pkas é o **primeiro adversário com Mega** (Charizard @ Charizardite X, Lv 70); **Doge**: Meowscarada 71, Ninetales 72, Vaporeon 72, Umbreon 73, Lugia 75, Latios @ Latiosite 77 por último; a IA mega-evolui só com a pedra (sem Key Stone para o oponente) |
| Falas | do roteiro (sec. 16) em inglês: Angelic ("I'm just freezing you"), Riven (o servidor; referências discretas a Hoc e Jade), Du ("HAHAHA"), Pkas (confiar na equipe, Charizard), Doge (o amigo e mestre que sumiu sem ser nomeado; "come and take it") |
| Sala do campeão | sem rival nem professor: Doge entrega o título e leva o jogador ao Hall da Fama; Hall da Fama com as falas do Doge |
| Pós-créditos | na 1ª vez no quarto depois do Hall da Fama, o PC apita: dados de Hoc, Riven e Jade apontando o cume acima da Passway e a convocação do Doge (`FLAG_HT_POSTGAME_DATA` 0x68 — a 0x20 parecia livre mas é de um item da Route 101); a escadaria da Passway abre com essa flag |
| Sprites | provisórios oficiais: Angelic = Sidney, Riven = Psychic M, Du = Black Belt, Pkas = Drake, Doge = Wallace |
| QA | `fluxo_cap11.py` (Route 11 e ilha), `fluxo_cap11b.py` (guardas, as 4 salas, Doge, Hall da Fama, FLAG_SYS_GAME_CLEAR), `fluxo_cap11c.py` (créditos → Continuar → quarto → cena do PC → jogo livre); correções que a QA achou: **VAR_ELITE_4_STATE** contava as salas na ordem vanilla (a sala de gelo esperava o valor 2 e não fazia a entrada) — renumerada (Glacia 0, Phoebe 1, Sidney 2, Drake 3); Lugia e Umbreon do Doge sem stall puro (Roost/Toxic → Ice Beam/Shadow Ball); contra o Doge (que troca de Pokémon) o QA lê `gBattleMons[1].species` e escolhe o golpe; **suíte 732/732** (Cap. 1–11: 705; Liga: 24; pós-créditos: 3 — as duas correções de ROM não mudaram nenhum endereço, então a Liga e o pós-créditos rodaram a partir do estado salvo no saguão da mesma suíte) — build 20v |

## 29. Capítulo 12 — Storm Mountain, Cynthia, Tavinho e o epílogo — 20/11/2026

| Item | Estado |
|---|---|
| Acesso | a escadaria da Passway abre com `FLAG_HT_POSTGAME_DATA` (a convocação do Doge no pós-créditos) e continua para o norte numa conexão contínua (trilha x = Passway x + 2); `MAPSEC_MT_CHIMNEY` (ao norte da Passway no mapa da região) virou **STORM MOUNTAIN** |
| Trilha | `MAP_PALM_STORM_TRAIL` 40×50 (General + Lavaridge, chuva com trovões): encosta inferior (patamar 5) com o **Steven** e o Metagross, desfiladeiro (patamar 7 num corredor entre as paredes do patamar 9, cristas de mata dos dois lados) com o **Leon** e o Charizard, o alto (patamar 9); falas do roteiro, cenas únicas sem batalha obrigatória (`FLAG_HT_STEVEN_MET` 0xE9, `FLAG_HT_LEON_MET` 0x1AA); 3 itens; encontros do pós-Liga (Bagon, Shelgon, Druddigon, Snorunt, Scyther e Gible raros, Lv 68–74) |
| Crista | `MAP_PALM_STORM_RIDGE` 36×46: cabana do **posto da Joy** (`MAP_PALM_STORM_CABIN`, interior genérico, Joy cura, Chansey) e placa; dois patamares de pedra solta; a **última escadaria** numa garganta estreita até o cume; a **Cynthia** na boca da garganta (uma rocha fecha o lado livre): pergunta se o jogador volta — SIM faz recuar, NÃO duas vezes → luta (Spiritomb 79, Roserade 80, Togekiss 81, Lucario 82, Milotic 83, Garchomp @ Garchompite 85); depois a Joy sobe e cura, a Cynthia sai da frente (`FLAG_HT_CYNTHIA_DONE` 0x1AB) |
| Cume | `MAP_PALM_STORM_SUMMIT` 24×22: pico de pedra; **Tavinho** (slot `TRAINER_MAXIE_MOSSDEEP`; a luta multi da Mossdeep, inalcançável, passou para outro slot do Maxie): Pelipper 87 (Drizzle), Swampert 88, Scizor 89, Garchomp 90, Urshifu Golpe Fluido 91, Kyogre @ Blue Orb 94 (Reversão Primal na entrada); depois: o **Medalhão de Atlas do jogador** (o da mãe, Cap. 1: "você não vai andar sozinho") faz o Tavinho lembrar; o Doge chega; falas finais do roteiro |
| Epílogo | Tavinho entrega a bola do Kyogre e a Orbe Azul; o Doge voa no Mega Latios; `MAP_PALM_MARINE_EPILOGUE` (layout da Marine Cave End): "Rest, big guy…", o Kyogre é selado; de volta ao cume, a tempestade passou (`VAR_HT_EPILOGUE` 0x409B ≥ 2 deixa trilha, crista e cume ensolarados) e a tela final **"No one has to carry the world alone."** |
| Sprites | provisórios nativos do Emerald: Leon = Tucker, Cynthia = Lucy, Tavinho = Noland (retrato de batalha: Red); os sprites de mapa do FRLG (Cooltrainer M, Red) ficam invisíveis no Emerald |
| QA | `FLAG_HT_QA_GODMODE` (0x1DF, só build não-release, nunca ligada no jogo): o dano no time do jogador fica em 1 — só o `fluxo_cap12b` liga, nas lutas da Cynthia e do Tavinho (um Mewtwo sozinho não vence Primal Kyogre na chuva com 4 Full Restores; o QA confere os scripts, não o balanceamento); `fluxo_cap12.py` (portão, conexão, Steven, Leon, itens, volta) e `fluxo_cap12b.py` (crista, Joy, Cynthia SIM/NÃO, luta, cume, Tavinho, epílogo, tela final); ajustes de QA achados na suíte (os scripts estavam certos; o QA conferia antes do fim das falas): portão da Passway, recuo da Cynthia, virar-e-andar depois de recuar, limite da espera da luta; as lutas longas variam o golpe quando o certo fica sem PP; o campeão Doge também com o godmode de QA (o rodízio por espécie ainda perdia por sorte); **suíte 756/756** (Cap. 1–11 + Liga + pós-créditos: 732; Cap. 12: 9 + 15) — a Liga, o pós-créditos e o Cap. 12 rodaram a partir dos estados da mesma suíte, com a mesma ROM — build 20w |
| Pendências | **decisão do diretor: quem entrega a Key Stone/Mega Ring no pós-jogo** (o cânone só diz que é liberada depois da Liga); sprites próprios; página Hollowtide nos créditos |

## 30. Ferrovia, créditos, estalagem — e a contagem da suíte — 20/11/2026

| Item | Estado |
|---|---|
| **Correção da contagem** | o log da suíte imprime cada conferência **duas vezes** (a linha ao vivo e a do resumo de cada fluxo), e os totais deste documento contavam as duas (`grep -c OK`): "676/676", "705", "732/732", "756/756" eram o dobro do número de conferências. Daqui em diante conta só a linha ao vivo (`grep -c "^OK "`): a **r53** tem **412 conferências, 0 falhas** (Cap. 1–12, Liga, pós-créditos, montanha, Cynthia, Tavinho, epílogo e ferrovia). As conferências em si não mudam: todas passaram nas suítes citadas |
| Ferrovia | as portas das estações (Voltara 26,17; Tradepost 14,7; Ferrália, sede da ferrovia, 28,12), antes fechadas, levam a saguões (layout do 1F da Devon) com bilheteira, dois viajantes e um funcionário na escada da plataforma; trens suspensos até o Vega (`FLAG_HT_VOLTARA_DONE`); a bilheteira oferece as outras duas cidades, uma de cada vez; `fluxo_trem.py` (suspensos no Cap. 4; Voltara → Ferrália → Voltara; portas nos dois sentidos) |
| Créditos | duas páginas depois do título: "Built on — pret / pokeemerald, RHH / pokeemerald-expansion" e "A fan project — POKéMON belongs to Nintendo, Creatures and GAME FREAK"; os créditos originais continuam |
| Estalagem da Passway | o estalajadeiro oferece pernoite (cura o time); o hóspede acompanha a história (estrada aberta/sem energia → trens → trilha do cume) |
| Pavilhão das Estrelas | as duas folhas da porta (46,9)/(47,9), antes sem destino, levam ao interior (layout do 1F do museu da Lilycove, o mesmo prédio de fora); fechado com o lago alto (a porta faz recuar, a placa diz), aberto depois de `FLAG_HT_HORIZON_DONE`; constelações de LUNIA nos quadros (Lantern, Crown, Piplup, Lake Mirror, Wayfarer, Twin Lights — nomes novos, sem tocar nas lacunas do cânone), maquete do telescópio, tábua dos primeiros moradores, réplica da Moon Stone (Route 7), visitantes; a escada do mirante fica com um atendente; `fluxo_pavilhao.py` |
| QA | **r54: 415 conferências, 0 falhas** (Cap. 1–12, ferrovia, estalagem; a saída da estalagem precisou de um toque mais longo no tapete — os últimos fluxos rodaram de novo na mesma ROM) — **build 20x**; r55 (com o pavilhão) em andamento |
