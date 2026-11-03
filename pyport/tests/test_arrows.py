"""Archers' arrows (ar.Z / ar.j / ar.ad, DECOMP-FIX F18)."""


def _setup(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import Arrow, Point
    monkeypatch.setattr(GameCanvas, "eC", [Arrow() for _ in range(3)])
    ex = type("Ex", (), {})()
    ex.a = [Point(), Point()]
    ex.a[0].a, ex.a[0].b = 150, 200
    ex.e = [4, 4]          # facing up (e >> 1 == 2)
    ex.j = 10
    monkeypatch.setattr(GameCanvas, "ex", [ex])
    return GameCanvas


def test_arrow_starts_at_the_archer(monkeypatch):
    from pow.game.map_engine import MapEngine
    ag = _setup(monkeypatch)
    MapEngine.Z_I(0)
    a = ag.eC[0]
    assert a.a == 1
    assert (a.b[0].a, a.b[0].b) == (149, 170)   # bow of an archer facing up: (-1, -30)
    MapEngine.ad_I(0)                                  # flies 12 px a tick toward where it faces
    assert (a.b[0].a, a.b[0].b) == (149, 158)
