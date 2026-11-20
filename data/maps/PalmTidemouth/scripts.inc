PalmTidemouth_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Palm201_Transition
	.byte 0

Palm201_Nami::
	lock
	faceplayer
	goto_if_set FLAG_HT_TIDEMOUTH_NAMI_MET, Palm201_NamiAgain
	msgbox Palm201_TextNami, MSGBOX_DEFAULT
	setflag FLAG_HT_TIDEMOUTH_NAMI_MET
	release
	end

Palm201_NamiAgain::
	msgbox Palm201_TextNamiAgain, MSGBOX_DEFAULT
	release
	end

Palm201_PortLock::
	lockall
	goto_if_set FLAG_HT_TIDEMOUTH_NAMI_MET, Palm201_Boat
	msgbox Palm201_TextPortLock, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm201_StepBackSouth
	waitmovement 0
	releaseall
	end

Palm201_GymLock::
	goto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm201_TransEnd
	lockall
	msgbox Palm201_TextGymLock, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm201_StepBackSouth
	waitmovement 0
	releaseall
	end

Palm201_StepBackNorth:
	walk_up
	step_end

Palm201_StepBackSouth:
	walk_down
	step_end

Palm201_Sailor::
	msgbox Palm201_Sailor_Text, MSGBOX_NPC
	end

Palm201_Tourist::
	msgbox Palm201_Tourist_Text, MSGBOX_NPC
	end

Palm201_HotelClerk::
	msgbox Palm201_HotelClerk_Text, MSGBOX_NPC
	end

Palm201_PortGuard::
	msgbox Palm201_PortGuard_Text, MSGBOX_NPC
	end

Palm201_GymGuard::
	msgbox Palm201_GymGuard_Text, MSGBOX_NPC
	end

Palm201_Kid::
	msgbox Palm201_Kid_Text, MSGBOX_NPC
	end

Palm201_OldWoman::
	msgbox Palm201_OldWoman_Text, MSGBOX_NPC
	end

Palm201_TownSign::
	msgbox Palm201_TownSign_Text, MSGBOX_SIGN
	end

Palm201_HotelSign::
	msgbox Palm201_HotelSign_Text, MSGBOX_SIGN
	end

Palm201_PortSign::
	msgbox Palm201_PortSign_Text, MSGBOX_SIGN
	end

Palm201_GymSign::
	msgbox Palm201_GymSign_Text, MSGBOX_SIGN
	end

Palm202_PcOldMan::
	msgbox Palm202_PcOldMan_Text, MSGBOX_NPC
	end

Palm202_PcGirl::
	msgbox Palm202_PcGirl_Text, MSGBOX_NPC
	end

Palm202_PcWoman::
	msgbox Palm202_PcWoman_Text, MSGBOX_NPC
	end

Palm202_MartMan::
	msgbox Palm202_MartMan_Text, MSGBOX_NPC
	end

Palm202_MartGent::
	msgbox Palm202_MartGent_Text, MSGBOX_NPC
	end

Palm202_MotelOwner::
	msgbox Palm202_MotelOwner_Text, MSGBOX_NPC
	end

Palm202_House1Woman::
	msgbox Palm202_House1Woman_Text, MSGBOX_NPC
	end

Palm202_House2Man::
	msgbox Palm202_House2Man_Text, MSGBOX_NPC
	end

Palm202_House2Woman::
	msgbox Palm202_House2Woman_Text, MSGBOX_NPC
	end

Palm202_House2Azumarill::
	lock
	faceplayer
	playmoncry SPECIES_AZUMARILL, CRY_MODE_NORMAL
	msgbox Palm202_House2Azumarill_Text, MSGBOX_DEFAULT
	waitmoncry
	release
	end


Palm201_TextNami:
	.string "NAMI: Okay, nobody goes in the water\n"
	.string "for now! Let's get everyone organized!\p"
	.string "…Oh! You're {PLAYER}, right? NEVARD\n"
	.string "told me about you.\p"
	.string "I'm NAMI, the GYM LEADER here. Sorry,\n"
	.string "the GYM is closed. The tide keeps\l"
	.string "rising, and people need help.\p"
	.string "I love traveling, but this is no\n"
	.string "sightseeing trip.\p"
	.string "The water started rising when that\n"
	.string "TEAM PALM “complex” showed up at sea.\p"
	.string "Those guys put an entire city at risk.$"

Palm201_TextNamiAgain:
	.string "NAMI: Help me keep people away from\n"
	.string "the water, okay?\p"
	.string "The ferry to the complex is suspended.\n"
	.string "I'm working on a way to get out there.$"

Palm201_TextPortLock:
	.string "SAILOR: Sorry! All ferries are\n"
	.string "suspended until the tide calms down.$"

Palm201_TextGymLock:
	.string "The GYM's door is locked.\p"
	.string "A note reads: “Out helping with the\n"
	.string "evacuation. Back soon! - NAMI”$"

Palm201_Sailor_Text:
	.string "I've sailed these waters for thirty\n"
	.string "years. The sea's never felt like this.\p"
	.string "It's like something far away is\n"
	.string "pulling on it.$"

Palm201_Tourist_Text:
	.string "I came here for a beach vacation!\n"
	.string "Now they say the beach might vanish!$"

Palm201_HotelClerk_Text:
	.string "The GRAND HOTEL is closed. We moved\n"
	.string "all our guests to higher ground.$"

Palm201_PortGuard_Text:
	.string "That metal platform out at sea? TEAM\n"
	.string "PALM calls it an “Oceanic Complex.”\p"
	.string "Turbines, tanks, computers… They say\n"
	.string "it makes money. I say it makes waves.$"

Palm201_GymGuard_Text:
	.string "NAMI's GYM has locks, pools and three\n"
	.string "water levels. Wait until you see it!\p"
	.string "…If the tide ever lets her open it.$"

Palm201_Kid_Text:
	.string "The pools at the water park keep\n"
	.string "overflowing by themselves!$"

Palm201_OldWoman_Text:
	.string "In my day, the tide went in and out\n"
	.string "like breathing. Now it only comes in.$"

Palm201_TownSign_Text:
	.string "TIDEMOUTH\n"
	.string "“Where every journey meets the sea.”$"

Palm201_HotelSign_Text:
	.string "TIDEMOUTH GRAND HOTEL\n"
	.string "Temporarily closed.$"

Palm201_PortSign_Text:
	.string "TIDEMOUTH HARBOR\n"
	.string "Ferries suspended until further notice.$"

Palm201_GymSign_Text:
	.string "TIDEMOUTH POKéMON GYM\n"
	.string "LEADER: NAMI\l"
	.string "“Ride the wave, don't fight it.”$"

Palm202_PcOldMan_Text:
	.string "I watched the water climb the pier\n"
	.string "steps from this window. One by one.$"

Palm202_PcGirl_Text:
	.string "NAMI carried my grandma to the\n"
	.string "POKéMON CENTER herself. She's amazing!$"

Palm202_PcWoman_Text:
	.string "NAMI and NEVARD from HARVESTVALE are\n"
	.string "engaged. Did you know?$"

Palm202_MartMan_Text:
	.string "Everyone's buying rain gear and\n"
	.string "POTIONS. Business is booming… sadly.$"

Palm202_MartGent_Text:
	.string "I sold my boat last month. Best\n"
	.string "decision I ever made, it turns out.$"

Palm202_MotelOwner_Text:
	.string "Welcome to the SEASHELL MOTEL!\n"
	.string "We're full of evacuees right now.\p"
	.string "But you can rest here anytime.$"

Palm202_House1Woman_Text:
	.string "I keep my WAILMER in the bathtub\n"
	.string "until the sea calms down.$"

Palm202_House2Man_Text:
	.string "The tide charts make no sense anymore.\n"
	.string "The moon isn't doing this.$"

Palm202_House2Woman_Text:
	.string "We put sandbags at the door. My\n"
	.string "AZUMARILL thinks it's a game.$"

Palm202_House2Azumarill_Text:
	.string "AZUMARILL: Rurill!$"
Palm201_Transition::
	goto_if_unset FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm201_TransEnd
	setweather WEATHER_SUNNY
Palm201_TransEnd::
	end

Palm201_Boat::
	msgbox Palm201_TextBoat, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm201_BoatNo
	warp MAP_PALM_OCEAN_COMPLEX_1F, 10, 26
	waitstate
	releaseall
	end
Palm201_BoatNo::
	applymovement OBJ_EVENT_ID_PLAYER, Palm201_StepBackSouth
	waitmovement 0
	releaseall
	end


Palm201_TextBoat:
	.string "SAILOR: NAMI asked me to take you out\n"
	.string "to that TEAM PALM complex.\p"
	.string "The sea is rough. Ready to go?$"