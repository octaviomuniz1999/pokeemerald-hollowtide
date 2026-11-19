PalmTeatro_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Palm090_StageRefresh
	.byte 0

Palm090_Left::
	lockall
	goto_if_set FLAG_PALM_JAY_WON, Palm090_PuzzleDone
	goto_if_eq VAR_TEMP_8, 0, Palm090_StepOne
	goto_if_eq VAR_TEMP_8, 2, Palm090_StepThree
	goto Palm090_Wrong

Palm090_Right::
	lockall
	goto_if_set FLAG_PALM_JAY_WON, Palm090_PuzzleDone
	goto_if_eq VAR_TEMP_8, 1, Palm090_StepTwo
	goto Palm090_Wrong

Palm090_Reset::
	lockall
	goto_if_set FLAG_PALM_JAY_WON, Palm090_PuzzleDone
	goto_if_eq VAR_TEMP_8, 3, Palm090_PuzzleDone
	msgbox Palm090_TextCenterPanel, MSGBOX_DEFAULT
	releaseall
	end

Palm090_StepOne::
	setvar VAR_TEMP_8, 1
	goto Palm090_Lit

Palm090_StepTwo::
	setvar VAR_TEMP_8, 2
	goto Palm090_Lit

Palm090_StepThree::
	setvar VAR_TEMP_8, 3
	goto Palm090_Lit

Palm090_Lit::
	playse SE_SWITCH
	call Palm090_StageDraw
	special DrawWholeMapView
	goto_if_eq VAR_TEMP_8, 3, Palm090_PuzzleDone
	goto_if_eq VAR_TEMP_8, 2, Palm090_LitTwo
	msgbox Palm090_TextStageLamp, MSGBOX_DEFAULT
	releaseall
	end

Palm090_LitTwo::
	msgbox Palm090_TextStageLampTwo, MSGBOX_DEFAULT
	releaseall
	end

Palm090_Wrong::
	setvar VAR_TEMP_8, 0
	call Palm090_StageDraw
	special DrawWholeMapView
	msgbox Palm090_TextReset, MSGBOX_DEFAULT
	releaseall
	end

Palm090_PuzzleDone::
	playse SE_SUCCESS
	msgbox Palm090_TextPuzzleDone, MSGBOX_DEFAULT
	releaseall
	end

Palm090_StageHint::
	msgbox Palm090_TextHint, MSGBOX_SIGN
	end

Palm090_Jay::
	goto_if_set FLAG_PALM_JAY_WON, Palm090_JayWon
	lock
	faceplayer
	goto_if_eq VAR_TEMP_8, 3, Palm090_JayBattle
	msgbox Palm090_TextBlocked, MSGBOX_DEFAULT
	release
	end

Palm090_JayBattle::
	trainerbattle_single TRAINER_PALM_JAY, Palm090_TextJayIntro, Palm090_TextJayLoss, Palm090_JayVictory, NO_MUSIC
	goto Palm090_JayVictory

Palm090_JayVictory::
	setflag FLAG_BADGE02_GET
	setflag FLAG_PALM_JAY_WON
	message Palm090_TextBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	waitbuttonpress
	closemessage
	goto Palm090_JayGiveTM

Palm090_JayWon::
	lock
	faceplayer
	goto_if_unset FLAG_PALM_JAY_TM, Palm090_JayGiveTM
	msgbox Palm090_TextJayAfter, MSGBOX_DEFAULT
	release
	end

Palm090_JayGiveTM::
	additem ITEM_TM_HEX, 1
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_PALM_JAY_TM
	msgreceiveditem Palm090_TextReceivedHex, ITEM_TM_HEX, 1, MUS_OBTAIN_TMHM
	release
	end

Palm090_Linh::
	trainerbattle_single TRAINER_PALM_LINH, Palm090_TextLinh, Palm090_TextLinhLoss
	release
	end

Palm090_Yumi::
	trainerbattle_single TRAINER_PALM_YUMI, Palm090_TextYumi, Palm090_TextYumiLoss
	release
	end

Palm090_TextHint:
	.string "SPOTLIGHTS\n"
	.string "Left, right, left.$"
Palm090_TextStageLamp:
	.string "The LEFT spotlight flickers on!\n"
	.string "Next: the RIGHT spotlight.$"
Palm090_TextReset:
	.string "The lights went out...\p"
	.string "Light them in order: LEFT, then\n"
	.string "RIGHT, then LEFT again.$"
Palm090_TextPuzzleDone:
	.string "The stage is lit!\n"
	.string "JAY is ready for you.$"
Palm090_TextBlocked:
	.string "JAY: My stage is still dark!\p"
	.string "Light the spotlights on the panels\n"
	.string "below: LEFT, then RIGHT, then LEFT.$"
Palm090_TextJayIntro:
	.string "JAY: Now that the lights are back,\n"
	.string "even the shadows want to dance!\p"
	.string "Let's give this crowd a show\n"
	.string "they'll remember!$"
Palm090_TextJayLoss:
	.string "JAY: That deserved an encore!$"
Palm090_TextBadge:
	.string "JAY: The ECHO BADGE is yours.\p"
	.string "The west beach trail is open.\n"
	.string "ROUTE 3 leads up to FERRALIA.$"
Palm090_TextReceivedHex:
	.string "{PLAYER} recebeu a TM51: Hex!$"
Palm090_TextJayAfter:
	.string "JAY: Head out along the west\n"
	.string "beach. Mind the cliffs up the coast!$"
Palm090_TextLinh:
	.string "LINH: Mic check! Let's test the\n"
	.string "sound with a battle!$"
Palm090_TextLinhLoss:
	.string "Que ritmo!$"
Palm090_TextYumi:
	.string "YUMI: Meet my partner!\n"
	.string "Isn't it a star?$"
Palm090_TextYumiLoss:
	.string "Fim da apresentacao!$"

Palm090_StageRefresh::
	call_if_set FLAG_PALM_JAY_WON, Palm090_CompletedLights
	call Palm090_StageDraw
	end

Palm090_CompletedLights::
	setvar VAR_TEMP_8, 3
	return

Palm090_StageDraw::
	setmetatile 3, 8, 663, TRUE
	setmetatile 5, 8, 663, TRUE
	setmetatile 7, 8, 663, TRUE
	call_if_ge VAR_TEMP_8, 1, Palm090_LightLeft
	call_if_ge VAR_TEMP_8, 2, Palm090_LightRight
	call_if_ge VAR_TEMP_8, 3, Palm090_LightCenter
	return

Palm090_LightLeft::
	setmetatile 3, 8, 664, TRUE
	return
Palm090_LightRight::
	setmetatile 7, 8, 665, TRUE
	return
Palm090_LightCenter::
	setmetatile 5, 8, 664, TRUE
	return

Palm090_TextCenterPanel:
	.string "A note is taped to the panel:\n"
	.string "“LEFT, RIGHT, LEFT.”$"

Palm090_TextStageLampTwo:
	.string "The RIGHT spotlight flickers on!\n"
	.string "Now the LEFT one again.$"
