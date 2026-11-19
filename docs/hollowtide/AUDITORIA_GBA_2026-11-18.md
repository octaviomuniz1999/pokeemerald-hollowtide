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
