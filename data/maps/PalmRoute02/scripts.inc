PalmRoute02_MapScripts::
	.byte 0

Palm080_ReturnColheita::
	warp MAP_OLDALE_TOWN, 18, 34
	waitstate
	end

Palm080_EnterBrisa::
	warp MAP_PALM_BRISA, 19, 2
	waitstate
	end

Palm080_RouteSignNorth::
	msgbox Palm080_TextRouteNorth, MSGBOX_SIGN
	end

Palm080_RouteSignSouth::
	msgbox Palm080_TextRouteSouth, MSGBOX_SIGN
	end

Palm080_TextRouteNorth:
	.string "ROUTE 2\n"
	.string "North: HARVESTVALE\p"
	.string "For BREEZEPORT, follow the trail\n"
	.string "south toward the sea.$"

Palm080_TextRouteSouth:
	.string "ROUTE 2\n"
	.string "BREEZEPORT CITY just ahead.$"

Palm080_RouteLIANG::
	trainerbattle_single TRAINER_PALM_ROUTE02_LIANG, Palm080_TextLIANGIntro, Palm080_TextLIANGLoss
	release
	end

Palm080_TextLIANGIntro:
	.string "Smell that? Salt air!\n"
	.string "Let's battle before the beach!$"

Palm080_TextLIANGLoss:
	.string "Boa batalha!$"

Palm080_RouteMEI_LAN::
	trainerbattle_single TRAINER_PALM_ROUTE02_MEI_LAN, Palm080_TextMEI_LANIntro, Palm080_TextMEI_LANLoss
	release
	end

Palm080_TextMEI_LANIntro:
	.string "My POKéMON love the sea breeze.\n"
	.string "Want to see why?$"

Palm080_TextMEI_LANLoss:
	.string "Boa batalha!$"

Palm080_RouteQIN::
	trainerbattle_single TRAINER_PALM_ROUTE02_QIN, Palm080_TextQINIntro, Palm080_TextQINLoss
	release
	end

Palm080_TextQINIntro:
	.string "Every trainer heading to\n"
	.string "BREEZEPORT has to get past me!$"

Palm080_TextQINLoss:
	.string "Boa batalha!$"
