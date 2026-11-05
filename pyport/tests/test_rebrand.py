"""PORT-EXTRA rebrand.py: no Gamevil in what the player sees (config.REBRAND)."""
import config
from pow.game import rebrand
from pow.game.scr_table import ScrTable

OLD = "game" + "vil"   # the original publisher


def _all(path):
    t = ScrTable(path)
    n = t.data[0] & 0xFF | (t.data[1] & 0xFF) << 8
    return [t.get(i) for i in range(n)]


def test_rebranded_tables(monkeypatch):
    monkeypatch.setattr(config, "REBRAND", True)
    for path in ("/gamestr.scr", "/help.scr", "/uimenu.scr"):
        for s in _all(path):
            assert s is None or OLD not in s.lower(), (path, s)
    assert ScrTable("/gamestr.scr").get(4) == "LIVE"
    assert ScrTable("/text.scr").get(62) == "Developer Team"
    assert ScrTable("/imgui.scr").get(36) == "gamevil"      # a file name, not shown


def test_original_when_off(monkeypatch):
    monkeypatch.setattr(config, "REBRAND", False)
    assert ScrTable("/gamestr.scr").get(4) == "GAMEVIL LIVE"


def test_mp_pages_keep_their_length(monkeypatch):
    monkeypatch.setattr(config, "REBRAND", True)
    lines = ["T", "Please visit", "www.gamevil.com", "for more", "information about", "the game.", "Next"]
    out = rebrand.mp_lines(lines)
    assert len(out) == len(lines) and out[-1] == "Next"
    assert not any(OLD in x.lower() for x in out)


def test_old_store_moves_to_new_name(tmp_path, monkeypatch):
    from pow.midp import rms
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    (tmp_path / (rms.OLD_PREFIX + "pow_data.rms.json")).write_text('["AAE="]', encoding="utf-8")
    rs = rms.RecordStore.openRecordStore("pow_data", False)
    assert bytes(rs.getRecord(1)) == b"\x00\x01"
    assert (tmp_path / "pow_data.rms.json").is_file()
    assert not (tmp_path / (rms.OLD_PREFIX + "pow_data.rms.json")).exists()


def test_server_saves_move_to_new_names(tmp_path):
    from pow_server.storage import Storage
    db = str(tmp_path / "s.sqlite")
    st = Storage(db)
    st.create_account("ANDREY", "1234")
    st.db.execute("INSERT INTO saves VALUES (?,?,?,?,?)", ("ANDREY", "game" + "vil_pow_data", 3, 1, "[]"))
    st.db.close()
    st = Storage(db)
    assert set(st.saves_get("ANDREY")) == {"pow_data"}
