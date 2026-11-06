"""PHASE_9 task 9.4: the binary codec matches the layout the original client reads/writes."""
import struct

import pytest

from pow_server import codec_bin
from pow_server import messages as M
from pow_server.model import default_character


class K:
    """What the original client uses to read a payload."""
    def __init__(self, data):
        self.a_, self.b_ = data, 0

    def a(self, n=None):
        if n is None:  # s8
            v = struct.unpack_from("<b", self.a_, self.b_)[0]
            self.b_ += 1
            return v
        raw = self.a_[self.b_:self.b_ + n]  # fixed string
        self.b_ += n
        return "" if raw[:1] == b"\0" else raw.split(b"\0")[0].decode().strip()

    def b(self):
        v = struct.unpack_from("<h", self.a_, self.b_)[0]
        self.b_ += 2
        return v

    def c(self):
        v = struct.unpack_from("<i", self.a_, self.b_)[0]
        self.b_ += 4
        return v


def payload(op, **fields):
    data = codec_bin.encode(op, fields, to_client=True)
    assert struct.unpack_from("<H", data)[0] == len(data)
    return data[2:]


def test_frame_roundtrip():
    f = codec_bin.frame(b"\x07\x01abc") + codec_bin.frame(b"\x01\x02")
    payloads, rest = codec_bin.unframe(f + b"\x09")
    assert payloads == [b"\x07\x01abc", b"\x01\x02"] and rest == b"\x09"
    with pytest.raises(codec_bin.CodecError):
        codec_bin.unframe(b"\x01\x00")


def test_login_answer_is_read_like_g_java():
    """263 = status + 104 bytes, read in the order of g:1938-1975."""
    ch = default_character("ANDREY")
    ch.name, ch.level, ch.wins, ch.losses, ch.hp, ch.weapon = "Hero", 37, 70000, 3, 950, 1
    p = payload(M.LOGIN_ANS, st=1, **ch.profile(notices=2))
    assert len(p) == 2 + 1 + 104
    k = K(p)
    assert k.b() == 263 and k.a() == 1
    assert k.a(8) == "Hero"
    assert k.a() == ch.face and k.b() == 37 and k.c() == 70000 and k.c() == 3 and k.b() == 950
    k.b(), k.b()
    assert k.a() == 1
    assert [k.a() for _ in range(4)] == [3, 11, 99, 99]     # Wind, Devil Soul: a new hero
    assert k.a(20) == ch.quote_start and k.a(20) == ch.quote_win
    costs = [k.a() for _ in range(11)]
    assert all(0 < c <= 100 for c in costs)
    k.a(), k.a(), k.a()
    assert k.a() == 2                                  # aN: notices pages
    k.a(8), k.a(8), k.a(), k.a(), k.a()
    assert k.b_ == len(p)


def test_fighter_is_72_bytes():
    p = payload(M.ROOM_JOIN, st=1, **default_character("ABCD").fighter(1))
    assert len(p) == 3 + 72
    k = K(p)
    k.b(), k.a()
    assert k.a() == 1 and k.a(8) == "ABCD"


def test_battle_end_is_33_bytes_and_the_loot_item():
    p = payload(M.BATTLE_END, st=1, win=1, gold=120, grade=4, fame=7, exp=33, loot="NONE", rank=5)
    assert len(p) == 3 + 33 + 10                # item {u16 id, 4 x s16} after the 33
    p = payload(M.BATTLE_END, st=1, win=1, loot="War Claymore", item_id=118, item_atk=9)
    msg = codec_bin.decode(p, from_client=False)
    assert msg["loot"] == "War Claymore" and (msg["item_id"], msg["item_atk"]) == (118, 9)


def test_turn_result_layout():
    """1028: 4 + 1 + 12*aT + 1 + 5*(records with a second target), g:2247-2299."""
    recs = [
        {"actor": 0, "action": 0, "actor_hp": 100, "actor_mp": 20, "target": 1, "result": 1,
         "target_hp": 77, "target_mp": 10, "has2nd": 0, "flags": 0},
        {"actor": 1, "action": 8, "actor_hp": 77, "actor_mp": 0, "target": 0, "result": 1,
         "target_hp": 60, "target_mp": 25, "has2nd": 1, "flags": 0,
         "target2": 2, "result2": 2, "target2_hp": 50, "target2_mp": 5},
    ]
    p = payload(M.TURN_RESULT, st=1, turn=None, actions=[0, 8, 99, 99], records=recs)
    assert len(p) == 3 + 4 + 1 + 24 + 1 + 5
    msg = codec_bin.decode(p, from_client=False)
    assert msg["actions"] == [0, 8, 99, 99]
    assert msg["records"][1]["target2_hp"] == 50 and msg["records"][0]["target_hp"] == 77
    with pytest.raises(ValueError, match="at most 4 records"):
        payload(M.TURN_RESULT, st=1, actions=[0] * 4, records=recs * 3)


def test_client_messages():
    data = codec_bin.encode(M.TURN, {"target": 1, "action": 0, "hit": 84}, to_client=False)
    assert data == bytes([7, 0]) + struct.pack("<H", 1027) + bytes([1, 0, 84])
    data = codec_bin.encode(M.LOGIN_FIRST, {"id": "ANDREY", "pwd": "1234", "ver": "0111"}, to_client=False)
    assert len(data) == 2 + 2 + 12 + 16 + 4
    msg = codec_bin.decode(data[2:], from_client=True)
    assert (msg["op"], msg["id"], msg["pwd"], msg["ver"]) == (278, "ANDREY", "1234", "0111")


def test_original_262_without_token_decodes_short():
    """The original client sends 262 without the token: the field is just missing."""
    raw = struct.pack("<H", 262) + b"ANDREY".ljust(12, b"\0") + b"0111"
    msg = codec_bin.decode(raw, from_client=True)
    assert msg["id"] == "ANDREY" and msg["ver"] == "0111" and "token" not in msg


def test_error_answers_carry_only_the_status():
    p = payload(M.NAME_SET_ANS, st=M.ERR_NAME_EXISTS)
    assert p == struct.pack("<Hb", 1281, -6)
    p = payload(M.LOGIN_FIRST_ANS, st=-1, reason=M.REASON_BAD_PASSWORD)
    assert codec_bin.decode(p, from_client=False) == {"op": 279, "st": -1, "reason": 1}


def test_rank_list_counts_rows():
    rows = [{"rank": i, "id": "PLAYER{}".format("ABC"[i - 1]), "value": 10 - i} for i in (1, 2, 3)]
    msg = codec_bin.decode(payload(M.RANK_LIST_ANS, st=1, rows=rows), from_client=False)
    assert msg["n"] == 3 and msg["rows"] == rows


def test_values_out_of_range_are_refused():
    with pytest.raises(codec_bin.CodecError):
        codec_bin.encode(M.BATTLE_END, {"gold": 40000}, to_client=True)   # s16 in 1032
