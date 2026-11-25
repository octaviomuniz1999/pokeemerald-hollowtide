#!/usr/bin/env python3
"""Conversao fiel dos mapas do GBA (23ap) para a grade do gerador do DS (CP-DS-03B; decisao do diretor: "siga a risca
o que fez no GBA").

Para cada tile do map.bin do GBA:
  - comportamento do metatile (metatile_attributes.bin): mato alto -> e; agua (lagoa, mar, canal) -> ~;
  - tabela explicita METATILES (id do metatile -> letra), feita conferindo a imagem de cada metatile usado
    (folhas de contato geradas por este script com --folha);
  - elevacao (bits 12-15): 3 = chao (altura 1 no DS), 4 = chao elevado (altura 2), 1 = agua, 0 = bloqueado
    (fica com a altura dos vizinhos).
Os mapas sao postos num desenho GLOBAL nas posicoes que fazem as ligacoes do GBA virarem divisas naturais
(CP-DS-03B_PLANO_SETORES.md par. 6) e o desenho e salvo no formato do mapa_grade.py (secao [tamanho] W H).
Construcoes (CONSTRUCOES): cada planta do GBA recebe um modelo do HGSS com a porta no tile do warp (ou o mais perto que
o modelo deixa); o tile da porta vira D (bloqueado com comportamento 0x69, como no HGSS).
Uso: gba2grade.py SAIDA.txt   |   gba2grade.py --folha MAPA PNG
"""
import collections, json, os, re, struct, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools", "hollowtide_qa"))

# --- tabela metatile -> letra (General = primario, 0x000-0x1FF; secundarios a partir de 0x200) -----------------------
GENERAL = {
    0x001: ".", 0x00F: "e", 0x003: "S", 0x01B: "S", 0x004: "f", 0x288: "f", 0x289: "f",
    0x00E: "T", 0x016: "T", 0x017: "T", 0x01D: "T", 0x01E: "T", 0x01F: "T", 0x026: "T", 0x027: "T", 0x1D6: "T", 0x1D7: "T",
    0x1DE: "T", 0x1DF: "T", 0x23B: "T",
    0x1CE: ".", 0x1CF: ".", 0x1D0: ".", 0x1D1: ".", 0x1D2: ".", 0x1D8: ".", 0x1D9: ".", 0x1DA: ".", 0x1E0: ".",
    0x1E1: ".", 0x1E2: ".", 0x103: ".", 0x105: ".", 0x10B: ".", 0x10D: ".", 0x113: ".", 0x115: ".",
    0x056: "c", 0x055: "#", 0x057: "#", 0x05D: "#", 0x05E: "=", 0x05F: "#", 0x065: "#", 0x067: "#",   # 05E = tabuado da ponte
    0x068: "#", 0x06A: "#", 0x070: "#", 0x072: "#", 0x078: "#", 0x079: "#", 0x07A: "#",
    0x0AF: "=",
    0x100: "=", 0x102: "=", 0x109: "=", 0x10A: "=", 0x110: "=", 0x112: "=",
    0x118: "=", 0x119: "=", 0x11A: "=", 0x120: "=", 0x121: "=", 0x122: "=", 0x128: "=", 0x129: "=", 0x12A: "=",
    0x138: "c", 0x13A: "c", 0x140: "c", 0x142: "c", 0x148: "c", 0x149: "c", 0x14A: "c",
    0x248: "=", 0x249: "=", 0x24A: "=", 0x24B: "=", 0x24C: "=", 0x250: "=", 0x251: "=", 0x252: "=", 0x253: "=",
    0x254: "=", 0x258: "=", 0x259: "=", 0x25A: "=", 0x25B: "=", 0x25C: "=",
    0x260: "#", 0x264: "#", 0x268: "#", 0x26C: "#",
    0x265: "=", 0x266: "=", 0x267: "=", 0x26D: "=", 0x26E: "=", 0x26F: "=",
}
GENERAL.update({0x1DC: "T", 0x1DD: "T",                            # metade de baixo das arvores grandes (Route 2)
                0x070: "#", 0x072: "#", 0x074: "#", 0x078: "#", 0x079: "#", 0x07A: "#", 0x07C: "#",
                0x087: "v", 0x089: "#", 0x091: "#", 0x0D5: "v", 0x0D6: "v"})       # muro do cercado e ressaltos
GENERAL.update({0x071: "#", 0x073: "#", 0x075: "#", 0x07B: "#", 0x0E2: "#",          # montanha e pedra (Breezeport)
                0x175: "#", 0x176: "#", 0x17A: "#", 0x17B: "#", 0x17C: "#", 0x17D: "#", 0x17E: "#",
                0x182: "#", 0x184: "#", 0x194: "#",                        # rochas na agua
                0x1D3: "T", 0x1DB: "T"})                                   # arbustos
GENERAL.update({0x1D4: "T", 0x1D5: "T", 0x1E4: "T", 0x1E5: "T", 0x1E6: "T", 0x1E7: "T",      # arvores grandes (Harvestvale)
                0x10C: "=", 0x104: "=", 0x114: "=", 0x124: "="})   # terra arada da plantacao e areias
GENERAL.update({0x0C6: "T", 0x0C7: "T"})                            # moita escura da borda oeste (Route 3)
PRIMARY_BUILDINGS = [range(0x028, 0x064), range(0x1AA, 0x1CE)]   # Mart/PC e ginasio do tileset General
for i in range(0x008, 0x023):
    if i not in (0x00D, 0x00E, 0x00F, 0x016, 0x017, 0x01B, 0x01D, 0x01E, 0x01F):
        GENERAL.setdefault(i, "B")          # casa de telhado vermelho do tileset General
# Metatiles a partir de 0x200 sao do tileset SECUNDARIO, que muda de mapa para mapa: as entradas >= 0x200 da tabela
# acima foram conferidas nos tilesets da Route 1 (EverGrande) e de Dawnmere (Petalburg) e so valem para eles.
SECONDARY_TABLE_TILESETS = {"gTileset_EverGrande", "gTileset_Petalburg"}
SECONDARY_BUILDINGS = range(0x200, 0x400)   # nos secundarios destes mapas, metatiles bloqueados = construcoes

# --- construcoes: modelo do HGSS sobre a planta do GBA -----------------------------------------------------------------
# Modelos com textura propria (NARC a/0/4/0); caixa (x0, x1, z0) em tiles a partir do ponto do objeto; porta = modelo da
# porta e deslocamento (dx, dz, dy) medidos nos mapas do HGSS; dtile = tile D (porta de verdade) a partir do objeto.
MODELOS = {
    0x13A: dict(nome="mst_okl (laboratorio de Pallet)", x0=-3.375, x1=3.875, z0=-2.125, porta=(0x0F, 0.0, 1.219, 0.16), dtile=(0, 1.5)),
    0x139: dict(nome="mst_rdh (casa de Pallet)", x0=-2.875, x1=3.125, z0=-2.375, porta=(0x136, -0.375, 1.219, 0.16), dtile=(-1, 1.5)),
    0x14: dict(nome="wk_hhouse (casa de New Bark)", x0=-2.875, x1=3.125, z0=-2.375, porta=(0x18, -0.375, 1.089, 0.0), dtile=(-1, 1.5)),
    0x16: dict(nome="wk_h01 (casa de New Bark)", x0=-2.25, x1=2.5, z0=-1.625, porta=(0x19, 0.126, 0.739, 0.07), dtile=(-0.5, 0.875)),
    0x25: dict(nome="yo_h01 (casa de Cherrygrove)", x0=-2.188, x1=2.5, z0=-1.625, porta=(0x32, 0.125, 0.731, 0.04), dtile=(-0.5, 1.0)),
    0x26: dict(nome="yo_h02 (casa de Cherrygrove)", x0=-2.188, x1=2.5, z0=-1.625, porta=(0x32, 0.12, 0.719, 0.04), dtile=(-0.5, 1.0)),
    0x29: dict(nome="kn_h01 (casa de Kanto)", x0=-2.188, x1=2.5, z0=-1.625, porta=(0x18, 0.113, 0.763, 0.062), dtile=(-0.5, 1.0)),
    0x27: dict(nome="fs (Poke Mart)", x0=-2.125, x1=3.633, z0=-1.812, porta=(0x0F, -0.558, 0.757, 0.0), dtile=(-0.5, 1.0)),
    0x28: dict(nome="pc (Centro Pokemon)", x0=-2.625, x1=3.0, z0=-2.0, porta=(0x0F, 0.0, 1.608, 0.0), dtile=(0, 1.5)),
    # area 7 (Olivine; lista de construcoes 6), para Breezeport
    0x6D: dict(nome="as_h01 (casa de Olivine)", x0=-2.14, x1=2.56, z0=-1.91, porta=(0x72, 0.197, 0.464, -0.09), dtile=(-0.5, 0.875)),
    0x66: dict(nome="tn_h01 (casa de Cianwood)", x0=-2.12, x1=2.5, z0=-1.62, porta=(0x67, 0.12, 0.719, 0.165), dtile=(-0.5, 1.0)),
    0x69: dict(nome="tn_photo (estudio de Cianwood)", x0=-2.0, x1=3.0, z0=-1.62, porta=(0x74, 0.12, 0.719, 0.165), dtile=(-0.5, 1.0)),
    0x6F: dict(nome="as_gym (ginasio de Olivine)", x0=-3.6, x1=3.76, z0=-2.5, porta=(0x10, 0.0, 1.312, 0.0), dtile=(0, 1.5)),
    0x6E: dict(nome="as_toudai (farol de Olivine)", x0=-3.53, x1=4.57, z0=-3.64, porta=None, dtile=(0, 0)),
    0x76: dict(nome="as_restaurant (restaurante de Olivine)", x0=-2.28, x1=2.52, z0=-2.03, porta=(0x78, 0.137, 0.316, 0.0), dtile=(-0.5, 1.0)),
    0x71: dict(nome="r39_naya (galpao da fazenda da Route 39)", x0=-1.83, x1=2.27, z0=-1.57, porta=None, dtile=(0, 0)),
    0x73: dict(nome="as_bench (banco com toldo do cais de Olivine)", x0=-2.0, x1=2.5, z0=-1.28, porta=None, dtile=(0, 0)),
    0x2D: dict(nome="hw_gym (ginasio de Azalea, de madeira)", x0=-3.6, x1=3.76, z0=-2.5,
               porta=(0x0F, 0.0, 1.312, 0.0), dtile=(0, 1.5)),
    # area 5 (Goldenrod; lista de construcoes 4), para Ferralia: caixa medida nos vertices do modelo; porta e tile do warp
    # medidos no Goldenrod do HGSS (objetos dos blocos 38-43 x warps da zona 073_T25)
    0x4C: dict(nome="ko_depart (loja de departamentos de Goldenrod)", x0=-2.6, x1=3.16, z0=-2.35,
               porta=(0x0F, 0.0, 2.0, 0.0), dtile=(0, 2.0)),
    0x4B: dict(nome="ko_cycle (bicicletaria)", x0=-2.38, x1=2.86, z0=-1.0, porta=(0x0F, 0.0, 1.349, 0.102), dtile=(0, 1.5)),
    0x4D: dict(nome="ko_flower (floricultura)", x0=-2.0, x1=2.5, z0=-1.78, porta=(0x0F, -0.503, 0.578, 0.032), dtile=(-0.5, 1.0)),
    0x4E: dict(nome="ko_funsui (fonte)", x0=-1.67, x1=1.67, z0=-1.67, porta=None, dtile=(0, 0)),
    0x4F: dict(nome="ko_game (cassino)", x0=-3.36, x1=3.81, z0=-2.0, porta=(0x0F, 0.0, 1.418, 0.095), dtile=(0, 1.5)),
    0x50: dict(nome="ko_gym (ginasio de Goldenrod)", x0=-3.6, x1=3.76, z0=-2.5, porta=(0x10, 0.0, 1.312, 0.0), dtile=(0, 1.5)),
    0x51: dict(nome="ko_h01 (casa de Goldenrod)", x0=-1.67, x1=2.08, z0=-1.35, porta=(0x5E, 0.176, 0.624, 0.0), dtile=(-0.5, 1.0)),
    0x57: dict(nome="ko_seimei (casa do avaliador de nomes)", x0=-2.33, x1=2.7, z0=-1.99, porta=None, dtile=(0, 1.0)),
    0x58: dict(nome="ko_station (estacao do Magnet Train)", x0=-3.67, x1=5.5, z0=-2.35,
               porta=(0x0F, -1.005, 2.313, 0.122), dtile=(-1.0, 2.69)),
    0x65: dict(nome="ko_h03x (predio de Goldenrod, sem entrada)", x0=-2.43, x1=2.89, z0=-1.94, porta=None, dtile=(0, 0)),
}
# Por mapa: retangulo da construcao no GBA (x0, y0, x1, y1, inclusivo, coordenadas do mapa do GBA), modelo, tile da porta
# no DS (= warp do GBA, salvo quando o modelo nao deixa) e se a porta e de verdade (warp) ou decorativa; "ajustes" sao
# tiles trocados para acompanhar a porta (letra, altura). A colisao e a uniao da planta do GBA com a do modelo.
CONSTRUCOES = {
    "Dawnmere": [
        dict(rect=(10, 4, 16, 8), modelo=0x13A, porta=(13, 8), warp=True, altura=2,
             nota="laboratorio do Prof. Alex: o unico laboratorio do HGSS que cabe na planta do GBA (colunas 10-16) tem a "
                  "porta no centro, 1 tile a oeste do warp do GBA (14,8); a escada vai junto (14,9 -> 13,9)",
             ajustes=[((13, 9), "=", "r"), ((14, 9), "=", "2"), ((15, 9), "S", "2")]),
        dict(rect=(19, 12, 23, 16), modelo=0x14, porta=(20, 16), warp=True, altura=1, nota="casa do warp MAYS_HOUSE"),
        dict(rect=(1, 7, 4, 9), modelo=0x16, porta=(2, 9), warp=True, altura=1, nota="casa do warp BRENDANS_HOUSE"),
        dict(rect=(6, 19, 10, 23), modelo=0x25, porta=(8, 23), warp=False, altura=1, nota="casa sem porta no GBA"),
        dict(rect=(18, 19, 22, 23), modelo=0x26, porta=(20, 23), warp=False, altura=1, nota="casa sem porta no GBA"),
    ],
    "Harvestvale": [
        dict(rect=(2, 17, 7, 21), modelo=0x2D, porta=(5, 21), warp=True, altura=1,
             nota="ginasio do Nevard (warp do GBA): o de Azalea; o de Celadon (Kanto) ficava sem textura na area 2"),
        dict(rect=(11, 18, 14, 21), modelo=0x28, porta=(12, 21), warp=True, altura=1, nota="Centro Pokemon"),
        dict(rect=(22, 29, 25, 31), modelo=0x27, porta=(23, 31), warp=True, altura=1, nota="Poke Mart"),
        dict(rect=(15, 9, 20, 11), modelo=0x14, porta=(17, 11), warp=True, altura=1, nota="casa (OLDALE_TOWN_HOUSE1)"),
        dict(rect=(20, 15, 23, 18), modelo=0x29, porta=(21, 18), warp=True, altura=1, nota="casa (OLDALE_TOWN_HOUSE2)"),
        # diretor, 25/11: "bancadas invisiveis a sudoeste da cidade": as barracas, o armazem e o celeiro do GBA tinham
        # so colisao; recebem modelos da area 7 que cabem na lista 0 (VRAM pequena)
        dict(rect=(3, 29, 4, 31), modelo=0x73, pos=(4.5, 30.6), porta=None, warp=False, altura=1, nota="barraca do mercado"),
        dict(rect=(7, 29, 8, 31), modelo=0x73, pos=(8.5, 30.6), porta=None, warp=False, altura=1, nota="barraca do mercado"),
        dict(rect=(12, 29, 14, 32), modelo=0x71, pos=(13.7, 31.0), porta=None, warp=False, altura=1, nota="armazem"),
        dict(rect=(30, 6, 32, 7), modelo=0x71, pos=(31.3, 7.8), porta=None, warp=False, altura=1, nota="celeiro"),
    ],
    "Route2": [
        dict(rect=(13, 33, 16, 36), modelo=0x25, porta=(14, 36), warp=False, altura=1,
             nota="casa de porta trancada (Palm280_DoorLocked na porta)"),
    ],
    "Brisa": [
        dict(rect=(13, 14, 16, 16), modelo=0x27, porta=(14, 16), warp=True, altura=1, nota="Poke Mart"),
        dict(rect=(22, 14, 25, 16), modelo=0x28, porta=(23, 16), warp=True, altura=1, nota="Centro Pokemon"),
        dict(rect=(3, 21, 6, 24), modelo=0x6D, porta=(4, 24), warp=True, altura=1, nota="casa (LILYCOVE_CITY_HOUSE1)"),
        dict(rect=(14, 21, 17, 24), modelo=0x6D, porta=(15, 24), warp=True, altura=1, nota="casa (LILYCOVE_CITY_HOUSE2)"),
        dict(rect=(3, 27, 6, 30), modelo=0x6D, porta=(4, 30), warp=True, altura=1, nota="casa (LILYCOVE_CITY_HOUSE3)"),
        dict(rect=(14, 27, 17, 30), modelo=0x6D, porta=(15, 30), warp=False, altura=1, nota="casa (LILYCOVE_CITY_HOUSE4)"),
        dict(rect=(63, 21, 66, 24), modelo=0x66, porta=(64, 24), warp=False, altura=1, nota="casa (DEWFORD_TOWN_HOUSE2)"),
        dict(rect=(63, 27, 66, 30), modelo=0x66, porta=(64, 30), warp=False, altura=1, nota="casa do esquecedor de golpes"),
        dict(rect=(44, 21, 50, 27), modelo=0x6F, porta=(47, 27), warp=True, altura=1,
             nota="teatro (PALM_TEATRO): o predio grande da area 7 com a porta no centro, como no GBA"),
        dict(rect=(52, 25, 57, 33), modelo=0x69, porta=(56, 33), warp=False, altura=1,
             nota="loja de departamentos (decorativa: decisao do diretor 24/11, nao existe no jogo); nenhum modelo da area 7 tem o tamanho dela"),
        dict(rect=(60, 39, 66, 43), modelo=0x76, porta=(63, 43), warp=False, altura=1, nota="casa de praia (sem warp no GBA)"),
        dict(rect=(61, 48, 68, 54), modelo=0x6E, pos=(64.5, 51.0), porta=None, warp=False, altura=1,
             nota="farol (decisao do diretor 24/11: o farol de Olivine; o GBA nao tem farol): na ponta de areia abaixo do "
                  "faroleiro (64,46) e da casa dele, decorativo, sem entrada"),
    ],
    # Ferralia (PalmFerralia), header de Goldenrod (T25, area 5): os modelos nativos da area; o warp do GBA vai para o
    # interior de Goldenrod que faz o mesmo papel (eventos_gba.py)
    "Ferralia": [
        dict(rect=(24, 4, 33, 12), modelo=0x58, porta=(28, 12), warp=True, altura=1, nota="estacao (PALM_STATION_FERRALIA)",
             ajustes=[((29, 12), "D", "1")]),
        dict(rect=(60, 4, 68, 8), modelo=0x4F, porta=(64, 8), warp=False, altura=1, nota="predio de porta trancada"),
        dict(rect=(3, 5, 9, 12), modelo=0x4C, porta=(5, 12), warp=True, altura=1, nota="predio alto (RUSTBORO_CITY_FLAT2_1F)"),
        dict(rect=(10, 8, 14, 11), modelo=0x51, porta=(12, 11), warp=True, altura=1, nota="casa (RUSTBORO_CITY_HOUSE1)"),
        dict(rect=(53, 5, 56, 11), modelo=0x65, pos=(55.0, 8.5), porta=None, warp=False, altura=1, nota="predio alto sem porta"),
        dict(rect=(18, 7, 22, 10), modelo=0x4D, porta=(20, 10), warp=False, altura=1, nota="casa de porta trancada"),
        dict(rect=(35, 8, 39, 11), modelo=0x51, porta=(37, 11), warp=True, altura=1, nota="casa (RUSTBORO_CITY_HOUSE2)"),
        dict(rect=(46, 8, 51, 12), modelo=0x50, porta=(49, 12), warp=True, altura=1, nota="ginasio (MAUVILLE_CITY_GYM)"),
        dict(rect=(43, 21, 49, 25), modelo=0x57, porta=(46, 25), warp=False, altura=1, nota="predio de porta trancada"),
        dict(rect=(19, 22, 22, 24), modelo=0x28, porta=(20, 24), warp=True, altura=1, nota="Centro Pokemon"),
        dict(rect=(35, 22, 38, 24), modelo=0x27, porta=(36, 24), warp=True, altura=1, nota="Poke Mart"),
        dict(rect=(51, 22, 56, 25), modelo=0x4B, porta=(53, 25), warp=False, altura=1, nota="predio de porta trancada"),
        dict(rect=(4, 23, 12, 27), modelo=0x4F, porta=(8, 27), warp=True, altura=1, nota="predio (RUSTBORO_CITY_FLAT1_1F)"),
        dict(rect=(27, 28, 29, 30), modelo=0x4E, pos=(28.5, 29.5), porta=None, warp=False, altura=1, nota="fonte da praca"),
        dict(rect=(43, 31, 46, 37), modelo=0x65, pos=(45.0, 34.5), porta=None, warp=False, altura=1, nota="predio alto sem porta"),
        dict(rect=(48, 31, 51, 37), modelo=0x65, pos=(50.0, 34.5), porta=None, warp=False, altura=1, nota="predio alto sem porta"),
        dict(rect=(53, 31, 56, 37), modelo=0x65, pos=(55.0, 34.5), porta=None, warp=False, altura=1, nota="predio alto sem porta"),
        dict(rect=(4, 33, 8, 36), modelo=0x51, porta=(6, 36), warp=False, altura=1, nota="casa de porta trancada"),
        dict(rect=(10, 33, 14, 36), modelo=0x51, porta=(12, 36), warp=False, altura=1, nota="casa de porta trancada"),
        dict(rect=(19, 43, 25, 47), modelo=0x4B, porta=(22, 47), warp=False, altura=1, nota="predio de porta trancada"),
        dict(rect=(4, 44, 9, 47), modelo=0x4D, porta=(6, 47), warp=False, altura=1, nota="casa de porta trancada"),
        dict(rect=(30, 44, 34, 47), modelo=0x51, porta=(32, 47), warp=False, altura=1, nota="casa de porta trancada"),
        dict(rect=(46, 44, 50, 47), modelo=0x51, porta=(48, 47), warp=True, altura=1, nota="casa (RUSTBORO_CITY_HOUSE3)"),
        dict(rect=(52, 44, 56, 47), modelo=0x4D, porta=(54, 47), warp=False, altura=1, nota="casa de porta trancada"),
        dict(rect=(61, 44, 66, 47), modelo=0x57, porta=(63, 47), warp=False, altura=1, nota="predio de porta trancada"),
    ],
    "Route3": [
        dict(rect=(18, 58, 21, 61), modelo=0x6D, porta=(19, 61), warp=False, altura=1,
             nota="casa da praia de porta trancada (Palm280_DoorLocked na porta), a mesma casa azul de Breezeport"),
    ],
    "Route1": [
        dict(rect=(4, 17, 10, 20), modelo=0x14, porta=(5, 20), warp=False, altura=1,
             nota="casa da horta (porta decorativa no GBA, sem warp); a casa de Pallet (mst_rdh), de telhado vermelho, "
                  "ficou sem textura: a lista de construcoes da area so tem VRAM para mais dois modelos"),
    ],
}
# lista de construcoes 0 (area 2: os headers de Dawnmere, Route 1 e Harvestvale), pelo land.json: entram o laboratorio
# de Pallet, o ginasio de Celadon e as portas deles; sai o wk_labo de New Bark (sem uso com Dawnmere original). A VRAM
# das texturas da lista tem limite: 53 248 bytes funcionaram, ~55 600 nao (o ultimo modelo ficou sem textura).
# As portas dos modelos de fora (0x137 de Pallet, 0x10 de ginasio) ficavam sem textura na area 2: os dois usam a
# porta p_door (0x0F), nativa da area (a do Centro e do Mart), da mesma largura.
MODELOS_NOVOS_NA_AREA = [0x13A, 0x2D, 0x71, 0x73]

# Redesenhos pedidos pelo diretor sobre a conversao fiel (retangulo no mapa do GBA, regra)
REDESENHO = {
    # 25/11: "Remocao desse lago no final da rota 1... substituir por outro layout, com flores, matinhos": a lagoa do
    # sudoeste e os canais da saida sul viram campo; a agua que encosta em terra vira flor, o miolo vira mato alto
    "Route1": [((0, 38, 23, 52), "lago_para_campo")],
}


def redesenhar(key, tiles, w, h):
    for (x0, y0, x1, y1), regra in REDESENHO.get(key, []):
        if regra == "lago_para_campo":
            agua = {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if tiles[y * w + x] == "~"}
            for x, y in agua:
                borda = any((x + dx, y + dy) not in agua for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                            if 0 <= x + dx < w and 0 <= y + dy < h)
                tiles[y * w + x] = "f" if borda else "e"
MODELOS_FORA_DA_AREA = [0x15]


def construcoes(key, gx, gy, grid, alt):
    """Carimba as construcoes do mapa no desenho global; devolve as linhas de [objetos] e o relatorio."""
    objs, rel = [], []
    for c in CONSTRUCOES.get(key, []):
        M = MODELOS[c["modelo"]]
        if c.get("pos"):                                 # ponto do objeto dado direto (construcao sem porta)
            ox, oz = c["pos"]
            px, pz = None, None
        else:
            px, pz = c["porta"]
            ox = px + 0.5 - M["dtile"][0]                # ponto do objeto (coordenadas de borda de tile, mapa do GBA)
            oz = pz + 0.5 - M["dtile"][1]
        x0, y0, x1, y1 = c["rect"]
        cells = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
        if pz is not None:
            cells |= {(x, y) for x in range(int(ox + M["x0"]) - 1, int(ox + M["x1"]) + 2)
                      for y in range(int(oz + M["z0"]) - 1, pz + 1)
                      if ox + M["x0"] + 0.25 <= x + 0.5 <= ox + M["x1"] - 0.25 and y + 0.5 >= oz + M["z0"] - 0.25}
        h = str(c["altura"])
        for x, y in cells:
            grid[gy + y][gx + x] = "B"; alt[gy + y][gx + x] = h
        if pz is not None:
            grid[gy + pz][gx + px] = "D" if c["warp"] else "B"
        for (x, y), ch, a in c.get("ajustes", []):
            grid[gy + y][gx + x] = ch; alt[gy + y][gx + x] = a
        X, Z = gx + ox - 0.5, gy + oz - 0.5             # [objetos] usa indice de tile (o Land.obj soma 0,5)
        objs.append(f"{c['modelo']} {X:g} {Z:g} 0")
        if M["porta"]:
            dm, ddx, ddz, ddy = M["porta"]
            objs.append(f"{dm} {X + ddx:g} {Z + ddz:g} {ddy:g}")
        rel.append({"modelo": M["nome"], "porta_ds": (gx + px, gy + pz) if pz is not None else None, "warp": c["warp"],
                    "nota": c["nota"]})
    return objs, rel


MAPS = {"Dawnmere": ("LittlerootTown", 0, 0), "Route1": ("Route101", 34, 17), "Harvestvale": ("OldaleTown", 35, 70),
        "Route2": ("PalmRoute02", 35, 107),        # ligacoes do GBA: Route 2 abaixo de Harvestvale (deslocamento 0)
        "Brisa": ("PalmBrisa", 35, 155),           # e Breezeport abaixo da Route 2 (deslocamento 0)
        "Route3": ("PalmRoute03", -21, 135),       # Route 3 a oeste de Breezeport (ligacao "left", deslocamento -20)
        "Ferralia": ("PalmFerralia", -37, 71)}     # Ferralia acima da Route 3 (ligacao "up", deslocamento -16)
# Bases de lampiao do GBA (auditoria de 25/11): viravam tile bloqueado sem modelo (um quadrado de grama no meio da
# calcada e uma parede invisivel). Recebem o poste de Olivine (as_light, 0xF8, acrescentado a lista 6 no land.json).
LAMPIOES = {"gTileset_Lilycove": {0x361, 0x364},          # 0x362 e topo de lampiao (andavel)
            "gTileset_Rustboro": {0x21A}}                  # Ferralia: base do poste (o topo 0x212 e andavel)
# Metatiles de tileset secundario com letra propria (a tabela GENERAL acima so vale para EverGrande/Petalburg):
# a cerca de ferro e os trilhos de madeira de Ferralia viravam construcao ('B', parede invisivel sem modelo)
SECUNDARIOS = {"gTileset_Rustboro": {0x2A7: "c", 0x2BE: "c", 0x319: "c", 0x352: "c", 0x35E: "c", 0x35F: "c"}}
MODELO_LAMPIAO = {"gTileset_Lilycove": 0xF8,                  # as_light, o poste de Olivine
                  "gTileset_Rustboro": 0x5F}                  # ko_light, o poste de Goldenrod (Ferralia)
ESCADAS = {0x0AF}                           # escada do GBA: rampa no DS (entre os vizinhos norte e sul)
# Deslocamento do desenho dentro da area de blocos. Cada celula de 32x32 tem UM header (zona de eventos, encontros,
# musica): com (30, 21), quase toda celula fica com um mapa so: Dawnmere na coluna de blocos 1, a Route 1 nas colunas
# 2-3 (linhas 1-2), Harvestvale na linha 3, a Route 2 nas linhas 4-5. Sobram as 5 primeiras linhas de Harvestvale
# (arvores e caminho) numa celula da Route 1: a chegada e o fazendeiro descem 3 linhas (eventos_gba.py).
# 25/11: +32 em x (uma celula inteira, a particao das celulas entre os mapas nao muda): Ferralia fica a oeste da
# Route 3 (ligacao "up" com deslocamento -16) e passava da borda esquerda do desenho.
MARGIN = (62, 21)


def behaviors(tileset_name):
    """Comportamento (byte baixo do atributo) de cada metatile do tileset."""
    import render_map as rm
    raw = open(rm.TILESETS[tileset_name]["attrs"], "rb").read()
    return [struct.unpack_from("<H", raw, 2 * i)[0] & 0xFF for i in range(len(raw) // 2)]


def mb_values():
    names = re.findall(r"^\s*(MB_\w+)", open(os.path.join(REPO, "include/constants/metatile_behaviors.h")).read(), re.M)
    return {n: i for i, n in enumerate(names)}


def load_map(name):
    import render_map as rm
    j = json.load(open(os.path.join(REPO, f"data/maps/{name}/map.json")))
    L = rm._maps()[j["layout"]]
    w, h = L["width"], L["height"]
    data = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
    vals = [struct.unpack_from("<H", data, 2 * i)[0] for i in range(w * h)]
    return j, L, w, h, vals


def convert(name):
    j, L, w, h, vals = load_map(name)
    mb = mb_values()
    prim, sec = behaviors(L["primary_tileset"]), behaviors(L["secondary_tileset"])
    tall = {mb[k] for k in mb if "TALL_GRASS" in k or "LONG_GRASS" in k}
    jump_s = mb["MB_JUMP_SOUTH"]
    shallow = {mb[k] for k in mb if k in ("MB_SHALLOW_WATER",)}
    water = {mb[k] for k in mb if any(t in k for t in ("POND_WATER", "DEEP_WATER", "OCEAN_WATER", "SEMI_DEEP", "INTERIOR_DEEP", "PUDDLE"))}
    tiles, elev, unknown = [], [], collections.Counter()
    for i, v in enumerate(vals):
        mt, col, el = v & 0x3FF, (v >> 10) & 3, v >> 12
        b = prim[mt] if mt < 0x200 else sec[mt - 0x200]
        if b in tall:
            c = "e"
        elif b == jump_s:
            c = "v"                                      # ressalto: pulo para o sul
        elif b in shallow:
            c = "="                                      # poca rasa (andavel): chao de terra no DS
        elif b in water:
            c = "~"
        elif mt in SECUNDARIOS.get(L["secondary_tileset"], {}) and col:
            c = SECUNDARIOS[L["secondary_tileset"]][mt]
        elif mt in GENERAL and (mt < 0x200 or L["secondary_tileset"] in SECONDARY_TABLE_TILESETS):
            c = GENERAL[mt]
        elif any(mt in r for r in PRIMARY_BUILDINGS):
            c = "B" if col else "="                      # parede/telhado de construcao; calcada na frente
        elif mt in SECONDARY_BUILDINGS and col:
            c = "B"
        elif mt in SECONDARY_BUILDINGS:
            c = "="                                      # chao de construcao andavel (calcada, degrau)
        else:
            c = "#" if col else "."
            unknown[mt] += 1
        if mt in LAMPIOES.get(L["secondary_tileset"], ()):
            c = "S"                                      # base do lampiao: modelo as_light (build_global)
        elif c in "#c" and not col:
            c = "="                                      # fidelidade: sem colisao no GBA, o tile e andavel no DS
        tiles.append(c); elev.append(el)
    return j, w, h, tiles, elev, unknown


def rocha_no_alto(tiles, H, w, h):
    """Rocha do penhasco ('#'): no GBA a faixa de pedra e a face e a beirada do patamar; no DS ela fica na altura do
    lado de CIMA (o mais alto dos vizinhos que nao sao rocha, a 1 tile; depois a 2), e a face do penhasco sai na borda
    de fora da faixa, continua. Antes cada tile de pedra herdava a altura da maioria dos vizinhos e as faces saiam em
    pedacos soltos (montanha de Breezeport, cercado da Route 2; auditoria de 25/11)."""
    rock = [t == "#" for t in tiles]
    novo = list(H)
    for i in range(w * h):
        if not rock[i]:
            continue
        x, y = i % w, i // w
        for r in (1, 2):
            nb = [H[(y + dy) * w + x + dx] for dx in range(-r, r + 1) for dy in range(-r, r + 1)
                  if 0 <= x + dx < w and 0 <= y + dy < h and not rock[(y + dy) * w + x + dx] and H[(y + dy) * w + x + dx] != "r"]
            if nb:
                novo[i] = max(int(v) for v in nb)
                break
    return novo


def terracos(tiles, hh, w, h):
    """Patamares de mapas que o GBA desenha planos (mesma elevacao dos dois lados), com paredoes de pedra e escadas so
    no desenho (Route 3): cada escada sobe um nivel para o norte. Grupos ligados de tiles andaveis (sem pedra, arvore,
    agua e escada) viram patamares; o grupo ao sul de uma escada fica um nivel abaixo do grupo ao norte; o grupo que
    toca a borda sul (praia) e o nivel 1. Arvores pegam o nivel do patamar mais perto; a pedra vai para o lado de cima.
    Sem isso os paredoes saiam como faixas de grama bloqueada, sem face de penhasco."""
    import collections
    livre = lambda i: tiles[i] not in "#T~RBSD" and hh[i] != "r"
    comp = [-1] * (w * h)
    n = 0
    for i in range(w * h):
        if comp[i] >= 0 or not livre(i):
            continue
        fila = [i]; comp[i] = n
        while fila:
            k = fila.pop(); x, y = k % w, k // w
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= x + dx < w and 0 <= y + dy < h:
                    j = (y + dy) * w + x + dx
                    if comp[j] < 0 and livre(j):
                        comp[j] = n; fila.append(j)
        n += 1
    sobe = collections.defaultdict(set)                  # grupo ao sul -> grupos ao norte (por escada)
    for x in range(w):
        y = 0
        while y < h:
            if hh[y * w + x] == "r":
                y0 = y
                while y < h and hh[y * w + x] == "r":
                    y += 1
                if y0 > 0 and y < h and comp[(y0 - 1) * w + x] >= 0 and comp[y * w + x] >= 0:
                    sobe[comp[y * w + x]].add(comp[(y0 - 1) * w + x])
            else:
                y += 1
    base = next((comp[i] for i in range(w * h - 1, -1, -1) if comp[i] >= 0 and tiles[i] != "~"), None)
    nivel = {base: 1} if base is not None else {}
    fila = collections.deque([base] if base is not None else [])
    while fila:
        c = fila.popleft()
        for d in sobe[c]:
            if d not in nivel:
                nivel[d] = nivel[c] + 1; fila.append(d)
    for c in range(n):                                   # escada vista do outro lado: desce
        for d in sobe[c]:
            if d in nivel and c not in nivel:
                nivel[c] = nivel[d] - 1
    # bolsoes sem escada (separados do patamar por arvores): o nivel do patamar alcancado mais perto, andando por
    # arvores e grama, sem atravessar pedra
    dist = {}
    fila = collections.deque()
    for i in range(w * h):
        if comp[i] in nivel:
            dist[i] = nivel[comp[i]]; fila.append(i)
    while fila:
        k = fila.popleft(); x, y = k % w, k // w
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= x + dx < w and 0 <= y + dy < h:
                j = (y + dy) * w + x + dx
                if j not in dist and tiles[j] not in "#~" and hh[j] != "r":
                    dist[j] = dist[k]; fila.append(j)
                    if comp[j] >= 0 and comp[j] not in nivel:
                        nivel[comp[j]] = dist[k]
    H = [hh[i] if hh[i] == "r" else (nivel.get(comp[i], 1) if comp[i] >= 0 else None) for i in range(w * h)]
    for y in range(h):                                   # os patamares correm de leste a oeste: arvore pega o nivel do
        fontes = [x for x in range(w) if comp[y * w + x] >= 0]   # tile andavel mais perto NA MESMA LINHA
        if not fontes:
            continue
        for x in range(w):
            i = y * w + x
            if H[i] is None and tiles[i] != "#":
                H[i] = H[y * w + min(fontes, key=lambda f: abs(f - x))]
    fila = collections.deque(i for i in range(w * h) if H[i] is not None and H[i] != "r")
    while fila:                                          # arvores, agua e construcoes: o nivel mais perto
        k = fila.popleft(); x, y = k % w, k // w
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= x + dx < w and 0 <= y + dy < h:
                j = (y + dy) * w + x + dx
                if H[j] is None and tiles[j] != "#":
                    H[j] = H[k]; fila.append(j)
    H = [1 if v is None else v for v in H]               # pedra: provisorio, a regra da rocha decide
    for _ in range(3):                                   # grupo de arvores afundado entre tiles mais altos sobe (poco)
        visto = set()
        for i in range(w * h):
            if tiles[i] != "T" or H[i] == "r" or i in visto:
                continue
            grupo, pilha, borda = [], [i], []
            visto.add(i)
            while pilha:
                k = pilha.pop(); grupo.append(k); x, y = k % w, k // w
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if not (0 <= x + dx < w and 0 <= y + dy < h):
                        continue
                    j = (y + dy) * w + x + dx
                    if tiles[j] == "#" or H[j] == "r":
                        continue
                    if tiles[j] == "T" and H[j] == H[i]:
                        if j not in visto:
                            visto.add(j); pilha.append(j)
                    else:
                        borda.append(H[j])
            if borda and min(borda) > H[i]:
                for k in grupo:
                    H[k] = min(borda)
    H = rocha_no_alto(tiles, H, w, h)
    for i in range(w * h):
        if hh[i] != "r":
            hh[i] = H[i]


TERRACOS = {"Route3"}
# Altura somada ao mapa inteiro, para casar com o vizinho na divisa: Ferralia fica no plato da Route 3 (a placa do GBA:
# "up the SERRA trail to the plateau and FERRALIA"), no nivel 4 do alto da Route 3; no nivel 1 a divisa virava um degrau
# de 3 tiles que o jogador nao descia (teste dirigido de 25/11)
ALTURA_BASE = {"Ferralia": 3}


def heights(w, h, elev, tiles=None):
    H = [{4: 2, 5: 2, 6: 3, 7: 3}.get(e, 1) for e in elev]  # 3 = chao (1); 4-5 = elevado (2); 6-7 = cume (3)
    for _ in range(2):                                   # tiles de elevacao 0 (bloqueados) herdam dos vizinhos
        for i, e in enumerate(elev):
            if e == 0:
                x, y = i % w, i // w
                nb = [H[(y + dy) * w + x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if 0 <= x + dx < w and 0 <= y + dy < h and elev[(y + dy) * w + x + dx] != 0]
                if nb:
                    H[i] = max(set(nb), key=nb.count)
    if tiles:
        # "poco": grupo de tiles de grama/flor/arvore/mato numa altura so, cercado (fora rocha, cerca e construcao)
        # so por tiles mais altos, sobe para a menor altura em volta. Os elevados do GBA tem arvores e flores com
        # elevacao 3 no meio do patamar 4 (lagoa cercada de Dawnmere): no DS saia uma face de penhasco solta em volta
        # de cada arvore (auditoria de 25/11)
        soft = set(".fghTe")
        borda = set("#cSBD")
        for _ in range(4):
            vistos, mudou = set(), False
            for i in range(w * h):
                if i in vistos or tiles[i] not in soft:
                    continue
                comp, pilha, alto, fora = [], [i], [], False
                vistos.add(i)
                while pilha:
                    k = pilha.pop(); comp.append(k)
                    x, y = k % w, k // w
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = x + dx, y + dy
                        if not (0 <= xx < w and 0 <= yy < h):
                            fora = True; continue
                        j = yy * w + xx
                        if tiles[j] in borda:
                            continue
                        if tiles[j] in soft and H[j] == H[i]:
                            if j not in vistos:
                                vistos.add(j); pilha.append(j)
                        else:
                            alto.append(H[j])
                if not fora and alto and min(alto) > H[i] and len(comp) <= 12:
                    for k in comp:
                        H[k] = min(alto)
                    mudou = True
            if not mudou:
                break
        H = rocha_no_alto(tiles, H, w, h)
        # arvores logo ao norte de um patamar mais alto (atras dele, para a camera) sobem para a altura do patamar,
        # ate 3 tiles para o norte: embaixo, a beirada do patamar cortava o pe das arvores numa linha reta (anel da
        # montanha de Breezeport; auditoria de 25/11)
        for i in range(w * h):
            x, y = i % w, i // w
            if tiles[i] == "T" and y + 1 < h and tiles[i + w] != "T" and H[i + w] > H[i] and tiles[i + w] != "~":
                for k in range(3):
                    j = i - k * w
                    if j < 0 or tiles[j] != "T" or H[j] >= H[i + w]:
                        break
                    H[j] = H[i + w]
    return H


def rochas_soltas(tiles, hh, w, h):
    """Pedra solta do GBA (rocha bloqueada no meio da areia ou do mar, ate 12 tiles): vira 'R', um bloco de rocha 1
    tile acima do chao em volta. Como '#', ela tinha chao de grama e saia como ilhas de grama no mar e quadrados
    verdes na praia de Breezeport (auditoria de 25/11)."""
    vistos = set()
    for i in range(w * h):
        if tiles[i] != "#" or i in vistos:
            continue
        comp, pilha, viz = [], [i], []
        vistos.add(i)
        while pilha:
            k = pilha.pop(); comp.append(k)
            x, y = k % w, k // w
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if not (0 <= x + dx < w and 0 <= y + dy < h):
                    continue
                j = (y + dy) * w + x + dx
                if tiles[j] == "#":
                    if j not in vistos:
                        vistos.add(j); pilha.append(j)
                else:
                    viz.append(j)
        if len(comp) <= 12 and viz and all(tiles[j] in "~=" for j in viz):
            base = max(int(hh[j]) for j in viz if hh[j] != "r")
            for k in comp:
                tiles[k], hh[k] = "R", base + 1


def build_global():
    W, H = 192, 256                                   # 6x8 celulas (Ferralia na coluna 0)
    grid = [["T"] * W for _ in range(H)]
    alt = [["1"] * W for _ in range(H)]
    owner = [[None] * W for _ in range(H)]
    report, objetos = {}, []
    for key, (name, ox, oy) in MAPS.items():
        j, w, h, tiles, elev, unknown = convert(name)
        redesenhar(key, tiles, w, h)
        hh = heights(w, h, elev, tiles)
        _, _, _, _, vals = load_map(name)
        for i, v in enumerate(vals):                     # escadas: rampa (so as que nao foram ajustadas a mao)
            if v & 0x3FF in ESCADAS and key != "Dawnmere":
                hh[i] = "r"
        if key in TERRACOS:
            terracos(tiles, hh, w, h)
        rochas_soltas(tiles, hh, w, h)
        if ALTURA_BASE.get(key):
            hh[:] = [v if v == "r" else int(v) + ALTURA_BASE[key] for v in hh]
        for i, v in enumerate(vals):
            # passagem de elevacao 0 andavel entre alturas diferentes (norte x sul): rampa. Era a entrada da lagoa
            # cercada de Dawnmere, que virava um degrau sem subida depois que o patamar ficou inteiro (25/11)
            x, y = i % w, i // w
            if v >> 12 == 0 and not (v >> 10) & 3 and tiles[i] in "=." and 0 < y < h - 1 and hh[i] != "r":
                n_, s_ = hh[i - w], hh[i + w]
                if "r" not in (n_, s_) and n_ != s_:
                    hh[i] = "r"
        gx, gy = ox + MARGIN[0], oy + MARGIN[1]
        for y in range(h):
            for x in range(w):
                grid[gy + y][gx + x] = tiles[y * w + x]
                alt[gy + y][gx + x] = str(hh[y * w + x])
                owner[gy + y][gx + x] = key
        objs, rel = construcoes(key, gx, gy, grid, alt)
        objetos += objs
        sec = load_map(name)[1]["secondary_tileset"]
        lamps = LAMPIOES.get(sec, ())
        for i, v in enumerate(vals):
            if v & 0x3FF in lamps:
                objetos.append(f"{MODELO_LAMPIAO[sec]} {gx + i % w} {gy + i // w} 0")
        for b in j.get("bg_events", []):                 # placas do GBA: modelo de placa do HGSS (board_b) no tile
            if b.get("type") == "sign" and not re.search(r"Lamp|Keeper|DoorLocked", b.get("script", "")):
                # placa de verdade (board_b, nas listas 0 e 6); lampioes e portas ficam sem modelo
                objetos.append(f"30 {gx + b['x']} {gy + b['y']} 0")
        report[key] = {"gba": name, "origem": (gx, gy), "tam": (w, h), "desconhecidos": dict(unknown),
                       "warps": [(wv["x"] + gx, wv["y"] + gy, wv["dest_map"]) for wv in j.get("warp_events", [])],
                       "construcoes": rel}
    # divisa entre mapas: tile de grama na primeira ou ultima coluna/linha de um mapa, entre caminho dos dois lados
    # (atravessando a divisa), vira caminho. No GBA a Route 101 comeca com uma coluna de grama e o caminho de
    # Dawnmere parava nela: no DS ficava um corte de grama no meio da saida leste (auditoria de 25/11).
    for key, r in report.items():
        gx, gy = r["origem"]; w, h = r["tam"]
        bordas = [(gx, y) for y in range(gy, gy + h)] + [(gx + w - 1, y) for y in range(gy, gy + h)] + \
                 [(x, gy) for x in range(gx, gx + w)] + [(x, gy + h - 1) for x in range(gx, gx + w)]
        for x, y in bordas:
            if grid[y][x] != ".":
                continue
            for dx, dy in ((1, 0), (0, 1)):
                a_, b_ = (x - dx, y - dy), (x + dx, y + dy)
                if all(0 <= p[0] < W and 0 <= p[1] < H for p in (a_, b_)) and grid[a_[1]][a_[0]] == "=" and \
                        grid[b_[1]][b_[0]] == "=" and owner[a_[1]][a_[0]] != owner[b_[1]][b_[0]]:
                    grid[y][x] = "="
    # mar alem dos mapas: tile sem mapa ao lado (ou abaixo) de agua do GBA continua agua, para o mar nao acabar numa
    # floresta (a borda externa do desenho recebe colisao no mapa_global, "barreira")
    for key, (name, ox, oy) in MAPS.items():
        gx, gy = ox + MARGIN[0], oy + MARGIN[1]
        w, h = report[key]["tam"]
        for y in range(gy, H):
            for x in range(W):
                if owner[y][x] is not None:
                    continue
                if not (y >= gy + h or (gy <= y < gy + h and (x < gx or x >= gx + w))):
                    continue
                sx, sy = min(max(x, gx), gx + w - 1), min(max(y, gy), gy + h - 1)
                if owner[sy][sx] == key and grid[sy][sx] == "~" and (y >= gy + h or abs(x - sx) <= 32):
                    grid[y][x], alt[y][x] = "~", alt[sy][sx]
    return grid, alt, owner, report, objetos


def folha(name, out):
    import render_map as rm
    from PIL import Image, ImageDraw
    j, L, w, h, vals = load_map(name)
    ts = rm.TilesetPair(L["primary_tileset"], L["secondary_tileset"])
    ids = sorted({v & 0x3FF for v in vals})
    cols, cell = 12, 40
    im = Image.new("RGB", (cols * cell, ((len(ids) + cols - 1) // cols) * (cell + 10)), (40, 40, 40)); d = ImageDraw.Draw(im)
    for k, mt in enumerate(ids):
        x, y = (k % cols) * cell, (k // cols) * (cell + 10)
        im.paste(ts.metatile(mt).resize((32, 32), Image.NEAREST), (x + 4, y + 2))
        d.text((x + 2, y + 34), f"{mt:03x}", fill=(255, 255, 0))
    im.save(out)


if __name__ == "__main__":
    if sys.argv[1] == "--folha":
        folha(sys.argv[2], sys.argv[3]); sys.exit()
    grid, alt, owner, report, objetos = build_global()
    for k, r in report.items():
        print(k, r["gba"], "origem", r["origem"], "tam", r["tam"], "metatiles sem tabela:", r["desconhecidos"])
    out = ["; desenho global de Dawnmere + Route 1 + Harvestvale, convertido do GBA por gba2grade.py (nao editar a mao)",
           "[doadores]", "2 0 5 4", "[tamanho]", f"{len(grid[0])} {len(grid)}", "[tiles]"] + ["".join(r) for r in grid] + ["[alturas]"] + ["".join(r) for r in alt] + ["[objetos]"] + objetos
    open(sys.argv[1], "w").write("\n".join(out) + "\n")
    json.dump(report, open(sys.argv[1] + ".json", "w"), indent=1)
