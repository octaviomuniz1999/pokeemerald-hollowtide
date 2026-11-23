#!/usr/bin/env bash
# Monta a ROM DS do Hollowtide: hg-engine (commit fixo) + ROM HeartGold EUA (IPKE) do diretor + os patches do repositorio.
#
# Uso: tools/hollowtide_ds/build.sh ROM_HEARTGOLD PASTA_HG_ENGINE [PASTA_DE_PATCHES ...]
#   PASTA_DE_PATCHES: padrao hollowtide_ds/patches/content (o jogo); hollowtide_ds/provas/fase0 refaz a prova da Fase 0.
# Saida: PASTA_HG_ENGINE/test.nds.
#
# Nada da Nintendo entra no git: os scripts, eventos e textos originais sao extraidos da ROM a cada build
# (`make dump_scripts`) e os nossos arquivos sao patches sobre esse despejo e sobre o hg-engine.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
ROM="$(realpath "$1")"; HG="$2"; shift 2
PATCH_DIRS=()
for d in "$@"; do PATCH_DIRS+=("$(realpath "$d")"); done
[ ${#PATCH_DIRS[@]} -eq 0 ] && PATCH_DIRS=("$REPO/hollowtide_ds/patches/content")
for d in "${PATCH_DIRS[@]}"; do [ -d "$d" ] || { echo "pasta de patches inexistente: $d"; exit 1; }; done
COMMIT="$(cat "$REPO/hollowtide_ds/hg-engine.commit")"

[ "$(dd if="$ROM" bs=1 skip=12 count=4 2>/dev/null)" = "IPKE" ] || { echo "a ROM precisa ser HeartGold EUA (IPKE)"; exit 1; }

if [ ! -d "$HG/.git" ]; then
    git clone https://github.com/BluRosie/hg-engine "$HG"
fi
cd "$HG"
git fetch -q origin "$COMMIT" 2>/dev/null || true
git checkout -q -f "$COMMIT"
git submodule update --init --recursive -q
# limpa edicoes e despejos de builds anteriores (build/ fica, para recompilar so o que mudou)
git checkout -q -- .
git clean -q -fd data/scr_seq data/eventdata data/text
cp "$ROM" rom.nds
[ -d .venv ] || { python3 -m venv .venv; .venv/bin/pip install -q -r requirements.txt; }
. .venv/bin/activate

git apply "$REPO/hollowtide_ds/patches/0001-hg-engine-base.patch"

# despejo dos scripts e eventos originais; o texto despejado pelo hg-engine nao volta igual ao ROM, entao sai
# todo e entram so os arquivos que os patches editam, extraidos pelo msg_dump.py (byte a byte)
make -s dump_scripts DUMP_ROM=rom.nds > build_dump.log 2>&1 || { tail -20 build_dump.log; exit 1; }
git checkout -q -- data/text/keys.csv
rm -f data/text/custom/*.txt
TXT="$(mktemp -d)"
python3 "$HERE/msg_dump.py" "$HG" rom.nds "$TXT" > /dev/null
for d in "${PATCH_DIRS[@]}"; do
    # arquivos inteiros nossos (scripts reescritos): copiados por cima do despejo antes dos patches da pasta
    if [ -d "$d/overlay" ]; then cp -r "$d/overlay/." .; echo "overlay: ${d#$REPO/}/overlay"; fi
    for p in "$d"/*.patch; do
        [ -e "$p" ] || continue
        for f in $(grep -oE '^\+\+\+ b/data/text/custom/[0-9]{3}\.txt' "$p" | sed 's|^+++ b/||'); do
            [ -e "$f" ] || cp "$TXT/$(basename "$f")" "$f"
        done
        patch -s -p1 --binary < "$p"
        echo "patch: ${p#$REPO/}"
    done
done
rm -rf "$TXT"

# o header gerado sobrevive a limpezas de build/, mas os .c que ele gera nao: forca a geracao
[ -e build/learnset/MachineMoveLearnsets.c ] || rm -f include/constants/generated/learnsets.h
make -j"$(nproc)" > build_make.log 2>&1 || { grep -nE "error|Error" build_make.log | head -20; exit 1; }

# mapas: o hg-engine nao cobre a matriz; as edicoes (matrix.json) entram direto na ROM pronta
MATRIX=()
for d in "${PATCH_DIRS[@]}"; do [ -e "$d/matrix.json" ] && MATRIX+=("$d/matrix.json"); done
[ ${#MATRIX[@]} -gt 0 ] && python3 "$HERE/matrix.py" test.nds "${MATRIX[@]}"
# trocas com NPC (NARC a/1/1/2): trades.json de cada pasta
TRADES=()
for d in "${PATCH_DIRS[@]}"; do [ -e "$d/trades.json" ] && TRADES+=("$d/trades.json"); done
[ ${#TRADES[@]} -gt 0 ] && python3 "$HERE/npc_trades.py" apply test.nds "${TRADES[@]}"
echo "ok: $HG/test.nds"
