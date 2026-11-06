"""The sound player pool of the multiplayer screens, on pygame.mixer.

WAV effects play straight from assets_mp; the menu music /snd1.mid is played with
pygame.mixer.music when the platform can (desktop SDL_mixer usually can), else silence.
the browser build has no WAV (pygbag refuses to pack them, tools/build_web.py
leaves them out): there the effect is the OGG next to it (assets_mp/sndN.ogg, made by
tools/convert_audio.py).
"""
import pathlib

import pygame

import config
from pow.midp.media import gain


class PlayerPool:
    def __init__(self, size, unused_count, unused_flag, unused_flag2):
        self.size = size
        self.snd = [None] * size
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

    @staticmethod
    def _path(name):
        path = pathlib.Path(config.MP_RES_ROOT) / name.lstrip("/")
        ogg = path.with_suffix(".ogg")
        if path.suffix == ".wav" and not path.exists() and ogg.exists():
            return ogg                     # the browser build (see the docstring)
        return path

    def load(self, name, index):  # load
        if not self.ok or not 0 <= index < self.size:
            return False
        if name.endswith(".mid"):
            self.snd[index] = ("mid", self._path(name))
            return True
        if self.snd[index] is None:
            try:
                self.snd[index] = pygame.mixer.Sound(str(self._path(name)))
            except Exception as ex:
                print("c: loading err:", ex)
                return False
        return True

    def play(self, index, loop):  # play (bl = loop)
        if not self.ok or self.vol <= 0 or not 0 <= index < self.size or self.snd[index] is None:
            return
        self.stop()
        s = self.snd[index]
        try:
            if isinstance(s, tuple):
                pygame.mixer.music.load(str(s[1]))
                pygame.mixer.music.set_volume(gain(self.vol))
                pygame.mixer.music.play(-1 if loop else 0)
                self.music = True
            else:
                s.set_volume(gain(self.vol))
                s.play(loops=-1 if loop else 0)
            self.cur = index
        except Exception as ex:
            print("c: play err:", ex)

    def stop(self):  # stop
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

    def set_volume(self, volume):  # volume 0..100
        self.vol = max(0, min(100, volume))
        # b(Player): setLevel on the playing Player too, not only on the next one
        s = self.snd[self.cur] if 0 <= self.cur < self.size else None
        try:
            if self.music:
                pygame.mixer.music.set_volume(gain(self.vol))
            elif s is not None and not isinstance(s, tuple):
                s.set_volume(gain(self.vol))
        except Exception:
            pass

    def tick(self):  # per tick
        pass
