PalmPillarton_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm131_Load
	.byte 0

Palm131_Load::
	call_if_set FLAG_HT_PILLARTON_VALVE_1, Palm131_DrawValve1
	call_if_set FLAG_HT_PILLARTON_VALVE_2, Palm131_DrawValve2
	call_if_set FLAG_HT_PILLARTON_VALVE_3, Palm131_DrawValve3
	call_if_unset FLAG_HT_PILLARTON_WATER, Palm131_LockGym
	end

Palm131_LockGym::
	setmetatile 43, 18, 722, TRUE
	return

Palm131_UnlockGym::
	setmetatile 43, 18, 461, TRUE
	special DrawWholeMapView
	return

Palm131_DrawValve1::
	setmetatile 16, 6, 866, TRUE
	return

Palm131_Valve1::
	lockall
	goto_if_set FLAG_HT_PILLARTON_VALVE_1, Palm131_ValveIsOpen
	msgbox Palm131_TextValveTurn, MSGBOX_DEFAULT
	setflag FLAG_HT_PILLARTON_VALVE_1
	call Palm131_DrawValve1
	special DrawWholeMapView
	playse SE_UNLOCK
	goto Palm131_ValveCount

Palm131_DrawValve2::
	setmetatile 26, 6, 866, TRUE
	return

Palm131_Valve2::
	lockall
	goto_if_set FLAG_HT_PILLARTON_VALVE_2, Palm131_ValveIsOpen
	msgbox Palm131_TextValveTurn, MSGBOX_DEFAULT
	setflag FLAG_HT_PILLARTON_VALVE_2
	call Palm131_DrawValve2
	special DrawWholeMapView
	playse SE_UNLOCK
	goto Palm131_ValveCount

Palm131_DrawValve3::
	setmetatile 36, 6, 866, TRUE
	return

Palm131_Valve3::
	lockall
	goto_if_set FLAG_HT_PILLARTON_VALVE_3, Palm131_ValveIsOpen
	msgbox Palm131_TextValveTurn, MSGBOX_DEFAULT
	setflag FLAG_HT_PILLARTON_VALVE_3
	call Palm131_DrawValve3
	special DrawWholeMapView
	playse SE_UNLOCK
	goto Palm131_ValveCount

Palm131_ValveIsOpen::
	msgbox Palm131_TextValveOpen, MSGBOX_DEFAULT
	releaseall
	end

Palm131_ValveCount::
	goto_if_unset FLAG_HT_PILLARTON_VALVE_1, Palm131_ValveMore
	goto_if_unset FLAG_HT_PILLARTON_VALVE_2, Palm131_ValveMore
	goto_if_unset FLAG_HT_PILLARTON_VALVE_3, Palm131_ValveMore
	msgbox Palm131_TextValvesAll, MSGBOX_DEFAULT
	releaseall
	end

Palm131_ValveMore::
	msgbox Palm131_TextValveMore, MSGBOX_DEFAULT
	releaseall
	end

Palm131_Lela::
	lock
	faceplayer
	goto_if_unset FLAG_HT_PILLARTON_VALVE_1, Palm131_LelaTaunt
	goto_if_unset FLAG_HT_PILLARTON_VALVE_2, Palm131_LelaTaunt
	goto_if_unset FLAG_HT_PILLARTON_VALVE_3, Palm131_LelaTaunt
	trainerbattle_single TRAINER_PALM_LELA, Palm131_TextLelaIntro, Palm131_TextLelaDefeat, Palm131_LelaDefeated
	release
	end

Palm131_LelaTaunt::
	msgbox Palm131_TextLelaTaunt, MSGBOX_DEFAULT
	release
	end

Palm131_LelaDefeated::
	msgbox Palm131_TextLelaAfter, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	setflag FLAG_HT_PILLARTON_WATER
	removeobject 2
	removeobject 1
	call Palm131_UnlockGym
	fadescreen FADE_FROM_BLACK
	msgbox Palm131_TextWaterBack, MSGBOX_DEFAULT
	release
	end

Palm131_DamGrunt1::
	trainerbattle_single TRAINER_PALM_DAM_GRUNT_1, Palm131_TextDamGrunt1Intro, Palm131_TextDamGrunt1Defeat
	msgbox Palm131_TextDamGrunt1After, MSGBOX_AUTOCLOSE
	end

Palm131_DamGrunt2::
	trainerbattle_single TRAINER_PALM_DAM_GRUNT_2, Palm131_TextDamGrunt2Intro, Palm131_TextDamGrunt2Defeat
	msgbox Palm131_TextDamGrunt2After, MSGBOX_AUTOCLOSE
	end

Palm130_Tchum::
	goto_if_set FLAG_HT_PILLARTON_WATER, Palm130_TchumAfter
	msgbox Palm130_Tchum_Text, MSGBOX_NPC
	end

Palm130_TchumAfter::
	msgbox Palm130_TchumAfter_Text, MSGBOX_NPC
	end

Palm130_OldCanal::
	msgbox Palm130_OldCanal_Text, MSGBOX_NPC
	end

Palm130_GardenLady::
	msgbox Palm130_GardenLady_Text, MSGBOX_NPC
	end

Palm130_Kid::
	msgbox Palm130_Kid_Text, MSGBOX_NPC
	end

Palm130_GymFan::
	msgbox Palm130_GymFan_Text, MSGBOX_NPC
	end

Palm130_CitySign::
	msgbox Palm130_CitySign_Text, MSGBOX_SIGN
	end

Palm130_GymSign::
	msgbox Palm130_GymSign_Text, MSGBOX_SIGN
	end

Palm130_PlantSign::
	msgbox Palm130_PlantSign_Text, MSGBOX_SIGN
	end

Palm130_DamSign::
	msgbox Palm130_DamSign_Text, MSGBOX_SIGN
	end


Palm130_Tchum_Text:
	.string "Welcome to PILLARTON! Everyone here\n"
	.string "stands on a solid foundation.\p"
	.string "Get it? FOUNDATION? Ground? Ha!\n"
	.string "...Nobody laughs anymore.\p"
	.string "Seriously, though: the water is\n"
	.string "vanishing. Half the city is stalled.\p"
	.string "NEVARD told me about a trainer who\n"
	.string "helped his fields. Was that you?\p"
	.string "TEAM PALM built a power plant on\n"
	.string "the dam. Go see for yourself.$"

Palm130_TchumAfter_Text:
	.string "You opened the valves and beat\n"
	.string "LELA? You really rock!\p"
	.string "...Rock. Ground. Never mind.\n"
	.string "My GYM opens soon. Be ready!$"

Palm130_OldCanal_Text:
	.string "That dry ditch was a canal once.\n"
	.string "Boats used to sail right here.\p"
	.string "Now you can see the bare rock.$"

Palm130_GardenLady_Text:
	.string "TEAM PALM planted these “contract\n"
	.string "gardens.” Lovely flowers...\p"
	.string "...watered with OUR water, while\n"
	.string "the city goes dry.$"

Palm130_Kid_Text:
	.string "The fountain at school stopped\n"
	.string "working. Can you fix the river?$"

Palm130_GymFan_Text:
	.string "TCHUM is a therapist and a GYM\n"
	.string "LEADER. He says GROUND-types teach\p"
	.string "you to stay grounded. Then he\n"
	.string "laughs at his own joke.$"

Palm130_CitySign_Text:
	.string "PILLARTON CITY\n"
	.string "“The city of pillars and dams.”$"

Palm130_GymSign_Text:
	.string "PILLARTON CITY POKéMON GYM\n"
	.string "LEADER: TCHUM\p"
	.string "“Keep your feet on the ground!”$"

Palm130_PlantSign_Text:
	.string "TEAM PALM POWER PLANT\n"
	.string "“Water into energy, energy into\l"
	.string "coins, coins into prosperity.”$"

Palm130_DamSign_Text:
	.string "PILLARTON DAM\n"
	.string "Service walkway. Watch your step.$"

Palm131_TextValveTurn:
	.string "It's a big valve wheel.\n"
	.string "{PLAYER} turned it with all their might!$"

Palm131_TextValveOpen:
	.string "The valve is already open. You can\n"
	.string "hear water rushing below.$"

Palm131_TextValveMore:
	.string "Water trickles through the dam.\n"
	.string "There must be more valves.$"

Palm131_TextValvesAll:
	.string "All three valves are open!\n"
	.string "The river roars back to life!$"

Palm131_TextLelaTaunt:
	.string "I'm LELA, TEAM PALM ADMIN.\n"
	.string "Contracts and operations.\p"
	.string "Those valves are company property,\n"
	.string "child. Run along.$"

Palm131_TextLelaIntro:
	.string "You're confusing scarcity with\n"
	.string "opportunity.\p"
	.string "Our technology turns water into\n"
	.string "energy, energy into coins, and\l"
	.string "coins into prosperity!$"

Palm131_TextLelaDefeat:
	.string "...You forgot to turn prosperity\n"
	.string "into drinking water, I suppose.$"

Palm131_TextLelaAfter:
	.string "You think you won because you\n"
	.string "opened three valves?\p"
	.string "This isn't the first obstacle we've\n"
	.string "faced. Nor will it be the last.$"

Palm131_TextWaterBack:
	.string "LELA and her crew left the dam.\n"
	.string "Water flows freely to the city!\p"
	.string "TCHUM headed back to his GYM.$"

Palm131_TextDamGrunt1Intro:
	.string "The dam is closed to the public!\n"
	.string "Especially to nosy kids!$"

Palm131_TextDamGrunt1Defeat:
	.string "Ugh, the admin's gonna yell at me.$"

Palm131_TextDamGrunt1After:
	.string "The plant needs every drop for the\n"
	.string "machines. People can wait!$"

Palm131_TextDamGrunt2Intro:
	.string "One step closer to those valves and\n"
	.string "you'll regret it!$"

Palm131_TextDamGrunt2Defeat:
	.string "I regret it. Happy?$"

Palm131_TextDamGrunt2After:
	.string "Admin LELA is at the plant. She'll\n"
	.string "put you in your place!$"

Palm142_EastGate::
	goto_if_set FLAG_BADGE04_GET, Palm142_EastGateOk
	lockall
	msgbox Palm142_TextEastGate, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm142_StepBackWest
	waitmovement 0
	releaseall
	end

Palm142_EastGateOk::
	end

Palm142_StepBackWest:
	walk_left
	step_end


Palm142_TextEastGate:
	.string "EAST: ROUTE 6 - SERENIA\p"
	.string "The garden path is closed until the\n"
	.string "city's GYM LEADER gives the word.$"