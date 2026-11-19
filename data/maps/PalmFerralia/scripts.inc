PalmFerralia_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm102_FerraliaLoad
	.byte 0

Palm102_FerraliaLoad::
	call_if_unset FLAG_HT_FERRALIA_CARGO_DONE, Palm102_LockGym
	end

Palm102_LockGym::
	setmetatile 49, 12, 722, TRUE
	return

Palm102_UnlockGym::
	setmetatile 49, 12, 461, TRUE
	special DrawWholeMapView
	return

Palm102_VesselYard::
	lock
	faceplayer
	goto_if_not_defeated TRAINER_PALM_YARD_GRUNT_1, Palm102_VesselAsk
	goto_if_not_defeated TRAINER_PALM_YARD_GRUNT_2, Palm102_VesselAsk
	msgbox Palm102_TextVesselThanks, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	setflag FLAG_HT_FERRALIA_CARGO_DONE
	removeobject 9
	removeobject 10
	removeobject 11
	call Palm102_UnlockGym
	fadescreen FADE_FROM_BLACK
	msgbox Palm102_TextVesselLeft, MSGBOX_DEFAULT
	release
	end

Palm102_VesselAsk::
	msgbox Palm102_TextVesselAsk, MSGBOX_DEFAULT
	release
	end

Palm102_YardGrunt1::
	trainerbattle_single TRAINER_PALM_YARD_GRUNT_1, Palm102_TextGrunt1Intro, Palm102_TextGrunt1Defeat
	msgbox Palm102_TextGrunt1After, MSGBOX_AUTOCLOSE
	end

Palm102_YardGrunt2::
	trainerbattle_single TRAINER_PALM_YARD_GRUNT_2, Palm102_TextGrunt2Intro, Palm102_TextGrunt2Defeat
	msgbox Palm102_TextGrunt2After, MSGBOX_AUTOCLOSE
	end

Palm101_GymFan::
	goto_if_set FLAG_HT_FERRALIA_CARGO_DONE, Palm101_GymFanOpen
	msgbox Palm101_GymFan_Text, MSGBOX_NPC
	end

Palm101_GymFanOpen::
	msgbox Palm101_GymFanOpen_Text, MSGBOX_NPC
	end

Palm101_Greeter::
	msgbox Palm101_Greeter_Text, MSGBOX_NPC
	end

Palm101_YardWorker::
	msgbox Palm101_YardWorker_Text, MSGBOX_NPC
	end

Palm101_FountainKid::
	msgbox Palm101_FountainKid_Text, MSGBOX_NPC
	end

Palm101_Commuter::
	msgbox Palm101_Commuter_Text, MSGBOX_NPC
	end

Palm101_Resident::
	msgbox Palm101_Resident_Text, MSGBOX_NPC
	end

Palm101_HQGuard::
	msgbox Palm101_HQGuard_Text, MSGBOX_NPC
	end

Palm101_ParkLady::
	msgbox Palm101_ParkLady_Text, MSGBOX_NPC
	end

Palm101_CitySign::
	msgbox Palm101_CitySign_Text, MSGBOX_SIGN
	end

Palm101_GymSign::
	msgbox Palm101_GymSign_Text, MSGBOX_SIGN
	end

Palm101_HQSign::
	msgbox Palm101_HQSign_Text, MSGBOX_SIGN
	end

Palm101_YardSign::
	msgbox Palm101_YardSign_Text, MSGBOX_SIGN
	end

Palm101_Route4Sign::
	msgbox Palm101_Route4Sign_Text, MSGBOX_SIGN
	end


Palm101_Greeter_Text:
	.string "Welcome to FERRALIA! Steel, trains\n"
	.string "and a million hurried footsteps.\p"
	.string "Stay on the sidewalks. Nobody here\n"
	.string "stops walking, not even for you!$"

Palm101_YardWorker_Text:
	.string "Before the whistle, you can hear\n"
	.string "the rails sing.\p"
	.string "Lately TEAM PALM only unloads its\n"
	.string "cargo after dark. Funny, huh?$"

Palm101_GymFan_Text:
	.string "The GYM is locked today. VESSEL went\n"
	.string "to the rail yard at dawn.\p"
	.string "Something about a shipment that\n"
	.string "never arrived...$"

Palm101_FountainKid_Text:
	.string "My dad says the fountain water\n"
	.string "comes all the way from the coast.\p"
	.string "Is that why it tastes salty?$"

Palm101_Commuter_Text:
	.string "Late again! The east line was\n"
	.string "closed for “inspection” all week.$"

Palm101_Resident_Text:
	.string "I moved here from HARVESTVALE.\n"
	.string "The city is loud, but the jobs\p"
	.string "are here. I miss the coffee\n"
	.string "fields, though.$"

Palm101_HQGuard_Text:
	.string "FERRALIA RAIL & STEEL headquarters.\n"
	.string "Staff only, I'm afraid.$"

Palm101_GymFanOpen_Text:
	.string "VESSEL is back! Word is a young\n"
	.string "trainer helped him at the yard.\p"
	.string "Was that you? Go get that BADGE!$"

Palm102_TextVesselAsk:
	.string "You there! I'm VESSEL, this city's\n"
	.string "GYM LEADER.\p"
	.string "A whole shipment of steel pipe\n"
	.string "vanished from my yard last night.\p"
	.string "Those TEAM PALM goons are loading\n"
	.string "it onto their own cars right now!\p"
	.string "I can't leave the gates. Can you\n"
	.string "stop them for me?$"

Palm102_TextVesselThanks:
	.string "You did it! The pipes are safe.\p"
	.string "They were going to lay them along\n"
	.string "the coast to pump the springs dry\l"
	.string "and sell the water back to us...\p"
	.string "That's TEAM PALM for you.\n"
	.string "Thank you, really.\p"
	.string "Come to the GYM. I'll give you the\n"
	.string "toughest battle this city has!$"

Palm102_TextVesselLeft:
	.string "VESSEL headed back to the GYM.$"

Palm102_TextGrunt1Intro:
	.string "Hey! This cargo's been reassigned\n"
	.string "to TEAM PALM. Beat it, kid!$"

Palm102_TextGrunt1Defeat:
	.string "The boss is gonna flip...$"

Palm102_TextGrunt1After:
	.string "Fine! Keep your rusty pipes!$"

Palm102_TextGrunt2Intro:
	.string "Water belongs to whoever owns the\n"
	.string "pipes. And we'll own them all!$"

Palm102_TextGrunt2Defeat:
	.string "Our schedule is ruined!$"

Palm102_TextGrunt2After:
	.string "Mark my words: the tide is turning\n"
	.string "TEAM PALM's way.$"

Palm101_ParkLady_Text:
	.string "This park is the city's lung.\n"
	.string "I walk here every morning.\p"
	.string "The grass is full of POKéMON that\n"
	.string "moved in from the SERRA.$"

Palm101_CitySign_Text:
	.string "FERRALIA CITY\n"
	.string "The heart of steel and rail.$"

Palm101_GymSign_Text:
	.string "FERRALIA CITY POKéMON GYM\n"
	.string "LEADER: VESSEL\p"
	.string "“The steel that sings!”$"

Palm101_HQSign_Text:
	.string "FERRALIA RAIL & STEEL\n"
	.string "Headquarters$"

Palm101_YardSign_Text:
	.string "FERRALIA CARGO YARD\n"
	.string "Authorized personnel only.$"

Palm101_Route4Sign_Text:
	.string "EAST LINE - ROUTE 4\n"
	.string "Closed for cargo inspection.$"