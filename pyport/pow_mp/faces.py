"""PORT-EXTRA: pictures of the MP client for the heroes 4..9 of the single player
(pow/game/heroes.py), made at load time from pictures that already exist; nothing is drawn new.

- /face4.png .. /face9.png: the HUD face strip of a fighter (g.m(): 41x12, the left half is
  drawn for the fighter on the left, the right half for the one on the right). The jar has
  face0..3 for the 4 heroes; here the strip is the eyes band of the hero's portrait jang_N
  (single-player resources, config.RES_ROOT), scaled down, and mirrored in the left half so
  that both look at the opponent.
- /act24.png .. /act35.png: the face panel of the fighter whose turn it is (86x19, two 43x19
  halves like the strip). The jar has act6..9 (normal) and act12..15 (attacking) for faces 0..3
  at act 6 + face and 12 + face; 10, 11, 16, 17 belong to the CPU fighter and the monster, so
  the heroes 4..9 use ACT_BASE + face (24..29) and ACT_BASE + 6 + face (30..35) instead (g.m()
  switch on ca[], pow_mp/_gen/g.py: cD = face + 14). The panel is the portrait's own pixels
  around the eyes, not scaled.
- /sprhead5.png .. /sprhead10.png: the jar ships the upper bodies of the generals (sprhead5..10
  = g_head1..6, all animations) only as *_r.png, the copy used for the fighter on the right; the
  same picture serves the left side too (sprhead1..4 and sprhead1..4_r look the same).
"""
import pathlib
import re
import struct
import zlib

import config

FACE_W, FACE_H = 20, 12          # one half of the strip
CROP = (5, 5, 41, 27)            # eyes band of a 46x46 portrait (x0, y0, x1, y1)

ACT_BASE = 20                    # act<ACT_BASE + face>: normal, act<ACT_BASE + 6 + face>: attacking
ACT_CROP = (2, 9, 45, 28)        # 43x19 around the eyes of a 46x46 portrait

_ACT = re.compile(r"^/?act(\d+)\.png$")
_FACE = re.compile(r"^/?face(\d+)\.png$")
_SPRHEAD = re.compile(r"^/?sprhead(\d+)\.png$")


def _png(w, h, rgba):
    """Minimal PNG encoder (RGBA, 8 bit), so that the picture goes through Image.createImage."""
    raw = b"".join(b"\0" + bytes(rgba[y * w * 4:(y + 1) * w * 4]) for y in range(h))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def face_strip(portrait_path):
    """PNG bytes of the 41x12 face strip from a 46x46 portrait."""
    import pygame
    src = pygame.image.load(str(portrait_path))
    x0, y0, x1, y1 = CROP
    band = pygame.Surface((x1 - x0, y1 - y0), pygame.SRCALPHA, 32)   # 32 bit for smoothscale
    band.blit(src, (0, 0), (x0, y0, x1 - x0, y1 - y0))
    thumb = pygame.transform.smoothscale(band, (FACE_W, FACE_H))
    strip = pygame.Surface((2 * FACE_W + 1, FACE_H), pygame.SRCALPHA, 32)
    strip.fill((0, 0, 0, 255))
    strip.blit(pygame.transform.flip(thumb, True, False), (0, 0))
    strip.blit(thumb, (FACE_W + 1, 0))
    w, h = strip.get_size()
    rgba = pygame.image.tobytes(strip, "RGBA")
    return _png(w, h, rgba)


def act_panel(portrait_path):
    """PNG bytes of the 86x19 face panel from a 46x46 portrait."""
    import pygame
    src = pygame.image.load(str(portrait_path))
    x0, y0, x1, y1 = ACT_CROP
    w, h = x1 - x0, y1 - y0
    half = pygame.Surface((w, h), pygame.SRCALPHA, 32)
    half.blit(src, (0, 0), (x0, y0, w, h))
    panel = pygame.Surface((2 * w, h), pygame.SRCALPHA, 32)
    panel.blit(pygame.transform.flip(half, True, False), (0, 0))
    panel.blit(half, (w, 0))
    return _png(2 * w, h, pygame.image.tobytes(panel, "RGBA"))


def _portrait(face):
    from pow.game import heroes
    p = pathlib.Path(config.RES_ROOT) / ("jang_%d.png" % heroes.portrait_index(face))
    return p if p.exists() else None


def read(name):
    """Bytes of a picture this module makes, or None for any other name."""
    m = _FACE.match(name)
    if m and 4 <= int(m.group(1)) < 10:
        p = _portrait(int(m.group(1)))
        return face_strip(p) if p else None
    m = _ACT.match(name)
    if m and ACT_BASE + 4 <= int(m.group(1)) < ACT_BASE + 16:
        k = int(m.group(1)) - ACT_BASE
        p = _portrait(k if k < 10 else k - 6)
        return act_panel(p) if p else None
    m = _SPRHEAD.match(name)
    if m and 5 <= int(m.group(1)) <= 10:
        p = pathlib.Path(config.MP_RES_ROOT) / ("sprhead%s_r.png" % m.group(1))
        return p.read_bytes() if p.exists() else None
    return None
