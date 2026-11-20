PalmRoute10_MapScripts::
	.byte 0

Palm200_RouteTOMAS::
	trainerbattle_single TRAINER_PALM_ROUTE10_TOMAS, Palm200_TextTOMASIntro, Palm200_TextTOMASLoss
	msgbox Palm200_TextTOMASAfter, MSGBOX_AUTOCLOSE
	end

Palm200_RouteRITA::
	trainerbattle_single TRAINER_PALM_ROUTE10_RITA, Palm200_TextRITAIntro, Palm200_TextRITALoss
	msgbox Palm200_TextRITAAfter, MSGBOX_AUTOCLOSE
	end

Palm200_RouteJONAS::
	trainerbattle_single TRAINER_PALM_ROUTE10_JONAS, Palm200_TextJONASIntro, Palm200_TextJONASLoss
	msgbox Palm200_TextJONASAfter, MSGBOX_AUTOCLOSE
	end

Palm200_RouteLUANA::
	trainerbattle_single TRAINER_PALM_ROUTE10_LUANA, Palm200_TextLUANAIntro, Palm200_TextLUANALoss
	msgbox Palm200_TextLUANAAfter, MSGBOX_AUTOCLOSE
	end

Palm200_SignNorth::
	msgbox Palm200_SignNorth_Text, MSGBOX_SIGN
	end

Palm200_SignSouth::
	msgbox Palm200_SignSouth_Text, MSGBOX_SIGN
	end

Palm200_SignBeacon::
	msgbox Palm200_SignBeacon_Text, MSGBOX_SIGN
	end


Palm200_TextTOMASIntro:
	.string "Ahoy! The sea's been restless all week.\n"
	.string "Let's see if you can keep your footing!$"

Palm200_TextTOMASLoss:
	.string "Capsized!$"

Palm200_TextTOMASAfter:
	.string "The waves come in higher every day.\n"
	.string "And there's no storm in sight.$"

Palm200_TextRITAIntro:
	.string "I'm not scared of the big waves!\n"
	.string "My POKéMON float just fine!$"

Palm200_TextRITALoss:
	.string "Glub glub…$"

Palm200_TextRITAAfter:
	.string "Mom says we can't swim near TIDEMOUTH\n"
	.string "anymore. The tide is too weird.$"

Palm200_TextJONASIntro:
	.string "The fish here swim against the\n"
	.string "current. Want to see one up close?$"

Palm200_TextJONASLoss:
	.string "They got away. Again.$"

Palm200_TextJONASAfter:
	.string "The lighthouses blink, but the boats\n"
	.string "stay in the harbor. Nobody sails now.$"

Palm200_TextLUANAIntro:
	.string "I swim this coast every morning!\n"
	.string "Race you to the next lighthouse!$"

Palm200_TextLUANALoss:
	.string "You're faster than the current!$"

Palm200_TextLUANAAfter:
	.string "There's something out at sea, past the\n"
	.string "harbor. A big metal thing. It hums.$"

Palm200_SignNorth_Text:
	.string "ROUTE 10 · LIGHTHOUSE COAST\n"
	.string "North: VOLTARA$"

Palm200_SignSouth_Text:
	.string "ROUTE 10\n"
	.string "South: TIDEMOUTH$"

Palm200_SignBeacon_Text:
	.string "GUIDE BEACON\n"
	.string "Keep your boat to the right of the\l"
	.string "light. The rocks bite!$"