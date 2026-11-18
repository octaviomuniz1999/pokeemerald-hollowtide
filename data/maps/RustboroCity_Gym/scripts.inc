RustboroCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Palm067_Enter
	map_script MAP_SCRIPT_ON_LOAD, Palm065_Load
	.byte 0

RustboroCity_Gym_EventScript_Roxanne::
	lock
	faceplayer
	call Palm067_CheckClear
	goto_if_eq VAR_RESULT, TRUE, Palm066_LeaderBattle
	goto_if_not_defeated TRAINER_JOSH, Palm066_Battle1
	goto_if_not_defeated TRAINER_TOMMY, Palm066_Battle2
Palm066_LeaderBattle::
	trainerbattle_single TRAINER_ROXANNE_1, RustboroCity_Gym_Text_RoxanneIntro, RustboroCity_Gym_Text_RoxanneDefeat, RustboroCity_Gym_EventScript_RoxanneDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_Gym_EventScript_RoxanneRematch
	goto_if_unset FLAG_RECEIVED_TM_ROCK_TOMB, RustboroCity_Gym_EventScript_GiveRockTomb
	msgbox RustboroCity_Gym_Text_RoxannePostBattle, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_RoxanneDefeated::
	message RustboroCity_Gym_Text_ReceivedStoneBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox RustboroCity_Gym_Text_StoneBadgeInfoTakeThis, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_RUSTBORO_GYM
	setflag FLAG_BADGE01_GET
	setvar VAR_RUSTBORO_CITY_STATE, 1
	addvar VAR_PETALBURG_GYM_STATE, 1
	setvar VAR_0x8008, 1
	call Common_EventScript_SetGymTrainers
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	goto RustboroCity_Gym_EventScript_GiveRockTomb
	end

RustboroCity_Gym_EventScript_GiveRockTomb::
	giveitem ITEM_TM_BULLET_SEED
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_ROCK_TOMB
	msgbox RustboroCity_Gym_Text_ExplainRockTomb, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_RoxanneRematch::
	trainerbattle_rematch_double TRAINER_ROXANNE_1, RustboroCity_Gym_Text_RoxannePreRematch, RustboroCity_Gym_Text_RoxanneRematchDefeat, RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons
	msgbox RustboroCity_Gym_Text_RoxannePostRematch, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Josh::
	trainerbattle_single TRAINER_JOSH, RustboroCity_Gym_Text_JoshIntro, RustboroCity_Gym_Text_JoshDefeat
	msgbox RustboroCity_Gym_Text_JoshPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Tommy::
	trainerbattle_single TRAINER_TOMMY, RustboroCity_Gym_Text_TommyIntro, RustboroCity_Gym_Text_TommyDefeat
	msgbox RustboroCity_Gym_Text_TommyPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_Marc::
	trainerbattle_single TRAINER_MARC, RustboroCity_Gym_Text_MarcIntro, RustboroCity_Gym_Text_MarcDefeat
	msgbox RustboroCity_Gym_Text_MarcPostBattle, MSGBOX_AUTOCLOSE
	end

RustboroCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_RUSTBORO_GYM, RustboroCity_Gym_EventScript_GymGuidePostVictory
	msgbox RustboroCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_GymGuidePostVictory::
	msgbox RustboroCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

RustboroCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE01_GET, RustboroCity_Gym_EventScript_GymStatueCertified
	goto RustboroCity_Gym_EventScript_GymStatue
	end

RustboroCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE01_GET, RustboroCity_Gym_EventScript_GymStatueCertified
	goto RustboroCity_Gym_EventScript_GymStatue
	end

RustboroCity_Gym_EventScript_GymStatueCertified::
	msgbox RustboroCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

RustboroCity_Gym_EventScript_GymStatue::
	msgbox RustboroCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

RustboroCity_Gym_EventScript_RegisterRoxanne::
	lockall
	pokenavcall RustboroCity_Gym_Text_RoxanneRegisterCall
	waitmessage
	delay 30
	playfanfare MUS_REGISTER_MATCH_CALL
	msgbox RustboroCity_Gym_Text_RegisteredRoxanne, MSGBOX_DEFAULT
	waitfanfare
	closemessage
	delay 30
	setflag FLAG_ENABLE_ROXANNE_MATCH_CALL
	clearflag FLAG_ENABLE_ROXANNE_FIRST_CALL
	releaseall
	end

RustboroCity_Gym_Text_GymGuideAdvice:
	.string "Hey there, future champ!\p"
	.string "This GYM runs on the same water\n"
	.string "as the coffee fields.\p"
	.string "Open the floodgates in order,\n"
	.string "1 to 3, and beat the two\l"
	.string "growers along the way.$"

RustboroCity_Gym_Text_GymGuidePostVictory:
	.string "You beat NEVARD!\n"
	.string "HARVESTVALE won't forget this.$"

RustboroCity_Gym_Text_JoshIntro:
	.string "I work the fields with NEVARD!\n"
	.string "Let's see your team!$"

RustboroCity_Gym_Text_JoshDefeat:
	.string "Guess I need to tend my POKéMON\n"
	.string "a little better…$"

RustboroCity_Gym_Text_JoshPostBattle:
	.string "NEVARD knows every tree in this\n"
	.string "valley by name.$"

RustboroCity_Gym_Text_TommyIntro:
	.string "Coffee grows with patience.\n"
	.string "So does my team!$"

RustboroCity_Gym_Text_TommyDefeat:
	.string "A good harvest… for you.$"

RustboroCity_Gym_Text_TommyPostBattle:
	.string "NEVARD's way stronger than me!$"

RustboroCity_Gym_Text_MarcIntro:
	.string "Out here, strength comes from\n"
	.string "the roots!$"

RustboroCity_Gym_Text_MarcDefeat:
	.string "My roots gave way!$"

RustboroCity_Gym_Text_MarcPostBattle:
	.string "Training in the fields really\n"
	.string "pays off.$"

RustboroCity_Gym_Text_RoxanneIntro:
	.string "NEVARD: Welcome to HARVESTVALE!\p"
	.string "I look after the coffee, and the\n"
	.string "POKéMON who live on this land.\p"
	.string "Thanks for bringing the water\n"
	.string "back. Now let's see if your team\l"
	.string "can bloom in battle, too!$"

RustboroCity_Gym_Text_RoxanneDefeat:
	.string "NEVARD: Ha! You won, fair and\n"
	.string "square.\p"
	.string "Like any good crop, a trainer\n"
	.string "needs time to grow.\l"
	.string "Looks like you've had plenty.\p"
	.string "Take the HARVEST BADGE!$"

RustboroCity_Gym_Text_ReceivedStoneBadge:
	.string "{PLAYER} received the HARVEST\n"
	.string "BADGE from NEVARD!$"

RustboroCity_Gym_Text_StoneBadgeInfoTakeThis:
	.string "NEVARD: Your first BADGE. Hold on\n"
	.string "to that feeling.\p"
	.string "And take this, too!$"

RustboroCity_Gym_Text_ExplainRockTomb:
	.string "NEVARD: That TM teaches BULLET\n"
	.string "SEED.\p"
	.string "It fires a burst of seeds, two to\n"
	.string "five times in a row!$"

RustboroCity_Gym_Text_RoxannePostBattle:
	.string "NEVARD: The fields change every\n"
	.string "season, and so will you.\p"
	.string "Keep looking after your POKéMON.\n"
	.string "They'll look after you.$"

RustboroCity_Gym_Text_GymStatue:
	.string "HARVESTVALE POKéMON GYM\n"
	.string "LEADER: NEVARD$"

RustboroCity_Gym_Text_GymStatueCertified:
	.string "HARVESTVALE POKéMON GYM\p"
	.string "NEVARD'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

RustboroCity_Gym_Text_RoxanneRegisterCall:
	.string "NEVARD: See you next harvest,\n"
	.string "{PLAYER}!$"

RustboroCity_Gym_Text_RegisteredRoxanne:
	.string "Registered NEVARD in the POKéNAV.$"

RustboroCity_Gym_Text_RoxannePreRematch:
	.string "NEVARD: Welcome back!\n"
	.string "Ready for another round?$"

RustboroCity_Gym_Text_RoxanneRematchDefeat:
	.string "NEVARD: Great battle!$"

RustboroCity_Gym_Text_RoxannePostRematch:
	.string "NEVARD: Come back anytime!$"

RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons:
	.string "NEVARD: Come back with at least\n"
	.string "two POKéMON for a rematch.$"

Palm067_Enter::
	setvar VAR_TEMP_8, 0
	end

Palm067_CheckClear::
	goto_if_unset FLAG_DEFEATED_RUSTBORO_GYM, Palm067_NotClear
	goto_if_not_defeated TRAINER_ROXANNE_1, Palm067_NotClear
	setvar VAR_RESULT, TRUE
	return

Palm067_NotClear::
	setvar VAR_RESULT, FALSE
	return

Palm065_Load::
	call Palm067_CheckClear
	goto_if_eq VAR_RESULT, TRUE, Palm065_LoadSolved
	goto_if_lt VAR_TEMP_8, 1, Palm067_LoadDone
	call Palm065_Water1
	goto_if_lt VAR_TEMP_8, 2, Palm067_LoadDone
	goto_if_not_defeated TRAINER_JOSH, Palm067_LoadFirstOnly
	call Palm065_Water2
	goto_if_lt VAR_TEMP_8, 3, Palm067_LoadDone
	goto_if_not_defeated TRAINER_TOMMY, Palm067_LoadSecondOnly
	call Palm065_Water3
	end

Palm067_LoadFirstOnly::
	setvar VAR_TEMP_8, 1
	end

Palm067_LoadSecondOnly::
	setvar VAR_TEMP_8, 2
	end

Palm067_LoadDone::
	end

Palm065_LoadSolved::
	setvar VAR_TEMP_8, 3
	call Palm065_Water1
	call Palm065_Water2
	call Palm065_Water3
	end

Palm065_Water1::
	setmetatile 3, 15, 653, TRUE
	setmetatile 3, 16, 654, TRUE
	return

Palm065_Gate1::
	lockall
	goto_if_ge VAR_TEMP_8, 1, Palm065_AlreadyOpen
	goto_if_ne VAR_TEMP_8, 0, Palm065_Wait
	setvar VAR_TEMP_8, 1
	call Palm065_Water1
	special DrawWholeMapView
	msgbox Palm065_Text1, MSGBOX_DEFAULT
	releaseall
	end

Palm065_Water2::
	setmetatile 7, 11, 655, TRUE
	setmetatile 7, 12, 656, TRUE
	setmetatile 7, 13, 657, TRUE
	return

Palm065_Gate2::
	lockall
	goto_if_ge VAR_TEMP_8, 2, Palm065_AlreadyOpen
	goto_if_ne VAR_TEMP_8, 1, Palm065_Wait
	goto_if_not_defeated TRAINER_JOSH, Palm066_Battle1
	setvar VAR_TEMP_8, 2
	call Palm065_Water2
	special DrawWholeMapView
	msgbox Palm065_Text2, MSGBOX_DEFAULT
	releaseall
	end

Palm065_Water3::
	setmetatile 3, 7, 658, TRUE
	setmetatile 3, 8, 659, TRUE
	setmetatile 3, 9, 654, TRUE
	setmetatile 4, 5, 660, FALSE
	setmetatile 5, 5, 661, FALSE
	setmetatile 6, 5, 662, FALSE
	return

Palm065_Gate3::
	lockall
	goto_if_ge VAR_TEMP_8, 3, Palm065_AlreadyOpen
	goto_if_ne VAR_TEMP_8, 2, Palm065_Wait
	goto_if_not_defeated TRAINER_TOMMY, Palm066_Battle2
	setvar VAR_TEMP_8, 3
	call Palm065_Water3
	special DrawWholeMapView
	msgbox Palm065_Text3, MSGBOX_DEFAULT
	releaseall
	end

Palm066_Battle1::
	msgbox Palm066_TextBattle1, MSGBOX_DEFAULT
	releaseall
	end

Palm066_Battle2::
	msgbox Palm066_TextBattle2, MSGBOX_DEFAULT
	releaseall
	end

Palm066_TextBattle1:
	.string "Beat the grower beside the\n"
	.string "field on the right.$"
Palm066_TextBattle2:
	.string "Beat the grower beside the\n"
	.string "field on the left.$"

Palm065_AlreadyOpen::
	msgbox Palm065_TextOpen, MSGBOX_DEFAULT
	releaseall
	end

Palm065_Wait::
	msgbox Palm065_TextWait, MSGBOX_DEFAULT
	releaseall
	end

Palm065_Text1:
	.string "FLOODGATE 1\n"
	.string "Water reaches the seedlings.$"
Palm065_Text2:
	.string "FLOODGATE 2\n"
	.string "Water reaches the grown trees.$"
Palm065_Text3:
	.string "FLOODGATE 3\n"
	.string "The bridge lowers. NEVARD awaits!$"
Palm065_TextOpen:
	.string "Water flows through this channel.$"
Palm065_TextWait:
	.string "No pressure in this channel yet.\n"
	.string "Ask the guide about the order.$"
