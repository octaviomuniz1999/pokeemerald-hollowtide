PalmBrisa_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm090_BrisaLoad
	.byte 0

Palm080_ReturnRoute::
	warp MAP_PALM_ROUTE02, 25, 31
	waitstate
	end

Palm080_BrisaHost::
	goto_if_set FLAG_PALM_BRISA_LIGHTS, Palm090_ArtistDone
	setflag FLAG_PALM_BRISA_STARTED
	msgbox Palm080_TextBrisaHost, MSGBOX_NPC
	end

Palm080_BrisaSign::
	msgbox Palm080_TextBrisaSign, MSGBOX_SIGN
	end

Palm080_TextBrisaHost:
	.string "Sou artista do Teatro dos Ecos.\n"
	.string "Tres faroletes apagaram.\p"
	.string "Acenda os tres no calcadao.\n"
	.string "A Jay espera no teatro.$"

Palm080_TextBrisaSign:
	.string "CIDADE DA BRISA\n"
	.string "Norte: ROTA 02.$"

Palm090_ArtistDone::
	msgbox Palm090_TextArtistDone, MSGBOX_NPC
	end

Palm090_TheaterSign::
	goto_if_set FLAG_PALM_BRISA_LIGHTS, Palm090_TheaterOpenSign
	msgbox Palm090_TextLocked, MSGBOX_SIGN
	end

Palm090_TheaterOpenSign::
	msgbox Palm090_TextArtistDone, MSGBOX_SIGN
	end

Palm090_PalmPoster::
	msgbox Palm090_TextPoster, MSGBOX_SIGN
	end

Palm090_EastSign::
	goto_if_set FLAG_PALM_JAY_WON, Palm091_EastOpen
	msgbox Palm090_TextEast, MSGBOX_SIGN
	end

Palm090_ToRoute03::
	goto_if_set FLAG_PALM_JAY_WON, Palm090_WarpRoute03
	lockall
	msgbox Palm090_TextEast, MSGBOX_DEFAULT
	releaseall
	end

Palm090_WarpRoute03::
	warp MAP_PALM_ROUTE03, 3, 13
	waitstate
	end

Palm090_TextArtistDone:
	.string "O palco voltou a ter luz.\n"
	.string "Jay espera no Teatro dos Ecos.$"
Palm090_TextLocked:
	.string "TEATRO DOS ECOS\p"
	.string "Fale com a artista do calcadao.$"
Palm090_TextPoster:
	.string "TEAM PALM\n"
	.string "Energia para um litoral melhor.$"
Palm090_TextEast:
	.string "LESTE: ROTA 03.\n"
	.string "A saida abre apos vencer Jay.$"

Palm090_CityNeedArtist::
	msgbox Palm090_TextLocked, MSGBOX_DEFAULT
	releaseall
	end

Palm090_CityCheck::
	goto_if_unset FLAG_PALM_BRISA_LAMP1, Palm090_CityMore
	goto_if_unset FLAG_PALM_BRISA_LAMP2, Palm090_CityMore
	goto_if_unset FLAG_PALM_BRISA_LAMP3, Palm090_CityMore
	setflag FLAG_PALM_BRISA_LIGHTS
	call Palm090_OpenTheater
	special DrawWholeMapView
	msgbox Palm090_TextAllLit, MSGBOX_DEFAULT
	releaseall
	end

Palm090_CityMore::
	msgbox Palm090_TextLamp, MSGBOX_DEFAULT
	releaseall
	end

Palm090_TextLamp:
	.string "O farolete esta aceso.$"
Palm090_TextAllLit:
	.string "Os tres faroletes estao acesos.\n"
	.string "O Teatro dos Ecos abriu!$"

Palm090_BrisaLoad::
	call_if_set FLAG_PALM_BRISA_LAMP1, Palm090_DrawLamp1
	call_if_set FLAG_PALM_BRISA_LAMP2, Palm090_DrawLamp2
	call_if_set FLAG_PALM_BRISA_LAMP3, Palm090_DrawLamp3
	call_if_set FLAG_PALM_BRISA_LIGHTS, Palm090_OpenTheater
	end

Palm090_OpenTheater::
	setmetatile 8, 17, 461, TRUE
	return

Palm090_DrawLamp1::
	setmetatile 4, 12, 892, TRUE
	return

Palm090_CityLamp1::
	lockall
	goto_if_unset FLAG_PALM_BRISA_STARTED, Palm090_CityNeedArtist
	goto_if_set FLAG_PALM_BRISA_LAMP1, Palm090_CityMore
	playse SE_SWITCH
	setflag FLAG_PALM_BRISA_LAMP1
	call Palm090_DrawLamp1
	special DrawWholeMapView
	goto Palm090_CityCheck

Palm090_DrawLamp2::
	setmetatile 12, 12, 892, TRUE
	return

Palm090_CityLamp2::
	lockall
	goto_if_unset FLAG_PALM_BRISA_STARTED, Palm090_CityNeedArtist
	goto_if_set FLAG_PALM_BRISA_LAMP2, Palm090_CityMore
	playse SE_SWITCH
	setflag FLAG_PALM_BRISA_LAMP2
	call Palm090_DrawLamp2
	special DrawWholeMapView
	goto Palm090_CityCheck

Palm090_DrawLamp3::
	setmetatile 14, 15, 892, TRUE
	return

Palm090_CityLamp3::
	lockall
	goto_if_unset FLAG_PALM_BRISA_STARTED, Palm090_CityNeedArtist
	goto_if_set FLAG_PALM_BRISA_LAMP3, Palm090_CityMore
	playse SE_SWITCH
	setflag FLAG_PALM_BRISA_LAMP3
	call Palm090_DrawLamp3
	special DrawWholeMapView
	goto Palm090_CityCheck

Palm091_EastOpen::
	msgbox Palm091_TextEastOpen, MSGBOX_SIGN
	end

Palm091_TextEastOpen:
	.string "LESTE: ROTA 03.\n"
	.string "Siga ate FERRALIA.$"
