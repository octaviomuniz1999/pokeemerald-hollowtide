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

Falta:
- a porta do laboratório aparece como um vão claro (o modelo da porta de Pallet não aparece, nem carregado antes do
  laboratório na lista; pode ser porta de vidro, conferir);
- Harvestvale (metatiles do tileset Slateport ainda sem tabela);
- troca do protótipo.
