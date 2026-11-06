"""Glue of the multiplayer screens: the loading order, one frame, the loop of the standalone client.

The game loop is one asyncio loop (the browser needs it), so a frame is an `async` step with
one step of the network "thread" (pow/game/online/net_thread.py).
"""
import importlib

from pow.midp import system

# the JVM order (interface l = consts first)
MODS = ["consts", "draw", "gfx", "font", "answer", "frame_writer", "frame_reader", "mp_canvas", "mp_game"]
_loaded = None


def load():
    """Import the MP classes, resolve their cross references, run the static
    initializers (interface l first, as the JVM would before g uses its constants)."""
    global _loaded
    if _loaded is not None:
        return _loaded
    mods = {name: importlib.import_module("pow.game.online." + name) for name in MODS}
    for mod in mods.values():
        mod._late_imports()
    for name in MODS:
        mods[name]._static_init()
    _loaded = mods
    return mods


async def frame(self, midlet):
    """One frame: keys, paint, music, the frame's wait. False once the
    screens are over (the Exit of the main menu, or the window closed)."""
    from pow.game.online.consts import Consts
    from pow.game.online.mp_canvas import MpCanvas
    from pow.game.online.net_thread import NetThread
    if self.quit_requested or midlet.destroyed:
        return False
    MpCanvas.frame_start = system.currentTimeMillis()
    NetThread.tick()                                   # the network thread
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
        wait_ms = Consts.speed_frame_ms[MpCanvas.speed] - int(system.currentTimeMillis() - MpCanvas.frame_start)
        await self.sleep_ms(max(20, wait_ms))
    self.apply_pause()
    MpCanvas.loop_started = True
    return not (self.quit_requested or midlet.destroyed)


def close(self):
    """After the screens: the server forgets this session (it lives on), the music stops.
    -> (what the battles earned when embedded, the window was closed)."""
    from pow.game.online import sp_bridge
    from pow.game.online.mp_canvas import MpCanvas
    from pow.game.online.net_thread import NetThread
    NetThread.close()
    if MpCanvas.game is not None:
        MpCanvas.game.stop_music()     # the outro stops it; a closed window does not
    return sp_bridge.take_rewards(), self.quit_requested


async def run(self, midlet):
    """The loop of the standalone client (mp_main.py)."""
    self.init_screen()
    while await frame(self, midlet):
        pass
