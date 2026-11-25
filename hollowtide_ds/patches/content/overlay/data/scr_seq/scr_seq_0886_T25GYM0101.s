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

.include "data/scr_seq/include/event_T25GYM0101.inc"


// text archive to grab from: 582.txt


.include "data/scr_seq/include/hollowtide_flags.inc"
// text archive to grab from: 582.txt
// Hollowtide: ginasio de Ferralia (GBA MauvilleCity_Gym do Hollowtide, lider Vessel, tipo Aco) no interior do ginasio
// de Goldenrod. Vessel (treinador 513) da a 3a insignia (Resonance Badge, no lugar da Plain Badge) e a TM91 Flash
// Cannon, como no GBA. O quebra-cabeca de chaves e portoes eletricos do GBA fica de fora; os treinadores lutam pela
// visao (std_npc_trainer, falas do 0100).

.data

scrdef scr_seq_T25GYM0101_000
scrdef scr_seq_T25GYM0101_001
scrdef scr_seq_T25GYM0101_002
scrdef scr_seq_T25GYM0101_003
scrdef scr_seq_T25GYM0101_004
scrdef_end

// Vessel
scr_seq_T25GYM0101_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_HT_DEFEATED_VESSEL, _HT_VesselAfter
	npc_msg 1
	closemsg
	trainer_battle 513, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq _HT_Lost
	settrainerflag 513
	give_badge BADGE_PLAIN
	setflag FLAG_HT_DEFEATED_VESSEL
	buffer_players_name 0
	play_fanfare SEQ_ME_BADGE
	npc_msg 2
	wait_fanfare
	wait_button
	closemsg
	setvar VAR_SPECIAL_x8004, ITEM_TM091
	setvar VAR_SPECIAL_x8005, 1
	callstd std_obtain_item_verbose
	npc_msg 3
	wait_button
	closemsg
	releaseall
	end

_HT_VesselAfter:
	npc_msg 4
	wait_button
	closemsg
	releaseall
	end

_HT_Lost:
	white_out
	releaseall
	end

// gatilho da Whitney no meio do ginasio: sai (zona 0719)
scr_seq_T25GYM0101_001:
	end

// guia do ginasio
scr_seq_T25GYM0101_002:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	goto_if_set FLAG_HT_DEFEATED_VESSEL, _HT_GuideAfter
	npc_msg 5
	wait_button
	closemsg
	releaseall
	end

_HT_GuideAfter:
	npc_msg 6
	wait_button
	closemsg
	releaseall
	end

// estatuas da entrada
scr_seq_T25GYM0101_003:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	goto_if_set FLAG_HT_DEFEATED_VESSEL, _HT_StatueCertified
	npc_msg 7
	wait_button
	closemsg
	releaseall
	end

_HT_StatueCertified:
	npc_msg 8
	wait_button
	closemsg
	releaseall
	end

scr_seq_T25GYM0101_004:
	end
	.balign 4
