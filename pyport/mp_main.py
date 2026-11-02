"""POW Multiplayer client (PHASE_9): python pyport/mp_main.py

    POW_MP_SERVER=local                  (default) the server runs inside the game
    POW_MP_SERVER=ws://localhost:28200   python -m pow_server in another terminal
    browser (tools/build_web.py --mp): index.html?server=wss://host:port, the same choice
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pow.midp import display, watchdog  # noqa: E402


def server_from_page():
    """Browser: ?server=ws(s)://host:port in the page address picks the server."""
    if sys.platform != "emscripten":
        return
    try:
        import platform
        import config
        where = platform.window.URLSearchParams.new(platform.window.location.search).get("server")
        if where:
            config.MP_SERVER = str(where)
            print("POW MP server:", config.MP_SERVER)
    except Exception as ex:
        print("POW MP server from the page address: %r" % ex)


async def play():
    """Runs the Multiplayer game on an open display. Returns True when it ended with its own
    Exit (main.py then goes back to the single player), False when the window was closed."""
    server_from_page()
    import pygame
    pygame.display.set_caption("Path of a Warrior Multiplayer")
    from pow_mp.Main import Main
    midlet = Main()
    await midlet.startApp()
    return not Main.b.quit_requested


async def main():
    display.init(headless=os.environ.get("SDL_VIDEODRIVER") == "dummy")
    watchdog.start()
    try:
        await play()
    except BaseException:
        watchdog.log_exception()
        raise
    finally:
        watchdog.stop()


if __name__ == "__main__":
    asyncio.run(main())
