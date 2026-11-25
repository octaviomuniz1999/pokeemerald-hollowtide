#!/usr/bin/env python3
"""Eventos de Dawnmere e da Route 1 nas posicoes do GBA (CP-DS-03B, etapas 3 e 4).

Os eventos ja portados no CP-DS-01/02 (zonas 057_T20 = Dawnmere e 030_R29 = Route 1) ficam com os mesmos scripts e
textos; so mudam de lugar, para os tiles do mapa do GBA no desenho global (gba2grade.py):
  mundo = (X0 + x_global, Z0 + z_global) (lunia_mundo.py); global = tile do GBA + origem do mapa no desenho
  (Dawnmere/LittlerootTown (2, 2); Route 1/Route101 (36, 19)).
Os NPCs ficam parados olhando para o lado do GBA (tipos de movimento do HGSS: 14 cima, 15 baixo, 16 esquerda,
17 direita, conferidos nos eventos originais).
Gera os patches da pasta de conteudo (07xx), sobre o estado da pasta de conteudo ja aplicado no hg-engine pelo build.sh (sem
estes patches: reverta-os com patch -R antes de regenerar):
  0700-dawnmere-eventos-gba.patch   (zone_event/057_T20.json)
  0701-dawnmere-trava-leste.patch   (scr_seq_0842_T20.s: a saida volta a ser a leste; o passo de volta e para oeste)
  0702-route1-eventos-gba.patch     (zone_event/030_R29.json)
  0703-harvestvale-eventos-gba.patch (zone_event/064_T21.json)
  0704-harvestvale-saida-sul.patch  (scr_seq_0850_T21.s: a saida para a Route 2 e a do sul, como no GBA)
  0706-route2-r30-eventos-gba.patch (zone_event/031_R30.json: Route 2, linhas 0-31 do GBA)
  0710-breezeport-eventos-gba.patch (zone_event/074_T26.json: Breezeport, mais o fim da Route 2 na linha dividida)
  0711-breezeport-scripts.patch     (scr_seq_0911_T26.s: placa e porta da Route 2, saida oeste para a Route 3, a pe)
  0714-route3-eventos-gba.patch     (zone_event/040_R39.json: Route 3 original, header da Route 39)
  0715-route3-placas.patch          (scr_seq_0249_R39.s: as 3 placas da Route 3)
  0716-route3-itens.patch           (scr_seq_0141.s: Big Pearl, Great Ball e Revive)
  0717-ferralia-eventos-gba.patch   (zone_event/073_T25.json: Ferralia original, header de Goldenrod)
  0718-ferralia-scripts.patch       (scr_seq_0885_T25.s: NPCs, placas, patio de cargas, porta do ginasio e portao leste)
  0719-ferralia-ginasio-eventos.patch (zone_event/133_T25GYM0101.json: Vessel e os treinadores do ginasio)
Uso: eventos_gba.py HG_ENGINE PASTA_SAIDA
"""
import difflib, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from lunia_mundo import X0, Z0, ORIGENS, gba   # canto do desenho na matriz 0 e de cada mapa do GBA no desenho
HG = None
_FLAGS = json.load(open(os.path.join(os.path.dirname(__file__), "..", "..", "hollowtide_ds/data/flags.json")))
CARGO = _FLAGS["FLAG_HT_FERRALIA_CARGO_DONE"]           # flag do HGSS por tras da do Hollowtide (para o JSON de zona)
OLHA = {"cima": (14, 0), "baixo": (15, 1), "esquerda": (16, 2), "direita": (17, 3)}

ZONAS = {
    "057_T20": dict(
        origem=ORIGENS["Dawnmere"],
        # script do evento do DS -> (tile do GBA, lado para onde olha) no LittlerootTown
        objetos={"_EV_scr_seq_T20_015 + 1": ((23, 18), "baixo"),     # guia (Palm040_Guide)
                 "_EV_scr_seq_T20_001 + 1": ((11, 24), "baixo"),     # vizinho (Palm040_Neighbor)
                 "_EV_scr_seq_T20_017 + 1": ((23, 10), "baixo")},    # mirante (Palm051_OverlookNpc)
        placas={"_EV_scr_seq_T20_013 + 1": (15, 9),                  # Palm040_LabSign
                "_EV_scr_seq_T20_007 + 1": (11, 19),                 # Palm040_HomeSign
                "_EV_scr_seq_T20_016 + 1": (18, 16),                 # Palm040_NeighborSign
                "_EV_scr_seq_T20_014 + 1": (17, 19)},                # Palm040_TownSign
        # placa da Route 1 do CP-DS-01 (script 19): sai; no GBA a Route 1 tem as placas norte e sul (0702)
        tirar_placas={"19"},
        # warps por destino; o GBA tem 3 portas. Os dois warps do HGSS sem par ficam nas portas decorativas (tiles
        # bloqueados, inalcancaveis), para os interiores continuarem com a volta valida.
        warps={"MAP_T20R0201": (2, 9),     # casa do jogador (T20R0201/0202) = BRENDANS_HOUSE (o jogo novo comeca nela)
               "MAP_T20R0101": (13, 8),    # laboratorio (T20R0101): porta do modelo, 1 tile a oeste do warp do GBA (14,8)
               "MAP_T20R0301": (20, 16),   # casa vizinha = MAYS_HOUSE
               "MAP_T20R0401": (8, 23),    # sem par no GBA: porta decorativa (bloqueada)
               "MAP_T20R0102": (20, 23)},  # sem par no GBA: porta decorativa (bloqueada)
        # trava da saida (Palm040_ExitEast): os tiles do GBA (33, 21-22); Dawnmere inteira fica numa celula so
        coord={"_EV_scr_seq_T20_002 + 1": ("gba", 33, 21, 1, 2)},
    ),
    "030_R29": dict(
        origem=ORIGENS["Route1"],
        objetos={"_EV_scr_seq_R29_002 + 1": ((12, 6), "esquerda"),   # andarilho (Palm050_Walker)
                 "485 - 1 + _std_npc_trainer": ((22, 25), "esquerda"),   # Kai (TRAINER_PALM_KAI)
                 "487 - 1 + _std_npc_trainer": ((17, 39), "direita"),    # Min (TRAINER_PALM_MIN)
                 "std_itemball_r29_potion": ((13, 24), None)},           # Potion
        placas={"_EV_scr_seq_R29_005 + 1": (7, 21),                  # Palm050_NorthSign
                "_EV_scr_seq_R29_004 + 1": (6, 48)},                 # Palm050_SouthSign
        tirar_placas=set(), warps={}, coord={},
        # arvore de frutas do GBA (Oran, 37,46): o HGSS nao tem arvore de frutas no campo; vira arvore de Apricorn
        # (diretor, 25/11). Numero 5: livre (era de uma das arvores das Routes 29-31, que o conteudo tirou)
        novos_obj=[{"de": "040_R39", "script": "std_apricorn_tree", "mapa": "Route1", "gba": (37, 46),
                    "campos": {"param0": 5}}],
        
    ),
    "064_T21": dict(
        origem=ORIGENS["Harvestvale"],
        # as linhas 0-4 de Harvestvale caem numa celula da Route 1 (um header por celula): o fazendeiro e a chegada
        # descem 3 linhas (GBA (11,3) e linha 2), para ficarem na zona de Harvestvale
        objetos={"_EV_scr_seq_T21_000 + 1": ((11, 6), "esquerda"),   # fazendeiro (Palm060_Farmer / Palm071)
                 "_EV_scr_seq_T21_004 + 1": ((7, 32), "baixo")},     # recruta da Team Palm no quiosque (Palm060_Kiosk)
        placas={"_EV_scr_seq_T21_006 + 1": (12, 11),                 # Palm060_Welcome
                "_EV_scr_seq_T21_005 + 1": (7, 22),                  # Palm060_GymSign
                "_EV_scr_seq_T21_007 + 1": (20, 35),                 # Palm060_ClosedRoad
                "_EV_scr_seq_T21_008 + 1": (10, 32),                 # Palm060_KioskSign
                "_EV_scr_seq_T21_009 + 1": (27, 23),                 # valvula = Palm062_WaterSign
                "12": (26, 19),                                      # Palm062_CoffeeSign
                "13": (16, 34),                                      # Palm064_DryingYard
                "14": (24, 18)},                                     # Palm064_WaterBoard
        tirar_placas=set(),
        warps={"MAP_T21PC0101": (12, 21),     # Centro Pokemon
               "MAP_T21FS0101": (23, 31),     # Poke Mart
               "MAP_T21R0301": (17, 11),      # OLDALE_TOWN_HOUSE1
               "MAP_T07GYM0101": (5, 21),     # ginasio do Nevard
               "MAP_T21R0501": (21, 18)},     # OLDALE_TOWN_HOUSE2
        coord={"_EV_scr_seq_T21_001 + 1": ("gba", 8, 5, 4, 1),       # chegada pelo norte (Palm072_Arrival, GBA linha 2)
               "_EV_scr_seq_T21_002 + 1": ("gba", 17, 35, 3, 1),     # saida sul para a Route 2 (Palm080_LeaveColheita)
               "_EV_scr_seq_T21_003 + 1": ("gba", 5, 22, 1, 1)},     # porta do ginasio fechada: o tile abaixo da porta
    ),
    # Route 2 (PalmRoute02): as linhas 0-31 caem nas celulas de header R30, as 32-47 nas de header R31 (as duas zonas
    # que ja eram a Route 2 do prototipo)
    "031_R30": dict(
        origem=ORIGENS["Route2"],
        objetos={"488 - 1 + _std_npc_trainer": ((26, 13), "esquerda"),   # Liang (Palm080_RouteLIANG)
                 "489 - 1 + _std_npc_trainer": ((16, 27), "direita"),    # Mei Lan (Palm080_RouteMEI_LAN)
                 "std_itemball_r30_potion": ((7, 26), None)},            # Super Potion
        placas={"_EV_scr_seq_R30_005 + 1": (16, 3)},                     # Palm080_RouteSignNorth
        tirar_placas={"_EV_scr_seq_R30_006 + 1"},   # porta trancada: a casa fica nas linhas do R31 (scr_seq_R31_003)
        warps={}, coord={},
    ),
    # Breezeport (PalmBrisa), header de Olivine (T26). A linha de blocos 5 e dividida com o fim da Route 2 e fica com
    # o header de Breezeport: Qin, a placa sul e a porta trancada da Route 2 entram nesta zona (novos_*)
    "074_T26": dict(
        origem=ORIGENS["Brisa"],
        objetos={"1": ((45, 29), "baixo"),        # artista, anfitria do festival (Palm080_BrisaHost)
                 "2": ((21, 8), "esquerda"),      # Palm093_Greeter
                 "5": ((30, 25), None),           # Palm093_PlazaGirl
                 "6": ((47, 7), "esquerda"),      # Palm093_LookoutHiker
                 "7": ((20, 41), None),           # Palm093_BeachWoman
                 "8": ((36, 44), "baixo"),        # Palm093_Fisherman
                 "9": ((50, 36), None),           # Palm093_JayFan
                 "10": ((64, 46), "baixo"),       # Palm093_KeeperOldMan
                 "11": ((12, 31), None),          # Palm093_PumpWife
                 "12": ((36, 19), None),          # Palm093_StoreKid (fala do Poke Mart)
                 "14": ((49, 30), "baixo")},      # Palm093_FestivalBeauty
        placas={"15": (22, 3),                    # Palm080_BrisaSign
                "16": (50, 28),                   # Palm090_TheaterSign
                "17": (27, 21),                   # Palm090_PalmPoster
                "18": (2, 37),                    # Palm090_EastSign (Route 3)
                "19": [(62, 43), (63, 43)],       # Palm092/Palm280_KeeperHouse
                "20": (12, 21), "21": (33, 22), "22": (60, 35)},   # lampioes do festival (Palm090_CityLamp1-3)
        tirar_placas=set(),
        warps={"MAP_T26GYM0101": (47, 27),        # Teatro (ginasio da Jay)
               "MAP_T26PC0101": (23, 16), "MAP_T26FS0101": (14, 16),
               "MAP_T26R0301": (4, 24), "MAP_T26R0501": (15, 24), "MAP_T26R0601": (4, 30),
               "MAP_R31R0101": (56, 33)},         # guarita do prototipo: sem uso (porta decorativa da loja, bloqueada)
        coord={"23": ("gba", 47, 28, 1, 1),       # porta do Teatro fechada ate as luzes: o tile abaixo da porta
               "24": ("gba", 0, 32, 1, 28)},      # saida para a Route 3: a borda oeste do GBA (Palm090_ToRoute03)
        novos_bg=[{"script": "3", "type": 1, "mapa": "Route2", "gba": (17, 40), "player_facing_dir": 4},   # placa sul
                  {"script": "4", "type": 1, "mapa": "Route2", "gba": (14, 36), "player_facing_dir": 4}],  # porta trancada
        novos_obj=[{"de": "032_R31", "script": "490 - 1 + _std_npc_trainer", "mapa": "Route2", "gba": (21, 35),
                    "lado": "esquerda"}],   # Qin
    ),
    # Route 3 (PalmRoute03), header da Route 39 (a Route 3 do prototipo, area de Olivine). Os eventos do HGSS que nao
    # existem em Lunia (Miltanks, fazendeiro, Cameron, Jasmine, a arvore de Apricorn) ficam escondidos; os 4
    # treinadores da Route 39 viram 4 dos 5 da Route 3 (ids ja convertidos no 0100) e o 5o e um objeto novo
    "040_R39": dict(
        origem=ORIGENS["Route3"],
        objetos={"TRAINER_SAILOR_EUGENE - 1 + _std_npc_trainer": ((36, 62), "esquerda", {     # Rui (Palm100_RouteRUI)
                     "script": "472 - 1 + _std_npc_trainer", "graphics_id": "SPRITE_FISHING_2", "param0": 4}),
                 "TRAINER_POKEFAN_M_DEREK - 1 + _std_npc_trainer": ((43, 44), "esquerda", {  # Tomas
                     "script": "401 - 1 + _std_npc_trainer", "graphics_id": "SPRITE_GSBOY3", "param0": 3}),
                 "TRAINER_POKEFAN_RUTH - 1 + _std_npc_trainer": ((12, 26), "direita", {      # Bento
                     "script": "432 - 1 + _std_npc_trainer", "graphics_id": "SPRITE_MOUNT_2", "param0": 3}),
                 "TRAINER_PSYCHIC_M_NELSON - 1 + _std_npc_trainer": ((33, 30), "esquerda", { # Iara
                     "script": "426 - 1 + _std_npc_trainer", "graphics_id": "SPRITE_PICNICGIRL_2", "param0": 2}),
                 "std_itemball_r39_tm60": ((3, 74), None)},          # Big Pearl (0716: o script de item troca o TM60)
        esconder={"_EV_scr_seq_R39_000 + 1", 0, "std_apricorn_tree", "_EV_scr_seq_R39_006 + 1", "_EV_scr_seq_R39_007 + 1"},
        placas={"_EV_scr_seq_R39_003 + 1": (28, 3),                  # Palm100_SignPlateau (0715)
                "_EV_scr_seq_R39_004 + 1": (42, 54),                 # Palm100_SignBeach
                "_EV_scr_seq_R39_005 + 1": (19, 61)},                # porta trancada da casa da praia (Palm280_DoorLocked)
        tirar_placas={"std_hiddenitem_r39_nugget", "std_hiddenitem_r39_pp_up", "std_hiddenitem_r39_x_attack",
                      "std_hiddenitem_r39_t26_full_heal"},            # itens escondidos do HGSS: o GBA nao tem
        # os warps da fazenda (casa e celeiro da Route 39) ficam no telhado da casa da praia (tiles bloqueados)
        warps={"MAP_R39R0101": (19, 58), "MAP_R39R0201": (20, 58)},
        coord={}, tirar_coord={"_EV_scr_seq_R39_002 + 1"},
        novos_obj=[{"de": "040_R39", "script": "TRAINER_SAILOR_EUGENE - 1 + _std_npc_trainer", "mapa": "Route3",
                    "gba": (30, 8), "lado": "baixo",                  # Davi (Palm100_RouteDAVI)
                    "campos": {"script": "439 - 1 + _std_npc_trainer", "graphics_id": "SPRITE_CAMPBOY_2", "param0": 2}},
                   {"de": "039_R38", "script": "std_itemball_r38_max_potion", "mapa": "Route3", "gba": (18, 29)},   # Great Ball
                   {"de": "039_R38", "script": "std_itemball_r38_lax_incense", "mapa": "Route3", "gba": (8, 9)}],   # Revive
    ),
    # Ferralia (PalmFerralia), header de Goldenrod (T25). Os NPCs e placas de Goldenrod ganham scripts simples com as
    # falas do GBA (0718); os da invasao da Equipe Rocket que sobram ficam escondidos. O evento do patio de cargas
    # (dono do patio e os dois recrutas, que destrava o ginasio) e o interior do ginasio ficam para a proxima etapa:
    # ate la a porta do ginasio fica trancada.
    "073_T25": dict(
        origem=ORIGENS["Ferralia"],
        objetos={"_EV_scr_seq_T25_000 + 1": ((41, 47), "baixo", {"graphics_id": "SPRITE_MAN1", "hidden_flag": "FLAG_NOTHING"}),
                 "_EV_scr_seq_T25_001 + 1": ((62, 35), "cima", {"graphics_id": "SPRITE_WORKMAN", "hidden_flag": "FLAG_NOTHING"}),
                 "_EV_scr_seq_T25_002 + 1": ((50, 15), "baixo", {"graphics_id": "SPRITE_GENTLEMAN", "hidden_flag": "FLAG_NOTHING"}),
                 "_EV_scr_seq_T25_003 + 1": ((28, 36), "baixo", {"graphics_id": "SPRITE_BOY1", "hidden_flag": "FLAG_NOTHING"}),
                 "_EV_scr_seq_T25_004 + 1": ((45, 39), "baixo", {"graphics_id": "SPRITE_MAN2", "hidden_flag": "FLAG_NOTHING"}),
                 "_EV_scr_seq_T25_005 + 1": ((12, 20), "baixo", {"graphics_id": "SPRITE_WOMAN2", "hidden_flag": "FLAG_NOTHING"}),
                 "_EV_scr_seq_T25_006 + 1": ((29, 15), "baixo", {"graphics_id": "SPRITE_ASSISTANTM", "hidden_flag": "FLAG_NOTHING"}),
                 "_EV_scr_seq_T25_007 + 1": ((31, 56), "baixo", {"graphics_id": "SPRITE_OLDWOMAN1", "hidden_flag": "FLAG_NOTHING"}),
                 # patio de cargas: Vessel e os dois recrutas da Team Palm; somem com FLAG_HT_FERRALIA_CARGO_DONE (a flag
                 # do HGSS por tras dela: o JSON de zona nao inclui hollowtide_flags.inc)
                 "_EV_scr_seq_T25_008 + 1": ((63, 29), "esquerda", {"graphics_id": "SPRITE_BIGMAN", "hidden_flag": CARGO}),
                 "_EV_scr_seq_T25_009 + 1": ((67, 28), "esquerda", {"script": "448 - 1 + _std_npc_trainer", "trainer_type": 1,
                                                                   "param0": 2, "hidden_flag": CARGO}),
                 "_EV_scr_seq_T25_010 + 1": ((66, 35), "cima", {"script": "447 - 1 + _std_npc_trainer", "trainer_type": 1,
                                                               "param0": 2, "hidden_flag": CARGO})},
        esconder={"_EV_scr_seq_T25_011 + 1",
                  "_EV_scr_seq_T25_012 + 1", "_EV_scr_seq_T25_013 + 1", "_EV_scr_seq_T25_014 + 1", "_EV_scr_seq_T25_015 + 1",
                  "_EV_scr_seq_T25_016 + 1", "_EV_scr_seq_T25_030 + 1", "_EV_scr_seq_T25_031 + 1", "_EV_scr_seq_T25_032 + 1", 0},
        placas={"_EV_scr_seq_T25_019 + 1": (39, 47),                 # Palm101_CitySign
                "_EV_scr_seq_T25_020 + 1": (45, 11),                 # Palm101_GymSign
                "_EV_scr_seq_T25_021 + 1": (27, 14),                 # Palm101_HQSign
                "_EV_scr_seq_T25_022 + 1": (57, 27),                 # Palm101_YardSign
                "_EV_scr_seq_T25_023 + 1": (69, 39),                 # Palm101_Route4Sign
                "_EV_scr_seq_T25_024 + 1": (64, 8),                  # Palm280_DoorLocked (mais 11 portas em novos_bg)
                "_EV_scr_seq_T25_025 + 1": (44, 67)},                # placa do plato da Route 3 (GBA 28,3 da Route 3):
                                                                      # o tile cai numa celula de Ferralia
        tirar_placas={"_EV_scr_seq_T25_026 + 1", "_EV_scr_seq_T25_027 + 1", "_EV_scr_seq_T25_028 + 1",
                      "_EV_scr_seq_T25_029 + 1", "std_hiddenitem_r34_t25_super_potion"},
        novos_bg=[{"script": "_EV_scr_seq_T25_024 + 1", "type": 1, "gba": p, "player_facing_dir": 4}
                  for p in ((20, 10), (46, 25), (53, 25), (6, 36), (12, 36), (6, 47), (22, 47), (32, 47), (54, 47), (63, 47))],
        # o ginasio abre depois do patio de cargas: gatilho no tile da frente da porta (script 026, sem placa agora)
        novos_coord=[{"script": "_EV_scr_seq_T25_026 + 1", "gba": (49, 13), "width": 1, "length": 1, "value": 0,
                      "var": "VAR_TEMP_x4003"}],
        # portas do GBA -> interiores de Goldenrod no mesmo papel; os warps de Goldenrod sem par vao para o telhado da
        # estacao (tiles bloqueados)
        warps={"MAP_T25R0501": (28, 12), "MAP_T25PC0101": (20, 24), "MAP_T25R1001": (36, 24),
               "MAP_T25R0301": (12, 11), "MAP_T25R0401": (37, 11), "MAP_T25R0801": (48, 47),
               "MAP_T25R0901": (5, 12), "MAP_T25R0201": (8, 27),
               "MAP_T25GYM0101": (49, 12), "MAP_R35R0101": (26, 5), "MAP_T25R0601": (31, 5), "MAP_T25SP0101": (32, 5),
               "MAP_D23R0101": (25, 6), "MAP_D37R0101": (26, 6), "MAP_T25R1201": (31, 6)},
        # portao leste (Palm103_EastGate): a Route 4 nao existe. O gatilho de Goldenrod so disparava durante a invasao
        # Rocket (variavel e valor do HGSS): com a variavel temporaria em 0 ele dispara sempre
        coord={"_EV_scr_seq_T25_017 + 1": ("gba", 70, 40, 1, 2, {"var": "VAR_TEMP_x4002", "value": 0})},
    ),
    # Ginasio de Ferralia (GBA MauvilleCity_Gym do Hollowtide: Vessel e treinadores) no interior do ginasio de Goldenrod;
    # posicoes do HGSS (origem 0,0: interior). Os 4 treinadores de Goldenrod viram Kirk, Shawn, Ben e Vivian; o 5o do
    # GBA (Angelo) fica de fora: o ginasio de Goldenrod nao tem um tile livre que nao feche o caminho. O quebra-cabeca de
    # chaves e portoes do GBA tambem fica de fora (scripts no overlay: scr_seq_0886_T25GYM0101.s)
    "133_T25GYM0101": dict(
        origem=(0, 0),
        objetos={"_EV_scr_seq_T25GYM0101_000 + 1": ((13, 4), None, {"graphics_id": "SPRITE_BIGMAN", "hidden_flag": "FLAG_NOTHING"}),
                 "TRAINER_LASS_CATHY - 1 + _std_npc_trainer": ((14, 15), None, {"script": "467 - 1 + _std_npc_trainer",
                                                                               "graphics_id": "SPRITE_MAN3", "param0": 2}),
                 "TRAINER_LASS_CARRIE - 1 + _std_npc_trainer": ((9, 18), None, {"script": "499 - 1 + _std_npc_trainer",
                                                                               "graphics_id": "SPRITE_MAN3", "param0": 1}),
                 "TRAINER_BEAUTY_VICTORIA - 1 + _std_npc_trainer": ((6, 11), None, {"script": "410 - 1 + _std_npc_trainer",
                                                                                   "graphics_id": "SPRITE_GSBOY1", "param0": 2}),
                 "TRAINER_BEAUTY_SAMANTHA - 1 + _std_npc_trainer": ((24, 18), None, {"script": "510 - 1 + _std_npc_trainer",
                                                                                    "graphics_id": "SPRITE_GIRL3", "param0": 2})},
        placas={}, tirar_placas=set(), warps={}, coord={}, tirar_coord={"_EV_scr_seq_T25GYM0101_001 + 1"},
    ),
}


def mover(j, z):
    ox, oy = z["origem"]
    w = lambda x, y: (X0 + ox + x, Z0 + oy + y)
    for o in j["object_events"]:
        if o["script"] in z["objetos"]:
            val = z["objetos"][o["script"]]
            (x, y), lado = val[0], val[1]
            o["x"], o["z"] = w(x, y)
            if lado:
                o["movement_type"], o["initial_dir"] = OLHA[lado]
                o["movement_range_x"] = o["movement_range_z"] = 0
            for k, v in (val[2] if len(val) > 2 else {}).items():   # troca de treinador/sprite (Route 3)
                o[k] = v
        elif o["script"] in z.get("esconder", ()):
            o["hidden_flag"] = "FLAG_GOT_TRAINER_CARD"   # ligada no comeco do jogo: o NPC do HGSS nunca aparece
    j["coord_events"] = [c for c in j.get("coord_events", []) if c["script"] not in z.get("tirar_coord", ())]
    j["bg_events"] = [b for b in j["bg_events"] if b["script"] not in z["tirar_placas"]]
    usados = {}
    for b in j["bg_events"]:
        if b["script"] in z["placas"]:
            pos = z["placas"][b["script"]]
            if isinstance(pos, list):                    # o mesmo script em varias placas: na ordem do arquivo
                k = usados.get(b["script"], 0); usados[b["script"]] = k + 1
                pos = pos[min(k, len(pos) - 1)]
            b["x"], b["z"] = w(*pos)
    for wp in j["warp_events"]:
        if wp["dest_header_id"] in z["warps"]:
            wp["x"], wp["z"] = w(*z["warps"][wp["dest_header_id"]])
    for o in z.get("novos_obj", []):
        src = json.load(open(os.path.join(HG, f"data/eventdata/zone_event/{o['de']}.json")))
        n = dict(next(e for e in src["object_events"] if e["script"] == o["script"]))
        n["id"] = len(j["object_events"])               # id numerico (um nome obj_* precisaria de simbolo no hg-engine)
        n["x"], n["z"] = gba(o["mapa"], *o["gba"])
        if o.get("lado"):
            n["movement_type"], n["initial_dir"] = OLHA[o["lado"]]
            n["movement_range_x"] = n["movement_range_z"] = 0
        for k, v in o.get("campos", {}).items():
            n[k] = v
        j["object_events"].append(n)
    for b in z.get("novos_bg", []):
        x, zz = gba(b["mapa"], *b["gba"]) if "mapa" in b else w(*b["gba"])
        j.setdefault("bg_events", []).append({"script": b["script"], "type": b["type"], "x": x, "z": zz, "y": 0,
                                              "player_facing_dir": b["player_facing_dir"]})
    for c in z.get("novos_coord", []):
        x, zz = w(*c["gba"])
        j.setdefault("coord_events", []).append({"script": c["script"], "x": x, "z": zz, "width": c["width"],
                                                 "length": c["length"], "y": 0, "value": c["value"], "var": c["var"]})
    for c in j.get("coord_events", []):
        if c["script"] in z["coord"]:
            ref, cx, cz, wd, ln = z["coord"][c["script"]][:5]
            c["x"], c["z"] = (X0 + cx, Z0 + cz) if ref == "global" else w(cx, cz)
            c["width"], c["length"] = wd, ln
            for k, v in (z["coord"][c["script"]][5] if len(z["coord"][c["script"]]) > 5 else {}).items():
                c[k] = v                                 # variavel/valor que armam o gatilho
    return j


def diff(rel, old, new):
    """Diff unificado aplicavel pelo patch(1), com a marca de arquivo sem quebra de linha no fim."""
    out = []
    for line in difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + rel, "b/" + rel):
        out.append(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n")
    return "".join(out)


def zona(hg, out, nome, arquivo):
    rel = f"data/eventdata/zone_event/{nome}.json"
    old = open(os.path.join(hg, rel)).read()
    new = json.dumps(mover(json.loads(old), ZONAS[nome]), indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")
    open(os.path.join(out, arquivo), "w").write(diff(rel, old, new))


def main(hg, out):
    global HG
    HG = hg
    zona(hg, out, "057_T20", "0700-dawnmere-eventos-gba.patch")
    zona(hg, out, "030_R29", "0702-route1-eventos-gba.patch")
    zona(hg, out, "064_T21", "0703-harvestvale-eventos-gba.patch")
    zona(hg, out, "031_R30", "0706-route2-r30-eventos-gba.patch")
    zona(hg, out, "074_T26", "0710-breezeport-eventos-gba.patch")
    # Breezeport: placa sul e porta trancada da Route 2 (zona de Breezeport); a saida para a Route 3 e a borda oeste
    # (passo de volta para leste) e, depois da Jay, a ponte provisoria para a Route 39 (a Route 3 do prototipo)
    rel = "data/scr_seq/scr_seq_0911_T26.s"
    old = open(os.path.join(hg, rel)).read()
    a = "scr_seq_T26_002:\nscr_seq_T26_003:\nscr_seq_T26_012:\n"
    assert a in old
    new = old.replace(a, "scr_seq_T26_012:\n")
    sign = lambda lab, msg, nota: (f"// {nota}\n{lab}:\n\tplay_se SEQ_SE_DP_SELECT\n\tlockall\n\tnpc_msg {msg}\n"
                                   "\twait_button\n\tclosemsg\n\treleaseall\n\tend\n\n")
    new = new.replace("// gatilhos de quadro e carga do HGSS (rival, Jasmine): nada\n",
                      sign("scr_seq_T26_002", 20, "placa sul da Route 2 (a linha de blocos 5 e de Breezeport)") +
                      sign("scr_seq_T26_003", 21, "porta trancada da Route 2 (Palm280_DoorLocked)") +
                      "// gatilhos de quadro e carga do HGSS (rival, Jasmine): nada\n", 1)
    new = new.replace("// saida norte (Route 3): fechada ate vencer a Jay",
                      "// saida para a Route 3: a borda oeste, como no GBA (Palm090_ToRoute03); fechada ate vencer a Jay")
    a = new.index("scr_seq_T26_023:"); b = new.index("_HT_NorthOpen:", a)
    new = new[:a] + new[a:b].replace("_HT_StepDown", "_HT_StepRight") + new[b:]
    # depois da Jay, a trava so libera a passagem (a variavel muda e o gatilho nao dispara mais): a Route 3 original
    # esta no desenho, a oeste, e se chega a pe (ate 25/11 havia aqui uma ponte provisoria para a Route 39)
    new = new.replace("_HT_NorthOpen:\n\tsetvar VAR_UNK_4078, 2\n\treleaseall\n\tend\n",
                      "_HT_NorthOpen:\n\tsetvar VAR_UNK_4078, 2   // a Route 3 fica a oeste, a pe\n\treleaseall\n\tend\n")
    new = new.rstrip("\n") + "\n_HT_StepRight:\n\tstep MOVEMENT_STEP_RIGHT, 1\n\tstep_end\n\t.balign 4\n"
    assert new.count("_HT_StepRight") == 2 and "a Route 3 fica a oeste" in new
    open(os.path.join(out, "0711-breezeport-scripts.patch"), "w").write(diff(rel, old, new))
    # Route 3: eventos nas posicoes do GBA (zona da Route 39)
    zona(hg, out, "040_R39", "0714-route3-eventos-gba.patch")
    # placas da Route 3: as da Route 39 eram placa de direcao e dicas de treinador; viram placas simples com as falas
    # do GBA (texts.json, banco 396)
    rel = "data/scr_seq/scr_seq_0249_R39.s"
    old = open(os.path.join(hg, rel)).read()
    new = old
    for scr, msg, nota in (("003", 0, "Palm100_SignPlateau"), ("004", 1, "Palm100_SignBeach"),
                           ("005", 2, "porta trancada da casa da praia (Palm280_DoorLocked)")):
        a = new.index(f"scr_seq_R39_{scr}:\n"); b = new.index("\tend\n", a) + len("\tend\n")
        new = new[:a] + (f"scr_seq_R39_{scr}:   // Route 3: {nota}\n\tplay_se SEQ_SE_DP_SELECT\n\tlockall\n"
                         f"\tnpc_msg {msg}\n\twait_button\n\tclosemsg\n\treleaseall\n\tend\n") + new[b:]
    assert new != old
    open(os.path.join(out, "0715-route3-placas.patch"), "w").write(diff(rel, old, new))
    # itens da Route 3 (GBA): Big Pearl, Great Ball e Revive, nos scripts de item da Route 39 (TM60) e da Route 38
    # (fora de Lunia)
    rel = "data/scr_seq/scr_seq_0141.s"
    old = open(os.path.join(hg, rel)).read()
    new = old
    for scr, era, item, nota in (("084", 387, 89, "Big Pearl (PalmRoute03 3,74); era TM60"),
                                 ("082", 24, 3, "Great Ball (PalmRoute03 18,29); era Max Potion da Route 38"),
                                 ("083", 255, 28, "Revive (PalmRoute03 8,9); era Lax Incense da Route 38")):
        a = f"scr_seq_0141_{scr}:\n\tsetvar VAR_SPECIAL_x8008, {era}\n"
        assert a in new, scr
        new = new.replace(a, f"scr_seq_0141_{scr}:\n\tsetvar VAR_SPECIAL_x8008, {item}   // Hollowtide: {nota}\n")
    open(os.path.join(out, "0716-route3-itens.patch"), "w").write(diff(rel, old, new))
    # Ferralia: os eventos de Goldenrod nas posicoes do GBA e scripts simples com as falas do GBA (banco 581)
    zona(hg, out, "073_T25", "0717-ferralia-eventos-gba.patch")
    rel = "data/scr_seq/scr_seq_0885_T25.s"
    old = open(os.path.join(hg, rel)).read()
    new = old
    npc = lambda n, k, nota: (f"scr_seq_T25_{n}:   // Ferralia: {nota}\n\tsimple_npc_msg {k}\n\tend\n")
    placa = lambda n, k, nota: (f"scr_seq_T25_{n}:   // Ferralia: {nota}\n\tplay_se SEQ_SE_DP_SELECT\n\tlockall\n"
                                f"\tnpc_msg {k}\n\twait_button\n\tclosemsg\n\treleaseall\n\tend\n")
    trocas = [("000", npc, 0, "Palm101_Greeter"), ("001", npc, 1, "Palm101_YardWorker"),
              ("003", npc, 3, "Palm101_FountainKid"), ("004", npc, 4, "Palm101_Commuter"), ("005", npc, 5, "Palm101_Resident"),
              ("006", npc, 6, "Palm101_HQGuard"), ("007", npc, 7, "Palm101_ParkLady"),
              ("019", placa, 8, "Palm101_CitySign"), ("020", placa, 9, "Palm101_GymSign"), ("021", placa, 10, "Palm101_HQSign"),
              ("022", placa, 11, "Palm101_YardSign"), ("023", placa, 12, "Palm101_Route4Sign"),
              ("024", placa, 13, "porta trancada (Palm280_DoorLocked)"), ("025", placa, 15, "placa do plato da Route 3")]
    for n, f, k, nota in trocas:
        a = new.index(f"scr_seq_T25_{n}:\n")
        b = new.index("\n\n", a) + 1                      # o script vai ate a primeira linha em branco
        corpo = new[a:b]
        assert "\tend\n" in corpo or "goto" in corpo or "simple_npc_msg" in corpo, n
        new = new[:a] + f(n, k, nota) + new[b:]
    corpos = {
        # Vessel no patio (Palm102_VesselYard): sem vencer os dois recrutas, pede ajuda; depois agradece, os tres somem
        # e o ginasio abre (FLAG_HT_FERRALIA_CARGO_DONE)
        "008": ("scr_seq_T25_008:   // Ferralia: Vessel no patio de cargas (Palm102_VesselYard)\n\tplay_se SEQ_SE_DP_SELECT\n"
                "\tlockall\n\tfaceplayer\n\tgoto_if_defeated 448, _HT_VesselG2\n\tgoto _HT_VesselAsk\n_HT_VesselG2:\n"
                "\tgoto_if_defeated 447, _HT_VesselThanks\n_HT_VesselAsk:\n\tnpc_msg 16\n\twait_button\n\tclosemsg\n"
                "\treleaseall\n\tend\n_HT_VesselThanks:\n\tnpc_msg 17\n\twait_button\n\tclosemsg\n"
                "\tsetflag FLAG_HT_FERRALIA_CARGO_DONE\n\thide_person obj_T25_rocketm_6\n\thide_person obj_T25_rocketm_11\n"
                "\thide_person obj_T25_rocketm_8\n\treleaseall\n\tend\n"),
        # fa do ginasio (Palm101_GymFan): a fala muda depois do patio
        "002": ("scr_seq_T25_002:   // Ferralia: fa do ginasio (Palm101_GymFan)\n\tplay_se SEQ_SE_DP_SELECT\n\tlockall\n"
                "\tfaceplayer\n\tgoto_if_set FLAG_HT_FERRALIA_CARGO_DONE, _HT_GymFanOpen\n\tnpc_msg 2\n\twait_button\n"
                "\tclosemsg\n\treleaseall\n\tend\n_HT_GymFanOpen:\n\tnpc_msg 18\n\twait_button\n\tclosemsg\n"
                "\treleaseall\n\tend\n"),
        # porta do ginasio: fechada (fala e um passo para baixo) ate o patio de cargas
        "026": ("scr_seq_T25_026:   // Ferralia: porta do ginasio, fechada ate o patio de cargas\n"
                "\tgoto_if_set FLAG_HT_FERRALIA_CARGO_DONE, _HT_GymOpen\n\tlockall\n\tnpc_msg 19\n\twait_button\n"
                "\tclosemsg\n\tapply_movement obj_player, _HT_StepDown\n\twait_movement\n\treleaseall\n_HT_GymOpen:\n"
                "\tend\n"),
    }
    for n, corpo in corpos.items():
        a = new.index(f"scr_seq_T25_{n}:\n"); b = new.index("\n\n", a) + 1
        new = new[:a] + corpo + new[b:]
    if "hollowtide_flags.inc" not in new:
        a = new.index('.include "data/scr_seq/include/event_T25.inc"\n') + len('.include "data/scr_seq/include/event_T25.inc"\n')
        new = new[:a] + '.include "data/scr_seq/include/hollowtide_flags.inc"\n' + new[a:]
    # portao leste (Palm103_EastGate): a Route 4 ainda nao existe; fala do GBA e um passo para oeste
    a = new.index("scr_seq_T25_017:\n"); b = new.index("\n\n", a) + 1
    new = new[:a] + ("scr_seq_T25_017:   // Ferralia: portao leste (Palm103_EastGate); a Route 4 ainda nao existe\n"
                     "\tlockall\n\tnpc_msg 14\n\twait_button\n\tclosemsg\n\tapply_movement obj_player, _HT_StepLeft\n"
                     "\twait_movement\n\treleaseall\n\tend\n") + new[b:]
    new = new.rstrip("\n") + ("\n_HT_StepLeft:\n\tstep MOVEMENT_STEP_LEFT, 1\n\tstep_end\n\t.balign 4\n"
                               "_HT_StepDown:\n\tstep MOVEMENT_STEP_DOWN, 1\n\tstep_end\n\t.balign 4\n")
    open(os.path.join(out, "0718-ferralia-scripts.patch"), "w").write(diff(rel, old, new))
    zona(hg, out, "133_T25GYM0101", "0719-ferralia-ginasio-eventos.patch")
    rel = "data/scr_seq/scr_seq_0850_T21.s"
    old = open(os.path.join(hg, rel)).read()
    new = old.replace("// chegada pelo leste (Route 1)", "// chegada pelo norte (Route 1), como no GBA (Palm072_Arrival)")
    new = new.replace("// saida norte (Route 2): fechada ate vencer o Nevard",
                      "// saida sul (Route 2), como no GBA (Palm080_LeaveColheita): fechada ate vencer o Nevard; volta um passo para cima")
    a = new.index("scr_seq_T21_002:"); b = new.index("_HT_ExitOk:", a)
    new = new[:a] + new[a:b].replace("_HT_StepDown", "_HT_StepUp") + new[b:]
    new = new.rstrip("\n") + "\n_HT_StepUp:\n\tstep MOVEMENT_STEP_UP, 1\n\tstep_end\n\t.balign 4\n"
    assert new.count("_HT_StepUp") == 2
    open(os.path.join(out, "0704-harvestvale-saida-sul.patch"), "w").write(diff(rel, old, new))
    rel = "data/scr_seq/scr_seq_0842_T20.s"
    old = open(os.path.join(hg, rel)).read()
    new = old.replace("// saida oeste (Route 1): sem Pokemon, volta um passo (GBA Palm040_ExitEast)",
                      "// saida leste (Route 1), como no GBA: sem Pokemon, volta um passo para oeste (Palm040_ExitEast)")
    a = new.rindex("_HT_StepBack:")
    new = new[:a] + new[a:].replace("step MOVEMENT_STEP_RIGHT, 1", "step MOVEMENT_STEP_LEFT, 1", 1)
    assert new != old
    open(os.path.join(out, "0701-dawnmere-trava-leste.patch"), "w").write(diff(rel, old, new))
    print("patches de eventos gerados em", out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
