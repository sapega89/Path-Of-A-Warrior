"""javax.microedition.lcdui.Canvas: size, repaint/serviceRepaints, phone key codes.

Key map = PHASE_1_FOUNDATION.md §5.
"""
import asyncio
import collections
import sys

import pygame

import config
from pow.midp import display, gamepad, system, watchdog
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
    # PORT-EXTRA: number row 1..5 = the five skill slots (phone keys 1 3 7 9 0); the phone
    # keypad (2 4 6 8 = arrows, 5 = OK) is on the numeric keypad
    pygame.K_1: 49, pygame.K_2: 51, pygame.K_3: 55, pygame.K_4: 57, pygame.K_5: 48,
    pygame.K_6: 54, pygame.K_7: 55, pygame.K_8: 56, pygame.K_9: 57, pygame.K_0: 48,
    pygame.K_u: 49, pygame.K_i: 51, pygame.K_o: 55, pygame.K_p: 57, pygame.K_k: 48,
    pygame.K_z: 42, pygame.K_x: 35,
    pygame.K_TAB: -100,                 # PORT-EXTRA: auto-hunt on / off (pow/game/autopilot.py)
    pygame.K_f: -100,                   # (F too: a browser may keep Tab for its own focus)
    # numeric keypad = phone keypad (8 up, 2 down, 4 left, 6 right, 5 OK)
    pygame.K_KP8: -1, pygame.K_KP2: -2, pygame.K_KP4: -3, pygame.K_KP6: -4, pygame.K_KP5: -5,
    pygame.K_KP0: 48, pygame.K_KP1: 49, pygame.K_KP3: 51, pygame.K_KP7: 55, pygame.K_KP9: 57,
    pygame.K_KP_MULTIPLY: 42, pygame.K_KP_DIVIDE: 35,
}

# PORT-EXTRA (config.SKILL_BAR): while the hero acts on the map, Z X C V B = belt slots 0..4
# (key codes -101..-105); elsewhere Z and X stay * and # (Assign Items)
BELT_KEYMAP = {pygame.K_z: -101, pygame.K_x: -102, pygame.K_c: -103, pygame.K_v: -104, pygame.K_b: -105}

# mouse wheel -> key, decided by the game (pow/game/pointer.py); right button = BACK
MOUSE_BACK = -7
AUTO_TOGGLE = -100                      # PORT-EXTRA: Tab / the AUTO corner of the map
DIRECTION_KEYS = (-1, -2, -3, -4, 50, 52, 54, 56)
_IS_WEB = sys.platform == "emscripten"
PAD_POLL_MS = 20                        # browser: how often a sleeping game loop reads the gamepad

# names used by scenario files (tools/shot.py)
KEYNAMES = {"UP": -1, "DOWN": -2, "LEFT": -3, "RIGHT": -4, "FIRE": -5, "OK": -5,
            "LSOFT": -6, "RSOFT": -7, "BACK": -7, "STAR": 42, "POUND": 35,
            "AUTO": -100}                       # PORT-EXTRA: Tab, auto-hunt / auto-battle
KEYNAMES.update({str(i): 48 + i for i in range(10)})
KEYNAMES.update({"BELT%d" % (i + 1): -101 - i for i in range(5)})


class Canvas:
    def __init__(self):
        self._repaint = False
        self.quit_requested = False
        self.key_queue = collections.deque()   # keys produced by the mouse, 1 per tick
        self.pointer = None                     # callable(x, y, button) -> list of key codes
        self.hold_dir = None                    # callable(x, y) -> direction key while dragging
        self.held = []                          # direction keys held down, last pressed last
        self.mouse_dir = None                   # direction of the held left mouse button
        self.autopilot = None                   # PORT-EXTRA: tick() -> key, .direction, player_key()
        self.belt_active = None                 # callable() -> True: Z X C V B are belt keys
        self.pads = gamepad.Gamepads() if config.GAMEPAD else None   # PORT-EXTRA: gamepad
        self.text_input = None                  # PORT-EXTRA: callable(char) -> True: typed text

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
            elif ev.type == pygame.KEYDOWN and (ev.key == pygame.K_F11 or (
                    ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and ev.mod & pygame.KMOD_ALT)):
                display.toggle_fullscreen()          # PORT-EXTRA: full screen
                display.present()
            elif ev.type == pygame.KEYDOWN and self.text_input is not None and ev.unicode and \
                    not ev.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT) and self.text_input(ev.unicode):
                pass                                 # PORT-EXTRA: a text box took the key (MP chat)
            elif ev.type == pygame.KEYDOWN:
                code = KEYMAP.get(ev.key)
                if ev.key in BELT_KEYMAP and self.belt_active is not None and self.belt_active():
                    code = BELT_KEYMAP[ev.key]
                if code is not None:
                    self.key_queue.clear()
                    if self.autopilot is not None and code != AUTO_TOGGLE:
                        self.autopilot.player_key()
                    if code in DIRECTION_KEYS:
                        self.hold(code)
                    self.keyPressed(code)
            elif ev.type == pygame.KEYUP:
                code = KEYMAP.get(ev.key)
                if code in DIRECTION_KEYS:
                    self.release(code)
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button in (1, 2, 3):
                x, y = self._to_screen(ev.pos)
                if ev.button == 3:
                    keys = self.pointer(x, y, "rclick") if self.pointer else [MOUSE_BACK]
                elif ev.button == 2:
                    keys = self.pointer(x, y, "middle") if self.pointer else []
                else:
                    keys = self.pointer(x, y, "click") if self.pointer else []
                    if self.autopilot is not None and keys and keys != [AUTO_TOGGLE]:
                        self.autopilot.player_key()
                    # a click that walks: the button held down keeps walking (HOLD_TO_MOVE)
                    self.mouse_dir = keys[0] if len(keys) == 1 and keys[0] in DIRECTION_KEYS else None
                self.key_queue.extend(keys)
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.mouse_dir = None
            elif ev.type == pygame.MOUSEMOTION and self.mouse_dir is not None and self.hold_dir:
                d = self.hold_dir(*self._to_screen(ev.pos))     # dragging turns the hero
                if d is not None:
                    self.mouse_dir = d
            elif self.pads is not None and ev.type in gamepad.EVENTS:
                self._pad_keys(self.pads.handle(ev))
            elif ev.type == pygame.MOUSEWHEEL and ev.y != 0 and self.pointer:
                x, y = self._to_screen(pygame.mouse.get_pos())
                self.key_queue.extend(self.pointer(x, y, "wheel_up" if ev.y > 0 else "wheel_down"))
        if self.pads is not None and self.pads.pads:
            self._pad_keys(self.pads.poll())
        # a phone delivers one key per tick: queued mouse keys go one by one
        if self.key_queue:
            self.keyPressed(self.key_queue.popleft())
        elif self.autopilot is not None:        # PORT-EXTRA: the auto-hunt presses its key
            key = self.autopilot.tick()
            if key is not None:
                self.keyPressed(key)

    def _pad_keys(self, keys):
        """PORT-EXTRA: (phone key, pressed) pairs of the gamepad, handled like the keyboard's."""
        for code, down in keys:
            if not down:
                self.release(code)
                continue
            if code in gamepad.BELT_CODES and not (self.belt_active is not None and self.belt_active()):
                continue                    # the belt only while the hero acts on the map
            self.key_queue.clear()
            if self.autopilot is not None and code != AUTO_TOGGLE:
                self.autopilot.player_key()     # as a key: the auto-hunt waits a moment
            if code in DIRECTION_KEYS:
                self.hold(code)
            self.keyPressed(code)

    def click(self, x, y, kind="click"):
        """Mouse input in screen coordinates (240x320), used by tests and tools/shot.py."""
        if kind == "back":
            self.key_queue.append(MOUSE_BACK)
        elif self.pointer:
            self.key_queue.extend(self.pointer(x, y, kind))

    # --- held direction keys (PORT-EXTRA config.HOLD_TO_MOVE: the phone had no key release) ---
    def hold(self, code):
        if code in self.held:
            self.held.remove(code)
        self.held.append(code)

    def release(self, code):
        if code in self.held:
            self.held.remove(code)

    def held_direction(self):
        """Phone code of the direction held now (mouse button first, then the last key), or None."""
        if self.mouse_dir is not None:
            return self.mouse_dir
        if self.held:
            return self.held[-1]
        return self.autopilot.direction if self.autopilot is not None else None

    @staticmethod
    def _to_screen(pos):
        return display.to_screen(pos)

    async def sleep_ms(self, ms):
        """Thread.sleep inside the game loop. Lets the browser breathe and reads keys."""
        watchdog.tick()
        if system.is_virtual():
            system.advance(ms)
            await asyncio.sleep(0)
        elif self.pads is not None and _IS_WEB and ms > PAD_POLL_MS:
            # PORT-EXTRA: in the browser SDL reads the gamepad only when events are pumped, so a
            # short tap between two ticks was lost; pump it every PAD_POLL_MS while sleeping
            # (pump() keeps the events in the queue for pump_events)
            left = ms
            while left > 0:
                step = min(left, PAD_POLL_MS)
                await asyncio.sleep(step / 1000.0)
                left -= step
                if left > 0:
                    pygame.event.pump()
        else:
            await asyncio.sleep(ms / 1000.0)
        self.pump_events()
