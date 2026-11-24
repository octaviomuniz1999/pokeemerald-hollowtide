# Ferramentas da versão DS (Hollowtide em HeartGold / hg-engine)

## Build

- `build.sh ROM_HEARTGOLD PASTA_HG_ENGINE [PASTAS_DE_PATCHES...]`: hg-engine no commit de
  `hollowtide_ds/hg-engine.commit` + ROM HeartGold EUA (IPKE) + `hollowtide_ds/patches/0001-hg-engine-base.patch` +
  os patches de conteúdo (padrão `hollowtide_ds/patches/content`). Extrai da ROM, a cada build, os scripts, eventos e
  textos originais (`make dump_scripts`), aplica os patches e compila → `PASTA_HG_ENGINE/test.nds`. ~1–3 min.
- `matrix.py ROM matrix.json…` / `matrix.py ROM --show N X0 Y0 X1 Y1`: matrizes de mapa (a/0/4/1); o `build.sh`
  aplica o `matrix.json` de cada pasta de patches depois do `make`.
- `land_data.py ROM land.json…` / `land_data.py ROM --show BLOCO`: blocos de mapa (a/0/6/5): objetos 3D (construções)
  e colisão/comportamento de tile; ida e volta byte a byte nos 676 blocos. O `build.sh` aplica o `land.json` de cada
  pasta de patches depois da matriz. Coordenadas: tile (tx, ty) do bloco ↔ objeto em x = tx−16+0,5, z = ty−16+0,5;
  mundo = célula da matriz × 32 + tile.
- `nsbmd.py`, `bdhc.py`, `g3d_dict.py`: modelo 3D, alturas e dicionários G3D (ida e volta byte a byte nos 676
  blocos); `nsbmd.compose` monta um modelo com materiais de vários blocos doadores da mesma área.
- `mapa_grade.py`: **gerador de setor a partir de uma grade de texto** (ver abaixo); `land.json` com
  `{"land": N, "grade": "arquivo.txt"}`.
- `text_patch.py HG_ENGINE`: `hollowtide_ds/data/texts.json` → `0500-texts.patch`. **Rodar depois de editar o
  `texts.json`**: a build usa o patch, não o JSON.
- `msg_dump.py HG_ENGINE ROM SAIDA [--check]`: textos (a/0/2/7) em `.txt` que voltam ao ROM byte a byte (829/829); o
  despejo de texto do próprio hg-engine perde as quebras de linha e não serve para recompilar.

## QA

- `ds_driver.py`: DeSmuME sem tela (`py-desmume`, `SDL_VIDEODRIVER=dummy`): botões, toque, capturas das duas telas,
  savestates (com os ponteiros do jogo ao lado, em `.ptr`) e leitura de mapa/posição do jogador pelos ganchos
  `FieldSystem_FlagCheck` e `PlayerAvatar_GetXCoord` (endereços do `rom.ld` do hg-engine).
- `ds_intro.py ROM SAIDA.dst`: jogo novo até o quarto do jogador (estado base dos testes; ~1m45).
- `prova_fase0.py ROM ESTADO_BASE CAPTURAS`: a prova de edição da Fase 0 (texto, script, presente, batalha vencida pelo
  toque, warp para a Route 29, encontro selvagem).

- `qa_cap1.py`, `qa_cap2.py`: Cap. 1 (quarto → Nevard → Breezeport) e Cap. 2 (Breezeport → Jay → saída norte).
- `qa_cp01.py ROM ESTADO_BASE PASTA`: prova de edição de mapa do CP-DS-01 (placa nova em Dawnmere: modelo, colisão
  dos dois lados, leitura, divisa com a Route 1 nos dois sentidos, salvar pelo menu, reiniciar, CONTINUE).
- `audit_dialogos.py HG_ENGINE ROM SAIDA.md`: auditoria das mensagens chamadas pelos scripts dos mapas jogáveis
  (referência, largura em pixels pela fonte do DS, linhas por caixa, nomes de Johto/Kanto, português, falas iguais às
  do HGSS), separando o que é alcançável do código morto.

**Estados salvos valem só para a ROM em que foram feitos.** O savestate guarda o mapa já carregado (e a tabela de
arquivos do cartucho); para testar uma edição, gere o estado base com `ds_intro.py` na ROM nova.

Ambiente: `python3 -m venv dsqa && dsqa/bin/pip install py-desmume ndspy`. A ROM nunca entra no repositório.

## Como desenhar um setor (mapa_grade.py)

Um setor é um bloco de 32×32 tiles. O arquivo de texto tem quatro seções:

```
[doadores]      blocos do HGSS de onde vêm as texturas, todos da mesma área do mapa onde o setor vai ficar
2 0 5 4         (área 2 = Dawnmere/Route 29: 0 New Bark, 2 e 5 Route 29/Cherrygrove, 4 Cherrygrove)
[tiles]         32 linhas de 32 letras
[alturas]       32 linhas de 32 caracteres: altura em tiles (0-9) ou r (rampa entre o vizinho norte e o sul)
[objetos]       "modelo x z" (construções da lista da área; a casa só com interior funcional)
```

| Letra | Tile | Colisão |
|---|---|---|
| `.` | grama | livre |
| `=` | caminho de terra (bordas e cantos do HGSS automáticos) | livre |
| `e` | mato alto | encontros |
| `f` `g` `h` | flores (três tipos) | livre |
| `~` | água (margem e cantos automáticos) | água |
| `T` | árvore: blocos 2×2 (pares viram um quad de 4 tiles) | bloqueado |
| `c` | cerca (trechos horizontais e verticais) | bloqueado |
| `#` | bloqueado invisível (beira de penhasco, lados de rampa) | bloqueado |
| `S` | tile de objeto (o modelo vem de `[objetos]`) | bloqueado |

O gerador cria sozinho:
- faces de penhasco em todo desnível entre tiles que não são rampa;
- as superfícies das rampas;
- as alturas BDHC;
- a colisão;
- quads de no máximo 4×4 tiles (polígonos maiores somem no DS).

Boas práticas, aprendidas no emulador:
- caminhos em trechos retos com curvas em L, de 2 a 3 tiles de largura (degraus de 1 tile geram cantos demais);
- as divisas têm de bater com o setor vizinho: mesmas colunas abertas e mesma altura nos dois lados;
- teste: build de prova com `land.json`, atalho de QA no PC do quarto (`provas/cp03b/0911`) e um `qa_*.py` com as
  colisões esperadas.

Limites conhecidos: os cantos côncavos da lagoa ainda mostram um pequeno corte; penhascos retos, sem as curvas do
HGSS; não há casas (precisam de interior e warp).
