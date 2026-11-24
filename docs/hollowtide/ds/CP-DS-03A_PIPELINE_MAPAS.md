# CP-DS-03A — Pipeline de mapas originais (terreno 3D próprio) — 24/11/2026

## 1. As atividades não são equivalentes (pedido do diretor)

| Atividade | O que é | Estado no projeto |
|---|---|---|
| Alterar um mapa de HeartGold | mexer em partes de um bloco existente (objeto, colisão, evento) | feito no CP-DS-01: placa em Dawnmere |
| Reutilizar um mapa com eventos próprios | geometria do HGSS intacta, NPCs/textos de Lunia | é o protótipo do caminho A (Dawnmere a Breezeport) |
| Remodelar significativamente | trocar a geometria de um bloco mantendo só materiais/texturas | **feito nesta prova** (bloco 57) |
| Criar um mapa novo | bloco novo, na matriz e com header próprios | o gerador já produz o bloco inteiro; falta um header/matriz próprios (CP-DS-03B) |
| Integrar | o bloco entra na ROM pelo build reproduzível | **feito** (`land.json` com `gerador`) |
| Validar no emulador | andar, colidir, subir o desnível, sair e voltar | ver §4 |

## 2. Ferramentas investigadas (requisitos reais)

| Ferramenta | Requisito real | Conclusão |
|---|---|---|
| Pokémon DS Map Studio (Trifindo) | Java (roda em Linux) e GUI. Exporta `.nsbmd` **só por meio do `g3dcvtr.exe` + `xerces-c_2_5_0.dll` do Nitro SDK da Nintendo**. O próprio repositório não distribui: a pasta `converter/` tem só "Paste g3dcvtr in this folder.txt" | ferramenta proprietária, sem fonte legítima; mesmo com Wine (disponível via apt), o pipeline dependeria dela. Não adotado |
| DSPRE | Windows/.NET (WinForms); importa `.nsbmd` já prontos (do PDSMS) | não gera terreno; não roda aqui sem Wine/.NET. Não adotado |
| apicula, Tinke e afins | leitores/conversores **de** NSBMD (para Collada, PNG) | não escrevem NSBMD |
| hg-engine | compila código e dados; **não cobre mapas** | os mapas ficam fora dele (`land.json` depois do `make`) |
| **Ferramentas próprias (Python + ndspy)** | nenhuma dependência externa além do ndspy | **adotado**: `nsbmd.py`, `bdhc.py`, `land_data.py`, `matrix.py`, `mapa_teste.py` |

Wine e Xvfb ficam como alternativa, se um dia o diretor quiser desenhar no PDSMS e tiver o conversor legítimo. Não
foram instalados: sem o `g3dcvtr` eles não resolvem nada.

## 3. O pipeline próprio

Formatos lidos e escritos, com **ida e volta byte a byte em todos os 676 blocos de mapa da ROM**:

- `land_data.py`: o bloco (a/0/6/5) com as seções permissões/colisão 32×32, construções, modelo e alturas.
- `nsbmd.py`: o modelo 3D. Mantém cabeçalho, nó, materiais (texturas do conjunto da área), dicionários e comandos de
  render. Decodifica e reescreve as **listas de desenho** (comandos GX: vértices, UV, normais) de cada forma.
  Escala conferida: 1 tile = 1024 unidades, chão a 1 tile de altura = y 1024.
- `bdhc.py`: as alturas. Pontos, normais, distâncias, placas retangulares (planas ou rampas) e as faixas em z com a
  lista de acesso. Tem gerador a partir de retângulos em tiles e leitura de altura num ponto.
- `mapa_teste.py`: gera um bloco inteiro a partir de um desenho em código: chão por material, caminho, rampa, faces de
  penhasco, mato alto, flores, fileiras de árvores, alturas BDHC compatíveis com o modelo, colisão
  (bloqueado/mato alto/livre) e construção (placa). Do bloco original só aproveita os materiais.
- Integração: `land.json` com `{"land": N, "gerador": "modulo"}`. O `build.sh` grava o bloco na ROM pronta e cada
  build regenera tudo. Nada da Nintendo vai para o git: o bloco é gerado na hora a partir da ROM do diretor.

- `g3d_dict.py` (24/11, para o CP-DS-03B): dicionários de nomes G3D (árvore PATRICIA). Reproduz byte a byte os 3380
  dicionários dos 676 modelos. É a base para montar modelos com materiais de mais de um bloco doador (um setor de
  Lunia precisa de lagoa, mato alto, cerca e flores, que não estão todos num mesmo bloco do HGSS).
- `nsbmd.py` ganhou `read_materials`/`build_materials` e `model_parts`/`build_model`: o modelo inteiro (comandos de
  render, materiais com os dicionários de texturas e paletas, formas e listas de desenho) é remontado a partir das
  partes, com número livre de materiais e formas. Conferido: **os 676 modelos remontados byte a byte**.
- `nsbmd.compose`: monta um modelo com materiais de **vários blocos doadores** da mesma área (dados do material,
  ligação de textura e paleta, flag da forma; prefere o doador que desenha o material). No DeSmuME (24/11), o mapa
  de teste ganhou uma lagoa com a água do bloco 59 (sea_un/sea_on) junto com os materiais do bloco 57. A água
  aparece animada, com margem, e a colisão de água (0x15) bloqueia o jogador; o QA do mapa de teste continua
  passando inteiro.
- `mapa_grade.py` (gerador v2, 24/11): o setor é desenhado num **arquivo de texto**, com grade 32×32 de letras por
  tipo de tile, grade de alturas com rampas e lista de objetos. O gerador deriva tudo:
  - chão por material e água em duas camadas;
  - faces de penhasco em todo desnível e lados de rampa;
  - árvores em blocos 2×2;
  - alturas BDHC e colisão.

  O mapa de teste reescrito nesse formato (`provas/cp03a/mapa_teste.txt`) tem colisão idêntica nos 1024 tiles,
  alturas idênticas nos 1024 centros e objetos iguais aos do gerador v1. No DeSmuME o QA passa inteiro. Erros vistos e
  corrigidos: árvores cortadas ao meio entre duas fileiras (agora em blocos 2×2) e meia árvore com metade da textura
  tree01, que é espelhada (árvore solta = tree01_re). Limite visual que fica: uma árvore solta ainda parece estreita.

Limites atuais (o que o CP-DS-03B ainda precisa):
- Penhascos retos, sem as curvas e bordas arredondadas do HGSS.
- Árvores em fileiras de quads inclinados, como no HGSS, mas sem as variações de borda.
- Um material de cada vez por forma (as formas e materiais vêm do bloco doador, então a área tem de ter as texturas).
- Header e célula de matriz próprios (hoje o bloco ocupa a célula da Route 39).

## 4. Prova: mapa de teste no lugar da metade sul da Route 39

Bloco 57 (célula (8,6) da matriz 0, mapa 43), ligado a pé ao corredor norte de Breezeport. Essa saída não é a
Route 3 (decisão do diretor), por isso ela serve de banco de testes. Desenho (colisão gerada; `#` bloqueado, `e` mato
alto):

```
################################
################################
################################
################################
####........................####   plato (altura 2), arvores na borda norte
####........................####
####..##................##..####   arvores soltas no plato
####..##................##..####
####...............#........####   placa (construcao, colisao)
####........................####
####........................####
####........................####
##############...###############   face do penhasco (z=12) e a rampa (colunas 14-16)
####.........#...#..........####   rampa: altura 2 -> 1 (BDHC inclinado), lados bloqueados
####.........#...#..........####
####....##..................####   campina (altura 1)
####....##..............##..####
####....................##..####
####........................####
####........................####
####..eeeeee................####   mato alto (encontros)
####..eeeeee................####
####..eeeeee................####
####..eeeeee................####
####..eeeeee................####
####..eeeeee................####
####......##................####
####......##................####
#####################.....######   caminho para Breezeport (colunas 21-25, altura 1 dos dois lados)
#####################.....######
#####################.....######
#####################.....######
```

## 5. Resultado no DeSmuME (`qa_cp03a.py`) — **passou**

Altura = y da posição 3D do objeto do jogador (LocalMapObject +0x74, fx32), lida da memória a cada passo.

| Passo | Mapa, x, z | Altura (tiles) |
|---|---|---|
| corredor norte de Breezeport (atalho de QA no PC do quarto, só na build de prova) | 77, 279, 226 | 1,0 |
| entra pela divisa (caminho) | **43**, 279, 223 | 1,0 |
| caminho ao norte, depois a oeste | 43, 279, 211 → 271, 211 | 1,0 |
| pé da rampa | 43, 271, 207 | 1,0 |
| meio da rampa | 43, 271, 205 | **1,5** |
| platô | 43, 271, 202 | **2,0** |
| RIGHT ×3 contra a placa (construção) | fica em 274, 200 | 2,0 |
| DOWN ×3 na beira do penhasco, de cima | fica em 266, 203 | 2,0 |
| UP ×3 contra o penhasco, de baixo | fica em 266, 205 | 1,0 |
| LEFT ×3 contra a floresta da borda | fica em 260, 205 | 1,0 |
| volta pela divisa | **77**, 279, 226 | 1,0 |
| entra de novo | **43**, 279, 222 | 1,0 |

Capturas (`CP-DS-03A_evidencias.png`, entregue ao diretor): o terreno gerado aparece com caminho de terra, mato
alto, árvores soltas e de borda, flores, a face do penhasco com a rampa e a placa no platô. A grama azulada é a
luz noturna do HGSS: o relógio do emulador segue a hora UTC da execução.

Erros encontrados no caminho e corrigidos (todos vistos no emulador):
1. **Lista de desenho vazia** numa forma sem uso interrompia o desenho de todas as formas seguintes do bloco: só a
   1ª da ordem de render (flores) aparecia. Agora as formas sem uso recebem BEGIN/END mínimos.
2. Quads grandes (chão 32×12 tiles num quad só): subdivididos em até 4×4, como o HGSS faz.
3. Buracos de 1 tile ao lado da rampa e desnível aberto nas bordas (x 0–4, 28–32): chão e face do penhasco completos.
4. Altura lida no campo errado do objeto (+0x68): o certo é a posição 3D em +0x74.

Ferramentas novas de QA: `qa_cp03a.py`; `inplace_block.py` (grava um bloco gerado no lugar do original, mantendo
os savestates, quando cabe na vaga). O atalho de QA (`provas/cp03a/0901`) leva o jogador do PC do quarto ao
corredor norte de Breezeport. Ele existe só na build de prova.

## 6. Conclusão e próximo passo (CP-DS-03B)

O pipeline gera e integra terreno 3D próprio (modelo, alturas, colisão e objeto), com conexão natural a um mapa
vizinho, e funciona no jogo. Isso ainda não é uma localidade de Lunia: é a prova técnica pedida. Para a primeira
localidade original (CP-DS-03B):
- desenho por setor com função definida (referências: Route 30, 38, 47, Goldenrod);
- penhascos com bordas e curvas;
- variações de árvore;
- header e célula de matriz próprios;
- conexões da geografia aprovada (ex.: Route 1 norte → sul).
