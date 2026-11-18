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
	.string "A agua daqui alimenta os\n"
	.string "cafezais da vila.\p"
	.string "Abra as comportas numeradas\n"
	.string "de 1 a 3.\p"
	.string "Pelo caminho, venca os dois\n"
	.string "treinadores do cafezal.$"

RustboroCity_Gym_Text_GymGuidePostVictory:
	.string "Parabens por vencer o NEVARD!\n"
	.string "A VILA DA COLHEITA agradece!$"

RustboroCity_Gym_Text_JoshIntro:
	.string "Eu trabalho com o NEVARD!\n"
	.string "Vamos ver sua equipe!$"

RustboroCity_Gym_Text_JoshDefeat:
	.string "Preciso cuidar mais das plantas...$"

RustboroCity_Gym_Text_JoshPostBattle:
	.string "Nevard conhece cada arvore daqui!$"

RustboroCity_Gym_Text_TommyIntro:
	.string "O cafe cresce com paciencia!\n"
	.string "Minha equipe tambem!$"

RustboroCity_Gym_Text_TommyDefeat:
	.string "Esta foi uma boa colheita...$"

RustboroCity_Gym_Text_TommyPostBattle:
	.string "O NEVARD e muito mais forte!$"

RustboroCity_Gym_Text_MarcIntro:
	.string "Na nossa terra, a forca vem\n"
	.string "das raizes!$"

RustboroCity_Gym_Text_MarcDefeat:
	.string "Minhas raizes enfraqueceram!$"

RustboroCity_Gym_Text_MarcPostBattle:
	.string "Treinar no cafezal da resultado.$"

RustboroCity_Gym_Text_RoxanneIntro:
	.string "NEVARD: Bem-vindo a COLHEITA!\p"
	.string "Cuido do cafe e dos POKéMON\n"
	.string "que vivem nestas terras.\p"
	.string "Mostre se sua equipe tambem\n"
	.string "pode florescer numa batalha!$"

RustboroCity_Gym_Text_RoxanneDefeat:
	.string "NEVARD: Voce venceu!\p"
	.string "Assim como uma boa plantacao,\n"
	.string "um treinador precisa crescer.\p"
	.string "Receba a INSIGNIA COLHEITA!$"

RustboroCity_Gym_Text_ReceivedStoneBadge:
	.string "{PLAYER} recebeu a INSIGNIA\n"
	.string "COLHEITA de NEVARD!$"

RustboroCity_Gym_Text_StoneBadgeInfoTakeThis:
	.string "A primeira insignia prova que\n"
	.string "voce e um grande treinador!\p"
	.string "Ela permite usar CUT fora de\n"
	.string "batalha. Pegue esta TM!$"

RustboroCity_Gym_Text_ExplainRockTomb:
	.string "Esta TM ensina BULLET SEED.\p"
	.string "Use o poder das sementes\n"
	.string "para enfrentar novos desafios!$"

RustboroCity_Gym_Text_RoxannePostBattle:
	.string "NEVARD: O campo sempre muda.\p"
	.string "Continue treinando e cuidando\n"
	.string "dos seus POKéMON!$"

RustboroCity_Gym_Text_GymStatue:
	.string "VILA DA COLHEITA - GINASIO\n"
	.string "LIDER NEVARD$"

RustboroCity_Gym_Text_GymStatueCertified:
	.string "VILA DA COLHEITA - GINASIO\p"
	.string "NEVARD APROVA: {PLAYER}$"

RustboroCity_Gym_Text_RoxanneRegisterCall:
	.string "NEVARD: Ate a proxima\n"
	.string "colheita, {PLAYER}!$"

RustboroCity_Gym_Text_RegisteredRoxanne:
	.string "Registrado NEVARD no POKéNAV.$"

RustboroCity_Gym_Text_RoxannePreRematch:
	.string "NEVARD: Bem-vindo de volta!\n"
	.string "Vamos lutar novamente?$"

RustboroCity_Gym_Text_RoxanneRematchDefeat:
	.string "NEVARD: Boa batalha!$"

RustboroCity_Gym_Text_RoxannePostRematch:
	.string "NEVARD: Ate outra vez!$"

RustboroCity_Gym_Text_RoxanneRematchNeedTwoMons:
	.string "NEVARD: Volte com pelo menos\n"
	.string "dois POKéMON para a revanche.$"

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
	.string "Venca o treinador ao lado\n"
	.string "do canteiro da direita.$"
Palm066_TextBattle2:
	.string "Venca o treinador ao lado\n"
	.string "do canteiro da esquerda.$"

Palm065_AlreadyOpen::
	msgbox Palm065_TextOpen, MSGBOX_DEFAULT
	releaseall
	end

Palm065_Wait::
	msgbox Palm065_TextWait, MSGBOX_DEFAULT
	releaseall
	end

Palm065_Text1:
	.string "COMPORTA 1\n"
	.string "A agua chegou as mudas.$"
Palm065_Text2:
	.string "COMPORTA 2\n"
	.string "A agua chegou aos pes adultos.$"
Palm065_Text3:
	.string "COMPORTA 3\n"
	.string "A ponte desceu. Nevard espera!$"
Palm065_TextOpen:
	.string "A agua corre por este canal.$"
Palm065_TextWait:
	.string "Sem pressao neste canal.\n"
	.string "Confira a ordem com o guia.$"
