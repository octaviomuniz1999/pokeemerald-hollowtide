PalmStationVoltara_MapScripts::
	.byte 0

Palm250_VoltClerk::
	lock
	faceplayer
	goto_if_unset FLAG_HT_VOLTARA_DONE, Palm250_Suspended
	msgbox Palm250_TextWelcome, MSGBOX_DEFAULT
	msgbox Palm250_TextAskFerr, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm250_GoFerr
	msgbox Palm250_TextAskTrad, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm250_GoTrad
	msgbox Palm250_TextComeAgain, MSGBOX_DEFAULT
	release
	end

Palm250_VoltTraveler::
	msgbox Palm250_TextVoltTraveler, MSGBOX_NPC
	end

Palm250_VoltTraveler2::
	msgbox Palm250_TextVoltTraveler2, MSGBOX_NPC
	end

Palm250_Suspended::
	msgbox Palm250_TextSuspended, MSGBOX_DEFAULT
	release
	end

Palm250_Staff::
	msgbox Palm250_TextStaff, MSGBOX_NPC
	end

Palm250_TextAllAboard::
	msgbox Palm250_TextBoard, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	playse SE_TRUCK_MOVE
	delay 60
	playse SE_DING_DONG
	waitse
	delay 40
	return

Palm250_GoVolt::
	call Palm250_TextAllAboard
	warpsilent MAP_PALM_STATION_VOLTARA, 5, 7
	waitstate
	release
	end

Palm250_GoFerr::
	call Palm250_TextAllAboard
	warpsilent MAP_PALM_STATION_FERRALIA, 5, 7
	waitstate
	release
	end

Palm250_GoTrad::
	call Palm250_TextAllAboard
	warpsilent MAP_PALM_STATION_TRADEPOST, 5, 7
	waitstate
	release
	end


Palm250_TextSuspended:
	.string "Welcome to the LUNIA RAILWAY.\p"
	.string "I'm sorry, all trains are suspended.\n"
	.string "The whole line lost power when\l"
	.string "VOLTARA went dark.$"

Palm250_TextWelcome:
	.string "Welcome to the LUNIA RAILWAY!\n"
	.string "The line is running again.$"

Palm250_TextAskVolt:
	.string "Would you like to take the train\n"
	.string "to VOLTARA?$"

Palm250_TextAskFerr:
	.string "Would you like to take the train\n"
	.string "to FERRALIA?$"

Palm250_TextAskTrad:
	.string "Would you like to take the train\n"
	.string "to TRADEPOST?$"

Palm250_TextComeAgain:
	.string "Please come again!$"

Palm250_TextBoard:
	.string "All aboard! Please mind the gap.$"

Palm250_TextStaff:
	.string "Sorry, the platforms are for staff\n"
	.string "and passengers with tickets only.$"

Palm250_TextVoltTraveler:
	.string "I came to VOLTARA for the GYM, but\n"
	.string "I'm staying for the trains. Fast!$"

Palm250_TextVoltTraveler2:
	.string "The station clock stopped during the\n"
	.string "blackout. Nobody has fixed it yet.$"

Palm250_TextFerrTraveler:
	.string "This used to be the railway company's\n"
	.string "head office. Now it's the station too.$"

Palm250_TextFerrTraveler2:
	.string "FERRALIA, TRADEPOST, VOLTARA…\n"
	.string "I commute between all three!$"

Palm250_TextTradTraveler:
	.string "Merchants ship everything by train.\n"
	.string "When the line stopped, prices went up.$"

Palm250_TextTradTraveler2:
	.string "I'm taking the train to FERRALIA to\n"
	.string "see the towers on the big avenue.$"