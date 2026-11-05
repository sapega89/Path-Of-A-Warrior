"""PORT-EXTRA: the Multiplayer screens as a part of the single player (main.py): Gamevil Live >
Multiplayer suspends the game loop with everything in memory, the Multiplayer client runs
embedded (no exit popup, no outro, the rewards kept in memory) and Live.after_multiplayer pays
the hero when the loop goes on."""
import asyncio
import struct
from types import SimpleNamespace

import pytest
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy video driver)


def test_suspend_stops_the_loop_and_loop_clears_it(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    monkeypatch.setattr(GameCanvas, "stop_sound", staticmethod(lambda: None))
    canvas = GameCanvas.__new__(GameCanvas)
    canvas.quit_requested = True                    # loop() ends at once
    GameCanvas.suspended = False
    GameCanvas.running = True
    canvas.suspend()
    assert GameCanvas.suspended and not GameCanvas.running
    asyncio.run(canvas.loop())
    assert not GameCanvas.suspended and GameCanvas.running


@pytest.fixture
def live(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    from pow.game.structs import Hero, Item, QuickSlot

    hero = Hero()
    hero.gold, hero.fame, hero.exp, hero.level = 100, 5, 0, 1
    hero.backpack = [Item() for _ in range(5)]
    hero.quick_slots = [QuickSlot() for _ in range(5)]
    monkeypatch.setattr(GameCanvas, "hero", hero)
    monkeypatch.setattr(GameCanvas, "menus", SimpleNamespace(load_exp_table=lambda: [50] * 10,
                                                              load_item_def=lambda item_id: None))
    shown = []
    popups = SimpleNamespace(show=shown.append, arg1="", arg2="", arg3="", answered=False)
    monkeypatch.setattr(GameCanvas, "popups", popups)
    monkeypatch.setattr(Live, "request_redraw", staticmethod(lambda: None))
    live = Live.__new__(Live)
    saved = []
    monkeypatch.setattr(live, "save_game", lambda: saved.append(1))
    return live, hero, shown, saved


def test_after_multiplayer_pays_the_hero_with_level_ups_and_the_popup(live):
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    live, hero, shown, saved = live
    live.after_multiplayer([{"gold": 20, "fame": 3, "exp": 70, "loot": [(150, 7, 0, 0, 0)]},
                            {"gold": 0, "fame": 0, "exp": 50, "loot": [(5, 0, 0, 0, 0)]}])
    assert (hero.gold, hero.fame) == (120, 8)
    assert (hero.level, hero.exp) == (3, 20)         # 120 exp, 50 a level
    assert (hero.backpack[0].id, hero.backpack[0].attack) == (150, 7)
    assert [(s.item, s.count) for s in hero.quick_slots if s.item][0] == (5, 1)
    assert shown == [41]
    assert (GameCanvas.popups.arg1, GameCanvas.popups.arg2, GameCanvas.popups.arg3) == ("120", "3", "2")
    assert Live.close_target == -1 and saved


def test_after_multiplayer_with_nothing_earned_shows_no_popup(live):
    live, hero, shown, saved = live
    live.after_multiplayer([])
    assert (hero.gold, hero.fame, hero.level, hero.exp) == (100, 5, 1, 0)
    assert shown == [] and saved


def test_loot_on_a_full_backpack_is_lost(live):
    live, hero, shown, saved = live
    for cell in hero.backpack:
        cell.id = 200
    assert live.give_loot((150, 1, 2, 3, 4)) is False
    assert all(cell.id == 200 for cell in hero.backpack)


def test_embedded_multiplayer_leaves_without_the_exit_popup_or_the_outro(monkeypatch):
    from pow_mp.mp_canvas import MpCanvas
    states = []
    monkeypatch.setattr(MpCanvas, "set_state", staticmethod(states.append))
    monkeypatch.setattr(MpCanvas, "embedded", True)
    monkeypatch.setattr(MpCanvas, "sp_account", True)
    monkeypatch.setattr(MpCanvas, "popup_shown", False)
    monkeypatch.setattr(MpCanvas, "key_in", -7)
    canvas = MpCanvas.__new__(MpCanvas)
    canvas._keys_main_menu(-7)
    assert states == [300] and not MpCanvas.popup_shown
    done = []
    monkeypatch.setattr(MpCanvas, "disconnect", staticmethod(lambda: done.append("disconnect")))
    monkeypatch.setattr(canvas, "stop_music", lambda: done.append("music"))
    monkeypatch.setattr(MpCanvas, "midlet", SimpleNamespace(destroyApp=lambda b: done.append("destroy"),
                                                           notifyDestroyed=lambda: done.append("destroyed")))
    monkeypatch.setattr(MpCanvas, "state_ticks", 0)
    canvas._paint_outro()
    assert done == ["disconnect", "music", "destroy", "destroyed"]
    assert MpCanvas.state_ticks == 0                 # the outro picture never started


def test_rewards_of_1032_wait_in_memory_when_embedded(monkeypatch):
    from pow_mp import sp_bridge
    from pow_mp.net_thread import NetThread
    monkeypatch.setattr(sp_bridge, "embedded", True)
    sp_bridge.pending.clear()
    head = struct.pack("<HbB", 1032, 1, 1) + struct.pack("<hBhh", 20, 2, 3, 120)
    NetThread._port_extra_in(head.ljust(12, b"\0"))
    with_loot = head.ljust(36, b"\0") + struct.pack("<Hhhhh", 150, 7, 0, 0, 0)
    NetThread._port_extra_in(with_loot)
    assert sp_bridge.take_rewards() == [{"gold": 20, "fame": 3, "exp": 120, "loot": []},
                                        {"gold": 20, "fame": 3, "exp": 120, "loot": [(150, 7, 0, 0, 0)]}]
    assert sp_bridge.take_rewards() == []


def test_main_menu_multiplayer_opens_gamevil_live_then_multiplayer(monkeypatch):
    import config
    from pow.game.game_canvas import GameCanvas
    from pow.game.live import Live
    from pow.game.live_online import Online
    monkeypatch.setattr(config, "ALWAYS_ONLINE", True)
    monkeypatch.setattr(Online, "wanted", True)
    monkeypatch.setattr(Online, "background", False)
    monkeypatch.setattr(Online, "offer", False)
    monkeypatch.setattr(Online, "mp_pending", True)
    monkeypatch.setattr(Online, "_game_menu_free", staticmethod(lambda: True))
    monkeypatch.setattr(GameCanvas, "in_live", False)
    monkeypatch.setattr(Live, "waiting", False)
    monkeypatch.setattr(Live, "pending_request", -1)
    monkeypatch.setattr(Live, "auto_mp", False)
    opened = []
    Online.tick(SimpleNamespace(open_live=lambda: opened.append(1)))
    assert opened == [1] and Live.auto_mp and not Online.mp_pending
