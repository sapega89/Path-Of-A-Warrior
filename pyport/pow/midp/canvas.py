"""javax.microedition.lcdui.Canvas: size, repaint/serviceRepaints, phone key codes.

Key map = PHASE_1_FOUNDATION.md §5.
"""
import asyncio

import pygame

import config
from pow.midp import display, system
from pow.midp.graphics import Graphics

# PC key -> phone key code (keyPressed argument)
KEYMAP = {
    pygame.K_UP: -1, pygame.K_w: -1,
    pygame.K_DOWN: -2, pygame.K_s: -2,
    pygame.K_LEFT: -3, pygame.K_a: -3,
    pygame.K_RIGHT: -4, pygame.K_d: -4,
    pygame.K_RETURN: -5, pygame.K_KP_ENTER: -5, pygame.K_SPACE: -5, pygame.K_j: -5,
    pygame.K_q: -6, pygame.K_F1: -6,
    pygame.K_ESCAPE: -7, pygame.K_BACKSPACE: -7,
    pygame.K_0: 48, pygame.K_1: 49, pygame.K_2: 50, pygame.K_3: 51, pygame.K_4: 52,
    pygame.K_5: 53, pygame.K_6: 54, pygame.K_7: 55, pygame.K_8: 56, pygame.K_9: 57,
    pygame.K_u: 49, pygame.K_i: 51, pygame.K_o: 55, pygame.K_p: 57, pygame.K_k: 48,
    pygame.K_z: 42, pygame.K_x: 35,
}

# names used by scenario files (tools/shot.py)
KEYNAMES = {"UP": -1, "DOWN": -2, "LEFT": -3, "RIGHT": -4, "FIRE": -5, "OK": -5,
            "LSOFT": -6, "RSOFT": -7, "BACK": -7, "STAR": 42, "POUND": 35}
KEYNAMES.update({str(i): 48 + i for i in range(10)})


class Canvas:
    def __init__(self):
        self._repaint = False
        self.quit_requested = False

    def getWidth(self):
        return config.SCREEN_W

    def getHeight(self):
        return config.SCREEN_H

    def setFullScreenMode(self, mode):
        pass

    def repaint(self, *args):
        self._repaint = True

    def serviceRepaints(self):
        if not self._repaint:
            return
        self._repaint = False
        self.paint(Graphics(display.screen))
        display.present()

    # --- input ------------------------------------------------------------
    def pump_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.quit_requested = True
            elif ev.type == pygame.KEYDOWN:
                code = KEYMAP.get(ev.key)
                if code is not None:
                    self.keyPressed(code)

    async def sleep_ms(self, ms):
        """Thread.sleep inside the game loop. Lets the browser breathe and reads keys."""
        if system.is_virtual():
            system.advance(ms)
            await asyncio.sleep(0)
        else:
            await asyncio.sleep(ms / 1000.0)
        self.pump_events()
