PalmVoltara_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm191_Load
	.byte 0

Palm191_Load::
	setmetatile 41, 30, 722, TRUE
	end

Palm191_Hoc::
	lock
	faceplayer
	goto_if_set FLAG_HT_VOLTARA_HOC_MET, Palm191_HocAgain
	msgbox Palm191_TextHoc, MSGBOX_DEFAULT
	setflag FLAG_HT_VOLTARA_HOC_MET
	release
	end

Palm191_HocAgain::
	msgbox Palm191_TextHocAgain, MSGBOX_DEFAULT
	release
	end

Palm191_DataLock::
	goto_if_set FLAG_HT_VOLTARA_HOC_MET, Palm191_Ok
	lockall
	msgbox Palm191_TextDataLock, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm191_StepBackSouth
	waitmovement 0
	releaseall
	end

Palm191_SouthGate::
	goto_if_set FLAG_BADGE07_GET, Palm191_Ok
	lockall
	msgbox Palm191_TextSouthGate, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm191_StepBackNorth
	waitmovement 0
	releaseall
	end

Palm191_Ok::
	end

Palm191_StepBackSouth:
	walk_down
	step_end

Palm191_StepBackNorth:
	walk_up
	step_end

Palm191_Worker::
	lock
	faceplayer
	goto_if_set FLAG_HT_VOLTARA_DONE, Palm191_WorkerDone
	msgbox Palm191_Worker_Text, MSGBOX_DEFAULT
	release
	end

Palm191_WorkerDone::
	msgbox Palm191_Worker_TextDone, MSGBOX_DEFAULT
	release
	end

Palm191_Scientist::
	msgbox Palm191_Scientist_Text, MSGBOX_NPC
	end

Palm191_Girl::
	msgbox Palm191_Girl_Text, MSGBOX_NPC
	end

Palm191_DoorGrunt::
	msgbox Palm191_DoorGrunt_Text, MSGBOX_NPC
	end

Palm191_SouthGuard::
	msgbox Palm191_SouthGuard_Text, MSGBOX_NPC
	end

Palm191_OldMan::
	msgbox Palm191_OldMan_Text, MSGBOX_NPC
	end

Palm191_TownSign::
	msgbox Palm191_TownSign_Text, MSGBOX_SIGN
	end

Palm191_StationSign::
	msgbox Palm191_StationSign_Text, MSGBOX_SIGN
	end

Palm191_DataSign::
	msgbox Palm191_DataSign_Text, MSGBOX_SIGN
	end

Palm191_GymSign::
	msgbox Palm191_GymSign_Text, MSGBOX_SIGN
	end

Palm192_PcWoman1::
	msgbox Palm192_PcWoman1_Text, MSGBOX_NPC
	end

Palm192_PcWoman2::
	msgbox Palm192_PcWoman2_Text, MSGBOX_NPC
	end

Palm192_PcBoy::
	msgbox Palm192_PcBoy_Text, MSGBOX_NPC
	end

Palm192_MartExpert::
	msgbox Palm192_MartExpert_Text, MSGBOX_NPC
	end

Palm192_MartMan::
	msgbox Palm192_MartMan_Text, MSGBOX_NPC
	end

Palm192_House1Man::
	msgbox Palm192_House1Man_Text, MSGBOX_NPC
	end

Palm192_House2Woman::
	msgbox Palm192_House2Woman_Text, MSGBOX_NPC
	end


Palm191_TextHoc:
	.string "HOC: Hey, you made it through the\n"
	.string "dark! Welcome to VOLTARA.\p"
	.string "The network went down again. And this\n"
	.string "system is older than I am…\p"
	.string "If DU were here, he'd have called me\n"
	.string "“grandpa” three times by now.\p"
	.string "…Sorry. I'm HOC, the GYM LEADER.\n"
	.string "Jay told me all about you.\p"
	.string "RIVEN found a pattern in the logs.\n"
	.string "The problem isn't just the plant.\p"
	.string "It's like something is answering\n"
	.string "from very far away.\p"
	.string "TEAM PALM has a DATA CENTER in town.\n"
	.string "Their relays are draining the grid.\p"
	.string "Go shut them down, {PLAYER}. I'll keep\n"
	.string "the station running on backup power.$"

Palm191_TextHocAgain:
	.string "HOC: The DATA CENTER is the big\n"
	.string "building to the east.\p"
	.string "Shut down their relays and the city\n"
	.string "gets its power back!$"

Palm191_TextDataLock:
	.string "A TEAM PALM GRUNT blocks the door.\p"
	.string "GRUNT: Private property! Nobody gets\n"
	.string "in without clearance.$"

Palm191_TextSouthGate:
	.string "The road south is closed.\p"
	.string "GUARD: Sorry, kid. Only trainers with\n"
	.string "VOLTARA's GYM BADGE may pass.$"

Palm191_Worker_Text:
	.string "The trains stopped when the power\n"
	.string "went out. The whole line is frozen.$"

Palm191_Worker_TextDone:
	.string "Power's back! The trains to FERRALIA\n"
	.string "and TRADEPOST can run again!$"

Palm191_Scientist_Text:
	.string "Every terminal in town shows the same\n"
	.string "error: “UPLINK BUSY.”\p"
	.string "Busy with what? We aren't sending\n"
	.string "anything…$"

Palm191_Girl_Text:
	.string "The streetlights blink at night,\n"
	.string "like they're trying to talk!$"

Palm191_DoorGrunt_Text:
	.string "GRUNT: Move along! This is a TEAM\n"
	.string "PALM facility.$"

Palm191_SouthGuard_Text:
	.string "The road south leads to the sea and\n"
	.string "the CITY OF TIDES.\p"
	.string "Only trainers with VOLTARA's BADGE\n"
	.string "may pass.$"

Palm191_OldMan_Text:
	.string "I helped build the first power line\n"
	.string "here, fifty years ago.\p"
	.string "It never hummed like it does now.$"

Palm191_TownSign_Text:
	.string "VOLTARA\n"
	.string "“The city that never sleeps.”$"

Palm191_StationSign_Text:
	.string "VOLTARA STATION\n"
	.string "Lines to FERRALIA and TRADEPOST.$"

Palm191_DataSign_Text:
	.string "TEAM PALM DATA CENTER\n"
	.string "Authorized personnel only.$"

Palm191_GymSign_Text:
	.string "VOLTARA POKéMON GYM\n"
	.string "LEADER: HOC\l"
	.string "“The circuit that never breaks.”$"

Palm192_PcWoman1_Text:
	.string "The POKéMON CENTER has its own\n"
	.string "generator. Thank goodness!$"

Palm192_PcWoman2_Text:
	.string "I came by train from FERRALIA. Now\n"
	.string "I'm stuck here until the power's back.$"

Palm192_PcBoy_Text:
	.string "My ROTOM keeps escaping into the\n"
	.string "outlets! It loves this city.$"

Palm192_MartExpert_Text:
	.string "Batteries? Sold out. Flashlights?\n"
	.string "Sold out. Everyone's buying them.$"

Palm192_MartMan_Text:
	.string "They say TEAM PALM's building never\n"
	.string "loses power. Funny, isn't it?$"

Palm192_House1Man_Text:
	.string "I fix old computers for a living.\n"
	.string "HOC is the best programmer I know.\p"
	.string "He's getting married to JAY from\n"
	.string "BREEZEPORT, you know!$"

Palm192_House2Woman_Text:
	.string "My fridge has been off for two days.\n"
	.string "I hope this ends soon…$"