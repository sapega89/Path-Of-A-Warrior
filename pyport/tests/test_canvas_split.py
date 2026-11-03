"""GameCanvas (ag.java) and MpCanvas (g.java) are split into mixin modules
(pow/game/canvas_*.py, pow_mp/mp_canvas_*.py). Edge cases of that split:
a method defined in two parts would silently shadow the other one (MRO), and a part whose module
globals were not wired up would only fail when that code path runs."""
import inspect

from pow.game import game_canvas
from pow_mp import game, mp_canvas

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
    assert len(_assert_no_method_defined_twice(mp_canvas.MpCanvas, "pow_mp.mp_canvas")) > 150
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
