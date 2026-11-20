PalmOceanComplex1F_MapScripts::
	.byte 0

Palm203_Boat::
	lock
	faceplayer
	msgbox Palm203_TextBoat, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm203_BoatNo
	warp MAP_PALM_TIDEMOUTH, 33, 38
	waitstate
	release
	end

Palm203_BoatNo::
	release
	end

Palm203_Grunt1::
	trainerbattle_single TRAINER_PALM_COMPLEX_GRUNT_1, Palm203_TextGrunt1Intro, Palm203_TextGrunt1Loss
	msgbox Palm203_TextGrunt1After, MSGBOX_AUTOCLOSE
	end

Palm203_Grunt2::
	trainerbattle_single TRAINER_PALM_COMPLEX_GRUNT_2, Palm203_TextGrunt2Intro, Palm203_TextGrunt2Loss
	msgbox Palm203_TextGrunt2After, MSGBOX_AUTOCLOSE
	end

Palm203_Grunt3::
	trainerbattle_single TRAINER_PALM_COMPLEX_GRUNT_3, Palm203_TextGrunt3Intro, Palm203_TextGrunt3Loss
	msgbox Palm203_TextGrunt3After, MSGBOX_AUTOCLOSE
	end

Palm203_Tank::
	msgbox Palm203_Tank_Text, MSGBOX_SIGN
	end

Palm203_Turbine::
	msgbox Palm203_Turbine_Text, MSGBOX_SIGN
	end


Palm203_TextBoat:
	.string "SAILOR: I'll wait for you here.\n"
	.string "Want to go back to TIDEMOUTH?$"

Palm203_TextGrunt1Intro:
	.string "A kid on our platform? Security!\n"
	.string "…Oh, that's me. Fine!$"

Palm203_TextGrunt1Loss:
	.string "Security has failed.$"

Palm203_TextGrunt1After:
	.string "The turbines feed the whole complex.\n"
	.string "The boss says it's the future.$"

Palm203_TextGrunt2Intro:
	.string "Every wave out there pays our bills!\n"
	.string "You're not stopping the machines!$"

Palm203_TextGrunt2Loss:
	.string "Wiped out!$"

Palm203_TextGrunt2After:
	.string "We mine PALM COIN with the power\n"
	.string "from the sea. Isn't that genius?$"

Palm203_TextGrunt3Intro:
	.string "ABELF is upstairs. Nobody bothers\n"
	.string "ABELF. Especially not you!$"

Palm203_TextGrunt3Loss:
	.string "…He's going to be so mad.$"

Palm203_TextGrunt3After:
	.string "Go on, then. See what happens when\n"
	.string "you meet the boss.$"

Palm203_Turbine_Text:
	.string "A massive turbine roars, pulling\n"
	.string "water from the sea.$"

Palm203_Tank_Text:
	.string "A reservoir tank. The water inside\n"
	.string "churns in slow circles.$"