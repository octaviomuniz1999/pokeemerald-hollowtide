PalmRoute04_MapScripts::
	.byte 0

Palm110_RouteYUE::
	trainerbattle_single TRAINER_PALM_ROUTE04_YUE, Palm110_TextYUEIntro, Palm110_TextYUELoss
	msgbox Palm110_TextYUEAfter, MSGBOX_AUTOCLOSE
	end

Palm110_RouteQIAO::
	trainerbattle_single TRAINER_PALM_ROUTE04_QIAO, Palm110_TextQIAOIntro, Palm110_TextQIAOLoss
	msgbox Palm110_TextQIAOAfter, MSGBOX_AUTOCLOSE
	end

Palm110_RouteMARA::
	trainerbattle_single TRAINER_PALM_ROUTE04_MARA, Palm110_TextMARAIntro, Palm110_TextMARALoss
	msgbox Palm110_TextMARAAfter, MSGBOX_AUTOCLOSE
	end

Palm110_Trader::
	msgbox Palm110_Trader_Text, MSGBOX_NPC
	end

Palm110_SignWest::
	msgbox Palm110_SignWest_Text, MSGBOX_SIGN
	end

Palm110_SignEast::
	msgbox Palm110_SignEast_Text, MSGBOX_SIGN
	end


Palm110_SignWest_Text:
	.string "ROUTE 4 - CARAVAN ROAD\n"
	.string "West: FERRALIA CITY\l"
	.string "East: TRADEPOST$"

Palm110_SignEast_Text:
	.string "TRADEPOST just ahead.\n"
	.string "“Two banks, one market.”$"

Palm110_Trader_Text:
	.string "This old shed used to be full of\n"
	.string "grain and coffee from HARVESTVALE.\p"
	.string "Since the trains stopped, we carry\n"
	.string "everything by cart. Slow, but honest.$"

Palm110_TextYUEIntro:
	.string "Special delivery! One battle,\n"
	.string "signed and sealed!$"

Palm110_TextYUELoss:
	.string "Return to sender...$"

Palm110_TextYUEAfter:
	.string "TEAM PALM wants us to pay for every\n"
	.string "road in PALM COIN. Can you believe it?$"

Palm110_TextQIAOIntro:
	.string "I used to lay track on this line.\n"
	.string "Now I lay out challengers!$"

Palm110_TextQIAOLoss:
	.string "Hah! Strong as a steel rail.$"

Palm110_TextQIAOAfter:
	.string "The line won't reopen until someone\n"
	.string "fixes the power down the coast.$"

Palm110_TextMARAIntro:
	.string "I collect rare POKéMON and rare\n"
	.string "views. This lookout has both!$"

Palm110_TextMARALoss:
	.string "A fine addition to my memories.$"

Palm110_TextMARAAfter:
	.string "From here you can see both banks of\n"
	.string "TRADEPOST. Pretty, isn't it?$"