"""POW Multiplayer client (PHASE_9): python pyport/mp_main.py

    POW_MP_SERVER=local                  (default) the server runs inside the game
    POW_MP_SERVER=ws://localhost:28200   python -m pow_server in another terminal
    browser (tools/build_web.py --mp): index.html?server=wss://host:port, the same choice
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pow.midp import display, watchdog


def server_from_page():
    """Browser: ?server=ws(s)://host:port in the page address picks the server."""
    if sys.platform != "emscripten":
        return
    try:
        import platform
        from urllib.parse import parse_qs

        import config
        # parsed here: pygbag's JS bridge has no URLSearchParams.new(...)
        where = parse_qs(str(platform.window.location.search).lstrip("?")).get("server", [""])[0]
        if where:
            config.MP_SERVER = str(where)
            print("POW MP server:", config.MP_SERVER)
    except Exception as ex:
        print(f"POW MP server from the page address: {ex!r}")


async def play(sound_on=None, embedded=False):
    """Runs the Multiplayer game on an open display. Returns True when it ended with its own
    Exit (main.py then goes back to the single player), False when the window was closed.
    sound_on: the single player's answer to "sound enabled?" (main.py), so the Multiplayer
    game skips its logo and asks nothing; None = its own logo and question.
    embedded: a part of the single player (Gamevil Live > Multiplayer): no exit popup and no
    outro, and the rewards of the battles wait in memory (take_rewards) for its hero."""
    server_from_page()
    import pygame
    pygame.display.set_caption("Path of a Warrior Multiplayer")
    from pow.game.online import sp_bridge
    from pow.game.online.midlet import Midlet
    from pow.game.online.mp_canvas import MpCanvas
    from pow.game.online.net_thread import NetThread
    MpCanvas.sound_from_sp = sound_on
    MpCanvas.embedded = sp_bridge.embedded = embedded
    midlet = Midlet()
    try:
        await midlet.startApp()
    finally:
        NetThread.close()                  # the server forgets this session (it lives on)
        if MpCanvas.game is not None:
            MpCanvas.game.stop_music()     # the outro stops it; a closed window does not
        pygame.display.set_caption("Path of a Warrior")
    return not Midlet.canvas.quit_requested


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
