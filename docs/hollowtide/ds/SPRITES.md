# Lacunas de sprites do hg-engine para Lunia

Especies e formas conferidas: 248; com alguma lacuna: 0.

| Pasta | Batalha | Seguidor | Ícone |
|---|---|---|---|
Conferido em 23/11/2026 (hg-engine `b578c990`):
- As 248 espécies e formas que o GBA 23ap usa (encontros, times, presentes) — inclusive Zorua/Zoroark de Hisui,
  Urshifu Golpe Fluido, Meowscarada, Dhelmise — e as formas de batalha dos times do cânone (Mega Charizard X,
  Mega Garchomp, Mega Latios, Kyogre Primal): **nenhuma lacuna** (batalha, seguidor e ícone).
- As 128 famílias citadas em `POKEDEX_LUNIA.md` (mais Jangmo-o/Hakamo-o/Kommo-o): **nenhuma lacuna**.
- Critério: no hg-engine a espécie sem arte usa a do Bulbasaur (mesmo arquivo); exemplos de lacunas reais fora de
  Lunia: Bramblin (batalha), Frigibax e Chi-Yu (seguidor).
Refazer: `tools/hollowtide_ds/lunia_inventory.py` e `tools/hollowtide_ds/sprite_gaps.py HG_ENGINE docs/hollowtide/ds/lunia_inventory.json docs/hollowtide/ds/SPRITES.md`.
