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

## Entrega

- Patch `.xdelta` sobre Pokémon Emerald (U), SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`, com conferência de hash; código-fonte, build e instruções. Sem ROM comercial.
- Ambiente de teste do usuário: **mGBA no Windows** — verificar saves e integridade do patch.
