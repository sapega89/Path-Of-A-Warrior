"""(asked by Andrey): "No connection" before the game starts (cloud_save SERVER_ONLY).

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
from pow.midp import canvas, display, rms

AUTO_RETRY_MS = 10000
KEYS_OK = (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_j, pygame.K_KP5)
KEYS_BACK = (pygame.K_ESCAPE, pygame.K_BACKSPACE)

_font = None
_pads = []              # the joysticks opened for their button events


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


def _keys():
    """(config.KEY_HINTS): the OK / BACK keys of the device last used."""
    if not config.KEY_HINTS:
        return "OK", "BACK"
    return ("A", "B") if canvas.input_source == "gamepad" else ("ENTER", "ESC")


def lines(sync):
    """What the screen says: the server is not there, or it refused the stored login."""
    ok, back = _keys()
    if sync.state == "off":
        return ["Login refused", "", ok + ": try again", back + ": other account"]
    return ["No connection", "to the server", "", "The game starts", "only online", "",
            ok + ": try again"]


def _open_pads():
    """a pad sends its button events only once opened (GameCanvas does it later)."""
    if not config.GAMEPAD or _pads:
        return
    try:
        if not pygame.joystick.get_init():
            pygame.joystick.init()
        for index in range(pygame.joystick.get_count()):
            _pads.append(pygame.joystick.Joystick(index))
    except Exception as ex:
        print(f"offline screen: gamepad {ex!r}")


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
    _open_pads()
    draw(sync)
    shown = time.monotonic()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                raise SystemExit
            if ev.type in (pygame.KEYDOWN, pygame.JOYBUTTONDOWN):   # config.KEY_HINTS
                source = "keyboard" if ev.type == pygame.KEYDOWN else "gamepad"
                if source != canvas.input_source:
                    canvas.input_source = source
                    draw(sync)
            back = (ev.type == pygame.KEYDOWN and ev.key in KEYS_BACK) or (
                ev.type == pygame.JOYBUTTONDOWN and ev.button == 1)     # B of the pad
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
                display.toggle_fullscreen()
                draw(sync)
            elif back and sync.state == "off":
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
