.include "asm/include/interop_macros.inc"

.include "asm/include/scriptmacros.inc"
.include "asm/include/flags.inc"
.include "asm/include/soundeffects.inc"
.include "asm/include/vars.inc"

.include "asm/include/events.inc"
.include "asm/include/game_stats.inc"
.include "asm/include/maps.inc"
.include "asm/include/map_sections.inc"
.include "asm/include/movements.inc"
.include "asm/include/rankings.inc"
.include "asm/include/spawns.inc"
.include "asm/include/std_scripts.inc"
.include "asm/include/trainers.inc"

#include "constants/item.h"
#include "constants/moves.h"
#include "constants/species.h"

.include "data/scr_seq/include/event_R29.inc"


// text archive to grab from: 373.txt
// Hollowtide: Route 1 (Route 29 do HGSS). Reescrito a partir do GBA (Palm050_*): o andarilho e as placas; os
// treinadores Kai e Min sao objetos com visao no zone_event 030 (_std_npc_trainer + falas do Trainers.c).
// Cenas do HGSS (tutorial de captura da Lyra) e NPCs de Johto sairam. Numeros dos scripts como no HGSS.

.data

scrdef scr_seq_R29_000
scrdef scr_seq_R29_001
scrdef scr_seq_R29_002
scrdef scr_seq_R29_003
scrdef scr_seq_R29_004
scrdef scr_seq_R29_005
scrdef scr_seq_R29_006
scrdef scr_seq_R29_007
scrdef scr_seq_R29_008
scrdef_end

scr_seq_R29_002:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	npc_msg 0
	wait_button
	closemsg
	releaseall
	end

scr_seq_R29_004:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 1
	wait_button
	closemsg
	releaseall
	end

scr_seq_R29_005:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 2
	wait_button
	closemsg
	releaseall
	end

scr_seq_R29_000:
scr_seq_R29_001:
scr_seq_R29_003:
scr_seq_R29_006:
scr_seq_R29_007:
scr_seq_R29_008:
	end
	.balign 4
