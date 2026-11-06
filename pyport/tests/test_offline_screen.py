"""the "No connection" screen of the server-only save (pow/game/offline_screen.py)."""
import asyncio

import pygame

from pow.game import offline_screen
from pow.midp import display


class Sync:
    def __init__(self, state):
        self.state = state
        self.reachable = False
        self.retries = 0

    def retry_now(self):
        self.retries += 1


def lit(screen):
    return sum(1 for x in range(0, 240, 2) for y in range(0, 320, 2) if screen.get_at((x, y))[:3] != (0, 0, 0))


def test_draws_both_messages():
    display.init(headless=True)
    offline_screen.draw(Sync("idle"))
    offline = pygame.image.tobytes(display.screen, "RGB")
    assert lit(display.screen) > 0
    offline_screen.draw(Sync("off"))
    assert pygame.image.tobytes(display.screen, "RGB") != offline


def test_ok_returns_for_another_try():
    display.init(headless=True)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0))
    asyncio.run(asyncio.wait_for(offline_screen.show(Sync("idle")), 5))


def test_back_on_a_refused_login_forgets_the_account(monkeypatch):
    display.init(headless=True)
    gone = []
    monkeypatch.setattr(offline_screen, "forget_account", lambda: gone.append(1))
    s = Sync("off")
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0))
    asyncio.run(asyncio.wait_for(offline_screen.show(s), 5))
    assert gone and s.retries == 1
