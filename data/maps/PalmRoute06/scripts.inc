PalmRoute06_MapScripts::
	.byte 0

Palm140_RouteREN::
	trainerbattle_single TRAINER_PALM_ROUTE06_REN, Palm140_TextRENIntro, Palm140_TextRENLoss
	msgbox Palm140_TextRENAfter, MSGBOX_AUTOCLOSE
	end

Palm140_RouteMIKA::
	trainerbattle_single TRAINER_PALM_ROUTE06_MIKA, Palm140_TextMIKAIntro, Palm140_TextMIKALoss
	msgbox Palm140_TextMIKAAfter, MSGBOX_AUTOCLOSE
	end

Palm140_RouteSAYO::
	trainerbattle_single TRAINER_PALM_ROUTE06_SAYO, Palm140_TextSAYOIntro, Palm140_TextSAYOLoss
	msgbox Palm140_TextSAYOAfter, MSGBOX_AUTOCLOSE
	end

Palm140_RouteHANA::
	trainerbattle_single TRAINER_PALM_ROUTE06_HANA, Palm140_TextHANAIntro, Palm140_TextHANALoss
	msgbox Palm140_TextHANAAfter, MSGBOX_AUTOCLOSE
	end

Palm140_SignWest::
	msgbox Palm140_SignWest_Text, MSGBOX_SIGN
	end

Palm140_SignEast::
	msgbox Palm140_SignEast_Text, MSGBOX_SIGN
	end

Palm140_Shrine::
	msgbox Palm140_Shrine_Text, MSGBOX_SIGN
	end


Palm140_SignWest_Text:
	.string "ROUTE 6 - GARDEN PATH\n"
	.string "West: PILLARTON CITY\l"
	.string "East: SERENIA$"

Palm140_SignEast_Text:
	.string "SERENIA just ahead.\n"
	.string "Please walk quietly.$"

Palm140_Shrine_Text:
	.string "A small wayside shrine.\n"
	.string "Someone left fresh flowers here.$"

Palm140_TextRENIntro:
	.string "I sensed you coming three bends\n"
	.string "ago. My POKéMON did too!$"

Palm140_TextRENLoss:
	.string "I didn't see that coming...$"

Palm140_TextRENAfter:
	.string "Lately the wind blows the wrong\n"
	.string "way near SERENIA. Strange, no?$"

Palm140_TextMIKAIntro:
	.string "Pink, fluffy and fierce!\n"
	.string "That's my team!$"

Palm140_TextMIKALoss:
	.string "Not so fierce after all...$"

Palm140_TextMIKAAfter:
	.string "COTTONEE love the breeze from the\n"
	.string "stone garden.$"

Palm140_TextSAYOIntro:
	.string "The garden whispers about you...\n"
	.string "Let's see if it's right.$"

Palm140_TextSAYOLoss:
	.string "The whispers were right.$"

Palm140_TextSAYOAfter:
	.string "People in SERENIA keep seeing old\n"
	.string "things in new places. Illusions...$"

Palm140_TextHANAIntro:
	.string "Breathe in the flowers... and\n"
	.string "then breathe in defeat!$"

Palm140_TextHANALoss:
	.string "I'm the one out of breath...$"

Palm140_TextHANAAfter:
	.string "JADE, SERENIA's GYM LEADER, walks\n"
	.string "here with her ESPEON every dawn.$"