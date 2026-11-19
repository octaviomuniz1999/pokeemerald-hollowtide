PalmRoute03_MapScripts::
	.byte 0

Palm100_ToFerralia::
	warp MAP_PALM_FERRALIA, 1, 10
	waitstate
	end

Palm100_SignBeach::
	msgbox Palm100_TextSignBeach, MSGBOX_SIGN
	end

Palm100_SignPlateau::
	msgbox Palm100_TextSignPlateau, MSGBOX_SIGN
	end

Palm100_RouteRUI::
	trainerbattle_single TRAINER_PALM_ROUTE03_RUI, Palm100_TextRUIIntro, Palm100_TextRUILoss
	msgbox Palm100_TextRUIAfter, MSGBOX_AUTOCLOSE
	end

Palm100_RouteTOMAS::
	trainerbattle_single TRAINER_PALM_ROUTE03_TOMAS, Palm100_TextTOMASIntro, Palm100_TextTOMASLoss
	msgbox Palm100_TextTOMASAfter, MSGBOX_AUTOCLOSE
	end

Palm100_RouteBENTO::
	trainerbattle_single TRAINER_PALM_ROUTE03_BENTO, Palm100_TextBENTOIntro, Palm100_TextBENTOLoss
	msgbox Palm100_TextBENTOAfter, MSGBOX_AUTOCLOSE
	end

Palm100_RouteIARA::
	trainerbattle_single TRAINER_PALM_ROUTE03_IARA, Palm100_TextIARAIntro, Palm100_TextIARALoss
	msgbox Palm100_TextIARAAfter, MSGBOX_AUTOCLOSE
	end

Palm100_RouteDAVI::
	trainerbattle_single TRAINER_PALM_ROUTE03_DAVI, Palm100_TextDAVIIntro, Palm100_TextDAVILoss
	msgbox Palm100_TextDAVIAfter, MSGBOX_AUTOCLOSE
	end


Palm100_TextSignBeach:
	.string "ROUTE 3\n"
	.string "East: BREEZEPORT CITY\p"
	.string "North: up the SERRA trail to\n"
	.string "the plateau and FERRALIA CITY.$"

Palm100_TextSignPlateau:
	.string "ROUTE 3 - PLATEAU\n"
	.string "North: FERRALIA CITY$"

Palm100_TextRUIIntro:
	.string "Shh! You'll scare the fish!\n"
	.string "...Fine, a battle it is!$"

Palm100_TextRUILoss:
	.string "Hooked, reeled in and released!$"

Palm100_TextRUIAfter:
	.string "The fish moved out past the rock\n"
	.string "since the water got warmer.$"

Palm100_TextTOMASIntro:
	.string "The forest on this slope is full\n"
	.string "of bugs! Want to see my best?$"

Palm100_TextTOMASLoss:
	.string "Bzzt... squashed.$"

Palm100_TextTOMASAfter:
	.string "COMBEE build their hives near the\n"
	.string "waterfalls up the SERRA.$"

Palm100_TextBENTOIntro:
	.string "This old trail is steep, but it\n"
	.string "keeps legs and POKéMON strong!$"

Palm100_TextBENTOLoss:
	.string "I need to catch my breath...$"

Palm100_TextBENTOAfter:
	.string "Few people take this path since\n"
	.string "the main stairs were built.$"

Palm100_TextIARAIntro:
	.string "I came up for a picnic, but a\n"
	.string "battle sounds even better!$"

Palm100_TextIARALoss:
	.string "My sandwiches are safe, at least.$"

Palm100_TextIARAAfter:
	.string "From the plateau you can see the\n"
	.string "smoke over FERRALIA's factories.$"

Palm100_TextDAVIIntro:
	.string "Made it to the plateau? Then\n"
	.string "you're ready for a real battle!$"

Palm100_TextDAVILoss:
	.string "Okay, you're the real deal.$"

Palm100_TextDAVIAfter:
	.string "FERRALIA never sleeps. Trains run\n"
	.string "day and night with heavy cargo.$"