"""(asked by Andrey): no name of the original publisher in the game's files and code,
and the stores renamed from its prefix move to the new names."""
import pathlib

import config

OLD = "game" + "vil"   # the original publisher
HERE = pathlib.Path(__file__).resolve().parents[1]


def test_no_publisher_in_resources_and_code():
    roots = [pathlib.Path(config.RES_ROOT), pathlib.Path(config.MP_RES_ROOT), HERE]
    found = []
    for root in roots:
        for p in root.rglob("*"):
            skip = {".git", "__pycache__", "docs", "vault", ".pytest_cache", ".idea", ".venv", "build"}
            if not p.is_file() or skip & set(p.parts) or p.suffix.lower() in (".sqlite", ".log"):
                continue        # notes about the original and local files, not the game
            if p.suffix.lower() in (".png", ".mid", ".wav", ".ogg", ".pal", ".ft2", ".pyc"):
                if OLD in p.name.lower():
                    found.append(str(p))
                continue
            if OLD.encode() in p.read_bytes().lower():
                found.append(str(p))
    assert sorted(set(found)) == [], found


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
