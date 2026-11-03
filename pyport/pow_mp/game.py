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
    self.a_v()
    MpCanvas.ee = system.currentTimeMillis()
    while not self.quit_requested and not midlet.destroyed:
        MpCanvas.ee = system.currentTimeMillis()
        NetThread.tick()                                   # the network thread (h.run)
        if MpCanvas.J:
            if MpCanvas.m != -999:
                self.f_I(MpCanvas.m)
                MpCanvas.m = -999
            MpCanvas.dY = False
            self.repaint()
            self.serviceRepaints()
            await self.sleep_ms(250)
        else:
            if MpCanvas.m != -999:
                self.f_I(MpCanvas.m)
                MpCanvas.m = -999
            MpCanvas.dY = False
            self.repaint()
            self.serviceRepaints()
            if MpCanvas.b is not None:
                if (10 <= MpCanvas.cY <= 89 and MpCanvas.cY != 88 and not MpCanvas.J) or MpCanvas.cY in (1, 6, 7):
                    self.s_I(1)
                MpCanvas.b.tick_music()
            if MpCanvas.cZ == MpCanvas.cY and MpCanvas.da < 25000:
                MpCanvas.da += 1
            if MpCanvas.da >= 25000:
                MpCanvas.da = 100
            n2 = Consts.ef[MpCanvas.an] - int(system.currentTimeMillis() - MpCanvas.ee)
            await self.sleep_ms(n2 if n2 > 20 else 20)
        self.b_v()
        MpCanvas.K = True
