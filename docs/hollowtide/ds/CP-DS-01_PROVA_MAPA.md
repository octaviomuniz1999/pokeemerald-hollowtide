# CP-DS-01 — Prova real de integração de mapa (24/11/2026) — **passou**

Mapa: **Dawnmere Village** (MAP_T20, id 60; bloco land_data 0 na célula (21,12) da matriz 0). Alteração pequena,
visível e reversível: uma **placa da Route 1** na saída oeste (tile 5,12 do bloco = mundo 677,396), com modelo 3D,
colisão e evento de leitura.

## A. Alterações

| Arquivo | O quê |
|---|---|
| `tools/hollowtide_ds/land_data.py` (novo) | lê/regrava blocos a/0/6/5 (permissões 32×32, construções de 48 bytes, terreno e alturas intactos); ida e volta byte a byte nos 676 blocos da ROM |
| `hollowtide_ds/patches/content/land.json` (novo) | bloco 0: + construção modelo 30 (placa de madeira, mesma das 4 placas da vila; está na lista de construções da área 2 → a/0/4/3[0]) no tile (5,12), y=1; tile (5,12) bloqueado (bit 0x8000) |
| `tools/hollowtide_ds/build.sh` | aplica os `land.json` na ROM pronta, depois da matriz |
| `hollowtide_ds/patches/content/0621-dawnmere-route-sign.patch` (novo) | placa (bg_event) em 677,396, script 19 |
| `overlay/data/scr_seq/scr_seq_0842_T20.s` | `scr_seq_T20_018`: lê a mensagem 8 |
| `hollowtide_ds/data/texts.json` → `0500-texts.patch` | 542/8 = `Route101_Text_RouteSign` do GBA, ↓ → ← (no DS a Route 1 e Harvestvale ficam a oeste; `_por_que`) |
| `tools/hollowtide_ds/gba_text.py` | setas `{LEFT_ARROW}`… → ← ↑ ↓ → (011B–011E do charmap do DS) |

Formato conferido nos dados: o objeto de um tile em (tx, ty) fica em x = tx−16+0,5, z = ty−16+0,5 (as 4 placas
originais de New Bark caem exatamente nos tiles das placas dos eventos).

## B. Testes

- Build: `tools/hollowtide_ds/build.sh heartgold_us.nds /home/user/blurosie/hg-engine` → `land_data: 1 bloco(s)
  editado(s)`, `ok: test.nds` (1 min 17 s).
- Emulador: DeSmuME (`py-desmume`). Estado base: `ds_intro.py` na ROM nova. QA: `tools/hollowtide_ds/qa_cp01.py`.

| Passo | Resultado (mapa, x, y) |
|---|---|
| quarto → mãe → Dawnmere → laboratório → inicial → Route 1 pela divisa oeste | (33, 671, 398) |
| volta a pé pela divisa | (60, 672, 398) |
| embaixo da placa | (60, 677, 397) |
| UP ×3 contra a placa | continua (60, 677, 397) — colide |
| de (678,396), LEFT ×3 contra a placa | continua (60, 678, 396) — colide |
| leitura | "Route 1 / ← Harvestvale" |
| sai de novo para a Route 1 e volta | (33, 671, 398) → (60, 672, 398) |
| salvar pelo menu (SAVE → Yes → "You saved…"), reiniciar o console, CONTINUE | volta embaixo da placa; UP abre a mesma caixa (interior idêntico pixel a pixel) |
| **RESULTADO** | **ok** |

Erros encontrados no caminho:
1. A placa mostrou "Call your mom on your Pokégear…": o `texts.json` foi editado sem rodar `text_patch.py`. A
   build usa o `0500-texts.patch`, então a mensagem 8 continuava a do HGSS. Corrigido, e a regra ficou no README.
2. Andar contra uma placa abre a leitura (comportamento do HGSS). O QA não pode virar para a placa antes de abrir o
   menu de salvar.
3. Um DeSmuME novo, em outro processo, não reconhece o `.dsv` gravado e cai em NEW GAME. Por isso o carregamento
   é provado com o reset do console, que mantém a memória do save, como um desligar e ligar.

## C. Evidência visual

`CP-DS-01_evidencias.png` (entregue ao diretor; capturas não entram no git). Mostra: a placa nova, as duas colisões,
a leitura, a divisa com a Route 1, o save e o CONTINUE.

## D. Entregável

`Pokemon_Hollowtide_DS_2026-11-24-cp01.xdelta` sobre HeartGold EUA (SHA-1 `4fcded0e…5a37`). ROM resultante SHA-1
`bdff0a46cb9735b3201be3d4805dcba453384297`, conferida: o patch reproduz a build testada.

## O que esta prova cobre e o que não cobre

Cobre: objeto 3D novo num bloco existente, colisão, evento, texto, compilação, conexão exterior nos dois sentidos,
save/load. **Não cobre terreno 3D novo** (`.nsbmd` + `.bdhc`). É o próximo bloqueio técnico
(`CP-DS-00_AUDITORIA.md` §5) e condição para corrigir a geografia de Route 2, Breezeport e Route 3 (CP-DS-03+).
