PalmStationTradepost_MapScripts::
	.byte 0

Palm250_TradClerk::
	lock
	faceplayer
	goto_if_unset FLAG_HT_VOLTARA_DONE, Palm250_Suspended
	msgbox Palm250_TextWelcome, MSGBOX_DEFAULT
	msgbox Palm250_TextAskVolt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm250_GoVolt
	msgbox Palm250_TextAskFerr, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm250_GoFerr
	msgbox Palm250_TextComeAgain, MSGBOX_DEFAULT
	release
	end

Palm250_TradTraveler::
	msgbox Palm250_TextTradTraveler, MSGBOX_NPC
	end

Palm250_TradTraveler2::
	msgbox Palm250_TextTradTraveler2, MSGBOX_NPC
	end
