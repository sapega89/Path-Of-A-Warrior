"""the on-screen keyboards of the Live registration (pow/game/key_grid.py,
config.REG_KEYBOARD) and the soft-key captions naming the key of the last device
(config.KEY_HINTS, pow/midp/canvas.py key_hints)."""
import pytest
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)

UP, DOWN, LEFT, RIGHT, FIRE, LSOFT, BACK = -1, -2, -3, -4, -5, -6, -7


def test_user_id_grid_has_the_letters_the_ok_cell_and_a_row_of_digits():
    from pow.game.key_grid import KeyGrid
    g = KeyGrid.user_id()
    assert ["".join(r) for r in g.rows] == ["ABCDEFGHIJKLMN", "OPQRSTUVWXYZOK", "0123456789"]
    assert g.rows[1][12] == "OK" and len(g.rows[1]) == 13
    assert g.width == 142                      # as wide as the original ag.f grid


def test_cursor_keeps_the_column_and_is_clamped_to_the_row_end():
    from pow.game.key_grid import KeyGrid
    g = KeyGrid.user_id()
    for _ in range(13):
        g.move(RIGHT)
    assert (g.row, g.col, g.label) == (0, 13, "N")
    assert g.move(DOWN) and (g.row, g.col, g.label) == (1, 12, "OK")
    assert g.move(DOWN) and (g.row, g.col, g.label) == (2, 9, "9")
    assert g.move(RIGHT) and (g.row, g.col, g.label) == (2, 0, "0")    # wraps in the row
    assert g.move(LEFT) and g.label == "9"
    assert g.move(UP) and (g.row, g.col) == (1, 9)
    assert not g.move(FIRE) and (g.row, g.col) == (1, 9)


@pytest.fixture
def live(monkeypatch):
    import config
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    from pow.game.name_buffer import NameBuffer

    monkeypatch.setattr(config, "REG_KEYBOARD", True)
    monkeypatch.setattr(Live, "request_redraw", staticmethod(lambda: None))
    monkeypatch.setattr(GameCanvas, "name_buf", NameBuffer("", 12, 10))
    live = Live.__new__(Live)
    asked = []
    monkeypatch.setattr(live, "ask_request", asked.append)
    monkeypatch.setattr(live, "leave_live", lambda: asked.append("left"))
    from pow.game.key_grid import KeyGrid
    Live.reg_step = 1
    Live.user_id = Live.password = ""
    Live.id_grid, Live.pwd_grid = KeyGrid.user_id(), KeyGrid.password()
    return live, asked


def _press(live, *keys):
    for k in keys:
        live.registration_keys(k)


def test_user_id_typed_on_the_grid_with_letters_and_digits(live):
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    live, asked = live
    _press(live, FIRE, RIGHT, FIRE)                 # A, B
    _press(live, DOWN, DOWN, FIRE, RIGHT, FIRE)     # row 0..9: "1", "2"
    assert GameCanvas.name_buf.get_text() == "AB12"
    _press(live, UP, LEFT, LEFT, LEFT)              # O..Z row, wraps left onto OK
    assert Live.id_grid.is_ok
    _press(live, FIRE)
    assert (Live.user_id, Live.reg_step) == ("AB12", 0)
    assert asked == []


def test_phone_number_keys_still_move_and_type_on_the_user_id_step(live):
    from pow.game.game_canvas import GameCanvas
    live, _ = live
    _press(live, 54, 53)                            # 6 = right, 5 = type: "B"
    _press(live, 56, 56, 53)                        # 8 8 = down twice: "1"
    assert GameCanvas.name_buf.get_text() == "B1"


def test_ok_cell_needs_four_characters_and_back_deletes(live):
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    live, asked = live
    _press(live, FIRE, FIRE, FIRE)                  # "AAA"
    _press(live, DOWN, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT)
    assert Live.id_grid.is_ok
    _press(live, FIRE)
    assert Live.reg_step == 1                       # too short: nothing happens
    _press(live, BACK)
    assert GameCanvas.name_buf.get_text() == "AA"
    _press(live, BACK, BACK, BACK)                  # empty + BACK = leave
    assert asked == ["left"]


def test_password_typed_on_the_digit_row_and_confirmed_on_ok(live):
    from pow.game.live import Live
    live, asked = live
    Live.reg_step = 0
    _press(live, RIGHT, FIRE, RIGHT, FIRE, RIGHT, FIRE)     # "123"
    _press(live, 53)                                          # the number key 5 is still a digit
    assert Live.password == "1235"
    _press(live, 50)                                          # 2 is a digit too, not "up"
    assert Live.password == "12352"
    for _ in range(4):
        live.registration_keys(LEFT)
    assert Live.pwd_grid.is_ok                                # 3 -> 0 -> OK (wraps)
    _press(live, FIRE)
    assert asked == [530] and Live.reg_from_popup and Live.blink


def test_ok_cell_of_the_password_needs_four_digits(live):
    from pow.game.live import Live
    live, asked = live
    Live.reg_step = 0
    _press(live, FIRE, FIRE, FIRE)                  # "000"
    _press(live, LEFT, FIRE)                        # 0 -> OK
    assert asked == [] and Live.password == "000"
    _press(live, BACK, BACK, BACK, BACK)            # delete all, then back to the UserID
    assert (Live.password, Live.reg_step) == ("", 1)


def test_name_buffer_takes_digits_from_the_keyboard():
    from pow.game.name_buffer import NameBuffer
    b = NameBuffer("", 12, 10)
    for k in (65, 49, 50, 66):
        b.handle_key(k)
    assert b.get_text() == "A12B"


def test_soft_key_hints_follow_the_device(monkeypatch):
    import config
    from pow.midp import canvas
    monkeypatch.setattr(config, "KEY_HINTS", True)
    monkeypatch.setattr(canvas, "input_source", "keyboard")
    assert canvas.key_hints() == ("Q:", "ESC:")
    monkeypatch.setattr(canvas, "input_source", "gamepad")
    assert canvas.key_hints() == ("SEL:", "B:")
    monkeypatch.setattr(config, "KEY_HINTS", False)
    assert canvas.key_hints() == ("", "")


def test_offline_screen_names_the_keys_of_the_device(monkeypatch):
    import config
    from pow.game import offline_screen
    from pow.midp import canvas

    class Sync:
        state = "off"
    monkeypatch.setattr(config, "KEY_HINTS", True)
    monkeypatch.setattr(canvas, "input_source", "gamepad")
    assert offline_screen.lines(Sync())[2:] == ["A: try again", "B: other account"]
    monkeypatch.setattr(canvas, "input_source", "keyboard")
    assert offline_screen.lines(Sync())[2:] == ["ENTER: try again", "ESC: other account"]
    monkeypatch.setattr(config, "KEY_HINTS", False)
    assert offline_screen.lines(Sync())[2:] == ["OK: try again", "BACK: other account"]
