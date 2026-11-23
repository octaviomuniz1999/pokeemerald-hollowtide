# Fase 2 — Lunia na geometria de HGSS (caminho A)

23/11/2026. Ferramentas: `tools/hollowtide_ds/hgss_catalog.py` (mapas, células da matriz, eventos),
`tools/hollowtide_ds/hgss_seams.py` (divisas andáveis pela colisão dos blocos), `tools/hollowtide_ds/matrix.py`.

## O que os dados mostram

- **O mundo externo de HGSS é uma matriz só** (matriz 0, 47×17 blocos de 32×32 tiles; `HGSS_MAPAS.md`). Cada célula diz
  o bloco 3D (land_data, com a colisão) e o mapa (header: nome, música, scripts, eventos). As coordenadas dos eventos
  são as da matriz inteira (a porta da guarita da Route 29 fica em x=625). Por isso **um lugar de Lunia pode ocupar
  células de mais de um mapa de HGSS** (ex.: Route 2 = Route 30 + Route 31): basta dar às células o mesmo header.
- **Lunia é contínua; HGSS não.** As divisas que se andam a pé (`HGSS_EMENDAS.md`) são 47; o resto das ligações de HGSS
  passa por guaritas (casas com duas portas), cavernas ou surf. A Route 29 liga a pé a New Bark (7 tiles de passagem)
  e a Cherrygrove (4); Goldenrod ↔ Route 34 tem 24; Goldenrod ↔ Route 35, Violet ↔ Route 36 e Ecruteak ↔ Route 38 são
  por guarita. (A conta lê só a colisão: é um piso — a divisa Route 1 ↔ Viridian, que se anda no jogo, aparece fechada
  do lado de Viridian; vale conferir no emulador antes de descartar uma ligação.)
- Objetos que bloqueiam caminho em HGSS (árvores de Cut, pedras, Sudowoodo) são eventos: saem quando os eventos de
  cada mapa forem trocados pelos de Lunia. Água, ressaltos e paredes são geometria e ficam.

## Regra de montagem

1. Cada lugar de Lunia recebe um ou mais mapas de HGSS **ligados entre si no próprio HGSS** (divisa andável ou
   guarita), na mesma ordem em que Lunia é percorrida. Assim nenhuma emenda nova precisa de modelo 3D.
2. Guaritas de HGSS ficam como passagens (placeholder até a arte, Fase 5). Cavernas e florestas internas de HGSS
   (Union Cave, Ilex Forest…) **não** entram como passagem: seriam masmorras que Lunia não tem.
3. Interiores (casas, Centro, Mart, ginásios) reaproveitam os de HGSS do mesmo tipo; um ginásio de Lunia pode ficar
   atrás de uma porta comum se a cidade de HGSS não tiver prédio de ginásio (placeholder).
4. Nomes de lugar, músicas e encontros são os de Lunia (headers e `map_bindings.json`); nada de HGSS aparece como nome.

## Decisão para a fatia vertical (Cap. 1: começo até o Nevard)

| Lunia | HGSS | Por quê |
|---|---|---|
| Dawnmere Village (casa, laboratório do Prof. Alex) | New Bark Town (`MAP_T20`, 1 bloco) + casa do jogador (`T20R0201` térreo, `T20R0202` quarto) + laboratório do Elm (`T20R0101`/`T20R0102`) | vila inicial com casa e laboratório; quarto já testado no harness |
| Route 1 | Route 29 (`MAP_R29`, 3 blocos) | primeira rota de grama; divisa andável com New Bark (7) e com Cherrygrove (4) |
| Harvestvale (Centro, Mart, casas, ginásio do Nevard, irrigação) | Cherrygrove City (`MAP_T21`, 2 blocos) | vila pequena com Centro e Mart, ligada à Route 29 a pé; ginásio por uma porta (interior de ginásio de HGSS) |

A saída leste de New Bark (Route 27, surf) e a guarita da Route 29 para a Route 46 ficam fechadas por eventos na
fatia. As próximas atribuições (Route 2 em diante) se decidem capítulo a capítulo, com a mesma regra, e entram nesta
tabela.

## Ligações de encontros já feitas

`hollowtide_ds/data/map_bindings.json`: Route 1 (GBA `MAP_ROUTE101`) → `ENCDATA_R29_ROUTE_29`.

Nomes de lugar (`hollowtide_ds/data/place_names.json` → texto 279): `MAPSEC_NEW_BARK_TOWN` = Dawnmere Village, `MAPSEC_ROUTE_29` = Route 1, `MAPSEC_CHERRYGROVE_CITY` = Harvestvale.

## Cap. 2 (Route 2 → Breezeport) — decisão de 23/11/2026

| Lunia | HGSS | Por quê |
|---|---|---|
| Route 2 (campo → litoral) | Route 30 + Route 31 (`MAP_R30`, `MAP_R31`) | ligadas a pé com Cherrygrove (saída norte de Harvestvale, já fechada até o Nevard); campo e mato alto |
| Breezeport (praia, farol, morro) | Olivine City (`MAP_T26`) | o único lugar de HGSS com farol, praia e porto juntos |
| Teatro (ginásio da Jay, Ghost) | interior do ginásio do Morty (Ecruteak, chão escuro) | placeholder de ginásio Ghost |

**Exceção à regra 1:** Olivine não se liga à Route 31 no HGSS. A guarita do fim da Route 31 (que levava a Violet)
passa a levar a Olivine — continua sendo uma porta de guarita (placeholder até a arte). Violet City fica de fora.
