# Músicas em MIDI → GBA

- `midinfo.py ARQ.mid`: faixas, instrumentos GM, notas e andamento.
- `midnotes.py ARQ.mid`: polifonia por canal e deslocamentos (em compassos) em que a música se repete — o maior
  é o tamanho do loop; a tabela por compasso mostra onde ele começa.
- `midloop.py IN OUT COMPASSO_INI COMPASSO_FIM`: corta no fim do loop e grava os marcadores `[`/`]` do mid2agb.

Temas da Cynthia (MIDIs do diretor): pré-batalha loop 3–48, batalha loop 6–66; velocidades ×1,6 e ×2,4;
voicegroup `sound/voicegroups/ht_cynthia.inc`; entradas em `sound/songs/midi/midi.cfg`, `sound/song_table.inc` e
`include/constants/songs.h` (610 e 611, depois dos fonemas).
