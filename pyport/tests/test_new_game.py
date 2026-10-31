"""Hero creation (New Game): the save written by ag.ar() is read back by ag.U() (Continue)."""
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)


def test_new_hero_save_roundtrip(tmp_path, monkeypatch):
    import config
    from pow.game.ag import ag
    from pow.game.al import al
    from pow.game.e import e
    from pow.game.structs import n
    from pow.midp.jrandom import Random
    from pow.midp.rms import RecordStore

    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    game = e.__new__(e)                 # no Canvas / thread, only the static state is used
    monkeypatch.setattr(ag, "bb", game)
    monkeypatch.setattr(ag, "bE", al("/edat.scr"))
    monkeypatch.setattr(ag, "by", Random(42))
    monkeypatch.setattr(ag, "cz", n())
    monkeypatch.setattr(ag, "cF", [0] * 2000)
    monkeypatch.setattr(ag, "bV", 2)
    monkeypatch.setattr(ag, "ep", 1)
    monkeypatch.setattr(ag, "cG", 0)
    monkeypatch.setattr(ag, "bH", [None] * 3)
    monkeypatch.setattr(ag, "fM", [False] * 16)
    monkeypatch.setattr(ag, "fL", [None] * 25)

    ag.cz.a_v()                         # n.a(): allocates X / Y / Z (ag.java:600)
    game.av()                           # ag.java:3222 fresh hero, gets item 116 equipped
    assert ag.cz.X[0].a == 116 and ag.cz.Y[0].a == 0
    ag.cz.k = "Leo"
    ag.cz.aB = 2
    ag.cz.o += 10
    ag.cz.J = 0
    ag.ep = 0                           # Hard
    ag.ax()
    game.ay()
    shop = [ag.fL[8 + b].a for b in range(17)]
    assert shop == sorted(shop) and all(101 <= s < 300 for s in shop)
    assert game.ar()                    # ag.java:2871 -> RecordStore "gamevil_pow_data"
    size = ag.cG
    rec = RecordStore.openRecordStore("gamevil_pow_data", False).getRecord(1)
    assert len(rec) == 2000 and rec[0] | rec[1] << 8 == size
    assert bytes(rec[2:10]) == b"Leo     "

    monkeypatch.setattr(ag, "cz", n())
    ag.cz.a_v()
    monkeypatch.setattr(ag, "fL", [None] * 25)
    ag.ep = 1
    game.U_v()                          # ag.java:2126 Continue
    assert ag.cz.k == "Leo"
    assert (ag.cz.l, ag.cz.o, ag.cz.q, ag.cz.m, ag.cz.n, ag.cz.J, ag.cz.aB) == (1, 40, 10, 5, 4, 0, 2)
    assert ag.cz.X[0].a == 116 and ag.cz.X[0].b == 1
    assert ag.ep == 0
    assert [ag.fL[8 + b].a for b in range(17)] == shop
    assert ag.cG == size
