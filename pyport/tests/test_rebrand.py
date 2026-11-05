"""PORT-EXTRA rebrand.py: no Gamevil in what the player sees (config.NO_GAMEVIL)."""
import config
from pow.game import rebrand
from pow.game.scr_table import ScrTable


def _all(path):
    t = ScrTable(path)
    n = t.data[0] & 0xFF | (t.data[1] & 0xFF) << 8
    return [t.get(i) for i in range(n)]


def test_no_gamevil_in_shown_tables(monkeypatch):
    monkeypatch.setattr(config, "NO_GAMEVIL", True)
    for path in ("/gamestr.scr", "/help.scr", "/uimenu.scr"):
        for s in _all(path):
            assert s is None or "gamevil" not in s.lower(), (path, s)
    assert ScrTable("/gamestr.scr").get(4) == "LIVE"
    assert ScrTable("/text.scr").get(62) == "Developer Team"
    assert ScrTable("/imgui.scr").get(36) == "gamevil"      # a file name, not shown


def test_original_when_off(monkeypatch):
    monkeypatch.setattr(config, "NO_GAMEVIL", False)
    assert ScrTable("/gamestr.scr").get(4) == "GAMEVIL LIVE"


def test_mp_pages_keep_their_length(monkeypatch):
    monkeypatch.setattr(config, "NO_GAMEVIL", True)
    lines = ["T", "Please visit", "www.gamevil.com", "for more", "information about", "the game.", "Next"]
    out = rebrand.mp_lines(lines)
    assert len(out) == len(lines) and out[-1] == "Next"
    assert not any("gamevil" in x.lower() for x in out)
