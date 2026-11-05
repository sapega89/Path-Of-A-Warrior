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
    display = None       # public static Display a = null;   Main.java:6
    canvas = None       # public static ag b = null;        Main.java:8
    started = False      # public static boolean c = false;  Main.java:10

    def __init__(self):
        self.props = _manifest()
        if config.CHEAT:   # PORT-EXTRA config.CHEAT: the manifest property GAMEVIL_CHEAT: TRUE
            self.props["GAMEVIL_CHEAT"] = "TRUE"
        self.destroyed = False
        self.to_multiplayer = False   # PORT-EXTRA: Main Menu > Multiplayer > YES (l.py, main.py)
        self.resume_sound = None      # PORT-EXTRA: back from the Multiplayer game (main.py): the
                                      # sound answer given before, the boot goes to the Main Menu

    def getAppProperty(self, key):
        return self.props.get(key)

    def run_game(self):  # Main.java:12-20  (returns the coroutine of the game thread)
        from pow.game.game_canvas import GameCanvas
        if Midlet.started:
            return None
        Midlet.started = True
        if GameCanvas.thread is None:
            GameCanvas.thread = Midlet.canvas.run()
        return GameCanvas.thread

    def pauseApp(self):  # Main.java:22-24
        Midlet.canvas.hideNotify()

    def destroyApp(self, paramBoolean):  # Main.java:26-29
        from pow.game.game_canvas import GameCanvas
        from pow.game.sound import Sound
        if Midlet.canvas is not None and GameCanvas.sound is not None and Sound.players is not None:
            Sound.players.close_all()

    def notifyDestroyed(self):
        from pow.game.game_canvas import GameCanvas
        self.destroyed = True
        GameCanvas.running = False

    def construct(self):  # Main.java:31-39
        from pow.game.game_canvas import GameCanvas, _late_init
        if Midlet.display is None:
            Midlet.started = False
            Midlet.display = True  # Display.getDisplay(this)
            _late_init()
            Midlet.canvas = GameCanvas(self)
            from pow.game.pointer import hold_dir, keys_for
            Midlet.canvas.pointer = keys_for   # PORT-EXTRA: mouse -> phone keys
            Midlet.canvas.hold_dir = hold_dir
            from pow.game.autopilot import Autopilot
            Autopilot.reset()
            Midlet.canvas.autopilot = Autopilot   # PORT-EXTRA: auto-hunt (config.AUTO_HUNT)
            from pow.game.skill_bar import playing
            Midlet.canvas.belt_active = playing   # PORT-EXTRA config.SKILL_BAR: Z X C V B = belt

    def startApp(self):  # Main.java:41-43  (tryNBuy_123456 -> constructor + startApp_123456)
        self.construct()
        return self.run_game()
