"""POW Multiplayer client (PHASE_9): python pyport/mp_main.py

    POW_MP_SERVER=local                  (default) the server runs inside the game
    POW_MP_SERVER=ws://localhost:28200   python -m pow_server in another terminal
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pow.midp import display, watchdog  # noqa: E402


async def main():
    display.init(headless=os.environ.get("SDL_VIDEODRIVER") == "dummy")
    import pygame
    pygame.display.set_caption("Path of a Warrior Multiplayer")
    watchdog.start()
    from pow_mp.Main import Main
    try:
        await Main().startApp()
    except BaseException:
        watchdog.log_exception()
        raise
    finally:
        watchdog.stop()


if __name__ == "__main__":
    asyncio.run(main())
