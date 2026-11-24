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

.include "data/scr_seq/include/event_T26.inc"


.include "data/scr_seq/include/hollowtide_flags.inc"
// text archive to grab from: 604.txt
// Hollowtide: Breezeport City (Olivine do HGSS). Reescrito a partir do GBA (Palm080/090/091/092/093): a artista e o
// festival (3 lampioes: casas do oeste, praca, cais), o Teatro (ginasio da Jay, porta do ginasio) fechado ate as
// luzes, a saida norte (Route 3) fechada ate vencer a Jay, NPCs e placas. Farol vira a casa do faroleiro (fechada);
// o porto (S.S. Aqua) fecha. VAR_UNK_4078: 0 lampioes apagados | 1 Teatro aberto | 2 Jay vencida.

.data

scrdef scr_seq_T26_000
scrdef scr_seq_T26_001
scrdef scr_seq_T26_002
scrdef scr_seq_T26_003
scrdef scr_seq_T26_004
scrdef scr_seq_T26_005
scrdef scr_seq_T26_006
scrdef scr_seq_T26_007
scrdef scr_seq_T26_008
scrdef scr_seq_T26_009
scrdef scr_seq_T26_010
scrdef scr_seq_T26_011
scrdef scr_seq_T26_012
scrdef scr_seq_T26_013
scrdef scr_seq_T26_014
scrdef scr_seq_T26_015
scrdef scr_seq_T26_016
scrdef scr_seq_T26_017
scrdef scr_seq_T26_018
scrdef scr_seq_T26_019
scrdef scr_seq_T26_020
scrdef scr_seq_T26_021
scrdef scr_seq_T26_022
scrdef scr_seq_T26_023
scrdef_end

// artista (anfitria do festival)
scr_seq_T26_000:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_HT_BREEZEPORT_LIGHTS, _HT_ArtistDone
	setflag FLAG_HT_BREEZEPORT_STARTED
	npc_msg 0
	wait_button
	closemsg
	releaseall
	end

_HT_ArtistDone:
	npc_msg 1
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_001:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 2
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_004:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 3
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_005:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 4
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_006:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 5
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_007:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 6
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_008:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 7
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_009:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 8
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_010:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 9
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_011:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 10
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_013:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 11
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_014:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 12
	wait_button
	closemsg
	releaseall
	end

// placa do Teatro
scr_seq_T26_015:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_set FLAG_HT_BREEZEPORT_LIGHTS, _HT_ArtistDone
	npc_msg 13
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_016:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 14
	wait_button
	closemsg
	releaseall
	end

// placa da trilha (Route 3)
scr_seq_T26_017:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_set FLAG_HT_DEFEATED_JAY, _HT_EastOpen
	npc_msg 15
	wait_button
	closemsg
	releaseall
	end

_HT_EastOpen:
	npc_msg 16
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_018:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 19
	wait_button
	closemsg
	releaseall
	end

scr_seq_T26_019:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_unset FLAG_HT_BREEZEPORT_STARTED, _HT_NeedArtist
	goto_if_set FLAG_HT_BREEZEPORT_LAMP1, _HT_LampGlowing
	setflag FLAG_HT_BREEZEPORT_LAMP1
	goto _HT_LampCheck

scr_seq_T26_020:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_unset FLAG_HT_BREEZEPORT_STARTED, _HT_NeedArtist
	goto_if_set FLAG_HT_BREEZEPORT_LAMP2, _HT_LampGlowing
	setflag FLAG_HT_BREEZEPORT_LAMP2
	goto _HT_LampCheck

scr_seq_T26_021:
	play_se SEQ_SE_DP_SELECT
	lockall
	goto_if_unset FLAG_HT_BREEZEPORT_STARTED, _HT_NeedArtist
	goto_if_set FLAG_HT_BREEZEPORT_LAMP3, _HT_LampGlowing
	setflag FLAG_HT_BREEZEPORT_LAMP3
	goto _HT_LampCheck

_HT_LampCheck:
	goto_if_unset FLAG_HT_BREEZEPORT_LAMP1, _HT_LampGlowing
	goto_if_unset FLAG_HT_BREEZEPORT_LAMP2, _HT_LampGlowing
	goto_if_unset FLAG_HT_BREEZEPORT_LAMP3, _HT_LampGlowing
	setflag FLAG_HT_BREEZEPORT_LIGHTS
	setvar VAR_UNK_4078, 1
	npc_msg 18
	wait_button
	closemsg
	releaseall
	end

_HT_LampGlowing:
	npc_msg 17
	wait_button
	closemsg
	releaseall
	end

_HT_NeedArtist:
	npc_msg 13
	wait_button
	closemsg
	releaseall
	end

// porta do Teatro: fechada ate as luzes
scr_seq_T26_022:
	lockall
	goto_if_set FLAG_HT_BREEZEPORT_LIGHTS, _HT_TheaterOpen
	npc_msg 13
	wait_button
	closemsg
	apply_movement obj_player, _HT_StepDown
	wait_movement
	releaseall
	end

_HT_TheaterOpen:
	setvar VAR_UNK_4078, 1
	releaseall
	end

// saida norte (Route 3): fechada ate vencer a Jay
scr_seq_T26_023:
	lockall
	goto_if_set FLAG_HT_DEFEATED_JAY, _HT_NorthOpen
	npc_msg 15
	wait_button
	closemsg
	apply_movement obj_player, _HT_StepDown
	wait_movement
	releaseall
	end

_HT_NorthOpen:
	setvar VAR_UNK_4078, 2
	releaseall
	end

// gatilhos de quadro e carga do HGSS (rival, Jasmine): nada
scr_seq_T26_002:
scr_seq_T26_003:
scr_seq_T26_012:
	end

	.balign 4
_HT_StepDown:
	step MOVEMENT_STEP_DOWN, 1
	step_end
	.balign 4
