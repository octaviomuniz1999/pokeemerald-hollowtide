PalmBrisa_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm090_BrisaLoad
	.byte 0

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
	setmetatile 12, 20, 866, FALSE
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
	setmetatile 33, 21, 863, FALSE
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
	setmetatile 60, 34, 863, FALSE
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

Palm093_Greeter::
	msgbox Palm093_Greeter_Text, MSGBOX_NPC
	end

Palm093_PlazaGirl::
	msgbox Palm093_PlazaGirl_Text, MSGBOX_NPC
	end

Palm093_LookoutHiker::
	msgbox Palm093_LookoutHiker_Text, MSGBOX_NPC
	end

Palm093_BeachWoman::
	msgbox Palm093_BeachWoman_Text, MSGBOX_NPC
	end

Palm093_Fisherman::
	msgbox Palm093_Fisherman_Text, MSGBOX_NPC
	end

Palm093_JayFan::
	msgbox Palm093_JayFan_Text, MSGBOX_NPC
	end

Palm093_KeeperOldMan::
	msgbox Palm093_KeeperOldMan_Text, MSGBOX_NPC
	end

Palm093_PumpWife::
	msgbox Palm093_PumpWife_Text, MSGBOX_NPC
	end

Palm093_StoreKid::
	msgbox Palm093_StoreKid_Text, MSGBOX_NPC
	end

Palm093_FestivalBeauty::
	msgbox Palm093_FestivalBeauty_Text, MSGBOX_NPC
	end


Palm093_Greeter_Text:
	.string "Welcome to BREEZEPORT!\p"
	.string "Follow the avenue down and you'll\n"
	.string "smell the sea before you see it.$"

Palm093_PlazaGirl_Text:
	.string "At night the festival lamps make\n"
	.string "the whole plaza sparkle!$"

Palm093_LookoutHiker_Text:
	.string "On clear days you can see a peak\n"
	.string "far to the north, lost in clouds.\p"
	.string "People say nobody climbs it\n"
	.string "anymore. I wonder why...$"

Palm093_BeachWoman_Text:
	.string "The water's warmer this year.\p"
	.string "And the tide comes in so fast now.\n"
	.string "It never used to.$"

Palm093_Fisherman_Text:
	.string "The fish bite less since those\n"
	.string "new pipes went in up the coast.\p"
	.string "TEAM PALM says it's progress.\n"
	.string "My nets say otherwise.$"

Palm093_JayFan_Text:
	.string "Have you seen JAY perform?\p"
	.string "Her ghosts dance with the stage\n"
	.string "lights. It gives me chills!$"

Palm093_KeeperOldMan_Text:
	.string "The lighthouse fell in last\n"
	.string "winter's storm.\p"
	.string "We're rebuilding it, stone by\n"
	.string "stone. Storms used to be gentler.$"

Palm093_PumpWife_Text:
	.string "My husband works at the pump\n"
	.string "station by the harbor.\p"
	.string "He says TEAM PALM bought half the\n"
	.string "pumps on this coast. Strange, no?$"

Palm093_StoreKid_Text:
	.string "The DEPARTMENT STORE by the beach\n"
	.string "sells everything. Even POKé BALLS!$"

Palm093_FestivalBeauty_Text:
	.string "Every summer the THEATER OF ECHOES\n"
	.string "hosts the festival.\p"
	.string "It's the heart of this city.\n"
	.string "Tonight, it beats again.$"