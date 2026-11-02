"""Reward popup after an ending (l.e(27), DECOMP-FIX F19): no None lines, hidden mission name shown."""
import pytest


def _popup(monkeypatch, ef, eg):
    from pow.game.game_canvas import GameCanvas
    from pow.game.popups import Popups
    data = bytearray(38 * 3 + 10 + 40)
    data[38 * 1 + 10:38 * 1 + 10 + 10] = b"Royal Seal"
    monkeypatch.setattr(GameCanvas, "load_data_file", staticmethod(lambda n: bytes(data)))
    monkeypatch.setattr(GameCanvas, "reward_item", ef)
    monkeypatch.setattr(GameCanvas, "reward_skill", eg)
    monkeypatch.setattr(GameCanvas, "state", 10)
    p = Popups()
    p.setup_popup(27)
    return p.lines[:p.line_count]


@pytest.mark.parametrize("ef,eg,lines", [
    (502, 0, ["Catherine's scarf", "received!"]),
    (0, 1, ["Hidden Mission!", "Royal Seal"]),
    (502, 1, ["Catherine's scarf", "received!", "", "Hidden Mission!", "Royal Seal"]),
])
def test_reward_popup_lines(monkeypatch, ef, eg, lines):
    assert _popup(monkeypatch, ef, eg) == lines
