PalmStormRidge_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Palm230_OnTransition
	.byte 0

Palm230_OnTransition:
	call_if_ge VAR_HT_EPILOGUE, 2, Palm24x_Sunny
	call_if_set FLAG_HT_CYNTHIA_DONE, Palm230_CynthiaAside
	end

Palm230_CynthiaAside::
	setobjectxyperm LOCALID_STORM_CYNTHIA, 19, 13
	setobjectmovementtype LOCALID_STORM_CYNTHIA, MOVEMENT_TYPE_FACE_LEFT
	return

Palm230_CynthiaStop::
	goto_if_set FLAG_HT_CYNTHIA_DONE, Palm230_End
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	goto Palm230_CynthiaTalk
	end

Palm230_Cynthia::
	lockall
	goto_if_set FLAG_HT_CYNTHIA_DONE, Palm230_CynthiaAfter
	goto Palm230_CynthiaTalk
	end

Palm230_CynthiaTalk::
	msgbox Palm230_TextCynthiaWarn1, MSGBOX_DEFAULT
	msgbox Palm230_TextCynthiaAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm230_TurnBack
	msgbox Palm230_TextCynthiaWarn2, MSGBOX_DEFAULT
	msgbox Palm230_TextCynthiaAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Palm230_TurnBack
	playbgm MUS_ENCOUNTER_CHAMPION, FALSE
	msgbox Palm230_TextCynthiaIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_STEVEN, Palm230_TextCynthiaDefeat
	msgbox Palm230_TextCynthiaPost, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox Palm230_TextJoyHeal, MSGBOX_DEFAULT
	applymovement LOCALID_STORM_CYNTHIA, Palm230_StepAside
	waitmovement 0
	setflag FLAG_HT_CYNTHIA_DONE
	call Palm230_CynthiaAside
	msgbox Palm230_TextCynthiaGo, MSGBOX_DEFAULT
	releaseall
	end

Palm230_TurnBack::
	msgbox Palm230_TextCynthiaThanks, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_PLAYER, Palm230_StepBackDown
	waitmovement 0
	releaseall
	end

Palm230_CynthiaAfter::
	msgbox Palm230_TextCynthiaGo, MSGBOX_DEFAULT
	releaseall
	end

Palm230_End::
	end

Palm230_StepAside:
	walk_right
	walk_in_place_faster_left
	step_end

Palm230_StepBackDown:
	walk_down
	step_end

Palm230_SignPost::
	msgbox Palm230_SignPost_Text, MSGBOX_SIGN
	end


Palm230_SignPost_Text:
	.string "POKéMON LEAGUE FIELD POST\n"
	.string "Medical care for trainers and POKéMON.$"

Palm230_TextCynthiaWarn1:
	.string "CYNTHIA: Stop right there.\p"
	.string "I'm CYNTHIA. I climbed this staircase\n"
	.string "yesterday… and I came back down in\l"
	.string "a hurry.\p"
	.string "I almost lost my whole team to the\n"
	.string "power of that orb.\p"
	.string "This mountain is not safe. Not for\n"
	.string "you, not for anyone.$"

Palm230_TextCynthiaAsk:
	.string "Will you turn back?$"

Palm230_TextCynthiaWarn2:
	.string "CYNTHIA: Please, listen to me.\p"
	.string "I'm not trying to prove I'm better\n"
	.string "than you.\p"
	.string "I'm trying to stop anyone else from\n"
	.string "getting hurt.$"

Palm230_TextCynthiaThanks:
	.string "CYNTHIA: Thank you. Go back to the\n"
	.string "post and rest.\p"
	.string "The storm will still be here.$"

Palm230_TextCynthiaIntro:
	.string "CYNTHIA: …I see.\p"
	.string "If you can't understand the risk,\n"
	.string "then you leave me no choice.\p"
	.string "GARCHOMP, let's stop them!$"

Palm230_TextCynthiaDefeat:
	.string "…You did it.$"

Palm230_TextCynthiaPost:
	.string "CYNTHIA: I saw a determination I\n"
	.string "didn't know how to recognize.\p"
	.string "When I faced him, he asked his\n"
	.string "POKéMON to fall back for a moment.\p"
	.string "Maybe there's still someone in\n"
	.string "there.$"

Palm230_TextJoyHeal:
	.string "NURSE JOY hurried up from the post\n"
	.string "and healed your POKéMON!\p"
	.string "JOY: There, all better. Rest a moment\n"
	.string "before you go up.$"

Palm230_TextCynthiaGo:
	.string "CYNTHIA: The summit is at the top of\n"
	.string "this staircase.\p"
	.string "There's no one else on the way.\n"
	.string "Whatever you find up there…\l"
	.string "don't face it alone in your heart.$"
@ Palm24x_Sunny (definido no cume)
