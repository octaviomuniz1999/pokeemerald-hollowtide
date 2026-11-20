PalmRoute15_MapScripts::
	.byte 0

Palm253_RouteOSCAR::
	trainerbattle_single TRAINER_PALM_ROUTE15_OSCAR, Palm253_TextOSCARIntro, Palm253_TextOSCARLoss
	msgbox Palm253_TextOSCARAfter, MSGBOX_AUTOCLOSE
	end

Palm253_RoutePEDRO::
	trainerbattle_single TRAINER_PALM_ROUTE15_PEDRO, Palm253_TextPEDROIntro, Palm253_TextPEDROLoss
	msgbox Palm253_TextPEDROAfter, MSGBOX_AUTOCLOSE
	end

Palm253_RouteNINA::
	trainerbattle_single TRAINER_PALM_ROUTE15_NINA, Palm253_TextNINAIntro, Palm253_TextNINALoss
	msgbox Palm253_TextNINAAfter, MSGBOX_AUTOCLOSE
	end

Palm253_SignEast::
	msgbox Palm253_SignEast_Text, MSGBOX_SIGN
	end


Palm253_SignEast_Text:
	.string "ROUTE 15 - COASTAL GROTTO\n"
	.string "East: ROUTE 11$"

Palm253_TextOSCARIntro:
	.string "Ahoy! The ferries stopped during the\n"
	.string "storm, so I walk the shore now.$"

Palm253_TextOSCARLoss:
	.string "Sunk without a trace!$"

Palm253_TextOSCARAfter:
	.string "The sea's calm again. Soon the boats\n"
	.string "will sail out of TIDEMOUTH like before.$"

Palm253_TextPEDROIntro:
	.string "You found my secret spot! Now you\n"
	.string "have to get past me.$"

Palm253_TextPEDROLoss:
	.string "Fine… Just don't tell anyone.$"

Palm253_TextPEDROAfter:
	.string "At high tide the sea fills this\n"
	.string "grotto. RELICANTH come in from the\l"
	.string "deep. Old fish, older than the LEAGUE.$"

Palm253_TextNINAIntro:
	.string "The sea breeze is perfect today.\n"
	.string "Let's battle before the tide turns!$"

Palm253_TextNINALoss:
	.string "My hair! The wind ruined it!$"

Palm253_TextNINAAfter:
	.string "Shells wash up on this beach after\n"
	.string "every storm. Some people find pearls.$"