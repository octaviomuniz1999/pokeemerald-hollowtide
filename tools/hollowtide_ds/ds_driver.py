#!/usr/bin/env python3
"""Harness de QA para o Hollowtide em HeartGold (hg-engine), sobre DeSmuME sem tela (py-desmume).

- liga a ROM, aperta botoes por N frames, tira capturas (as duas telas), salva/carrega estados;
- le o estado do jogo por ganchos de execucao (enderecos do rom.ld do hg-engine): o ponteiro do FieldSystem vem de
  FieldSystem_FlagCheck (r0) e o do avatar do jogador de PlayerAvatar_GetXCoord (r0);
  FieldSystem->location (0x20) -> {mapId, warpId, x, z}; avatar->mapObject (0x30) -> xCurr (0x64), yCurr (0x6C).
Requer SDL_VIDEODRIVER=dummy e SDL_AUDIODRIVER=dummy (definidos aqui se faltarem).
"""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
from desmume.emulator import DeSmuME
from desmume.controls import keymask, Keys

FLAGCHECK = 0x020403FC
GETX = 0x0205C67C
KEYS = {"A": Keys.KEY_A, "B": Keys.KEY_B, "START": Keys.KEY_START, "SELECT": Keys.KEY_SELECT,
        "UP": Keys.KEY_UP, "DOWN": Keys.KEY_DOWN, "LEFT": Keys.KEY_LEFT, "RIGHT": Keys.KEY_RIGHT,
        "L": Keys.KEY_L, "R": Keys.KEY_R, "X": Keys.KEY_X, "Y": Keys.KEY_Y}


class DS:
    def __init__(self, rom, savetype=0):
        self.emu = DeSmuME()
        if savetype:
            self.emu.set_savetype(savetype)             # tipo de memoria de save (0 = autodetectar)
        self.emu.open(rom)
        self.emu.volume_set(0)
        self.fsys = 0
        self.avatar = 0
        self.falas = os.environ.get("QA_FALAS")   # pasta: guarda cada pagina de fala (caixa de texto do campo) antes de apertar
        self._fala_n, self._fala_last = 0, None
        if self.falas:
            os.makedirs(self.falas, exist_ok=True)
        self._hook()

    def _hook(self):
        mem = self.emu.memory
        def on_flag(addr, size):
            self.fsys = mem.register_arm9.r0
        def on_getx(addr, size):
            self.avatar = mem.register_arm9.r0
        mem.register_exec(FLAGCHECK, on_flag)
        mem.register_exec(GETX, on_getx)

    def reset(self):
        """Reinicia o console (a memoria do save fica); os ganchos sao registrados de novo."""
        self.emu.reset()
        self.fsys = self.avatar = 0
        self._hook()

    def wait(self, n):
        for _ in range(n):
            self.emu.cycle(with_joystick=False)

    BOX = (10, 150, 234, 186)                       # interior da caixa de texto do campo (tela de cima)

    def box_visible(self, im=None):
        """Caixa de texto do campo: moldura cinza (96,96,104) dos dois lados e fundo branco."""
        im = im or self.emu.screenshot()
        px = lambda p: im.getpixel(p)[:3]
        return px((6, 150)) == px((240, 160)) == (96, 96, 104) and px((12, 160)) == (248, 248, 248)

    def capture_fala(self):
        """Espera a pagina terminar de escrever e guarda a tela se o texto for novo."""
        im = self.emu.screenshot()
        if not self.box_visible(im):
            return
        for _ in range(30):                          # ate o texto parar de mudar (a impressao e letra a letra)
            self.wait(6)
            im2 = self.emu.screenshot()
            if im2.crop(self.BOX).tobytes() == im.crop(self.BOX).tobytes():
                break
            im = im2
        crop = im.crop(self.BOX).tobytes()
        if crop != self._fala_last and self.box_visible(im):
            self._fala_last = crop
            self._fala_n += 1
            w = self.where()
            im.crop((0, 0, 256, 192)).save(os.path.join(self.falas, f"{self._fala_n:04d}_m{w[0] if w else 'x'}.png"))

    def press(self, key, hold=6, after=20):
        if self.falas:
            self.capture_fala()
        k = keymask(KEYS[key])
        self.emu.input.keypad_add_key(k); self.wait(hold)
        self.emu.input.keypad_rm_key(k); self.wait(after)

    def mash(self, key, n, after=20):
        for _ in range(n):
            self.press(key, 4, after)

    def touch(self, x, y, hold=6, after=30):
        """Toque na tela de baixo (coordenadas 0-255 x 0-191)."""
        self.emu.input.touch_set_pos(x, y); self.wait(hold)
        self.emu.input.touch_release(); self.wait(after)

    def u32(self, addr):
        return self.emu.memory.unsigned.read_long(addr)

    def where(self):
        """(mapId, x, y) do jogador, ou None fora do campo."""
        if self.avatar and not self.fsys:
            self._find_fsys()
        if not (self.fsys and self.avatar):
            return None
        loc = self.u32(self.fsys + 0x20)
        obj = self.u32(self.avatar + 0x30)
        if not (0x02000000 <= loc < 0x02400000 and 0x02000000 <= obj < 0x02400000):
            return None
        return (self.u32(loc), self.u32(obj + 0x64), self.u32(obj + 0x6C))

    def _find_fsys(self):
        """Depois de um CONTINUE nenhum script roda e FieldSystem_FlagCheck nao e chamada: acha o FieldSystem pelo
        ponteiro do avatar, que ele guarda em +0x40 (conferido num estado em que os dois ganchos tinham disparado)."""
        import struct
        blk = bytes(self.emu.memory.unsigned[0x02000000:0x02400000])
        needle = struct.pack("<I", self.avatar)
        i = blk.find(needle)
        while i >= 0:
            cand = 0x02000000 + i - 0x40
            loc = self.u32(cand + 0x20)
            if 0x02000000 <= loc < 0x02400000 and self.u32(loc) < 1000:
                self.fsys = cand
                return
            i = blk.find(needle, i + 1)

    def shot(self, path):
        self.emu.screenshot().save(path)

    def top_is_field(self):
        """Tela de baixo do campo: a margem esquerda do painel do menu e verde (8,260) e (8,360); na batalha ela e a
        interface de luta. (Os pontos do meio somem quando o menu ganha os icones de Pokemon e Pokedex.)"""
        im = self.emu.screenshot()
        return all(im.getpixel(p)[:3] == (24, 200, 112) for p in [(8, 260), (8, 360)])

    def save(self, path):
        """Salva o estado e, ao lado, os ponteiros capturados (a RAM volta igual ao carregar)."""
        self.emu.savestate.save_file(path)
        with open(path + ".ptr", "w") as f:
            f.write(f"{self.fsys:x} {self.avatar:x}\n")

    def load(self, path):
        self.emu.savestate.load_file(path)
        try:
            a, b = open(path + ".ptr").read().split()
            self.fsys, self.avatar = int(a, 16), int(b, 16)
        except (OSError, ValueError):
            self.fsys = self.avatar = 0
