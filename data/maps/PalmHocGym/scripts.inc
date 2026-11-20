PalmHocGym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm194_Load
	.byte 0

Palm194_Load::
	goto_if_lt VAR_HT_HOC_GYM, 1, Palm194_LoadEnd
	setmetatile 4, 13, 560, FALSE
	setmetatile 5, 13, 561, FALSE
	setmetatile 4, 14, 568, FALSE
	setmetatile 5, 14, 569, FALSE
	setmetatile 0, 15, 518, FALSE
	goto_if_lt VAR_HT_HOC_GYM, 2, Palm194_LoadEnd
	setmetatile 7, 10, 562, FALSE
	setmetatile 8, 10, 563, FALSE
	setmetatile 7, 11, 570, FALSE
	setmetatile 8, 11, 571, FALSE
	setmetatile 4, 12, 518, FALSE
	goto_if_lt VAR_HT_HOC_GYM, 3, Palm194_LoadEnd
	setmetatile 4, 10, 562, FALSE
	setmetatile 5, 10, 563, FALSE
	setmetatile 4, 11, 570, FALSE
	setmetatile 5, 11, 571, FALSE
	setmetatile 8, 9, 518, FALSE
	goto_if_lt VAR_HT_HOC_GYM, 4, Palm194_LoadEnd
	setmetatile 4, 6, 560, FALSE
	setmetatile 5, 6, 561, FALSE
	setmetatile 4, 7, 568, FALSE
	setmetatile 5, 7, 569, FALSE
	setmetatile 3, 9, 518, FALSE
Palm194_LoadEnd::
	end

Palm194_Console1::
	goto_if_ge VAR_HT_HOC_GYM, 1, Palm194_End
	lockall
	playse SE_SWITCH
	setmetatile 0, 15, 518, FALSE
	setmetatile 4, 13, 560, FALSE
	setmetatile 5, 13, 561, FALSE
	setmetatile 4, 14, 568, FALSE
	setmetatile 5, 14, 569, FALSE
	special DrawWholeMapView
	playse SE_UNLOCK
	setvar VAR_HT_HOC_GYM, 1
	msgbox Palm194_TextConsole1, MSGBOX_DEFAULT
	releaseall
	end

Palm194_Console2::
	goto_if_ge VAR_HT_HOC_GYM, 2, Palm194_End
	lockall
	playse SE_SWITCH
	setmetatile 4, 12, 518, FALSE
	setmetatile 7, 10, 562, FALSE
	setmetatile 8, 10, 563, FALSE
	setmetatile 7, 11, 570, FALSE
	setmetatile 8, 11, 571, FALSE
	special DrawWholeMapView
	playse SE_UNLOCK
	setvar VAR_HT_HOC_GYM, 2
	msgbox Palm194_TextConsole2, MSGBOX_DEFAULT
	releaseall
	end

Palm194_Console3::
	goto_if_ge VAR_HT_HOC_GYM, 3, Palm194_End
	lockall
	playse SE_SWITCH
	setmetatile 8, 9, 518, FALSE
	setmetatile 4, 10, 562, FALSE
	setmetatile 5, 10, 563, FALSE
	setmetatile 4, 11, 570, FALSE
	setmetatile 5, 11, 571, FALSE
	special DrawWholeMapView
	playse SE_UNLOCK
	setvar VAR_HT_HOC_GYM, 3
	msgbox Palm194_TextConsole3, MSGBOX_DEFAULT
	releaseall
	end

Palm194_Console4::
	goto_if_ge VAR_HT_HOC_GYM, 4, Palm194_End
	lockall
	playse SE_SWITCH
	setmetatile 3, 9, 518, FALSE
	setmetatile 4, 6, 560, FALSE
	setmetatile 5, 6, 561, FALSE
	setmetatile 4, 7, 568, FALSE
	setmetatile 5, 7, 569, FALSE
	special DrawWholeMapView
	playse SE_UNLOCK
	setvar VAR_HT_HOC_GYM, 4
	msgbox Palm194_TextConsole4, MSGBOX_DEFAULT
	releaseall
	end

Palm194_End::
	end

Palm194_Hoc::
	trainerbattle_single TRAINER_PALM_HOC, Palm194_TextHocIntro, Palm194_TextHocDefeat, Palm194_HocDefeated, NO_MUSIC
	msgbox Palm194_TextHocAfter, MSGBOX_DEFAULT
	release
	end

Palm194_HocDefeated::
	message Palm194_TextBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox Palm194_TextBadgeExplain, MSGBOX_DEFAULT
	setflag FLAG_BADGE07_GET
	setflag FLAG_DEFEATED_LAVARIDGE_GYM
	giveitem ITEM_TM_VOLT_SWITCH
	msgbox Palm194_TextTM, MSGBOX_DEFAULT
	msgbox Palm194_TextRiven, MSGBOX_DEFAULT
	release
	end

Palm194_Rotom::
	lock
	faceplayer
	playmoncry SPECIES_ROTOM, CRY_MODE_NORMAL
	msgbox Palm194_TextRotom, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Palm194_Guide::
	lock
	faceplayer
	goto_if_set FLAG_BADGE07_GET, Palm194_GuideAfter
	msgbox Palm194_TextGuide, MSGBOX_DEFAULT
	release
	end

Palm194_GuideAfter::
	msgbox Palm194_TextGuideAfter, MSGBOX_DEFAULT
	release
	end

Palm194_Statue::
	lockall
	goto_if_set FLAG_BADGE07_GET, Palm194_StatueWon
	msgbox Palm194_TextStatue, MSGBOX_DEFAULT
	releaseall
	end

Palm194_StatueWon::
	msgbox Palm194_TextStatueWon, MSGBOX_DEFAULT
	releaseall
	end

Palm194_Diagram::
	msgbox Palm194_TextDiagram, MSGBOX_SIGN
	end

Palm194_TrainerA::
	trainerbattle_single TRAINER_PALM_HOC_GYM_A, Palm194_TextAIntro, Palm194_TextADefeat
	msgbox Palm194_TextAAfter, MSGBOX_AUTOCLOSE
	end

Palm194_TrainerB::
	trainerbattle_single TRAINER_PALM_HOC_GYM_B, Palm194_TextBIntro, Palm194_TextBDefeat
	msgbox Palm194_TextBAfter, MSGBOX_AUTOCLOSE
	end

Palm194_TrainerC::
	trainerbattle_single TRAINER_PALM_HOC_GYM_C, Palm194_TextCIntro, Palm194_TextCDefeat
	msgbox Palm194_TextCAfter, MSGBOX_AUTOCLOSE
	end


Palm194_TextGuide:
	.string "Hey, future CHAMPION {PLAYER}!\p"
	.string "This is THE CIRCUIT. HOC uses\n"
	.string "ELECTRIC-type POKéMON.\p"
	.string "Every beam in here is live. The four\n"
	.string "floor switches are power consoles.\p"
	.string "Each console cuts the beam that guards\n"
	.string "the next one. Find them in order, and\l"
	.string "the current leads you to HOC!\p"
	.string "GROUND-type POKéMON are a great help.$"

Palm194_TextGuideAfter:
	.string "You closed the whole circuit!\n"
	.string "HOC hasn't lost like that in years.$"

Palm194_TextDiagram:
	.string "A wiring diagram is taped to the wall:\p"
	.string "“CONSOLE 1 - LOW BEAM\n"
	.string "CONSOLE 2 - EAST BEAM\l"
	.string "CONSOLE 3 - CENTER BEAM\l"
	.string "CONSOLE 4 - LEADER”$"

Palm194_TextConsole1:
	.string "Click! The console powers down the\n"
	.string "low beam. The current moves on…$"

Palm194_TextConsole2:
	.string "Click! The east beam goes dark.$"

Palm194_TextConsole3:
	.string "Click! The center beam goes dark.$"

Palm194_TextConsole4:
	.string "Click! The last beam goes dark.\n"
	.string "The way to HOC is open!$"

Palm194_TextStatue:
	.string "VOLTARA CITY POKéMON GYM\p"
	.string "HOC's CERTIFIED TRAINERS:\n"
	.string "{PLAYER}?$"

Palm194_TextStatueWon:
	.string "VOLTARA CITY POKéMON GYM\p"
	.string "HOC's CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

Palm194_TextRotom:
	.string "ROTOM: Bzzt! Bzzzt!\p"
	.string "ROTOM is spinning around the gym's\n"
	.string "cables, sparking happily.$"

Palm194_TextHocIntro:
	.string "HOC: Thanks for bringing the power\n"
	.string "back, {PLAYER}. The whole city owes you.\p"
	.string "But in here, I'm the GYM LEADER.\n"
	.string "And my circuit never breaks!$"

Palm194_TextHocDefeat:
	.string "Short circuit! You really are strong.$"

Palm194_TextBadge:
	.string "{PLAYER} received the CIRCUIT BADGE\n"
	.string "from HOC.$"

Palm194_TextBadgeExplain:
	.string "The CIRCUIT BADGE proves you can keep\n"
	.string "the current flowing, no matter what.\p"
	.string "Here, take this too.$"

Palm194_TextTM:
	.string "That's VOLT SWITCH. Attack, then swap\n"
	.string "out. Smart battling, like good code.$"

Palm194_TextRiven:
	.string "…Oh, a message from RIVEN.\p"
	.string "“HOC, tell the kid to keep the data\n"
	.string "safe. Don't ask why. Not yet.”\p"
	.string "Huh. You heard him. Keep it safe.$"

Palm194_TextHocAfter:
	.string "HOC: The road south leads to the sea.\n"
	.string "JAY says the tides are acting weird.\p"
	.string "Be careful out there, {PLAYER}.$"

Palm194_TextAIntro:
	.string "My guitar runs on pure voltage!\n"
	.string "Let's rock this circuit!$"

Palm194_TextADefeat:
	.string "Blew a fuse…$"

Palm194_TextAAfter:
	.string "Console 2 is in the east wing. Step on\n"
	.string "it and the east beam goes down.$"

Palm194_TextBIntro:
	.string "Only true experts reach this room.\n"
	.string "Prove you belong here!$"

Palm194_TextBDefeat:
	.string "Impressive wiring.$"

Palm194_TextBAfter:
	.string "The center beam opens the west room.\n"
	.string "That's where the last console is.$"

Palm194_TextCIntro:
	.string "One console left. And one expert\n"
	.string "standing in your way!$"

Palm194_TextCDefeat:
	.string "The current flows through you.$"

Palm194_TextCAfter:
	.string "Go on. HOC is waiting.$"