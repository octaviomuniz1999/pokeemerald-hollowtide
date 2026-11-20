PalmNamiGym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm205_Load
	.byte 0

Palm205_Load::
	goto_if_ge VAR_HT_NAMI_GYM, 1, Palm205_Load2
	setmetatile 11, 26, 571, FALSE
	setmetatile 12, 26, 572, FALSE
	setmetatile 10, 27, 177, TRUE
	setmetatile 11, 27, 177, TRUE
	setmetatile 12, 27, 177, TRUE
	setmetatile 13, 27, 177, TRUE
	setmetatile 10, 28, 161, TRUE
	setmetatile 11, 28, 161, TRUE
	setmetatile 12, 28, 161, TRUE
	setmetatile 13, 28, 161, TRUE
	setmetatile 10, 29, 161, TRUE
	setmetatile 11, 29, 161, TRUE
	setmetatile 12, 29, 161, TRUE
	setmetatile 13, 29, 161, TRUE
	setmetatile 10, 30, 161, TRUE
	setmetatile 11, 30, 161, TRUE
	setmetatile 12, 30, 161, TRUE
	setmetatile 13, 30, 161, TRUE
	setmetatile 10, 31, 161, TRUE
	setmetatile 11, 31, 161, TRUE
	setmetatile 12, 31, 161, TRUE
	setmetatile 13, 31, 161, TRUE
	setmetatile 11, 32, 571, FALSE
	setmetatile 12, 32, 555, FALSE
Palm205_Load2::
	goto_if_ge VAR_HT_NAMI_GYM, 2, Palm205_Load3
	setmetatile 11, 16, 571, FALSE
	setmetatile 12, 16, 572, FALSE
	setmetatile 10, 17, 177, TRUE
	setmetatile 11, 17, 177, TRUE
	setmetatile 12, 17, 177, TRUE
	setmetatile 13, 17, 177, TRUE
	setmetatile 10, 18, 161, TRUE
	setmetatile 11, 18, 161, TRUE
	setmetatile 12, 18, 161, TRUE
	setmetatile 13, 18, 161, TRUE
	setmetatile 10, 19, 161, TRUE
	setmetatile 11, 19, 161, TRUE
	setmetatile 12, 19, 161, TRUE
	setmetatile 13, 19, 161, TRUE
	setmetatile 10, 20, 161, TRUE
	setmetatile 11, 20, 161, TRUE
	setmetatile 12, 20, 161, TRUE
	setmetatile 13, 20, 161, TRUE
	setmetatile 10, 21, 161, TRUE
	setmetatile 11, 21, 161, TRUE
	setmetatile 12, 21, 161, TRUE
	setmetatile 13, 21, 161, TRUE
	setmetatile 11, 22, 571, FALSE
	setmetatile 12, 22, 555, FALSE
Palm205_Load3::
	goto_if_ge VAR_HT_NAMI_GYM, 3, Palm205_Load4
	setmetatile 10, 8, 177, TRUE
	setmetatile 11, 8, 177, TRUE
	setmetatile 12, 8, 177, TRUE
	setmetatile 13, 8, 177, TRUE
	setmetatile 10, 9, 161, TRUE
	setmetatile 11, 9, 161, TRUE
	setmetatile 12, 9, 161, TRUE
	setmetatile 13, 9, 161, TRUE
	setmetatile 10, 10, 161, TRUE
	setmetatile 11, 10, 161, TRUE
	setmetatile 12, 10, 161, TRUE
	setmetatile 13, 10, 161, TRUE
	setmetatile 10, 11, 161, TRUE
	setmetatile 11, 11, 161, TRUE
	setmetatile 12, 11, 161, TRUE
	setmetatile 13, 11, 161, TRUE
	setmetatile 10, 12, 161, TRUE
	setmetatile 11, 12, 161, TRUE
	setmetatile 12, 12, 161, TRUE
	setmetatile 13, 12, 161, TRUE
	setmetatile 11, 13, 571, FALSE
	setmetatile 12, 13, 555, FALSE
Palm205_Load4::
	end

Palm205_Lever1::
	lockall
	goto_if_ge VAR_HT_NAMI_GYM, 1, Palm205_LeverDone
	msgbox Palm205_TextLever, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm205_Release
	playse SE_SWITCH
	waitse
	playse SE_M_WATERFALL
	setmetatile 11, 26, 563, FALSE
	setmetatile 12, 26, 563, FALSE
	setmetatile 10, 27, 178, FALSE
	setmetatile 11, 27, 563, FALSE
	setmetatile 12, 27, 563, FALSE
	setmetatile 13, 27, 176, FALSE
	setmetatile 10, 28, 186, FALSE
	setmetatile 11, 28, 563, FALSE
	setmetatile 12, 28, 563, FALSE
	setmetatile 13, 28, 184, FALSE
	setmetatile 10, 29, 186, FALSE
	setmetatile 11, 29, 563, FALSE
	setmetatile 12, 29, 563, FALSE
	setmetatile 13, 29, 184, FALSE
	setmetatile 10, 30, 186, FALSE
	setmetatile 11, 30, 563, FALSE
	setmetatile 12, 30, 563, FALSE
	setmetatile 13, 30, 184, FALSE
	setmetatile 10, 31, 186, FALSE
	setmetatile 11, 31, 563, FALSE
	setmetatile 12, 31, 563, FALSE
	setmetatile 13, 31, 184, FALSE
	setmetatile 11, 32, 563, FALSE
	setmetatile 12, 32, 563, FALSE
	special DrawWholeMapView
	setvar VAR_HT_NAMI_GYM, 1
	msgbox Palm205_TextDrained1, MSGBOX_DEFAULT
	releaseall
	end

Palm205_Lever2::
	lockall
	goto_if_ge VAR_HT_NAMI_GYM, 2, Palm205_LeverDone
	msgbox Palm205_TextLever, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm205_Release
	playse SE_SWITCH
	waitse
	playse SE_M_WATERFALL
	setmetatile 11, 16, 563, FALSE
	setmetatile 12, 16, 563, FALSE
	setmetatile 10, 17, 178, FALSE
	setmetatile 11, 17, 563, FALSE
	setmetatile 12, 17, 563, FALSE
	setmetatile 13, 17, 176, FALSE
	setmetatile 10, 18, 186, FALSE
	setmetatile 11, 18, 563, FALSE
	setmetatile 12, 18, 563, FALSE
	setmetatile 13, 18, 184, FALSE
	setmetatile 10, 19, 186, FALSE
	setmetatile 11, 19, 563, FALSE
	setmetatile 12, 19, 563, FALSE
	setmetatile 13, 19, 184, FALSE
	setmetatile 10, 20, 186, FALSE
	setmetatile 11, 20, 563, FALSE
	setmetatile 12, 20, 563, FALSE
	setmetatile 13, 20, 184, FALSE
	setmetatile 10, 21, 186, FALSE
	setmetatile 11, 21, 563, FALSE
	setmetatile 12, 21, 563, FALSE
	setmetatile 13, 21, 184, FALSE
	setmetatile 11, 22, 563, FALSE
	setmetatile 12, 22, 563, FALSE
	special DrawWholeMapView
	setvar VAR_HT_NAMI_GYM, 2
	msgbox Palm205_TextDrained2, MSGBOX_DEFAULT
	releaseall
	end

Palm205_Lever3::
	lockall
	goto_if_ge VAR_HT_NAMI_GYM, 3, Palm205_LeverDone
	msgbox Palm205_TextLever, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm205_Release
	playse SE_SWITCH
	waitse
	playse SE_M_WATERFALL
	setmetatile 10, 8, 178, FALSE
	setmetatile 11, 8, 563, FALSE
	setmetatile 12, 8, 563, FALSE
	setmetatile 13, 8, 176, FALSE
	setmetatile 10, 9, 186, FALSE
	setmetatile 11, 9, 563, FALSE
	setmetatile 12, 9, 563, FALSE
	setmetatile 13, 9, 184, FALSE
	setmetatile 10, 10, 186, FALSE
	setmetatile 11, 10, 563, FALSE
	setmetatile 12, 10, 563, FALSE
	setmetatile 13, 10, 184, FALSE
	setmetatile 10, 11, 186, FALSE
	setmetatile 11, 11, 563, FALSE
	setmetatile 12, 11, 563, FALSE
	setmetatile 13, 11, 184, FALSE
	setmetatile 10, 12, 186, FALSE
	setmetatile 11, 12, 563, FALSE
	setmetatile 12, 12, 563, FALSE
	setmetatile 13, 12, 184, FALSE
	setmetatile 11, 13, 563, FALSE
	setmetatile 12, 13, 563, FALSE
	special DrawWholeMapView
	setvar VAR_HT_NAMI_GYM, 3
	msgbox Palm205_TextDrained3, MSGBOX_DEFAULT
	releaseall
	end

Palm205_LeverDone::
	msgbox Palm205_TextLeverDone, MSGBOX_DEFAULT
	releaseall
	end

Palm205_Release::
	releaseall
	end

Palm205_Exit::
	warp MAP_PALM_TIDEMOUTH, 18, 25
	waitstate
	end

Palm205_Nami::
	trainerbattle_single TRAINER_PALM_NAMI, Palm205_TextNamiIntro, Palm205_TextNamiDefeat, Palm205_NamiDefeated, NO_MUSIC
	msgbox Palm205_TextNamiAfter, MSGBOX_DEFAULT
	release
	end

Palm205_NamiDefeated::
	message Palm205_TextBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox Palm205_TextBadgeExplain, MSGBOX_DEFAULT
	setflag FLAG_BADGE08_GET
	setflag FLAG_DEFEATED_SOOTOPOLIS_GYM
	giveitem ITEM_HM_WATERFALL
	msgbox Palm205_TextTM, MSGBOX_DEFAULT
	release
	end

Palm205_Wailmer::
	lock
	faceplayer
	playmoncry SPECIES_WAILMER, CRY_MODE_NORMAL
	msgbox Palm205_TextWailmer, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Palm205_Guide::
	lock
	faceplayer
	goto_if_set FLAG_BADGE08_GET, Palm205_GuideAfter
	msgbox Palm205_TextGuide, MSGBOX_DEFAULT
	release
	end

Palm205_GuideAfter::
	msgbox Palm205_TextGuideAfter, MSGBOX_DEFAULT
	release
	end

Palm205_Board::
	msgbox Palm205_TextBoard, MSGBOX_SIGN
	end

Palm205_TrainerA::
	trainerbattle_single TRAINER_PALM_NAMI_GYM_A, Palm205_TextAIntro, Palm205_TextADefeat
	msgbox Palm205_TextAAfter, MSGBOX_AUTOCLOSE
	end

Palm205_TrainerB::
	trainerbattle_single TRAINER_PALM_NAMI_GYM_B, Palm205_TextBIntro, Palm205_TextBDefeat
	msgbox Palm205_TextBAfter, MSGBOX_AUTOCLOSE
	end

Palm205_TrainerC::
	trainerbattle_single TRAINER_PALM_NAMI_GYM_C, Palm205_TextCIntro, Palm205_TextCDefeat
	msgbox Palm205_TextCAfter, MSGBOX_AUTOCLOSE
	end


Palm205_TextGuide:
	.string "Hey, future CHAMPION {PLAYER}!\p"
	.string "This is THE LOCKS. NAMI uses\n"
	.string "WATER-type POKéMON.\p"
	.string "Three pools block the way. The lever\n"
	.string "beside each pool drains a channel\l"
	.string "through it.\p"
	.string "Drain them one by one, and the water\n"
	.string "will lead you to NAMI!\p"
	.string "GRASS and ELECTRIC moves help a lot.$"

Palm205_TextGuideAfter:
	.string "All three locks open and NAMI beaten!\n"
	.string "You really ride the wave!$"

Palm205_TextBoard:
	.string "TIDEMOUTH GYM · THE LOCKS\p"
	.string "“Each lever drains one pool.\n"
	.string "Mind the order. Mind your step.”$"

Palm205_TextLever:
	.string "A big lever controls the lock gates.\n"
	.string "Pull it?$"

Palm205_TextDrained1:
	.string "Whoosh! The first pool drains into\n"
	.string "the canal. A path opens!$"

Palm205_TextDrained2:
	.string "Whoosh! The second pool drains.\n"
	.string "The way north is clear!$"

Palm205_TextDrained3:
	.string "Whoosh! The last pool drains.\n"
	.string "NAMI's stage is open!$"

Palm205_TextLeverDone:
	.string "The lock is already open.$"

Palm205_TextWailmer:
	.string "WAILMER: Wooo!\p"
	.string "WAILMER splashes happily.$"

Palm205_TextNamiIntro:
	.string "NAMI: You did it, {PLAYER}! The tide\n"
	.string "is back to normal, thanks to you.\p"
	.string "I love traveling. Every port has its\n"
	.string "own sea, its own rhythm.\p"
	.string "But a GYM LEADER has to stand firm,\n"
	.string "even when the waves get wild.\p"
	.string "Ride the wave with me. Let's go!$"

Palm205_TextNamiDefeat:
	.string "What a swell battle!\n"
	.string "You rode every wave I sent!$"

Palm205_TextBadge:
	.string "{PLAYER} received the TIDE BADGE\n"
	.string "from NAMI.$"

Palm205_TextBadgeExplain:
	.string "That's the TIDE BADGE. With eight\n"
	.string "badges, every POKéMON will obey you.\p"
	.string "And the POKéMON LEAGUE will open\n"
	.string "its gates for you!\p"
	.string "Here, take this too.$"

Palm205_TextTM:
	.string "That's WATERFALL. Your POKéMON can\n"
	.string "climb waterfalls with it.\p"
	.string "NEVARD will be so proud when I tell\n"
	.string "him you beat me.\p"
	.string "The LEAGUE is past ROUTE 11, across\n"
	.string "the sea. Good luck, {PLAYER}!$"

Palm205_TextNamiAfter:
	.string "NAMI: That mountain on the monitor…\n"
	.string "I can't stop thinking about it.\p"
	.string "But first, the LEAGUE! Show them what\n"
	.string "TIDEMOUTH taught you!$"

Palm205_TextAIntro:
	.string "The pools are my home turf!\n"
	.string "Splash attack!$"

Palm205_TextADefeat:
	.string "I sank…$"

Palm205_TextAAfter:
	.string "The next lever is on the east side.\n"
	.string "Watch your step on the wet tiles!$"

Palm205_TextBIntro:
	.string "NAMI trains us every morning at\n"
	.string "sunrise. We're tough!$"

Palm205_TextBDefeat:
	.string "Out of breath…$"

Palm205_TextBAfter:
	.string "The last lever is on the west side,\n"
	.string "right after this pool.$"

Palm205_TextCIntro:
	.string "Only one pool left between you and\n"
	.string "NAMI. And me!$"

Palm205_TextCDefeat:
	.string "You're a natural swimmer!$"

Palm205_TextCAfter:
	.string "Go on. NAMI is waiting on the stage.$"