"""aq.java - Player pool. SPIKE-SIMPLIFIED (literal port = PHASE_1 task 1.5).

Same public methods as aq.java, implemented with pygame.mixer:
  /sndN.mid and /sndN.wav are played from pyport/assets/audio/sndN.ogg
  (made by tools/convert_audio.py; MIDI is rendered with FluidSynth + FluidR3_GM).
"""
import pathlib

import pygame

AUDIO = pathlib.Path(__file__).resolve().parents[2] / "assets" / "audio"


class aq:
    def __init__(self, paramInt1, paramInt2, paramBoolean1, paramBoolean2):  # aq.java:40-54
        self.e = paramInt1
        self.a = [None] * self.e      # Player[] -> pygame Sound
        self.j = 100                  # volume 0..100
        self.n = -1                   # playing index
        self.p = -1                   # looping index (resumed by d())
        self.c = False
        self.ok = pygame.mixer.get_init() is not None
        if not self.ok:
            try:
                pygame.mixer.init()
                self.ok = True
            except Exception as ex:
                print("aq: no audio:", ex)

    def a_v(self):  # aq.java:75-78  close all
        for b in range(self.e):
            self.a[b] = None

    def a_TI(self, paramString, paramInt):  # aq.java:177-179  load
        if not self.ok or self.a[paramInt] is not None:
            return self.a[paramInt] is not None
        name = pathlib.Path(paramString).stem + ".ogg"
        try:
            self.a[paramInt] = pygame.mixer.Sound(str(AUDIO / name))
            return True
        except Exception as ex:
            print("loading err:", ex)
            return False

    def a_IZ(self, paramInt, paramBoolean):  # aq.java:88-95  play
        if paramInt < 0 or self.j <= 0 or not self.ok or self.a[paramInt] is None:
            return
        self.p = paramInt if paramBoolean else -1
        self.g()
        snd = self.a[paramInt]
        snd.set_volume(self.j / 100.0)
        snd.play(loops=-1 if paramBoolean else 0)
        self.n = paramInt

    def b_v(self):  # aq.java:216-221  stop
        self.p = -1
        self.g()

    def g(self):  # aq.java:223-235
        if self.n != -1 and self.a[self.n] is not None:
            self.a[self.n].stop()

    def a_I(self, paramInt):  # aq.java:242-247  volume
        if 0 <= paramInt <= 100:
            self.j = paramInt
        if self.n != -1 and self.a[self.n] is not None:
            self.a[self.n].set_volume(self.j / 100.0)

    def c_v(self):  # aq.java:260-269  hideNotify
        self.c = True
        self.g()
        self.n = -1

    def d_v(self):  # aq.java:271-276  showNotify
        self.c = False
        if self.p != -1:
            self.a_IZ(self.p, True)

    def e_v(self):  # aq.java:278-290  per tick (re-start after endOfMedia) - not needed with loops=-1
        pass
