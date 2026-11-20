PalmRoute13_MapScripts::
	.byte 0

Palm251_RouteLUNA::
	trainerbattle_single TRAINER_PALM_ROUTE13_LUNA, Palm251_TextLUNAIntro, Palm251_TextLUNALoss
	msgbox Palm251_TextLUNAAfter, MSGBOX_AUTOCLOSE
	end

Palm251_RouteKAIO::
	trainerbattle_single TRAINER_PALM_ROUTE13_KAIO, Palm251_TextKAIOIntro, Palm251_TextKAIOLoss
	msgbox Palm251_TextKAIOAfter, MSGBOX_AUTOCLOSE
	end

Palm251_RouteRAUL::
	trainerbattle_single TRAINER_PALM_ROUTE13_RAUL, Palm251_TextRAULIntro, Palm251_TextRAULLoss
	msgbox Palm251_TextRAULAfter, MSGBOX_AUTOCLOSE
	end

Palm251_SignWest::
	msgbox Palm251_SignWest_Text, MSGBOX_SIGN
	end


Palm251_SignWest_Text:
	.string "ROUTE 13 - MIRROR GROVE\n"
	.string "West: ROUTE 7$"

Palm251_TextLUNAIntro:
	.string "Look into the water… Is that your\n"
	.string "reflection? Or is it looking back?$"

Palm251_TextLUNALoss:
	.string "Hehehe… The grove liked that battle.$"

Palm251_TextLUNAAfter:
	.string "The ponds here never ripple. People\n"
	.string "say they show you as you really are.$"

Palm251_TextKAIOIntro:
	.string "I've been copying your steps since\n"
	.string "you came in. Didn't you notice?$"

Palm251_TextKAIOLoss:
	.string "I can copy moves, but not your\n"
	.string "strength.$"

Palm251_TextKAIOAfter:
	.string "A fox with a white mane plays tricks\n"
	.string "on travelers here. One moment it's a\l"
	.string "stone, the next it's gone.$"

Palm251_TextRAULIntro:
	.string "These stones were set in a circle\n"
	.string "long ago. I'm here to find out why!$"

Palm251_TextRAULLoss:
	.string "Ow… Back to my notes, then.$"

Palm251_TextRAULAfter:
	.string "Four stones, four ponds, and a path\n"
	.string "that always brings you back to the\l"
	.string "start. Somebody planned this place.$"