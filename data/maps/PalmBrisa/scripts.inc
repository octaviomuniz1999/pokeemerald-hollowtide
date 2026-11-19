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
	.string "I perform at the THEATER OF ECHOES.\p"
	.string "Tonight is the festival, but three\n"
	.string "street lamps went dark!\p"
	.string "One by the west houses, one in\n"
	.string "the plaza, one on the boardwalk.\p"
	.string "Could you switch them back on?\n"
	.string "The show can't start in the dark.$"

Palm080_TextBrisaSign:
	.string "BREEZEPORT CITY\n"
	.string "Where the sea breeze never sleeps.\p"
	.string "North: ROUTE 2$"

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
	.string "The stage has its lights back!\n"
	.string "JAY is waiting at the THEATER.$"
Palm090_TextLocked:
	.string "THEATER OF ECHOES\p"
	.string "Closed until the festival lamps\n"
	.string "are lit. Ask the artist out front.$"
Palm090_TextPoster:
	.string "TEAM PALM\n"
	.string "Clean energy for a better coast!\p"
	.string "Someone has scribbled underneath:\n"
	.string "“Better for whom?”$"
Palm090_TextEast:
	.string "WEST BEACH TRAIL - ROUTE 3\p"
	.string "The trail is closed during the\n"
	.string "festival. Ask GYM LEADER JAY.$"

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
	.string "The lamp is glowing.$"
Palm090_TextAllLit:
	.string "All three lamps are glowing!\n"
	.string "The THEATER OF ECHOES is open!$"

Palm090_BrisaLoad::
	call_if_set FLAG_PALM_BRISA_LAMP1, Palm090_DrawLamp1
	call_if_set FLAG_PALM_BRISA_LAMP2, Palm090_DrawLamp2
	call_if_set FLAG_PALM_BRISA_LAMP3, Palm090_DrawLamp3
	call_if_set FLAG_PALM_BRISA_LIGHTS, Palm090_OpenTheater
	call_if_unset FLAG_PALM_BRISA_LIGHTS, Palm090_LockTheater
	end

Palm090_OpenTheater::
	setmetatile 47, 27, 475, TRUE
	return

Palm090_DrawLamp1::
	setmetatile 12, 20, 576, FALSE
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
	setmetatile 33, 21, 576, FALSE
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
	setmetatile 60, 34, 576, FALSE
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
	.string "WEST BEACH TRAIL - ROUTE 3\n"
	.string "Up the coast to FERRALIA CITY.$"

Palm090_LockTheater::
	setmetatile 47, 27, 738, TRUE
	return

Palm092_KeeperHouse::
	msgbox Palm092_TextKeeperHouse, MSGBOX_SIGN
	end

Palm092_TextKeeperHouse:
	.string "LIGHTHOUSE KEEPER'S HOUSE$"
