PalmFerralia_MapScripts::
	.byte 0

Palm091_FerraliaSign::
	msgbox Palm091_TextFerralia, MSGBOX_SIGN
	end

Palm091_DepotSign::
	msgbox Palm091_TextDepot, MSGBOX_SIGN
	end

Palm091_Worker::
	msgbox Palm091_TextWorker, MSGBOX_NPC
	end

Palm091_TextFerralia:
	.string "FERRALIA\n"
	.string "Patio de carga.\p"
	.string "Oeste: ROTA 03 e BRISA.$"
Palm091_TextDepot:
	.string "DEPOSITO FERROVIARIO\n"
	.string "Acesso restrito.$"
Palm091_TextWorker:
	.string "Antes do apito, da pra ouvir\n"
	.string "o trilho cantar.\p"
	.string "De uns dias pra ca, a Palm so\n"
	.string "descarrega depois do anoitecer.$"

Palm100_FerraliaToRoute03::
	warp MAP_PALM_ROUTE03, 25, 2
	waitstate
	end
