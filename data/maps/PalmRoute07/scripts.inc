PalmRoute07_MapScripts::
	.byte 0

Palm160_RouteHENRY::
	trainerbattle_single TRAINER_PALM_ROUTE07_HENRY, Palm160_TextHENRYIntro, Palm160_TextHENRYLoss
	msgbox Palm160_TextHENRYAfter, MSGBOX_AUTOCLOSE
	end

Palm160_RouteCONNIE::
	trainerbattle_single TRAINER_PALM_ROUTE07_CONNIE, Palm160_TextCONNIEIntro, Palm160_TextCONNIELoss
	msgbox Palm160_TextCONNIEAfter, MSGBOX_AUTOCLOSE
	end

Palm160_RouteCELIA::
	trainerbattle_single TRAINER_PALM_ROUTE07_CELIA, Palm160_TextCELIAIntro, Palm160_TextCELIALoss
	msgbox Palm160_TextCELIAAfter, MSGBOX_AUTOCLOSE
	end

Palm160_RouteCOLIN::
	trainerbattle_single TRAINER_PALM_ROUTE07_COLIN, Palm160_TextCOLINIntro, Palm160_TextCOLINLoss
	msgbox Palm160_TextCOLINAfter, MSGBOX_AUTOCLOSE
	end

Palm160_SignSouth::
	msgbox Palm160_SignSouth_Text, MSGBOX_SIGN
	end

Palm160_SignNorth::
	msgbox Palm160_SignNorth_Text, MSGBOX_SIGN
	end

Palm160_SignCircle::
	msgbox Palm160_SignCircle_Text, MSGBOX_SIGN
	end


Palm160_TextHENRYIntro:
	.string "Shh! The lake is so still today\n"
	.string "you can see the clouds in it.\p"
	.string "Let's battle quietly, all right?$"

Palm160_TextHENRYLoss:
	.string "My line's all tangled now…$"

Palm160_TextHENRYAfter:
	.string "The water's higher than last week.\n"
	.string "And it hasn't rained a single drop.$"

Palm160_TextCONNIEIntro:
	.string "This route is called the PATH OF\n"
	.string "MIRRORS. Can you guess why?$"

Palm160_TextCONNIELoss:
	.string "My reflection looks so sad now!$"

Palm160_TextCONNIEAfter:
	.string "On a calm day, the lake copies\n"
	.string "the whole sky. Even the stars!$"

Palm160_TextCELIAIntro:
	.string "I packed sweets for a picnic by the\n"
	.string "flowers. Battle first, snack later!$"

Palm160_TextCELIALoss:
	.string "Oof… I need a sugar break.$"

Palm160_TextCELIAAfter:
	.string "FLABÉBÉ pick one flower and keep it\n"
	.string "for their whole lives. How sweet!$"

Palm160_TextCOLINIntro:
	.string "From up here I watch the birds\n"
	.string "fly over the lake. And you!$"

Palm160_TextCOLINLoss:
	.string "Grounded, like a fledgling…$"

Palm160_TextCOLINAfter:
	.string "At night, CLEFAIRY gather inside\n"
	.string "this ring of stones to dance.\p"
	.string "People say they come from the moon.$"

Palm160_SignSouth_Text:
	.string "ROUTE 7 · PATH OF MIRRORS\n"
	.string "South: SERENIA$"

Palm160_SignNorth_Text:
	.string "ROUTE 7\n"
	.string "North: HORIZON CITY$"

Palm160_SignCircle_Text:
	.string "MOON CIRCLE\p"
	.string "Please leave the stones as they are.\n"
	.string "The CLEFAIRY like them that way.$"