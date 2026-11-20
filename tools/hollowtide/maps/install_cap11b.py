#!/usr/bin/env python3
"""Capitulo 11 (parte 2): a Liga Pokemon de Lunia ("A Elite dos Nerds") e o campeao Doge.

- ordem das salas pelo estilo de cada uma (a cor do piso combina com o tipo):
  saguao -> Hall5 -> sala de gelo (Angelic, Gelo) -> Hall1 -> sala roxa (Riven, Normal) -> Hall2 ->
  sala de tatame (Du, Lutador) -> Hall3 -> sala laranja (Pkas, Solar, Mega Charizard X) -> Hall4 -> campeao;
- times do canone (hollowtide_canon.json / roteiro, sec. 16) com golpes; Pkas e o primeiro adversario a usar
  Mega Evolucao; Doge fecha com Mega Latios;
- sala do campeao sem a cena de Hoenn (rival e professor): Doge entrega o titulo e leva o jogador ao Hall
  da Fama; textos do Hall da Fama com o Doge;
- Route 11: times com golpes definidos (o Altaria do Felix nao aprende mais Perish Song pelo nivel).
Rodar depois de install_cap11.py.
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
from canvas import ROOT
from install_cap4 import jload, jsave

IV = lambda n: f"IVs: {n} HP / {n} Atk / {n} Def / {n} SpA / {n} SpD / {n} Spe"


def mon(species, level, moves, iv=30, item=None, ability=None):
    s = species + (f" @ {item}" if item else "") + "\n"
    if ability:
        s += f"Ability: {ability}\n"
    s += f"Level: {level}\n{IV(iv)}\n" + "".join(f"- {m}\n" for m in moves)
    return s


def header(tid, name, cls, pic, gender, music, items, ai, mugshot=None):
    s = f"=== {tid} ===\nName: {name}\nClass: {cls}\nPic: {pic}\nGender: {gender}\nMusic: {music}\n"
    if items:
        s += f"Items: {' / '.join(items)}\n"
    s += f"Double Battle: No\nAI: {ai}\n"
    if mugshot:
        s += f"Mugshot: {mugshot}\n"
    return s + "\n"


E4_AI = "Check Bad Move / Try To Faint"
FR2 = ["Full Restore", "Full Restore"]
PARTIES = {
    # ---------------- Route 11 (treinadores de elite)
    "TRAINER_VINCENT": header("TRAINER_VINCENT", "VINCENT", "Cooltrainer", "Cooltrainer M", "Male", "Cool", None, "Check Bad Move") + "\n".join([
        mon("Lucario", 53, ["Aura Sphere", "Flash Cannon", "Dark Pulse", "Extreme Speed"], 20),
        mon("Gyarados", 53, ["Waterfall", "Crunch", "Ice Fang", "Dragon Dance"], 20),
        mon("Magnezone", 54, ["Thunderbolt", "Flash Cannon", "Tri Attack", "Volt Switch"], 20)]),
    "TRAINER_FELIX": header("TRAINER_FELIX", "FELIX", "Cooltrainer", "Cooltrainer F", "Female", "Cool", None, "Check Bad Move") + "\n".join([
        mon("Altaria", 53, ["Dragon Pulse", "Moonblast", "Flamethrower", "Cotton Guard"], 20),
        mon("Gardevoir", 54, ["Psychic", "Moonblast", "Shadow Ball", "Calm Mind"], 20),
        mon("Milotic", 54, ["Hydro Pump", "Ice Beam", "Dragon Pulse", "Recover"], 20)]),
    "TRAINER_LEROY": header("TRAINER_LEROY", "LEROY", "Cooltrainer", "Cooltrainer M", "Male", "Cool", None, "Check Bad Move") + "\n".join([
        mon("Hawlucha", 54, ["Flying Press", "X-Scissor", "Poison Jab", "Swords Dance"], 20),
        mon("Druddigon", 54, ["Dragon Claw", "Fire Punch", "Thunder Punch", "Sucker Punch"], 20),
        mon("Garchomp", 55, ["Earthquake", "Dragon Claw", "Stone Edge", "Fire Fang"], 20)]),
    # ---------------- Elite (slots vanilla: Glacia -> Angelic, Phoebe -> Riven, Sidney -> Du, Drake -> Pkas)
    "TRAINER_GLACIA": header("TRAINER_GLACIA", "ANGELIC", "Elite Four", "Elite Four Sidney", "Male", "Elite Four", FR2, E4_AI, "Blue") + "\n".join([
        mon("Ninetales-Alola", 55, ["Blizzard", "Moonblast", "Aurora Veil", "Freeze-Dry"], ability="Snow Warning"),
        mon("Froslass", 56, ["Ice Beam", "Shadow Ball", "Thunderbolt", "Will-O-Wisp"]),
        mon("Glaceon", 57, ["Blizzard", "Shadow Ball", "Water Pulse", "Calm Mind"]),
        mon("Weavile", 58, ["Triple Axel", "Knock Off", "Ice Shard", "Swords Dance"]),
        mon("Mamoswine", 59, ["Earthquake", "Icicle Crash", "Ice Shard", "Stone Edge"], 31, "Sitrus Berry")]),
    "TRAINER_PHOEBE": header("TRAINER_PHOEBE", "RIVEN", "Elite Four", "Psychic M", "Male", "Elite Four", FR2, E4_AI, "Purple") + "\n".join([
        mon("Furfrou", 58, ["Double Edge", "Sucker Punch", "U-turn", "Thunder Wave"]),
        mon("Stoutland", 59, ["Facade", "Crunch", "Play Rough", "Wild Charge"], ability="Intimidate"),
        mon("Porygon2", 59, ["Tri Attack", "Ice Beam", "Thunderbolt", "Recover"], item="Eviolite"),
        mon("Zoroark-Hisui", 60, ["Shadow Ball", "Hyper Voice", "Focus Blast", "Nasty Plot"]),
        mon("Porygon-Z", 62, ["Tri Attack", "Dark Pulse", "Ice Beam", "Thunderbolt"], 31, "Sitrus Berry", "Adaptability")]),
    "TRAINER_SIDNEY": header("TRAINER_SIDNEY", "DU", "Elite Four", "Black Belt", "Male", "Elite Four", FR2, E4_AI, "Green") + "\n".join([
        mon("Hawlucha", 61, ["Flying Press", "Close Combat", "Poison Jab", "Swords Dance"]),
        mon("Infernape", 62, ["Close Combat", "Flare Blitz", "Mach Punch", "U-turn"]),
        mon("Lucario", 63, ["Aura Sphere", "Flash Cannon", "Dark Pulse", "Nasty Plot"]),
        mon("Kommo-o", 64, ["Clanging Scales", "Close Combat", "Iron Head", "Dragon Dance"]),
        mon("Conkeldurr", 66, ["Drain Punch", "Mach Punch", "Knock Off", "Ice Punch"], 31, "Sitrus Berry", "Guts")]),
    "TRAINER_DRAKE": header("TRAINER_DRAKE", "PKAS", "Elite Four", "Elite Four Drake", "Male", "Elite Four", FR2, E4_AI, "Yellow") + "\n".join([
        mon("Torkoal", 65, ["Lava Plume", "Solar Beam", "Earth Power", "Yawn"], ability="Drought"),
        mon("Venusaur", 66, ["Solar Beam", "Sludge Bomb", "Weather Ball", "Sleep Powder"], ability="Chlorophyll"),
        mon("Heliolisk", 67, ["Thunderbolt", "Weather Ball", "Grass Knot", "Volt Switch"], ability="Solar Power"),
        mon("Volcarona", 68, ["Fiery Dance", "Bug Buzz", "Giga Drain", "Quiver Dance"]),
        mon("Charizard", 70, ["Flare Blitz", "Dragon Claw", "Earthquake", "Dragon Dance"], 31, "Charizardite X")]),
    # ---------------- campeao
    "TRAINER_WALLACE": header("TRAINER_WALLACE", "DOGE", "Champion", "Champion Wallace", "Male", "Male",
                              ["Full Restore"] * 4, E4_AI, "Yellow") + "\n".join([
        mon("Meowscarada", 71, ["Flower Trick", "Knock Off", "U-turn", "Play Rough"], 31),
        mon("Ninetales", 72, ["Fire Blast", "Energy Ball", "Will-O-Wisp", "Nasty Plot"], 31, ability="Flash Fire"),
        mon("Vaporeon", 72, ["Scald", "Ice Beam", "Shadow Ball", "Hyper Voice"], 31),
        mon("Umbreon", 73, ["Foul Play", "Moonlight", "Toxic", "Snarl"], 31),
        mon("Lugia", 75, ["Aeroblast", "Psychic", "Calm Mind", "Roost"], 31, ability="Multiscale"),
        mon("Latios", 77, ["Draco Meteor", "Luster Purge", "Calm Mind", "Surf"], 31, "Latiosite")]),
}

# ordem nova: (sala, warp de baixo -> hall anterior, warp de cima -> hall seguinte)
CHAIN = [("MAP_EVER_GRANDE_CITY_HALL5", None), ("MAP_EVER_GRANDE_CITY_GLACIAS_ROOM", "EverGrandeCity_GlaciasRoom"),
         ("MAP_EVER_GRANDE_CITY_HALL1", None), ("MAP_EVER_GRANDE_CITY_PHOEBES_ROOM", "EverGrandeCity_PhoebesRoom"),
         ("MAP_EVER_GRANDE_CITY_HALL2", None), ("MAP_EVER_GRANDE_CITY_SIDNEYS_ROOM", "EverGrandeCity_SidneysRoom"),
         ("MAP_EVER_GRANDE_CITY_HALL3", None), ("MAP_EVER_GRANDE_CITY_DRAKES_ROOM", "EverGrandeCity_DrakesRoom"),
         ("MAP_EVER_GRANDE_CITY_HALL4", None), ("MAP_EVER_GRANDE_CITY_CHAMPIONS_ROOM", "EverGrandeCity_ChampionsRoom")]
FOLDER = {"MAP_EVER_GRANDE_CITY_HALL%d" % i: "EverGrandeCity_Hall%d" % i for i in range(1, 6)}
FOLDER.update({m: f for (m, f) in CHAIN if f})
GFX = {"EverGrandeCity_GlaciasRoom": "OBJ_EVENT_GFX_SIDNEY", "EverGrandeCity_PhoebesRoom": "OBJ_EVENT_GFX_PSYCHIC_M",
       "EverGrandeCity_SidneysRoom": "OBJ_EVENT_GFX_BLACK_BELT", "EverGrandeCity_DrakesRoom": "OBJ_EVENT_GFX_DRAKE"}


def set_parties():
    p = f"{ROOT}/src/data/trainers.party"
    t = open(p).read()
    for tid, block in PARTIES.items():
        pat = re.compile(r"=== %s ===\n.*?(?=\n=== )" % tid, re.S)
        assert len(pat.findall(t)) == 1, tid
        t = pat.sub(lambda _m: block.rstrip("\n") + "\n", t)
    open(p, "w").write(t)


def rewire():
    """Cada hall: warps de baixo (y=12/33) -> sala anterior (warp 1, a porta de cima); warp de cima -> sala
    seguinte (warp 0). Cada sala: warp 0 (baixo) -> hall anterior (warp 1); warp 1 (cima) -> hall seguinte (warp 0)."""
    for i, (m, _) in enumerate(CHAIN):
        f = FOLDER[m]
        mp = f"{ROOT}/data/maps/{f}/map.json"
        j = jload(mp)
        prev = CHAIN[i - 1][0] if i > 0 else "MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F"
        nxt = CHAIN[i + 1][0] if i + 1 < len(CHAIN) else "MAP_EVER_GRANDE_CITY_HALL_OF_FAME"
        top = min(w["y"] for w in j["warp_events"])
        for w in j["warp_events"]:
            if w["y"] == top:
                w["dest_map"], w["dest_warp_id"] = nxt, "0"
            elif prev != "MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F":
                w["dest_map"], w["dest_warp_id"] = prev, "1"
        if f in GFX:
            j["object_events"][0]["graphics_id"] = GFX[f]
        if f == "EverGrandeCity_ChampionsRoom":
            j["object_events"] = j["object_events"][:1]          # sem rival e sem professor
        jsave(mp, j)


def renumber_state():
    """VAR_ELITE_4_STATE conta as salas na ordem vanilla (Sidney 0->1, Phoebe 1->2, Glacia 2->3, Drake 3->4).
    Na ordem nova: Glacia 0->1, Phoebe 1->2 (igual), Sidney 2->3, Drake 3->4 (igual)."""
    sub = {"EverGrandeCity_GlaciasRoom": [("map_script_2 VAR_ELITE_4_STATE, 2,", "map_script_2 VAR_ELITE_4_STATE, 0,"),
                                          ("setvar VAR_ELITE_4_STATE, 3", "setvar VAR_ELITE_4_STATE, 1"),
                                          ("call_if_eq VAR_ELITE_4_STATE, 3,", "call_if_eq VAR_ELITE_4_STATE, 1,")],
           "EverGrandeCity_SidneysRoom": [("map_script_2 VAR_ELITE_4_STATE, 0,", "map_script_2 VAR_ELITE_4_STATE, 2,"),
                                          ("setvar VAR_ELITE_4_STATE, 1", "setvar VAR_ELITE_4_STATE, 3"),
                                          ("call_if_eq VAR_ELITE_4_STATE, 1,", "call_if_eq VAR_ELITE_4_STATE, 3,")]}
    for f, pairs in sub.items():
        p = f"{ROOT}/data/maps/{f}/scripts.inc"
        t = open(p).read()
        for a, b in pairs:
            if b not in t:
                assert t.count(a) == 1, (f, a)
                t = t.replace(a, b)
        open(p, "w").write(t)


CHAMPION = """EverGrandeCity_ChampionsRoom_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, EverGrandeCity_ChampionsRoom_OnWarp
	map_script MAP_SCRIPT_ON_FRAME_TABLE, EverGrandeCity_ChampionsRoom_OnFrame
	.byte 0

EverGrandeCity_ChampionsRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, EverGrandeCity_ChampionsRoom_EventScript_PlayerTurnNorth
	.2byte 0

EverGrandeCity_ChampionsRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

EverGrandeCity_ChampionsRoom_OnFrame:
	map_script_2 VAR_TEMP_1, 0, EverGrandeCity_ChampionsRoom_EventScript_EnterRoom
	.2byte 0

EverGrandeCity_ChampionsRoom_EventScript_EnterRoom::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_WalkUp4
	waitmovement 0
	delay 40
	applymovement LOCALID_PLAYER, EverGrandeCity_ChampionsRoom_Movement_PlayerApproachChampion
	waitmovement 0
	setvar VAR_TEMP_1, 1
	goto EverGrandeCity_ChampionsRoom_EventScript_Doge
	releaseall
	end

EverGrandeCity_ChampionsRoom_Movement_PlayerApproachChampion:
	walk_up
	walk_up
	step_end

EverGrandeCity_ChampionsRoom_EventScript_Doge::
	playbgm MUS_ENCOUNTER_CHAMPION, FALSE
	msgbox EverGrandeCity_ChampionsRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_WALLACE, EverGrandeCity_ChampionsRoom_Text_Defeat
	goto EverGrandeCity_ChampionsRoom_EventScript_Defeated
	end

EverGrandeCity_ChampionsRoom_EventScript_Defeated::
	playse SE_DOOR
	setmetatile 6, 1, METATILE_EliteFour_OpenDoorChampion_Frame, FALSE
	setmetatile 6, 2, METATILE_EliteFour_OpenDoorChampion_Opening, FALSE
	special DrawWholeMapView
	msgbox EverGrandeCity_ChampionsRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CHAMPIONS_ROOM_WALLACE, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	delay 20
	applymovement LOCALID_CHAMPIONS_ROOM_WALLACE, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox EverGrandeCity_ChampionsRoom_Text_ComeWithMe, MSGBOX_DEFAULT
	closemessage
	delay 30
	applymovement LOCALID_CHAMPIONS_ROOM_WALLACE, EverGrandeCity_ChampionsRoom_Movement_ChampionExit
	applymovement LOCALID_PLAYER, EverGrandeCity_ChampionsRoom_Movement_PlayerExit
	waitmovement 0
	setflag FLAG_HIDE_PETALBURG_GYM_GREETER
	warp MAP_EVER_GRANDE_CITY_HALL_OF_FAME, 7, 16
	waitstate
	releaseall
	end

EverGrandeCity_ChampionsRoom_Movement_PlayerExit:
	walk_up
	walk_up
	walk_up
	delay_16
	walk_up
	delay_8
	set_invisible
	step_end

EverGrandeCity_ChampionsRoom_Movement_ChampionExit:
	walk_up
	walk_up
	walk_up
	set_invisible
	step_end

EverGrandeCity_ChampionsRoom_Text_IntroSpeech:
	.string "x$"

EverGrandeCity_ChampionsRoom_Text_Defeat:
	.string "x$"

EverGrandeCity_ChampionsRoom_Text_PostBattleSpeech:
	.string "x$"

EverGrandeCity_ChampionsRoom_Text_ComeWithMe:
	.string "x$"
"""


def main():
    set_parties()
    rewire()
    renumber_state()
    open(f"{ROOT}/data/maps/EverGrandeCity_ChampionsRoom/scripts.inc", "w").write(CHAMPION)
    subprocess.run([sys.executable, f"{ROOT}/tools/hollowtide/texts.py", f"{ROOT}/tools/hollowtide/text/ch11b.txt"], check=True)
    print("Cap. 11 (parte 2) instalado: Elite (Angelic, Riven, Du, Pkas) e campeao Doge")


if __name__ == "__main__":
    main()
