PalmTradepost_MapScripts::
	.byte 0

Palm111_Wen::
	lock
	faceplayer
	goto_if_set FLAG_HT_TRADEPOST_DONE, Palm111_WenDone
	goto_if_set FLAG_HT_TRADEPOST_PERMIT, Palm111_WenResolve
	msgbox Palm111_TextWenAsk, MSGBOX_DEFAULT
	setflag FLAG_HT_TRADEPOST_WEN_ASKED
	release
	end

Palm111_WenResolve::
	msgbox Palm111_TextWenResolve, MSGBOX_DEFAULT
	closemessage
	applymovement 3, Palm111_MessengerLeaves
	waitmovement 0
	removeobject 3
	setflag FLAG_HT_TRADEPOST_DONE
	msgbox Palm111_TextWenReward, MSGBOX_DEFAULT
	giveitem ITEM_AMULET_COIN
	release
	end

Palm111_WenDone::
	msgbox Palm111_TextWenDone, MSGBOX_DEFAULT
	release
	end

Palm111_MessengerLeaves:
	walk_right
	walk_right
	walk_up
	walk_up
	walk_up
	step_end

Palm111_StationOperator::
	lock
	faceplayer
	goto_if_set FLAG_HT_TRADEPOST_PERMIT, Palm111_OperatorAfter
	goto_if_unset FLAG_HT_TRADEPOST_WEN_ASKED, Palm111_OperatorIdle
	msgbox Palm111_TextOperatorGive, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	message Palm111_TextGotPermit
	waitfanfare
	waitmessage
	setflag FLAG_HT_TRADEPOST_PERMIT
	msgbox Palm111_TextOperatorAfter, MSGBOX_DEFAULT
	release
	end

Palm111_OperatorIdle::
	msgbox Palm111_TextOperatorIdle, MSGBOX_DEFAULT
	release
	end

Palm111_OperatorAfter::
	msgbox Palm111_TextOperatorAfter, MSGBOX_DEFAULT
	release
	end

Palm111_FruitSeller::
	goto_if_set FLAG_HT_TRADEPOST_DONE, Palm111_FruitSellerHappy
	msgbox Palm111_FruitSeller_Text, MSGBOX_NPC
	end

Palm111_FruitSellerHappy::
	msgbox Palm111_FruitSellerHappy_Text, MSGBOX_NPC
	end

Palm111_PalmMessenger::
	msgbox Palm111_PalmMessenger_Text, MSGBOX_NPC
	end

Palm111_Porter::
	msgbox Palm111_Porter_Text, MSGBOX_NPC
	end

Palm111_DockSailor::
	msgbox Palm111_DockSailor_Text, MSGBOX_NPC
	end

Palm111_NorthWorker::
	msgbox Palm111_NorthWorker_Text, MSGBOX_NPC
	end

Palm111_TownSign::
	msgbox Palm111_TownSign_Text, MSGBOX_SIGN
	end

Palm111_AssociationSign::
	msgbox Palm111_AssociationSign_Text, MSGBOX_SIGN
	end

Palm111_StationSign::
	msgbox Palm111_StationSign_Text, MSGBOX_SIGN
	end

Palm111_NorthSign::
	msgbox Palm111_NorthSign_Text, MSGBOX_SIGN
	end

Palm111_KioskSign::
	msgbox Palm111_KioskSign_Text, MSGBOX_SIGN
	end


Palm111_TextWenAsk:
	.string "Ah, a traveler. I'm WEN, head of\n"
	.string "the MERCHANTS' ASSOCIATION.\p"
	.string "That TEAM PALM messenger says the\n"
	.string "road and the docks are theirs now.\p"
	.string "“Pay in PALM COIN or your cargo\n"
	.string "waits forever,” she says.\p"
	.string "But this market has an old charter.\n"
	.string "The original CARGO PERMIT proves\p"
	.string "anyone may trade here freely.\n"
	.string "The station keeps it in its archive.\p"
	.string "Would you ask the operator for it?\n"
	.string "These old knees can't climb stairs.$"

Palm111_TextWenResolve:
	.string "The original CARGO PERMIT! Signed\n"
	.string "by every family on both banks.\p"
	.string "Messenger! Read this. No company\n"
	.string "owns these roads. Not now, not ever.$"

Palm111_TextWenReward:
	.string "Hah! Did you see her face?\p"
	.string "Goods only exist because people from\n"
	.string "everywhere can trade and trust.\p"
	.string "Nobody should own every road.\n"
	.string "Please, take this as thanks.$"

Palm111_TextWenDone:
	.string "The market is open again, thanks\n"
	.string "to you.\p"
	.string "The road north to PILLARTON is\n"
	.string "still flooded, I'm afraid.$"

Palm111_TextOperatorIdle:
	.string "Passenger service is suspended.\n"
	.string "No trains until the power is back.$"

Palm111_TextOperatorGive:
	.string "WEN sent you? For the CARGO PERMIT?\n"
	.string "Of course. Here it is.$"

Palm111_TextGotPermit:
	.string "{PLAYER} received the CARGO PERMIT!$"

Palm111_TextOperatorAfter:
	.string "Take good care of that permit.\n"
	.string "It's older than the railway!$"

Palm111_PalmMessenger_Text:
	.string "With PALM COIN, all your cargo moves\n"
	.string "through our network!\p"
	.string "You just accept our terms... and\n"
	.string "all our future price changes.$"

Palm111_FruitSeller_Text:
	.string "My oranges are rotting in a crate\n"
	.string "at the dock. TEAM PALM won't release\p"
	.string "it unless I pay in their coin!$"

Palm111_FruitSellerHappy_Text:
	.string "My crates are back! Fresh fruit for\n"
	.string "everyone, paid any way you like!$"

Palm111_Porter_Text:
	.string "Both banks of the canal trade every\n"
	.string "day. That's why they call this town\p"
	.string "TRADEPOST. Well, that and the sign.$"

Palm111_DockSailor_Text:
	.string "The canal runs all the way to the\n"
	.string "sea. Boats used to come every day.$"

Palm111_NorthWorker_Text:
	.string "Sorry, the road north is closed.\n"
	.string "The river flooded the lowlands.\p"
	.string "They say PILLARTON's dams are\n"
	.string "acting strange...$"

Palm111_TownSign_Text:
	.string "TRADEPOST\n"
	.string "“Two banks, one market.”$"

Palm111_AssociationSign_Text:
	.string "MERCHANTS' ASSOCIATION\n"
	.string "Free trade since the first caravan.$"

Palm111_StationSign_Text:
	.string "TRADEPOST STATION\n"
	.string "Passenger service suspended.$"

Palm111_NorthSign_Text:
	.string "NORTH: ROUTE 5 - PILLARTON\n"
	.string "Closed due to flooding.$"

Palm111_KioskSign_Text:
	.string "TEAM PALM LOGISTICS\n"
	.string "“One coin. One network. One future.”$"