OldaleTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Palm060_EnterHarvest
	map_script MAP_SCRIPT_ON_LOAD, Palm071_LoadDoor
	.byte 0

OldaleTown_OnTransition:
	call Common_EventScript_SetupRivalGfxId
	setflag FLAG_VISITED_OLDALE_TOWN
	call_if_unset FLAG_ADVENTURE_STARTED, OldaleTown_EventScript_BlockWestEntrance
	call_if_unset FLAG_RECEIVED_POTION_OLDALE, OldaleTown_EventScript_MoveMartEmployee
	call_if_set FLAG_ADVENTURE_STARTED, OldaleTown_EventScript_SetOldaleState
	end

@ This script seems pointless because nothing uses VAR_OLDALE_TOWN_STATE
OldaleTown_EventScript_SetOldaleState::
	setvar VAR_OLDALE_TOWN_STATE, 1
	return

OldaleTown_EventScript_BlockWestEntrance::
	setobjectxyperm LOCALID_FOOTPRINTS_MAN, 1, 11
	setobjectmovementtype LOCALID_FOOTPRINTS_MAN, MOVEMENT_TYPE_FACE_LEFT
	return

OldaleTown_EventScript_MoveMartEmployee::
	setobjectxyperm LOCALID_OLDALE_MART_EMPLOYEE, 13, 14
	setobjectmovementtype LOCALID_OLDALE_MART_EMPLOYEE, MOVEMENT_TYPE_FACE_DOWN
	return

OldaleTown_EventScript_TownSign::
	msgbox OldaleTown_Text_TownSign, MSGBOX_SIGN
	end

OldaleTown_EventScript_Girl::
	msgbox OldaleTown_Text_SavingMyProgress, MSGBOX_NPC
	end

OldaleTown_EventScript_MartEmployee::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_POTION_OLDALE, OldaleTown_EventScript_ExplainPotion
	goto_if_set FLAG_TEMP_1, OldaleTown_EventScript_ExplainPotion
	setflag FLAG_TEMP_1
	playbgm MUS_FOLLOW_ME, FALSE
	msgbox OldaleTown_Text_IWorkAtPokemonMart, MSGBOX_DEFAULT
	closemessage
	switch VAR_FACING
	case DIR_SOUTH, OldaleTown_EventScript_GoToMartSouth
	case DIR_NORTH, OldaleTown_EventScript_GoToMartNorth
	case DIR_EAST, OldaleTown_EventScript_GoToMartEast
	end

OldaleTown_EventScript_GoToMartSouth::
	applymovement LOCALID_OLDALE_MART_EMPLOYEE, OldaleTown_Movement_EmployeeSouth
	applymovement LOCALID_PLAYER, OldaleTown_Movement_PlayerSouth
	waitmovement 0
	goto OldaleTown_EventScript_ExplainPokemonMart
	end

OldaleTown_EventScript_GoToMartNorth::
	applymovement LOCALID_OLDALE_MART_EMPLOYEE, OldaleTown_Movement_EmployeeNorth
	applymovement LOCALID_PLAYER, OldaleTown_Movement_PlayerNorth
	waitmovement 0
	goto OldaleTown_EventScript_ExplainPokemonMart
	end

OldaleTown_EventScript_GoToMartEast::
	applymovement LOCALID_PLAYER, OldaleTown_Movement_PlayerEast
	applymovement LOCALID_OLDALE_MART_EMPLOYEE, OldaleTown_Movement_EmployeeEast
	waitmovement 0
	goto OldaleTown_EventScript_ExplainPokemonMart
	end

OldaleTown_EventScript_ExplainPokemonMart::
	msgbox OldaleTown_Text_ThisIsAPokemonMart, MSGBOX_DEFAULT
	giveitem ITEM_POTION
	goto_if_eq VAR_RESULT, FALSE, OldaleTown_EventScript_BagIsFull
	msgbox OldaleTown_Text_PotionExplanation, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_POTION_OLDALE
	fadedefaultbgm
	release
	end

OldaleTown_EventScript_ExplainPotion::
	msgbox OldaleTown_Text_PotionExplanation, MSGBOX_DEFAULT
	release
	end

OldaleTown_EventScript_BagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	fadedefaultbgm
	release
	end

OldaleTown_Movement_EmployeeEast:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_in_place_faster_down
	step_end

OldaleTown_Movement_EmployeeSouth:
	walk_left
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_in_place_faster_down
	step_end

OldaleTown_Movement_EmployeeNorth:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_in_place_faster_down
	step_end

OldaleTown_Movement_Unknown1:
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	delay_8
	walk_in_place_faster_down
	step_end

OldaleTown_Movement_PlayerEast:
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

OldaleTown_Movement_PlayerSouth:
	delay_16
	delay_16
	delay_16
	delay_16
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

OldaleTown_Movement_PlayerNorth:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

OldaleTown_Movement_Unknown2:
	walk_left
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

OldaleTown_EventScript_FootprintsMan::
	lock
	faceplayer
	goto_if_set FLAG_ADVENTURE_STARTED, OldaleTown_EventScript_NotBlockingPath
	msgbox OldaleTown_Text_DiscoveredFootprints, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FOOTPRINTS_MAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

OldaleTown_EventScript_BlockedPath::
	lockall
	applymovement LOCALID_PLAYER, OldaleTown_Movement_PlayerStepBack
	applymovement LOCALID_FOOTPRINTS_MAN, OldaleTown_Movement_BackUp
	waitmovement 0
	msgbox OldaleTown_Text_WaitDontComeInHere, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_FOOTPRINTS_MAN, OldaleTown_Movement_ReturnToOriginalPosition
	waitmovement 0
	releaseall
	end

OldaleTown_EventScript_NotBlockingPath::
	msgbox OldaleTown_Text_FinishedSketchingFootprints, MSGBOX_DEFAULT
	release
	end

OldaleTown_EventScript_Rival::
	lockall
	applymovement LOCALID_OLDALE_RIVAL, Common_Movement_FacePlayer
	waitmovement 0
	setvar VAR_0x8009, 0
	goto OldaleTown_EventScript_ShowRivalMessage
	end

OldaleTown_EventScript_RivalTrigger1::
	lockall
	applymovement LOCALID_OLDALE_RIVAL, OldaleTown_Movement_RivalApproachPlayer1
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	setvar VAR_0x8009, 1
	goto OldaleTown_EventScript_ShowRivalMessage
	end

OldaleTown_EventScript_RivalTrigger2::
	lockall
	applymovement LOCALID_OLDALE_RIVAL, OldaleTown_Movement_RivalApproachPlayer2
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	setvar VAR_0x8009, 1
	goto OldaleTown_EventScript_ShowRivalMessage
	end

OldaleTown_EventScript_RivalTrigger3::
	lockall
	applymovement LOCALID_OLDALE_RIVAL, OldaleTown_Movement_RivalApproachPlayer3
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	setvar VAR_0x8009, 1
	goto OldaleTown_EventScript_ShowRivalMessage
	end

OldaleTown_EventScript_ShowRivalMessage::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, OldaleTown_EventScript_ShowMayMessage
	goto_if_eq VAR_RESULT, FEMALE, OldaleTown_EventScript_ShowBrendanMessage
	end

OldaleTown_EventScript_ShowMayMessage::
	msgbox OldaleTown_Text_MayLetsGoBack, MSGBOX_DEFAULT
	goto OldaleTown_EventScript_RivalFinish
	end

OldaleTown_EventScript_ShowBrendanMessage::
	msgbox OldaleTown_Text_BrendanLetsGoBack, MSGBOX_DEFAULT
	goto OldaleTown_EventScript_RivalFinish
	end

OldaleTown_EventScript_RivalFinish::
	closemessage
	call_if_eq VAR_0x8009, 0, OldaleTown_EventScript_DoExitMovement1
	call_if_eq VAR_0x8009, 1, OldaleTown_EventScript_DoExitMovement2
	applymovement LOCALID_OLDALE_RIVAL, OldaleTown_Movement_RivalExit
	waitmovement 0
	removeobject LOCALID_OLDALE_RIVAL
	setvar VAR_OLDALE_RIVAL_STATE, 2
	setflag FLAG_HIDE_OLDALE_TOWN_RIVAL
	releaseall
	end

OldaleTown_EventScript_DoExitMovement1::
	goto_if_ne VAR_FACING, DIR_SOUTH, OldaleTown_EventScript_DoExitMovement2
	applymovement LOCALID_OLDALE_RIVAL, OldaleTown_Movement_RivalExit
	waitmovement 0
	return

OldaleTown_EventScript_DoExitMovement2::
	applymovement LOCALID_PLAYER, OldaleTown_Movement_WatchRivalExit
	applymovement LOCALID_OLDALE_RIVAL, OldaleTown_Movement_RivalExit
	waitmovement 0
	return

OldaleTown_Movement_RivalApproachPlayer1:
	walk_left
	walk_left
	step_end

OldaleTown_Movement_RivalApproachPlayer2:
	walk_left
	step_end

OldaleTown_Movement_RivalApproachPlayer3:
	face_left
	step_end

OldaleTown_Movement_RivalExit:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

OldaleTown_Movement_WatchRivalExit:
	delay_8
	delay_4
	walk_in_place_faster_down
	step_end

OldaleTown_Movement_PlayerStepBack:
	delay_8
	walk_right
	step_end

OldaleTown_Movement_BackUp:
	walk_fast_up
	walk_in_place_faster_left
	lock_facing_direction
	walk_right
	unlock_facing_direction
	step_end

OldaleTown_Movement_ReturnToOriginalPosition:
	walk_down
	walk_left
	step_end

OldaleTown_Text_SavingMyProgress:
	.string "Todo mundo aqui ajuda nas\n"
	.string "plantacoes de cafe.\p"
	.string "O NEVARD e nosso lider de GINASIO!$"

OldaleTown_Text_IWorkAtPokemonMart:
	.string "Hi!\n"
	.string "I work at a POKéMON MART.\p"
	.string "Can I get you to come with me?$"

OldaleTown_Text_ThisIsAPokemonMart:
	.string "This is a POKéMON MART.\n"
	.string "Just look for our blue roof.\p"
	.string "We sell a variety of goods including\n"
	.string "POKé BALLS for catching POKéMON.\p"
	.string "Here, I'd like you to have this as\n"
	.string "a promotional item.$"

OldaleTown_Text_PotionExplanation:
	.string "A POTION can be used anytime, so it's\n"
	.string "even more useful than a POKéMON CENTER\l"
	.string "in certain situations.$"

OldaleTown_Text_WaitDontComeInHere:
	.string "Espere! Estou procurando\n"
	.string "POKéMON nos cafezais.\p"
	.string "Volte mais tarde!$"

OldaleTown_Text_DiscoveredFootprints:
	.string "Estou seguindo rastros de\n"
	.string "POKéMON nas plantacoes.\p"
	.string "Nao da para passar daqui agora.$"

OldaleTown_Text_FinishedSketchingFootprints:
	.string "I finished sketching the footprints of\n"
	.string "a rare POKéMON.\p"
	.string "But it turns out they were only my\n"
	.string "own footprints…$"

OldaleTown_Text_MayLetsGoBack:
	.string "MAY: {PLAYER}{KUN}!\n"
	.string "Over here!\l"
	.string "Let's hurry home!$"

OldaleTown_Text_BrendanLetsGoBack:
	.string "BRENDAN: I'm heading back to my dad's\n"
	.string "LAB now.\l"
	.string "{PLAYER}, you should hustle back, too.$"

OldaleTown_Text_TownSign:
	.string "VILA DA COLHEITA\n"
	.string "Cafe, terra e trabalho.$"


@ Pokemon PALM: identificacao da porta temporaria do ginasio.
PokemonPalm_EventScript_ColheitaGymSign::
	msgbox PokemonPalm_Text_ColheitaGymSign, MSGBOX_SIGN
	end

PokemonPalm_Text_ColheitaGymSign:
	.string "GINASIO DA COLHEITA\n"
	.string "LIDER NEVARD - TIPO GRAMA\p"
	.string "A entrada fica nesta casa.$"

@ PALM: exterior da Vila da Colheita
Palm060_EnterHarvest::
	call_if_set FLAG_DEFEATED_RUSTBORO_GYM, Palm071_Migrate
	setflag FLAG_VISITED_OLDALE_TOWN
	setflag FLAG_UNUSED_0x021
	end

Palm060_Farmer::
	goto_if_set FLAG_PALM_IRRIGATION_RESTORED, Palm071_FarmerRestored
	msgbox Palm071_TextFarmer, MSGBOX_NPC
	end

Palm060_Kiosk::
	goto_if_set FLAG_PALM_IRRIGATION_RESTORED, Palm073_RecruitRestored
	goto_if_defeated TRAINER_PALM_IRRIGATION_RECRUIT, Palm072_RecruitReminder
	trainerbattle_single TRAINER_PALM_IRRIGATION_RECRUIT, Palm071_TextRecruit, Palm071_TextRecruitLoss
	release
	end

Palm073_RecruitRestored::
	msgbox Palm073_TextRecruitRestored, MSGBOX_NPC
	end

Palm072_RecruitReminder::
	msgbox Palm072_TextValveHint, MSGBOX_NPC
	end

Palm072_Arrival::
	setvar VAR_TEMP_8, 1
	goto_if_set FLAG_PALM_IRRIGATION_RESTORED, Palm072_ArrivalDone
	goto_if_set FLAG_PALM_COLHEITA_GUIDE_INTRO, Palm072_ArrivalDone
	lockall
	setflag FLAG_PALM_COLHEITA_GUIDE_INTRO
	applymovement LOCALID_PALM_COLHEITA_GUIDE, Palm073_GuideNotice
	waitmovement LOCALID_PALM_COLHEITA_GUIDE
	goto_if_defeated TRAINER_PALM_IRRIGATION_RECRUIT, Palm072_ArrivalValve
	msgbox Palm072_TextArrival, MSGBOX_DEFAULT
	releaseall
	end

Palm072_ArrivalValve::
	msgbox Palm072_TextValveHint, MSGBOX_DEFAULT
	releaseall
	end

Palm072_ArrivalDone::
	end

Palm060_Welcome::
	msgbox Palm060_TextWelcome, MSGBOX_SIGN
	end

Palm060_ClosedRoad::
	goto_if_set FLAG_DEFEATED_RUSTBORO_GYM, Palm080_ColheitaRouteOpen
	msgbox Palm060_TextClosedRoad, MSGBOX_SIGN
	end

Palm060_KioskSign::
	msgbox Palm060_TextKioskSign, MSGBOX_SIGN
	end

Palm060_GymSign::
	goto_if_set FLAG_PALM_IRRIGATION_RESTORED, Palm071_GymOpen
	msgbox Palm071_TextGymLocked, MSGBOX_SIGN
	end

Palm060_TextGymSign:
	.string "GINASIO DA COLHEITA\n"
	.string "LIDER: NEVARD.$"

Palm060_TextFarmer:
	.string "O canal leva agua aos cafezais.\n"
	.string "O ginasio do NEVARD fica a leste.$"

Palm060_TextKiosk:
	.string "A TEAM PALM anda de olho na agua\n"
	.string "que passa pelos cafezais.$"

Palm060_TextWelcome:
	.string "VILA DA COLHEITA\n"
	.string "Norte: ROTA 01.\n"
	.string "Sudeste: QUIOSQUE DA TEAM PALM.$"

Palm060_TextClosedRoad:
	.string "ROTA 02\n"
	.string "A passagem abre depois de Nevard.$"

Palm060_TextKioskSign:
	.string "QUIOSQUE DA TEAM PALM\p"
	.string "Controle de agua e irrigacao.$"


Palm062_CoffeeSign::
	msgbox Palm062_CoffeeText, MSGBOX_SIGN
	end

Palm062_WaterSign::
	lockall
	goto_if_set FLAG_PALM_IRRIGATION_RESTORED, Palm071_ValveRestored
	goto_if_not_defeated TRAINER_PALM_IRRIGATION_RECRUIT, Palm071_ValveLocked
	playse SE_SWITCH
	setflag FLAG_PALM_IRRIGATION_RESTORED
	call Palm071_OpenDoor
	special DrawWholeMapView
	msgbox Palm071_TextRestored, MSGBOX_DEFAULT
	releaseall
	end

Palm062_CoffeeText:
	.string "CAFEZAIS DA COLHEITA\n"
	.string "A agua do canal irriga os canteiros.$"

Palm062_WaterText:
	.string "CANAL COMUNITARIO\n"
	.string "A agua e partilhada entre as rocas.$"

Palm064_DryingYard::
	msgbox Palm064_DryingYard_Text, MSGBOX_SIGN
	end

Palm064_DryingYard_Text:
	.string "TERREIRO DE SECAGEM\n"
	.string "Os graos ficam no sol.\p"
	.string "Quando a chuva chega, a vila\n"
	.string "corre para recolher as esteiras!$"

Palm064_WaterBoard::
	msgbox Palm064_WaterBoard_Text, MSGBOX_SIGN
	end

Palm064_WaterBoard_Text:
	.string "QUADRO DA IRRIGACAO\n"
	.string "Cada canteiro tem a sua vez.\p"
	.string "Um folheto da TEAM PALM cobre\n"
	.string "parte da escala: AGUA SOB CONTRATO.$"

Palm071_LoadDoor::
	call_if_set FLAG_DEFEATED_RUSTBORO_GYM, Palm071_Migrate
	goto_if_unset FLAG_PALM_IRRIGATION_RESTORED, Palm071_LockDoor
	call Palm071_OpenDoor
	end

Palm071_LockDoor::
	setmetatile 5, 21, 918, TRUE
	end

Palm071_OpenDoor::
	setmetatile 5, 21, 461, TRUE
	return

Palm071_Migrate::
	setflag FLAG_PALM_IRRIGATION_RESTORED
	setflag FLAG_PALM_HIDE_IRRIGATION_RECRUIT
	return

Palm071_FarmerRestored::
	msgbox Palm071_TextFarmerRestored, MSGBOX_NPC
	end

Palm071_GymOpen::
	msgbox Palm060_TextGymSign, MSGBOX_SIGN
	end

Palm071_ValveLocked::
	msgbox Palm071_TextValveLocked, MSGBOX_DEFAULT
	releaseall
	end

Palm071_ValveRestored::
	msgbox Palm071_TextValveRestored, MSGBOX_DEFAULT
	releaseall
	end

Palm071_TextFarmer:
	.string "A PALM fechou a valvula do canal.\p"
	.string "Quer cobrar pela agua que sempre\n"
	.string "foi de todos. O recruta esta no\n"
	.string "quiosque, ao sul.$"

Palm071_TextRecruit:
	.string "A TEAM PALM agora cuida da agua.\p"
	.string "Quer irrigar sem assinar contrato?\n"
	.string "Vai ter que passar por mim!$"

Palm071_TextRecruitLoss:
	.string "Tome a chave da valvula!\n"
	.string "Ela fica junto ao canal, a leste.$"

Palm073_GuideNotice:
	face_left
	emote_exclamation_mark
	step_end

Palm073_TextRecruitRestored:
	.string "A TEAM PALM vai rever o contrato.$"

Palm072_TextArrival:
	.string "MORADORA: Ei, voce!\p"
	.string "A TEAM PALM fechou a valvula.\n"
	.string "O ginasio ficou sem agua.\p"
	.string "O recruta com a chave esta no\n"
	.string "quiosque azul, ao sudoeste.$"

Palm072_TextValveHint:
	.string "Com a chave, abra a valvula.\p"
	.string "Procure a valvula na margem\n"
	.string "oeste do canal, perto do cafezal.$"

Palm071_TextGymLocked:
	.string "GINASIO DA COLHEITA\p"
	.string "O ginasio reabre quando a agua\n"
	.string "voltar aos cafezais.$"

Palm071_TextValveLocked:
	.string "A valvula esta travada.\p"
	.string "O recruta do quiosque azul\n"
	.string "esta com a chave.$"

Palm071_TextRestored:
	.string "Voce destravou a valvula!\p"
	.string "A agua voltou aos cafezais.\n"
	.string "Nevard abriu o ginasio.$"

Palm071_TextValveRestored:
	.string "A agua corre para os cafezais.$"

Palm071_TextFarmerRestored:
	.string "A agua chegou aos canteiros!\n"
	.string "Nevard espera voce no ginasio.$"

Palm080_LeaveColheita::
	goto_if_set FLAG_DEFEATED_RUSTBORO_GYM, Palm080_ToRoute02
	lockall
	msgbox Palm060_TextClosedRoad, MSGBOX_DEFAULT
	releaseall
	end

Palm080_ToRoute02::
	warp MAP_PALM_ROUTE02, 12, 2
	waitstate
	end

Palm080_ColheitaRouteOpen::
	msgbox Palm080_TextRouteOpen, MSGBOX_SIGN
	end

Palm080_TextRouteOpen:
	.string "ROTA 02\n"
	.string "Sul: CIDADE DA BRISA.$"
