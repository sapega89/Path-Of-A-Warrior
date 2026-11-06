"""Archers' arrows."""


def _setup(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import Arrow, Point
    monkeypatch.setattr(GameCanvas, "arrows", [Arrow() for _ in range(3)])
    ex = type("Ex", (), {})()
    ex.pos = [Point(), Point()]
    ex.pos[0].x, ex.pos[0].y = 150, 200
    ex.dir = [4, 4]        # facing up (dir >> 1 == 2)
    ex.attack = 10
    monkeypatch.setattr(GameCanvas, "actors", [ex])
    return GameCanvas


def test_arrow_starts_at_the_archer(monkeypatch):
    from pow.game.map_engine import MapEngine
    ag = _setup(monkeypatch)
    MapEngine.shoot_arrow(0)
    a = ag.arrows[0]
    assert a.active == 1
    assert (a.pos[0].x, a.pos[0].y) == (149, 170)   # bow of an archer facing up: (-1, -30)
    MapEngine.move_arrow(0)                                  # flies 12 px a tick toward where it faces
    assert (a.pos[0].x, a.pos[0].y) == (149, 158)
