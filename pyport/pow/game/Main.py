"""Main.java - the MIDlet. Literal port (the com.movaya try&buy wrapper is not ported)."""
import pathlib

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


class Main:
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
        from pow.game.ag import ag
        if Main.c:
            return None
        Main.c = True
        if ag.bt is None:
            ag.bt = Main.b.run()
        return ag.bt

    def pauseApp(self):  # Main.java:22-24
        Main.b.hideNotify()

    def destroyApp(self, paramBoolean):  # Main.java:26-29
        from pow.game.ag import ag
        from pow.game.k import k
        if Main.b is not None and ag.bg is not None and k.a is not None:
            k.a.a_v()

    def notifyDestroyed(self):
        from pow.game.ag import ag
        self.destroyed = True
        ag.gh = False

    def constructor_123456(self):  # Main.java:31-39
        from pow.game.ag import ag, _late_init
        if Main.a is None:
            Main.c = False
            Main.a = True  # Display.getDisplay(this)
            _late_init()
            Main.b = ag(self)
            from pow.game.pointer import hold_dir, keys_for
            Main.b.pointer = keys_for   # PORT-EXTRA: mouse -> phone keys
            Main.b.hold_dir = hold_dir

    def startApp(self):  # Main.java:41-43  (tryNBuy_123456 -> constructor + startApp_123456)
        self.constructor_123456()
        return self.startApp_123456()
