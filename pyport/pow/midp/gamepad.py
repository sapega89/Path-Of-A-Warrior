"""PORT-EXTRA: a gamepad / joystick on the PC (config.GAMEPAD), as phone keys like the keyboard.

    left stick, d-pad    arrows (held = the hero keeps walking, as with the keys)
    A                    OK / attack            B          BACK
    X  Y  LB  RB  LT     the 5 skill keys (phone 1 3 7 9 0)
    RT                   *  (potion)            L3         #  (potion)
    R3                   AUTO: auto-hunt / auto-battle on / off
    Start                right soft key (PAUSE / BACK)
    Back / Select        left soft key (SKIP, EXCHANGE)

A pad SDL knows as a game controller (Xbox, PlayStation, Switch Pro, most others; in the browser
any pad with the "standard" layout) uses these names whatever its own button numbers are.
Any other joystick: buttons 0-7 are taken in the Xbox order (A B X Y LB RB Back Start), the first
hat and the first two axes move. Pads may be plugged in and out while the game runs.
"""
import pygame

try:
    from pygame._sdl2 import controller as sdl_controller
except Exception:          # an old pygame / a build without it: plain joysticks only
    sdl_controller = None

UP, DOWN, LEFT, RIGHT = -1, -2, -3, -4
OK, LSOFT, BACK = -5, -6, -7
SKILLS = (49, 51, 55, 57, 48)
STAR, POUND = 42, 35
AUTO = -100             # PORT-EXTRA: auto-hunt / auto-battle on / off (as Tab)

DEADZONE = 0.5          # how far a stick goes before it counts as a direction
TRIGGER = 0.5           # how far a trigger goes before it counts as pressed

# SDL game controller buttons -> phone keys
CONTROLLER_BUTTONS = {
    pygame.CONTROLLER_BUTTON_A: OK,
    pygame.CONTROLLER_BUTTON_B: BACK,
    pygame.CONTROLLER_BUTTON_X: SKILLS[0],
    pygame.CONTROLLER_BUTTON_Y: SKILLS[1],
    pygame.CONTROLLER_BUTTON_LEFTSHOULDER: SKILLS[2],
    pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: SKILLS[3],
    pygame.CONTROLLER_BUTTON_START: BACK,
    pygame.CONTROLLER_BUTTON_BACK: LSOFT,
    pygame.CONTROLLER_BUTTON_LEFTSTICK: POUND,
    pygame.CONTROLLER_BUTTON_RIGHTSTICK: AUTO,      # PORT-EXTRA: auto-hunt / auto-battle
    pygame.CONTROLLER_BUTTON_DPAD_UP: UP,
    pygame.CONTROLLER_BUTTON_DPAD_DOWN: DOWN,
    pygame.CONTROLLER_BUTTON_DPAD_LEFT: LEFT,
    pygame.CONTROLLER_BUTTON_DPAD_RIGHT: RIGHT,
}
CONTROLLER_TRIGGERS = {
    pygame.CONTROLLER_AXIS_TRIGGERLEFT: SKILLS[4],
    pygame.CONTROLLER_AXIS_TRIGGERRIGHT: STAR,
}
# any other joystick: Xbox order of the first buttons
JOYSTICK_BUTTONS = {0: OK, 1: BACK, 2: SKILLS[0], 3: SKILLS[1], 4: SKILLS[2], 5: SKILLS[3],
                    6: LSOFT, 7: BACK, 8: POUND, 9: AUTO}

DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
EVENTS = (pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP,
          pygame.JOYHATMOTION, pygame.JOYAXISMOTION, pygame.CONTROLLERBUTTONDOWN,
          pygame.CONTROLLERBUTTONUP, pygame.CONTROLLERAXISMOTION)


def stick_direction(x, y):
    """Stick position (-1..1 each) -> direction key or None (the bigger axis wins)."""
    if max(abs(x), abs(y)) < DEADZONE:
        return None
    if abs(x) > abs(y):
        return RIGHT if x > 0 else LEFT
    return DOWN if y > 0 else UP


def hat_direction(hx, hy):
    """Hat (-1/0/1 each, y up = 1) -> direction key or None."""
    if hy:
        return UP if hy > 0 else DOWN
    if hx:
        return RIGHT if hx > 0 else LEFT
    return None


class Pad:
    """One plugged pad: what it holds now, so that a move is only reported when it changes."""

    def __init__(self, device, is_controller):
        self.device = device                 # Controller or Joystick (kept open)
        self.is_controller = is_controller
        self.axes = {}                       # axis -> value -1..1
        self.stick = None                    # direction held by the stick
        self.hat = None                      # direction held by the hat / d-pad
        self.triggers = set()                # trigger axes pressed now
        self.dpad = []                       # d-pad buttons held now, last pressed last


class Gamepads:
    """Turns pygame joystick / controller events into (phone key, pressed) pairs."""

    def __init__(self):
        self.pads = {}                       # instance id -> Pad
        try:
            if not pygame.joystick.get_init():
                pygame.joystick.init()
            if sdl_controller is not None and not sdl_controller.get_init():
                sdl_controller.init()
        except Exception as ex:
            print("gamepad: %r" % ex)

    # -- devices --
    def _add(self, index):
        try:
            if sdl_controller is not None and sdl_controller.is_controller(index):
                dev = sdl_controller.Controller(index)
                iid = dev.as_joystick().get_instance_id()
                self.pads[iid] = Pad(dev, True)
                print("gamepad: %s" % dev.name)
            else:
                dev = pygame.joystick.Joystick(index)
                dev.init()
                self.pads[dev.get_instance_id()] = Pad(dev, False)
                print("joystick: %s" % dev.get_name())
        except Exception as ex:
            print("gamepad %d: %r" % (index, ex))

    def _remove(self, iid):
        """-> the direction keys the pad held (to let them go)."""
        pad = self.pads.pop(iid, None)
        if pad is None:
            return []
        return [(d, False) for d in (pad.stick, pad.hat) if d is not None]

    # -- events --
    def handle(self, ev):
        """-> list of (phone key code, True = pressed / False = let go) for one pygame event."""
        t = ev.type
        if t == pygame.JOYDEVICEADDED:
            self._add(ev.device_index)
            return []
        if t == pygame.JOYDEVICEREMOVED:
            return self._remove(ev.instance_id)
        pad = self.pads.get(getattr(ev, "instance_id", None))
        if pad is None:
            return []
        if pad.is_controller:
            if t in (pygame.CONTROLLERBUTTONDOWN, pygame.CONTROLLERBUTTONUP):
                code = CONTROLLER_BUTTONS.get(ev.button)
                if code is None:
                    return []
                down = t == pygame.CONTROLLERBUTTONDOWN
                if code in DIRECTIONS:            # several held: the last one counts, then the rest
                    if code in pad.dpad:
                        pad.dpad.remove(code)
                    if down:
                        pad.dpad.append(code)
                    return self._set_hat(pad, pad.dpad[-1] if pad.dpad else None)
                return [(code, True)] if down else []
            if t == pygame.CONTROLLERAXISMOTION:
                value = ev.value / 32767.0
                if ev.axis in CONTROLLER_TRIGGERS:
                    return self._trigger(pad, ev.axis, value, CONTROLLER_TRIGGERS[ev.axis])
                if ev.axis in (pygame.CONTROLLER_AXIS_LEFTX, pygame.CONTROLLER_AXIS_LEFTY):
                    return self._axis(pad, 0 if ev.axis == pygame.CONTROLLER_AXIS_LEFTX else 1, value)
            return []                        # the same pad's JOY* events are not used twice
        if t == pygame.JOYBUTTONDOWN:
            code = JOYSTICK_BUTTONS.get(ev.button)
            return [(code, True)] if code is not None else []
        if t == pygame.JOYHATMOTION and ev.hat == 0:
            return self._set_hat(pad, hat_direction(*ev.value))
        if t == pygame.JOYAXISMOTION and ev.axis in (0, 1):
            return self._axis(pad, ev.axis, ev.value)
        return []

    @staticmethod
    def _set_hat(pad, d):
        if d == pad.hat:
            return []
        out = [(pad.hat, False)] if pad.hat is not None else []
        pad.hat = d
        return out + ([(d, True)] if d is not None else [])

    @staticmethod
    def _axis(pad, axis, value):
        pad.axes[axis] = value
        d = stick_direction(pad.axes.get(0, 0.0), pad.axes.get(1, 0.0))
        if d == pad.stick:
            return []
        out = [(pad.stick, False)] if pad.stick is not None else []
        pad.stick = d
        return out + ([(d, True)] if d is not None else [])

    @staticmethod
    def _trigger(pad, axis, value, code):
        if value >= TRIGGER and axis not in pad.triggers:
            pad.triggers.add(axis)
            return [(code, True)]
        if value < TRIGGER * 0.6 and axis in pad.triggers:
            pad.triggers.discard(axis)
        return []
