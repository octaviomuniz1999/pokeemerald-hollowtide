PalmOceanComplexCore_MapScripts::
	.byte 0

Palm204_Abelf::
	trainerbattle_single TRAINER_PALM_ABELF, Palm204_TextAbelfIntro, Palm204_TextAbelfLoss, Palm204_AbelfDefeated
	msgbox Palm204_TextAbelfAfter, MSGBOX_DEFAULT
	release
	end

Palm204_AbelfDefeated::
	msgbox Palm204_TextAbelfAfter, MSGBOX_DEFAULT
	release
	end

Palm204_Nami::
	lock
	faceplayer
	goto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm204_NamiDone
	goto_if_defeated TRAINER_PALM_ABELF, Palm204_NamiConsole
	msgbox Palm204_TextNami, MSGBOX_DEFAULT
	release
	end

Palm204_NamiConsole::
	msgbox Palm204_TextNamiConsole, MSGBOX_DEFAULT
	release
	end

Palm204_NamiDone::
	msgbox Palm204_TextNamiDone, MSGBOX_DEFAULT
	release
	end

Palm204_Console::
	lockall
	goto_if_set FLAG_HT_TIDEMOUTH_COMPLEX_DONE, Palm204_ConsoleOff
	goto_if_not_defeated TRAINER_PALM_ABELF, Palm204_ConsoleGuarded
	msgbox Palm204_TextConsole, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm204_Release
	playse SE_PC_OFF
	waitse
	msgbox Palm204_TextShutdown, MSGBOX_DEFAULT
	setflag FLAG_HT_TIDEMOUTH_COMPLEX_DONE
	playse SE_PIN
	msgbox Palm204_TextMountain, MSGBOX_DEFAULT
	msgbox Palm204_TextNamiDone, MSGBOX_DEFAULT
	releaseall
	end

Palm204_ConsoleOff::
	msgbox Palm204_TextConsoleOff, MSGBOX_DEFAULT
	releaseall
	end

Palm204_ConsoleGuarded::
	msgbox Palm204_TextConsoleGuarded, MSGBOX_DEFAULT
	releaseall
	end

Palm204_Monitor::
	msgbox Palm204_TextMonitor, MSGBOX_SIGN
	end

Palm204_Release::
	releaseall
	end


Palm204_TextNami:
	.string "NAMI: {PLAYER}! I came on my WAILORD.\n"
	.string "I couldn't just wait in town.\p"
	.string "That's ABELF, the head of TEAM PALM.\n"
	.string "Let's end this together!$"

Palm204_TextAbelfIntro:
	.string "ABELF: Ah, the child from the news.\n"
	.string "And the GYM LEADER, too.\p"
	.string "I'm not building a power plant.\n"
	.string "I'm creating the future of the economy.\p"
	.string "NAMI: You're flooding the city!\p"
	.string "ABELF: Temporary sacrifices.\n"
	.string "Permanent profit.\p"
	.string "NAMI: Then we'll end that future of\n"
	.string "yours right now. {PLAYER}, go!$"

Palm204_TextAbelfLoss:
	.string "ABELF: …So the future can lose.$"

Palm204_TextAbelfAfter:
	.string "ABELF: Take your victory. Shut it all\n"
	.string "down, if you like.\p"
	.string "We were never trying to rule the sea.\n"
	.string "We were looking for a source of power\l"
	.string "that vanished long ago.\p"
	.string "The machines only caught its echoes.\n"
	.string "Whatever is out there, it isn't mine\l"
	.string "to control anymore.$"

Palm204_TextNamiConsole:
	.string "NAMI: The main console is right there.\n"
	.string "Shut it down, {PLAYER}!$"

Palm204_TextConsoleGuarded:
	.string "ABELF is standing in front of the\n"
	.string "main console.$"

Palm204_TextConsole:
	.string "The main console controls every\n"
	.string "turbine and every machine.\p"
	.string "Shut down the system?$"

Palm204_TextShutdown:
	.string "The turbines wind down one by one.\n"
	.string "The roar of the sea grows quiet…\p"
	.string "TEAM PALM's machines are silent.$"

Palm204_TextMountain:
	.string "…For less than a second, an image\n"
	.string "flickers on the main monitor.\p"
	.string "The outline of a mountain, under\n"
	.string "a dark, swirling sky.\p"
	.string "Then the screen goes black.$"

Palm204_TextNamiDone:
	.string "NAMI: We did it! The tide is already\n"
	.string "going down. The city is safe!\p"
	.string "But that mountain on the screen…\n"
	.string "The storm isn't over, is it?\p"
	.string "Come to my GYM when you're ready.\n"
	.string "Let's battle like we mean it!$"

Palm204_TextConsoleOff:
	.string "The main console is dark and silent.$"

Palm204_TextMonitor:
	.string "The monitor shows tide graphs.\n"
	.string "The lines are slowly falling.$"