"""Glue of the generated MP client (pow_mp/_gen): loading order and the async main loop.

g.run() / g.c() of the jar is a thread with Thread.sleep; the browser needs one asyncio loop,
so run() below is g.c() with `await` (same order of steps, g.java:414-469), plus one step of
the network "thread" (pow_mp/h.py) per frame.
"""
import importlib

from pow.midp import system

MODS = ["l", "f", "i", "j", "k", "e", "d", "g", "m"]
_loaded = None


def load():
    """Import the generated classes, resolve their cross references, run the static
    initializers (interface l first, as the JVM would before g uses its constants)."""
    global _loaded
    if _loaded is not None:
        return _loaded
    from pow_mp.a import a
    from pow_mp.c import c
    from pow_mp.h import h
    from pow_mp.n import n
    mods = {name: importlib.import_module("pow_mp._gen." + name) for name in MODS}
    for mod in mods.values():
        mod._late_imports()
        mod.a, mod.c, mod.h, mod.n = a, c, h, n
    for name in MODS:
        getattr(mods[name], "_static_init_" + name)()
    _loaded = mods
    return mods


async def run(self, midlet):
    """g.run() + g.c() (g.java:414-469)."""
    from pow_mp._gen.g import g
    from pow_mp._gen.l import l
    from pow_mp.h import h
    self.a_v()
    g.ee = system.currentTimeMillis()
    while not self.quit_requested and not midlet.destroyed:
        g.ee = system.currentTimeMillis()
        h.tick()                                   # the network thread (h.run)
        if g.J:
            if g.m != -999:
                self.f_I(g.m)
                g.m = -999
            g.dY = False
            self.repaint()
            self.serviceRepaints()
            await self.sleep_ms(250)
        else:
            if g.m != -999:
                self.f_I(g.m)
                g.m = -999
            g.dY = False
            self.repaint()
            self.serviceRepaints()
            if g.b is not None:
                if (10 <= g.cY <= 89 and g.cY != 88 and not g.J) or g.cY in (1, 6, 7):
                    self.s_I(1)
                g.b.ak_v()
            if g.cZ == g.cY and g.da < 25000:
                g.da += 1
            if g.da >= 25000:
                g.da = 100
            n2 = l.ef[g.an] - int(system.currentTimeMillis() - g.ee)
            await self.sleep_ms(n2 if n2 > 20 else 20)
        self.b_v()
        g.K = True
