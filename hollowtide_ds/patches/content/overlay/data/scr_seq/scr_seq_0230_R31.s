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

.include "data/scr_seq/include/event_R31.inc"


// text archive to grab from: 378.txt
// Hollowtide: Route 2, trecho norte (Route 31 do HGSS), ate a guarita que leva a Breezeport. GBA Palm080_*:
// placa; Qin e treinador com visao no zone_event 032. Entrada da Dark Cave e NPCs do HGSS sairam.

.data

scrdef scr_seq_R31_000
scrdef scr_seq_R31_001
scrdef scr_seq_R31_002
scrdef scr_seq_R31_003
scrdef scr_seq_R31_004
scrdef scr_seq_R31_005
scrdef_end

scr_seq_R31_002:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 0
	wait_button
	closemsg
	releaseall
	end

scr_seq_R31_000:
scr_seq_R31_001:
scr_seq_R31_003:
scr_seq_R31_004:
scr_seq_R31_005:
	end
	.balign 4
