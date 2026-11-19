PalmRoute08_MapScripts::
	.byte 0

Palm180_RouteALAN::
	trainerbattle_single TRAINER_PALM_ROUTE08_ALAN, Palm180_TextALANIntro, Palm180_TextALANLoss
	msgbox Palm180_TextALANAfter, MSGBOX_AUTOCLOSE
	end

Palm180_RouteKIYO::
	trainerbattle_single TRAINER_PALM_ROUTE08_KIYO, Palm180_TextKIYOIntro, Palm180_TextKIYOLoss
	msgbox Palm180_TextKIYOAfter, MSGBOX_AUTOCLOSE
	end

Palm180_RouteCORA::
	trainerbattle_single TRAINER_PALM_ROUTE08_CORA, Palm180_TextCORAIntro, Palm180_TextCORALoss
	msgbox Palm180_TextCORAAfter, MSGBOX_AUTOCLOSE
	end

Palm180_RouteAURON::
	trainerbattle_single TRAINER_PALM_ROUTE08_AURON, Palm180_TextAURONIntro, Palm180_TextAURONLoss
	msgbox Palm180_TextAURONAfter, MSGBOX_AUTOCLOSE
	end

Palm180_SignSouth::
	msgbox Palm180_SignSouth_Text, MSGBOX_SIGN
	end

Palm180_SignView::
	msgbox Palm180_SignView_Text, MSGBOX_SIGN
	end

Palm180_SignNorth::
	msgbox Palm180_SignNorth_Text, MSGBOX_SIGN
	end


Palm180_TextALANIntro:
	.string "These slopes are older than any map.\n"
	.string "Let's see if your legs are as tough!$"

Palm180_TextALANLoss:
	.string "Whew! I'm out of breath…$"

Palm180_TextALANAfter:
	.string "Up top it gets cold fast, even in\n"
	.string "summer. The mountain keeps its winter.$"

Palm180_TextKIYOIntro:
	.string "I train against the mountain wind!\n"
	.string "You'll make a fine sparring partner!$"

Palm180_TextKIYOLoss:
	.string "My stance was too stiff…$"

Palm180_TextKIYOAfter:
	.string "A good fighter bends like grass in\n"
	.string "the wind. I still have a lot to learn.$"

Palm180_TextCORAIntro:
	.string "Each step up this slope is training!\n"
	.string "Ready for a real workout?$"

Palm180_TextCORALoss:
	.string "Okay, okay! You win this round!$"

Palm180_TextCORAAfter:
	.string "PASSWAY VILLAGE is just ahead.\n"
	.string "The hot spring there is the best!$"

Palm180_TextAURONIntro:
	.string "From here you can see the whole lake,\n"
	.string "and the clouds gathering up north.\p"
	.string "Show me what you've learned so far.$"

Palm180_TextAURONLoss:
	.string "You've walked a long road. It shows.$"

Palm180_TextAURONAfter:
	.string "Those clouds over the summit haven't\n"
	.string "moved in weeks. Strange weather…$"

Palm180_SignSouth_Text:
	.string "ROUTE 8 · OLD SLOPES\n"
	.string "South: HORIZON CITY$"

Palm180_SignView_Text:
	.string "LAKE VIEWPOINT\p"
	.string "On clear nights, the lake below\n"
	.string "holds every star in the sky.$"

Palm180_SignNorth_Text:
	.string "ROUTE 8\n"
	.string "North: PASSWAY VILLAGE$"