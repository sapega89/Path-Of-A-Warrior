"""Archers' arrows (ar.Z / ar.j / ar.ad, DECOMP-FIX F18)."""


def _setup(monkeypatch):
    from pow.game.ag import ag
    from pow.game.structs import f, h
    monkeypatch.setattr(ag, "eC", [f() for _ in range(3)])
    ex = type("Ex", (), {})()
    ex.a = [h(), h()]
    ex.a[0].a, ex.a[0].b = 150, 200
    ex.e = [4, 4]          # facing up (e >> 1 == 2)
    ex.j = 10
    monkeypatch.setattr(ag, "ex", [ex])
    return ag


def test_arrow_starts_at_the_archer(monkeypatch):
    from pow.game.ar import ar
    ag = _setup(monkeypatch)
    ar.Z_I(0)
    a = ag.eC[0]
    assert a.a == 1
    assert (a.b[0].a, a.b[0].b) == (149, 170)   # bow of an archer facing up: (-1, -30)
    ar.ad_I(0)                                  # flies 12 px a tick toward where it faces
    assert (a.b[0].a, a.b[0].b) == (149, 158)
