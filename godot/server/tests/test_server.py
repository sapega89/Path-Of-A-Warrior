import asyncio
import json

import pytest
import websockets

from game_server import protocol
from game_server.net import serve
from game_server.security import Guard, Meter
from game_server.server import Session
from game_server.storage import Storage

DEVICE = "d" * 32


def req(type_, id_=1, **fields):
    return json.dumps({"type": type_, "id": id_, "v": protocol.VERSION, **fields})


def session(peer=None, guard=None):
    return Session(Storage(), guard or Guard(), peer)


def ask(s, type_, **fields):
    return json.loads(s.handle(req(type_, **fields)))


def test_hello_and_version():
    s = session()
    assert ask(s, "hello") == {"type": "hello_ok", "id": 1, "server": "mercenarys-path", "v": 1}
    old = json.loads(s.handle(json.dumps({"type": "hello", "id": 7, "v": 0})))
    assert old == {"type": "error", "id": 7, "code": "update"}
    assert json.loads(s.handle("not json"))["code"] == "bad"
    assert ask(s, "fly")["code"] == "unknown"


def test_guest_login_and_token():
    st = Storage()
    s = Session(st, Guard())
    a = ask(s, "guest_login", device=DEVICE)
    assert a["type"] == "guest_login_ok" and a["account"].startswith("g")
    again = ask(Session(st, Guard()), "guest_login", device=DEVICE)
    assert again["account"] == a["account"], "the same device, the same account"
    assert ask(Session(st, Guard()), "login", account=a["account"], token=again["token"])["type"] == "login_ok"
    assert ask(Session(st, Guard()), "login", account=a["account"], token=a["token"])["code"] == "login", \
        "an older token no longer works"
    assert ask(s, "guest_login", device="short")["code"] == "bad"


def test_hero_needs_login():
    assert ask(session(), "hero_get")["code"] == "auth"


def test_hero_saved_and_loaded():
    s = session()
    ask(s, "guest_login", device=DEVICE)
    assert ask(s, "hero_get") == {"type": "hero_get_ok", "id": 1, "hero": None, "rev": 0}
    hero = {"name": "Ivan", "level": 3}
    assert ask(s, "hero_put", hero=hero, rev=0)["rev"] == 1
    assert ask(s, "hero_get")["hero"] == hero
    assert ask(s, "hero_put", hero=hero, rev=0)["code"] == "stale", "saved since from somewhere else"
    assert ask(s, "hero_put", hero=hero, rev=1)["rev"] == 2
    assert ask(s, "hero_put", hero={"x": "y" * protocol.MAX_HERO}, rev=2)["code"] == "too_big"
    assert ask(s, "hero_put", hero=[1], rev=2)["code"] == "bad"


def test_new_accounts_are_limited_per_address():
    st, g = Storage(), Guard(new_accounts=2)
    for i in range(2):
        assert ask(Session(st, g, "1.2.3.4"), "guest_login", device="%032d" % i)["type"] == "guest_login_ok"
    assert ask(Session(st, g, "1.2.3.4"), "guest_login", device="%032d" % 9)["code"] == "limit"
    assert ask(Session(st, g, "1.2.3.4"), "guest_login", device="%032d" % 0)["type"] == "guest_login_ok", \
        "a device that has an account still logs in"


def test_meter_and_connections():
    t = [0.0]
    m = Meter(3, lambda: t[0])
    assert [m.allow() for _ in range(4)] == [True, True, True, False]
    t[0] = 1.0
    assert m.allow()
    g = Guard(max_connections=1)
    assert g.open_connection("a") and not g.open_connection("a")
    g.close_connection("a")
    assert g.open_connection("a")


def test_over_websocket():
    async def run():
        loop = asyncio.get_running_loop()
        ready = loop.create_future()
        task = asyncio.ensure_future(serve("127.0.0.1", 0, ":memory:", ready=ready))
        server = await ready
        port = list(server.sockets)[0].getsockname()[1]
        async with websockets.connect("ws://127.0.0.1:%d" % port) as ws:
            await ws.send(req("guest_login", 5, device=DEVICE))
            a = json.loads(await ws.recv())
            assert a["id"] == 5 and a["type"] == "guest_login_ok"
            await ws.send(req("hero_put", 6, hero={"name": "A"}, rev=0))
            assert json.loads(await ws.recv())["rev"] == 1
        task.cancel()
    asyncio.run(run())
