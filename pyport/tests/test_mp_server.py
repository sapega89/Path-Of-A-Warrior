"""PHASE_9: the server's menu-side messages (login, character, ranking, options)."""
import random

import pytest

from pow_server import codec_bin, messages as M
from pow_server.server import GameServer


class Client:
    """A fake client: sends C->S messages, keeps the decoded S->C ones."""
    def __init__(self, server):
        self.got = []
        self.session = server.connect(lambda f: self.got.extend(
            codec_bin.decode(p, from_client=False) for p in codec_bin.unframe(f)[0]))

    def ask(self, op, **fields):
        self.got.clear()
        frame = codec_bin.encode(op, fields, to_client=False)
        self.session.receive(codec_bin.unframe(frame)[0][0])
        return self.got[-1] if self.got else None


def login(server, uid="ANDREY", pwd="1234"):
    first = Client(server)
    ans = first.ask(M.LOGIN_FIRST, id=uid, pwd=pwd, ver=M.GAME_VER)
    assert ans["op"] == 279 and ans["st"] == 1 and len(ans["token"]) == 16
    first.session.close()                      # the client hangs up after 279 (g:1912-1920)
    c = Client(server)
    prof = c.ask(M.LOGIN, id=uid, ver=M.GAME_VER, token=ans["token"])
    assert prof["op"] == 263 and prof["st"] == 1
    return c, prof


@pytest.fixture(params=["sqlite", "memory"])
def server(request):
    from pow_server.storage import MemoryStorage, Storage
    st = Storage() if request.param == "sqlite" else MemoryStorage()
    return GameServer(st, notices=[["Welcome to the", "new server!"], ["Page two"]],
                      rng=random.Random(7))


def test_login_creates_account_and_profile(server):
    c, prof = login(server)
    assert prof["name"] == "ANDREY" and prof["level"] == 1 and prof["slots"] == [3, 99, 99, 99]
    assert prof["notices"] == 2
    page = c.ask(M.NOTICE, page=1)
    assert page["lines"][:2] == ["Welcome to the", "new server!"] and page["remaining"] == 1
    assert c.ask(M.NOTICE, page=2)["remaining"] == 0
    _, again = login(server)
    assert again["notices"] == 0               # notices are shown once


def test_notices_survive_a_dropped_connection(server):
    c, prof = login(server)
    assert prof["notices"] == 2
    c.ask(M.NOTICE, page=1)
    c.session.close()                          # dropped before the last page
    c, prof = login(server)
    assert prof["notices"] == 2
    c.ask(M.NOTICE, page=1)
    c.ask(M.NOTICE, page=2)
    _, prof = login(server)
    assert prof["notices"] == 0


def test_login_errors(server):
    login(server)
    c = Client(server)
    assert c.ask(M.LOGIN_FIRST, id="ANDREY", pwd="9999", ver="0111")["reason"] == M.REASON_BAD_PASSWORD
    assert c.ask(M.LOGIN_FIRST, id="ab", pwd="1234", ver="0111")["st"] != 1
    assert c.ask(M.LOGIN, id="NOBODY", ver="0111")["st"] == M.LOGIN_NOT_REGISTERED
    assert c.ask(M.LOGIN, id="ANDREY", ver="0111")["st"] == M.LOGIN_BAD_TOKEN       # no token
    assert c.ask(M.LOGIN, id="ANDREY", ver="0111", token="0" * 16)["st"] == M.LOGIN_BAD_TOKEN
    assert c.ask(M.ATTRIBUTES) is None         # not logged in: ignored


def test_no_auto_register():
    s = GameServer(auto_register=False)
    assert Client(s).ask(M.LOGIN_FIRST, id="ANDREY", pwd="1234", ver="0111")["reason"] == M.REASON_NO_ID


def test_legacy_login_without_token():
    s = GameServer(require_token=False)
    login(s)
    assert Client(s).ask(M.LOGIN, id="ANDREY", ver="0111")["st"] == 1


def test_second_login_kicks_the_first(server):
    a, _ = login(server)
    b, _ = login(server)
    assert a.got[-1]["op"] == M.KICKED and a.session.closed and not b.session.closed
    assert server.online["ANDREY"] is b.session


def test_display_name_and_quotes(server):
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "OLGA")
    assert a.ask(M.NAME_SET, name="Warrior")["st"] == 1
    assert b.ask(M.NAME_SET, name="WARRIOR")["st"] == M.ERR_NAME_EXISTS
    assert b.ask(M.NAME_SET, name="bad name")["st"] == M.ERR_NOT_ACCEPTABLE
    assert a.ask(M.QUOTE_START, quote="Fight me!")["st"] == 1
    assert a.ask(M.QUOTE_WIN, quote="")["st"] == M.ERR_NOT_ACCEPTABLE
    _, prof = login(server, "ANDREY")
    assert prof["name"] == "Warrior" and prof["quote_start"] == "Fight me!"


def test_character_screens(server):
    c, _ = login(server)
    att = c.ask(M.ATTRIBUTES)
    assert att["op"] == 1288 and att["hp"] > 0
    sk = c.ask(M.SKILLS)
    assert sk["n"] == 1 and sk["skills"] == [{"id": 3, "level": 1}]
    assert c.ask(M.SKILL_SLOTS, slots=[99, 3, 99, 99])["st"] == 1
    assert c.ask(M.SKILL_SLOTS, slots=[4, 99, 99, 99])["st"] != 1      # not learned
    assert c.ask(M.SKILL_SLOTS, slots=[3, 3, 99, 99])["st"] != 1       # twice
    assert c.ask(M.RECORDS)["op"] == 1297
    assert c.ask(M.EXP_FAME_GOLD)["gold"] == 0


def test_options(server):
    c, _ = login(server)
    assert c.ask(M.OPTIONS)["invitation"] == 1
    assert c.ask(M.OPTIONS_SET, invitation=0)["st"] == 1
    assert c.ask(M.OPTIONS)["invitation"] == 0
    assert c.ask(M.OPTIONS_SET, invitation=5)["st"] != 1


def test_ranking(server):
    fame = {"AAAA": 5, "BBBB": 50, "CCCC": 20, "DDDD": 1, "EEEE": 9}
    clients = {}
    for uid, f in fame.items():
        clients[uid], _ = login(server, uid)
        clients[uid].session.char.mp_fame = f
        clients[uid].session.save()
    me = clients["EEEE"]
    assert me.ask(M.RANK_MINE, cat=1) == {"op": 1301, "st": 1, "rank": 3, "value": 9}
    top = me.ask(M.RANK_LIST, code=11, page=1)       # Fame, Top Rankers
    assert [r["id"] for r in top["rows"]] == ["BBBB", "CCCC", "EEEE"]
    near = clients["DDDD"].ask(M.RANK_LIST, code=12, page=1)   # Fame, Ranks Near Me (last)
    assert [r["rank"] for r in near["rows"]] == [3, 4, 5]
    assert me.ask(M.RANK_LIST, code=99, page=1)["st"] != 1


def test_ranking_always_three_rows(server):
    """The client draws 3 boxes whatever arrives, so a short table is padded (g:612-622)."""
    c, _ = login(server, "SOLO")
    rows = c.ask(M.RANK_LIST, code=21, page=1)["rows"]
    assert [r["id"] for r in rows] == ["SOLO", "", ""]


def test_other_modes_not_there_yet(server):
    c, _ = login(server)
    assert c.ask(M.MATCH, mode=1) == {"op": 513, "st": -11}
    assert c.ask(M.MATCH, mode=2) == {"op": 513, "st": -11}
    assert c.ask(M.INVITE, mode=0, id="SOMEONE")["st"] == -11


def _duel(c, action=0, hit=88, rounds=60):
    """Play a duel to the end with one action; returns (513, 514, every 1028, 1032)."""
    c.ask(M.MATCH, mode=0)
    room, fighter, ready = c.got
    turns = []
    for _ in range(rounds):
        ans = c.ask(M.ROUND_READY)
        if ans["op"] == M.BATTLE_END:
            return room, fighter, turns, ans
        assert ans["op"] == M.ROUND_START and ans["st"] == 1
        turns.append(c.ask(M.TURN, target=1, action=action, hit=hit))
    raise AssertionError("the duel did not end in %d rounds" % rounds)


def test_duel_vs_cpu(server):
    c, prof = login(server)
    room, fighter, turns, end = _duel(c)
    assert room["op"] == 513 and room["st"] == 1 and room["slot"] == 0 and room["mode"] == 0
    assert fighter["op"] == 514 and fighter["slot"] == 1
    assert 30 <= fighter["face"] <= 33                      # CPU fighter (g:2197-2206)
    assert 3 <= len(turns) <= 40
    for t in turns:
        assert t["op"] == 1028 and t["st"] == 1 and 1 <= len(t["records"]) <= 2
        for r in t["records"]:
            assert r["action"] not in (1, 2)                # stances never get a record
            assert 0 <= r["actor_mp"] <= 100 and r["actor_hp"] >= 0
    last = turns[-1]["records"][-1]
    assert last["target_hp"] == 0 or last["actor_hp"] == 0 or any(
        r["target_hp"] == 0 for t in turns[-1:] for r in t["records"])
    assert end["op"] == 1032 and end["win"] in (0, 1) and end["loot"] == "NONE"
    ch = server.storage.load("ANDREY")
    assert (ch.wins, ch.losses) == ((1, 0) if end["win"] else (0, 1))
    assert c.session.battle is None
    c.ask(M.MATCH, mode=0)                                  # a new duel can start
    assert [m["op"] for m in c.got] == [513, 514, 1024] and c.got[0]["st"] == 1


def test_duel_attacking_with_perfect_hits_usually_wins(server):
    wins = 0
    for i in range(6):
        c, _ = login(server, "PLAYER" + "ABCDEF"[i])
        wins += _duel(c, hit=100)[3]["win"]
    assert wins >= 4


def test_leaving_a_duel_counts_as_a_loss(server):
    c, _ = login(server)
    c.ask(M.MATCH, mode=0)
    c.ask(M.ROUND_READY)
    c.session.close()                    # Exit Battle: the client hangs up (g:2990-2997)
    ch = server.storage.load("ANDREY")
    assert (ch.wins, ch.losses) == (0, 1)
    c2, prof = login(server)
    assert prof["losses"] == 1
    c2.ask(M.MATCH, mode=0)
    assert c2.got[0]["st"] == 1


def test_turn_without_a_battle_is_ignored(server):
    c, _ = login(server)
    assert c.ask(M.TURN, target=1, action=0, hit=50) is None
    assert c.ask(M.ROUND_READY) is None


def test_garbage_is_ignored(server):
    c = Client(server)
    c.session.receive(b"\x01")
    c.session.receive(b"\x39\x30")              # unknown opcode
    assert c.got == []


def test_storage_survives_restart(tmp_path):
    from pow_server.storage import Storage
    db = str(tmp_path / "mp.sqlite")
    s = GameServer(Storage(db))
    c, _ = login(s)
    c.ask(M.NAME_SET, name="Keep")
    s2 = GameServer(Storage(db))
    _, prof = login(s2)
    assert prof["name"] == "Keep"
