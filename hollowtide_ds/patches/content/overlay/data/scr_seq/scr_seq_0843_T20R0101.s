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

.include "data/scr_seq/include/event_T20R0101.inc"


// text archive to grab from: 543.txt
// Hollowtide: laboratorio do Prof. Alex (Dawnmere). Reescrito a partir do GBA (Palm040_Alex, Palm040_Aide):
// tudo acontece ao falar com o professor (ou na maquina das Poke Balls); as cenas do Elm do HGSS sairam.
// Os numeros dos scripts seguem os do HGSS porque o header do mapa e os eventos (zone_event 058) apontam para eles.

.data

scrdef scr_seq_T20R0101_000
scrdef scr_seq_T20R0101_001
scrdef scr_seq_T20R0101_002
scrdef scr_seq_T20R0101_003
scrdef scr_seq_T20R0101_004
scrdef scr_seq_T20R0101_005
scrdef scr_seq_T20R0101_006
scrdef scr_seq_T20R0101_007
scrdef scr_seq_T20R0101_008
scrdef scr_seq_T20R0101_009
scrdef scr_seq_T20R0101_010
scrdef scr_seq_T20R0101_011
scrdef scr_seq_T20R0101_012
scrdef scr_seq_T20R0101_013
scrdef scr_seq_T20R0101_014
scrdef scr_seq_T20R0101_015
scrdef_end

// Prof. Alex
scr_seq_T20R0101_000:
scr_seq_T20R0101_012:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	goto_if_set FLAG_GOT_STARTER, _HT_AlexDone
	buffer_players_name 0
	npc_msg 0
	closemsg
	choose_starter
	setflag FLAG_GOT_STARTER
	scrcmd_605 3, 2
	toggle_following_pokemon_movement 0
	scrcmd_608
	wait 10, VAR_SPECIAL_RESULT
	toggle_following_pokemon_movement 1
	get_partymon_species 0, VAR_TEMP_x4001
	set_starter_choice VAR_TEMP_x4001
	buffer_players_name 0
	npc_msg 1
	setflag FLAG_GOT_POKEDEX
	play_fanfare SEQ_ME_POKEGET
	npc_msg 2
	wait_fanfare
	closemsg
	setvar VAR_SPECIAL_x8004, ITEM_POKE_BALL
	setvar VAR_SPECIAL_x8005, 5
	callstd std_obtain_item_verbose
	setvar VAR_SPECIAL_x8004, ITEM_POTION
	setvar VAR_SPECIAL_x8005, 2
	callstd std_obtain_item_verbose
	setvar VAR_SCENE_ELMS_LAB, 1
	setvar VAR_SCENE_NEW_BARK_TOWN_OW, 1
_HT_AlexDone:
	npc_msg 3
	wait_button
	closemsg
	releaseall
	end

// assistente
scr_seq_T20R0101_001:
	play_se SEQ_SE_DP_SELECT
	lockall
	faceplayer
	npc_msg 4
	wait_button
	closemsg
	releaseall
	end

// estantes e computador (textos do HGSS)
scr_seq_T20R0101_005:
	buffer_players_name 0
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 93
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20R0101_006:
	buffer_players_name 0
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 94
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20R0101_007:
	buffer_players_name 0
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 95
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20R0101_008:
	buffer_players_name 0
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 96
	wait_button
	closemsg
	releaseall
	end

scr_seq_T20R0101_009:
	play_se SEQ_SE_DP_SELECT
	lockall
	npc_msg 97
	wait_button
	closemsg
	releaseall
	end

// cenas do HGSS (entrada, chamadas, assistente com o ovo...): fora
scr_seq_T20R0101_002:
scr_seq_T20R0101_003:
scr_seq_T20R0101_004:
scr_seq_T20R0101_010:
scr_seq_T20R0101_011:
scr_seq_T20R0101_013:
scr_seq_T20R0101_014:
scr_seq_T20R0101_015:
	end
	.balign 4
