#!/usr/bin/env python3
"""Varredura visual dos mapas convertidos (auditoria de acabamento, 25/11): capturas em grade de cada mapa do GBA.

Usa a build de conteudo + provas/visual (o PC do quarto espera 20 quadros e faz `warp MAP_T20, 0, 1111, 2222`). Para cada ponto da grade:
volta ao estado salvo diante do PC, troca na RAM o destino do warp (mapa da celula, x, z) e aperta A. O warp carrega
o mapa de verdade (blocos 3D, colisao, NPCs da zona), o que mexer so na posicao do jogador nao faz.

Uso: qa_visual.py ROM ESTADO_DO_QUARTO PASTA [MAPA ...] [--passo 12x8] [--interior MAPA X Z ...]
Relogio fixado em 13h com faketime (apt install faketime), para as capturas sairem com luz do dia.\nSaida: PASTA/<mapa>/x_y.png (tela de cima) e PASTA/<mapa>.png (folha de contato com as coordenadas do GBA).
"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
from ds_driver import DS
import lunia_mundo as L

TAM = {"Dawnmere": (34, 29), "Route1": (40, 53), "Harvestvale": (39, 37), "Route2": (40, 48), "Brisa": (72, 60), "Route3": (56, 80), "Ferralia": (72, 64)}
PADRAO = struct.pack("<5H", 176, 60, 0, 1111, 2222)   # warp MAP_T20, 0, 1111, 2222 (provas/visual)


def headers(rom):
    import ndspy.rom, ndspy.narc
    from matrix import Matrix
    r = ndspy.rom.NintendoDSRom.fromFile(rom)
    m = Matrix(ndspy.narc.NARC(r.getFileByName("a/0/4/1")).files[0])
    return lambda x, z: m.headers[(z // 32) * m.w + x // 32]


class Visita:
    def __init__(self, rom, estado, pasta):
        self.d = DS(rom)
        self.hdr = headers(rom)
        self.pc = os.path.join(pasta, "_pc.dst")
        d = self.d
        d.load(estado); d.wait(30)
        d.press("UP", 16, 24); d.press("UP", 4, 20)
        d.save(self.pc)

    def ir(self, x, z, espera=90, mapa=None):
        """Warp para a coordenada de mundo (x, z) (ou para (x, z) do mapa dado, ex. um interior). Devolve where()."""
        d = self.d
        d.load(self.pc); d.wait(2)
        d.press("A", 4, 4)                              # o script carrega e fica na espera de 20 quadros
        ram = bytes(d.emu.memory.unsigned[0x02000000:0x02400000])
        i = ram.find(PADRAO)
        assert i >= 0, "comando warp da prova 0921 nao achado na RAM"
        a = 0x02000000 + i
        d.emu.memory.write_short(a + 2, mapa if mapa is not None else self.hdr(x, z))
        d.emu.memory.write_short(a + 6, x)
        d.emu.memory.write_short(a + 8, z)
        for _ in range(40):
            d.wait(15)
            w = d.where()
            if w and (w[1], w[2]) == (x, z):
                break
        for _ in range(60):                             # troca de header: o fade demora mais (musica, nome da area)
            im = d.emu.screenshot().crop((0, 0, 256, 192)).convert("L")
            if sum(im.resize((32, 24)).getdata()) / 768 > 40:
                break
            d.wait(15)
        d.wait(espera)
        return d.where()

    def foto(self, path):
        self.d.emu.screenshot().crop((0, 0, 256, 192)).save(path)


def folha(fotos, cols, path, rotulo):
    from PIL import Image, ImageDraw
    rows = (len(fotos) + cols - 1) // cols
    im = Image.new("RGB", (cols * 256, rows * 192), (0, 0, 0))
    dr = ImageDraw.Draw(im)
    for k, (p, txt) in enumerate(fotos):
        x, y = (k % cols) * 256, (k // cols) * 192
        im.paste(Image.open(p), (x, y))
        dr.rectangle((x, y + 178, x + 70, y + 191), fill=(0, 0, 0))
        dr.text((x + 2, y + 179), txt, fill=(255, 255, 0))
    im.save(path)


def main(argv):
    rom, estado, pasta = argv[:3]
    resto = argv[3:]
    passo = (12, 8)
    if "--passo" in resto:
        k = resto.index("--passo"); passo = tuple(map(int, resto[k + 1].split("x"))); del resto[k:k + 2]
    interiores = []
    while "--interior" in resto:                         # --interior MAPA X Z: uma captura dentro de um interior
        k = resto.index("--interior"); interiores.append(tuple(map(int, resto[k + 1:k + 4]))); del resto[k:k + 4]
    mapas = resto or ([] if interiores else list(TAM))
    os.makedirs(pasta, exist_ok=True)
    v = Visita(rom, estado, pasta)
    for mid, x, z in interiores:
        r = v.ir(x, z, mapa=mid)
        v.foto(f"{pasta}/interior_{mid}_{x}_{z}.png"); print("interior", mid, x, z, "->", r)
    for mapa in mapas:
        w, h = TAM[mapa]
        os.makedirs(f"{pasta}/{mapa}", exist_ok=True)
        xs = list(range(passo[0] // 2, w, passo[0])); ys = list(range(passo[1] // 2 - 1, h, passo[1]))
        fotos = []
        for y in ys:
            for x in xs:
                wx, wz = L.gba(mapa, x, y)
                r = v.ir(wx, wz)
                p = f"{pasta}/{mapa}/{x}_{y}.png"
                v.foto(p); fotos.append((p, f"{x},{y}"))
                if not r or (r[1], r[2]) != (wx, wz):
                    print(mapa, x, y, "warp nao chegou:", r)
        folha(fotos, len(xs), f"{pasta}/{mapa}.png", mapa)
        print(mapa, len(fotos), "capturas")


if __name__ == "__main__":
    import shutil
    if "FAKETIME" not in os.environ and shutil.which("faketime"):   # luz do dia: o HGSS escurece o campo a noite
        os.execvp("faketime", ["faketime", "-f", "@2026-11-25 13:00:00", sys.executable] + sys.argv)
    main(sys.argv[1:])
