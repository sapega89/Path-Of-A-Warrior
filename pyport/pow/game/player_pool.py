"""aq.java - Player pool. SPIKE-SIMPLIFIED (literal port = PHASE_1 task 1.5).

Same public methods as aq.java, implemented with pygame.mixer:
  /sndN.mid and /sndN.wav are played from pyport/assets/audio/sndN.ogg
  (made by tools/convert_audio.py; MIDI is rendered with FluidSynth + FluidR3_GM).
"""
import pathlib

import pygame

AUDIO = pathlib.Path(__file__).resolve().parents[2] / "assets" / "audio"


class PlayerPool:
    def __init__(self, paramInt1, paramInt2, paramBoolean1, paramBoolean2):  # aq.java:40-54
        self.count = paramInt1
        self.players = [None] * self.count      # Player[] -> pygame Sound
        self.volume = 100                  # volume 0..100
        self.playing = -1                   # playing index
        self.looping = -1                   # looping index (resumed by d())
        self.paused = False
        self.ok = pygame.mixer.get_init() is not None
        if not self.ok:
            try:
                pygame.mixer.init()
                self.ok = True
            except Exception as ex:
                print("aq: no audio:", ex)

    def a_v(self):  # aq.java:75-78  close all
        for b in range(self.count):
            self.players[b] = None

    def a_TI(self, paramString, paramInt):  # aq.java:177-179  load
        if not self.ok or self.players[paramInt] is not None:
            return self.players[paramInt] is not None
        name = pathlib.Path(paramString).stem + ".ogg"
        try:
            self.players[paramInt] = pygame.mixer.Sound(str(AUDIO / name))
            return True
        except Exception as ex:
            print("loading err:", ex)
            return False

    def a_IZ(self, paramInt, paramBoolean):  # aq.java:88-95  play
        if paramInt < 0 or self.volume <= 0 or not self.ok or self.players[paramInt] is None:
            return
        self.looping = paramInt if paramBoolean else -1
        self.g()
        snd = self.players[paramInt]
        snd.set_volume(self.volume / 100.0)
        snd.play(loops=-1 if paramBoolean else 0)
        self.playing = paramInt

    def b_v(self):  # aq.java:216-221  stop
        self.looping = -1
        self.g()

    def g(self):  # aq.java:223-235
        if self.playing != -1 and self.players[self.playing] is not None:
            self.players[self.playing].stop()

    def a_I(self, paramInt):  # aq.java:242-247  volume
        if 0 <= paramInt <= 100:
            self.volume = paramInt
        if self.playing != -1 and self.players[self.playing] is not None:
            self.players[self.playing].set_volume(self.volume / 100.0)

    def c_v(self):  # aq.java:260-269  hideNotify
        self.paused = True
        self.g()
        self.playing = -1

    def d_v(self):  # aq.java:271-276  showNotify
        self.paused = False
        if self.looping != -1:
            self.a_IZ(self.looping, True)

    def e_v(self):  # aq.java:278-290  per tick (re-start after endOfMedia) - not needed with loops=-1
        pass
