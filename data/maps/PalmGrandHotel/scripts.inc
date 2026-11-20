PalmGrandHotel_MapScripts::
	.byte 0

Palm271_Reception::
	lock
	faceplayer
	msgbox Palm271_TextReception, MSGBOX_DEFAULT
	msgbox Palm271_TextRest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm271_NoRest
	closemessage
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	special HealPlayerParty
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox Palm271_TextMorning, MSGBOX_DEFAULT
	release
	end

Palm271_NoRest::
	msgbox Palm271_TextNoRest, MSGBOX_DEFAULT
	release
	end

Palm271_Concierge::
	msgbox Palm271_TextConcierge, MSGBOX_NPC
	end

Palm271_Staff::
	msgbox Palm271_TextStaff, MSGBOX_NPC
	end

Palm271_Elevator::
	msgbox Palm271_TextElevator, MSGBOX_NPC
	end

Palm271_Guest1::
	msgbox Palm271_TextGuest1, MSGBOX_NPC
	end

Palm271_Guest2::
	msgbox Palm271_TextGuest2, MSGBOX_NPC
	end

Palm271_Guest3::
	msgbox Palm271_TextGuest3, MSGBOX_NPC
	end

Palm271_Wailmer::
	lock
	playmoncry SPECIES_AZUMARILL, CRY_MODE_NORMAL
	msgbox Palm271_TextWailmer, MSGBOX_DEFAULT
	waitmoncry
	release
	end


Palm271_TextReception:
	.string "Welcome to the TIDEMOUTH GRAND HOTEL!\p"
	.string "Oh! You're the trainer who stopped the\n"
	.string "tide. NAMI told us everything.$"

Palm271_TextRest:
	.string "Please, rest with us tonight. It's on\n"
	.string "the house, of course.$"

Palm271_TextMorning:
	.string "Good morning! The sea is calm today.\p"
	.string "We hope you enjoyed your stay.$"

Palm271_TextNoRest:
	.string "Our doors are always open to you.$"

Palm271_TextConcierge:
	.string "The water park reopened yesterday,\n"
	.string "and the ferries run on time again.\p"
	.string "TIDEMOUTH is back to normal!$"

Palm271_TextStaff:
	.string "The upper floors are still drying out\n"
	.string "after the flood. Guests only, please.$"

Palm271_TextElevator:
	.string "The elevator is under maintenance.\n"
	.string "The salt water got into everything.$"

Palm271_TextGuest1:
	.string "We stayed on the hill during the\n"
	.string "storm. The view of the sea was scary.$"

Palm271_TextGuest2:
	.string "Mommy said AZUMARILL is the hotel's\n"
	.string "mascot! It's so round!$"

Palm271_TextGuest3:
	.string "I came for a quiet vacation and got a\n"
	.string "flood instead. Still a good story!$"

Palm271_TextWailmer:
	.string "AZUMARILL: Ma-rill!\p"
	.string "The hotel's mascot greets every guest\n"
	.string "with a little bounce.$"