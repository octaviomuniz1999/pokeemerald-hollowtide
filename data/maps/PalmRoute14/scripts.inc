PalmRoute14_MapScripts::
	.byte 0

Palm252_RouteBETO::
	trainerbattle_single TRAINER_PALM_ROUTE14_BETO, Palm252_TextBETOIntro, Palm252_TextBETOLoss
	msgbox Palm252_TextBETOAfter, MSGBOX_AUTOCLOSE
	end

Palm252_RouteCLARA::
	trainerbattle_single TRAINER_PALM_ROUTE14_CLARA, Palm252_TextCLARAIntro, Palm252_TextCLARALoss
	msgbox Palm252_TextCLARAAfter, MSGBOX_AUTOCLOSE
	end

Palm252_RouteOTTO::
	trainerbattle_single TRAINER_PALM_ROUTE14_OTTO, Palm252_TextOTTOIntro, Palm252_TextOTTOLoss
	msgbox Palm252_TextOTTOAfter, MSGBOX_AUTOCLOSE
	end

Palm252_SignEast::
	msgbox Palm252_SignEast_Text, MSGBOX_SIGN
	end

Palm252_SignLookout::
	msgbox Palm252_SignLookout_Text, MSGBOX_SIGN
	end


Palm252_SignEast_Text:
	.string "ROUTE 14 - ATLAS LOOKOUT\n"
	.string "East: PASSWAY VILLAGE$"

Palm252_SignLookout_Text:
	.string "ATLAS LOOKOUT\n"
	.string "From here you can watch the road for\l"
	.string "miles in every direction.\p"
	.string "In PASSWAY, they say a faithful\n"
	.string "guardian once kept watch on this spot.$"

Palm252_TextBETOIntro:
	.string "I patrol this road every day.\n"
	.string "Let's see if you're up to the climb!$"

Palm252_TextBETOLoss:
	.string "You've got a good pace. Keep it up.$"

Palm252_TextBETOAfter:
	.string "The dog POKéMON here are loyal to\n"
	.string "whoever shares the road with them.$"

Palm252_TextCLARAIntro:
	.string "My babies need practice. Would you\n"
	.string "mind battling them?$"

Palm252_TextCLARALoss:
	.string "Oh, good job, everyone! Even so.$"

Palm252_TextCLARAAfter:
	.string "HERDIER never forget a friend's\n"
	.string "scent. Not even after many years.$"

Palm252_TextOTTOIntro:
	.string "Up here, you can see where you came\n"
	.string "from. Can you see where you're going?$"

Palm252_TextOTTOLoss:
	.string "Ha! You clearly can.$"

Palm252_TextOTTOAfter:
	.string "On clear mornings, an ABSOL sits at\n"
	.string "the edge of the lookout. Folks say it\l"
	.string "only shows up before a storm.$"