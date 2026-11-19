#!/bin/bash
# QA completo: intro -> lab -> Rota 1 -> Harvestvale -> transicoes -> Cap. 1 -> Cap. 2 -> Route 2 (treinadores). Uso: qa_completo.sh RUNNER WORKDIR
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd); R=$1; W=$2; mkdir -p "$W"
SB1=$(awk '$2=="gSaveBlock1Ptr" && $1 ~ /^0x03/ {print substr($1,3); exit}' "$ROOT/pokeemerald.map")
{ cat "$ROOT/tools/hollowtide_qa/roteiros/01_intro_ate_casa.txt"; echo pos; echo "expect_map 1 0"; echo "savestate $W/casa.ss"; } > "$W/intro.txt"
"$R" "$ROOT/pokeemerald.gba" "$W/intro.txt" - "$SB1" | tail -2
python3 -I "$ROOT/tools/hollowtide_qa/fluxo_inicial.py" "$ROOT/pokeemerald.gba" "$R" "$W" "$W/casa.ss" | tail -1
python3 -I "$ROOT/tools/hollowtide_qa/fluxo_transicoes.py" "$ROOT/pokeemerald.gba" "$R" "$W" "$W/e2e_colheita.ss" | sed -n "/^RESUMO/,$ p"
python3 -I "$ROOT/tools/hollowtide_qa/fluxo_cap1_eventos.py" "$ROOT/pokeemerald.gba" "$R" "$W" "$W/e2e_colheita.ss" | tail -12
python3 -I "$ROOT/tools/hollowtide_qa/fluxo_cap2_eventos.py" "$ROOT/pokeemerald.gba" "$R" "$W" "$W/cap1_pos_nevard.ss" | tail -16
python3 -I "$ROOT/tools/hollowtide_qa/fluxo_rota2.py" "$ROOT/pokeemerald.gba" "$R" "$W" "$W/cap1_pos_nevard.ss" | tail -11
python3 -I "$ROOT/tools/hollowtide_qa/fluxo_rota3.py" "$ROOT/pokeemerald.gba" "$R" "$W" "$W/cap2_pos_jay.ss" | tail -16
