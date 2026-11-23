@ Hollowtide: trocas do Tradepost (install_trades.py)

Palm261_TradeKadabra::
	lock
	faceplayer
	goto_if_set FLAG_HT_TRADE_KADABRA, Palm261_KadabraDone
	ingame_trade INGAME_TRADE_HT_KADABRA, Palm261_TextKadabraWant, Palm261_KadabraDecline, Palm261_KadabraWrong, Palm261_TextKadabraThanks
	setflag FLAG_HT_TRADE_KADABRA
	release
	end

Palm261_KadabraDecline::
	msgbox Palm261_TextKadabraDecline, MSGBOX_DEFAULT
	release
	end

Palm261_KadabraWrong::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox Palm261_TextTradeWrong, MSGBOX_DEFAULT
	release
	end

Palm261_KadabraDone::
	msgbox Palm261_TextKadabraDone, MSGBOX_DEFAULT
	release
	end

Palm261_TextKadabraWant:
	.string "TRADEPOST rule: nobody owns the road,\n"
	.string "but everybody trades on it!\p"
	.string "I'll trade my {STR_VAR_2} for\n"
	.string "a {STR_VAR_1}. Deal?$"
Palm261_TextKadabraThanks:
	.string "A fair trade! Funny thing, KADABRA\n"
	.string "always changes when it changes hands.$"
Palm261_TextKadabraDecline:
	.string "No deal? The fair is open all day.$"
Palm261_TextKadabraDone:
	.string "My MEOWTH already counts coins better\n"
	.string "than I do!$"

Palm261_TradeMachoke::
	lock
	faceplayer
	goto_if_set FLAG_HT_TRADE_MACHOKE, Palm261_MachokeDone
	ingame_trade INGAME_TRADE_HT_MACHOKE, Palm261_TextMachokeWant, Palm261_MachokeDecline, Palm261_MachokeWrong, Palm261_TextMachokeThanks
	setflag FLAG_HT_TRADE_MACHOKE
	release
	end

Palm261_MachokeDecline::
	msgbox Palm261_TextMachokeDecline, MSGBOX_DEFAULT
	release
	end

Palm261_MachokeWrong::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox Palm261_TextTradeWrong, MSGBOX_DEFAULT
	release
	end

Palm261_MachokeDone::
	msgbox Palm261_TextMachokeDone, MSGBOX_DEFAULT
	release
	end

Palm261_TextMachokeWant:
	.string "I need someone to help carry crates\n"
	.string "at the station. A {STR_VAR_1} would do.\p"
	.string "Want my {STR_VAR_2} in exchange?$"
Palm261_TextMachokeThanks:
	.string "Treat it well! A traded MACHOKE gets\n"
	.string "a lot stronger, you know.$"
Palm261_TextMachokeDecline:
	.string "Too bad. These crates won't move\n"
	.string "themselves.$"
Palm261_TextMachokeDone:
	.string "TIMBURR and I move the cargo\n"
	.string "together now. Thanks again!$"

Palm261_TradeGraveler::
	lock
	faceplayer
	goto_if_set FLAG_HT_TRADE_GRAVELER, Palm261_GravelerDone
	ingame_trade INGAME_TRADE_HT_GRAVELER, Palm261_TextGravelerWant, Palm261_GravelerDecline, Palm261_GravelerWrong, Palm261_TextGravelerThanks
	setflag FLAG_HT_TRADE_GRAVELER
	release
	end

Palm261_GravelerDecline::
	msgbox Palm261_TextGravelerDecline, MSGBOX_DEFAULT
	release
	end

Palm261_GravelerWrong::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox Palm261_TextTradeWrong, MSGBOX_DEFAULT
	release
	end

Palm261_GravelerDone::
	msgbox Palm261_TextGravelerDone, MSGBOX_DEFAULT
	release
	end

Palm261_TextGravelerWant:
	.string "I collect rocks from every road.\n"
	.string "I don't have a {STR_VAR_1} yet!\p"
	.string "I'll give you my {STR_VAR_2} for one.\n"
	.string "How about it?$"
Palm261_TextGravelerThanks:
	.string "Ha! Look at it! Some rocks only\n"
	.string "shine after a long trip.$"
Palm261_TextGravelerDecline:
	.string "Maybe next time you pass by.$"
Palm261_TextGravelerDone:
	.string "My collection keeps growing. Every\n"
	.string "road has its own kind of stone.$"

Palm261_TradeHaunter::
	lock
	faceplayer
	goto_if_set FLAG_HT_TRADE_HAUNTER, Palm261_HaunterDone
	ingame_trade INGAME_TRADE_HT_HAUNTER, Palm261_TextHaunterWant, Palm261_HaunterDecline, Palm261_HaunterWrong, Palm261_TextHaunterThanks
	setflag FLAG_HT_TRADE_HAUNTER
	release
	end

Palm261_HaunterDecline::
	msgbox Palm261_TextHaunterDecline, MSGBOX_DEFAULT
	release
	end

Palm261_HaunterWrong::
	bufferspeciesname STR_VAR_1, VAR_0x8009
	msgbox Palm261_TextTradeWrong, MSGBOX_DEFAULT
	release
	end

Palm261_HaunterDone::
	msgbox Palm261_TextHaunterDone, MSGBOX_DEFAULT
	release
	end

Palm261_TextHaunterWant:
	.string "Sometimes trash is a treasure.\n"
	.string "I'd love a {STR_VAR_1}.\p"
	.string "I'll trade my {STR_VAR_2}. It's\n"
	.string "a little spooky, but very loyal.$"
Palm261_TextHaunterThanks:
	.string "Hehehe… HAUNTER always shows its\n"
	.string "true face after a trade.$"
Palm261_TextHaunterDecline:
	.string "Too spooky? I understand.$"
Palm261_TextHaunterDone:
	.string "TRUBBISH and I clean the canal at\n"
	.string "night. It's happier than ever.$"

Palm261_TextTradeWrong:
	.string "Hmm? That doesn't look like\n"
	.string "a {STR_VAR_1} to me.$"
