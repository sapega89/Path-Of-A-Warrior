"""Live: the full (wide) description instead of the running strip, and the layouts
that make room for it (Buy lots, B11 Sell price from the warehouse)."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import config  # noqa: E402


def test_wide_description_in_live(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.menus import Menus
    calls = []
    monkeypatch.setattr(Menus, "draw_wide_description", lambda self: calls.append("wide"))
    monkeypatch.setattr(config, "WIDE_DESC", True)
    monkeypatch.setattr(GameCanvas, "state", 11)
    Menus.draw_description_strip(Menus.__new__(Menus))
    assert calls == ["wide"]


def test_buy_lots_grid_above_the_description(monkeypatch):
    """the 2 rows of lots end at the description strip (y 200)."""
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    from pow.game.live_screen import LiveScreen
    tops = []
    monkeypatch.setattr(LiveScreen, "draw_hero_gold", lambda self, y: tops.append(y))
    monkeypatch.setattr(LiveScreen, "draw_centred_box", lambda self, y, w, h: 20)
    monkeypatch.setattr(LiveScreen, "draw_number_commas", lambda *a: None)
    monkeypatch.setattr(Live, "draw_text_centred_in", staticmethod(lambda *a: None))
    monkeypatch.setattr(Live, "draw_item_cell", staticmethod(lambda *a: None))
    stub = type("M", (), {"draw_item_grid": lambda self, y, items, marks: tops.append(y),
                          "draw_description_strip": lambda self: None})()
    monkeypatch.setattr(GameCanvas, "menus", stub)
    monkeypatch.setattr(GameCanvas, "describe_shop_item", lambda *a: None)
    monkeypatch.setattr(GameCanvas, "draw_softkeys", lambda *a: None)
    monkeypatch.setattr("pow.game.live_screen.Gfx.set_font", lambda *a: None)
    monkeypatch.setattr(Live, "category", 2)
    GameCanvas.cursor[6] = 32 * 2 - 4 + 2
    GameCanvas.cursor[18] = 0
    LiveScreen.draw_buy_lots(LiveScreen.__new__(LiveScreen))
    gold, grid = tops
    assert gold >= 22 and grid + GameCanvas.cursor[6] <= 200, tops


def test_sell_price_describes_the_warehouse_item(monkeypatch):
    """selling from the warehouse describes the warehouse item, and the wide box
    sits under the price box (y 210..232), not over the item."""
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    from pow.game.live_screen import LiveScreen
    seen = []
    monkeypatch.setattr(config, "WIDE_DESC", True)
    monkeypatch.setattr(GameCanvas, "describe_shop_item", lambda item, *a: seen.append(item))
    monkeypatch.setattr(LiveScreen, "draw_panel", lambda *a: None)
    monkeypatch.setattr(LiveScreen, "draw_input_box", lambda *a: None)
    monkeypatch.setattr(Live, "draw_text_centred_in", staticmethod(lambda *a: None))
    monkeypatch.setattr(Live, "draw_item_cell", staticmethod(lambda *a: None))
    monkeypatch.setattr("pow.game.live_screen.Gfx.set_font", lambda *a: None)
    monkeypatch.setattr("pow.game.menus.Menus.item_name", staticmethod(lambda *a: ""))
    monkeypatch.setattr(GameCanvas, "draw_softkeys", lambda *a: None)
    monkeypatch.setattr(GameCanvas, "menus", type("M", (), {"draw_description_strip": lambda self: None})())
    monkeypatch.setattr(GameCanvas, "hero", type("H", (), {"backpack": ["bp"] * config.BACKPACK_SIZE})())
    monkeypatch.setattr(Live, "warehouse", ["wh"] * config.WAREHOUSE_SIZE)
    GameCanvas.cursor[18] = 0
    Live.flags[7] = 1
    LiveScreen.draw_sell_price(LiveScreen.__new__(LiveScreen))
    assert seen == ["wh"]
    assert GameCanvas.info_box.rect.y + GameCanvas.view_y >= 234
