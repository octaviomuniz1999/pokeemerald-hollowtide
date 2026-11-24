# CP-DS-00 — Auditoria e baseline da versão DS (24/11/2026)

Ordem mestre do diretor (24/11): IMPLEMENTAR → INTEGRAR → COMPILAR → TESTAR → DOCUMENTAR. Checkpoint do estado
recebido: tag git local `cp-ds-00-recebido` (commit `dae09bc0`).

## 1. Identificação técnica

| Item | Valor |
|---|---|
| Repositório | `octaviomuniz1999/pokeemerald-hollowtide`, ramo `claude/new-session-tnwrgl`. O GBA (pokeemerald-expansion) é só referência de conteúdo; o DS fica em `hollowtide_ds/` (patches e dados) e `tools/hollowtide_ds/` (ferramentas) |
| hg-engine | `BluRosie/hg-engine` commit `b578c990` (`hollowtide_ds/hg-engine.commit`), checkout em `/home/user/blurosie/hg-engine` (dependência externa, não versionada aqui) |
| ROM-base | Pokémon HeartGold EUA (IPKE), SHA-1 `4fcded0e2713dc03929845de631d0932ea2b5a37` — fica fora do git |
| Sistema | Linux 6.18 (container), Python 3.13, `arm-none-eabi-gcc`, Java (sem .NET, sem Wine) |
| Bibliotecas | `ndspy` 4.2 (NARC/ROM), `py-desmume` 0.0.9 (emulador sem tela), Pillow |
| Ferramentas de mapa | DSPRE (Windows/.NET) não roda aqui. Pokémon DS Map Studio é Java (GUI); exportar `.nsbmd` exige o `g3dcvtr` do Nitro SDK (Windows) → sem Wine, não dá para gerar terreno 3D novo neste container. **Ferramentas próprias** (Python + ndspy): `matrix.py` (matriz a/0/4/1), **`land_data.py` (novo: blocos a/0/6/5 — objetos 3D e colisão)**, `hgss_catalog.py`, `hgss_seams.py` |
| Build | `tools/hollowtide_ds/build.sh ROM_HEARTGOLD /home/user/blurosie/hg-engine` → `test.nds` (≈1 min 20 s): hg-engine no commit fixo + patch base + despejo de scripts/eventos/textos + `patches/content/` (overlay, patches em ordem) + `make` + matriz, **blocos de mapa (`land.json`)** e trocas gravados na ROM pronta |
| Emulador | DeSmuME via `py-desmume`, harness `tools/hollowtide_ds/ds_driver.py` (lê mapa/posição por ganchos no `FieldSystem`; capturas; estados; `reset()`) |
| Pipeline de scripts | `BUILD_DUMPED_SCR_SEQ` e `BUILD_DUMPED_EVENTDATA` **ligados** pelo `0001-hg-engine-base.patch` (Fase 0, 23/11): os scripts `data/scr_seq/*.s` e eventos `data/eventdata/zone_event/*.json` despejados da ROM são os que compilam; sem isso o hg-engine usa os binários originais e nenhum evento de Lunia entraria. Textos: `data/text/custom/NNN.txt` despejados + `0500-texts.patch` (gerado de `hollowtide_ds/data/texts.json` por `text_patch.py`) — **o patch é o que vale na build; editar o `texts.json` sem rodar `text_patch.py` não muda a ROM** (foi a causa do 1º defeito do CP-DS-01) |

## 2. Por que "os mapas não foram integrados"

Diagnóstico honesto: no **caminho A** (aprovado em 23/11, `PLANO_HEARTGOLD.md` §0) **nenhuma geometria nova foi
construída**. Cada lugar de Lunia é um mapa de HGSS **intacto em 3D e colisão**, com eventos, textos, nomes de lugar,
treinadores e encontros de Lunia. No emulador, o jogador vê New Bark, Cherrygrove e Olivine com NPCs, placas e
falas de Lunia. Não houve edição de modelo, colisão, altura ou objeto 3D até o CP-DS-01. Não existe nenhum arquivo
de mapa criado e não usado: o que existe é a reutilização, integrada e testada.

Divergências entre a geografia do HGSS reaproveitada e a ordem mestre (§8):

| Item da ordem | Estado na ROM | Situação |
|---|---|---|
| Route 1: três mapas exteriores, norte-sul | Route 29: 3 blocos, **leste-oeste** | 3 blocos ok; orientação diverge |
| Route 2: começa a sudeste de Harvestvale, campo → litoral → praia | Route 30 + 31: sai pelo **norte** de Cherrygrove; campo; chega a Breezeport por uma **porta de guarita** (exceção registrada) | diverge (transição costeira e emenda natural faltam) |
| Breezeport: 6 setores em 3×2, farol, montanha | Olivine: **2×2 = 4 blocos**; farol fechado (casa do faroleiro); sem montanha | diverge |
| Route 3: sai pelo oeste/noroeste de Breezeport, subida da serra | prevista na Route 39, que sai pelo **norte** de Olivine (ainda não montada) | **decisão pendente** antes do CP-DS-06 |
| Ferralia: metrópole | não montada | pendente (CP-DS-07) |

Corrigir isso exige geometria nova (caminhos B/C do plano), que depende de gerar terreno 3D (`.nsbmd` + `.bdhc`).
O CP-DS-01 prova o que já é possível aqui: objetos 3D, colisão, eventos e conexões. Terreno 3D novo é o próximo
bloqueio técnico (§5).

## 3. Mapas da região jogável (estado comprovado)

Níveis: Planejado / Asset / **Integrado** (na ROM) / **Jogável** (testado no emulador) / Validado (critérios de
qualidade da ordem).

| Lunia | Mapa HGSS (id) | Blocos land_data (matriz 0: célula → bloco) | Área | Header: scripts / textos / eventos | Conexões | Estado |
|---|---|---|---|---|---|---|
| Dawnmere Village | MAP_T20 (60) | (21,12) → 0 | 2 | 842 / 542 / 57 | a pé: Route 1 (oeste, 7 tiles) | **Jogável**; bloco 0 **editado** (CP-DS-01) |
| casa do jogador | T20R0201 (63), T20R0202 (64) | matrizes 71, 72 → 216, 217 | 25 | 845/545/60, 846/546/61 | porta de Dawnmere | Jogável |
| laboratório do Prof. Alex | T20R0101 (61) | matriz 100 → 244 | 25 | 843 / 543 / 58 | porta de Dawnmere | Jogável |
| Route 1 | MAP_R29 (33) | (18..20,12) → 1, 2, 3 | 2 | 225 / 373 / 30 | a pé: Dawnmere, Harvestvale | Jogável (Kai, Min) |
| Harvestvale | MAP_T21 (67) | (16..17,12) → 4, 5 | 2 | 850 / 550 / 64 | a pé: Route 1, Route 2 (norte) | Jogável (recruta, válvula) |
| ginásio do Nevard | T07GYM0101 (395) | matriz 258 → 316, 374 | 52 | 786 / 492 / 352 | porta | Jogável (batalha; **comportas pendentes**) |
| Route 2 | MAP_R30 (34) + MAP_R31 (35) | (17,9..11) → 6, 7, 8; (16..17,8) → 9, 10 | 2 | 227/375/31, 230/378/32 | a pé: Harvestvale; guarita | Jogável (Liang, Mei Lan, Qin) |
| guarita | R31R0101 (97) | matriz 70 → 243 | 63 | 231 / 379 / 94 | portas: Route 2 ↔ Breezeport | Jogável |
| Breezeport City | MAP_T26 (77) | (8..9,7..8) → 58, 59, 60, 61 | 7 | 911 / 604 / 74 | guarita; norte → Route 39 | Jogável (festival, lampiões) |
| Teatro (ginásio da Jay) | T26GYM0101 (138) | matriz 91 → 253 | 32 | 913 / 606 / 134 | porta | Jogável (refletores, batalha, saída norte liberada — `qa_cap2.py` 24/11) |
| Route 3 | MAP_R39 (43) | (8,5..6) → 56, 57 | 7 | 249 / 396 / 40 | — | Planejado (eventos de HGSS) |

Colisões, alturas e modelos: os do HGSS (válidos no jogo original). Seguidor: o inicial segue o jogador (recurso de HGSS)
em Dawnmere e na divisa com a Route 1 (capturas do CP-DS-01); escadas, desníveis e portas ainda não foram testados à parte.

## 4. Diálogos — auditoria sistemática

Ferramenta nova: `tools/hollowtide_ds/audit_dialogos.py`. Ela pega os 27 mapas da região jogável (os externos e tudo o que
se alcança por warps) e as 182 mensagens chamadas por scripts. Para cada uma, confere:
- se a mensagem existe e não está vazia;
- a largura em pixels pela tabela da fonte do DS (limite de 215 px = a maior linha do HGSS nos mesmos arquivos);
- linhas demais na caixa;
- nomes de Johto/Kanto;
- português;
- se a fala ficou igual à do HGSS.

Também separa as falas **alcançáveis** (scripts chamados por NPC, placa, gatilho ou header do mapa, e o que eles
alcançam por goto, call e queda) do código morto das cenas de HGSS desligadas.

Resultado na ROM anterior ao CP-DS-01 → depois das correções:

| Defeito (alcançável) | Causa | Correção |
|---|---|---|
| Placa nova mostrava "Call your mom on your Pokégear…" | `texts.json` editado sem regenerar `0500-texts.patch`: a mensagem 8 continuava a do HGSS | regenerado; regra registrada (§1) |
| Guia de Dawnmere: "Route 1 starts at the east edge." | direção do GBA; no DS a saída é a oeste | `replace` registrado (`_por_que`) |
| Saída sem Pokémon: lab "to the north"; mãe: lab "to the north" | idem (da saída o lab fica a leste; da casa, a oeste) | idem |
| TV da cozinha: "Cinnabar Volcano Burger!" (Kanto) | fala genérica do HGSS no interior | `hgss_replace` (novo em `text_patch.py`): "Volcano Burger!" |
| Quarto: "Wii is huge in Johto, too!" | idem | Johto → Lunia |
| Casa do pescador de Breezeport: "Olivine is on the sea!" | idem | Olivine → Breezeport |
| Casa de Breezeport (T26R0301): pede KRABBY por VOLTORB, mas a vaga de troca 2 virou a troca do GBA (Graveler por Roggenrola) | NPC de troca do HGSS ficou e a vaga foi reaproveitada | NPC removido (`0695`) — as trocas do GBA são de outro lugar (Palm261) |
| Centro Pokémon e casa de Breezeport: falas sobre Cianwood | NPCs de Johto | removidos (`0695`) |
| Casa T20R0102 de Dawnmere: esposa e filho do professor ("my husband…") | família do Elm, fora do cânone | removidos (`0695`) |

Restam, alcançáveis: (a) o livro "Travel Tip 4: The Pokégear…" no laboratório. O jogador de Lunia não recebe o
Pokégear: fica pendente, falta definir o texto. (b) `scr_seq_T20R0201_006`, a cena "Professor Elm told me…": o
header só a chama com `VAR_SCENE_PLAYERS_HOUSE_1F == 3`, e só um mapa de Kanto põe esse valor, então na prática ela
é inalcançável. Falas genéricas do HGSS em interiores (enfermeira, vendedor, dicas) ficam como placeholder, com
nomes de Johto trocados. Nenhuma linha passa da caixa, nenhuma mensagem chamada falta ou está vazia, não há
português no jogo. Relatório completo regenerável:
`audit_dialogos.py /home/user/blurosie/hg-engine test.nds SAIDA.md`.

Pendente de texto/mapa (não é defeito de pipeline): "DEPARTMENT STORE by the beach" (604/10). Olivine só tem um
Poké Mart, e a decisão é do diretor. As placas e falas "West Beach Trail – Route 3" (604/15-16, 606/2-3) apontam
para o oeste, mas a saída montada hoje é a norte (Route 39). Fecha junto com a decisão da Route 3 (CP-DS-06).

## 5. Próximo bloqueio técnico (terreno 3D novo)

Objetos 3D (construções da lista da área, a/0/4/3), colisão, eventos, warps e matriz: **provados** (CP-DS-01).
Terreno novo (`.nsbmd` do bloco + `.bdhc` de alturas): o Pokémon DS Map Studio é Java e roda aqui só com tela virtual. A
exportação para `.nsbmd` passa pelo `g3dcvtr` (Windows). Caminhos a investigar no CP-DS-03, antes de construir
cidade nova: instalar Wine + Xvfb e rodar a cadeia PDSMS → g3dcvtr aqui; ou gerar `.nsbmd`/`.bdhc` direto em
Python, a partir de blocos de HGSS recombinados (alturas planas e rampas simples).
