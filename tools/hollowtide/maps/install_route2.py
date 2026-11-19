#!/usr/bin/env python3
"""Instala a Route 2 gerada (MAP_PALM_ROUTE02) e as conexoes continuas Harvestvale <-> Route 2 <-> Breezeport.

- salva o layout LAYOUT_PALM_ROUTE02 (40x48, General + Lilycove) com placas de madeira nas pontas;
- conexoes sem fade: Harvestvale (OldaleTown) desce para a Route 2 e a Route 2 desce para a Breezeport,
  todas com offset 0 (trilha da Harvestvale em x 17-19, calcamento da Breezeport em x 18-21);
- abre a saida sul da Harvestvale (linhas 35-36, x 17-19) e troca o warp por uma trava que faz o jogador
  recuar um passo enquanto o Nevard nao for derrotado;
- treinadores com linha de visao, posicionados ao lado da trilha (andabilidade e elevacao conferidas).
Rodar depois de install_breezeport.py (que tambem grava a conexao da Breezeport para o norte).
"""
import collections, json, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "mapgen"))
import route2 as R2
from canvas import ROOT

OD = collections.OrderedDict
SIGN_GRASS = 3          # placa de madeira sobre grama (General), colisao 1
# (x, y, grafico, direcao, visao, script)
TRAINERS = [
    (26, 13, "HIKER", "LEFT", 3, "Palm080_RouteLIANG"),       # ao lado da curva leste da trilha
    (16, 27, "LASS", "RIGHT", 3, "Palm080_RouteMEI_LAN"),    # antes do mirante, olhando a trilha
    (21, 35, "YOUNGSTER", "LEFT", 3, "Palm080_RouteQIN"),    # na areia, ultimo desafio antes da cidade
]
# recompensa visivel fora do caminho (mirante); flag de item de mapa Hoenn sem acesso em Lunia
ITEMS = [(7, 26, "ITEM_SUPER_POTION", "FLAG_ITEM_ROUTE_102_POTION")]
SIGNS = [(16, 3, "Palm080_RouteSignNorth"), (17, 40, "Palm080_RouteSignSouth")]
OLDALE_GATE = [(17, 35), (18, 35), (19, 35)]


STONE = set(range(520, 539))          # calcamento da praca (secundario Slateport)
VIEW_X = (9, 28)                      # colunas visiveis a partir da trilha da Route 2 (x 16-21, +-7)
VIEW_ROWS = 4                         # linhas da Harvestvale visiveis do topo da Route 2


def harvestvale_dirt_edge(v, ow, oh):
    from canvas import _autotiler
    at = _autotiler("gTileset_General", None)
    from autotile import GENERAL_CLASSES
    path = STONE | GENERAL_CLASSES["sand"]          # idempotente: terra ja aplicada conta como caminho
    grid = [["sand" if (v[y * ow + x] & 0x3FF) in path else "grass" for x in range(ow)] for y in range(oh)]
    out = list(v)
    for y in range(oh - VIEW_ROWS, oh):
        for x in range(VIEW_X[0], VIEW_X[1] + 1):
            if grid[y][x] == "sand" and (v[y * ow + x] & 0x3FF) in STONE | {529}:
                m, _ = at.tile(grid, x, y)
                assert m < 512, (x, y, m)
                out[y * ow + x] = m | (3 << 12)
    return out


def conn(direction, mapname):
    return [OD([("map", mapname), ("offset", 0), ("direction", direction)])]


def jload(p):
    return json.load(open(p), object_pairs_hook=OD)


def jsave(p, j):
    open(p, "w").write(json.dumps(j, indent=2, ensure_ascii=False) + "\n")


def main():
    c = R2.compose()
    for (x, y, _) in SIGNS:
        c.put(x, y, SIGN_GRASS, 1, 3)
    bl = c.save("PalmRoute02", border=(468, 469, 476, 477))
    w = c.w

    lay = jload(f"{ROOT}/data/layouts/layouts.json")
    for l in lay["layouts"]:
        if l.get("id") == "LAYOUT_PALM_ROUTE02":
            l["width"], l["height"] = c.w, c.h
            l["primary_tileset"], l["secondary_tileset"] = c.primary, c.secondary
    jsave(f"{ROOT}/data/layouts/layouts.json", lay)

    p = f"{ROOT}/data/maps/PalmRoute02/map.json"
    j = jload(p)
    j["connections"] = conn("up", "MAP_OLDALE_TOWN") + conn("down", "MAP_PALM_BRISA")
    j["object_events"] = []
    for (x, y, gfx, d, sight, script) in TRAINERS:
        v = bl[y * w + x]
        assert (v >> 10) & 3 == 0, f"treinador {script} em tile bloqueado {(x, y)}"
        j["object_events"].append(OD([("graphics_id", f"OBJ_EVENT_GFX_{gfx}"), ("x", x), ("y", y), ("elevation", v >> 12),
                                      ("movement_type", f"MOVEMENT_TYPE_FACE_{d}"), ("movement_range_x", 0), ("movement_range_y", 0),
                                      ("trainer_type", "TRAINER_TYPE_NORMAL"), ("trainer_sight_or_berry_tree_id", str(sight)),
                                      ("script", script), ("flag", "0")]))
    for (x, y, item, flag) in ITEMS:
        v = bl[y * w + x]
        assert (v >> 10) & 3 == 0, f"item {item} em tile bloqueado {(x, y)}"
        j["object_events"].append(OD([("graphics_id", "OBJ_EVENT_GFX_ITEM_BALL"), ("x", x), ("y", y), ("elevation", v >> 12),
                                      ("movement_type", "MOVEMENT_TYPE_FACE_DOWN"), ("movement_range_x", 0), ("movement_range_y", 0),
                                      ("trainer_type", "TRAINER_TYPE_NONE"), ("trainer_sight_or_berry_tree_id", item),
                                      ("script", "Common_EventScript_FindItem"), ("flag", flag)]))
    j["warp_events"] = []
    j["coord_events"] = []
    j["bg_events"] = [OD([("type", "sign"), ("x", x), ("y", y), ("elevation", 0),
                          ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", s)]) for (x, y, s) in SIGNS]
    jsave(p, j)

    # scripts da rota: sem warps; derrota em ingles
    sp = f"{ROOT}/data/maps/PalmRoute02/scripts.inc"
    s = open(sp).read()
    s = re.sub(r"Palm080_ReturnColheita::\n(\t.*\n)+\n", "", s)
    s = re.sub(r"Palm080_EnterBrisa::\n(\t.*\n)+\n", "", s)
    losses = {"LIANG": "Whoa! Your team hits harder\\nthan a rockslide!",
              "MEI_LAN": "Swept away like a wave...\\nYou're good!",
              "QIN": "Okay, okay! BREEZEPORT is\\nall yours. Go on!"}
    for k, t in losses.items():
        a, b = t.split("\\n")
        s = re.sub(rf"(Palm080_Text{k}Loss:\n)(\t\.string .*\n)+", rf'\g<1>\t.string "{a}\\n"\n\t.string "{b}$"\n', s)
    open(sp, "w").write(s)

    # Harvestvale: conexao para o sul e saida aberta na calcada (pedra 528/529/530)
    op = f"{ROOT}/data/maps/OldaleTown/map.json"
    o = jload(op)
    o["connections"] = conn("down", "MAP_PALM_ROUTE02")
    jsave(op, o)
    e = [l for l in lay["layouts"] if l.get("id") == o["layout"]][0]
    ow, oh = e["width"], e["height"]
    mp = f"{ROOT}/{e['blockdata_filepath']}"
    v = list(struct.unpack(f"<{ow * oh}H", open(mp, "rb").read()))
    for y in (oh - 2, oh - 1):
        for x in (17, 18, 19):
            v[y * ow + x] = 529 | (3 << 12)
    # O GBA desenha o mapa conectado com o tileset do mapa ATUAL: o que a Route 2 (secundario Lilycove) enxerga
    # da Harvestvale (secundario Slateport) tem que ser so do primario. As 4 linhas finais da Harvestvale na
    # janela da trilha viram estrada de terra (General): o calcamento da vila termina e comeca a estrada rural.
    v = harvestvale_dirt_edge(v, ow, oh)
    open(mp, "wb").write(struct.pack(f"<{ow * oh}H", *v))
    osp = f"{ROOT}/data/maps/OldaleTown/scripts.inc"
    s = open(osp).read()
    new_leave = ("Palm080_LeaveColheita::\n\tgoto_if_set FLAG_DEFEATED_RUSTBORO_GYM, Palm080_LeaveColheitaOk\n"
                 "\tlockall\n\tmsgbox Palm060_TextClosedRoad, MSGBOX_DEFAULT\n"
                 "\tapplymovement OBJ_EVENT_ID_PLAYER, Palm080_StepBack\n\twaitmovement 0\n\treleaseall\n\tend\n\n"
                 "Palm080_LeaveColheitaOk::\n\tend\n\n"
                 "Palm080_StepBack:\n\twalk_up\n\tstep_end\n\n")
    s = re.sub(r"Palm080_LeaveColheita::\n(?:.*\n)*?\n(?=Palm080_ColheitaRouteOpen::)", new_leave, s)
    s = re.sub(r"Palm080_ToRoute02::\n(\t.*\n)+\n", "", s)
    open(osp, "w").write(s)
    assert "Palm080_StepBack:" in s and "Palm080_ToRoute02" not in s
    print("Route 2 instalada:", c.w, "x", c.h, "| conexoes Harvestvale/Route 2/Breezeport")


if __name__ == "__main__":
    main()
