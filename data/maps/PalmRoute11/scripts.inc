PalmRoute11_MapScripts::
	.byte 0

Palm210_BadgeGate::
	goto_if_set FLAG_BADGE08_GET, Palm210_Ok
	lockall
	msgbox Palm210_TextBadgeGate, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm210_StepBackEast
	waitmovement 0
	releaseall
	end

Palm210_Ok::
	end

Palm210_StepBackEast:
	walk_right
	step_end

Palm210_RouteVINCENT::
	trainerbattle_single TRAINER_PALM_ROUTE11_VINCENT, Palm210_TextVINCENTIntro, Palm210_TextVINCENTLoss
	msgbox Palm210_TextVINCENTAfter, MSGBOX_AUTOCLOSE
	end

Palm210_RouteFELIX::
	trainerbattle_single TRAINER_PALM_ROUTE11_FELIX, Palm210_TextFELIXIntro, Palm210_TextFELIXLoss
	msgbox Palm210_TextFELIXAfter, MSGBOX_AUTOCLOSE
	end

Palm210_RouteLEROY::
	trainerbattle_single TRAINER_PALM_ROUTE11_LEROY, Palm210_TextLEROYIntro, Palm210_TextLEROYLoss
	msgbox Palm210_TextLEROYAfter, MSGBOX_AUTOCLOSE
	end

Palm210_SignEast::
	msgbox Palm210_SignEast_Text, MSGBOX_SIGN
	end

Palm210_SignCave::
	msgbox Palm210_SignCave_Text, MSGBOX_SIGN
	end


Palm210_TextBadgeGate:
	.string "GUARD: Halt! This road leads to the\n"
	.string "POKéMON LEAGUE.\p"
	.string "Only trainers with all eight GYM\n"
	.string "BADGES of LUNIA may pass.$"

Palm210_TextVINCENTIntro:
	.string "Every trainer on this road has eight\n"
	.string "badges. Let's see what yours are worth!$"

Palm210_TextVINCENTLoss:
	.string "Worth a lot, apparently.$"

Palm210_TextVINCENTAfter:
	.string "The tunnel through the mountain leads\n"
	.string "to the LEAGUE island. Good luck.$"

Palm210_TextFELIXIntro:
	.string "I lost to the ELITE FOUR last year.\n"
	.string "This time I'm training on this road!$"

Palm210_TextFELIXLoss:
	.string "I still have a lot to learn…$"

Palm210_TextFELIXAfter:
	.string "They say the first ELITE member\n"
	.string "freezes challengers solid. Stay warm!$"

Palm210_TextLEROYIntro:
	.string "The last trainer before the tunnel!\n"
	.string "Show me you deserve the LEAGUE!$"

Palm210_TextLEROYLoss:
	.string "You deserve it. No doubt.$"

Palm210_TextLEROYAfter:
	.string "DOGE is the CHAMPION. Nobody has\n"
	.string "beaten him since he won the title.$"

Palm210_SignEast_Text:
	.string "ROUTE 11 · LEAGUE ROAD\n"
	.string "East: TIDEMOUTH$"

Palm210_SignCave_Text:
	.string "LEAGUE TUNNEL\n"
	.string "To the POKéMON LEAGUE.$"