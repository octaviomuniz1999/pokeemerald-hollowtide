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
    def __init__(self, rom):
        self.emu = DeSmuME()
        self.emu.open(rom)
        self.emu.volume_set(0)
        self.fsys = 0
        self.avatar = 0
        mem = self.emu.memory
        def on_flag(addr, size):
            self.fsys = mem.register_arm9.r0
        def on_getx(addr, size):
            self.avatar = mem.register_arm9.r0
        mem.register_exec(FLAGCHECK, on_flag)
        mem.register_exec(GETX, on_getx)

    def wait(self, n):
        for _ in range(n):
            self.emu.cycle(with_joystick=False)

    def press(self, key, hold=6, after=20):
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
        if not (self.fsys and self.avatar):
            return None
        loc = self.u32(self.fsys + 0x20)
        obj = self.u32(self.avatar + 0x30)
        if not (0x02000000 <= loc < 0x02400000 and 0x02000000 <= obj < 0x02400000):
            return None
        return (self.u32(loc), self.u32(obj + 0x64), self.u32(obj + 0x6C))

    def shot(self, path):
        self.emu.screenshot().save(path)

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
