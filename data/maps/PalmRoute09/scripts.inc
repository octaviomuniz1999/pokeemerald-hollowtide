PalmRoute09_MapScripts::
	.byte 0

Palm190_EastGate::
	goto_if_set FLAG_HT_PASSWAY_EAST_OPEN, Palm190_Ok
	lockall
	msgbox Palm190_TextEastGate, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm190_StepBackWest
	waitmovement 0
	releaseall
	end

Palm190_Ok::
	end

Palm190_StepBackWest:
	walk_left
	step_end

Palm190_RouteJOSEPH::
	trainerbattle_single TRAINER_PALM_ROUTE09_JOSEPH, Palm190_TextJOSEPHIntro, Palm190_TextJOSEPHLoss
	msgbox Palm190_TextJOSEPHAfter, MSGBOX_AUTOCLOSE
	end

Palm190_RouteDREW::
	trainerbattle_single TRAINER_PALM_ROUTE09_DREW, Palm190_TextDREWIntro, Palm190_TextDREWLoss
	msgbox Palm190_TextDREWAfter, MSGBOX_AUTOCLOSE
	end

Palm190_RouteHEIDI::
	trainerbattle_single TRAINER_PALM_ROUTE09_HEIDI, Palm190_TextHEIDIIntro, Palm190_TextHEIDILoss
	msgbox Palm190_TextHEIDIAfter, MSGBOX_AUTOCLOSE
	end

Palm190_RouteFABIAN::
	trainerbattle_single TRAINER_PALM_ROUTE09_FABIAN, Palm190_TextFABIANIntro, Palm190_TextFABIANLoss
	msgbox Palm190_TextFABIANAfter, MSGBOX_AUTOCLOSE
	end

Palm190_SignWest::
	msgbox Palm190_SignWest_Text, MSGBOX_SIGN
	end

Palm190_SignEast::
	msgbox Palm190_SignEast_Text, MSGBOX_SIGN
	end

Palm190_SignStation::
	msgbox Palm190_SignStation_Text, MSGBOX_SIGN
	end


Palm190_TextEastGate:
	.string "The city gate of VOLTARA is shut.\n"
	.string "The lights on the panel are dead.\p"
	.string "A note reads: “POWER OUTAGE.\n"
	.string "The gate will reopen soon.”$"

Palm190_TextJOSEPHIntro:
	.string "My amp runs on ELECTRIC POKéMON!\n"
	.string "Let me play you a shocking solo!$"

Palm190_TextJOSEPHLoss:
	.string "That was a broken string…$"

Palm190_TextJOSEPHAfter:
	.string "The power lines buzz louder near\n"
	.string "VOLTARA. Like the whole city hums.$"

Palm190_TextDREWIntro:
	.string "I'm camping by the tracks to watch\n"
	.string "the trains. But none have come by!$"

Palm190_TextDREWLoss:
	.string "No trains, and now no wins either…$"

Palm190_TextDREWAfter:
	.string "The trains stopped running when the\n"
	.string "network in VOLTARA went down.$"

Palm190_TextHEIDIIntro:
	.string "My POKéMON love the static in the\n"
	.string "air here! Want a little zap?$"

Palm190_TextHEIDILoss:
	.string "My hair is standing straight up!$"

Palm190_TextHEIDIAfter:
	.string "HELIOPTILE soak up sunlight to make\n"
	.string "electricity. Isn't that clever?$"

Palm190_TextFABIANIntro:
	.string "The station staff ran off when the\n"
	.string "power died. I'm still here, though!$"

Palm190_TextFABIANLoss:
	.string "Power down. Total blackout.$"

Palm190_TextFABIANAfter:
	.string "Some guys in green uniforms keep\n"
	.string "going in and out of VOLTARA.\p"
	.string "Funny. Everyone else got stuck\n"
	.string "outside because of the outage.$"

Palm190_SignWest_Text:
	.string "ROUTE 9 · IRON CORRIDOR\n"
	.string "West: PASSWAY VILLAGE$"

Palm190_SignEast_Text:
	.string "ROUTE 9\n"
	.string "East: VOLTARA$"

Palm190_SignStation_Text:
	.string "ROUTE 9 POWER SUBSTATION\n"
	.string "Danger! High voltage!\l"
	.string "Authorized staff only.$"
Palm190_SubstationDoor::
	msgbox Palm190_TextSubstationDoor, MSGBOX_SIGN
	end


Palm190_TextSubstationDoor:
	.string "The door is locked tight.\p"
	.string "A low hum comes from the machines\n"
	.string "inside.$"