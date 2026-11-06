"""Bugs of the original game that the port fixes for good."""
import pytest
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)


@pytest.fixture
def game(tmp_path, monkeypatch):
    import config
    from pow.game.game_canvas import GameCanvas
    from pow.game.menus import Menus
    from pow.game.scr_table import ScrTable
    from pow.game.structs import Hero
    from pow.midp.jrandom import Random
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    g = Menus.__new__(Menus)
    for name, value in (("menus", g), ("scr_data", ScrTable("/edat.scr")), ("rng", Random(42)), ("hero", Hero()),
                        ("save_buf", [0] * 2000), ("state", 2), ("difficulty", 1), ("save_pos", 0), ("item_tables", [None] * 3),
                        ("tables_loaded", [False] * 16), ("shop", [None] * 25),
                        ("generals", [[0] * 45 for _ in range(3)])):
        monkeypatch.setattr(GameCanvas, name, value)
    GameCanvas.hero.reset_inventory()
    g.new_hero()
    assert GameCanvas.load_item_tables()
    return g


def test_rare_items_get_their_stats(game):
    pike = game.make_item(503)                       # Heaven's Pike: ATK 135, DEF 36 (shinki.arr)
    assert (pike.attack, pike.defense) == (135, 36)
    spear = game.make_item(301)                      # a Special item
    assert (spear.attack, spear.defense) == (30, 1)


def test_level_128_and_above_survives_the_save(game, monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import Hero
    GameCanvas.hero.name = "Leo"
    GameCanvas.hero.level = 150
    GameCanvas.reset_quick_items()
    game.fill_shop()
    assert game.save_game()
    monkeypatch.setattr(GameCanvas, "hero", Hero())
    GameCanvas.hero.reset_inventory()
    monkeypatch.setattr(GameCanvas, "shop", [None] * 25)
    game.load_game()
    assert GameCanvas.hero.level == 150


def test_emperors_seal_lists_all_44_generals(game):
    from pow.game.game_canvas import GameCanvas
    from pow.game.menus import Menus
    Menus.seal_list()
    names = [GameCanvas.generals[2][i] for i in range(44)]
    assert names[:3] == [4, 5, 6] and names[-1] == 140 and all(names)
    Menus.load_general_table()
    assert GameCanvas.general_table.get_string(names[0] - 1, 0)    # a general's name from general.arr


def test_fire_on_the_5th_item_slot_does_not_open_help(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.map_engine import MapEngine
    fired = []
    monkeypatch.setattr(GameCanvas, "menus", type("M", (), {"key_fire": lambda self: fired.append(1)})())
    monkeypatch.setattr(GameCanvas, "map_mode", type("MM", (), {"mode": 2, "sub": 0})())
    monkeypatch.setattr(GameCanvas, "menu", [10, 4, 0, 0, 0, 0])   # pause menu > Items, cursor on slot 5
    for name, value in (("key", -5), ("state", 3), ("actor_count", 0), ("boss_fight", 0), ("waves", [0] * 4)):
        monkeypatch.setattr(GameCanvas, name, value)
    MapEngine.__new__(MapEngine).pause_menu_keys()
    assert (GameCanvas.state, bool(fired)) == (3, False)
