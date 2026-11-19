PalmRoute05_MapScripts::
	.byte 0

Palm120_RouteTIAGO::
	trainerbattle_single TRAINER_PALM_ROUTE05_TIAGO, Palm120_TextTIAGOIntro, Palm120_TextTIAGOLoss
	msgbox Palm120_TextTIAGOAfter, MSGBOX_AUTOCLOSE
	end

Palm120_RouteODAIR::
	trainerbattle_single TRAINER_PALM_ROUTE05_ODAIR, Palm120_TextODAIRIntro, Palm120_TextODAIRLoss
	msgbox Palm120_TextODAIRAfter, MSGBOX_AUTOCLOSE
	end

Palm120_RouteLIA::
	trainerbattle_single TRAINER_PALM_ROUTE05_LIA, Palm120_TextLIAIntro, Palm120_TextLIALoss
	msgbox Palm120_TextLIAAfter, MSGBOX_AUTOCLOSE
	end

Palm120_RouteDUDU::
	trainerbattle_single TRAINER_PALM_ROUTE05_DUDU, Palm120_TextDUDUIntro, Palm120_TextDUDULoss
	msgbox Palm120_TextDUDUAfter, MSGBOX_AUTOCLOSE
	end

Palm120_SignSouth::
	msgbox Palm120_SignSouth_Text, MSGBOX_SIGN
	end

Palm120_SignNorth::
	msgbox Palm120_SignNorth_Text, MSGBOX_SIGN
	end


Palm120_SignSouth_Text:
	.string "ROUTE 5 - RIVER DELTA\n"
	.string "South: TRADEPOST$"

Palm120_SignNorth_Text:
	.string "NORTH: PILLARTON CITY\n"
	.string "“The city of pillars and dams.”$"

Palm120_TextTIAGOIntro:
	.string "The river's lower than I've ever\n"
	.string "seen it. The fish are restless!$"

Palm120_TextTIAGOLoss:
	.string "Snapped my line...$"

Palm120_TextTIAGOAfter:
	.string "Someone upstream is holding back\n"
	.string "the water. It isn't the rain.$"

Palm120_TextODAIRIntro:
	.string "This island used to be a sandbar.\n"
	.string "Now it's my training ground!$"

Palm120_TextODAIRLoss:
	.string "Washed away!$"

Palm120_TextODAIRAfter:
	.string "GROUND-types love the dry riverbed\n"
	.string "on the east bank.$"

Palm120_TextLIAIntro:
	.string "I came to see the delta bloom, but\n"
	.string "a battle will do!$"

Palm120_TextLIALoss:
	.string "Wilted...$"

Palm120_TextLIAAfter:
	.string "PILLARTON's dams are huge. You can\n"
	.string "see them from the hills up north.$"

Palm120_TextDUDUIntro:
	.string "Old bones and old riverbeds! This\n"
	.string "dry channel is full of history!$"

Palm120_TextDUDULoss:
	.string "My finds, my pride... crushed.$"

Palm120_TextDUDUAfter:
	.string "When the river ran here, the delta\n"
	.string "had three arms. Now it has two.$"