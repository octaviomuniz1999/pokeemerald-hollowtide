PalmMarineEpilogue_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Palm241_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Palm241_OnFrame
	.byte 0

Palm241_OnTransition:
	setflag FLAG_HIDE_MAP_NAME_POPUP
	end

Palm241_OnFrame:
	map_script_2 VAR_HT_EPILOGUE, 1, Palm241_Scene
	.2byte 0

Palm241_Scene::
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Palm241_Hide
	waitmovement 0
	msgbox Palm241_TextHoenn, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_EPILOGUE_DOGE, Palm241_DogeWalk
	waitmovement 0
	playmoncry SPECIES_KYOGRE, CRY_MODE_NORMAL
	waitmoncry
	msgbox Palm241_TextDoge, MSGBOX_DEFAULT
	closemessage
	playse SE_ORB
	fadescreen FADE_TO_WHITE
	removeobject LOCALID_EPILOGUE_KYOGRE
	fadescreen FADE_FROM_WHITE
	msgbox Palm241_TextSealed, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HIDE_MAP_NAME_POPUP
	setvar VAR_HT_EPILOGUE, 2
	fadescreen FADE_TO_BLACK
	warpsilent MAP_PALM_STORM_SUMMIT, 11, 8
	waitstate
	releaseall
	end

Palm241_Hide:
	set_invisible
	step_end

Palm241_DogeWalk:
	walk_up
	walk_in_place_faster_up
	step_end

Palm241_TextHoenn:
	.string "MARINE CAVE, HOENN.$"
Palm241_TextDoge:
	.string "DOGE: Rest, big guy.\p"
	.string "We'll take care of the rest.$"
Palm241_TextSealed:
	.string "KYOGRE returned to the depths of the\n"
	.string "MARINE CAVE, sealed with the BLUE ORB.$"
