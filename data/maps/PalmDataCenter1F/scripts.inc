PalmDataCenter1F_MapScripts::
	.byte 0

Palm193_Screen::
	msgbox Palm193_TextScreen, MSGBOX_SIGN
	end

Palm193_Grunt1::
	trainerbattle_single TRAINER_PALM_DATA_GRUNT_1, Palm193_TextGrunt1Intro, Palm193_TextGrunt1Loss
	msgbox Palm193_TextGrunt1After, MSGBOX_AUTOCLOSE
	end

Palm193_Grunt2::
	trainerbattle_single TRAINER_PALM_DATA_GRUNT_2, Palm193_TextGrunt2Intro, Palm193_TextGrunt2Loss
	msgbox Palm193_TextGrunt2After, MSGBOX_AUTOCLOSE
	end


Palm193_TextScreen:
	.string "The screen scrolls endless lines of\n"
	.string "numbers. “RELAY LOAD: 100%”.$"

Palm193_TextGrunt1Intro:
	.string "How did you get in here?\n"
	.string "The relays are classified!$"

Palm193_TextGrunt1Loss:
	.string "Short-circuited…$"

Palm193_TextGrunt1After:
	.string "VEGA is upstairs with the relays.\n"
	.string "He won't be as easy as me!$"

Palm193_TextGrunt2Intro:
	.string "These machines mine data and coins\n"
	.string "all day. And you won't stop them!$"

Palm193_TextGrunt2Loss:
	.string "Error… Error…$"

Palm193_TextGrunt2After:
	.string "Fine. Go upstairs. VEGA will deal\n"
	.string "with you.$"