"""PORT-EXTRA skill bar, belt and skill card (pow/game/skill_bar.py, config.SKILL_BAR / SKILL_CARD)."""
import types


def _hero(GameCanvas, monkeypatch):
    from pow.game.structs import QuickSlot
    cz = types.SimpleNamespace(attack=20, attack_buff=0, defense=10, max_hp=100, mp=8,
                               skill_levels=[0] * 19, hotkeys=[12, 17, 0, 0, 0],
                               quick_slots=[QuickSlot() for _ in range(5)], anims=None, action=[0])
    monkeypatch.setattr(GameCanvas, "hero", cz)
    return cz


def test_mp_need_matches_the_combat_cost(monkeypatch):
    from pow.game import skill_bar
    from pow.game.game_canvas import GameCanvas
    from pow.game.map_engine import MapEngine
    cz = _hero(GameCanvas, monkeypatch)
    for sid in range(12, 31):
        for lv in (1, 4, 10):
            cz.skill_levels[sid - 12] = lv
            cz.mp = 999
            assert MapEngine.skill_mp_cost(sid) == skill_bar.mp_need(sid, lv)


def test_skill_lines(monkeypatch):
    from pow.game import skill_bar
    from pow.game.game_canvas import GameCanvas
    _hero(GameCanvas, monkeypatch)
    monkeypatch.setattr(GameCanvas, "speed", 2)
    assert skill_bar.skill_lines(12, 10) == ["DMG 30 x3"]        # 20 + 20*10/20, frames 3 4 5
    assert skill_bar.skill_lines(15, 1) == ["HP+20"]             # 100 * (4 + 1) / 25
    assert skill_bar.skill_lines(19, 8) == ["ATK+6 DEF+3 18s"]   # 150 ticks * 120 ms


def test_click_on_the_bar(monkeypatch):
    import config
    from pow.game import skill_bar
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import Point
    monkeypatch.setattr(config, "SKILL_BAR", True)
    monkeypatch.setattr(GameCanvas, "canvas_size", types.SimpleNamespace(x=240, y=320))
    y = skill_bar.bar_top() + 10
    assert skill_bar.key_at(5, y) == -101          # Z
    assert skill_bar.key_at(100, y) == -105        # B
    assert skill_bar.key_at(120, y) == -999        # the gap
    assert skill_bar.key_at(130, y) == 49          # skill 1 (phone key 1)
    assert skill_bar.key_at(235, y) == 48          # skill 5 (phone key 0)
    assert skill_bar.key_at(130, y - 30) is None   # the map above the bar
    monkeypatch.setattr(config, "SKILL_BAR", False)
    assert skill_bar.key_at(130, y) is None
