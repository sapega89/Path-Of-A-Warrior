"""Entry point for the PC and for the browser (pygbag needs `asyncio.run(main())` here).

    python pyport/main.py            # window 480x640 (POW_SCALE=3 -> 720x960)
    python -m pygbag build/web       # browser, see tools/build_web.py
    POW_LIVE_SERVER=ws://host:28200/live   Gamevil Live on `python -m pow_server` (default: inside
                                     the game); browser: index.html?live=wss://host:port/live

Main Menu > Multiplayer > YES ends the single player and starts the Multiplayer game in the same
window (mp_main.play; the server choice is POW_MP_SERVER / index.html?server=...). Its Exit comes
back here: the process restarts (the browser reloads the page), so the single player begins from
a clean state, as when the phone started the other jar.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config  # noqa: E402
from pow.midp import display, watchdog  # noqa: E402


def rms_selftest():
    """Task 0.8: proves that RecordStore survives a restart / page reload.
    Uses its own store, so the game's data is not touched. Look for the line in the
    console (browser: F12): the number must grow by 1 after every reload."""
    from pow.midp.rms import RecordStore
    try:
        rs = RecordStore.openRecordStore("pow_selftest", True)
        if rs.getNumRecords() == 0:
            rs.addRecord(bytearray(4), 0, 4)
        rec = rs.getRecord(1)
        n = int.from_bytes(rec, "little") + 1
        rs.setRecord(1, bytearray(n.to_bytes(4, "little")), 0, 4)
        back = int.from_bytes(RecordStore.openRecordStore("pow_selftest", False).getRecord(1), "little")
        print("RMS selftest: launch #%d, read back %d -> %s (%s)" % (n, back, "OK" if back == n else "FAIL", sys.platform))
    except Exception as ex:
        print("RMS selftest: FAIL", repr(ex))


def demo_save():
    """SPIKE-ONLY: New Game (name entry, prologue) is a Phase 2 screen, so without a save the
    Game Menu cannot be reached. When there is no save yet, write the smallest save that
    ag.U() accepts (hero "HERO", all values 0); then Main Menu -> Continue opens the Game Menu.
    Off by default; turn on with --demo or POW_DEMO_SAVE=1. An existing save is never touched."""
    from pow.midp.rms import RecordStore
    rs = RecordStore.openRecordStore("gamevil_pow_data", True)
    if rs.getNumRecords() == 0:
        data = bytearray(965)
        data[0], data[1] = 965 & 0xFF, 965 >> 8
        data[2:10] = b"HERO    "
        rs.addRecord(data, 0, len(data))
        print("demo save created (Continue -> Game Menu)")


def live_from_page():
    """Browser: ?live=ws(s)://host:port/live in the page address picks the Gamevil Live server."""
    if sys.platform != "emscripten":
        return
    try:
        import platform
        where = platform.window.URLSearchParams.new(platform.window.location.search).get("live")
        if where:
            config.LIVE_SERVER = str(where)
            print("Gamevil Live server:", config.LIVE_SERVER)
    except Exception as ex:
        print("Gamevil Live server from the page address: %r" % ex)


def restart():
    """Back from the Multiplayer game: start the single player again from scratch."""
    if sys.platform == "emscripten":
        import platform
        platform.window.location.reload()
        return
    # a new process, not os.execv: on Windows execv does not quote its arguments, so a path with
    # a space ("C:\\Users\\Andrey S\\...") would break; a frozen exe has no main.py to pass
    import subprocess
    import pygame
    args = [sys.executable] + ([] if getattr(sys, "frozen", False) else [os.path.abspath(__file__)])
    sys.stdout.flush()
    pygame.quit()                          # the old window closes before the new one opens
    subprocess.Popen(args + sys.argv[1:])


async def main():
    live_from_page()
    display.init(headless=os.environ.get("SDL_VIDEODRIVER") == "dummy")
    watchdog.start()
    rms_selftest()
    if (config.DEMO_SAVE or "--demo" in sys.argv) and "--no-demo" not in sys.argv:
        demo_save()
    from pow.game.midlet import Midlet
    midlet = Midlet()
    try:
        await midlet.startApp()
        if midlet.to_multiplayer and not (Midlet.b is not None and Midlet.b.quit_requested):
            import mp_main
            if await mp_main.play():
                restart()
    except BaseException:
        watchdog.log_exception()
        raise
    finally:
        watchdog.stop()


if __name__ == "__main__":
    asyncio.run(main())
