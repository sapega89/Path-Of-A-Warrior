"""MpCanvas (g.java) is split into mixin modules pow_mp/mp_canvas_*.py. Edge cases of that split:
a method defined in two parts would silently shadow the other one (MRO), and a part whose module
globals were not wired up would only fail when that code path runs."""
import inspect

from pow_mp import game, mp_canvas


def test_no_method_is_defined_twice():
    owners = {}
    for cls in mp_canvas.MpCanvas.__mro__:
        if cls.__module__.startswith("pow_mp.mp_canvas"):
            for name, value in vars(cls).items():
                if inspect.isfunction(value) or isinstance(value, staticmethod):
                    assert name not in owners, (name, owners.get(name), cls.__name__)
                    owners[name] = cls.__name__


def test_parts_see_the_real_class_and_late_imports():
    game.load()
    for part in mp_canvas._PARTS:
        assert part.MpCanvas is mp_canvas.MpCanvas
        for name in mp_canvas._LATE_NAMES:
            if name in vars(part):
                assert vars(part)[name] is vars(mp_canvas)[name] is not None, (part.__name__, name)
