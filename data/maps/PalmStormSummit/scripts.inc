PalmStormSummit_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Palm240_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Palm240_OnFrame
	.byte 0

Palm240_OnTransition:
	call_if_lt VAR_HT_EPILOGUE, 2, Palm240_HideDoge
	call_if_ge VAR_HT_EPILOGUE, 2, Palm240_DogeHere
	call_if_ge VAR_HT_EPILOGUE, 2, Palm24x_Sunny
	end

Palm240_HideDoge::
	setflag FLAG_HT_HIDE_SUMMIT_DOGE
	return

Palm240_DogeHere::
	clearflag FLAG_HT_HIDE_SUMMIT_DOGE
	setobjectxyperm LOCALID_SUMMIT_DOGE, 12, 7
	setobjectmovementtype LOCALID_SUMMIT_DOGE, MOVEMENT_TYPE_FACE_DOWN
	return

Palm24x_Sunny::
	setweather WEATHER_SUNNY
	return

Palm240_OnFrame:
	map_script_2 VAR_HT_EPILOGUE, 2, Palm240_Ending
	.2byte 0

Palm240_Scene::
	goto_if_set FLAG_HT_SUMMIT_DONE, Palm240_End
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Palm240_TextIntro, MSGBOX_DEFAULT
	playmoncry SPECIES_KYOGRE, CRY_MODE_NORMAL
	waitmoncry
	msgbox Palm240_TextBattle, MSGBOX_DEFAULT
	playbgm MUS_VS_KYOGRE_GROUDON, FALSE
	trainerbattle_no_intro TRAINER_MAXIE_MOSSDEEP, Palm240_TextDefeat
	setflag FLAG_HT_SUMMIT_DONE
	msgbox Palm240_TextMedallion, MSGBOX_DEFAULT
	msgbox Palm240_TextTavinho1, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HT_HIDE_SUMMIT_DOGE
	addobject LOCALID_SUMMIT_DOGE
	applymovement LOCALID_SUMMIT_DOGE, Palm240_DogeArrives
	waitmovement 0
	msgbox Palm240_TextDoge1, MSGBOX_DEFAULT
	msgbox Palm240_TextTavinho2, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	msgbox Palm240_TextHandOver, MSGBOX_DEFAULT
	closemessage
	setvar VAR_HT_EPILOGUE, 1
	warpsilent MAP_PALM_MARINE_EPILOGUE, 12, 26
	waitstate
	releaseall
	end

Palm240_DogeArrives:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_up
	walk_in_place_faster_up
	step_end

Palm240_Ending::
	lockall
	setvar VAR_HT_EPILOGUE, 3
	delay 30
	msgbox Palm240_TextReturn, MSGBOX_DEFAULT
	msgbox Palm240_TextDoge2, MSGBOX_DEFAULT
	closemessage
	delay 30
	fadescreen FADE_TO_BLACK
	msgbox Palm240_TextFinal, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_FROM_BLACK
	delay 30
	call Palm240_GiveKeyStone
	releaseall
	end

Palm240_GiveKeyStone::
	goto_if_set FLAG_HT_RECEIVED_KEY_STONE, Palm240_Ret
	msgbox Palm240_TextKeyStone, MSGBOX_DEFAULT
	giveitem ITEM_MEGA_RING
	setflag FLAG_HT_RECEIVED_KEY_STONE
	msgbox Palm240_TextKeyStoneHint, MSGBOX_DEFAULT
	closemessage
	return

Palm240_Ret::
	return

Palm240_Tavinho::
	lock
	faceplayer
	goto_if_set FLAG_HT_SUMMIT_DONE, Palm240_TavinhoAfter
	release
	end

Palm240_TavinhoAfter::
	msgbox Palm240_TextTavinhoAfter, MSGBOX_DEFAULT
	release
	end

Palm240_Doge::
	lock
	faceplayer
	goto_if_unset FLAG_HT_RECEIVED_KEY_STONE, Palm240_DogeKeyStone
	msgbox Palm240_TextDogeAfter, MSGBOX_DEFAULT
	release
	end

Palm240_DogeKeyStone::
	call Palm240_GiveKeyStone
	release
	end

Palm240_End::
	end

Palm240_TextIntro:
	.string "???: …So the LEAGUE sent someone else.\p"
	.string "TAVINHO: I'm TAVINHO. I used to be\n"
	.string "the CHAMPION.\p"
	.string "I caught KYOGRE. I stopped those\n"
	.string "people from using it.\p"
	.string "I thought I could master the orb.\p"
	.string "There was always something that\n"
	.string "needed protecting. I just had to be\l"
	.string "stronger.$"
Palm240_TextBattle:
	.string "TAVINHO: If I can't protect everyone…\n"
	.string "who will?\p"
	.string "Turn back… or show me you can carry\n"
	.string "this weight better than I can!$"
Palm240_TextDefeat:
	.string "…The rain is stopping.$"
Palm240_TextMedallion:
	.string "{PLAYER}'s ATLAS MEDALLION slipped out\n"
	.string "and caught the last light of the storm.\p"
	.string "TAVINHO: That dog… ATLAS.\p"
	.string "The one who walks beside anyone who\n"
	.string "needs company on the road.\p"
	.string "Your mom gave you that, didn't she?\n"
	.string "So you'd never walk alone.$"
Palm240_TextTavinho1:
	.string "TAVINHO: I spent so long trying to be\n"
	.string "strong for everyone…\p"
	.string "that I forgot I could need someone\n"
	.string "too.$"
Palm240_TextDoge1:
	.string "DOGE: TAVINHO!\p"
	.string "You were always there when we needed\n"
	.string "you. Now it's our turn.$"
Palm240_TextTavinho2:
	.string "TAVINHO: DOGE…\p"
	.string "No one has to carry the world\n"
	.string "alone… I used to say that myself.$"
Palm240_TextHandOver:
	.string "TAVINHO handed KYOGRE's POKé BALL and\n"
	.string "the BLUE ORB to DOGE.\p"
	.string "DOGE climbed onto his MEGA LATIOS\n"
	.string "and flew south, toward HOENN…$"
Palm240_TextReturn:
	.string "Hours later, DOGE came back to the\n"
	.string "summit.\p"
	.string "The storm was gone.$"
Palm240_TextDoge2:
	.string "DOGE: KYOGRE is resting in the MARINE\n"
	.string "CAVE, sealed with the orb.\p"
	.string "And you, TAVINHO… next time, try\n"
	.string "talking to us before catching a\l"
	.string "legendary that can destroy the world.\p"
	.string "HAHAHA!$"
Palm240_TextFinal:
	.string "No one has to carry the world alone.$"
Palm240_TextTavinhoAfter:
	.string "TAVINHO: Thank you, {PLAYER}.\p"
	.string "I'll come down from the mountain\n"
	.string "soon. I have a lot of people to\l"
	.string "apologize to.$"
Palm240_TextDogeAfter:
	.string "DOGE: A friendly rematch someday?\n"
	.string "You, me and TAVINHO.\p"
	.string "Just not in a storm. HAHAHA!$"
Palm240_TextKeyStone:
	.string "DOGE: Oh, one more thing, {PLAYER}.\p"
	.string "Take this. It's a MEGA RING, with a\n"
	.string "KEY STONE set in it.\p"
	.string "You saw what PKAS's CHARIZARD and my\n"
	.string "LATIOS can do. A CHAMPION should have\l"
	.string "one too.$"
Palm240_TextKeyStoneHint:
	.string "DOGE: A KEY STONE needs a MEGA STONE\n"
	.string "held by the right POKéMON.\p"
	.string "The strongest POKéMON of this mountain\n"
	.string "live in the cave beside the summit.\l"
	.string "They say a few stones are hidden in\l"
	.string "there… if you can handle the climb.$"

Palm242_HollowWind::
	goto_if_set FLAG_HT_SUMMIT_DONE, Palm240_End
	lockall
	msgbox Palm242_TextWind, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, Palm242_StepBack
	waitmovement 0
	releaseall
	end

Palm242_StepBack:
	walk_down
	step_end

Palm242_TextWind:
	.string "A fierce wind howls out of the cave.\p"
	.string "It's impossible to go in while the\n"
	.string "storm is raging.$"
