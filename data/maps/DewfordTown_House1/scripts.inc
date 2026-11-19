DewfordTown_House1_MapScripts::
	.byte 0

DewfordTown_House1_EventScript_Man::
	msgbox DewfordTown_House1_Text_LotToBeSaidForLivingOnIsland, MSGBOX_NPC
	end

DewfordTown_House1_EventScript_Woman::
	msgbox DewfordTown_House1_Text_LifeGoesSlowlyOnIsland, MSGBOX_NPC
	end

DewfordTown_House1_EventScript_Zigzagoon::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ZIGZAGOON, CRY_MODE_NORMAL
	msgbox DewfordTown_House1_Text_Zigzagoon, MSGBOX_DEFAULT
	waitmoncry
	release
	end

DewfordTown_House1_Text_LotToBeSaidForLivingOnIsland:
	.string "There's a lot to be said for living on\n"
	.string "a small island like this in harmony with\l"
	.string "POKéMON and the family.$"

DewfordTown_House1_Text_LifeGoesSlowlyOnIsland:
	.string "I grew up inland, in the city.\n"
	.string "I moved here when I married.\p"
	.string "Life by the beach goes slowly.\n"
	.string "But waking up to the sea every\l"
	.string "morning--that's happiness, too.$"

DewfordTown_House1_Text_Zigzagoon:
	.string "ZIGZAGOON: Guguuh!$"

