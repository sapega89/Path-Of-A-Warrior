"""Hero creation (New Game): the save written by ag.ar() is read back by ag.U() (Continue)."""
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)


def test_new_hero_save_roundtrip(tmp_path, monkeypatch):
    import config
    from pow.game.game_canvas import GameCanvas
    from pow.game.scr_table import ScrTable
    from pow.game.menus import Menus
    from pow.game.structs import Hero
    from pow.midp.jrandom import Random
    from pow.midp.rms import RecordStore

    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    game = Menus.__new__(Menus)                 # no Canvas / thread, only the static state is used
    monkeypatch.setattr(GameCanvas, "bb", game)
    monkeypatch.setattr(GameCanvas, "bE", ScrTable("/edat.scr"))
    monkeypatch.setattr(GameCanvas, "by", Random(42))
    monkeypatch.setattr(GameCanvas, "cz", Hero())
    monkeypatch.setattr(GameCanvas, "cF", [0] * 2000)
    monkeypatch.setattr(GameCanvas, "bV", 2)
    monkeypatch.setattr(GameCanvas, "ep", 1)
    monkeypatch.setattr(GameCanvas, "cG", 0)
    monkeypatch.setattr(GameCanvas, "bH", [None] * 3)
    monkeypatch.setattr(GameCanvas, "fM", [False] * 16)
    monkeypatch.setattr(GameCanvas, "fL", [None] * 25)

    GameCanvas.cz.a_v()                         # n.a(): allocates X / Y / Z (ag.java:600)
    game.av()                           # ag.java:3222 fresh hero, gets item 116 equipped
    assert GameCanvas.cz.X[0].a == 116 and GameCanvas.cz.Y[0].a == 0
    GameCanvas.cz.k = "Leo"
    GameCanvas.cz.aB = 2
    GameCanvas.cz.o += 10
    GameCanvas.cz.J = 0
    GameCanvas.ep = 0                           # Hard
    GameCanvas.ax()
    game.ay()
    shop = [GameCanvas.fL[8 + b].a for b in range(17)]
    assert shop == sorted(shop) and all(101 <= s < 300 for s in shop)
    assert game.ar()                    # ag.java:2871 -> RecordStore "gamevil_pow_data"
    size = GameCanvas.cG
    rec = RecordStore.openRecordStore("gamevil_pow_data", False).getRecord(1)
    assert len(rec) == 2000 and rec[0] | rec[1] << 8 == size
    assert bytes(rec[2:10]) == b"Leo     "

    monkeypatch.setattr(GameCanvas, "cz", Hero())
    GameCanvas.cz.a_v()
    monkeypatch.setattr(GameCanvas, "fL", [None] * 25)
    GameCanvas.ep = 1
    game.U_v()                          # ag.java:2126 Continue
    assert GameCanvas.cz.k == "Leo"
    assert (GameCanvas.cz.l, GameCanvas.cz.o, GameCanvas.cz.q, GameCanvas.cz.m, GameCanvas.cz.n, GameCanvas.cz.J, GameCanvas.cz.aB) == (1, 40, 10, 5, 4, 0, 2)
    assert GameCanvas.cz.X[0].a == 116 and GameCanvas.cz.X[0].b == 1
    assert GameCanvas.ep == 0
    assert [GameCanvas.fL[8 + b].a for b in range(17)] == shop
    assert GameCanvas.cG == size
