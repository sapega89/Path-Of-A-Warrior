"""ORIG-BUG: bugs of the original game, fixed behind config.ORIG_BUG (False = the original)."""
import pytest

from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)


@pytest.fixture
def game(tmp_path, monkeypatch):
    import config
    from pow.game.ag import ag
    from pow.game.al import al
    from pow.game.e import e
    from pow.game.structs import n
    from pow.midp.jrandom import Random
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    g = e.__new__(e)
    for name, value in (("bb", g), ("bE", al("/edat.scr")), ("by", Random(42)), ("cz", n()),
                        ("cF", [0] * 2000), ("bV", 2), ("ep", 1), ("cG", 0), ("bH", [None] * 3),
                        ("fM", [False] * 16), ("fL", [None] * 25),
                        ("fn", [[0] * 45 for _ in range(3)])):
        monkeypatch.setattr(ag, name, value)
    ag.cz.a_v()
    g.av()
    assert ag.az()
    return g


@pytest.mark.parametrize("fixed", [True, False])
def test_b1_rare_items_get_their_stats(game, monkeypatch, fixed):
    import config
    monkeypatch.setitem(config.ORIG_BUG, "B1", fixed)
    pike = game.J_I(503)                       # Heaven's Pike: ATK 135, DEF 36 (shinki.arr)
    assert (pike.b, pike.c) == ((135, 36) if fixed else (0, 0))
    spear = game.J_I(301)                      # Special items were always right
    assert (spear.b, spear.c) == (30, 1)


@pytest.mark.parametrize("fixed", [True, False])
def test_b2_level_128_and_above_survives_the_save(game, monkeypatch, fixed):
    import config
    from pow.game.ag import ag
    from pow.game.structs import n
    monkeypatch.setitem(config.ORIG_BUG, "B2", fixed)
    ag.cz.k = "Leo"
    ag.cz.l = 150
    ag.ax()
    game.ay()
    assert game.ar()
    monkeypatch.setattr(ag, "cz", n())
    ag.cz.a_v()
    monkeypatch.setattr(ag, "fL", [None] * 25)
    game.U_v()
    assert ag.cz.l == (150 if fixed else 150 - 256)


@pytest.mark.parametrize("fixed", [True, False])
def test_b3_emperors_seal_lists_all_44_generals(game, monkeypatch, fixed):
    import config
    from pow.game.ag import ag
    from pow.game.e import e
    monkeypatch.setitem(config.ORIG_BUG, "B3", fixed)
    if config.ORIG_BUG["B3"]:
        e.seal_list()
    names = [ag.fn[2][i] for i in range(44)]
    if fixed:
        assert names[:3] == [4, 5, 6] and names[-1] == 140 and all(names)
        e.bh_v()
        assert ag.fr.b_II(names[0] - 1, 0)    # a general's name from general.arr
    else:
        assert not any(names)
