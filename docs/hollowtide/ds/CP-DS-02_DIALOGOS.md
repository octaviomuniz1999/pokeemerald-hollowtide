# CP-DS-02 — Diálogos: testes dirigidos no jogo (24/11/2026)

## Método

- `ds_driver.py` com `QA_FALAS=PASTA` guarda **cada página de fala** do jogo antes de cada botão apertado. Ele detecta
  a caixa de texto (moldura e fundo), espera o texto parar de escrever e grava a tela se o texto for novo.
- O percurso é o dos QAs que já existiam, executados de verdade no DeSmuME:
  - `ds_intro.py`: introdução e nome;
  - `qa_cap1.py`: mãe e medalhão, Dawnmere, laboratório e inicial, Route 1 (Kai, Min), Harvestvale (chegada,
    recruta, válvula, ginásio), ginásio e batalha do Nevard (insígnia, TM), Route 2 (Liang, Mei Lan, Qin), guarita,
    chegada a Breezeport;
  - `qa_cap2.py`: Teatro fechado, artista, 3 lampiões, refletores, batalha da Jay (insígnia, TM65), saída norte.
- As capturas foram revisadas por mapa (montagens das caixas de texto). O auditor automático (`audit_dialogos.py`)
  continua como apoio: cobre falas que o percurso não alcança.

## Defeitos encontrados executando os scripts no jogo, e correções

| # | Onde | Defeito | Causa | Correção |
|---|---|---|---|---|
| 1 | Introdução | o professor era o **Prof. Oak** do HGSS ("My name is Professor Oak…") | o texto 219 (intro) nunca tinha sido trocado | mensagens 6, 35, 36, 40 e 43 = discurso do **Prof. Alex** do GBA (`gText_Birch_*`); fins em `\r` como o DS espera; sprite segue o placeholder oficial |
| 2 | Falas de treinador (Kai, Nevard…) | maiúsculas do GBA: "our POKéMON", "NEVARD: Ha!", "Take the HARVEST BADGE!" | `convert_trainers.py` tinha conversão própria, sem a de caixa | passa a usar a mesma conversão do `gba_text.py` |
| 3 | Todos os textos do GBA | nomes em maiúsculas fora da lista (LINH, YUMI, JUAN, SERRA…) | a lista de nomes era parcial | regra geral: palavra toda em maiúsculas vira caixa mista, menos siglas (TM, HP, PP, OK, KO) e a ênfase do quebra-cabeça da Jay (LEFT/RIGHT) |
| 4 | Batalha do recruta | "You are challenged by **Team Rocket** Grunt!" | a Team Palm reaproveita a classe da Team Rocket | nome da classe (textos 730/731) = **Team Palm**, como no GBA (`battle_main.c`) |
| 5 | Batalha da Jay | "You are challenged by **PKMN Trainer** Jay!" | as classes de líder que o hg-engine acrescentou (Fantina 133, Byron 134: Jay e Vessel) estavam sem nome | nome = **Leader** (730/731) |
| 6 | Falas de treinador longas | 2 linhas passavam da caixa (218 e 220 px; limite 215) | quebras do GBA, caixa do DS mais estreita para essa fonte | `convert_trainers.py` refaz as quebras **só** das caixas que estouram, com o padrão do DS |
| 7 | Livro do laboratório | "Travel Tip 4: The Pokégear…" (o jogador de Lunia não tem Pokégear) | livro genérico do HGSS | texto do diretor: "A field guide to Pokémon habitats and care. Professor Alex has marked several pages for new Trainers." |
| 8 | Breezeport | "DEPARTMENT STORE by the beach" (não existe no mapa) | texto do GBA | texto do diretor: "You can stock up on supplies at the Poké Mart." |

Corrigidos antes, na 1ª leva (CP-DS-00/01): direções do GBA, Johto/Kanto em falas genéricas, NPCs do HGSS fora de
Lunia, placa nova de Dawnmere.

## Pendências registradas (fora da parte jogável atual)

- Treinadores dos ginásios da Chelsia e da Nami (capítulos futuros): o conversor pegou falas do Emerald que sobraram
  nos scripts do GBA ("Leader Juan", "taught Wallace", "Sootopolis Gym"). Revisar quando esses capítulos forem
  montados no DS. Não aparecem até Breezeport.
- Os 5 textos de treinador com o nome do jogador (Hoc, Abelf, Nami, campeão) são de capítulos futuros.

## Resultado (execução final na ROM corrigida, 24/11)

| Percurso | Resultado | Páginas de fala capturadas |
|---|---|---|
| `ds_intro.py` | quarto (64, 6, 6) | 76: discurso do **Prof. Alex** ("…from right here in Dawnmere", "Come see me in my Pokémon Lab") |
| `qa_cap1.py` | **ok** em todos os trechos (casa → Harvestvale → Nevard → Route 2 → Breezeport) | 516 |
| `qa_cap2.py` | **ok** (Teatro → Jay → saída norte) | 94 |
| `qa_textos.py` | livro do laboratório e menino da loja | os dois textos do diretor, completos |

Conferido nas capturas: "Let’s see what our Pokémon can do!" (Kai); "You are challenged by **Team Palm Grunt**!";
"Nevard: Ha! You won, fair and square." / "Take the Harvest Badge!" / "A received the Harvest Badge from Nevard!" /
"Obtained a TM009!"; "You are challenged by **Leader Jay**!" / "Jay: The Echo Badge is yours." / "Obtained a
TM065!"; "A field guide to Pokémon habitats and care. Professor Alex has marked several pages for new Trainers.";
"You can stock up on supplies at the Poké Mart." Nenhuma caixa vazia, nenhum texto cortado, nada em português.

Ainda em aberto, sem mudar texto: as falas "west beach trail" da Jay e da placa apontam para o oeste, como o diretor
decidiu para a Route 3. A saída montada hoje (a norte, protótipo) não é a definitiva e fica pendente até o mapa da
Route 3.
