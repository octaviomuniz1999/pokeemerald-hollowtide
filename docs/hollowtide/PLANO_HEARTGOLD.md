# Plano — Pokémon Hollowtide em HeartGold (hg-engine)

Versão de referência do GBA: **23ap** (506/506 testes). O GBA fica congelado como referência jogável do conteúdo
(história, mapas, times, encontros, textos) enquanto a versão DS é construída.

## 0. Decisões do diretor (23/11/2026)

- Mapas: **caminho A** — Lunia montada com a geometria 3D que o HeartGold já tem, eventos e textos por script.
- Arte (modelos, sprites originais, Town Map): **depois do fim da produção**; até lá, placeholders oficiais.
- GBA: **congelado** na 23ap; não se mexe nele por enquanto.

## Estado da Fase 0 (23/11/2026) — concluída

| Item | Estado |
|---|---|
| hg-engine | commit fixo `b578c990` (`hollowtide_ds/hg-engine.commit`); `make` exige `rom.nds` com código **IPKE** (HeartGold EUA) já na leitura do Makefile |
| ROM | HeartGold EUA, **IPKE**, SHA-1 `4fcded0e2713dc03929845de631d0932ea2b5a37`; fora do repositório |
| Build | **ok**: `tools/hollowtide_ds/build.sh` refaz tudo do zero em ~1–3 min e reproduz byte a byte a ROM conferida à mão (0 de 537 arquivos diferentes) |
| Emulador de QA | **ok**: DeSmuME sem tela (`py-desmume`); `ds_intro.py` leva um jogo novo ao quarto em ~1m45 (responde ao que está na tela — menu de tópicos, teclado do nome — em vez de seguir uma sequência fixa: o relógio do DS muda o tempo das falas; 3/3 seguidas); leitura de mapa/posição, entrada, toque, capturas, estados |
| Scripts, eventos e textos como código-fonte | **ok** — o hg-engine tem `make dump_scripts`: os 963 scripts (a/0/1/2) viram `.s`, os 491 arquivos de eventos (a/0/3/2) viram JSON e recompilam **idênticos** ao ROM (só mudam os que editamos e o script comum do próprio hg-engine). Os textos (a/0/2/7) saem pelo `msg_dump.py` (829/829 idênticos; o despejo de texto do hg-engine perde quebras de linha) |
| Prova: texto | **ok** — mensagem do Wii do quarto trocada, vista na tela |
| Prova: script | **ok** — o mesmo objeto passa a dar um Mudkip Lv10 e abrir batalha |
| Prova: treinador | **ok** — Youngster Joey com Fennekin Lv5 (espécie da Gen 6, com sprite) na batalha; a fala de entrada só aparece pela visão do treinador (não testada) |
| Prova: warp | **ok** — via `ndspy` direto na ROM (escada → mapa 66) e via JSON no build (escada → porta da guarita da Route 29) |
| Prova: encontro | **ok** — Route 29 só com Sprigatito (Gen 9) em `data/Encounters.c`: Sprigatito Lv2 selvagem no mato alto |
| Prova: matriz de mapas | **ok** — `matrix.py` (passo depois do `make`, a partir de `matrix.json`): a célula (19,12) da matriz 0 (bloco da guarita da Route 29) recebeu o bloco de New Bark; no jogo o nome continua "Route 29" e a paisagem é a de New Bark. Edita só o NARC da matriz (a/0/4/1) |
| Fluxo | `prova_fase0.py` faz tudo numa passada a partir do estado base (inclui vencer a batalha pelo toque: FIGHT e golpe 2) |
| Lição | estado salvo só vale na ROM em que foi feito: o mapa carregado fica na RAM; toda prova de edição parte de um boot limpo |

**Recomendação: caminho A confirmado.** O que o plano dava como "não coberto" (scripts de evento, NPCs, warps, textos de
mapa) está coberto: tudo vira código-fonte editável, recompilável e testável aqui, como no decomp do GBA. O único
pedaço sem ferramenta continua sendo a geometria 3D (blocos e matriz), que o caminho A reaproveita do HeartGold.

Layout no repositório: `hollowtide_ds/` (patches de conteúdo + ajustes do hg-engine; nada da Nintendo no git) e
`tools/hollowtide_ds/` (build, extração de textos, QA). Ver `hollowtide_ds/README.md`.

## Estado da Fase 1 (23/11/2026)

| Item | Estado |
|---|---|
| Inventário de Lunia | `tools/hollowtide_ds/lunia_inventory.py` → `docs/hollowtide/ds/lunia_inventory.json`: percorre o mundo do GBA a partir do quarto (conexões, warps, warps de script) — 144 mapas, 122 treinadores (slots de Hoenn resolvidos pelos `#define` de `opponents.h`), 23 tabelas de encontro, 7 presentes; fora do percurso: Victory Road e Route 128 (ligações de Hoenn que sobraram na Ever Grande City; no cânone a Route 11 leva direto à Liga e não há rival) |
| Sprites | **sem lacunas** (`docs/hollowtide/ds/SPRITES.md`): as 248 espécies/formas usadas, as Megas/Primal do cânone e as 128 famílias da Pokédex têm batalha, seguidor e ícone no hg-engine |
| Times | **ok** — `tools/hollowtide_ds/convert_trainers.py` → `hollowtide_ds/patches/content/0100-trainers.patch`: os 116 treinadores de Lunia (122 nomes; 6 são aliases do mesmo slot) nos índices 400–515 de HGSS (tabela fixa em `hollowtide_ds/data/trainer_slots.json`; constantes `TRAINER_HT_*` em `data/scr_seq/include/hollowtide_trainers.inc`). Espécie, nível, golpes, item, habilidade (pelo slot quando é a 1/2/oculta), IVs, itens de bolsa e as falas (entrada, derrota, depois) vindas dos scripts do GBA. Classe: líderes/Elite/campeões com classe de HGSS do mesmo papel (título certo na batalha), demais pelo sprite do GBA — placeholders até a arte. IA de especialista em líderes, Elite, campeões e chefes da Team Palm |
| Prova: times | **ok** — batalha contra o Doge (índice 511) no emulador: Meowscarada Lv71 usando Flower Trick, golpes do GBA |
| A conferir | 5 falas com o nome do jogador (`{STRVAR_1 3, 0, 0}`): Doge (derrota, dentro da batalha), Hoc, Abelf e Nami — os scripts da Fase 3 precisam de `buffer_players_name 0` antes; nomes com mais de 10 letras saem abreviados pelo hg-engine (Meowscarada → "Mewscarada") |
| Encontros | **ok** — `tools/hollowtide_ds/convert_encounters.py`: as 23 tabelas de Lunia validadas e convertidas (grama com as mesmas chances por vaga e o nível no meio da faixa do GBA; surf igual; Old/Super Rod exatas, Good Rod 45/40/15 em vez de 60/20/20 — as vagas do DS não permitem; manhã/dia/noite iguais, como no GBA). Cada tabela entra no ENCDATA do mapa de HGSS que hospedar o lugar de Lunia (`hollowtide_ds/data/map_bindings.json`, Fase 2) |
| Prova: encontros | **ok** — Route 2 ligada provisoriamente à tabela da Route 29 (`provas/fase1_encontros`): Wingull Lv11 no mato alto |
| Trocas | **ok** — `tools/hollowtide_ds/npc_trades.py`: as 4 trocas do Tradepost (Kadabra "Kada", Machoke "Muscle", Graveler "Pebbles", Haunter "Boo") nas vagas 0–3 das 13 trocas de HGSS (NARC `a/1/1/2`, aplicado pelo `build.sh` depois do `make`; apelidos/OT no texto 200; constantes `NPC_TRADE_HT_*`) |
| Prova: troca | **ok** no emulador: "Rafa sent over Kada." — mas **a troca com NPC do DS não faz o Pokémon evoluir** (no GBA o Kadabra vira Alakazam ao chegar). Fica para a Fase 3: gancho no hg-engine que chama a evolução por troca depois de `npc_trade_exec` |
| Presentes | os 4 presentes de Lunia (Porygon Lv24, Furfrou Lv27, Eevee Lv30, Rotom Lv40 — `hollowtide_gifts.inc`) viram `give_mon` nos scripts da Fase 3 (prova de `give_mon` já feita na Fase 0). Os iniciais vêm da escolha de inicial do GBA (Snivy/Fennekin/Mudkip), não de `givemon`; os Cyndaquil/Totodile/Chikorita do laboratório são sobra do Emerald |
| Próximo | Fase 2 (ver abaixo) |

## Estado da Fase 2 (23/11/2026)

| Item | Estado |
|---|---|
| Catálogo de HGSS | `hgss_catalog.py` → `docs/hollowtide/ds/HGSS_MAPAS.md` (76 mapas externos na matriz do mundo) e `hgss_seams.py` → `HGSS_EMENDAS.md` (47 divisas andáveis pela colisão dos blocos) |
| Regra de montagem | `docs/hollowtide/ds/FASE2_MAPAS.md`: cada lugar de Lunia em mapas de HGSS já ligados entre si (divisa ou guarita), na ordem de Lunia; um lugar pode juntar células de vários mapas (os eventos usam coordenadas da matriz inteira); sem cavernas/florestas de HGSS como passagem |
| Fatia vertical (Cap. 1) | Dawnmere = New Bark (+ casa do jogador e laboratório do Elm), Route 1 = Route 29, Harvestvale = Cherrygrove; encontros da Route 1 já ligados à Route 29 e compilando com times e trocas |
| Nomes de lugar | **ok** — `tools/hollowtide_ds/place_names.py` (texto 279, um nome por MAPSEC; fonte `hollowtide_ds/data/place_names.json`): Dawnmere Village, Route 1, Harvestvale. No emulador: placa "Route 1" ao chegar na Route 29 e Fletchling Lv4 selvagem (tabela da Route 1 de Lunia) — `provas/fase2` |
| Músicas | ficam as de HGSS por enquanto (New Bark, Route 29, Cherrygrove): no GBA o cânone usou faixas existentes por atmosfera; os temas próprios entram na Fase 5 |
| Iniciais | **ok** — `0050-starters.patch` (tabela do hg-engine em `src/starters.c`: Snivy, Fennekin, Mudkip, na ordem Grama/Fogo/Água das bolas de HGSS) e texto 190 da tela de escolha com o Prof. Alex (`tools/hollowtide_ds/text_patch.py` + `hollowtide_ds/data/texts.json` → `0500-texts.patch`, para qualquer texto de HGSS). No emulador (`provas/fase2_inicial`): as três bolas mostram Snivy/Fennekin/Mudkip, a escolha do Mudkip entra no time (Mudkip Lv5 na batalha seguinte). Toque: bola lateral gira a roda, bola da frente escolhe/confirma, tocar fora cancela |
| Medalhão de Atlas | **ok** — `tools/hollowtide_ds/items.py` + `hollowtide_ds/data/items.json` → `0060-items.patch`: a vaga do Relic Gold (o GBA já usava esse ícone) vira o Medalhão de Atlas (itens-chave, não pode jogar fora, preço 0, nome/descrição do GBA); constante `ITEM_ATLAS_MEDALLION` |
| Casa do jogador | **ok** — `0600-dawnmere-house.patch` (térreo, T20R0201): na primeira descida a mãe chama, entrega o Medalhão ("A obtained an Atlas Medallion!", vai para os itens-chave) e diz as falas do GBA; a cena do Pokégear do HGSS sai, mas as flags de bolsa/cartão/salvar/opções continuam. Falar com a mãe: antes do inicial, "Prof. Alex stopped by earlier"; depois, cura o time. Conferido no emulador |
| Textos do GBA | `tools/hollowtide_ds/gba_text.py`: o `texts.json` aceita `{"gba": "Label"}` e converte (\\p → \\f, \\l → \\r, {PLAYER} → buffer 0, ' → ’, nomes em caixa mista: MOM → Mom, PROF. ALEX → Prof. Alex, POKéMON → Pokémon) |
| Laboratório | **ok** — script reescrito em `hollowtide_ds/patches/content/overlay/data/scr_seq/scr_seq_0843_T20R0101.s` (o `build.sh` copia `overlay/` por cima do despejo) + `0610-dawnmere-lab-events.patch` (sem policial, Lyra e gatilhos de chão) + texto 543 do GBA. No emulador, do quarto ao laboratório: falar com o Prof. Alex → falas do GBA → tela das bolas → "A fine choice… It's a Pokédex" → Pokédex, Poké Balls, Potions → missão (Route 1, Harvestvale, Nevard); o inicial já segue o jogador. Sem cena automática na entrada |
| Dawnmere (exterior) | **ok** — script reescrito em `overlay/data/scr_seq/scr_seq_0842_T20.s` + `0620-dawnmere-events.patch` + texto 542: guia, vizinha e o morador do mirante com as falas do GBA, 4 placas (laboratório, casa, vizinhos, vila); saída oeste (7 tiles) travada sem Pokémon com a fala do GBA e um passo de volta; sem a cena da Lyra/Marill, Elm, Silver, mãe na rua e o Potion escondido do HGSS; os gatilhos de quadro do header mudam a variável para não repetir |
| Direções adaptadas | no DS a Route 1 (Route 29) fica a **oeste** de Dawnmere: placa da vila "West exit" (GBA: East) e missão do Prof. Alex "Follow Route 1 to the west." (GBA: east, depois atravessar o rio ao sul). Registradas em `texts.json` (`replace` + `_por_que`) |
| QA do Cap. 1 | `tools/hollowtide_ds/qa_cap1.py`: quarto → mãe e medalhão → Dawnmere → saída barrada sem Pokémon → laboratório → inicial → saída oeste → Route 1 (mapa 33). **ok** |
| Route 1 | **ok** — overlay do script da Route 29 + `0630-route1-events.patch` + texto 373: andarilho e placas do GBA; Kai e Min como treinadores com visão (`_std_npc_trainer` + falas do `Trainers.c`); Potion mantido; tutorial da Lyra, NPCs de Johto, árvores de Cut, Apricorn e Nugget escondido fora. No emulador: Kai vê o jogador e diz a fala do GBA; Min também; derrota leva para casa e a mãe cura. **Pendente:** a árvore de Oran do GBA (HGSS não tem árvore de berry igual) |
| Harvestvale | overlay do script de Cherrygrove + `0640-harvestvale-events.patch` + texto 550: fazendeiro (cena de chegada pelo leste), recruta da Team Palm no quiosque (sudoeste) com a chave, válvula na margem oeste, 8 placas do GBA, porta do ginásio (casa R0401) fechada até a água voltar, saída norte (Route 2) fechada até vencer o Nevard; `VAR_SCENE_CHERRYGROVE_CITY_OW` 0 chegada / 1 ginásio fechado / 2 água / 3 Nevard. Conferido: chegada, porta fechada, batalha do recruta, saída norte fechada. Corrigido: `trainer_battle` por script não marca o treinador como vencido (`settrainerflag`) |
| Ginásio do Nevard | interior do ginásio da Erika (placeholder) + overlay + `0650-nevard-gym-events.patch` + texto 492: Josh, Tommy, Marc (visão) e Nevard; Harvest Badge (1ª insígnia) e TM09 Bullet Seed. **Pendente:** quebra-cabeça das comportas do GBA; nome da insígnia no menu ("Zephyr Badge" do HGSS) |
| Flags de Lunia | `tools/hollowtide_ds/flags.py` → `hollowtide_ds/data/flags.json` + `hollowtide_flags.inc`: flags de eventos de Kanto (exclusivas de um script de mapa de Kanto, fora do código C; conferido a cada execução) |
| Textos do hg-engine | `texts.json` aceita `"engine:NNN"` com trocas registradas (040: a mãe depois de uma derrota cita o Prof. Alex, não o Elm) |
| QA | `qa_cap1.py` vai do quarto a Harvestvale e testa os eventos de lá; `provas/qa_forte` dá um Lucario Lv50 só no build de QA (o robô luta mal; a curva do jogo não muda) |
| Próximo | terminar o QA de Harvestvale (válvula → ginásio aberto) e o QA dentro do ginásio (treinadores, Nevard, insígnia, TM, saída norte liberada); depois a Route 2 |

## 1. O que o hg-engine resolve e o que não resolve

Fonte: README e wiki do `BluRosie/hg-engine` (lidos em 23/11/2026).

| Área | hg-engine | Observação |
|---|---|---|
| Base | HeartGold **inglês**, `rom.nds` na raiz; `make` gera `test.nds` | build em Linux (gcc-arm-none-eabi, cmake, python, rust), WSL, macOS ou Docker — roda neste container |
| Batalha | mecânicas modernas, tipo Fada, habilidades ocultas, **Mega e Primal**, climas novos, itens e golpes de gerações novas | tudo o que o cânone usa (Mega Charizard X, Mega Latios, Mega Garchomp, Primal Kyogre) está na lista |
| Espécies | dados de todas até Gen 9 (Teal Mask); **sprites ainda incompletos** | conferir uma a uma as ~150 espécies da Pokédex de Lunia (Fennekin, Snivy, Zorua de Hisui, Dhelmise, Meowscarada, Urshifu…) |
| Dados | C e JSON editáveis em `data/`: `Species.c`, `learnsets/learnsets.json`, `Evolutions.c`, `Encounters.c`, `Trainers.c` (time e falas juntos), sprites em `data/graphics/sprites` | dá para gerar por script a partir dos dados do GBA (times, encontros, presentes) |
| **Mapas** | **não cobre** a geometria | mapas DS são blocos 32×32 com modelo 3D (NSBMD), colisão/permissões e uma matriz de blocos por área |
| **Scripts de evento e textos de mapa** | **cobre** (descoberto na Fase 0) | `make dump_scripts` + `BUILD_DUMPED_SCR_SEQ`/`BUILD_DUMPED_EVENTDATA`: scripts em `.s`, eventos (NPCs, warps, gatilhos, placas) em JSON, textos em `.txt` |
| Licença | uso livre **sem dinheiro envolvido**; nada atrás de paywall; copiar os créditos (`CREDITS.md`) | distribuição por patch xdelta, como hoje |

## 2. A decisão que define o projeto: como fazer os mapas

Os editores usuais de mapas e eventos de DS (DSPRE e Pokémon DS Map Studio) são programas gráficos de Windows; não
rodam neste container. Há três caminhos:

- **A — Reaproveitar a geometria de HGSS (recomendado para começar).** Monto Lunia na matriz de mapas com blocos 3D
  que o jogo já tem (cidades, rotas, cavernas de Johto/Kanto), reorganizados para a estrutura consolidada de Lunia. Eventos, warps,
  NPCs, cabeçalhos (nome, música, clima) e textos por script (Python + `ndspy` para abrir e regravar os arquivos do
  ROM). Totalmente automatizável e testável aqui; o visual lembra HGSS até haver modelos próprios.
- **B — Modelos 3D próprios.** Mapas desenhados no Pokémon DS Map Studio (ou Blender) por alguém com Windows — você ou
  um artista — e eu integro, coloco eventos e testo. Mais fiel à identidade de Lunia; depende de arte.
- **C — Híbrido.** Começa em A para ter o jogo inteiro jogável e troca bloco a bloco por modelos próprios (B) nas
  cidades principais.

## 3. Fases e pontos de verificação

**Fase 0 — Viabilidade (1–2 rodadas).** Nada de conteúdo até isto passar.
- Clonar o hg-engine, compilar com a sua ROM de HeartGold (EN) e gerar `test.nds` aqui.
- Montar o harness de QA de DS (emulador sem tela com leitura de memória e entrada — DeSmuME via `py-desmume`, ou
  melonDS), equivalente ao `mgba_runner` atual: ligar, andar, ler mapa/posição/flags, tirar capturas.
- Provas de ponta a ponta: trocar um texto, um treinador e uma tabela de encontro e ver no emulador; mudar um warp e
  um NPC num mapa existente via `ndspy`; trocar um bloco da matriz.
- Relatório: o que funcionou, o que não, e a recomendação final A/B/C.

**Fase 1 — Dados de Lunia.** Conversores do GBA para o hg-engine: times (`trainers.party` → `data/Trainers.c`, com os
golpes definidos), encontros por mapa (`wild_encounters.json` → `data/Encounters.c`), presentes e trocas, itens; checagem
de sprites das espécies da Pokédex (lista do que falta); configuração de Mega/Primal, Fada, Exp. Share e curva de
níveis (o que o GBA já balanceou: Route 1 até Lv 9, Breezeport 14–18, área 80+ do cume).

**Fase 2 — Esqueleto do mundo.** Matriz de Lunia na estrutura consolidada: Dawnmere, Harvestvale, Breezeport, Ferrália…
até a Liga e a Storm Mountain, com conexões, nomes de lugar, músicas e clima. Fatia vertical: **Cap. 1 jogável do começo ao
Nevard**, com QA no emulador, antes de seguir.

**Fase 3 — Eventos e história.** Portar os scripts dos capítulos (os scripts do GBA não rodam no DS: a linguagem de
eventos é outra). Converter o que for mecânico (falas, flags, treinadores com visão, itens) e reescrever à mão as
cenas (Lela, Vega, Abelf, Liga, Cynthia, Tavinho, epílogo). Os textos em inglês já escritos vêm junto.

**Fase 4 — Capítulos 1 a 12 e rotas opcionais**, um por vez, cada um com fluxo de QA, como no GBA.

**Fase 5 — Arte e som.** Sprites de treinador (no DS há o sprite oficial da Cynthia de Platinum), personagens
originais (Elite, Tavinho, Leon), Town Map de Lunia, músicas (os MIDIs da Cynthia viram sequências do DS) e, no
caminho B/C, os modelos 3D.

**Fase 6 — Entrega.** Patch xdelta sobre a ROM de HeartGold (EN), LEIA-ME, créditos do hg-engine.

## 4. O que já serve do projeto GBA

- Cânone, DECISOES, POKEDEX_LUNIA, curva de níveis e os relatórios de balanceamento.
- Todos os textos em inglês (diálogos, placas, treinadores), times e golpes, encontros, presentes e trocas.
- A estrutura consolidada dos mapas (renderizações, posições de eventos e conexões) como planta baixa para a matriz DS.
- Os fluxos de QA como roteiro do que testar em cada capítulo (a ferramenta muda, os casos ficam).

## 5. O que preciso de você

1. **Uma ROM de Pokémon HeartGold em inglês** (de um cartucho seu), enviada aqui como na base do Emerald.
2. **Caminho dos mapas:** A, B ou C.
3. **Arte:** quem faz os modelos 3D e os sprites originais, se for o caminho B/C.
4. **O GBA:** fica congelado na 23ap como referência, ou ainda quer ajustes nele?

## 6. Riscos

- Mapas e eventos de DS sem editor gráfico neste ambiente: mitigado pelo caminho A e pela Fase 0.
- Sprites de espécies novas ainda incompletos no hg-engine: lista de lacunas na Fase 1; espécies sem sprite ficam
  fora até haver arte.
- Pokémon seguidores: HGSS tem seguidores só das espécies originais; o suporte a espécies novas precisa ser conferido
  (página "Overworld System" do wiki, ainda não lida).
- Escala: o DS dá mais trabalho por mapa que o GBA; a fatia vertical do Cap. 1 mede o ritmo real antes de prometer
  prazos para o resto.
