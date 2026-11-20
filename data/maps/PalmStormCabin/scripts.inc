PalmStormCabin_MapScripts::
	.byte 0

Palm231_Joy::
	lock
	faceplayer
	goto_if_set FLAG_HT_CYNTHIA_DONE, Palm231_JoyAfter
	msgbox Palm231_TextJoy, MSGBOX_DEFAULT
	goto Palm231_Heal
	end

Palm231_JoyAfter::
	msgbox Palm231_TextJoyAfter, MSGBOX_DEFAULT
	goto Palm231_Heal
	end

Palm231_Heal::
	closemessage
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox Palm231_TextHealed, MSGBOX_DEFAULT
	release
	end

Palm231_Chansey::
	lock
	playmoncry SPECIES_CHANSEY, CRY_MODE_NORMAL
	msgbox Palm231_TextChansey, MSGBOX_DEFAULT
	waitmoncry
	release
	end


Palm231_TextJoy:
	.string "JOY: Oh! You came all the way up here?\p"
	.string "The LEAGUE sent me to look after the\n"
	.string "CHAMPIONS' teams.\p"
	.string "The CHAMPION CYNTHIA arrived in very\n"
	.string "bad shape. But now her team is fully\l"
	.string "recovered.\p"
	.string "She's on the last staircase, and she\n"
	.string "asked that no one try to get past her.\p"
	.string "Let me take care of your POKéMON.$"

Palm231_TextJoyAfter:
	.string "JOY: You got past CYNTHIA…\p"
	.string "Then let me make sure your team is\n"
	.string "ready for what's up there.$"

Palm231_TextHealed:
	.string "JOY: Your POKéMON are fully healed.\n"
	.string "Please be careful up there.$"

Palm231_TextChansey:
	.string "CHANSEY: Chaaan-sey!\p"
	.string "It's carrying a basket of clean\n"
	.string "bandages.$"