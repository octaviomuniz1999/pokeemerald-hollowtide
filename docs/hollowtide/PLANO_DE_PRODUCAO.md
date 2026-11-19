# Plano de produção — Pokémon Hollowtide (GBA)

Construção autônoma até o capítulo final. Cada capítulo só fecha quando passa no **portão de qualidade**.
Status ao lado de cada item: `[ ]` a fazer · `[~]` em andamento · `[x]` concluído e verificado.

## Portão de qualidade (vale para todo mapa/capítulo)

1. `map_lint.py` sem erros nem avisos (metatiles vazios, colisão divergente do padrão oficial, eventos fora do mapa).
2. Revisão visual por `render_map.py` (com `--collision --events`): caminhos conectados, cantos e bordas completos,
   relevo por tiles corretos, sem faces de penhasco andáveis, sem vazios desproporcionais nem padrões repetitivos.
3. QA em emulador (`tools/hollowtide_qa`): todas as passagens de ida e volta, travas de história nos dois estados,
   NPCs interagíveis, eventos do capítulo executados até o fim, salvar/carregar.
4. Batalha principal do capítulo vencível com time de nível esperado (curva com Exp. Share sempre ativo).
5. Texto 100% em inglês, revisado (ortografia, quebras de linha, tom do personagem).
6. Build limpo, commit + push, auditoria atualizada.

## Fundação

- [x] Importação do Alpha 02, merge com upstream, respawn corrigido
- [x] Decisões e tabela de nomes (`DECISOES.md`), região Lunia, seções de mapa em inglês
- [x] Exp. Share sempre ativo, seguidores, dia/noite (padrão da expansion), flags de QA
- [x] Ferramentas: renderizador, folha de metatiles, linter, correção de colisão, runner/driver de emulador
- [x] Título com HOLLOWTIDE e créditos "Created by respectlol1" (fundo do título: Rayquaza placeholder — Kyogre revelaria o pós-jogo)
- [~] Pokédex regional: design em `POKEDEX_LUNIA.md`; tabelas de encontro aplicadas por capítulo ao construir os mapas
- [~] Curva de níveis da campanha (Cap. 1 ajustado; demais capítulos ao construir)
- [ ] Field moves sem HM (itens-chave/habilidades de campo)
- [ ] Town Map de Lunia (gráfico + seções)

## Capítulos

| Cap. | Conteúdo | Base atual |
|---|---|---|
| 1 `[~]` | Dawnmere → Route 1 → Harvestvale; Prof. Alex, mãe + Medalhão de Atlas; recruta da Team Palm e irrigação; ginásio de Nevard (comportas) | colisão corrigida; texto 100% EN; Medalhão; tela de 3 Poké Balls; comportas persistentes; Team Palm verde-oliva; eventos 10/10 no emulador; **falta**: teste de balanceamento com itens/2º Pokémon, revisão de arte dos interiores e do lab |
| 2 `[~]` | Route 2 (campo → litoral) → Breezeport (cidade costeira ampla, farol, morro tipo Corcovado, orla); ginásio de Jay (Teatro dos Ecos) | refazer em escala (placeholder 20×20 do Alpha 02) |
| 3 | Route 3 (praia → costa → serra → planalto, saída oeste/noroeste de Breezeport) → Ferralia (metrópole, ferrovia, viadutos, indústria); Vessel; "Carga Desviada" | refazer |
| 4 | Route 4 → Tradepost ("Preço da Troca", Mestre Wen, PALM Coin) | novo |
| 5 | Route 5 → Pillarton (barragens, Lela); Tchum | novo |
| 6 | Route 6 → Serenia (jardins, espelhos, Lau); Jade | novo |
| 7 | Route 7 → Horizon City (lago, constelações, sensores submersos); Chelsia | novo |
| 8 | Route 8 → Passway (estalagens, mirante, montanha fechada até o pós-Liga) | novo |
| 9 | Route 9 → Voltara (energia, ferrovia, centro de dados, Vega); Hoc | novo |
| 10 | Route 10 → Tidemouth (porto, marés, complexo oceânico, Abelf); Nami; a tempestade continua | novo |
| 11 | Route 11 → Pokémon League (Angelic, Riven, Du, Pkas com a 1ª Mega, Doge com Lugia e Mega Latios) → créditos | novo |
| 12 | Pós-Liga: convocação de Doge, montanha, Steven/Leon, Joy, Cynthia, Tavinho (Primal Kyogre), Medalhão, Marine Cave/Hoenn; Key Stone liberada | novo |
| — | Rotas opcionais 12–15 (River Bend, Mirror Grove, Atlas Lookout, Coastal Grotto), encaixadas nos capítulos onde a geografia permitir | novo |

## Referências de qualidade (estudo, não cópia)

Ritmo e leitura de mapa de Ruby/Sapphire/Emerald e HGSS (rotas com bifurcações curtas, recompensas visíveis
fora do caminho, marcos verticais), cidades de Black/White para densidade urbana (Castelia como atmosfera de
Ferralia), cidades costeiras de HGSS (Olivine) para Breezeport. Narrativa ambiental: placas, NPCs e lugares
contam a história da água antes de qualquer cena longa.

## Ferramentas de QA disponíveis

- `tools/hollowtide_qa/qa_completo.sh RUNNER WORKDIR`: intro → lab → Rota 1 → Harvestvale → transições → eventos do Cap. 1.
- `fluxo_cap1_balanco.py` (com `HT_STARTER`): partida realista no nível de chegada, por inicial.
- Ganchos de QA só em build não-release: `FLAG_HT_QA_BOOST_PARTY` (+ `VAR_HT_QA_LEVEL`), `FLAG_HT_QA_NO_ENCOUNTERS`,
  `FLAG_HT_QA_NO_TRAINER_SEE`. **Distribuição sempre com `make RELEASE=1`.**

## Ferramenta de mapas (estado)

- `[x]` `tools/hollowtide/mapgen`: corpus dos mapas oficiais, autotile aprendido (grama, mato, árvores, mata, areia,
  poça, lago, mar, água rasa, ladeiras S/L/O, flores; calçamento do secundário Lilycove), Canvas com carimbos de
  prédios e colisão de referência.
- `[x]` relevo: platôs (elev. 5) com face de rocha aprendida do corpus, parede sul dupla, escadas (175, elev. 0), terreno sobre o platô herdando a altura; árvores 2×2 determinísticas.
- `[ ]` margem inferior de lagos (família 'pond').
- `[ ]` metatiles compostos (farol) nos slots livres do secundário.
- `[~]` Breezeport: esboço em `tools/hollowtide/maps/breezeport.py` (fora do jogo até passar no portão de qualidade).

## Próximo passo técnico (histórico)

Ferramenta de construção de mapas (`tools/hollowtide/mapgen`): pincéis com autotile aprendido dos mapas oficiais
(caminhos, água com margem, florestas, ladeiras/penhascos com elevação), carimbos de prédios extraídos dos tilesets
e validação automática (linter + render). Base para a Route 2 e a Breezeport em escala.
