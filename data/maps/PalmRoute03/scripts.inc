PalmRoute03_MapScripts::
	.byte 0

Palm090_BackBrisa::
	warp MAP_PALM_BRISA, 2, 41
	waitstate
	end

Palm090_Route03Sign::
	msgbox Palm090_TextRoute03, MSGBOX_SIGN
	end

Palm090_TextRoute03:
	.string "ROTA 03\n"
	.string "Oeste: CIDADE DA BRISA.\p"
	.string "Leste: FERRALIA.$"

Palm091_RouteEast::
	msgbox Palm091_TextRouteEast, MSGBOX_SIGN
	end

Palm091_TextRouteEast:
	.string "FERRALIA: logo adiante.\n"
	.string "Entrada do patio de carga.$"
