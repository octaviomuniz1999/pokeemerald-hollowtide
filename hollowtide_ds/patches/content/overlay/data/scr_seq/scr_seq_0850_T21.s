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

.include "data/scr_seq/include/event_T21.inc"


.include "data/scr_seq/include/hollowtide_flags.inc"
// text archive to grab from: 550.txt
// Hollowtide: Harvestvale (Cherrygrove do HGSS). Reescrito a partir do GBA (Palm060/062/064/071/072/073/080):
// fazendeiro, quiosque da Team Palm (recruta com a chave), valvula da irrigacao, ginasio do Nevard (porta da
// casa R0401) fechado ate a agua voltar, saida norte (Route 2) fechada ate vencer o Nevard.
// VAR_SCENE_CHERRYGROVE_CITY_OW: 0 chegada | 1 ginasio fechado | 2 agua de volta | 3 Nevard vencido.

.data

scrdef scr_seq_T21_000
scrdef scr_seq_T21_001
scrdef scr_seq_T21_002
scrdef scr_seq_T21_003
scrdef scr_seq_T21_004
scrdef scr_seq_T21_005
scrdef scr_seq_T21_006
scrdef scr_seq_T21_007
scrdef scr_seq_T21_008
scrdef scr_seq_T21_009
scrdef scr_seq_T21_010
scrdef scr_seq_T21_011
scrdef scr_seq_T21_012
scrdef scr_seq_T21_013
scrdef_end

// fazendeiro (e quem chama na chegada)
scr_seq_T21_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_HT_IRRIGATION_RESTORED, _HT_FarmerRestored
	npc_msg 0
	wait_button
	closemsg
	releaseall
	end

_HT_FarmerRestored:
	npc_msg 1
	wait_button
	closemsg
	releaseall
	end

// chegada pelo leste (Route 1)
scr_seq_T21_001:
	lockall
	setvar VAR_SCENE_CHERRYGROVE_CITY_OW, 1
	goto_if_set FLAG_HT_HARVESTVALE_GUIDE_INTRO, _HT_ArrivalEnd
	setflag FLAG_HT_HARVESTVALE_GUIDE_INTRO
	apply_movement obj_T21_gsoldman1, _HT_Notice
	wait_movement
	npc_msg 6
	wait_button
	closemsg
_HT_ArrivalEnd:
	releaseall
	end

// saida norte (Route 2): fechada ate vencer o Nevard
scr_seq_T21_002:
	lockall
	goto_if_set FLAG_HT_DEFEATED_NEVARD, _HT_ExitOk
	npc_msg 8
	wait_button
	closemsg
	apply_movement obj_player, _HT_StepDown
	wait_movement
	releaseall
	end

_HT_ExitOk:
	setvar VAR_SCENE_CHERRYGROVE_CITY_OW, 3
	releaseall
	end

// recruta da Team Palm no quiosque
scr_seq_T21_004:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_HT_IRRIGATION_RESTORED, _HT_RecruitRestored
	goto_if_defeated 483, _HT_RecruitHint
	npc_msg 2
	closemsg
	trainer_battle 483, 0, 0, 0
	check_battle_won VAR_SPECIAL_RESULT
	compare VAR_SPECIAL_RESULT, 0
	goto_if_eq _HT_Lost
	releaseall
	end

_HT_RecruitHint:
	npc_msg 4
	wait_button
	closemsg
	releaseall
	end

_HT_RecruitRestored:
	npc_msg 5
	wait_button
	closemsg
	releaseall
	end

_HT_Lost:
	white_out
	releaseall
	end

// porta do ginasio fechada ate a agua voltar
scr_seq_T21_003:
	lockall
	goto_if_set FLAG_HT_IRRIGATION_RESTORED, _HT_GymOpen
	npc_msg 10
	wait_button
	closemsg
	apply_movement obj_player, _HT_StepDown
	wait_movement
	releaseall
	end

_HT_GymOpen:
	setvar VAR_SCENE_CHERRYGROVE_CITY_OW, 2
	releaseall
	end

// valvula
scr_seq_T21_009:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_set FLAG_HT_IRRIGATION_RESTORED, _HT_ValveDone
	goto_if_not_defeated 483, _HT_ValveLocked
	setflag FLAG_HT_IRRIGATION_RESTORED
	setvar VAR_SCENE_CHERRYGROVE_CITY_OW, 2
	buffer_players_name 0
	npc_msg 14
	wait_button
	closemsg
	releaseall
	end

_HT_ValveLocked:
	npc_msg 13
	wait_button
	closemsg
	releaseall
	end

_HT_ValveDone:
	npc_msg 15
	wait_button
	closemsg
	releaseall
	end

// placa do ginasio (muda quando a agua volta)
scr_seq_T21_005:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_set FLAG_HT_IRRIGATION_RESTORED, _HT_GymSignOpen
	npc_msg 10
	wait_button
	closemsg
	releaseall
	end

_HT_GymSignOpen:
	npc_msg 11
	wait_button
	closemsg
	releaseall
	end

scr_seq_T21_006:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 7
	wait_button
	closemsg
	releaseall
	end

scr_seq_T21_007:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 9
	wait_button
	closemsg
	releaseall
	end

scr_seq_T21_008:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 12
	wait_button
	closemsg
	releaseall
	end

// script de carga do header (on-transition): nada a fazer
scr_seq_T21_010:
	end

scr_seq_T21_011:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 16
	wait_button
	closemsg
	releaseall
	end

scr_seq_T21_012:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 17
	wait_button
	closemsg
	releaseall
	end

scr_seq_T21_013:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 18
	wait_button
	closemsg
	releaseall
	end


	.balign 4
_HT_Notice:
	step MOVEMENT_EMOTE_EXCLAMATION, 1
	step_end
	.balign 4
_HT_StepDown:
	step MOVEMENT_STEP_DOWN, 1
	step_end
	.balign 4
