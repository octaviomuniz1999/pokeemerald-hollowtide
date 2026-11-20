PalmHorizon_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm170_Load
	.byte 0

Palm170_Load::
	goto_if_set FLAG_HT_HORIZON_DONE, Palm170_LoadDone
	setmetatile 39, 29, 738, TRUE
	setmetatile 13, 18, 184, TRUE
	setmetatile 14, 18, 161, TRUE
	setmetatile 15, 18, 161, TRUE
	setmetatile 16, 18, 161, TRUE
	setmetatile 17, 18, 161, TRUE
	setmetatile 18, 18, 161, TRUE
	setmetatile 19, 18, 161, TRUE
	setmetatile 20, 18, 161, TRUE
	setmetatile 21, 18, 161, TRUE
	setmetatile 22, 18, 161, TRUE
	setmetatile 23, 18, 161, TRUE
	setmetatile 24, 18, 161, TRUE
	setmetatile 25, 18, 161, TRUE
	setmetatile 26, 18, 161, TRUE
	setmetatile 27, 18, 161, TRUE
	setmetatile 28, 18, 161, TRUE
	setmetatile 29, 18, 161, TRUE
	setmetatile 30, 18, 161, TRUE
	setmetatile 31, 18, 161, TRUE
	setmetatile 32, 18, 161, TRUE
	setmetatile 33, 18, 161, TRUE
	setmetatile 34, 18, 161, TRUE
	setmetatile 35, 18, 161, TRUE
	setmetatile 36, 18, 161, TRUE
	setmetatile 37, 18, 186, TRUE
	setmetatile 13, 19, 184, TRUE
	setmetatile 14, 19, 161, TRUE
	setmetatile 15, 19, 161, TRUE
	setmetatile 16, 19, 161, TRUE
	setmetatile 17, 19, 161, TRUE
	setmetatile 18, 19, 161, TRUE
	setmetatile 19, 19, 161, TRUE
	setmetatile 20, 19, 161, TRUE
	setmetatile 21, 19, 161, TRUE
	setmetatile 22, 19, 161, TRUE
	setmetatile 23, 19, 161, TRUE
	setmetatile 24, 19, 161, TRUE
	setmetatile 25, 19, 161, TRUE
	setmetatile 26, 19, 161, TRUE
	setmetatile 27, 19, 161, TRUE
	setmetatile 28, 19, 161, TRUE
	setmetatile 29, 19, 161, TRUE
	setmetatile 30, 19, 161, TRUE
	setmetatile 31, 19, 161, TRUE
	setmetatile 32, 19, 161, TRUE
	setmetatile 33, 19, 161, TRUE
	setmetatile 34, 19, 161, TRUE
	setmetatile 35, 19, 161, TRUE
	setmetatile 36, 19, 161, TRUE
	setmetatile 37, 19, 186, TRUE
	setmetatile 14, 20, 555, FALSE
	setmetatile 17, 20, 555, FALSE
	setmetatile 20, 20, 555, FALSE
	setmetatile 23, 20, 555, FALSE
	setmetatile 26, 20, 555, FALSE
	setmetatile 29, 20, 555, FALSE
	setmetatile 32, 20, 555, FALSE
	setmetatile 35, 20, 555, FALSE
	end

Palm170_LoadDone::
	end

Palm170_Chelsia::
	lockall
	applymovement 1, Common_Movement_FacePlayer
	waitmovement 0
	msgbox Palm170_TextChelsia1, MSGBOX_DEFAULT
	applymovement 2, Palm170_PiplupPoint
	waitmovement 0
	playmoncry SPECIES_PIPLUP, CRY_MODE_NORMAL
	msgbox Palm170_TextPiplupPoints, MSGBOX_DEFAULT
	waitmoncry
	msgbox Palm170_TextChelsia2, MSGBOX_DEFAULT
	setflag FLAG_HT_HORIZON_CHELSIA_MET
	fadescreen FADE_TO_BLACK
	removeobject 1
	removeobject 2
	fadescreen FADE_FROM_BLACK
	releaseall
	end

Palm170_PiplupPoint:
	face_left
	delay_16
	jump_in_place_left
	step_end

Palm170_Piplup::
	lock
	faceplayer
	playmoncry SPECIES_PIPLUP, CRY_MODE_NORMAL
	msgbox Palm170_TextPiplup, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Palm170_StationLock::
	goto_if_set FLAG_HT_HORIZON_CHELSIA_MET, Palm170_StationOk
	lockall
	msgbox Palm170_TextStationLocked, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm170_StepBackSouth
	waitmovement 0
	releaseall
	end

Palm170_StationOk::
	end

Palm170_NorthGate::
	goto_if_set FLAG_BADGE06_GET, Palm170_StationOk
	lockall
	msgbox Palm170_TextNorthGate, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm170_StepBackSouth
	waitmovement 0
	releaseall
	end

Palm170_StepBackSouth:
	walk_down
	step_end

Palm170_OldMan::
	lock
	faceplayer
	goto_if_set FLAG_HT_HORIZON_DONE, Palm170_OldManDone
	msgbox Palm170_OldMan_Text, MSGBOX_DEFAULT
	release
	end

Palm170_OldManDone::
	msgbox Palm170_OldMan_TextDone, MSGBOX_DEFAULT
	release
	end

Palm170_GymGuard::
	lock
	faceplayer
	goto_if_set FLAG_HT_HORIZON_DONE, Palm170_GymGuardDone
	msgbox Palm170_GymGuard_Text, MSGBOX_DEFAULT
	release
	end

Palm170_GymGuardDone::
	msgbox Palm170_GymGuard_TextDone, MSGBOX_DEFAULT
	release
	end

Palm170_Fisher::
	msgbox Palm170_Fisher_Text, MSGBOX_NPC
	end

Palm170_Astronomer::
	msgbox Palm170_Astronomer_Text, MSGBOX_NPC
	end

Palm170_Girl::
	msgbox Palm170_Girl_Text, MSGBOX_NPC
	end

Palm170_Worker::
	msgbox Palm170_Worker_Text, MSGBOX_NPC
	end

Palm170_Woman::
	msgbox Palm170_Woman_Text, MSGBOX_NPC
	end

Palm170_TownSign::
	msgbox Palm170_TownSign_Text, MSGBOX_SIGN
	end

Palm170_StationSign::
	msgbox Palm170_StationSign_Text, MSGBOX_SIGN
	end

Palm170_PavilionSign::
	msgbox Palm170_PavilionSign_Text, MSGBOX_SIGN
	end

Palm170_GymSign::
	msgbox Palm170_GymSign_Text, MSGBOX_SIGN
	end

Palm171_PcWoman::
	msgbox Palm171_PcWoman_Text, MSGBOX_NPC
	end

Palm171_PcGirl::
	msgbox Palm171_PcGirl_Text, MSGBOX_NPC
	end

Palm171_MartWoman::
	msgbox Palm171_MartWoman_Text, MSGBOX_NPC
	end

Palm171_MartBoy::
	msgbox Palm171_MartBoy_Text, MSGBOX_NPC
	end

Palm171_MartSailor::
	msgbox Palm171_MartSailor_Text, MSGBOX_NPC
	end

Palm171_House1Man::
	msgbox Palm171_House1Man_Text, MSGBOX_NPC
	end

Palm171_House1Woman::
	msgbox Palm171_House1Woman_Text, MSGBOX_NPC
	end

Palm171_House3Woman::
	msgbox Palm171_House3Woman_Text, MSGBOX_NPC
	end

Palm171_House3Boy::
	msgbox Palm171_House3Boy_Text, MSGBOX_NPC
	end

Palm171_House3Skitty::
	lock
	faceplayer
	playmoncry SPECIES_SKITTY, CRY_MODE_NORMAL
	msgbox Palm171_House3Skitty_Text, MSGBOX_DEFAULT
	waitmoncry
	release
	end


Palm170_TextChelsia1:
	.string "…Oh! Sorry, I didn't see you there.\p"
	.string "I'm CHELSIA, the GYM LEADER here.\n"
	.string "And this is PIPLUP, my partner.\p"
	.string "I don't understand it… Yesterday\n"
	.string "the lake was below the garden steps.\p"
	.string "Now the water has covered the whole\n"
	.string "garden. And it hasn't rained at all!$"

Palm170_TextPiplupPoints:
	.string "PIPLUP: Pip! Piplup!\p"
	.string "PIPLUP is pointing at the LAKE\n"
	.string "CONTROL STATION.$"

Palm170_TextChelsia2:
	.string "CHELSIA: The station? It controls the\n"
	.string "floodgates… and it goes under the lake.\p"
	.string "You want us to go that way, PIPLUP?\n"
	.string "Very well! Let's go together!\p"
	.string "{PLAYER}, would you come with us?\n"
	.string "I'll open the station door for you.$"

Palm170_TextPiplup:
	.string "PIPLUP: Piplup! Pip!$"

Palm170_TextStationLocked:
	.string "The door is locked.\p"
	.string "HORIZON LAKE CONTROL STATION\n"
	.string "Staff only.$"

Palm170_TextNorthGate:
	.string "The mountain road north is closed.\p"
	.string "A sign reads: “ROUTE 8 · Closed\n"
	.string "until the lake is safe again.”$"

Palm170_OldMan_Text:
	.string "Seventy years I've lived by this lake.\p"
	.string "It rises in the rainy season, sure.\n"
	.string "But not like this. Not in clear skies.$"

Palm170_OldMan_TextDone:
	.string "The water went back down overnight!\p"
	.string "The lake breathes slow and calm again.\n"
	.string "Thank you, young one.$"

Palm170_Fisher_Text:
	.string "The fish are swimming in circles,\n"
	.string "all facing the same way.\p"
	.string "As if something under the water was\n"
	.string "calling them.$"

Palm170_Astronomer_Text:
	.string "I study the stars at the STAR\n"
	.string "PAVILION.\p"
	.string "On still nights, the lake reflects\n"
	.string "every constellation. This town was\l"
	.string "named for that horizon.\p"
	.string "Lately the water trembles, and the\n"
	.string "reflection breaks apart.$"

Palm170_Girl_Text:
	.string "CHELSIA's PIPLUP walks behind her\n"
	.string "everywhere she goes!\p"
	.string "I want a partner just like that.$"

Palm170_Worker_Text:
	.string "I work at the lake station, but my\n"
	.string "key card stopped working yesterday.\p"
	.string "Some people in green uniforms said\n"
	.string "they were doing “maintenance”…$"

Palm170_Woman_Text:
	.string "My garden was by the lake.\n"
	.string "Now the fish live in it.$"

Palm170_GymGuard_Text:
	.string "CHELSIA's GYM is closed today.\p"
	.string "She's worried about the lake. She\n"
	.string "won't battle until it's settled.$"

Palm170_GymGuard_TextDone:
	.string "The lake is calm again, and CHELSIA's\n"
	.string "GYM is open!\p"
	.string "She's waiting for you inside.$"

Palm170_TownSign_Text:
	.string "HORIZON CITY\n"
	.string "“Where the sky rests on the water.”$"

Palm170_StationSign_Text:
	.string "HORIZON LAKE CONTROL STATION\n"
	.string "Floodgates · Underwater lab$"

Palm170_PavilionSign_Text:
	.string "STAR PAVILION\n"
	.string "Closed while the lake is rising.$"

Palm170_GymSign_Text:
	.string "HORIZON CITY POKéMON GYM\n"
	.string "LEADER: CHELSIA\l"
	.string "“A little light to find the way.”$"

Palm171_PcWoman_Text:
	.string "Travelers from SERENIA always stop\n"
	.string "here to watch the sunset on the lake.$"

Palm171_PcGirl_Text:
	.string "My MARILL won't go near the water.\n"
	.string "It keeps hiding under my bed!$"

Palm171_MartWoman_Text:
	.string "Everyone's buying REPELS and ROPES.\n"
	.string "They say the lake might flood the town.$"

Palm171_MartBoy_Text:
	.string "I'm saving up for a fishing rod.\n"
	.string "FEEBAS live in this lake, you know!$"

Palm171_MartSailor_Text:
	.string "I sail the lake ferry. Well… I did,\n"
	.string "until the water got this strange.$"

Palm171_House1Man_Text:
	.string "The lake has ups and downs, like the\n"
	.string "moon has phases. That's normal.\p"
	.string "But now it rises without the moon,\n"
	.string "without the rain. That's not normal.$"

Palm171_House1Woman_Text:
	.string "We moved our things upstairs, just\n"
	.string "in case. I hope we never need to.$"

Palm171_House3Woman_Text:
	.string "My brother says the lake is angry.\n"
	.string "I think it's just… scared.$"

Palm171_House3Boy_Text:
	.string "I saw lights under the water at night!\n"
	.string "Blue blinking lights. Like machines!$"

Palm171_House3Skitty_Text:
	.string "SKITTY: Mew?$"
Palm260_PavilionClosed::
	goto_if_set FLAG_HT_HORIZON_DONE, Palm260_End
	lockall
	msgbox Palm260_TextClosed, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, Palm260_StepBack
	waitmovement 0
	releaseall
	end

Palm260_StepBack:
	walk_down
	step_end

Palm260_PavilionSign::
	goto_if_set FLAG_HT_HORIZON_DONE, Palm260_PavilionSignOpen
	msgbox Palm170_PavilionSign_Text, MSGBOX_SIGN
	end

Palm260_PavilionSignOpen::
	msgbox Palm260_TextSignOpen, MSGBOX_SIGN
	end

Palm260_End::
	end


Palm260_TextClosed:
	.string "The doors are locked. A note says:\n"
	.string "“Closed while the lake is rising.”$"

Palm260_TextSignOpen:
	.string "STAR PAVILION\n"
	.string "“The constellations of LUNIA.”$"