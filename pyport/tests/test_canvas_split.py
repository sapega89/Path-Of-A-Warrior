"""GameCanvas and MpCanvas are split into mixin modules
(pow/game/canvas_*.py, pow/game/online/mp_canvas_*.py). Edge cases of that split:
a method defined in two parts would silently shadow the other one (MRO), and a part whose module
globals were not wired up would only fail when that code path runs."""
import inspect

from pow.game import game_canvas
from pow.game.online import game, mp_canvas

GC_PARTS = ("pow.game.game_canvas", "pow.game.canvas_")


def _assert_no_method_defined_twice(canvas, prefixes):
    owners = {}
    for cls in canvas.__mro__:
        if cls.__module__.startswith(prefixes):
            for name, value in vars(cls).items():
                if inspect.isfunction(value) or isinstance(value, staticmethod):
                    assert name not in owners, (name, owners.get(name), cls.__name__)
                    owners[name] = cls.__name__
    return owners


def test_no_method_is_defined_twice():
    assert len(_assert_no_method_defined_twice(mp_canvas.MpCanvas, "pow.game.online.mp_canvas")) > 150
    assert len(_assert_no_method_defined_twice(game_canvas.GameCanvas, GC_PARTS)) > 150


def test_game_canvas_parts_see_the_real_class():
    parts = {cls.__module__ for cls in game_canvas.GameCanvas.__mro__ if cls.__module__.startswith("pow.game.canvas_")}
    assert len(parts) == 6
    for name in parts:
        assert __import__(name, fromlist=["x"]).GameCanvas is game_canvas.GameCanvas


def test_parts_see_the_real_class_and_late_imports():
    game.load()
    for part in mp_canvas._PARTS:
        assert part.MpCanvas is mp_canvas.MpCanvas
        for name in mp_canvas._LATE_NAMES:
            if name in vars(part):
                assert vars(part)[name] is vars(mp_canvas)[name] is not None, (part.__name__, name)


def test_dispatch_tables_point_at_the_class_methods():
    """paint_screen / handle_key / on_answer pick a handler from a table built in the class body;
    an override of a handler in another part would be bypassed by the table, so none may exist."""
    canvas = mp_canvas.MpCanvas
    for table in ("_PAINT_BY_STATE", "_KEYS_BY_STATE", "_ANSWER_BY_OPCODE"):
        handlers = getattr(canvas, table)
        assert len(handlers) > 20
        for key, handler in handlers.items():
            assert getattr(canvas, handler.__name__) is handler, (table, key)


def test_single_player_dispatch_tables_point_at_the_class_methods():
    from pow.game.live import Live
    from pow.game.menus import Menus
    for cls, table in ((Live, "_ANSWER_BY_OPCODE"), (Menus, "_FIRE_BY_MENU")):
        handlers = getattr(cls, table)
        assert len(handlers) > 10
        for key, handler in handlers.items():
            assert getattr(cls, handler.__name__) is handler, (table, key)
