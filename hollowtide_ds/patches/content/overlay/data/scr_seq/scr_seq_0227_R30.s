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

.include "data/scr_seq/include/event_R30.inc"


// text archive to grab from: 375.txt
// Hollowtide: Route 2, trecho sul (Route 30 do HGSS). GBA Palm080_*: placa, porta trancada; Liang e Mei Lan sao
// treinadores com visao no zone_event 031. Cenas do HGSS (Joey, Mikey, casa do Mr. Pokemon) sairam.

.data

scrdef scr_seq_R30_000
scrdef scr_seq_R30_001
scrdef scr_seq_R30_002
scrdef scr_seq_R30_003
scrdef scr_seq_R30_004
scrdef scr_seq_R30_005
scrdef scr_seq_R30_006
scrdef scr_seq_R30_007
scrdef scr_seq_R30_008
scrdef scr_seq_R30_009
scrdef scr_seq_R30_010
scrdef_end

scr_seq_R30_005:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 0
	wait_button
	closemsg
	releaseall
	end

scr_seq_R30_006:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 1
	wait_button
	closemsg
	releaseall
	end

scr_seq_R30_000:
scr_seq_R30_001:
scr_seq_R30_002:
scr_seq_R30_003:
scr_seq_R30_004:
scr_seq_R30_007:
scr_seq_R30_008:
scr_seq_R30_009:
scr_seq_R30_010:
	end
	.balign 4
