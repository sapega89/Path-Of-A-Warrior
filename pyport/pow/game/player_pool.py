"""aq.java - Player pool. SPIKE-SIMPLIFIED (literal port = PHASE_1 task 1.5).

Same public methods as aq.java, implemented with pygame.mixer:
  /sndN.mid and /sndN.wav are played from pyport/assets/audio/sndN.ogg
  (made by tools/convert_audio.py; MIDI is rendered with FluidSynth + FluidR3_GM).
"""
import pathlib

import pygame

from pow.midp.media import gain

AUDIO = pathlib.Path(__file__).resolve().parents[2] / "assets" / "audio"


class PlayerPool:
    def __init__(self, count, unused_count, unused_flag, unused_flag2):  # aq.java:40-54
        self.count = count
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

    def close_all(self):  # aq.java:75-78  close all
        for b in range(self.count):
            self.players[b] = None

    def load(self, path, index):  # aq.java:177-179  load
        if not self.ok or self.players[index] is not None:
            return self.players[index] is not None
        name = pathlib.Path(path).stem + ".ogg"
        try:
            self.players[index] = pygame.mixer.Sound(str(AUDIO / name))
            return True
        except Exception as ex:
            print("loading err:", ex)
            return False

    def play(self, index, loop):  # aq.java:88-95  play
        if index < 0 or self.volume <= 0 or not self.ok or self.players[index] is None:
            return
        self.looping = index if loop else -1
        self.stop_current()
        snd = self.players[index]
        snd.set_volume(gain(self.volume))
        snd.play(loops=-1 if loop else 0)
        self.playing = index

    def stop(self):  # aq.java:216-221  stop
        self.looping = -1
        self.stop_current()

    def stop_current(self):  # aq.java:223-235
        if self.playing != -1 and self.players[self.playing] is not None:
            self.players[self.playing].stop()

    def set_volume(self, volume):  # aq.java:242-247  volume
        if 0 <= volume <= 100:
            self.volume = volume
        if self.playing != -1 and self.players[self.playing] is not None:
            self.players[self.playing].set_volume(gain(self.volume))

    def pause(self):  # aq.java:260-269  hideNotify
        self.paused = True
        self.stop_current()
        self.playing = -1

    def resume(self):  # aq.java:271-276  showNotify
        self.paused = False
        if self.looping != -1:
            self.play(self.looping, True)

    def tick(self):  # aq.java:278-290  per tick (re-start after endOfMedia) - not needed with loops=-1
        pass
