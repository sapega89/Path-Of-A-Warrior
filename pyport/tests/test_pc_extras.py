"""PC controls: full screen, the wide description box, the gamepad."""
import pygame

# ---- full screen ---------------------------------------------------------------------------------

def test_fit_takes_the_biggest_whole_scale_and_centres(display):
    assert display.fit((1920, 1080)) == pygame.Rect(600, 60, 720, 960)       # x3, bars on all sides
    assert display.fit((1366, 768)) == pygame.Rect(443, 64, 480, 640)        # x2
    assert display.fit((200, 200)).size == (240, 320)                        # never below x1


def test_clicks_in_full_screen_land_on_the_phone_screen(display, monkeypatch, tmp_path):
    import config
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    display.set_fullscreen(True)
    try:
        assert display.fullscreen
        v = display.view
        assert display.to_screen((v.x, v.y)) == (0, 0)
        assert display.to_screen((v.right - 1, v.bottom - 1)) == (239, 319)
        assert display.to_screen((0, 0)) == (0, 0)                           # on a black bar: clamped
        display.present()
        assert display._load() is True                                       # remembered
    finally:
        display.set_fullscreen(False)
    assert not display.fullscreen
    assert display.window.get_size() == (240, 320)
    assert display._load() is False


# ---- wide description ----------------------------------------------------------------------------

def test_description_parts_are_packed_into_lines(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.menus import Menus
    monkeypatch.setattr(GameCanvas, "measure_text", staticmethod(lambda s: 8 * len(s)))
    lines = Menus.wide_description_lines("Iron Claymore / ATK+12 / Available at Lv1", 224)
    assert lines == ["Iron Claymore / ATK+12", "Available at Lv1"]
    # "/ Price" without a space before the slash splits too
    assert Menus.wide_description_lines("Recover 30% of total HP/ Price: 60", 224) == [
        "Recover 30% of total HP", "Price: 60"]
    # a part longer than the line breaks between words
    assert Menus.wide_description_lines("a" * 20 + " " + "b" * 20, 224) == ["a" * 20, "b" * 20]


# ---- gamepad -------------------------------------------------------------------------------------

def _pads(is_controller):
    from pow.midp import gamepad
    g = gamepad.Gamepads()
    g.pads[7] = gamepad.Pad(None, is_controller)
    return g


def _ev(t, **kw):
    return pygame.event.Event(t, instance_id=7, **kw)


def test_controller_buttons_are_phone_keys():
    g = _pads(True)
    press = lambda b: g.handle(_ev(pygame.CONTROLLERBUTTONDOWN, button=b))     # noqa: E731
    assert press(pygame.CONTROLLER_BUTTON_A) == [(-5, True)]
    assert press(pygame.CONTROLLER_BUTTON_B) == [(-7, True)]
    assert press(pygame.CONTROLLER_BUTTON_X) == [(49, True)]
    assert press(pygame.CONTROLLER_BUTTON_RIGHTSHOULDER) == [(57, True)]
    assert press(pygame.CONTROLLER_BUTTON_START) == [(-7, True)]
    # the same pad's raw joystick events are not used a second time
    assert g.handle(_ev(pygame.JOYBUTTONDOWN, button=0)) == []
    # triggers: one press per pull
    pull = lambda a, v: g.handle(_ev(pygame.CONTROLLERAXISMOTION, axis=a, value=v))  # noqa: E731
    assert pull(pygame.CONTROLLER_AXIS_TRIGGERLEFT, 30000) == [(48, True)]
    assert pull(pygame.CONTROLLER_AXIS_TRIGGERLEFT, 32767) == []
    assert pull(pygame.CONTROLLER_AXIS_TRIGGERLEFT, 0) == []
    assert pull(pygame.CONTROLLER_AXIS_TRIGGERRIGHT, 32767) == [(42, True)]


def test_stick_and_dpad_hold_a_direction():
    g = _pads(True)
    move = lambda a, v: g.handle(_ev(pygame.CONTROLLERAXISMOTION, axis=a, value=v))  # noqa: E731
    assert move(pygame.CONTROLLER_AXIS_LEFTX, 32000) == [(-4, True)]               # right
    assert move(pygame.CONTROLLER_AXIS_LEFTX, 31000) == []                         # still right
    assert move(pygame.CONTROLLER_AXIS_LEFTY, -32767) == [(-4, False), (-1, True)]  # up wins
    assert move(pygame.CONTROLLER_AXIS_LEFTY, 0) == [(-1, False), (-4, True)]
    assert move(pygame.CONTROLLER_AXIS_LEFTX, 1000) == [(-4, False)]               # centre
    dpad = lambda t, b: g.handle(_ev(t, button=b))                                  # noqa: E731
    assert dpad(pygame.CONTROLLERBUTTONDOWN, pygame.CONTROLLER_BUTTON_DPAD_DOWN) == [(-2, True)]
    assert dpad(pygame.CONTROLLERBUTTONUP, pygame.CONTROLLER_BUTTON_DPAD_DOWN) == [(-2, False)]
    # right, then up while right is still held: letting up go walks right again
    assert dpad(pygame.CONTROLLERBUTTONDOWN, pygame.CONTROLLER_BUTTON_DPAD_RIGHT) == [(-4, True)]
    assert dpad(pygame.CONTROLLERBUTTONDOWN, pygame.CONTROLLER_BUTTON_DPAD_UP) == [(-4, False), (-1, True)]
    assert dpad(pygame.CONTROLLERBUTTONUP, pygame.CONTROLLER_BUTTON_DPAD_UP) == [(-1, False), (-4, True)]
    assert dpad(pygame.CONTROLLERBUTTONUP, pygame.CONTROLLER_BUTTON_DPAD_RIGHT) == [(-4, False)]


def test_plain_joystick_and_unplugging():
    g = _pads(False)
    assert g.handle(_ev(pygame.JOYBUTTONDOWN, button=0)) == [(-5, True)]
    assert g.handle(_ev(pygame.JOYBUTTONDOWN, button=3)) == [(51, True)]
    assert g.handle(_ev(pygame.JOYHATMOTION, hat=0, value=(-1, 0))) == [(-3, True)]
    assert g.handle(_ev(pygame.JOYAXISMOTION, axis=1, value=0.9)) == [(-2, True)]
    assert sorted(g.handle(_ev(pygame.JOYDEVICEREMOVED))) == [(-3, False), (-2, False)]
    assert g.handle(_ev(pygame.JOYBUTTONDOWN, button=0)) == []                     # gone


def test_canvas_walks_while_the_stick_is_held(display):
    from pow.midp import gamepad
    from pow.midp.canvas import Canvas
    c = Canvas()
    got = []
    c.keyPressed = got.append
    c.pads.pads[7] = gamepad.Pad(None, True)
    pygame.event.post(_ev(pygame.CONTROLLERAXISMOTION, axis=pygame.CONTROLLER_AXIS_LEFTX, value=-32767))
    c.pump_events()
    assert got == [-3] and c.held_direction() == -3
    pygame.event.post(_ev(pygame.CONTROLLERAXISMOTION, axis=pygame.CONTROLLER_AXIS_LEFTX, value=0))
    c.pump_events()
    assert c.held_direction() is None


def test_right_stick_uses_the_belt_once_per_push():
    g = _pads(True)
    move = lambda a, v: g.handle(_ev(pygame.CONTROLLERAXISMOTION, axis=a, value=v))  # noqa: E731
    assert move(pygame.CONTROLLER_AXIS_RIGHTY, -32000) == [(-101, True)]          # up = Z
    assert move(pygame.CONTROLLER_AXIS_RIGHTY, -32767) == []                      # still up: once
    assert move(pygame.CONTROLLER_AXIS_RIGHTY, 0) == []
    assert move(pygame.CONTROLLER_AXIS_RIGHTX, 32000) == [(-102, True)]           # right = X
    assert move(pygame.CONTROLLER_AXIS_RIGHTX, 0) == []
    assert move(pygame.CONTROLLER_AXIS_RIGHTY, 32000) == [(-103, True)]           # down = C
    assert move(pygame.CONTROLLER_AXIS_RIGHTY, 0) == []
    assert move(pygame.CONTROLLER_AXIS_RIGHTX, -32000) == [(-104, True)]          # left = V
    assert g.pads[7].stick is None                                               # no walking


def test_canvas_belt_only_on_the_map_and_pad_pauses_autohunt(display):
    from pow.midp import gamepad
    from pow.midp.canvas import Canvas
    c = Canvas()
    got = []
    c.keyPressed = got.append
    c.pads.pads[7] = gamepad.Pad(None, True)
    paused = []

    class Auto:
        direction = None

        def player_key(self):
            paused.append(1)

        def tick(self):
            return None
    c.autopilot = Auto()
    push = lambda v: pygame.event.post(_ev(pygame.CONTROLLERAXISMOTION,           # noqa: E731
                                           axis=pygame.CONTROLLER_AXIS_RIGHTY, value=v))
    push(-32767)
    c.pump_events()
    assert got == [] and paused == []               # not on the map: nothing
    push(0)
    c.belt_active = lambda: True
    push(-32767)
    c.pump_events()
    assert got == [-101] and paused == [1]
    pygame.event.post(_ev(pygame.CONTROLLERBUTTONDOWN, button=pygame.CONTROLLER_BUTTON_RIGHTSTICK))
    c.pump_events()
    assert got == [-101, -100] and paused == [1]   # AUTO itself does not pause it


def test_poll_reads_the_sticks_sdl_did_not_report():
    """Browser: SDL keeps the first move of an axis as its resting value, without an event."""
    from pow.midp import gamepad

    class Dev:
        axes = {}

        def get_axis(self, a):
            return self.axes.get(a, 0)
    g = gamepad.Gamepads()
    dev = Dev()
    g.pads[7] = gamepad.Pad(dev, True)
    assert g.poll() == []
    dev.axes = {pygame.CONTROLLER_AXIS_RIGHTY: 32767}
    assert g.poll() == [(-103, True)]                      # right stick down = belt slot C
    assert g.poll() == []                                  # once
    dev.axes = {pygame.CONTROLLER_AXIS_LEFTX: -32767}
    assert g.poll() == [(-3, True)]                        # left stick = walk left, held
    assert g.handle(_ev(pygame.CONTROLLERAXISMOTION, axis=pygame.CONTROLLER_AXIS_LEFTX,
                        value=-32767)) == []               # the event later: no second press
    dev.axes = {}
    assert g.poll() == [(-3, False)]


def test_a_new_canvas_opens_the_pads_plugged_in_before(monkeypatch):
    """Main Menu > Multiplayer: the MP canvas is new, SDL does not send JOYDEVICEADDED again."""
    from pow.midp import gamepad
    added = []
    monkeypatch.setattr(pygame.joystick, "get_count", lambda: 2)
    monkeypatch.setattr(gamepad.Gamepads, "_add", lambda self, i: added.append(i))
    gamepad.Gamepads()
    assert added == [0, 1]
