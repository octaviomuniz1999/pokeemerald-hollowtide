FortreeCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FortreeCity_Gym_OnTransition
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, FortreeCity_Gym_OnWarp
	.byte 0

FortreeCity_Gym_OnTransition:
	special RotatingGate_InitPuzzle
	setflag FLAG_TEMP_HIDE_FOLLOWER @ Hide follower bc of rotating gates
	end

FortreeCity_Gym_OnWarp:
	map_script_2 VAR_TEMP_0, VAR_TEMP_0, FortreeCity_Gym_EventScript_InitRotatingGates
	.2byte 0

@ NOTE: This rotating gate puzzle makes use of VAR_TEMP_0 - VAR_TEMP_3
FortreeCity_Gym_EventScript_InitRotatingGates::
	special RotatingGate_InitPuzzleAndGraphics
	end

FortreeCity_Gym_EventScript_Winona::
	trainerbattle_single TRAINER_WINONA_1, FortreeCity_Gym_Text_WinonaIntro, FortreeCity_Gym_Text_WinonaDefeat, FortreeCity_Gym_EventScript_WinonaDefeated, NO_MUSIC
	specialvar VAR_RESULT, ShouldTryRematchBattle
	goto_if_eq VAR_RESULT, TRUE, FortreeCity_Gym_EventScript_WinonaRematch
	msgbox FortreeCity_Gym_Text_WinonaPostBattle, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_WinonaDefeated::
	message FortreeCity_Gym_Text_ReceivedFeatherBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox FortreeCity_Gym_Text_ExplainFeatherBadgeTakeThis, MSGBOX_DEFAULT
	giveitem ITEM_TM_BULLDOZE
	msgbox FortreeCity_Gym_Text_ExplainAerialAce, MSGBOX_DEFAULT
	setflag FLAG_DEFEATED_FORTREE_GYM
	setflag FLAG_BADGE04_GET
	setvar VAR_0x8008, 6
	call Common_EventScript_SetGymTrainers
	release
	end

FortreeCity_Gym_EventScript_GiveAerialAce2::
	giveitem ITEM_TM_AERIAL_ACE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox FortreeCity_Gym_Text_ExplainAerialAce, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_AERIAL_ACE
	release
	end

FortreeCity_Gym_EventScript_GiveAerialAce::
	giveitem ITEM_TM_AERIAL_ACE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox FortreeCity_Gym_Text_ExplainAerialAce, MSGBOX_DEFAULT
	setflag FLAG_RECEIVED_TM_AERIAL_ACE
	return

FortreeCity_Gym_EventScript_WinonaRematch::
	trainerbattle_rematch_double TRAINER_WINONA_1, FortreeCity_Gym_Text_WinonaPreRematch, FortreeCity_Gym_Text_WinonaRematchDefeat, FortreeCity_Gym_Text_WinonaRematchNeedTwoMons
	msgbox FortreeCity_Gym_Text_WinonaPostRematch, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Jared::
	trainerbattle_single TRAINER_JARED, FortreeCity_Gym_Text_JaredIntro, FortreeCity_Gym_Text_JaredDefeat
	msgbox FortreeCity_Gym_Text_JaredPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Edwardo::
	trainerbattle_single TRAINER_EDWARDO, FortreeCity_Gym_Text_EdwardoIntro, FortreeCity_Gym_Text_EdwardoDefeat
	msgbox FortreeCity_Gym_Text_EdwardoPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Flint::
	trainerbattle_single TRAINER_FLINT, FortreeCity_Gym_Text_FlintIntro, FortreeCity_Gym_Text_FlintDefeat
	msgbox FortreeCity_Gym_Text_FlintPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Ashley::
	trainerbattle_single TRAINER_ASHLEY, FortreeCity_Gym_Text_AshleyIntro, FortreeCity_Gym_Text_AshleyDefeat
	msgbox FortreeCity_Gym_Text_AshleyPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Humberto::
	trainerbattle_single TRAINER_HUMBERTO, FortreeCity_Gym_Text_HumbertoIntro, FortreeCity_Gym_Text_HumbertoDefeat
	msgbox FortreeCity_Gym_Text_HumbertoPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_Darius::
	trainerbattle_single TRAINER_DARIUS, FortreeCity_Gym_Text_DariusIntro, FortreeCity_Gym_Text_DariusDefeat
	msgbox FortreeCity_Gym_Text_DariusPostBattle, MSGBOX_AUTOCLOSE
	end

FortreeCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_FORTREE_GYM, FortreeCity_Gym_EventScript_GymGuidePostVictory
	msgbox FortreeCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_GymGuidePostVictory::
	msgbox FortreeCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

FortreeCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_BADGE04_GET, FortreeCity_Gym_EventScript_GymStatueCertified
	goto FortreeCity_Gym_EventScript_GymStatue
	end

FortreeCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_BADGE04_GET, FortreeCity_Gym_EventScript_GymStatueCertified
	goto FortreeCity_Gym_EventScript_GymStatue
	end

FortreeCity_Gym_EventScript_GymStatueCertified::
	msgbox FortreeCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

FortreeCity_Gym_EventScript_GymStatue::
	msgbox FortreeCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

FortreeCity_Gym_Text_GymGuideAdvice:
	.string "Hey, future CHAMPION {PLAYER}!\p"
	.string "TCHUM, the LEADER of PILLARTON GYM,\n"
	.string "uses GROUND-type POKéMON.\p"
	.string "WATER and GRASS moves soak right\n"
	.string "into them. Electric moves? Useless!\p"
	.string "The turning gates here work like\n"
	.string "floodgates. Push them to open a path!$"

FortreeCity_Gym_Text_GymGuidePostVictory:
	.string "You beat TCHUM! Now that's what I\n"
	.string "call breaking new ground!$"

FortreeCity_Gym_Text_JaredIntro:
	.string "The gates are heavy, but my\n"
	.string "POKéMON are heavier!$"

FortreeCity_Gym_Text_JaredDefeat:
	.string "Buried...$"

FortreeCity_Gym_Text_JaredPostBattle:
	.string "Push a gate from the side of its\n"
	.string "arm, and it swings out of the way.$"

FortreeCity_Gym_Text_EdwardoIntro:
	.string "Bones, rocks and sand: the history\n"
	.string "of the earth is in my team!$"

FortreeCity_Gym_Text_EdwardoDefeat:
	.string "Ancient history now...$"

FortreeCity_Gym_Text_EdwardoPostBattle:
	.string "TCHUM's MAROWAK hits hard with its\n"
	.string "bone. Don't underestimate it!$"

FortreeCity_Gym_Text_FlintIntro:
	.string "I've been digging tunnels since I\n"
	.string "was a kid!$"

FortreeCity_Gym_Text_FlintDefeat:
	.string "Dead end...$"

FortreeCity_Gym_Text_FlintPostBattle:
	.string "If you get stuck in the gates, just\n"
	.string "walk out and come back. They reset!$"

FortreeCity_Gym_Text_AshleyIntro:
	.string "Mud pies are my specialty! Ready\n"
	.string "to get messy?$"

FortreeCity_Gym_Text_AshleyDefeat:
	.string "Splat!$"

FortreeCity_Gym_Text_AshleyPostBattle:
	.string "TCHUM laughs at all his own jokes.\n"
	.string "It's kind of sweet, honestly.$"

FortreeCity_Gym_Text_HumbertoIntro:
	.string "Solid rock, solid strategy!$"

FortreeCity_Gym_Text_HumbertoDefeat:
	.string "Cracked!$"

FortreeCity_Gym_Text_HumbertoPostBattle:
	.string "The dam held for a hundred years.\n"
	.string "Our GYM will hold too!$"

FortreeCity_Gym_Text_DariusIntro:
	.string "These ruins hold secrets... and\n"
	.string "so does my team!$"

FortreeCity_Gym_Text_DariusDefeat:
	.string "Secret revealed...$"

FortreeCity_Gym_Text_DariusPostBattle:
	.string "LARVITAR eats soil to grow. One day\n"
	.string "it'll be a mountain!$"

FortreeCity_Gym_Text_WinonaIntro:
	.string "So the hero of the dam made it\n"
	.string "through my floodgates!\p"
	.string "It's time for some TERapy.\p"
	.string "Promise me one thing: whatever\n"
	.string "happens, don't lose your footing!\p"
	.string "...Okay, that one was awful.\n"
	.string "I know. Let's battle!$"

FortreeCity_Gym_Text_WinonaDefeat:
	.string "You kept your feet on the ground\n"
	.string "the whole time. Impressive!\p"
	.string "Take the PILLAR BADGE!$"

FortreeCity_Gym_Text_ReceivedFeatherBadge:
	.string "{PLAYER} received the PILLAR BADGE\n"
	.string "from TCHUM.$"

FortreeCity_Gym_Text_ExplainFeatherBadgeTakeThis:
	.string "The PILLAR BADGE shows you can\n"
	.string "stand firm when the ground shakes.\p"
	.string "Wear it well, and stay grounded!$"

FortreeCity_Gym_Text_ExplainAerialAce:
	.string "That's BULLDOZE! Stomp the ground\n"
	.string "and slow down everyone you hit.\p"
	.string "Solid, simple, effective. Like a\n"
	.string "good foundation!$"

FortreeCity_Gym_Text_RegisteredWinona:
	.string "Registered GYM LEADER WINONA\n"
	.string "in the POKéNAV.$"

FortreeCity_Gym_Text_WinonaPostBattle:
	.string "NEVARD was right about you.\p"
	.string "A city stands on its pillars, and\n"
	.string "people stand on each other. Remember\l"
	.string "that out there.$"

FortreeCity_Gym_Text_GymStatue:
	.string "PILLARTON CITY POKéMON GYM$"

FortreeCity_Gym_Text_GymStatueCertified:
	.string "PILLARTON CITY POKéMON GYM\p"
	.string "TCHUM'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

FortreeCity_Gym_Text_WinonaPreRematch:
	.string "WINONA: We humans can never escape\n"
	.string "gravity's pull on the ground.\p"
	.string "But by striving for excellence,\n"
	.string "we have the power to soar!\p"
	.string "You have scaled the pinnacle as\n"
	.string "the reigning CHAMPION.\p"
	.string "Please, allow me to see your power\n"
	.string "at full flight!$"

FortreeCity_Gym_Text_WinonaRematchDefeat:
	.string "I failed to reach your height again…$"

FortreeCity_Gym_Text_WinonaPostRematch:
	.string "WINONA: Even though I have lost,\n"
	.string "the wings of my heart remain unbroken.\p"
	.string "I can rise and soar again and\n"
	.string "yet again.\p"
	.string "I am convinced of it!$"

FortreeCity_Gym_Text_WinonaRematchNeedTwoMons:
	.string "WINONA: We humans can never escape\n"
	.string "gravity's pull on the ground.\p"
	.string "But by striving for excellence,\n"
	.string "we have the power to soar!\p"
	.string "You have scaled the pinnacle as\n"
	.string "the reigning CHAMPION.\p"
	.string "Please, allow me to see your power\n"
	.string "at full flight!\p"
	.string "Oh, no… Do you have but one\n"
	.string "POKéMON with you?\p"
	.string "Please return with two POKéMON\n"
	.string "at the very least.$"
