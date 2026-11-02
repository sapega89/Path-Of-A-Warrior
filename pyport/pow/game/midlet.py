"""Main.java - the MIDlet. Literal port (the com.movaya try&buy wrapper is not ported)."""

import config
from pow.midp import resources


def _manifest():
    props = {}
    p = resources.root() / "META-INF" / "MANIFEST.MF"
    try:
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if ": " in line:
                k_, v = line.split(": ", 1)
                props[k_.strip()] = v.strip()
    except OSError:
        pass
    return props


class Midlet:
    a = None       # public static Display a = null;   Main.java:6
    b = None       # public static ag b = null;        Main.java:8
    c = False      # public static boolean c = false;  Main.java:10

    def __init__(self):
        self.props = _manifest()
        if config.CHEAT:   # PORT-EXTRA config.CHEAT: the manifest property GAMEVIL_CHEAT: TRUE
            self.props["GAMEVIL_CHEAT"] = "TRUE"
        self.destroyed = False
        self.to_multiplayer = False   # PORT-EXTRA: Main Menu > Multiplayer > YES (l.py, main.py)

    def getAppProperty(self, key):
        return self.props.get(key)

    def startApp_123456(self):  # Main.java:12-20  (returns the coroutine of the game thread)
        from pow.game.game_canvas import GameCanvas
        if Midlet.c:
            return None
        Midlet.c = True
        if GameCanvas.bt is None:
            GameCanvas.bt = Midlet.b.run()
        return GameCanvas.bt

    def pauseApp(self):  # Main.java:22-24
        Midlet.b.hideNotify()

    def destroyApp(self, paramBoolean):  # Main.java:26-29
        from pow.game.game_canvas import GameCanvas
        from pow.game.sound import Sound
        if Midlet.b is not None and GameCanvas.bg is not None and Sound.a is not None:
            Sound.a.a_v()

    def notifyDestroyed(self):
        from pow.game.game_canvas import GameCanvas
        self.destroyed = True
        GameCanvas.gh = False

    def constructor_123456(self):  # Main.java:31-39
        from pow.game.game_canvas import GameCanvas, _late_init
        if Midlet.a is None:
            Midlet.c = False
            Midlet.a = True  # Display.getDisplay(this)
            _late_init()
            Midlet.b = GameCanvas(self)
            from pow.game.pointer import hold_dir, keys_for
            Midlet.b.pointer = keys_for   # PORT-EXTRA: mouse -> phone keys
            Midlet.b.hold_dir = hold_dir

    def startApp(self):  # Main.java:41-43  (tryNBuy_123456 -> constructor + startApp_123456)
        self.constructor_123456()
        return self.startApp_123456()
