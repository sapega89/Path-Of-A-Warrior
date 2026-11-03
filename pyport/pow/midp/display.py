"""The phone screen: one 240x320 surface, shown in a window scaled by an integer factor.

Headless mode (SDL_VIDEODRIVER=dummy) is used by tools/shot.py and tests.

PORT-EXTRA full screen (F11 / Alt+Enter, Options > Screen): the 240x320 picture is scaled by the
biggest whole factor that fits the monitor and centred, with black bars around it. The choice is
kept in RecordStore "pow_display" and comes back on the next start. In the browser the page itself
goes full screen (Fullscreen API) and pygbag fits the canvas into it.
"""
import os
import sys

import pygame

import config

screen = None      # pygame.Surface 240x320 - what the game draws on
window = None      # the real window (scaled)
frame_hooks = []   # callables(screen) after every painted frame (screenshots, tests)
fullscreen = False
view = None        # pygame.Rect of the window where the 240x320 picture is shown
_clear = True      # paint the black bars once after the window changed

STORE = "pow_display"


def init(headless=False):
    global screen
    if headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    pygame.init()
    want = config.FULLSCREEN if config.FULLSCREEN is not None else _load()
    _set_mode(bool(want) and not headless and not _browser())
    pygame.display.set_caption("Path of a Warrior")
    screen = pygame.Surface((config.SCREEN_W, config.SCREEN_H)).convert()
    screen.fill((0, 0, 0))


def _browser():
    return sys.platform == "emscripten"


def _set_mode(full):
    global window, fullscreen, view, _clear
    w, h = config.SCREEN_W * config.SCALE, config.SCREEN_H * config.SCALE
    if full:
        try:
            window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        except pygame.error as ex:
            print("full screen failed: %r" % ex)
            full = False
    if not full:
        window = pygame.display.set_mode((w, h))
    fullscreen = full
    view = fit(window.get_size())
    _clear = True


def fit(size):
    """Where the 240x320 picture goes in a window of `size`: the biggest whole scale, centred."""
    ww, wh = size
    s = max(1, min(ww // config.SCREEN_W, wh // config.SCREEN_H))
    w, h = config.SCREEN_W * s, config.SCREEN_H * s
    return pygame.Rect((ww - w) // 2, (wh - h) // 2, w, h)


def is_fullscreen():
    if _browser():
        try:
            import platform
            return bool(platform.window.document.fullscreenElement)
        except Exception:
            return False
    return fullscreen


def set_fullscreen(full):
    """Turns full screen on or off and remembers the choice."""
    full = bool(full)
    if _browser():
        try:
            import platform
            doc = platform.window.document
            if full and not doc.fullscreenElement:
                doc.documentElement.requestFullscreen()
            elif not full and doc.fullscreenElement:
                doc.exitFullscreen()
        except Exception as ex:
            print("Fullscreen API: %r" % ex)
        return
    if window is not None and full != fullscreen:
        _set_mode(full)
    _save(full)


def toggle_fullscreen():
    set_fullscreen(not is_fullscreen())


def _load():
    from pow.midp.rms import RecordStore
    try:
        rs = RecordStore.openRecordStore(STORE, False)
        if rs is not None and rs.getNumRecords() > 0:
            return rs.getRecord(1)[0] == 1
    except Exception:
        pass
    return False


def _save(full):
    from pow.midp.rms import RecordStore
    try:
        rs = RecordStore.openRecordStore(STORE, True)
        data = bytearray([1 if full else 0])
        if rs.getNumRecords() == 0:
            rs.addRecord(data, 0, 1)
        else:
            rs.setRecord(1, data, 0, 1)
    except Exception as ex:
        print("pow_display: %r" % ex)


def to_screen(pos):
    """Window pixel -> pixel of the 240x320 screen (clamped to it)."""
    if window is None or view is None:
        return pos
    x = (pos[0] - view.x) * config.SCREEN_W // max(1, view.w)
    y = (pos[1] - view.y) * config.SCREEN_H // max(1, view.h)
    return min(max(x, 0), config.SCREEN_W - 1), min(max(y, 0), config.SCREEN_H - 1)


def present():
    global view, _clear
    for hook in frame_hooks:
        hook(screen)
    if window is not None:
        size = window.get_size()
        if view is None or (view.right > size[0] or view.bottom > size[1]):
            view = fit(size)
            _clear = True
        if _clear:
            window.fill((0, 0, 0))
            _clear = False
        if view.size == screen.get_size():
            window.blit(screen, view.topleft)
        else:
            pygame.transform.scale(screen, view.size, window.subsurface(view))  # nearest neighbour
        pygame.display.flip()
