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
	.string "ROTA 02\n"
	.string "Norte: VILA DA COLHEITA.\p"
	.string "Para BRISA, siga a trilha ao sul.$"

Palm080_TextRouteSouth:
	.string "ROTA 02\n"
	.string "CIDADE DA BRISA logo ao sul.\n"
	.string "Siga pelo caminho de terra.$"

Palm080_RouteLIANG::
	trainerbattle_single TRAINER_PALM_ROUTE02_LIANG, Palm080_TextLIANGIntro, Palm080_TextLIANGLoss
	release
	end

Palm080_TextLIANGIntro:
	.string "Vamos batalhar na ROTA 02!$"

Palm080_TextLIANGLoss:
	.string "Boa batalha!$"

Palm080_RouteMEI_LAN::
	trainerbattle_single TRAINER_PALM_ROUTE02_MEI_LAN, Palm080_TextMEI_LANIntro, Palm080_TextMEI_LANLoss
	release
	end

Palm080_TextMEI_LANIntro:
	.string "Vamos batalhar na ROTA 02!$"

Palm080_TextMEI_LANLoss:
	.string "Boa batalha!$"

Palm080_RouteQIN::
	trainerbattle_single TRAINER_PALM_ROUTE02_QIN, Palm080_TextQINIntro, Palm080_TextQINLoss
	release
	end

Palm080_TextQINIntro:
	.string "Vamos batalhar na ROTA 02!$"

Palm080_TextQINLoss:
	.string "Boa batalha!$"
