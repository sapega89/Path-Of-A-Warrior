"""PORT-EXTRA: a bigger backpack (config.BACKPACK_SIZE) and Warehouse (config.WAREHOUSE_SIZE), old
saves still load; above Lv69 the gear drops keep the odds of Lv45-69 (config.DROPS_AFTER_69)."""
import random
import struct

import pytest
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)

import config


@pytest.fixture
def game(tmp_path, monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.menus import Menus
    from pow.game.scr_table import ScrTable
    from pow.game.structs import Hero
    from pow.midp.jrandom import Random

    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    g = Menus.__new__(Menus)
    monkeypatch.setattr(GameCanvas, "menus", g)
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
    GameCanvas.hero.reset_inventory()
    g.new_hero()
    GameCanvas.hero.name = "Leo"
    GameCanvas.reset_quick_items()
    g.fill_shop()
    return g


def _reload(game, monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import Hero
    monkeypatch.setattr(GameCanvas, "hero", Hero())
    GameCanvas.hero.reset_inventory()
    monkeypatch.setattr(GameCanvas, "shop", [None] * 25)
    game.load_game()
    return GameCanvas.hero


def test_sizes():
    from pow.game import consts
    from pow.game.live import Live
    from pow.game.structs import Hero
    assert config.BACKPACK_SIZE > 25 and config.BACKPACK_SIZE % 5 == 0
    assert config.WAREHOUSE_SIZE > 100 and config.WAREHOUSE_SIZE % 5 == 0 and config.WAREHOUSE_SIZE < 256
    assert len(Hero().backpack) == config.BACKPACK_SIZE
    assert consts.menu_sizes[17] == config.BACKPACK_SIZE            # cells of the Inventory menu
    assert len(Live.warehouse) == config.WAREHOUSE_SIZE


def test_full_backpack_survives_save_and_load(game, monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.midp.rms import RecordStore
    cz = GameCanvas.hero
    for b in range(config.BACKPACK_SIZE):
        assert game.give_item(101 + b, 0) != 0, b               # ag.k(): the first free cell
    assert game.give_item(150, 0) == 0                          # full
    cz.backpack[config.BACKPACK_SIZE - 1].enchant = 7
    assert game.save_game()
    size = GameCanvas.save_pos
    rec = RecordStore.openRecordStore("pow_data", False).getRecord(1)
    assert rec[0] | rec[1] << 8 == size == 965 + 2 + 11 * (config.BACKPACK_SIZE - 25)

    cz = _reload(game, monkeypatch)
    assert [it.id for it in cz.backpack] == [101 + b for b in range(config.BACKPACK_SIZE)]
    assert cz.backpack[-1].enchant == 7
    assert GameCanvas.save_pos == size


def test_old_save_loads_with_the_new_cells_empty(game, monkeypatch):
    """A save of the 25-cell backpack (record length 965, as before this change) loads; the new
    cells are empty and the next save adds them."""
    from pow.game.game_canvas import GameCanvas
    from pow.midp.rms import RecordStore
    for b in range(25):
        game.give_item(101 + b, 0)
    assert game.save_game()
    rs = RecordStore.openRecordStore("pow_data", False)
    old = bytearray(rs.getRecord(1)[:965])
    old[0], old[1] = 965 & 0xFF, 965 >> 8
    rs.setRecord(1, old, 0, len(old))

    cz = _reload(game, monkeypatch)
    assert cz.name == "Leo"
    assert [it.id for it in cz.backpack[:25]] == [101 + b for b in range(25)]
    assert all(it.id == 0 for it in cz.backpack[25:])
    assert GameCanvas.save_pos == 965

    assert game.give_item(160, 0) != 0                          # a 26th item fits now
    assert game.save_game()                                     # into the short record: grows it
    cz = _reload(game, monkeypatch)
    assert cz.backpack[25].id == 160


def test_inventory_pages(game, display):
    """menu 17: 3 rows a page, the cursor walks every cell (UP from the top wraps to the end)."""
    from pow.game.game_canvas import GameCanvas
    cM = GameCanvas.menu
    cM[0], cM[2] = 17, 0
    GameCanvas.menu_count = config.BACKPACK_SIZE
    game.key_up()
    assert cM[2] == config.BACKPACK_SIZE - 5
    game.key_down_arrow()
    assert cM[2] == 0


def _tiers(rand, level, n=6000):
    from pow.game.game_canvas import GameCanvas
    from pow.game.map_engine import MapEngine
    from pow.game.structs import Hero
    eng = MapEngine.__new__(MapEngine)
    eng.rand = rand
    GameCanvas.hero = Hero()
    GameCanvas.hero.level = level
    got = [eng.random_drop(2) for _ in range(n)]
    return {(g - 101) % 5 for g in got if 100 < g < 10000}


def test_drops_above_lv69_keep_the_lv45_69_odds(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    monkeypatch.setattr(GameCanvas, "hero", None)
    rng = random.Random(7)
    def rand(n):
        return rng.randrange(n)
    assert _tiers(rand, 50) == {0, 1, 2, 3, 4}
    assert _tiers(rand, 80) == {0, 1, 2, 3, 4}                  # Lv1 / Lv10 gear still drops
    monkeypatch.setattr(config, "DROPS_AFTER_69", False)
    assert min(_tiers(rand, 80)) == 2                           # the original: {0, 0, 33, 77, 100}


def test_mp_loot_uses_the_new_cells_of_an_old_save(tmp_path, monkeypatch):
    from test_mp_sp_bridge import make_save, store

    from pow_mp import sp_bridge as S
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    data = bytearray(make_save())
    assert data[0] | data[1] << 8 == S.SAVE_LEN                 # a save of before the change
    for i in range(25):
        struct.pack_into("<h", data, S.OFF_BACKPACK + 11 * i, 101)
    store(data)
    assert S.add_item(118, 9, 0, 0, 0) == 0                     # not waiting: cell 26
    d = S.read_save()
    assert d[S.SAVE_LEN] == S.BACKPACK_EXTRA_MARK
    assert struct.unpack_from("<hhhhhB", d, S.SAVE_LEN + 2) == (118, 9, 0, 0, 0, 0)
    assert d[0] | d[1] << 8 == S.SAVE_LEN + 2 + 11 * (config.BACKPACK_SIZE - 25)


def test_live_grid_above_softkeys(monkeypatch):
    """ORIG-BUG B9: the Backpack / Warehouse grid of Live ends above the description strip
    (y 200) and the soft keys, also with the bigger Warehouse."""
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    from pow.game.live_screen import LiveScreen
    tops = []
    monkeypatch.setattr(LiveScreen, "draw_caption_box", lambda self, s, y: tops.append(y))
    stub = type("M", (), {"draw_item_grid": lambda self, y, items, marks: tops.append(y),
                          "draw_description_strip": lambda self: None})()
    monkeypatch.setattr(GameCanvas, "menus", stub)
    monkeypatch.setattr(GameCanvas, "describe_shop_item", lambda *a: None)
    monkeypatch.setattr(GameCanvas, "hero", type("H", (), {"backpack": [None] * config.BACKPACK_SIZE})())
    monkeypatch.setattr(Live, "warehouse", [None] * config.WAREHOUSE_SIZE)
    monkeypatch.setattr(GameCanvas, "draw_softkeys", lambda *a: None)
    GameCanvas.cursor[6] = 32 * 3 - 4 + 2
    GameCanvas.cursor[18] = 0
    for flag in (0, 1):
        Live.flags[7] = flag
        tops.clear()
        LiveScreen.draw_grid(LiveScreen.__new__(LiveScreen))
        caption, grid = tops
        assert caption >= 22 and grid + GameCanvas.cursor[6] <= 198, tops
