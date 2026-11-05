"""Entry point for the PC and for the browser (pygbag needs `asyncio.run(main())` here).

    python pyport/main.py            # window 480x640 (POW_SCALE=3 -> 720x960)
    python -m pygbag build/web       # browser, see tools/build_web.py
    POW_LIVE_SERVER=ws://host:28200/live   Gamevil Live on `python -m pow_server` (default: inside
                                     the game); browser: index.html?live=wss://host:port/live
    POW_SAVE_SERVER=auto                 the save also kept on that server (path /save) for the
                                     Gamevil Live account; off / ws(s)://host:port/save;
                                     browser: index.html?save=...

Main Menu > Multiplayer > YES ends the single player and starts the Multiplayer game in the same
window and process (mp_main.play; the server choice is POW_MP_SERVER / index.html?server=...),
without its logo and sound question. Its Exit comes back here: the single player starts again
from a clean state (its modules are imported anew, as when the phone started the other jar), but
straight at the Main Menu: no logo, sound question or title, no new process or page reload.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from pow.midp import display, watchdog


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
        from urllib.parse import parse_qs
        # parsed here: pygbag's JS bridge has no URLSearchParams.new(...)
        params = parse_qs(str(platform.window.location.search).lstrip("?"))
        where = params.get("live", [""])[0]
        if where:
            config.LIVE_SERVER = where
            print("Gamevil Live server:", config.LIVE_SERVER)
        save = params.get("save", [""])[0]
        if save:
            config.SAVE_SERVER = save
    except Exception as ex:
        print(f"Gamevil Live server from the page address: {ex!r}")


# the modules whose state lives on between the games: the server saves (their background task)
# and the transports (the in-game server with its accounts, pow_mp/net/transport.py)
_KEEP = ("pow.game.cloud_save", "pow_mp.net", "pow_mp.net.transport")


def fresh_games():
    """PORT-EXTRA: forget the single-player and Multiplayer modules, so that the next Midlet
    starts with the static fields of a new JVM (what the process restart used to give)."""
    kept = {m: sys.modules[m] for m in _KEEP if m in sys.modules}
    for m in list(sys.modules):
        if m in ("pow.game", "pow_mp") or m.startswith(("pow.game.", "pow_mp.")):
            del sys.modules[m]
    sys.modules.update(kept)
    import importlib
    for name, mod in kept.items():         # `from pow.game import cloud_save` finds the kept one
        parent, _, leaf = name.rpartition(".")
        setattr(importlib.import_module(parent), leaf, mod)


async def main():
    live_from_page()
    display.init(headless=os.environ.get("SDL_VIDEODRIVER") == "dummy")
    watchdog.start()
    rms_selftest()
    if (config.DEMO_SAVE or "--demo" in sys.argv) and "--no-demo" not in sys.argv:
        demo_save()
    from pow.game import cloud_save, offline_screen
    # PORT-EXTRA: a newer save of this account from the server, before the hero is loaded;
    # server only: the game starts only online ("No connection" until it is)
    await cloud_save.boot(offline_screen=offline_screen.show)
    resume_sound = None                    # None: the boot asks; True / False: straight to the menu
    try:
        while True:
            from pow.game.game_canvas import GameCanvas
            from pow.game.midlet import Midlet
            if cloud_save.sync is not None:  # a newer hero taken during the Multiplayer game:
                cloud_save.sync.restart_requested = False   # the game below loads it anyway
            midlet = Midlet()
            midlet.resume_sound = resume_sound
            await midlet.startApp()
            await cloud_save.flush()
            if Midlet.canvas is not None and Midlet.canvas.quit_requested:
                break                      # the window was closed
            if cloud_save.sync is not None and cloud_save.sync.restart_requested:
                pass                       # the server's hero replaced the one in memory: load it
            elif midlet.to_multiplayer:
                import mp_main
                from pow.midp import canvas
                keymap = dict(canvas.KEYMAP)                 # the MP number row types digits
                if not await mp_main.play(sound_on=GameCanvas.sound_on):
                    break
                canvas.KEYMAP.clear()
                canvas.KEYMAP.update(keymap)
            else:
                break                      # its own Exit
            # the sound question answered (state 0 = the boot screens): not asked again
            resume_sound = GameCanvas.sound_on if GameCanvas.state != 0 else resume_sound
            fresh_games()
    except BaseException:
        watchdog.log_exception()
        raise
    finally:
        watchdog.stop()


if __name__ == "__main__":
    asyncio.run(main())
