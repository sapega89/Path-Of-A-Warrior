"""Reward popup after an ending (l.e(27), DECOMP-FIX F19): no None lines, hidden mission name shown."""
import pytest


def _popup(monkeypatch, ef, eg):
    from pow.game.ag import ag
    from pow.game.l import l
    data = bytearray(38 * 3 + 10 + 40)
    data[38 * 1 + 10:38 * 1 + 10 + 10] = b"Royal Seal"
    monkeypatch.setattr(ag, "v_I", staticmethod(lambda n: bytes(data)))
    monkeypatch.setattr(ag, "ef", ef)
    monkeypatch.setattr(ag, "eg", eg)
    monkeypatch.setattr(ag, "bV", 10)
    p = l()
    p.e_I(27)
    return p.l[:p.i]


@pytest.mark.parametrize("ef,eg,lines", [
    (502, 0, ["Catherine's scarf", "received!"]),
    (0, 1, ["Hidden Mission!", "Royal Seal"]),
    (502, 1, ["Catherine's scarf", "received!", "", "Hidden Mission!", "Royal Seal"]),
])
def test_reward_popup_lines(monkeypatch, ef, eg, lines):
    assert _popup(monkeypatch, ef, eg) == lines
