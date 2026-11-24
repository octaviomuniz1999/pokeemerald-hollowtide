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

.include "data/scr_seq/include/event_T26GYM0101.inc"


.include "data/scr_seq/include/hollowtide_flags.inc"
// text archive to grab from: 606.txt
// Hollowtide: Teatro (ginasio da Jay) em Breezeport, no interior do ginasio de Olivine (placeholder). GBA
// PalmTeatro: refletores ESQUERDA, DIREITA, ESQUERDA (VAR_TEMP_x4000, zera ao sair, como VAR_TEMP_8 no GBA), Linh e
// Yumi lutam ao conversar, Jay so luta com o palco aceso. Echo Badge (2a insignia) e TM65 Shadow Claw (no GBA era
// TM Hex; o hg-engine nao tem TM de Hex — troca decidida pelo diretor em 24/11/2026).

.data

scrdef scr_seq_T26GYM0101_000
scrdef scr_seq_T26GYM0101_001
scrdef scr_seq_T26GYM0101_002
scrdef scr_seq_T26GYM0101_003
scrdef scr_seq_T26GYM0101_004
scrdef scr_seq_T26GYM0101_005
scrdef scr_seq_T26GYM0101_006
scrdef scr_seq_T26GYM0101_007
scrdef scr_seq_T26GYM0101_008
scrdef scr_seq_T26GYM0101_009
scrdef scr_seq_T26GYM0101_010
scrdef scr_seq_T26GYM0101_011
scrdef scr_seq_T26GYM0101_012
scrdef_end

// Jay
scr_seq_T26GYM0101_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_HT_DEFEATED_JAY, _HT_JayAfter
	compare VAR_TEMP_x4000, 3
	goto_if_ne _HT_JayBlocked
	npc_msg 1
	closemsg
	trainer_battle 484, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq _HT_Lost
	settrainerflag 484
	give_badge BADGE_HIVE
	setflag FLAG_HT_DEFEATED_JAY
	setvar VAR_UNK_4078, 2
	play_fanfare SEQ_ME_BADGE
	npc_msg 2
	wait_fanfare
	wait_button
	closemsg
	setvar VAR_SPECIAL_x8004, ITEM_TM065
	setvar VAR_SPECIAL_x8005, 1
	callstd std_obtain_item_verbose
	closemsg
	releaseall
	end

_HT_JayBlocked:
	npc_msg 0
	wait_button
	closemsg
	releaseall
	end

_HT_JayAfter:
	npc_msg 3
	wait_button
	closemsg
	releaseall
	end

_HT_Lost:
	white_out
	releaseall
	end

// Linh e Yumi: lutam ao conversar
scr_seq_T26GYM0101_004:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_defeated 486, _HT_LinhAfter
	npc_msg 4
	closemsg
	trainer_battle 486, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq _HT_Lost
	settrainerflag 486
	releaseall
	end

_HT_LinhAfter:
	npc_msg 12
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26GYM0101_005:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_defeated 491, _HT_YumiAfter
	npc_msg 5
	closemsg
	trainer_battle 491, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq _HT_Lost
	settrainerflag 491
	releaseall
	end

_HT_YumiAfter:
	npc_msg 13
	wait_button
	closemsg
	releaseall
	end

// refletor da ESQUERDA
scr_seq_T26GYM0101_008:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_set FLAG_HT_DEFEATED_JAY, _HT_Done
	compare VAR_TEMP_x4000, 0
	goto_if_eq _HT_StepOne
	compare VAR_TEMP_x4000, 2
	goto_if_eq _HT_StepThree
	goto _HT_Wrong

// refletor da DIREITA
scr_seq_T26GYM0101_009:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_set FLAG_HT_DEFEATED_JAY, _HT_Done
	compare VAR_TEMP_x4000, 1
	goto_if_ne _HT_Wrong
	setvar VAR_TEMP_x4000, 2
	npc_msg 7
	wait_button
	closemsg
	releaseall
	end

_HT_StepOne:
	setvar VAR_TEMP_x4000, 1
	npc_msg 6
	wait_button
	closemsg
	releaseall
	end

_HT_StepThree:
	setvar VAR_TEMP_x4000, 3
_HT_Done:
	npc_msg 9
	wait_button
	closemsg
	releaseall
	end

_HT_Wrong:
	setvar VAR_TEMP_x4000, 0
	npc_msg 8
	wait_button
	closemsg
	releaseall
	end

// bilhete no painel do meio e placa dos refletores
scr_seq_T26GYM0101_010:
	play_se SEQ_SE_DP_SELECT
	lockall
	compare VAR_TEMP_x4000, 3
	goto_if_eq _HT_Done
	npc_msg 10
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26GYM0101_011:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 11
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26GYM0101_001:
scr_seq_T26GYM0101_002:
scr_seq_T26GYM0101_003:
scr_seq_T26GYM0101_006:
scr_seq_T26GYM0101_007:
scr_seq_T26GYM0101_012:
	end
	.balign 4
