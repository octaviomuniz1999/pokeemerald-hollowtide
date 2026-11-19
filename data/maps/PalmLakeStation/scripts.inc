PalmLakeStation_MapScripts::
	.byte 0

Palm172_Chelsia::
	lock
	faceplayer
	goto_if_set FLAG_HT_HORIZON_DONE, Palm172_ChelsiaDone
	msgbox Palm172_TextChelsia, MSGBOX_DEFAULT
	release
	end

Palm172_ChelsiaDone::
	msgbox Palm172_TextChelsiaDone, MSGBOX_DEFAULT
	release
	end

Palm172_Piplup::
	lock
	faceplayer
	playmoncry SPECIES_PIPLUP, CRY_MODE_NORMAL
	msgbox Palm170_TextPiplup, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Palm172_Grunt1::
	trainerbattle_single TRAINER_PALM_STATION_GRUNT_1, Palm172_TextGrunt1Intro, Palm172_TextGrunt1Loss
	msgbox Palm172_TextGrunt1After, MSGBOX_AUTOCLOSE
	end

Palm172_Grunt2::
	trainerbattle_single TRAINER_PALM_STATION_GRUNT_2, Palm172_TextGrunt2Intro, Palm172_TextGrunt2Loss
	msgbox Palm172_TextGrunt2After, MSGBOX_AUTOCLOSE
	end

Palm172_Grunt3::
	trainerbattle_single TRAINER_PALM_STATION_GRUNT_3, Palm172_TextGrunt3Intro, Palm172_TextGrunt3Loss
	msgbox Palm172_TextGrunt3After, MSGBOX_AUTOCLOSE
	end

Palm172_Amp1::
	lockall
	goto_if_set FLAG_HT_HORIZON_AMP_1, Palm172_AmpOff
	msgbox Palm172_TextAmp, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm172_Release
	setflag FLAG_HT_HORIZON_AMP_1
	playse SE_PC_OFF
	waitse
	msgbox Palm172_TextAmpDown, MSGBOX_DEFAULT
	releaseall
	end

Palm172_Amp2::
	lockall
	goto_if_set FLAG_HT_HORIZON_AMP_2, Palm172_AmpOff
	msgbox Palm172_TextAmp, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm172_Release
	setflag FLAG_HT_HORIZON_AMP_2
	playse SE_PC_OFF
	waitse
	msgbox Palm172_TextAmpDown, MSGBOX_DEFAULT
	releaseall
	end

Palm172_Amp3::
	lockall
	goto_if_set FLAG_HT_HORIZON_AMP_3, Palm172_AmpOff
	msgbox Palm172_TextAmp, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm172_Release
	setflag FLAG_HT_HORIZON_AMP_3
	playse SE_PC_OFF
	waitse
	msgbox Palm172_TextAmpDown, MSGBOX_DEFAULT
	releaseall
	end

Palm172_AmpOff::
	msgbox Palm172_TextAmpIsOff, MSGBOX_DEFAULT
	releaseall
	end

Palm172_Release::
	releaseall
	end

Palm172_FreeMARILL::
	lockall
	playmoncry SPECIES_MARILL, CRY_MODE_NORMAL
	msgbox Palm172_TextNetMARILL, MSGBOX_DEFAULT
	waitmoncry
	setflag FLAG_HT_HORIZON_PKMN_1
	playse SE_BALL_OPEN
	removeobject 6
	msgbox Palm172_TextFreedMARILL, MSGBOX_DEFAULT
	releaseall
	end

Palm172_FreePSYDUCK::
	lockall
	playmoncry SPECIES_PSYDUCK, CRY_MODE_NORMAL
	msgbox Palm172_TextNetPSYDUCK, MSGBOX_DEFAULT
	waitmoncry
	setflag FLAG_HT_HORIZON_PKMN_2
	playse SE_BALL_OPEN
	removeobject 7
	msgbox Palm172_TextFreedPSYDUCK, MSGBOX_DEFAULT
	releaseall
	end

Palm172_FreeLOTAD::
	lockall
	playmoncry SPECIES_LOTAD, CRY_MODE_NORMAL
	msgbox Palm172_TextNetLOTAD, MSGBOX_DEFAULT
	waitmoncry
	setflag FLAG_HT_HORIZON_PKMN_3
	playse SE_BALL_OPEN
	removeobject 8
	msgbox Palm172_TextFreedLOTAD, MSGBOX_DEFAULT
	releaseall
	end

Palm172_Terminal::
	lockall
	goto_if_set FLAG_HT_HORIZON_DONE, Palm172_TerminalDone
	goto_if_unset FLAG_HT_HORIZON_AMP_1, Palm172_TerminalBusy
	goto_if_unset FLAG_HT_HORIZON_AMP_2, Palm172_TerminalBusy
	goto_if_unset FLAG_HT_HORIZON_AMP_3, Palm172_TerminalBusy
	goto_if_unset FLAG_HT_HORIZON_PKMN_1, Palm172_TerminalBusy
	goto_if_unset FLAG_HT_HORIZON_PKMN_2, Palm172_TerminalBusy
	goto_if_unset FLAG_HT_HORIZON_PKMN_3, Palm172_TerminalBusy
	msgbox Palm172_TextTerminal, MSGBOX_DEFAULT
	playse SE_PC_LOGIN
	waitse
	msgbox Palm172_TextRecord, MSGBOX_DEFAULT
	setflag FLAG_HT_HORIZON_DONE
	applymovement 1, Common_Movement_FacePlayer
	waitmovement 0
	msgbox Palm172_TextChelsiaRecord, MSGBOX_DEFAULT
	releaseall
	end

Palm172_TerminalBusy::
	msgbox Palm172_TextTerminalBusy, MSGBOX_DEFAULT
	releaseall
	end

Palm172_TerminalDone::
	msgbox Palm172_TextRecord, MSGBOX_DEFAULT
	releaseall
	end


Palm172_TextChelsia:
	.string "CHELSIA: The hum is coming from those\n"
	.string "big tanks. Amplifiers? Here?\p"
	.string "And there are POKéMON caught in nets\n"
	.string "over there!\p"
	.string "Please shut down the machines and\n"
	.string "free the POKéMON. I'll watch the exit.$"

Palm172_TextChelsiaDone:
	.string "CHELSIA: The lake is breathing again.\n"
	.string "Thank you, {PLAYER}.\p"
	.string "Even when everything seems confusing,\n"
	.string "a little light helps you find the way.\p"
	.string "I'll be waiting at my GYM.\n"
	.string "Come and see me there!$"

Palm172_TextGrunt1Intro:
	.string "Hey! This station is under TEAM PALM\n"
	.string "“maintenance”! Beat it!$"

Palm172_TextGrunt1Loss:
	.string "Maintenance… failed.$"

Palm172_TextGrunt1After:
	.string "We only turned them up a little!\n"
	.string "The readings were so interesting…$"

Palm172_TextGrunt2Intro:
	.string "The amplifiers make the water dance!\n"
	.string "You're not touching them!$"

Palm172_TextGrunt2Loss:
	.string "The data! My beautiful data!$"

Palm172_TextGrunt2After:
	.string "Each tank pushes a wave through the\n"
	.string "lake. Three tanks, three waves.$"

Palm172_TextGrunt3Intro:
	.string "Those POKéMON swam into our nets\n"
	.string "on their own! Finders keepers!$"

Palm172_TextGrunt3Loss:
	.string "Fine, fine, let them go…$"

Palm172_TextGrunt3After:
	.string "We were going to let them go anyway.\n"
	.string "Probably.$"

Palm172_TextAmp:
	.string "A machine is humming loudly.\n"
	.string "A label reads “AMPLIFIER · PALM”.\p"
	.string "Shut it down?$"

Palm172_TextAmpDown:
	.string "The amplifier powered down.\n"
	.string "The humming fades away…$"

Palm172_TextAmpIsOff:
	.string "The amplifier is silent.$"

Palm172_TextNetMARILL:
	.string "A MARILL is tangled in a TEAM PALM\n"
	.string "net!$"

Palm172_TextFreedMARILL:
	.string "You untangled the net.\n"
	.string "MARILL dove happily into the pool!$"

Palm172_TextNetPSYDUCK:
	.string "A PSYDUCK is stuck in a net, holding\n"
	.string "its head in pain.$"

Palm172_TextFreedPSYDUCK:
	.string "You freed PSYDUCK!\n"
	.string "It waddled off toward the water.$"

Palm172_TextNetLOTAD:
	.string "A LOTAD is wrapped up in a net!$"

Palm172_TextFreedLOTAD:
	.string "You cut the net open.\n"
	.string "LOTAD floated away, relieved!$"

Palm172_TextTerminalBusy:
	.string "The terminal shows three wave graphs\n"
	.string "and three warning lights.\p"
	.string "Something here is still running, and\n"
	.string "POKéMON are still trapped.$"

Palm172_TextTerminal:
	.string "All the warning lights are off.\n"
	.string "One file was left on the screen.$"

Palm172_TextRecord:
	.string "UNIDENTIFIED RECORD\n"
	.string "SOURCE: EXTERNAL\l"
	.string "DIRECTION: NORTH\l"
	.string "SIGNAL: IRREGULAR\p"
	.string "There is nothing else in the file.$"

Palm172_TextChelsiaRecord:
	.string "CHELSIA: “External… north…”\n"
	.string "What does that mean?\p"
	.string "Whatever TEAM PALM was measuring,\n"
	.string "the lake was only an echo of it.\p"
	.string "Look, the water is already going\n"
	.string "down! Thank you, {PLAYER}!\p"
	.string "I'll open my GYM right away.\n"
	.string "Come and challenge me there!$"