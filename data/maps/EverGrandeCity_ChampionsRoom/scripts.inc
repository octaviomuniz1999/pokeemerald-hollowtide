EverGrandeCity_ChampionsRoom_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, EverGrandeCity_ChampionsRoom_OnWarp
	map_script MAP_SCRIPT_ON_FRAME_TABLE, EverGrandeCity_ChampionsRoom_OnFrame
	.byte 0

EverGrandeCity_ChampionsRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, EverGrandeCity_ChampionsRoom_EventScript_PlayerTurnNorth
	.2byte 0

EverGrandeCity_ChampionsRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

EverGrandeCity_ChampionsRoom_OnFrame:
	map_script_2 VAR_TEMP_1, 0, EverGrandeCity_ChampionsRoom_EventScript_EnterRoom
	.2byte 0

EverGrandeCity_ChampionsRoom_EventScript_EnterRoom::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkUp4
	waitmovement 0
	delay 40
	applymovement LOCALID_PLAYER, EverGrandeCity_ChampionsRoom_Movement_PlayerApproachChampion
	waitmovement 0
	setvar VAR_TEMP_1, 1
	goto EverGrandeCity_ChampionsRoom_EventScript_Doge
	releaseall
	end

EverGrandeCity_ChampionsRoom_Movement_PlayerApproachChampion:
	walk_up
	walk_up
	step_end

EverGrandeCity_ChampionsRoom_EventScript_Doge::
	playbgm MUS_ENCOUNTER_CHAMPION, FALSE
	msgbox EverGrandeCity_ChampionsRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_WALLACE, EverGrandeCity_ChampionsRoom_Text_Defeat
	goto EverGrandeCity_ChampionsRoom_EventScript_Defeated
	end

EverGrandeCity_ChampionsRoom_EventScript_Defeated::
	playse SE_DOOR
	setmetatile 6, 1, METATILE_EliteFour_OpenDoorChampion_Frame, FALSE
	setmetatile 6, 2, METATILE_EliteFour_OpenDoorChampion_Opening, FALSE
	special DrawWholeMapView
	msgbox EverGrandeCity_ChampionsRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CHAMPIONS_ROOM_WALLACE, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	delay 20
	applymovement LOCALID_CHAMPIONS_ROOM_WALLACE, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox EverGrandeCity_ChampionsRoom_Text_ComeWithMe, MSGBOX_DEFAULT
	closemessage
	delay 30
	applymovement LOCALID_CHAMPIONS_ROOM_WALLACE, EverGrandeCity_ChampionsRoom_Movement_ChampionExit
	applymovement LOCALID_PLAYER, EverGrandeCity_ChampionsRoom_Movement_PlayerExit
	waitmovement 0
	setflag FLAG_HIDE_PETALBURG_GYM_GREETER
	warp MAP_EVER_GRANDE_CITY_HALL_OF_FAME, 7, 16
	waitstate
	releaseall
	end

EverGrandeCity_ChampionsRoom_Movement_PlayerExit:
	walk_up
	walk_up
	walk_up
	delay_16
	walk_up
	delay_8
	set_invisible
	step_end

EverGrandeCity_ChampionsRoom_Movement_ChampionExit:
	walk_up
	walk_up
	walk_up
	set_invisible
	step_end

EverGrandeCity_ChampionsRoom_Text_IntroSpeech:
	.string "DOGE: So you're {PLAYER}.\n"
	.string "I've heard a lot about you.\p"
	.string "Before I became CHAMPION, I lost to\n"
	.string "the old CHAMPION more times than I\l"
	.string "can count. He was my friend.\l"
	.string "My teacher.\p"
	.string "He didn't disappear because he lost\n"
	.string "the title.\p"
	.string "When I won, he looked happy for me.\n"
	.string "That's why I need to find out what\l"
	.string "happened to him.\p"
	.string "But that's my problem, not yours.\p"
	.string "If you want this position, come and\n"
	.string "take it. I won't make it easy.$"

EverGrandeCity_ChampionsRoom_Text_Defeat:
	.string "…That's it.\p"
	.string "No tricks, no luck.\n"
	.string "You earned it, {PLAYER}.$"

EverGrandeCity_ChampionsRoom_Text_PostBattleSpeech:
	.string "DOGE: The title is yours.\n"
	.string "Fair and square.\p"
	.string "From today, you are the CHAMPION\n"
	.string "of the LUNIA POKéMON LEAGUE.$"

EverGrandeCity_ChampionsRoom_Text_ComeWithMe:
	.string "DOGE: Come with me. There's a room\n"
	.string "where we honor CHAMPIONS…\p"
	.string "and the POKéMON who stood with them.$"
