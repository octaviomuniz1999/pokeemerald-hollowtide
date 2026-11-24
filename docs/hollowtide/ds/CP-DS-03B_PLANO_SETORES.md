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

Ainda não está no padrão artístico pedido:
- o caminho tem bordas em degrau (faltam as peças de borda do HGSS, `road01_r`/`road01_sub`);
- a margem da lagoa é reta (faltam `pond_edge`/`pond_line`);
- as árvores soltas saem estreitas (falta o carimbo de árvore isolada do HGSS);
- não há casa com cerca e horta (faltam cercas no gerador; a casa só entra com interior funcional).

Ao sul da célula de prova aparece o mar do bloco vazio; no definitivo ali fica o setor C.
