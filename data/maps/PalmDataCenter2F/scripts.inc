PalmDataCenter2F_MapScripts::
	.byte 0

Palm193_Vega::
	trainerbattle_single TRAINER_PALM_VEGA, Palm193_TextVegaIntro, Palm193_TextVegaLoss
	msgbox Palm193_TextVegaAfter, MSGBOX_DEFAULT
	release
	end

Palm193_Log::
	msgbox Palm193_TextLog, MSGBOX_SIGN
	end

Palm193_Relay1::
	lockall
	goto_if_set FLAG_HT_VOLTARA_RELAY_1, Palm193_RelayOff
	goto_if_not_defeated TRAINER_PALM_VEGA, Palm193_RelayGuarded
	msgbox Palm193_TextRelay, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm193_Release
	setflag FLAG_HT_VOLTARA_RELAY_1
	playse SE_PC_OFF
	waitse
	msgbox Palm193_TextRelayDown, MSGBOX_DEFAULT
	goto Palm193_CheckDone

Palm193_Relay2::
	lockall
	goto_if_set FLAG_HT_VOLTARA_RELAY_2, Palm193_RelayOff
	goto_if_not_defeated TRAINER_PALM_VEGA, Palm193_RelayGuarded
	msgbox Palm193_TextRelay, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm193_Release
	setflag FLAG_HT_VOLTARA_RELAY_2
	playse SE_PC_OFF
	waitse
	msgbox Palm193_TextRelayDown, MSGBOX_DEFAULT
	goto Palm193_CheckDone

Palm193_Relay3::
	lockall
	goto_if_set FLAG_HT_VOLTARA_RELAY_3, Palm193_RelayOff
	goto_if_not_defeated TRAINER_PALM_VEGA, Palm193_RelayGuarded
	msgbox Palm193_TextRelay, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm193_Release
	setflag FLAG_HT_VOLTARA_RELAY_3
	playse SE_PC_OFF
	waitse
	msgbox Palm193_TextRelayDown, MSGBOX_DEFAULT
	goto Palm193_CheckDone

Palm193_CheckDone::
	goto_if_unset FLAG_HT_VOLTARA_RELAY_1, Palm193_Release
	goto_if_unset FLAG_HT_VOLTARA_RELAY_2, Palm193_Release
	goto_if_unset FLAG_HT_VOLTARA_RELAY_3, Palm193_Release
	setflag FLAG_HT_VOLTARA_DONE
	playse SE_SUCCESS
	msgbox Palm193_TextPowerBack, MSGBOX_DEFAULT
	releaseall
	end

Palm193_RelayOff::
	msgbox Palm193_TextRelayIsOff, MSGBOX_DEFAULT
	releaseall
	end

Palm193_RelayGuarded::
	msgbox Palm193_TextRelayGuarded, MSGBOX_DEFAULT
	releaseall
	end

Palm193_Release::
	releaseall
	end


Palm193_TextVegaIntro:
	.string "VEGA: So you're the kid who keeps\n"
	.string "switching off our machines.\p"
	.string "These relays feed every sensor TEAM\n"
	.string "PALM owns. You won't touch them.$"

Palm193_TextVegaLoss:
	.string "…Fine. The data is already backed up.$"

Palm193_TextVegaAfter:
	.string "VEGA: You shut down the terminals,\n"
	.string "but you didn't turn off the source.\p"
	.string "The signal comes from a place nobody\n"
	.string "should be looking at.$"

Palm193_TextRelay:
	.string "A RELAY hums loudly, blinking red.\n"
	.string "Shut it down?$"

Palm193_TextRelayDown:
	.string "The relay went dark.$"

Palm193_TextRelayIsOff:
	.string "This relay is already off.$"

Palm193_TextRelayGuarded:
	.string "VEGA is watching the relays.\n"
	.string "You can't get close!$"

Palm193_TextLog:
	.string "A log file is open on the screen:\p"
	.string "“SENSOR FEED: NORTH…”\n"
	.string "The rest of the file is encrypted.$"

Palm193_TextPowerBack:
	.string "All three relays are dark!\p"
	.string "You hear the city hum back to life\n"
	.string "outside. The power is back!\p"
	.string "HOC will be waiting at his GYM.$"