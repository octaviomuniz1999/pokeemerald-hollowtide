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

.include "data/scr_seq/include/event_T20.inc"


// text archive to grab from: 542.txt
// Hollowtide: Dawnmere Village (exterior de New Bark). Reescrito a partir do GBA (Palm040_*): NPCs, placas e a
// saida para a Route 1 travada sem Pokemon. As cenas do HGSS (Lyra e Marill, Elm, Silver) sairam.
// Os numeros dos scripts seguem os do HGSS (header 0615 e zone_event 057 apontam para eles).

.data

scrdef scr_seq_T20_000
scrdef scr_seq_T20_001
scrdef scr_seq_T20_002
scrdef scr_seq_T20_003
scrdef scr_seq_T20_004
scrdef scr_seq_T20_005
scrdef scr_seq_T20_006
scrdef scr_seq_T20_007
scrdef scr_seq_T20_008
scrdef scr_seq_T20_009
scrdef scr_seq_T20_010
scrdef scr_seq_T20_011
scrdef scr_seq_T20_012
scrdef scr_seq_T20_013
scrdef scr_seq_T20_014
scrdef scr_seq_T20_015
scrdef scr_seq_T20_016
scrdef scr_seq_T20_017
scrdef scr_seq_T20_018
scrdef_end

scr_seq_T20_015:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 0
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20_001:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 1
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20_017:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	buffer_players_name 0
	npc_msg 2
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20_013:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 3
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20_007:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 4
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20_016:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 5
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20_014:
	play_se SEQ_SE_DP_SELECT
	lockall
	buffer_players_name 0
	npc_msg 6
	wait_button
	closemsg
	releaseall
	end

// placa da Route 1 na saida oeste (nova; CP-DS-01: modelo e colisao em land.json, placa em 0621)
scr_seq_T20_018:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 8
	wait_button
	closemsg
	releaseall
	end

// saida oeste (Route 1): sem Pokemon, volta um passo (GBA Palm040_ExitEast)
scr_seq_T20_002:
	lockall
	goto_if_set FLAG_GOT_STARTER, _HT_ExitOk
	npc_msg 7
	wait_button
	closemsg
	apply_movement obj_player, _HT_StepBack
	wait_movement
	releaseall
	end

_HT_ExitOk:
	setvar VAR_SCENE_NEW_BARK_WEST_EXIT, 1
	releaseall
	end

// gatilhos de quadro do header: mudam a variavel para nao repetir a cada quadro
scr_seq_T20_003:
	setvar VAR_SCENE_PLAYERS_HOUSE_1F, 2
	end

scr_seq_T20_008:
	setvar VAR_SCENE_NEW_BARK_TOWN_OW, 2
	end

// cenas e scripts de carga do HGSS: fora
scr_seq_T20_000:
scr_seq_T20_004:
scr_seq_T20_005:
scr_seq_T20_006:
scr_seq_T20_009:
scr_seq_T20_010:
scr_seq_T20_011:
scr_seq_T20_012:
	end

	.balign 4
_HT_StepBack:
	step MOVEMENT_STEP_RIGHT, 1
	step_end
	.balign 4
