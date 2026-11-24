# CP-DS-03B — Plano de setores: Dawnmere Village e Route 1 (24/11/2026)

Primeira localidade original, depois da prova do CP-DS-03A. Este documento define **a função de cada setor antes
de construir** (pedido do diretor). Referência autoral prioritária: os mapas do GBA 23ap, Dawnmere = `LittlerootTown`
(34×29) e Route 1 = `Route101` (40×53, alongada de norte a sul). Referências de composição do DS: Route 30 (casas,
árvores, mato alto em ilhas), Route 38 (cercas e pastos), Route 47 (desníveis). Nenhum mapa existente é copiado.

## 1. Geografia (do GBA, confirmada pelas decisões do diretor)

```
             [ Route 1 — setor N ]   ← entra pelo oeste, vindo de Dawnmere
[Dawnmere] → [ Route 1 — setor C ]   (canal e ponte)
             [ Route 1 — setor S ]
             [ Harvestvale        ]   ← entra pelo norte
```

- Dawnmere tem uma só saída, a leste. No GBA ela é a placa "East exit: Route 1". No DS ela volta a ser **leste**:
  as adaptações para "oeste", feitas no protótipo, deixam de valer quando este mapa entrar.
- A Route 1 corre **norte → sul** em três setores de 32×32 (um bloco cada), como pede a decisão do diretor e como
  é o `Route101` do GBA. Fala do Prof. Alex no GBA: "Follow Route 1 east, then head south across the river."
- Harvestvale fica ao sul da Route 1. A Route 2 sai do sudeste de Harvestvale (decisão do diretor); fica para a
  etapa seguinte.

## 2. Setores e função

| Setor | Função na jogabilidade | Composição (do `Route101` do GBA, adaptada ao DS) | Eventos de Lunia já existentes |
|---|---|---|---|
| **Dawnmere** (1 bloco) | vila inicial: casa, laboratório, vizinhos; ensina a andar e a ler placas; saída única a leste, travada sem Pokémon | laboratório do Prof. Alex ao norte, num pátio cercado com canteiros; lago cercado ao nordeste; casa do jogador e a dos vizinhos no centro; caminhos de terra em grade; laguinho a oeste; floresta na borda sul; flores nos cantos das casas | mãe, Prof. Alex, guia, vizinha, mirante, 4 placas, trava da saída (todos já portados, CP-DS-01/02) |
| **Route 1 N** | primeiro contato com mato alto e treinadores; espaço aberto e seguro | entrada pelo oeste por um caminho entre flores; casa isolada a oeste com cerca e horta; caminho de terra sinuoso descendo para o sul; lagoa grande a nordeste; ilhas de mato alto a leste; árvores soltas e em pares | andarilho, Kai (visão), Oran (árvore pendente) |
| **Route 1 C** | travessia: o canal cortando a rota de leste a oeste, a ponte como ponto de passagem obrigatório | canal largo de margens de pedra (água animada), ponte de madeira no centro, árvores e postes na margem norte; um degrau de altura (a ponte acima da água) | Min (visão) perto da ponte; placa "Route 1 / South: Harvestvale" |
| **Route 1 S** | chegada ao campo agrícola: prenuncia Harvestvale (irrigação, plantações) | lagoa a sudoeste com saída de água; plantação cercada a sudeste (horta, espantalho); mato alto entre as duas; caminho de pedra na saída sul; desnível suave com rampa | placa "Route 1 / South: Harvestvale"; Potion |

Para cada setor, antes de gerar: grade de colisão (bloqueado, mato alto, água, livre), alturas, materiais e objetos,
conferidos nas divisas (as colunas abertas e a altura têm de ser iguais nos dois lados).

## 3. O que o gerador precisa ganhar (a partir de `mapa_teste.py`)

| Recurso | Para quê | Como |
|---|---|---|
| desenho por grade de texto | um setor = uma grade 32×32 legível no repositório, revisável pelo diretor | letras por tipo de tile (grama, caminho, mato alto, água, flor, árvore, cerca, penhasco, rampa) e um mapa de alturas |
| água (lagoa, canal) | Route 1 C e S, lagos de Dawnmere | materiais `pond_on`/`pond_edge`/`pond_line` e `sea_*` da área 2, com borda; colisão de água (comportamento de surf) |
| penhasco com borda e cantos | desníveis como os do HGSS (Route 47) | peças do `wall01_*`/`cliff01` do HGSS, copiadas do bloco doador e posicionadas, em vez de faces retas |
| variação de árvore | florestas sem repetição | os vários quads de árvore do HGSS (`tree01`, `_re`, `_un`) em carimbos 2×2 e 4×2 alternados |
| cercas, flores, horta | Dawnmere e Route 1 S | `fence_a/b`, `flower01-03`, `grass02`; casas e postes pela lista de construções da área (a/0/4/3) |
| header e célula próprios | sair da célula da Route 39 do teste | células livres da matriz 0 (linhas 13-16, abaixo de Dawnmere/Route 29, hoje vazias) + headers de Lunia; os eventos já portados mudam de coordenada |

## 4. Decisões abertas para o diretor

1. **Onde na matriz:** proponho as células livres abaixo do protótipo atual (linhas 13-16 da matriz 0) para os
   4 blocos (Dawnmere + 3 setores). O protótipo do caminho A fica intacto até a troca. A alternativa é substituir
   direto os blocos de New Bark e da Route 29.
2. **Dawnmere entra junto?** Proponho começar pela Route 1 N (setor de grama, sem água) para estabilizar o gerador
   v2. Depois vêm a Route 1 C (água e ponte), a S e Dawnmere.
3. **Saída de Dawnmere:** volta a ser leste, como no GBA, com as placas e falas do GBA sem adaptação.

## 5. Rascunho do setor N (24/11) — funciona no jogo; qualidade visual ainda básica

`hollowtide_ds/provas/cp03b/rota1_n.txt` (grade) → `mapa_grade.py` → bloco 11, na célula (22,12): vizinha leste de
Dawnmere, da Route 27, livre no protótipo. Só na build de prova, sem mexer na matriz definitiva. Materiais da área 2,
de 4 blocos doadores (New Bark e Route 29/Cherrygrove). No DeSmuME (`qa_cp03b.py`) passaram:
- entrada pelo oeste (712, 390);
- caminho sinuoso até o fim da área de prova (721, 414);
- colisão contra a lagoa (721, 391), contra uma árvore (712, 408) e contra o fim do caminho.

Capturas: `CP-DS-03B_rota1n.png`, entregue ao diretor.

Melhorado (24/11):
- bordas do caminho com as peças do HGSS (`road01_r`): faixa de 1 tile do lado da grama (u 250 → 6) e cantos externos
  com a outra metade da textura, como na Route 29;
- caminho redesenhado em trechos retos com curvas em L, de 3 tiles de largura. O desenho anterior, em degraus de
  1 tile, gerava dezenas de cantos sobrepostos;
- sentido do v das bordas como na Route 29: caminho ao norte +x, ao sul −x, a leste +z, a oeste −z. Espelhada, a
  textura fazia riscos em diagonal.

- cercas como as de New Bark (`fence_b`: trecho horizontal inclinado, trecho vertical em faixa) e uma horta cercada
  com três tipos de flor (`flower01-03`, alinhamento de UV corrigido como o do HGSS).

Ainda não está no padrão artístico pedido:

- a casa da horta (só entra com interior funcional);
- (resolvido) cantos da lagoa: convexos e côncavos com o perfil da margem girado em volta da quina.

Ao sul da célula de prova aparece o mar do bloco vazio; no definitivo ali fica o setor C.

## 6. Decisões do diretor (24/11) e plano de execução

O diretor deixou as células comigo; a geometria segue o GBA à risca; a saída de Dawnmere é a leste.

**Conversão fiel.** Cada mapa do GBA (`LittlerootTown` 34×29 = Dawnmere, `Route101` 40×53 = Route 1, `OldaleTown`
39×37 = Harvestvale) é convertido tile a tile para a grade do gerador:
- tabela explícita metatile do GBA → letra da grade;
- alturas pelos bits de elevação;
- construções do GBA → modelos de construção da área com a porta no tile do warp;
- NPCs, placas e gatilhos nas posições do `map.json` do GBA.

**Ligações do GBA, que viram divisas naturais no DS:**
- saída leste de Dawnmere (x 33, linhas 21–22) ↔ entrada oeste da Route 1 (linhas 4–5);
- saída sul da Route 1 (colunas 9–10, linha 52) ↔ entrada norte de Harvestvale (colunas 8–11, linha 0).

**Células (decisão minha).** Um só desenho contínuo, recortado em blocos de 32×32, nas linhas 13–16 da matriz 0
(livres, logo abaixo do protótipo):
- Dawnmere a oeste;
- a Route 1 encostada no leste de Dawnmere, deslocada 17 linhas para baixo (a divisa fica nas mesmas linhas do GBA);
- Harvestvale logo abaixo da Route 1, 1 coluna à direita.

Cada célula recebe o header do mapa que ocupa a maior parte dela. O protótipo do caminho A fica intacto até a
troca.

**Etapas:**
1. tabela de metatiles + conversor → desenho global → blocos;
2. Dawnmere na build de prova (visual, colisão, alturas);
3. eventos de Dawnmere nas posições do GBA;
4. Route 1;
5. Harvestvale;
6. troca do protótipo pela versão original na build de conteúdo, com QA completo do Cap. 1.

### Andamento (24/11, à tarde)

Etapa 1 feita e testada no DeSmuME (`provas/cp03c`, `qa_cp03c.py`):
- `gba2grade.py` converte Littleroot → Dawnmere e Route101 → Route 1, com a tabela de metatiles e esta regra de
  fidelidade: sem colisão no GBA, o tile é andável no DS.
- `mapa_global.py` gera a malha do desenho inteiro, reparte por bloco e acrescenta 16 blocos novos (676–691) nas
  células (21,13)–(24,16) da matriz 0. Cada célula recebe o header do mapa que ocupa a maior parte dela
  (Dawnmere 60, Route 1 33, Harvestvale 67).
- Orçamento de vértices: faixas de margem e de borda de caminho juntadas em trechos de até 4 tiles, perfis
  reduzidos e cantos em 1 segmento. O bloco mais pesado tem ~2,3 mil vértices, como os do HGSS.
- No jogo, com o atalho de QA do PC, a Dawnmere convertida aparece com ruas, cercas, canteiros, o pátio elevado do
  laboratório e o lago. A saída leste (x 707) leva à Route 1 (header 33), e a Route 1 aparece com florestas,
  caminhos floridos, lago, canal e ponte. A ponte é atravessável; por enquanto é uma faixa de terra, sem modelo de
  ponte.
- A fresta preta nas divisas de bloco foi fechada nas divisas verticais: o chão avança 1/16 de tile.

Construções (24/11, fim da tarde), testadas no DeSmuME (`qa_cp03c.py`, mesmas 8 paradas, todas ok):
- `gba2grade.py` (tabela `CONSTRUCOES`) põe um modelo do HGSS sobre cada planta do GBA, com a porta no tile do
  warp. A colisão é a união da planta do GBA com a do modelo. O tile da porta vira D (0x69).
- Casa do warp MAYS_HOUSE → `wk_hhouse`. Fica com a porta em (20,16), como no GBA.
- Casa do warp BRENDANS_HOUSE → `wk_h01`. Porta em (2,9), como no GBA.
- As duas casas sem porta do GBA → `yo_h01` e `yo_h02`, com a porta decorativa e bloqueada.
- Laboratório do Prof. Alex → `mst_okl` (o laboratório de Pallet).
  - O `wk_labo` de New Bark tem a porta 2 tiles a oeste do centro e não cabe na planta.
  - O `mst_okl` cabe exatamente nas colunas 10–16 do GBA. Como a porta dele é central, ela fica 1 tile a oeste do warp
    do GBA (14,8 → 13,8), e a escada do pátio vai junto (14,9 → 13,9, agora uma rampa).
  - O modelo e a porta (0x13A, 0x137) entram na lista de construções 0 (a/0/4/3), que é a lista da área 2.
- Casa da horta da Route 1 → `wk_hhouse`, com a porta decorativa no tile do GBA.
  - A casa de Pallet (telhado vermelho, mais parecida) ficou sem textura no jogo: a lista de construções só tem VRAM
    para mais dois modelos.
- A linha escura na divisa horizontal era a altitude da matriz. As células da linha 13 tinham altitude 1–2, restos
  da Route 29, e as de baixo tinham 0. O desenho global agora zera a altitude das células que ocupa.

Eventos de Dawnmere (etapa 3, 24/11), na build de prova (`provas/cp03c`, patches 0922/0923 gerados por
`eventos_gba.py`). Os eventos já portados no CP-DS-01/02 continuam com os mesmos scripts e textos; só mudam para os
tiles do `LittlerootTown` do GBA:
- warps: a casa do jogador (T20R0201) vai para a porta de BRENDANS_HOUSE (2,9), onde o jogo novo do GBA começa. O
  laboratório (T20R0101) vai para a porta do modelo (13,8), e a casa vizinha (T20R0301) para a de MAYS_HOUSE (20,16).
  Os dois warps do HGSS sem par no GBA ficam nas portas decorativas, que são bloqueadas;
- as 4 placas nos tiles do GBA, com o modelo de placa do HGSS (`board_b`). A placa do mirante (`Palm064_RiverLookout`)
  tem só o modelo: o texto dela ainda não foi portado;
- guia, vizinho e mirante nos tiles do GBA;
- trava da saída a leste, numa coluna inteira (x 31, a última da célula de Dawnmere). O passo de volta agora é para
  oeste;
- a placa da Route 1 (script 19, do CP-DS-01) sai de Dawnmere, porque no GBA ela não fica lá. Volta na etapa 4.

`qa_cp03d.py` testa tudo pelo fluxo do jogo, sem atalho. Passou:
- sair da casa pela porta do GBA (676,428);
- ler a placa da casa ("A's House");
- a trava sem Pokémon (fala do GBA e um passo para oeste, 702);
- ler a placa do laboratório;
- entrar no laboratório pela porta nova e receber o inicial do Prof. Alex;
- sair dele em (687,427);
- passar pela saída leste até a Route 1 (header 33), com o inicial seguindo.

Capturas: `CP-DS-03B_eventos_dawnmere.png`.

Notas:
- As colunas 32–35 de Dawnmere caem na célula de header da Route 1: o nome do lugar muda 4 tiles antes da divisa do
  GBA.
- O guia anda (tipo de movimento do HGSS), e o GBA o deixa parado olhando para baixo. Acertar na troca.
- As falas com direções adaptadas ao protótipo ("to the west"…) voltam ao texto do GBA na troca (etapa 6).

Route 1 e Harvestvale (etapas 4 e 5, 24/11), na build de prova (`provas/cp03c`).
- Eventos da Route 1 (patch 0924, `eventos_gba.py`) nos tiles do `Route101` do GBA:
  - andarilho, Potion e as placas norte e sul;
  - Kai e Min parados, olhando para o lado do GBA, com o alcance de visão do GBA.
  - Os tipos de movimento do HGSS (14 cima, 15 baixo, 16 esquerda, 17 direita) foram conferidos nos eventos
    originais. O guia, o vizinho e o mirante de Dawnmere também ficam parados olhando para baixo, como no GBA.
- Harvestvale:
  - tabela de metatiles do `OldaleTown`: árvores grandes, terra arada, areias e construções dos tilesets General e
    secundário. Nenhum metatile ficou sem tabela;
  - construções nas portas do GBA: ginásio do Nevard → `ta_gym` (o de Celadon, tipo Planta), Centro → `pc`,
    Mart → `fs`, casas → `wk_hhouse` e `kn_h01`;
  - lista de construções 0: entram o ginásio e a porta de ginásio, e sai o `wk_labo` de New Bark, sem uso com a
    Dawnmere original. O total de texturas fica em 51.200 bytes, abaixo do original.
- `qa_cp03d.py`, com o Tyranitar de `provas/qa_forte`: o inicial de nível 6 perdeu para o Kai com o robô. Passou em
  tudo, do quarto até o Mart de Harvestvale:
  - placa norte, andarilho, Potion;
  - Kai e Min, que veem o jogador e lutam;
  - placa sul;
  - entrada em Harvestvale (header 67) e as ruas entre casas, ginásio, Centro e Mart.
- Capturas: `CP-DS-03B_eventos_dawnmere.png`, `CP-DS-03B_route1_harvestvale.png`.

Eventos de Harvestvale (24/11, noite), nos patches 0925/0926 gerados por `eventos_gba.py`. Vão para os tiles do
`OldaleTown` do GBA:
- o fazendeiro, parado olhando para a esquerda, e o recruta do quiosque;
- as 8 placas;
- a válvula, que no GBA é a placa da água (`Palm062_WaterSign`, 27,23);
- os 5 warps: ginásio, Centro, Mart, `HOUSE1` e `HOUSE2`;
- a chegada (linha 2, colunas 8–11);
- a trava do ginásio, no tile abaixo da porta;
- a saída para a Route 2, que volta a ser **ao sul** como no GBA (`Palm080_LeaveColheita`, 17–19, 35). O passo de
  volta dela agora é para cima.

`qa_cp03d.py` testou a história de Harvestvale pelo fluxo do jogo. Passou, junto com o resto (13 checagens):
- o fazendeiro chama na chegada;
- placa de boas-vindas;
- ginásio fechado (fala e um passo para baixo);
- batalha com o recruta;
- válvula ("A turned the valve!");
- saída sul fechada antes do Nevard (um passo para cima);
- ginásio aberto depois da água (interior do Nevard).

Capturas: `CP-DS-03B_eventos_harvestvale.png`.

### Etapa 6 (24/11, noite): troca do protótipo na build de conteúdo

Dawnmere, a Route 1 e Harvestvale originais estão agora na **build de conteúdo**:
- `patches/content/land.json`: o desenho global e a lista de construções;
- `0700`–`0704`: os eventos nas posições do GBA;
- `0705`: a ponte provisória.

Os mapas do caminho A (New Bark, Route 29, Cherrygrove) ficam nas células antigas, sem eventos e inalcançáveis.

- **Textos:** as 11 falas e placas que tinham direções adaptadas ao protótipo voltam ao texto do GBA (`texts.json`,
  sem `replace`): mãe, missão, guia, placa da vila, trava, andarilho, placas norte e sul da Route 1, boas-vindas e
  estrada fechada de Harvestvale. As adaptações da Route 2 e de Breezeport ficam, porque esses mapas continuam no
  protótipo.
- **Ponte provisória** (`ponte_route2.py`, 0705). A Route 2 original ainda não existe:
  - depois do Nevard, a saída sul de Harvestvale (GBA) leva ao começo da Route 2 do protótipo (548,382);
  - descendo a Route 2, a última linha antes das células antigas leva de volta à saída sul de Harvestvale.
  - Sai quando a Route 2 for convertida.
- **QA** (`qa_cp03d.py --cap1`, build de conteúdo + `provas/qa_forte`, ROM recém-construída). Passou nas 18 checagens,
  do quarto até Breezeport:
  - porta da casa, placas, trava;
  - laboratório e inicial;
  - Route 1 (Kai, Min, placas);
  - Harvestvale (chegada, ginásio fechado, recruta, válvula, saída sul fechada, ginásio aberto);
  - Nevard e a volta pela porta do GBA;
  - a ponte nos dois sentidos;
  - a Route 2 do protótipo até Breezeport (5 batalhas).
  - Capturas: `CP-DS-03B_etapa6_cap1.png`.
- **Falha registrada:** na primeira tentativa, a build falhou num trecho do 0705 (arquivo sem quebra de linha no fim)
  e o QA rodou numa ROM antiga. Os geradores de patch agora escrevem a marca `\ No newline at end of file`, e a
  sequência build → QA para no primeiro erro.

### Route 2 original e nova posição na matriz (24/11, noite)

**Um header por célula.** Cada célula de 32×32 tem um só header: zona de eventos, encontros e música. Com as divisas
do GBA fora das divisas das células, as últimas 8 linhas da Route 1 caíam numa célula de Harvestvale, e por isso:
- a placa sul da Route 1 não lia;
- o mato alto daquele trecho ficava sem encontros.

O QA conferia só a posição e não pegou; a falha foi achada ao planejar a Route 2.

**Nova posição.** O desenho foi para o canto superior esquerdo da matriz 0, células (0,0)–(3,5), vazias no HGSS, onde
cabe a cadeia vertical do GBA até Breezeport. Ele fica deslocado (30,21) para que quase toda célula tenha um mapa só:
- Dawnmere na coluna de blocos 1;
- a Route 1 nas colunas 2–3;
- Harvestvale na linha 3;
- a Route 2 nas linhas 4–5.

Sobram as 5 primeiras linhas de Harvestvale (árvores e caminho) numa célula da Route 1. Por isso o fazendeiro e o
gatilho da chegada descem 3 linhas, a única adaptação. A trava de Dawnmere volta ao tile exato do GBA (33, 21–22).
`tools/hollowtide_ds/lunia_mundo.py` dá a origem de cada mapa do GBA, e os geradores e os QAs usam coordenadas do GBA
por mapa.

**Route 2** (`PalmRoute02`, 40×48), convertida abaixo de Harvestvale como no GBA:
- **Mapa:**
  - ressaltos de pulo para o sul (`v`, 0x803B, com uma beirada desenhada);
  - o cercado elevado com a escada como rampa (alturas calculadas no desenho inteiro, porque a rampa termina na
    divisa de bloco);
  - a areia e a poça rasa como chão andável;
  - a casa de porta trancada (`yo_h01`).
- **Headers:** R30 nas linhas 0–31 do GBA e R31 nas 32–47 (`headers_celula` no `land.json`), as zonas que já eram a
  Route 2 do protótipo.
- **Eventos** (0706–0708):
  - Liang, Mei Lan, Qin, Potion e as placas norte e sul nos tiles do GBA;
  - a porta trancada, com a fala do GBA no banco da R31;
  - a saída sul leva à guarita do protótipo, e dali a Breezeport. É a nova ponte provisória, até Breezeport ser
    convertida;
  - a ponte antiga (0705, saída sul de Harvestvale → Route 2 do protótipo) saiu: agora se desce de Harvestvale para
    a Route 2 a pé.
- **Texto:** a placa norte da Route 2 volta ao GBA ("North: Harvestvale").

**QA** (`qa_cp03d.py --cap1`, build de conteúdo + `qa_forte`). Passou nas 21 checagens, do quarto até Breezeport:
- a placa sul da Route 1 agora lê;
- Route 2 a pé desde Harvestvale;
- Liang, Mei Lan e Qin com a visão do GBA;
- porta trancada, placas, guarita e Breezeport.
- Capturas: `CP-DS-03B_route2.png`.

Falta:
- o item da Route 2 é Potion; no GBA é Super Potion (já estava no backlog);
- modelos para o armazém, as barracas do mercado e o celeiro de Harvestvale (hoje são só colisão). As árvores soltas
  em volta deles saem cortadas;
- a porta do laboratório (vão claro) e a do ginásio (branca): os modelos de porta de fora da área ficam sem textura,
  mesmo dentro do total de bytes;
- placa e falas com direções adaptadas ao protótipo ("East: Dawnmere"…): voltam ao texto do GBA na troca;
- Harvestvale (metatiles do tileset Slateport ainda sem tabela);
- troca do protótipo.

### Plano de Breezeport (estudado em 24/11, noite; próxima frente)

- **A matriz não cresce.** `MAP_MATRIX_MAX_SIZE` do HeartGold é 799 células, exatamente as 47×17 da matriz 0
  (pokeheartgold, `include/map_matrix.h`). A área vazia do canto superior esquerdo tem 7 linhas de células.
- **Avaliação dos deslocamentos.** Testei todos os deslocamentos verticais que fariam a cadeia inteira (Dawnmere →
  Breezeport, 214 linhas) caber nas linhas 0–6. Todos deixam de 7 a 15 eventos e de 60 a 230 tiles de mato alto
  numa célula de outro mapa. Fica a posição atual (30,21), sem conflito até a Route 2.
- **Onde Breezeport entra.** Abaixo da Route 2, nas linhas de blocos 5–7 e colunas 2–4.
  - As células (2..4, 7) hoje são só mar de preenchimento do HGSS (bloco 208, header 0), ao lado de uma área de Johto
    na linha 8. Elas são substituídas.
  - A última linha do desenho fica com colisão, para ninguém surfar até os mapas do HGSS.
- **Linha de blocos 5, dividida.** A Route 2 (GBA 32–47) e Breezeport (GBA 0–15) dividem essa linha; as células
  ficam com o header de Breezeport.
  - Os 3 eventos da Route 2 ali passam para a zona de Breezeport: Qin (script padrão de treinador), a placa sul e a
    porta trancada (2 scripts e 2 falas novas no banco de Breezeport).
  - A Route 2 não tem mato alto nessas linhas.
  - Sem guarita: da Route 2 se desce a pé para Breezeport, como no GBA e como o diretor pediu.
- **Área 7.** As células de Breezeport ficam com o header de Olivine (T26), que é da área 7: outro conjunto de texturas
  de terreno e outra lista de construções, com os modelos de Olivine, inclusive o farol. Os blocos de Breezeport têm
  de ser compostos com doadores da área 7:
  - Olivine (blocos 58–61) tem `grass01`, `road01`, árvores, `wall01_g`, `cliff01`, mar, `pond_line`/`sea_line02`,
    `beach01`, `fence_a` e `sea_rock`;
  - faltam `road01_r`, `egrass`, flores e `fence_b`. Procurar na Route 39 (área 7) ou trocar a letra pelo material
    disponível;
  - o gerador precisa de doadores por mapa (`doadores_por_mapa` no `land.json`).
- **Tabela de metatiles.** Os metatiles de 0x200 em diante são do tileset secundário. As entradas desse trecho valem
  só para os tilesets em que foram conferidas (EverGrande e Petalburg). Breezeport (Lilycove) está toda na tabela.
- **Pendente:** a Route 3 sai pela borda oeste de Breezeport (GBA: `Palm090_ToRoute03`, linhas 48–59, deslocamento
  −20). Não começar.

### Breezeport original (24/11, noite)

`PalmBrisa` (72×60) convertida abaixo da Route 2, nas linhas de blocos 5–7, como no plano acima.

- **Mapa:** a montanha com platô (altura 2) e cume (3), com as escadas como rampas; avenida, praça, praia e mar. O mar
  segue pelas áreas sem mapa vizinhas a ele, e a borda externa do desenho tem colisão (`barreira`).
- **Área 7:** os blocos com o header de Olivine usam doadores de Olivine (58–61) e da Route 39 (54–57); as flores de
  outros tipos viram `flower01`. Correção: a área 7 usa a lista de construções 6 e o conjunto de texturas 7. Achei
  isso em a/0/4/2 (área → lista, texturas); antes eu supunha lista = área, o que só valia por acaso para a área 2.
- **Construções** (lista 6):
  - casas → `as_h01` e `tn_h01`;
  - Teatro → `as_gym`, com a porta central como no GBA;
  - PC e Mart nas portas do GBA;
  - loja de departamentos → `tn_photo`, decorativa e trancada (decisão do diretor: não existe no jogo);
  - casa de praia → `as_restaurant`.
  - As 3 casas do GBA sem interior no DS ficam com a porta decorativa.
- **Eventos** (0710–0712):
  - os 11 NPCs e as 9 placas do protótipo nos tiles do GBA, inclusive os 3 lampiões do festival;
  - 6 warps (Teatro, PC, Mart e 3 casas);
  - a trava do Teatro, no tile abaixo da porta;
  - a saída para a Route 3, na borda oeste como no GBA (antes era ao norte). Antes da Jay, a fala e um passo para
    leste; depois, a ponte provisória para a Route 39, a Route 3 do protótipo. Descendo a Route 39, volta-se à borda
    oeste de Breezeport;
  - Qin, a placa sul e a porta trancada da Route 2 passaram para a zona de Breezeport (linha de blocos dividida);
  - sem guarita: da Route 2 se desce a pé para Breezeport.
- **QA** (`qa_cp03d.py --cap1`): passou nas 22 checagens, do quarto até Breezeport:
  - porta trancada, Qin e placa sul da Route 2 já na zona de Breezeport;
  - entrada a pé e placa de Breezeport;
  - Teatro fechado (fala e um passo para baixo);
  - saída oeste fechada (fala e um passo para leste).
  - Capturas: `CP-DS-03B_breezeport.png`.
- **Falha registrada:** a primeira build falhou porque dei ao Qin um id textual sem símbolo no hg-engine; agora o id é
  numérico.
- **Falta em Breezeport:**
  - os encontros selvagens do GBA (terra, água, pesca), porque o T26 ainda usa os do protótipo;
  - modelo para os postes da avenida;
  - o farol que o diretor pediu: o mapa do GBA não tem farol, e o modelo existe na área 7 (`as_toudai`).
