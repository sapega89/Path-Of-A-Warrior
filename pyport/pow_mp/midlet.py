"""Main.java of the MP jar - the MIDlet. Hand-written (like pow/game/Main.py).

    from pow_mp.Main import Main; await Main().startApp()
"""
import pathlib

import config


def _manifest():
    props = {}
    p = pathlib.Path(config.MP_RES_ROOT) / "META-INF" / "MANIFEST.MF"
    try:
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if ": " in line:
                k_, v = line.split(": ", 1)
                props[k_.strip()] = v.strip()
    except OSError:
        pass
    return props


def _digit_keys():
    """The number row types its own digit (the MP password and Challenge screens read 0-9).
    The single-player map puts skill slots there (phone keys 1 3 7 9 0, pow/midp/canvas.py),
    which would make "2" type a "3"."""
    import pygame
    from pow.midp.canvas import KEYMAP
    for i in range(10):
        KEYMAP[getattr(pygame, "K_%d" % i)] = 48 + i


class Midlet:
    display = None      # Display
    canvas = None      # g (the canvas)
    started = False     # started

    def __init__(self):  # Main.java:12-17
        from pow_mp import game
        _digit_keys()
        game.load()
        from pow_mp.mp_canvas import MpCanvas
        self.props = _manifest()
        self.destroyed = False
        Midlet.started = False
        Midlet.display = True
        Midlet.canvas = MpCanvas(self)

    def getAppProperty(self, key):
        return self.props.get(key)

    def destroyApp(self, bl):
        pass

    def notifyDestroyed(self):
        self.destroyed = True

    def startApp(self):  # Main.java:19-27: the game thread -> the async loop
        from pow_mp import game
        if Midlet.started:
            return None
        Midlet.started = True
        return game.run(Midlet.canvas, self)

    def pauseApp(self):
        if Midlet.canvas is not None:
            Midlet.canvas.hideNotify()
