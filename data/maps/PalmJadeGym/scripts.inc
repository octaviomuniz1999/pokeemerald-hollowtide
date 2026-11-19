PalmJadeGym_MapScripts::
	.byte 0

Palm150_Jade::
	trainerbattle_single TRAINER_PALM_JADE, Palm150_TextJadeIntro, Palm150_TextJadeDefeat, Palm150_JadeDefeated, NO_MUSIC
	msgbox Palm150_TextJadeAfter, MSGBOX_DEFAULT
	release
	end

Palm150_JadeDefeated::
	message Palm150_TextBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox Palm150_TextBadgeExplain, MSGBOX_DEFAULT
	setflag FLAG_BADGE05_GET
	setflag FLAG_DEFEATED_PETALBURG_GYM
	giveitem ITEM_TM_PSYCHIC
	msgbox Palm150_TextTM, MSGBOX_DEFAULT
	release
	end

Palm150_Lau::
	lock
	faceplayer
	playmoncry SPECIES_ESPEON, CRY_MODE_NORMAL
	msgbox Palm150_TextLau, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Palm150_GymGuide::
	msgbox Palm150_TextGuide, MSGBOX_NPC
	end

Palm150_TrainerA::
	trainerbattle_single TRAINER_PALM_JADE_GYM_A, Palm150_TextAIntro, Palm150_TextADefeat
	msgbox Palm150_TextAAfter, MSGBOX_AUTOCLOSE
	end

Palm150_TrainerB::
	trainerbattle_single TRAINER_PALM_JADE_GYM_B, Palm150_TextBIntro, Palm150_TextBDefeat
	msgbox Palm150_TextBAfter, MSGBOX_AUTOCLOSE
	end

Palm150_TrainerC::
	trainerbattle_single TRAINER_PALM_JADE_GYM_C, Palm150_TextCIntro, Palm150_TextCDefeat
	msgbox Palm150_TextCAfter, MSGBOX_AUTOCLOSE
	end

Palm150_Mirror1::
	msgbox Palm150_TextMirror1, MSGBOX_SIGN
	end

Palm150_Mirror2::
	msgbox Palm150_TextMirror2, MSGBOX_SIGN
	end

Palm150_Mirror3::
	msgbox Palm150_TextMirror3, MSGBOX_SIGN
	end

Palm150_DoorEntranceL::
	lockall
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, 37
	msgbox Palm150_TextEnterDoor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm150_EnterRoom
	releaseall
	end

Palm150_DoorEntranceR::
	lockall
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, 37
	msgbox Palm150_TextEnterDoor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm150_EnterRoom
	releaseall
	end

Palm150_DoorAL::
	lockall
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, 27
	msgbox Palm150_TextSymbolMOON, MSGBOX_DEFAULT
	msgbox Palm150_TextEnterDoor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm150_EnterRoom
	releaseall
	end

Palm150_DoorAR::
	lockall
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, 41
	msgbox Palm150_TextSymbolSUN, MSGBOX_DEFAULT
	msgbox Palm150_TextEnterDoor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm150_EnterRoom
	releaseall
	end

Palm150_DoorBL::
	lockall
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, 41
	msgbox Palm150_TextSymbolSUN, MSGBOX_DEFAULT
	msgbox Palm150_TextEnterDoor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm150_EnterRoom
	releaseall
	end

Palm150_DoorBR::
	lockall
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, 17
	msgbox Palm150_TextSymbolSTAR, MSGBOX_DEFAULT
	msgbox Palm150_TextEnterDoor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm150_EnterRoom
	releaseall
	end

Palm150_DoorCL::
	lockall
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, 7
	msgbox Palm150_TextSymbolSUN, MSGBOX_DEFAULT
	msgbox Palm150_TextEnterDoor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm150_EnterRoom
	releaseall
	end

Palm150_DoorCR::
	lockall
	setvar VAR_0x8008, 1
	setvar VAR_0x8009, 41
	msgbox Palm150_TextSymbolMOON, MSGBOX_DEFAULT
	msgbox Palm150_TextEnterDoor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm150_EnterRoom
	releaseall
	end

Palm150_EnterRoom::
	closemessage
	delay 20
	warpdoor MAP_PALM_JADE_GYM, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end


Palm150_TextGuide:
	.string "Hey, future CHAMPION {PLAYER}!\p"
	.string "This is the MIRROR GARDEN. JADE uses\n"
	.string "PSYCHIC-type POKéMON.\p"
	.string "Read the three mirrors here and\n"
	.string "remember their symbols in order.\p"
	.string "In each room, take the door that\n"
	.string "shows the next symbol. A wrong door\l"
	.string "brings you back here!$"

Palm150_TextMirror1:
	.string "The first mirror shows a MOON.$"

Palm150_TextMirror2:
	.string "The second mirror shows a STAR.$"

Palm150_TextMirror3:
	.string "The third mirror shows a SUN.$"

Palm150_TextSymbolMOON:
	.string "A MOON is carved above the door.$"

Palm150_TextSymbolSTAR:
	.string "A STAR is carved above the door.$"

Palm150_TextSymbolSUN:
	.string "A SUN is carved above the door.$"

Palm150_TextEnterDoor:
	.string "Step through the door?$"

Palm150_TextJadeIntro:
	.string "JADE: You remembered the mirrors.\n"
	.string "LAU knew you would.\p"
	.string "LAU trusts you. So do I.\n"
	.string "But there's something we must\l"
	.string "understand before it's too late.\p"
	.string "First, show me how clear your mind\n"
	.string "can be!$"

Palm150_TextJadeDefeat:
	.string "JADE: Your heart didn't waver once.\p"
	.string "Please, take the SERENITY BADGE.$"

Palm150_TextJadeAfter:
	.string "JADE: That presence LAU senses...\n"
	.string "it's sad, not angry.\p"
	.string "Whoever it is, they are still trying\n"
	.string "to protect something. Keep going.$"

Palm150_TextBadge:
	.string "{PLAYER} received the SERENITY BADGE\n"
	.string "from JADE.$"

Palm150_TextBadgeExplain:
	.string "The SERENITY BADGE helps you stay\n"
	.string "calm when the world is not.\p"
	.string "Take this as well.$"

Palm150_TextTM:
	.string "That TM is PSYCHIC. A strong mind\n"
	.string "is the sharpest weapon.$"

Palm150_TextLau:
	.string "LAU: Fuu...\n"
	.string "LAU looks at you calmly.$"

Palm150_TextAIntro:
	.string "The mirrors told you the way...\n"
	.string "but can you see through me?$"

Palm150_TextADefeat:
	.string "I didn't foresee that.$"

Palm150_TextAAfter:
	.string "Remember the order. MOON first,\n"
	.string "then the rest!$"

Palm150_TextBIntro:
	.string "Every reflection hides a secret.\n"
	.string "Mine hides a battle!$"

Palm150_TextBDefeat:
	.string "My reflection cracked...$"

Palm150_TextBAfter:
	.string "Doubt is the only wrong door.$"

Palm150_TextCIntro:
	.string "One more symbol stands between you\n"
	.string "and JADE. Do you remember it?$"

Palm150_TextCDefeat:
	.string "Your memory is sharp!$"

Palm150_TextCAfter:
	.string "JADE and LAU are waiting.\n"
	.string "Go on.$"