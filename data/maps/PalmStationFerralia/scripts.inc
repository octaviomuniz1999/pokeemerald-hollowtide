PalmStationFerralia_MapScripts::
	.byte 0

Palm250_FerrClerk::
	lock
	faceplayer
	goto_if_unset FLAG_HT_VOLTARA_DONE, Palm250_Suspended
	msgbox Palm250_TextWelcome, MSGBOX_DEFAULT
	msgbox Palm250_TextAskVolt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm250_GoVolt
	msgbox Palm250_TextAskTrad, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm250_GoTrad
	msgbox Palm250_TextComeAgain, MSGBOX_DEFAULT
	release
	end

Palm250_FerrTraveler::
	msgbox Palm250_TextFerrTraveler, MSGBOX_NPC
	end

Palm250_FerrTraveler2::
	msgbox Palm250_TextFerrTraveler2, MSGBOX_NPC
	end
