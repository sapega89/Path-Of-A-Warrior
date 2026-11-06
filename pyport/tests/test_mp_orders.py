"""orders of the online game (pow_server/orders.py, plan item 22)."""
import random

import pytest

from pow_server import messages as M
from pow_server import orders
from pow_server.server import GameServer
from tests.test_mp_server import _ops, _play, login


@pytest.fixture(params=["sqlite", "memory"])
def server(request):
    from pow_server.storage import MemoryStorage, Storage
    st = Storage() if request.param == "sqlite" else MemoryStorage()
    return GameServer(st, rng=random.Random(7), match_wait=0)


def test_no_order_at_first(server):
    a, _ = login(server, "ANDREY")
    info = a.ask(M.ORDER_INFO)
    assert info["op"] == M.ORDER_INFO_ANS and info["st"] == 1
    assert info["name"] == "" and info["rows"] == []


def test_create_join_list_and_leave(server):
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    c, _ = login(server, "CYRIL")
    assert a.ask(M.ORDER_CREATE, name="WOLVES")["st"] == 1
    assert b.ask(M.ORDER_CREATE, name="WOLVES")["st"] == M.ERR_NAME_EXISTS
    assert b.ask(M.ORDER_CREATE, name="AB")["st"] == M.ERR_NOT_ACCEPTABLE
    assert b.ask(M.ORDER_JOIN, name="BEARS")["st"] == M.ERR_ORDER_NONE
    assert b.ask(M.ORDER_JOIN, name="WOLVES")["st"] == 1
    assert b.ask(M.ORDER_JOIN, name="WOLVES")["st"] == M.ERR_ORDER_IN
    assert a.ask(M.ORDER_CREATE, name="BEARS")["st"] == M.ERR_ORDER_IN
    c.ask(M.ORDER_JOIN, name="WOLVES")
    c.session.close()                                  # C is offline now
    info = b.ask(M.ORDER_INFO)
    assert info["name"] == "WOLVES"
    assert [(r["id"], r["online"], r["leader"]) for r in info["rows"]] == [
        ("ANDREY", 1, 1), ("BORYS", 1, 0), ("CYRIL", 0, 0)]             # the leader first
    assert info["rows"][0]["level"] == 1
    assert b.ask(M.ORDER_LEAVE)["st"] == 1
    assert b.ask(M.ORDER_INFO)["name"] == ""
    assert [r["id"] for r in a.ask(M.ORDER_INFO)["rows"]] == ["ANDREY", "CYRIL"]
    assert server.storage.load("BORYS").order == ""
    a.ask(M.ORDER_LEAVE)                               # the leader leaves: the oldest member leads
    rows = b.ask(M.ORDER_JOIN, name="WOLVES") and b.ask(M.ORDER_INFO)["rows"]
    assert [(r["id"], r["leader"]) for r in rows] == [("CYRIL", 1), ("BORYS", 0)]


def test_the_last_member_leaving_frees_the_name(server):
    a, _ = login(server, "ANDREY")
    a.ask(M.ORDER_CREATE, name="WOLVES")
    a.ask(M.ORDER_LEAVE)
    assert orders.get(server.storage, "WOLVES") is None
    b, _ = login(server, "BORYS")
    assert b.ask(M.ORDER_CREATE, name="WOLVES")["st"] == 1


def test_thirty_members_at_most(server):
    a, _ = login(server, "ANDREY")
    a.ask(M.ORDER_CREATE, name="WOLVES")
    doc = orders.get(server.storage, "WOLVES")
    doc["members"] += ["M" * 4 + chr(65 + i // 26) + chr(65 + i % 26) for i in range(29)]
    server.storage.live_put("order:WOLVES", doc)
    b, _ = login(server, "BORYS")
    assert b.ask(M.ORDER_JOIN, name="WOLVES")["st"] == M.ERR_ORDER_FULL


def test_membership_survives_a_new_login(server):
    a, _ = login(server, "ANDREY")
    a.ask(M.ORDER_CREATE, name="WOLVES")
    a.session.close()
    a, _ = login(server, "ANDREY")
    assert a.ask(M.ORDER_INFO)["name"] == "WOLVES"


def _members(server):
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    a.ask(M.ORDER_CREATE, name="WOLVES")
    b.ask(M.ORDER_JOIN, name="WOLVES")
    return a, b


def test_team_duel_needs_the_same_order(server):
    a, _ = login(server, "ANDREY")
    login(server, "BORYS")
    assert a.ask(M.INVITE, mode=M.INVITE_TEAM, id="BORYS")["st"] == M.ERR_NOT_MEMBER
    assert a.session.room is None


def test_team_duel_two_members_on_one_side(server):
    a, b = _members(server)
    b.got.clear()
    a.ask(M.INVITE, mode=M.INVITE_TEAM, id="BORYS")
    assert _ops(a) == [769, 514, 514, 514, 1024] and _ops(b) == [770, 514, 514, 514, 1024]
    assert a.got[0]["mode"] == 1 and b.got[0]["mode"] == 1          # a 2-on-2 Duel for the clients
    assert a.got[0]["slot"] == 0 and b.got[0]["slot"] == 2
    fs = a.session.room.battle.fighters
    assert not fs[0].cpu and not fs[2].cpu and fs[1].cpu and fs[3].cpu
    assert fs[0].team == fs[2].team == 0
    _turns, ea, eb = _play(a, b, rounds=200)
    assert ea["win"] == eb["win"]                                     # one side, one result
    assert a.session.room is None and b.session.room is None


def test_mission_invite_from_the_order(server):
    a, b = _members(server)
    b.got.clear()
    a.ask(M.INVITE, mode=2, id="BORYS")
    assert a.got[0]["op"] == M.INVITE_ANS and b.got[0]["op"] == M.INVITED and b.got[0]["slot"] == 2


def test_team_duel_partner_busy_or_offline(server):
    a, b = _members(server)
    b.ask(M.MATCH, mode=0)                                           # B is in a duel now
    assert a.ask(M.INVITE, mode=M.INVITE_TEAM, id="BORYS")["st"] == -5
    b.session.close()
    assert a.ask(M.INVITE, mode=M.INVITE_TEAM, id="BORYS")["st"] == -3


def test_records_carry_the_order_name(server):
    a, _ = login(server, "ANDREY")
    assert a.ask(M.RECORDS)["order"] == ""
    a.ask(M.ORDER_CREATE, name="WOLVES")
    assert a.ask(M.RECORDS)["order"] == "WOLVES"
