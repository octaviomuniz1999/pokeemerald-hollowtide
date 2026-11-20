PalmRoute12_MapScripts::
	.byte 0

Palm250_RouteARTUR::
	trainerbattle_single TRAINER_PALM_ROUTE12_ARTUR, Palm250_TextARTURIntro, Palm250_TextARTURLoss
	msgbox Palm250_TextARTURAfter, MSGBOX_AUTOCLOSE
	end

Palm250_RouteBIA::
	trainerbattle_single TRAINER_PALM_ROUTE12_BIA, Palm250_TextBIAIntro, Palm250_TextBIALoss
	msgbox Palm250_TextBIAAfter, MSGBOX_AUTOCLOSE
	end

Palm250_RouteNICO::
	trainerbattle_single TRAINER_PALM_ROUTE12_NICO, Palm250_TextNICOIntro, Palm250_TextNICOLoss
	msgbox Palm250_TextNICOAfter, MSGBOX_AUTOCLOSE
	end

Palm250_SignEast::
	msgbox Palm250_SignEast_Text, MSGBOX_SIGN
	end


Palm250_SignEast_Text:
	.string "ROUTE 12 - RIVER BEND\n"
	.string "East: ROUTE 5$"

Palm250_TextARTURIntro:
	.string "Shh! The BASCULIN gather right at\n"
	.string "the bend. You'll scare them off!$"

Palm250_TextARTURLoss:
	.string "Fine, fine… They were gone anyway.$"

Palm250_TextARTURAfter:
	.string "When the dam held the water back, the\n"
	.string "river nearly forgot this bend.\p"
	.string "Now it's full again, and so is my net.$"

Palm250_TextBIAIntro:
	.string "I came for a quiet picnic by the\n"
	.string "water. A battle works too!$"

Palm250_TextBIALoss:
	.string "My sandwiches are safe, at least.$"

Palm250_TextBIAAfter:
	.string "There's a little beach on the inside\n"
	.string "of the bend. Kids leave treasures\l"
	.string "in the sand there.$"

Palm250_TextNICOIntro:
	.string "Hear that? The TYMPOLE are singing.\n"
	.string "Let's make some noise too!$"

Palm250_TextNICOLoss:
	.string "Okay, okay! I'll keep it down.$"

Palm250_TextNICOAfter:
	.string "Some people say a frog POKéMON with\n"
	.string "foam around its neck hides in the\l"
	.string "tall grass here. I've never seen it.$"