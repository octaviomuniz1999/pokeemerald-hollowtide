#!/usr/bin/env python3
"""Ginasio da Jade ("Jardim dos Espelhos") — mapa novo MAP_PALM_JADE_GYM, 9x48, salas do ginasio de Petalburg.

De baixo para cima: entrada (os tres espelhos mostram a sequencia LUA, ESTRELA, SOL), sala A, sala B, sala C
e a sala da lider. Cada sala de puzzle tem duas portas com simbolos gravados; a porta certa leva a sala
seguinte, a errada devolve a entrada. Jade: Chimecho 34, Gardevoir 36, Espeon (Lau) 38 -> Insignia da
Serenidade (FLAG_BADGE05_GET) + TM Psychic. A porta do ginasio em Serenia abre depois do altar.
Rodar depois de install_cap6.py.
"""
import collections, json, os, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import serenia as SE
from canvas import ROOT
from install_cap4 import jload, jsave, obj, sign, map_json, register

OD = collections.OrderedDict
W = 9
# (linha inicial no mapa novo, linha inicial no ginasio de Petalburg): salas de 8 linhas + 2 de vazio
ROOMS = {"leader": (0, 0), "C": (10, 52), "B": (20, 78), "A": (30, 91), "entrance": (40, 104)}
H = 48
SEQUENCE = ["MOON", "STAR", "SUN"]
DOORS = {"A": ("MOON", "SUN"), "B": ("SUN", "STAR"), "C": ("SUN", "MOON")}   # (porta esquerda, porta direita)
DOOR_OPEN_TOP = 0x21C   # METATILE_PetalburgGym_SlidingDoor_Frame4 (embaixo: +8 = porta, MB_PETALBURG_GYM_DOOR)
NEXT = {"A": "B", "B": "C", "C": "leader"}


class Layout:
    def __init__(self):
        L = {l["id"]: l for l in jload(f"{ROOT}/data/layouts/layouts.json")["layouts"] if "id" in l}
        e = L["LAYOUT_PETALBURG_CITY_GYM"]
        self.src = struct.unpack(f"<{e['width'] * e['height']}H", open(f"{ROOT}/{e['blockdata_filepath']}", "rb").read())
        self.w, self.h = W, H
        self.primary, self.secondary = e["primary_tileset"], e["secondary_tileset"]
        void = self.src[9 * W]
        self.bl = [void] * (W * H)
        for _, (dst, srcy) in ROOMS.items():
            for dy in range(8):
                for x in range(W):
                    self.bl[(dst + dy) * W + x] = self.src[(srcy + dy) * W + x]

        # portas abertas (ultimo quadro da porta deslizante de Petalburg): no topo de cada sala com portas
        for name in ("entrance", "A", "B", "C"):
            y0 = ROOMS[name][0]
            for x in (1, 7):
                self.bl[y0 * W + x] = DOOR_OPEN_TOP | (1 << 10)
                self.bl[(y0 + 1) * W + x] = (DOOR_OPEN_TOP + 8) | (1 << 10)
        # piso de chegada (fundo de cada sala): seta para baixo, volta a entrada (MB_SOUTH_ARROW_WARP)
        for name in ("A", "B", "C", "leader"):
            y0 = ROOMS[name][0]
            self.bl[(y0 + 7) * W + 1] = 0x210 | (3 << 12)
            self.bl[(y0 + 7) * W + 2] = 0x211 | (3 << 12)

    def build(self):
        return self.bl


def main():
    lay = Layout()
    bl = lay.build()
    register("PalmJadeGym", "LAYOUT_PALM_JADE_GYM", lay, bl)
    # borda: o vazio do ginasio (a borda padrao de arvores nao existe nestes tilesets)
    open(f"{ROOT}/data/layouts/PalmJadeGym/border.bin", "wb").write(struct.pack("<4H", *[lay.src[9 * W]] * 4))
    j = map_json("MAP_PALM_JADE_GYM", "PalmJadeGym", "LAYOUT_PALM_JADE_GYM", "MUS_GYM", "MAPSEC_FALLARBOR_TOWN", "MAP_TYPE_INDOOR", None)
    j.update({"weather": "WEATHER_NONE", "allow_cycling": False, "allow_running": False, "show_map_name": False,
              "battle_scene": "MAP_BATTLE_SCENE_GYM"})
    warps = []
    def warp(x, y, dest_map, dest_id):
        warps.append(OD([("x", x), ("y", y), ("elevation", 0), ("dest_map", dest_map), ("dest_warp_id", str(dest_id))]))
        return len(warps) - 1
    e0 = ROOMS["entrance"][0]
    w_exit_l = warp(4, e0 + 7, "MAP_PALM_SERENIA", 5)        # saida para Serenia (porta do ginasio = warp 5 da vila)
    warp(5, e0 + 7, "MAP_PALM_SERENIA", 5)
    # chegadas (piso de baixo de cada sala) — indices preenchidos depois
    arrive = {}
    for name in ("A", "B", "C", "leader"):
        y0 = ROOMS[name][0]
        arrive[name] = warp(1, y0 + 7, "MAP_PALM_JADE_GYM", 0)      # destino: entrada (volta)
        warp(2, y0 + 7, "MAP_PALM_JADE_GYM", 0)
    # portas (para onde a porta da sala leva quem volta pelo piso de baixo / erra): warps de chegada nas portas
    entrance_doors = (warp(1, e0 + 1, "MAP_PALM_JADE_GYM", arrive["A"]), warp(7, e0 + 1, "MAP_PALM_JADE_GYM", arrive["A"]))
    for name in ("A", "B", "C"):
        y0 = ROOMS[name][0]
        warp(1, y0 + 1, "MAP_PALM_JADE_GYM", entrance_doors[0]); warp(7, y0 + 1, "MAP_PALM_JADE_GYM", entrance_doors[0])
    # voltar pelo piso de baixo leva a entrada (porta esquerda)
    for name in ("A", "B", "C", "leader"):
        warps[arrive[name]]["dest_warp_id"] = str(entrance_doors[0])
        warps[arrive[name] + 1]["dest_warp_id"] = str(entrance_doors[0])
    # destino de cada porta (como em Petalburg: a porta e um sinal que pergunta e usa warpdoor)
    dest = {}
    dest[("entrance", "L")] = dest[("entrance", "R")] = (1, ROOMS["A"][0] + 7)
    for name in ("A", "B", "C"):
        right_symbol = SEQUENCE["ABC".index(name)]
        for side, si in (("L", 0), ("R", 1)):
            dest[(name, side)] = (1, ROOMS[NEXT[name]][0] + 7) if DOORS[name][si] == right_symbol else (1, e0 + 1)
    j["warp_events"] = warps
    # objetos: Jade, treinadores, guia
    yl, ya, yb, yc = ROOMS["leader"][0], ROOMS["A"][0], ROOMS["B"][0], ROOMS["C"][0]
    j["object_events"] = [
        obj("LIZA", 4, yl + 2, "MOVEMENT_TYPE_FACE_DOWN", "Palm150_Jade"),
        obj("OBJ_EVENT_GFX_SPECIES(ESPEON)", 5, yl + 2, "MOVEMENT_TYPE_FACE_DOWN", "Palm150_Lau"),
        obj("PSYCHIC_M", 4, ya + 4, "MOVEMENT_TYPE_FACE_DOWN", "Palm150_TrainerA", "TRAINER_TYPE_NORMAL", 2),
        obj("HEX_MANIAC", 4, yb + 4, "MOVEMENT_TYPE_FACE_DOWN", "Palm150_TrainerB", "TRAINER_TYPE_NORMAL", 2),
        obj("PSYCHIC_M", 4, yc + 4, "MOVEMENT_TYPE_FACE_DOWN", "Palm150_TrainerC", "TRAINER_TYPE_NORMAL", 2),
        obj("MAN_2", 6, e0 + 5, "MOVEMENT_TYPE_FACE_DOWN", "Palm150_GymGuide"),
    ]
    j["bg_events"] = [sign(3, e0 + 1, "Palm150_Mirror1"), sign(4, e0 + 1, "Palm150_Mirror2"), sign(5, e0 + 1, "Palm150_Mirror3"),
                      sign(1, e0 + 1, "Palm150_DoorEntranceL"), sign(7, e0 + 1, "Palm150_DoorEntranceR")]
    for name in ("A", "B", "C"):
        y0 = ROOMS[name][0]
        j["bg_events"] += [sign(1, y0 + 1, f"Palm150_Door{name}L"), sign(7, y0 + 1, f"Palm150_Door{name}R")]
    jsave(f"{ROOT}/data/maps/PalmJadeGym/map.json", j)

    sc = ["PalmJadeGym_MapScripts::\n\t.byte 0\n",
          "Palm150_Jade::\n\ttrainerbattle_single TRAINER_PALM_JADE, Palm150_TextJadeIntro, Palm150_TextJadeDefeat, Palm150_JadeDefeated, NO_MUSIC\n"
          "\tmsgbox Palm150_TextJadeAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm150_JadeDefeated::\n\tmessage Palm150_TextBadge\n\twaitmessage\n\tcall Common_EventScript_PlayGymBadgeFanfare\n"
          "\tmsgbox Palm150_TextBadgeExplain, MSGBOX_DEFAULT\n\tsetflag FLAG_BADGE05_GET\n\tsetflag FLAG_DEFEATED_PETALBURG_GYM\n"
          "\tgiveitem ITEM_TM_PSYCHIC\n\tmsgbox Palm150_TextTM, MSGBOX_DEFAULT\n\trelease\n\tend\n",
          "Palm150_Lau::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_ESPEON, CRY_MODE_NORMAL\n\tmsgbox Palm150_TextLau, MSGBOX_DEFAULT\n\twaitmoncry\n\trelease\n\tend\n",
          "Palm150_GymGuide::\n\tmsgbox Palm150_TextGuide, MSGBOX_NPC\n\tend\n"]
    for k, tid in (("A", "TRAINER_PALM_JADE_GYM_A"), ("B", "TRAINER_PALM_JADE_GYM_B"), ("C", "TRAINER_PALM_JADE_GYM_C")):
        sc.append(f"Palm150_Trainer{k}::\n\ttrainerbattle_single {tid}, Palm150_Text{k}Intro, Palm150_Text{k}Defeat\n"
                  f"\tmsgbox Palm150_Text{k}After, MSGBOX_AUTOCLOSE\n\tend\n")
    for i in (1, 2, 3):
        sc.append(f"Palm150_Mirror{i}::\n\tmsgbox Palm150_TextMirror{i}, MSGBOX_SIGN\n\tend\n")
    for side in ("L", "R"):
        x, y = dest[("entrance", side)]
        sc.append(f"Palm150_DoorEntrance{side}::\n\tlockall\n\tsetvar VAR_0x8008, {x}\n\tsetvar VAR_0x8009, {y}\n"
                  "\tmsgbox Palm150_TextEnterDoor, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, YES, Palm150_EnterRoom\n\treleaseall\n\tend\n")
    for name in ("A", "B", "C"):
        for side, s in (("L", DOORS[name][0]), ("R", DOORS[name][1])):
            x, y = dest[(name, side)]
            sc.append(f"Palm150_Door{name}{side}::\n\tlockall\n\tsetvar VAR_0x8008, {x}\n\tsetvar VAR_0x8009, {y}\n"
                      f"\tmsgbox Palm150_TextSymbol{s}, MSGBOX_DEFAULT\n\tmsgbox Palm150_TextEnterDoor, MSGBOX_YESNO\n"
                      "\tgoto_if_eq VAR_RESULT, YES, Palm150_EnterRoom\n\treleaseall\n\tend\n")
    sc.append("Palm150_EnterRoom::\n\tclosemessage\n\tdelay 20\n\twarpdoor MAP_PALM_JADE_GYM, VAR_0x8008, VAR_0x8009\n"
              "\twaitstate\n\treleaseall\n\tend\n")
    open(f"{ROOT}/data/maps/PalmJadeGym/scripts.inc", "w").write("\n".join(sc))

    # Serenia: porta do ginasio vira warp 5 e abre depois do altar
    sp = f"{ROOT}/data/maps/PalmSerenia/map.json"
    s = jload(sp)
    pos = {label: (name, x, y) for (name, x, y, label) in SE.BUILDINGS}
    gname, gx0, gy0 = pos["gym"]
    gx, gy = gx0 + 3, gy0 + 4
    s["warp_events"] = [w for w in s["warp_events"] if w["dest_map"] != "MAP_PALM_JADE_GYM"]
    assert len(s["warp_events"]) == 5, "Serenia deveria ter 5 portas antes do ginasio"
    s["warp_events"].append(OD([("x", gx), ("y", gy), ("elevation", 0), ("dest_map", "MAP_PALM_JADE_GYM"), ("dest_warp_id", str(w_exit_l))]))
    for o in s["object_events"]:
        if o["script"] in ("Palm141_Jade", "Palm141_Lau"):
            o["flag"] = "FLAG_HT_SERENIA_DONE"          # Jade e Lau vao para o ginasio
    jsave(sp, s)
    ss = f"{ROOT}/data/maps/PalmSerenia/scripts.inc"
    t = open(ss).read()
    t = t.replace("Palm141_Load::\n\tsetmetatile", "Palm141_Load::\n\tgoto_if_set FLAG_HT_SERENIA_DONE, Palm141_LoadOpen\n\tsetmetatile", 1)
    if "Palm141_LoadOpen::" not in t:
        t += "\nPalm141_LoadOpen::\n\tend\n"
    lw = jload(f"{ROOT}/data/layouts/layouts.json")
    se = [l for l in lw["layouts"] if l.get("id") == "LAYOUT_PALM_SERENIA"][0]
    sbl = struct.unpack(f"<{se['width'] * se['height']}H", open(f"{ROOT}/{se['blockdata_filepath']}", "rb").read())
    door_mt = sbl[gy * se["width"] + gx] & 0x3FF
    t = t.replace("\tsetflag FLAG_HT_SERENIA_DONE\n\treleaseall\n\tend\n",
                  f"\tsetflag FLAG_HT_SERENIA_DONE\n\tsetmetatile {gx}, {gy}, {door_mt}, TRUE\n\tspecial DrawWholeMapView\n"
                  "\tplayse SE_UNLOCK\n\tmsgbox Palm141_TextGymOpens, MSGBOX_DEFAULT\n\treleaseall\n\tend\n", 1)
    open(ss, "w").write(t)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch6_gym.txt"], check=True)
    print("Ginasio da Jade instalado:", W, "x", H, "| porta em Serenia", (gx, gy), "| warps", len(warps))


if __name__ == "__main__":
    main()
