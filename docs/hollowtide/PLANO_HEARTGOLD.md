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
