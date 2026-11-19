PalmPassway_MapScripts::
	.byte 0

Palm181_StairGate::
	goto_if_set FLAG_SYS_GAME_CLEAR, Palm181_Ok
	lockall
	msgbox Palm181_TextStairGate, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm181_StepBackSouth
	waitmovement 0
	releaseall
	end

Palm181_EastGate::
	goto_if_set FLAG_HT_PASSWAY_EAST_OPEN, Palm181_Ok
	lockall
	msgbox Palm181_TextEastGate, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Palm181_StepBackWest
	waitmovement 0
	releaseall
	end

Palm181_Ok::
	end

Palm181_StepBackSouth:
	walk_down
	step_end

Palm181_StepBackWest:
	walk_left
	step_end

Palm181_Spring::
	lockall
	msgbox Palm181_TextSpring, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm181_SpringNo
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	fadescreen FADE_FROM_BLACK
	msgbox Palm181_TextSpringDone, MSGBOX_DEFAULT
	releaseall
	end

Palm181_SpringNo::
	releaseall
	end

Palm181_Guardian::
	msgbox Palm181_Guardian_Text, MSGBOX_NPC
	end

Palm181_Watcher::
	msgbox Palm181_Watcher_Text, MSGBOX_NPC
	end

Palm181_Traveler::
	msgbox Palm181_Traveler_Text, MSGBOX_NPC
	end

Palm181_Kid::
	msgbox Palm181_Kid_Text, MSGBOX_NPC
	end

Palm181_Worker::
	msgbox Palm181_Worker_Text, MSGBOX_NPC
	end

Palm181_Bather::
	msgbox Palm181_Bather_Text, MSGBOX_NPC
	end

Palm181_TownSign::
	msgbox Palm181_TownSign_Text, MSGBOX_SIGN
	end

Palm181_Mural::
	msgbox Palm181_Mural_Text, MSGBOX_SIGN
	end

Palm181_StairSign::
	msgbox Palm181_StairSign_Text, MSGBOX_SIGN
	end

Palm182_PcGirl::
	msgbox Palm182_PcGirl_Text, MSGBOX_NPC
	end

Palm182_PcExpert::
	msgbox Palm182_PcExpert_Text, MSGBOX_NPC
	end

Palm182_PcWoman::
	msgbox Palm182_PcWoman_Text, MSGBOX_NPC
	end

Palm182_MartWoman::
	msgbox Palm182_MartWoman_Text, MSGBOX_NPC
	end

Palm182_MartMan::
	msgbox Palm182_MartMan_Text, MSGBOX_NPC
	end

Palm182_MartSkitty::
	lock
	faceplayer
	playmoncry SPECIES_SKITTY, CRY_MODE_NORMAL
	msgbox Palm182_MartSkitty_Text, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Palm182_Innkeeper::
	msgbox Palm182_Innkeeper_Text, MSGBOX_NPC
	end

Palm182_InnGuest::
	msgbox Palm182_InnGuest_Text, MSGBOX_NPC
	end

Palm182_Elder::
	msgbox Palm182_Elder_Text, MSGBOX_NPC
	end

Palm182_ElderGrandkid::
	msgbox Palm182_ElderGrandkid_Text, MSGBOX_NPC
	end

Palm182_HouseWoman::
	msgbox Palm182_HouseWoman_Text, MSGBOX_NPC
	end

Palm182_HouseGirl::
	msgbox Palm182_HouseGirl_Text, MSGBOX_NPC
	end

Palm182_HouseBoy::
	msgbox Palm182_HouseBoy_Text, MSGBOX_NPC
	end


Palm181_TextStairGate:
	.string "GUARDIAN: Hold it right there!\p"
	.string "This trail is not a tourist route.\n"
	.string "The winds up there are too strong,\l"
	.string "and the LEAGUE has closed the way.$"

Palm181_TextEastGate:
	.string "A rockslide is blocking the road east.\p"
	.string "Workers are clearing it. The road to\n"
	.string "VOLTARA should open soon.$"

Palm181_TextSpring:
	.string "Steam rises from the hot spring.\n"
	.string "Would you like to rest a while?$"

Palm181_TextSpringDone:
	.string "You and your POKéMON feel completely\n"
	.string "refreshed!$"

Palm181_Guardian_Text:
	.string "GUARDIAN: I've guarded these stairs\n"
	.string "for twenty years.\p"
	.string "I've never seen the sky above the\n"
	.string "summit this dark. Nobody goes up.$"

Palm181_Watcher_Text:
	.string "Look up there, past the stairs.\p"
	.string "The clouds over the summit turn\n"
	.string "darker every evening.\p"
	.string "Old travelers say the mountain is\n"
	.string "waiting for something.$"

Palm181_Traveler_Text:
	.string "I came all the way from FERRALIA.\n"
	.string "Every traveler rests in PASSWAY\l"
	.string "before crossing to the other side.$"

Palm181_Kid_Text:
	.string "Grandma says a black dog once\n"
	.string "guarded our village!\p"
	.string "I've never seen it, though.$"

Palm181_Worker_Text:
	.string "We're clearing the rockslide on the\n"
	.string "road to VOLTARA. Give us a little time!$"

Palm181_Bather_Text:
	.string "Aaah… This spring has warmed tired\n"
	.string "travelers for hundreds of years.$"

Palm181_TownSign_Text:
	.string "PASSWAY VILLAGE\n"
	.string "“Rest here before the mountain.”$"

Palm181_StairSign_Text:
	.string "SUMMIT TRAIL\n"
	.string "Closed by order of the POKéMON LEAGUE.$"

Palm181_Mural_Text:
	.string "An old mural is carved into the rock.\p"
	.string "It shows travelers climbing a\n"
	.string "mountain under a dark sky.\p"
	.string "At the center, someone holds up a\n"
	.string "round emblem…\p"
	.string "It looks a lot like your ATLAS\n"
	.string "MEDALLION.$"

Palm182_PcGirl_Text:
	.string "The nurse here makes tea with herbs\n"
	.string "from the mountain. It smells so good!$"

Palm182_PcExpert_Text:
	.string "I came to climb the summit, but the\n"
	.string "trail is closed. I'll wait. Mountains\l"
	.string "are patient, and so am I.$"

Palm182_PcWoman_Text:
	.string "In PASSWAY, everyone helps travelers.\n"
	.string "That's our oldest tradition.$"

Palm182_MartWoman_Text:
	.string "Buy warm clothes before going north!\n"
	.string "Oh, you don't need them? Lucky you.$"

Palm182_MartMan_Text:
	.string "FULL HEALS sell out every winter.\n"
	.string "The mountain wind is no joke.$"

Palm182_MartSkitty_Text:
	.string "SKITTY: Mew!$"

Palm182_Innkeeper_Text:
	.string "Welcome to the PASSWAY INN!\p"
	.string "Travelers have slept under this roof\n"
	.string "since before the roads were paved.$"

Palm182_InnGuest_Text:
	.string "I'm waiting for the road to VOLTARA\n"
	.string "to open. I hope it's soon!$"

Palm182_Elder_Text:
	.string "ELDER: Ah, a young traveler.\n"
	.string "Sit, sit.\p"
	.string "They say that, long ago, someone left\n"
	.string "here the sign of a faithful guardian.\p"
	.string "A circle as pale as the moon, on the\n"
	.string "chest of a black dog.\p"
	.string "Some people believe that carrying the\n"
	.string "world means not letting anyone help.\p"
	.string "But even guardians need to rest.$"

Palm182_ElderGrandkid_Text:
	.string "Grandma tells that story to everyone\n"
	.string "who passes through the village.\p"
	.string "I think she's waiting for someone.$"

Palm182_HouseWoman_Text:
	.string "My husband works on the rockslide.\n"
	.string "He comes home covered in dust!$"

Palm182_HouseGirl_Text:
	.string "When the clouds get dark, we stay\n"
	.string "inside and play cards.$"

Palm182_HouseBoy_Text:
	.string "I want to climb the summit someday.\n"
	.string "The GUARDIAN never lets anyone pass!$"