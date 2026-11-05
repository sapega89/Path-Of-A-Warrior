"""PHASE_9 task 9.10: the multiplayer hero from the single-player save, rewards back into it."""
import struct

import pytest

import config
from pow.game.online import sp_bridge as S
from pow_server import codec_bin
from pow_server import messages as M
from pow_server.server import GameServer
from pow_server.storage import MemoryStorage


def make_save(level=12, atk=40, def_=30, hp=250, mp=90, gold=1000, fame=50, exp=7,
              face=2, weapon_id=118, skills=None, slots=(12 + 0, 12 + 3, 0, 0, 0)):
    """A 965-byte record laid out like ag.java:2865-2950 (the writer of ag.U)."""
    d = bytearray(S.SAVE_LEN)
    d[0], d[1] = S.SAVE_LEN & 0xFF, S.SAVE_LEN >> 8
    d[2:10] = b"HERO    "
    d[S.OFF_LEVEL] = level
    struct.pack_into("<hhhhhh", d, S.OFF_ATK, atk, def_, hp, hp, mp, mp)
    struct.pack_into("<iii", d, S.OFF_GOLD, gold, fame, exp)
    for i, v in enumerate(slots):
        d[S.OFF_SLOTS + i] = v
    for idx, lvl in (skills or {0: 3, 3: 2, 11: 5}).items():   # Wind 3, Medium Heal 2, a fire skill
        d[S.OFF_SKILLS + idx] = lvl
    # weapon in X[0] with +5 ATK, a helmet in X[1] with +3 DEF +10 HP
    struct.pack_into("<hhhhhB", d, S.OFF_ITEMS, weapon_id, 5, 0, 0, 0, 0)
    struct.pack_into("<hhhhhB", d, S.OFF_ITEMS + 11, 131, 0, 3, 10, 0, 0)
    struct.pack_into("<I", d, S.OFF_DY, 0b1011)
    d[S.OFF_FACE] = face
    return bytes(d)


@pytest.fixture
def save_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    return tmp_path


def store(data):
    from pow.midp.rms import RecordStore
    rs = RecordStore.openRecordStore(S.SAVE_STORE, True)
    rs.addRecord(bytearray(data), 0, len(data))


def test_hero_from_save():
    h = S.hero(make_save())
    assert (h["level"], h["hp"], h["mp"], h["atk"], h["def"]) == (12, 250, 90, 40, 30)
    assert (h["atk_bonus"], h["def_bonus"], h["hp_bonus"], h["mp_bonus"]) == (5, 3, 10, 0)
    assert h["face"] == 2 and h["weapon"] == 0                 # 118 War Claymore: long
    assert S.hero(make_save(weapon_id=103))["weapon"] == 1     # 103 War Blade: short
    assert h["skills"][3 - 3] == 3 and h["skills"][9 - 3] == 2 and sum(h["skills"]) == 5
    assert h["slots"] == [3, 9, 99, 99]                        # V[] index + 12 -> as.gG
    assert h["progress"] == 3
    assert S.hero(None) is None


def test_no_save_no_hero(save_dir):
    assert S.read_save() is None
    assert S.add_rewards(10, 1, 1) is False


def test_rewards_go_into_the_save(save_dir):
    store(make_save(gold=1000, fame=50, exp=7))
    assert S.add_rewards(120, 15, 40)
    d = S.read_save()
    assert struct.unpack_from("<iii", d, S.OFF_GOLD) == (1120, 65, 47)
    assert S.add_rewards(0, -100, 0)                           # fame never goes below 0
    assert struct.unpack_from("<i", S.read_save(), S.OFF_FAME)[0] == 0


def _login(server, extra):
    out = []
    sess = server.connect(lambda f: out.extend(codec_bin.decode(p, from_client=False)
                                               for p in codec_bin.unframe(f)[0]))
    sess.receive(codec_bin.unframe(codec_bin.encode(M.LOGIN_FIRST, {"id": "HERO", "pwd": "1234",
                                                                     "ver": M.GAME_VER}, to_client=False))[0][0])
    tok = out[-1]["token"]
    sess.close()
    out.clear()
    sess = server.connect(lambda f: out.extend(codec_bin.decode(p, from_client=False)
                                               for p in codec_bin.unframe(f)[0]))
    msg = dict({"id": "HERO", "ver": M.GAME_VER, "token": tok}, **extra)
    sess.receive(codec_bin.unframe(codec_bin.encode(M.LOGIN, msg, to_client=False))[0][0])
    return sess, out


def test_server_takes_the_hero_from_login():
    server = GameServer(MemoryStorage())
    hero = S.hero(make_save())
    _sess, out = _login(server, dict({"sp": 1}, **{"sp_" + k: v for k, v in hero.items()}))
    prof = out[-1]
    assert prof["st"] == 1 and prof["level"] == 12 and prof["hp"] == 260 and prof["face"] == 2
    assert prof["slots"] == [3, 9, 99, 99]
    ch = server.storage.load("HERO")
    assert ch.sp_linked and ch.atk == 40 and ch.atk_bonus == 5 and ch.skills == {3: 3, 9: 2}
    assert ch.sp_progress == 3


def test_login_without_a_save_keeps_the_default_hero():
    server = GameServer(MemoryStorage())
    _sess, out = _login(server, {"sp": 0})
    assert out[-1]["level"] == 1 and not server.storage.load("HERO").sp_linked


def test_slots_chosen_in_multiplayer_survive_the_next_login():
    server = GameServer(MemoryStorage())
    extra = dict({"sp": 1}, **{"sp_" + k: v for k, v in S.hero(make_save()).items()})
    sess, out = _login(server, extra)
    ch = server.storage.load("HERO")
    ch.slots = [9, 3, 99, 99]                       # 1291 from the Skills screen
    server.storage.save(ch)
    sess.close()
    sess, out = _login(server, extra)
    assert out[-1]["slots"] == [9, 3, 99, 99]
