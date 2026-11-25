# Decisões de produção — trilha GBA (respondidas em 18/11/2026)

Fonte: respostas do diretor criativo (via ChatGPT) às perguntas de abertura. Prevalecem sobre documentos históricos.
GBA e DS compartilham cânone, personagens, narrativa e progressão; diferenças de engine não autorizam mudanças criativas.

## Identidade

- Região: **Lunia**. Título: **Pokémon Hollowtide**. Créditos: **"Created by respectlol1"**.
- Jogo integralmente em **inglês**.

| Original (PT, DS) | GBA (EN) | Líder / função |
|---|---|---|
| Vila Inicial | Dawnmere Village | casa, Prof. Alex |
| Rota 01 | Route 1 | |
| Vila da Colheita | Harvestvale | Nevard (Grass) |
| Rota 02 | Route 2 | |
| Cidade da Brisa | Breezeport City | Jay (Ghost) |
| Rota 03 | Route 3 | |
| Ferrália | Ferralia City | Vessel (Steel) |
| Rota 04 | Route 4 | |
| Entreposto Comercial | Tradepost | sem ginásio |
| Rota 05 | Route 5 | |
| Cidade dos Pilares | Pillarton City | Tchum (Ground) |
| Rota 06 | Route 6 | |
| Vila Serenia | Serenia Village | Jade (Psychic) |
| Rota 07 | Route 7 | |
| Cidade do Horizonte | Horizon City | Chelsia (Fairy) |
| Rota 08 | Route 8 | |
| Vila da Passagem | Passway Village | sem ginásio |
| Rota 09 | Route 9 | |
| Voltara | Voltara City | Hoc (Electric) |
| Rota 10 | Route 10 | |
| Cidade das Marés | Tidemouth City | Nami (Water) |
| Rota 11 | Route 11 | |
| Liga Pokémon | Pokémon League | Elite + Doge |
| Rota 12 Desvio do Rio | Route 12 (River Bend) | opcional |
| Rota 13 Bosque Espelhado | Route 13 (Mirror Grove) | opcional |
| Rota 14 Mirante de Atlas | Route 14 (Atlas Lookout) | opcional |
| Rota 15 Gruta Costeira | Route 15 (Coastal Grotto) | opcional |

## Sistemas

- Dificuldade moderada, sem punição artificial; IA inteligente nos líderes; sem level cap.
- **Exp. Share sempre ativo** (flag ligada no início); balancear níveis considerando isso.
- Mecânicas modernas até Gen 9 (Fada, físico/especial, habilidades). **Sem Dynamax, Z-Moves e Tera** para ninguém.
- **Mega Evolução do jogador só após a Liga** (Key Stone/Mega Ring no pós-jogo). Pkas é a primeira Mega mostrada (Mega Charizard X); Doge fecha com Mega Latios.
- Pokédex regional curada (~250 espécies, todas as gerações, por bioma). Iniciais Snivy/Fennekin/Mudkip e espécies dos times principais obrigatórias. **Kyogre e Lugia nunca como encontro selvagem comum.**
- Pokémon seguidor e dia/noite por relógio: ativos, com verificação de sprites/paletas.
- Sem HMs obrigatórias: habilidades de campo/itens-chave, mantendo bloqueios que fazem sentido.
  - 20/11 (diretor: "você decide" / "o ponto mais coeso para entregar o surf"): a Nami entrega a **HM03 Surf** no fim
    do Complexo Oceânico (ela chega montada no Wailord; levou o jogador de barco até ali). A **HM07 Waterfall** continua HM
    (trocar por TM renumeraria as HMs dos saves), mas as HMs passam a poder ser esquecidas (`P_CAN_FORGET_HIDDEN_MOVE`).
- **Sem rival.**
- Rotas 12–15 no jogo base, com exploração e recompensas.
- Sem Battle Frontier/revanches extensas. Pós-jogo obrigatório: Cynthia, Tavinho, Primal Kyogre, Medalhão de Atlas, resolução em Hoenn — com narrativa, não batalha avulsa.

## Narrativa e arte

- Sem bordões obrigatórios; personalidade documentada, diálogos naturais. Tchum tem trocadilhos.
- Medalhão de Atlas: a mãe entrega no prólogo como herança, item-chave sem poder; origem revelada aos poucos até o pós-jogo; **sem parentesco biológico** do protagonista com Atlas.
- Corcovado, Paulista, Serra do Mar etc. só como referência; locais com nomes fictícios.
- Team Palm: recoloração provisória verde-oliva escura de sprites existentes, sem alterar globalmente sprites usados em outros lugares; sem futebol.
- Música: faixas existentes do Emerald/Expansion por atmosfera.
- Cynthia (20/11, pedido do diretor): retrato de batalha e boneco de mapa extraídos da hack *PK Black Pearl EMR*
  (ROM fornecida pelo diretor; o retrato é o sprite oficial de Platinum convertido para GBA). Arquivos
  `graphics/trainers/front_pics/champion_cynthia.png`, `graphics/object_events/pics/people/champion_cynthia.png` e
  `graphics/object_events/palettes/champion_cynthia.pal`. A hack não tem tema musical da Cynthia (tabela de músicas igual
  à do Emerald). As músicas vieram depois, em MIDI enviado pelo diretor: tema de pré-batalha (só no diálogo antes da luta)
  e tema de batalha próprios.

## Versão DS (HeartGold + hg-engine)

- 24/11 (diretor): a Jay entrega o **TM65 Shadow Claw** no lugar do TM Hex do GBA (o hg-engine não tem TM de Hex).
- 24/11 (diretor, resposta à auditoria CP-DS-00/01): **mapas originais são obrigatórios**. O caminho A (mapas de
  Johto intactos com eventos de Lunia) vale só como protótipo funcional; a versão final tem geografia, rotas e
  ambientes próprios de Lunia, coerentes com o Town Map (recursos, objetos, tilesets e técnicas de HGSS podem ser
  reutilizados; mapas inteiros de Johto como localidades definitivas, não).
  - Route 1: três setores, direção **norte → sul**.
  - Route 2: sai do **sudeste de Harvestvale**, perto do ginásio; campo → vegetação costeira → praia → Breezeport,
    por conexões exteriores naturais (sem guarita/porta).
  - Breezeport: **6 setores em 3 × 2**, com praia, orla, farol, **montanha (obrigatória)**, residências, comércio,
    Centro, Mart, ginásio da Jay.
  - Route 3: sai pelo **oeste/noroeste** de Breezeport; praia → costa → encosta → serra → planalto → Ferralia. A saída
    norte de Olivine não é definitiva; pendente até haver o mapa.
  - Ferralia: metrópole (São Paulo; referências Goldenrod, Saffron, Castelia), sem áreas vazias.
  - Textos: livro do laboratório = "A field guide to Pokémon habitats and care. Professor Alex has marked several
    pages for new Trainers."; sem loja de departamentos: "You can stock up on supplies at the Poké Mart."
  - SAVE/CONTINUE só vale validado com o emulador encerrado e reaberto (sem savestate).
  - Antes de construir Lunia: prova de terreno 3D próprio (caminho, vegetação, desnível real, objeto, colisão,
    alturas, conexão, entrada e retorno) validada no DeSmuME.
  - **Push remoto suspenso** até o diretor pedir a publicação; commits locais e ramos isolados; nada de force push.
  - Ordem: CP-DS-02 → CP-DS-02B (save) → CP-DS-03A (pipeline de mapas) → CP-DS-03B (primeira localidade original).
- 24/11 (diretor, decisões do CP-DS-03B): células do mapa-múndi **a critério do Claude**; **seguir à risca o GBA**
  (os mapas autorais do GBA 23ap, convertidos para o DS, com a mesma geometria); saída de Dawnmere **a leste**, como
  no GBA (as adaptações para "oeste" do protótipo deixam de valer quando os mapas originais entrarem).

## Entrega

- Patch `.xdelta` sobre Pokémon Emerald (U), SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`, com conferência de hash; código-fonte, build e instruções. Sem ROM comercial.
- Ambiente de teste do usuário: **mGBA no Windows** — verificar saves e integridade do patch.

## 24/11/2026 (noite) — CP-DS-03B etapa 6: mapas originais na build de conteúdo

- Dawnmere, Route 1 e Harvestvale convertidos do GBA substituem o protótipo do caminho A na build de conteúdo.
- As adaptações de direção feitas para o protótipo nesses três mapas voltam ao texto do GBA.
- Ponte provisória (decisão minha, para o jogo seguir jogável): a saída sul de Harvestvale (GBA) leva à Route 2 do
  protótipo, e descendo a Route 2 volta-se a Harvestvale. Sai quando a Route 2 for convertida (Route 2 = etapa
  seguinte, saindo do sudeste de Harvestvale, como o diretor definiu).
- Construções: o laboratório do Prof. Alex usa o modelo do laboratório de Pallet, com a porta 1 tile a oeste do GBA.
  É o único laboratório do HGSS que cabe na planta. O ginásio do Nevard usa o de Celadon (tipo Planta).

## 24/11/2026 (noite) — CP-DS-03B: Route 2 original e nova posição do desenho

- O desenho de Lunia foi para as células (0,0) em diante da matriz 0 (vazias no HGSS), deslocado (30,21). Cada
  célula tem um header só, e esse deslocamento faz cada célula ter um mapa só. Corrige a placa sul e os encontros do
  fim da Route 1, que estavam numa célula de Harvestvale.
- Adaptação mínima: o fazendeiro e a chegada de Harvestvale descem 3 linhas, porque as 5 primeiras linhas de
  Harvestvale ficam numa célula da Route 1.
- Route 2 convertida do GBA, abaixo de Harvestvale, com ligação a pé. A ponte provisória passa para a saída sul da
  Route 2 → guarita → Breezeport do protótipo.

## 24/11/2026 (noite) — publicação

- O diretor autorizou voltar a publicar ("volta com os pushes quando julgar necessário, e vai seguindo"). Publico as
  entregas validadas no branch claude/new-session-tnwrgl, sem force push e sem ROM ou save.

## 24/11/2026 (noite) — Breezeport original

- Breezeport convertida do GBA abaixo da Route 2, com ligação a pé (sem a guarita do protótipo).
- A saída para a Route 3 volta a ser a borda oeste (GBA). A Route 3 ainda é a do protótipo (Route 39), então há uma
  ponte provisória nos dois sentidos, depois da Jay.
- O teatro usa o modelo do ginásio de Olivine (a porta central coincide com a do GBA). A loja de departamentos fica
  decorativa, como o diretor decidiu.
- Farol: o diretor autorizou o farol de Olivine. Ele fica na ponta de areia abaixo do faroleiro e da casa dele
  (GBA 61–68 × 48–54), decorativo.

## 25/11/2026 — auditoria corretiva de acabamento dos mapas do DS
- Correções de acabamento entram no conversor e no gerador (`gba2grade.py`, `mapa_grade.py`, `mapa_global.py`),
  nunca à mão num mapa: assim cada tipo de erro sai do mapa inteiro. O GBA segue congelado em 23ap.
- Árvores no padrão da Route 29: `tree01` (árvore inteira, 4 tiles) e `tree01_re` (fileira). Os arbustos de 1 tile
  do GBA viram árvores em meia escala.
- Lampiões do GBA → poste de Olivine (`as_light`). Pedras soltas → bloco de rocha. Nenhum tile bloqueado fica sem
  modelo visível.
- A colisão não muda numa rodada de acabamento sem estar listada: `check_colisao.py --antes` compara as builds.
- Um modelo de construção tem de estar na lista de toda célula de onde é visto (`check_construcoes.py`).

## 25/11/2026 — Route 3 original
- O diretor mandou seguir (o laboratório fica de lado): a Route 3 do GBA entra no desenho, a oeste de Breezeport, no
  header da Route 39 (a Route 3 do protótipo). Ferralia ainda não.
- Mapas que o GBA desenha planos, com paredões e escadas só no desenho, ganham patamares no DS: cada escada sobe um
  nível (`TERRACOS` em `gba2grade.py`).
- Os NPCs do HGSS que não existem em Lunia ficam escondidos (`hidden_flag FLAG_GOT_TRAINER_CARD`), em vez de apagados:
  os ids dos objetos e dos scripts continuam válidos.
- Depois da Jay, a saída oeste de Breezeport leva à Route 3 a pé; a ponte provisória para a Route 39 saiu.

## 25/11/2026 — Ferralia original e desenho deslocado
- O desenho global andou uma célula para leste (+32 em x): Ferralia, acima da Route 3, passava da borda. Deslocar uma
  célula inteira preserva a partição de células e headers de todos os mapas já prontos.
- Ferralia usa o header de Goldenrod (a metrópole do HGSS): os modelos nativos da área cabem na cidade (estação do
  Magnet Train, ginásio, Centro, loja, prédios, fonte, postes) sem mexer no teto de texturas.
- Ferralia fica no nível do platô da Route 3, como diz a placa do GBA.
- O evento do pátio de cargas (que destrava o ginásio) e o ginásio ficam para a etapa seguinte; até lá a porta do
  ginásio fica trancada, para não abrir um ginásio com o interior de Goldenrod.
