@ Hollowtide: presentes do canone (install_gifts.py)

Palm260_GiftEevee::
	lock
	faceplayer
	goto_if_set FLAG_HT_GIFT_EEVEE, Palm260_EeveeAfter
	goto_if_unset FLAG_HT_SERENIA_DONE, Palm260_EeveeBefore
	msgbox Palm260_TextEeveeOffer, MSGBOX_DEFAULT
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_EEVEE
	givemon SPECIES_EEVEE, 30
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, Palm260_EeveeParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, Palm260_EeveePC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

Palm260_EeveeParty::
	call Palm260_EeveeFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_EeveeDone
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto Palm260_EeveeDone
	end

Palm260_EeveePC::
	call Palm260_EeveeFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_EeveePCDone
	call Common_EventScript_NameReceivedBoxMon
Palm260_EeveePCDone::
	call Common_EventScript_TransferredToPC
Palm260_EeveeDone::
	setflag FLAG_HT_GIFT_EEVEE
	msgbox Palm260_TextEeveeAfter, MSGBOX_DEFAULT
	release
	end

Palm260_EeveeFanfare::
	bufferspeciesname STR_VAR_2, SPECIES_EEVEE
	playfanfare MUS_OBTAIN_ITEM
	message Palm260_TextObtainedMon
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_EEVEE
	return

Palm260_EeveeAfter::
	msgbox Palm260_TextEeveeAfter, MSGBOX_DEFAULT
	release
	end

Palm260_EeveeBefore::
	msgbox Palm141_Gardener_Text, MSGBOX_DEFAULT
	release
	end

Palm260_TextEeveeOffer:
	.string "Since the shrine was restored, this\n"
	.string "EEVEE comes to the garden every day.\p"
	.string "It keeps watching travelers pass by,\n"
	.string "like LAU once did with JADE.\p"
	.string "I think it wants to go with you.\n"
	.string "Will you take care of it?$"

Palm260_TextEeveeAfter:
	.string "EEVEE can become many things.\p"
	.string "Whatever it becomes, I'm sure it will\n"
	.string "remember this garden.$"

Palm260_GiftPorygon::
	lock
	faceplayer
	goto_if_set FLAG_HT_GIFT_PORYGON, Palm260_PorygonAfter
	goto_if_unset FLAG_BADGE03_GET, Palm260_PorygonBefore
	msgbox Palm260_TextPorygonOffer, MSGBOX_DEFAULT
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_PORYGON
	givemon SPECIES_PORYGON, 24
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, Palm260_PorygonParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, Palm260_PorygonPC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

Palm260_PorygonParty::
	call Palm260_PorygonFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_PorygonDone
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto Palm260_PorygonDone
	end

Palm260_PorygonPC::
	call Palm260_PorygonFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_PorygonPCDone
	call Common_EventScript_NameReceivedBoxMon
Palm260_PorygonPCDone::
	call Common_EventScript_TransferredToPC
Palm260_PorygonDone::
	setflag FLAG_HT_GIFT_PORYGON
	msgbox Palm260_TextPorygonAfter, MSGBOX_DEFAULT
	release
	end

Palm260_PorygonFanfare::
	bufferspeciesname STR_VAR_2, SPECIES_PORYGON
	playfanfare MUS_OBTAIN_ITEM
	message Palm260_TextObtainedMon
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_PORYGON
	return

Palm260_PorygonAfter::
	msgbox Palm260_TextPorygonAfter, MSGBOX_DEFAULT
	release
	end

Palm260_PorygonBefore::
	msgbox Palm250_TextStaff, MSGBOX_DEFAULT
	release
	end

Palm260_TextPorygonOffer:
	.string "Thanks to you, the cargo is moving\n"
	.string "again and our network is back online.\p"
	.string "While we rebuilt the timetables, this\n"
	.string "POKéMON showed up in our data.\p"
	.string "It's a PORYGON. It should see the real\n"
	.string "world. Will you take it?$"

Palm260_TextPorygonAfter:
	.string "Some say an UP-GRADE can make PORYGON\n"
	.string "even smarter. Data never stops\l"
	.string "growing, I guess!$"

Palm260_GiftRotom::
	lock
	faceplayer
	goto_if_set FLAG_HT_GIFT_ROTOM, Palm260_RotomAfter
	goto_if_unset FLAG_HT_VOLTARA_DONE, Palm260_RotomBefore
	msgbox Palm260_TextRotomOffer, MSGBOX_DEFAULT
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_ROTOM
	givemon SPECIES_ROTOM, 40
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, Palm260_RotomParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, Palm260_RotomPC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

Palm260_RotomParty::
	call Palm260_RotomFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_RotomDone
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto Palm260_RotomDone
	end

Palm260_RotomPC::
	call Palm260_RotomFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_RotomPCDone
	call Common_EventScript_NameReceivedBoxMon
Palm260_RotomPCDone::
	call Common_EventScript_TransferredToPC
Palm260_RotomDone::
	setflag FLAG_HT_GIFT_ROTOM
	msgbox Palm260_TextRotomAfter, MSGBOX_DEFAULT
	removeobject VAR_LAST_TALKED
	release
	end

Palm260_RotomFanfare::
	bufferspeciesname STR_VAR_2, SPECIES_ROTOM
	playfanfare MUS_OBTAIN_ITEM
	message Palm260_TextObtainedMon
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_ROTOM
	return

Palm260_RotomAfter::
	msgbox Palm260_TextRotomAfter, MSGBOX_DEFAULT
	release
	end

Palm260_RotomBefore::
	msgbox Palm260_TextRotomBefore, MSGBOX_DEFAULT
	release
	end

Palm260_TextRotomOffer:
	.string "The relays are off. The ROTOM is free!\p"
	.string "It spins around you and buzzes happily.\n"
	.string "It seems to want to come along.$"

Palm260_TextRotomAfter:
	.string "Bzzzt!$"

Palm260_GiftFurfrou::
	lock
	faceplayer
	goto_if_set FLAG_HT_GIFT_FURFROU, Palm260_FurfrouAfter
	goto_if_unset FLAG_HT_TRADEPOST_DONE, Palm260_FurfrouBefore
	msgbox Palm260_TextFurfrouOffer, MSGBOX_DEFAULT
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_FURFROU
	givemon SPECIES_FURFROU, 27
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, Palm260_FurfrouParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, Palm260_FurfrouPC
	goto Common_EventScript_NoMoreRoomForPokemon
	end

Palm260_FurfrouParty::
	call Palm260_FurfrouFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_FurfrouDone
	call Common_EventScript_GetGiftMonPartySlot
	call Common_EventScript_NameReceivedPartyMon
	goto Palm260_FurfrouDone
	end

Palm260_FurfrouPC::
	call Palm260_FurfrouFanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Palm260_FurfrouPCDone
	call Common_EventScript_NameReceivedBoxMon
Palm260_FurfrouPCDone::
	call Common_EventScript_TransferredToPC
Palm260_FurfrouDone::
	setflag FLAG_HT_GIFT_FURFROU
	msgbox Palm260_TextFurfrouAfter, MSGBOX_DEFAULT
	release
	end

Palm260_FurfrouFanfare::
	bufferspeciesname STR_VAR_2, SPECIES_FURFROU
	playfanfare MUS_OBTAIN_ITEM
	message Palm260_TextObtainedMon
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_FURFROU
	return

Palm260_FurfrouAfter::
	msgbox Palm260_TextFurfrouAfter, MSGBOX_DEFAULT
	release
	end

Palm260_FurfrouBefore::
	msgbox VerdanturfTown_House_Text_TrainersGatherAtPokemonLeague, MSGBOX_DEFAULT
	release
	end

Palm260_TextFurfrouOffer:
	.string "With the fair open again, my salon is\n"
	.string "full of customers!\p"
	.string "This FURFROU was waiting for a new\n"
	.string "partner. It's freshly groomed, too.\p"
	.string "Would you give it a home?$"

Palm260_TextFurfrouAfter:
	.string "Bring it back anytime for a trim.\n"
	.string "A happy FURFROU is a stylish FURFROU!$"

Palm260_TextObtainedMon:
	.string "{PLAYER} received {STR_VAR_2}!$"

Palm260_TextRotomBefore:
	.string "Bzzt… A ROTOM is trapped in the relay's\n"
	.string "current. It can't get out.$"
