PalmStormTrail_MapScripts::
	.byte 0

Palm220_StevenScene::
	goto_if_set FLAG_HT_STEVEN_MET, Palm220_End
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox Palm220_TextSteven, MSGBOX_DEFAULT
	setflag FLAG_HT_STEVEN_MET
	releaseall
	end

Palm220_LeonScene::
	goto_if_set FLAG_HT_LEON_MET, Palm220_End
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	playmoncry SPECIES_CHARIZARD, CRY_MODE_NORMAL
	waitmoncry
	msgbox Palm220_TextLeon, MSGBOX_DEFAULT
	setflag FLAG_HT_LEON_MET
	releaseall
	end

Palm220_End::
	end

Palm220_Steven::
	lock
	faceplayer
	msgbox Palm220_TextStevenAfter, MSGBOX_DEFAULT
	release
	end

Palm220_Leon::
	lock
	faceplayer
	msgbox Palm220_TextLeonAfter, MSGBOX_DEFAULT
	release
	end

Palm220_Metagross::
	lock
	playmoncry SPECIES_METAGROSS, CRY_MODE_NORMAL
	msgbox Palm220_TextMetagross, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Palm220_Charizard::
	lock
	playmoncry SPECIES_CHARIZARD, CRY_MODE_NORMAL
	msgbox Palm220_TextCharizard, MSGBOX_DEFAULT
	waitmoncry
	release
	end


Palm220_TextSteven:
	.string "STEVEN: …You're the new CHAMPION.\n"
	.string "DOGE said you might come.\p"
	.string "I'm STEVEN. I came from HOENN when\n"
	.string "the storm readings reached us.\p"
	.string "I lost to him.\p"
	.string "The pressure of that energy was\n"
	.string "different from anything we ever\l"
	.string "studied in HOENN.\p"
	.string "Don't underestimate the storm.$"

Palm220_TextStevenAfter:
	.string "STEVEN: METAGROSS and I will rest here\n"
	.string "for a while.\p"
	.string "The trail splits the mountain in two\n"
	.string "further up. Stay on the path.$"

Palm220_TextMetagross:
	.string "METAGROSS: Gu-gugugu…\p"
	.string "It looks tired, but it's still\n"
	.string "keeping watch over STEVEN.$"

Palm220_TextLeon:
	.string "LEON: Hold on. You're the one DOGE\n"
	.string "sent for, right?\p"
	.string "I'm LEON. CHARIZARD and I went up\n"
	.string "this gorge a few hours ago.\p"
	.string "My CHARIZARD fought with everything\n"
	.string "it had.\p"
	.string "Even so, I had to fall back to keep\n"
	.string "it safe.\p"
	.string "If you keep going, know that your\n"
	.string "courage will come at a price.$"

Palm220_TextLeonAfter:
	.string "LEON: Past the gorge, there's a nurse\n"
	.string "from the LEAGUE.\p"
	.string "She came all the way up here to look\n"
	.string "after the CHAMPIONS' teams.$"

Palm220_TextCharizard:
	.string "CHARIZARD: Grooar…\p"
	.string "Its tail flame is small, but it\n"
	.string "still burns steadily.$"