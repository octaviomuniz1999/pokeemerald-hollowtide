PalmSerenia_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm141_Load
	.byte 0

Palm141_Load::
	setmetatile 33, 18, 458, TRUE
	end

Palm141_Jade::
	lock
	faceplayer
	goto_if_set FLAG_HT_SERENIA_DONE, Palm141_JadeDone
	goto_if_set FLAG_HT_SERENIA_JADE_MET, Palm141_JadeAgain
	msgbox Palm141_TextJadeMeet, MSGBOX_DEFAULT
	setflag FLAG_HT_SERENIA_JADE_MET
	release
	end

Palm141_JadeAgain::
	msgbox Palm141_TextJadeAgain, MSGBOX_DEFAULT
	release
	end

Palm141_JadeDone::
	msgbox Palm141_TextJadeDone, MSGBOX_DEFAULT
	release
	end

Palm141_Lau::
	lock
	faceplayer
	playmoncry SPECIES_ESPEON, CRY_MODE_NORMAL
	msgbox Palm141_TextLau, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Palm141_Fragment::
	lock
	msgbox Palm141_TextFragment, MSGBOX_DEFAULT
	setflag FLAG_HT_SERENIA_FRAGMENT
	removeobject 3
	release
	end

Palm141_Altar::
	lockall
	goto_if_set FLAG_HT_SERENIA_DONE, Palm141_AltarDone
	goto_if_set FLAG_HT_SERENIA_FRAGMENT, Palm141_AltarPlace
	msgbox Palm141_TextAltarEmpty, MSGBOX_DEFAULT
	releaseall
	end

Palm141_AltarPlace::
	msgbox Palm141_TextAltarPlace, MSGBOX_DEFAULT
	playse SE_M_CONFUSE_RAY
	waitse
	msgbox Palm141_TextInscription, MSGBOX_DEFAULT
	setflag FLAG_HT_SERENIA_DONE
	releaseall
	end

Palm141_AltarDone::
	msgbox Palm141_TextInscription, MSGBOX_DEFAULT
	releaseall
	end

Palm141_Illusion1::
	lockall
	goto_if_unset FLAG_HT_SERENIA_JADE_MET, Palm141_IllusionSolid
	msgbox Palm141_TextIllusion, MSGBOX_DEFAULT
	playse SE_M_TELEPORT
	setflag FLAG_HT_SERENIA_ILLUSION_1
	removeobject 8
	removeobject 9
	releaseall
	end

Palm141_Illusion2::
	lockall
	goto_if_unset FLAG_HT_SERENIA_JADE_MET, Palm141_IllusionSolid
	msgbox Palm141_TextIllusion, MSGBOX_DEFAULT
	playse SE_M_TELEPORT
	setflag FLAG_HT_SERENIA_ILLUSION_2
	removeobject 10
	removeobject 11
	releaseall
	end

Palm141_Illusion3::
	lockall
	goto_if_unset FLAG_HT_SERENIA_JADE_MET, Palm141_IllusionSolid
	msgbox Palm141_TextIllusion, MSGBOX_DEFAULT
	playse SE_M_TELEPORT
	setflag FLAG_HT_SERENIA_ILLUSION_3
	removeobject 12
	removeobject 13
	releaseall
	end

Palm141_IllusionSolid::
	msgbox Palm141_TextIllusionSolid, MSGBOX_DEFAULT
	releaseall
	end

Palm141_Elder::
	msgbox Palm141_Elder_Text, MSGBOX_NPC
	end

Palm141_Girl::
	msgbox Palm141_Girl_Text, MSGBOX_NPC
	end

Palm141_GymGuard::
	msgbox Palm141_GymGuard_Text, MSGBOX_NPC
	end

Palm141_Gardener::
	msgbox Palm141_Gardener_Text, MSGBOX_NPC
	end

Palm141_TownSign::
	msgbox Palm141_TownSign_Text, MSGBOX_SIGN
	end

Palm141_GymSign::
	msgbox Palm141_GymSign_Text, MSGBOX_SIGN
	end

Palm141_SpringSign::
	msgbox Palm141_SpringSign_Text, MSGBOX_SIGN
	end


Palm141_TextJadeMeet:
	.string "JADE: Lau, sweetheart, come here.\n"
	.string "You're sensing it again, aren't you?\p"
	.string "Oh! A traveler. I'm JADE, the GYM\n"
	.string "LEADER of SERENIA. This is LAU.\p"
	.string "It doesn't feel hostile. It feels...\n"
	.string "like someone's memory, very strong.\p"
	.string "When we're frightened, we can't\n"
	.string "always ask for help in a way that\p"
	.string "others understand.\p"
	.string "TEAM PALM took fragments from our\n"
	.string "shrine to “measure” something.\p"
	.string "Since then, illusions block the path\n"
	.string "to the spring. Would you help us?\p"
	.string "LAU trusts you. The illusions should\n"
	.string "part for you now.$"

Palm141_TextJadeAgain:
	.string "JADE: The path to the spring is\n"
	.string "just north. LAU will guide you.$"

Palm141_TextJadeDone:
	.string "JADE: LAU trusts you. So do I.\p"
	.string "But there's something we must\n"
	.string "understand before it's too late.\p"
	.string "My GYM opens soon. Rest first.$"

Palm141_TextLau:
	.string "LAU: Eee-fuu!\n"
	.string "LAU's eyes glow softly.$"

Palm141_TextIllusionSolid:
	.string "A heavy boulder blocks the path.\n"
	.string "It won't budge.$"

Palm141_TextIllusion:
	.string "The boulder shimmers and fades...\n"
	.string "It was only an illusion!$"

Palm141_TextFragment:
	.string "{PLAYER} found a glowing SHRINE\n"
	.string "FRAGMENT! TEAM PALM must have\p"
	.string "dropped it while fleeing.$"

Palm141_TextAltarEmpty:
	.string "An empty niche in the stone by\n"
	.string "the spring. Something is missing.$"

Palm141_TextAltarPlace:
	.string "{PLAYER} placed the SHRINE FRAGMENT\n"
	.string "in the niche. It fits perfectly!\p"
	.string "A soft light spreads over the\n"
	.string "spring...$"

Palm141_TextInscription:
	.string "Words appear on the old stone:\p"
	.string "“When the sky forgets its rain,\n"
	.string "a sleeping power may call the tide\p"
	.string "over the mountains.”$"

Palm141_Elder_Text:
	.string "In my youth, the wind always blew\n"
	.string "from the sea. Now it can't decide.$"

Palm141_Girl_Text:
	.string "I saw my grandma's old teapot on\n"
	.string "the bridge! Then it was gone...$"

Palm141_GymGuard_Text:
	.string "JADE's GYM is closed while she\n"
	.string "looks after the shrine.$"

Palm141_Gardener_Text:
	.string "A stone garden teaches patience.\n"
	.string "Every rock has its own place.$"

Palm141_TownSign_Text:
	.string "SERENIA\n"
	.string "“A quiet place to remember.”$"

Palm141_GymSign_Text:
	.string "SERENIA POKéMON GYM\n"
	.string "LEADER: JADE\p"
	.string "“The mind is a mirror.”$"

Palm141_SpringSign_Text:
	.string "SACRED SPRING\n"
	.string "Please return what you borrow.$"