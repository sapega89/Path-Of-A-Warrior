"""PORT-EXTRA (asked by Andrey): "No connection" before the game starts (cloud_save SERVER_ONLY).

The game starts only online. While cloud_save.boot() cannot reach the server (or the server
refused the stored login), this screen is shown instead of the game: OK / a click tries again
(and so does the screen itself every AUTO_RETRY_MS); on a refused login BACK forgets the stored
account (the registration screen then asks for it again in the game). Drawn with the game's
bitmap font (0_font.png) straight on the 240x320 screen, before GameCanvas exists.
"""
import asyncio
import time

import pygame

import config
from pow.game.font import Font
from pow.midp import display, rms

AUTO_RETRY_MS = 10000
KEYS_OK = (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_j, pygame.K_KP5)
KEYS_BACK = (pygame.K_ESCAPE, pygame.K_BACKSPACE)

_font = None


def _glyphs():
    global _font
    if _font is None:
        _font = Font("/0_font.png", 8, 17, 9, 0xFFFFFF)
    return _font


def _text(screen, text, y, font):
    w = font.string_width(text)
    x = (config.SCREEN_W - w) // 2
    for ch in text:
        if ch != " " and font.image is not None:
            sx = Font.glyph_index(ch) * font.glyph_w
            screen.blit(font.image.surface, (x, y), pygame.Rect(sx, 0, font.glyph_w, font.glyph_h))
        x += font.char_width(ch)


def lines(sync):
    """What the screen says: the server is not there, or it refused the stored login."""
    if sync.state == "off":
        return ["Login refused", "", "OK: try again", "BACK: other account"]
    return ["No connection", "to the server", "", "The game starts", "only online", "",
            "OK: try again"]


def draw(sync, trying=False):
    screen = display.screen
    screen.fill((0, 0, 0))
    font = _glyphs()
    rows = ["Connecting..."] if trying else lines(sync)
    y = (config.SCREEN_H - len(rows) * 20) // 2
    for row in rows:
        _text(screen, row, y, font)
        y += 20
    display.present()


def forget_account():
    """BACK on "Login refused": the stored UserID / password go; the game asks for an account."""
    from pow.game import cloud_save
    rms.RecordStore.deleteRecordStore(cloud_save.REGIST)


async def show(sync):
    """Until the player (or the timer) asks for another try; main.py's boot() then tries."""
    draw(sync)
    shown = time.monotonic()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                raise SystemExit
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
                display.toggle_fullscreen()
                draw(sync)
            elif ev.type == pygame.KEYDOWN and ev.key in KEYS_BACK and sync.state == "off":
                forget_account()
                sync.reachable = False
                sync.retry_now()
                draw(sync, trying=True)
                return
            elif (ev.type == pygame.KEYDOWN and ev.key in KEYS_OK) or ev.type in (
                    pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN, pygame.JOYBUTTONDOWN):
                draw(sync, trying=True)
                return
        if sync.state != "off" and (time.monotonic() - shown) * 1000 >= AUTO_RETRY_MS:
            draw(sync, trying=True)
            return
        await asyncio.sleep(0.05)
