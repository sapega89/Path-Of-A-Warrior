"""c.java - the MMAPI Player pool of the MP jar. SPIKE-SIMPLIFIED like SP aq.py: pygame.mixer.

WAV effects play straight from assets_mp; the menu music /snd1.mid is played with
pygame.mixer.music when the platform can (desktop SDL_mixer usually can), else silence.
"""
import pathlib

import pygame

import config
from pow.midp.media import gain


class PlayerPool:
    def __init__(self, n2, n3, bl, bl2):  # c.java:24
        self.size = n2
        self.snd = [None] * n2
        self.vol = 100
        self.cur = -1
        self.music = False
        self.ok = pygame.mixer.get_init() is not None
        if not self.ok:
            try:
                pygame.mixer.init()
                self.ok = True
            except Exception as ex:
                print("c: no audio:", ex)

    def _path(self, string):
        return pathlib.Path(config.MP_RES_ROOT) / string.lstrip("/")

    def load(self, string, n2):  # c.java  load
        if not self.ok or not 0 <= n2 < self.size:
            return False
        if string.endswith(".mid"):
            self.snd[n2] = ("mid", self._path(string))
            return True
        if self.snd[n2] is None:
            try:
                self.snd[n2] = pygame.mixer.Sound(str(self._path(string)))
            except Exception as ex:
                print("c: loading err:", ex)
                return False
        return True

    def play(self, n2, bl):  # c.java  play (bl = loop)
        if not self.ok or self.vol <= 0 or not 0 <= n2 < self.size or self.snd[n2] is None:
            return
        self.stop()
        s = self.snd[n2]
        try:
            if isinstance(s, tuple):
                pygame.mixer.music.load(str(s[1]))
                pygame.mixer.music.set_volume(gain(self.vol))
                pygame.mixer.music.play(-1 if bl else 0)
                self.music = True
            else:
                s.set_volume(gain(self.vol))
                s.play(loops=-1 if bl else 0)
            self.cur = n2
        except Exception as ex:
            print("c: play err:", ex)

    def stop(self):  # c.java  stop
        if not self.ok:
            return
        if self.cur != -1 and not isinstance(self.snd[self.cur], tuple) and self.snd[self.cur] is not None:
            self.snd[self.cur].stop()
        if self.music:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
            self.music = False
        self.cur = -1

    def set_volume(self, n2):  # c.java  volume 0..100
        self.vol = max(0, min(100, n2))
        # c.java b(Player): setLevel on the playing Player too, not only on the next one
        s = self.snd[self.cur] if 0 <= self.cur < self.size else None
        try:
            if self.music:
                pygame.mixer.music.set_volume(gain(self.vol))
            elif s is not None and not isinstance(s, tuple):
                s.set_volume(gain(self.vol))
        except Exception:
            pass

    def tick(self):  # c.java  per tick
        pass
