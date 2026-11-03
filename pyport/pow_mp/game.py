"""Glue of the MP client: loading order and the async main loop.

g.run() / g.c() of the jar is a thread with Thread.sleep; the browser needs one asyncio loop,
so run() below is g.c() with `await` (same order of steps, g.java:414-469), plus one step of
the network "thread" (pow_mp/net_thread.py) per frame.
"""
import importlib

from pow.midp import system

# static initialisers in the JVM order (interface l = consts first)
MODS = ["consts", "draw", "gfx", "font", "answer", "frame_writer", "frame_reader", "mp_canvas", "mp_game"]
_loaded = None


def load():
    """Import the MP classes, resolve their cross references, run the static
    initializers (interface l first, as the JVM would before g uses its constants)."""
    global _loaded
    if _loaded is not None:
        return _loaded
    mods = {name: importlib.import_module("pow_mp." + name) for name in MODS}
    for mod in mods.values():
        mod._late_imports()
    for name in MODS:
        mods[name]._static_init()
    _loaded = mods
    return mods


async def run(self, midlet):
    """g.run() + g.c() (g.java:414-469)."""
    from pow_mp.mp_canvas import MpCanvas
    from pow_mp.consts import Consts
    from pow_mp.net_thread import NetThread
    self.init_screen()
    MpCanvas.frame_start = system.currentTimeMillis()
    while not self.quit_requested and not midlet.destroyed:
        MpCanvas.frame_start = system.currentTimeMillis()
        NetThread.tick()                                   # the network thread (h.run)
        if MpCanvas.paused:
            if MpCanvas.key != -999:
                self.handle_key(MpCanvas.key)
                MpCanvas.key = -999
            MpCanvas.painted = False
            self.repaint()
            self.serviceRepaints()
            await self.sleep_ms(250)
        else:
            if MpCanvas.key != -999:
                self.handle_key(MpCanvas.key)
                MpCanvas.key = -999
            MpCanvas.painted = False
            self.repaint()
            self.serviceRepaints()
            if MpCanvas.game is not None:
                if (10 <= MpCanvas.state <= 89 and MpCanvas.state != 88 and not MpCanvas.paused) or MpCanvas.state in (1, 6, 7):
                    self.start_music(1)
                MpCanvas.game.tick_music()
            if MpCanvas.prev_state == MpCanvas.state and MpCanvas.state_ticks < 25000:
                MpCanvas.state_ticks += 1
            if MpCanvas.state_ticks >= 25000:
                MpCanvas.state_ticks = 100
            n2 = Consts.ef[MpCanvas.speed] - int(system.currentTimeMillis() - MpCanvas.frame_start)
            await self.sleep_ms(n2 if n2 > 20 else 20)
        self.apply_pause()
        MpCanvas.K = True
