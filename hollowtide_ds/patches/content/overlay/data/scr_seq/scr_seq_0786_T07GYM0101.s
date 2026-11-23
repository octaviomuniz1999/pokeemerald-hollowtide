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

.include "data/scr_seq/include/event_T07GYM0101.inc"


.include "data/scr_seq/include/hollowtide_flags.inc"
// text archive to grab from: 492.txt
// Hollowtide: ginasio do Nevard em Harvestvale (interior do ginasio da Erika, placeholder ate a arte; o
// quebra-cabeca das comportas do GBA ainda nao foi portado). Falas do GBA (RustboroCity_Gym_Text_*).

.data

scrdef scr_seq_T07GYM0101_000
scrdef scr_seq_T07GYM0101_001
scrdef scr_seq_T07GYM0101_002
scrdef_end

// Nevard
scr_seq_T07GYM0101_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_HT_DEFEATED_NEVARD, _HT_NevardAfter
	npc_msg 0
	closemsg
	trainer_battle 497, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq _HT_Lost
	give_badge BADGE_ZEPHYR
	settrainerflag 463
	settrainerflag 507
	settrainerflag 471
	setflag FLAG_HT_DEFEATED_NEVARD
	setvar VAR_SCENE_CHERRYGROVE_CITY_OW, 3
	buffer_players_name 0
	npc_msg 2
	play_fanfare SEQ_ME_BADGE
	wait_fanfare
	npc_msg 3
	closemsg
	setvar VAR_SPECIAL_x8004, ITEM_TM009
	setvar VAR_SPECIAL_x8005, 1
	callstd std_obtain_item_verbose
	npc_msg 4
	wait_button
	closemsg
	releaseall
	end

_HT_NevardAfter:
	npc_msg 5
	wait_button
	closemsg
	releaseall
	end

_HT_Lost:
	white_out
	releaseall
	end

// estatuas da entrada
scr_seq_T07GYM0101_001:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 6
	wait_button
	closemsg
	releaseall
	end

scr_seq_T07GYM0101_002:
	end
	.balign 4
