"""Hero creation (New Game): the save written by ag.ar() is read back by ag.U() (Continue)."""
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)


def test_new_hero_save_roundtrip(tmp_path, monkeypatch):
    import config
    from pow.game.game_canvas import GameCanvas
    from pow.game.menus import Menus
    from pow.game.scr_table import ScrTable
    from pow.game.structs import Hero
    from pow.midp.jrandom import Random
    from pow.midp.rms import RecordStore

    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    game = Menus.__new__(Menus)                 # no Canvas / thread, only the static state is used
    monkeypatch.setattr(GameCanvas, "menus", game)
    monkeypatch.setattr(GameCanvas, "scr_data", ScrTable("/edat.scr"))
    monkeypatch.setattr(GameCanvas, "rng", Random(42))
    monkeypatch.setattr(GameCanvas, "hero", Hero())
    monkeypatch.setattr(GameCanvas, "save_buf", [0] * 2000)
    monkeypatch.setattr(GameCanvas, "state", 2)
    monkeypatch.setattr(GameCanvas, "difficulty", 1)
    monkeypatch.setattr(GameCanvas, "save_pos", 0)
    monkeypatch.setattr(GameCanvas, "item_tables", [None] * 3)
    monkeypatch.setattr(GameCanvas, "tables_loaded", [False] * 16)
    monkeypatch.setattr(GameCanvas, "shop", [None] * 25)

    GameCanvas.hero.reset_inventory()  # allocates X / Y / Z
    game.new_hero()                           # fresh hero, gets item 116 equipped
    assert GameCanvas.hero.equipped[0].id == 116 and GameCanvas.hero.backpack[0].id == 0
    GameCanvas.hero.name = "Leo"
    GameCanvas.hero.head = 2
    GameCanvas.hero.base_hp += 10
    GameCanvas.hero.stat_points = 0
    GameCanvas.difficulty = 0                           # Hard
    GameCanvas.reset_quick_items()
    game.fill_shop()
    shop = [GameCanvas.shop[8 + b].id for b in range(17)]
    assert shop == sorted(shop) and all(101 <= s < 300 for s in shop)
    assert game.save_game()                    # -> RecordStore "gamevil_pow_data"
    size = GameCanvas.save_pos
    rec = RecordStore.openRecordStore("gamevil_pow_data", False).getRecord(1)
    assert len(rec) == 2000 and rec[0] | rec[1] << 8 == size
    assert bytes(rec[2:10]) == b"Leo     "

    monkeypatch.setattr(GameCanvas, "hero", Hero())
    GameCanvas.hero.reset_inventory()
    monkeypatch.setattr(GameCanvas, "shop", [None] * 25)
    GameCanvas.difficulty = 1
    game.load_game()                          # Continue
    assert GameCanvas.hero.name == "Leo"
    assert (GameCanvas.hero.level, GameCanvas.hero.base_hp, GameCanvas.hero.base_mp, GameCanvas.hero.base_attack, GameCanvas.hero.base_defense, GameCanvas.hero.stat_points, GameCanvas.hero.head) == (1, 40, 10, 5, 4, 0, 2)
    assert GameCanvas.hero.equipped[0].id == 116 and GameCanvas.hero.equipped[0].attack == 1
    assert GameCanvas.difficulty == 0
    assert [GameCanvas.shop[8 + b].id for b in range(17)] == shop
    assert GameCanvas.save_pos == size
