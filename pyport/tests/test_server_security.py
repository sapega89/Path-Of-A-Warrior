"""PORT-EXTRA: the server's security settings (pow_server/security.py, ws_server.py)."""
import asyncio
import json

import pytest

from pow_server import security
from pow_server.cloud import CloudServer
from pow_server.storage import open_storage


class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


def guard(clock, **kw):
    return security.Guard(clock=clock, **kw)


def test_wrong_passwords_block_the_account_then_expire():
    clock, st = Clock(), open_storage()
    st.create_account("ANDREY", "1234")
    g = guard(clock, login_fails=3, login_block=60)
    for _ in range(3):
        assert not g.check_password(st, "ANDREY", "0000", "1.2.3.4")
    assert not g.check_password(st, "ANDREY", "1234", "5.6.7.8")   # blocked, even the right one
    clock.t += 61
    assert g.check_password(st, "ANDREY", "1234", "5.6.7.8")


def test_wrong_passwords_block_the_address_for_every_account():
    clock, st = Clock(), open_storage()
    for uid in ("AAAA", "BBBB", "CCCC", "DDDD"):
        st.create_account(uid, "1234")
    g = guard(clock, login_fails=3)
    for uid in ("AAAA", "BBBB", "CCCC"):                          # one wrong guess per account
        assert not g.check_password(st, uid, "0000", "1.2.3.4")
    assert not g.check_password(st, "DDDD", "1234", "1.2.3.4")   # this address is blocked
    assert g.check_password(st, "DDDD", "1234", "9.9.9.9")


def test_old_failures_and_a_right_password_reset_the_count():
    clock, st = Clock(), open_storage()
    st.create_account("ANDREY", "1234")
    g = guard(clock, login_fails=3, login_window=100)
    g.check_password(st, "ANDREY", "0000")
    g.check_password(st, "ANDREY", "0000")
    clock.t += 101                                                # the window passed
    g.check_password(st, "ANDREY", "0000")
    assert g.check_password(st, "ANDREY", "1234")
    g.check_password(st, "ANDREY", "0000")
    g.check_password(st, "ANDREY", "0000")
    assert g.check_password(st, "ANDREY", "1234")                 # the right one cleared it


def test_new_accounts_and_connections_per_address():
    clock = Clock()
    g = guard(clock, new_accounts=2, new_accounts_window=100, max_connections=2)
    assert g.may_create("1.2.3.4") and g.may_create("1.2.3.4")
    assert not g.may_create("1.2.3.4") and g.may_create("5.6.7.8")
    clock.t += 101
    assert g.may_create("1.2.3.4")
    assert g.open_connection("1.2.3.4") and g.open_connection("1.2.3.4")
    assert not g.open_connection("1.2.3.4")
    g.close_connection("1.2.3.4")
    assert g.open_connection("1.2.3.4")


def test_message_meter():
    clock = Clock()
    m = security.MessageMeter(3, clock)
    assert all(m.allow() for _ in range(3))
    assert not m.allow()
    clock.t += 1.5
    assert m.allow()


def test_save_login_goes_through_the_guard():
    st = open_storage()
    st.create_account("ANDREY", "1234")
    server = CloudServer(st)
    server.guard = security.Guard(login_fails=2)
    out = []
    s = server.connect(out.append)
    s.peer = "1.2.3.4"
    for pwd in ("0000", "0000", "1234"):
        s.receive(json.dumps({"op": "login", "id": "ANDREY", "pwd": pwd}))
    assert [json.loads(x)["ok"] for x in out] == [False, False, False]


def test_live_registration_limit():
    import struct

    from pow_server.live import LiveServer
    server = LiveServer(open_storage())
    server.guard = security.Guard(new_accounts=1)
    for uid in ("AAAA", "BBBB"):
        s = server.connect(lambda f: None)
        s.peer = "1.2.3.4"
        s.receive(struct.pack("<H", 530) + uid.encode().ljust(12, b"\0") + b"1234".ljust(16, b"\0")
                  + b"1501" + bytes(8))
    assert server.storage.has_account("AAAA") and not server.storage.has_account("BBBB")


# --- the real server ------------------------------------------------------------------------
async def _serve(**kw):
    from pow_server.ws_server import serve
    ready = asyncio.get_running_loop().create_future()
    task = asyncio.ensure_future(serve("127.0.0.1", 0, ":memory:", ready=ready, server_bots=False, **kw))
    _server, ports = await asyncio.wait_for(ready, 5)
    return task, ports[0]


def test_origin_check_lets_in_the_game_page_and_the_desktop():
    from websockets.asyncio.client import connect
    from websockets.exceptions import InvalidStatus

    async def go():
        task, port = await _serve(origins=["https://pow.example"])
        try:
            async with connect(f"ws://127.0.0.1:{port}/save") as ws:            # desktop: no Origin
                await ws.send(json.dumps({"op": "get"}))
                assert json.loads(await ws.recv())["err"] == "login first"
            async with connect(f"ws://127.0.0.1:{port}/save", origin="https://pow.example") as ws:
                await ws.send(json.dumps({"op": "get"}))
                await ws.recv()
            with pytest.raises(InvalidStatus):
                await connect(f"ws://127.0.0.1:{port}/save", origin="https://evil.example")
        finally:
            task.cancel()
    asyncio.run(go())


def test_too_many_connections_and_messages_are_closed():
    from websockets.asyncio.client import connect
    from websockets.exceptions import ConnectionClosed

    async def go():
        task, port = await _serve(guard=security.Guard(max_connections=2, max_messages=5))
        try:
            a = await connect(f"ws://127.0.0.1:{port}/save")
            b = await connect(f"ws://127.0.0.1:{port}/save")
            c = await connect(f"ws://127.0.0.1:{port}/save")
            with pytest.raises(ConnectionClosed):
                await asyncio.wait_for(c.recv(), 5)                  # the third one is closed
            await b.close()
            async def flood():                                       # a flood closes the connection
                for _ in range(20):
                    await a.send(json.dumps({"op": "get"}))
                for _ in range(20):
                    await asyncio.wait_for(a.recv(), 5)
            with pytest.raises(ConnectionClosed):
                await flood()
        finally:
            task.cancel()
    asyncio.run(go())


def test_every_frame_counts_on_websocket_and_raw_tcp():
    """Many protocol frames in one WebSocket message, or on the raw TCP port, count one by one."""
    import struct

    from websockets.asyncio.client import connect
    from websockets.exceptions import ConnectionClosed

    from pow_server import codec_bin

    burst = b"".join(codec_bin.frame(struct.pack("<H", 288)) for _ in range(20))

    async def go():
        from pow_server.ws_server import serve
        ready = asyncio.get_running_loop().create_future()
        task = asyncio.ensure_future(serve("127.0.0.1", 0, ":memory:", tcp_port=0, ready=ready,
                                           server_bots=False, guard=security.Guard(max_messages=5)))
        _server, (ws_port, tcp_port) = await asyncio.wait_for(ready, 5)
        try:
            async with connect(f"ws://127.0.0.1:{ws_port}/") as ws:
                await ws.send(burst)

                async def read_all():
                    while True:
                        await asyncio.wait_for(ws.recv(), 5)
                with pytest.raises(ConnectionClosed):
                    await read_all()
            reader, writer = await asyncio.open_connection("127.0.0.1", tcp_port)
            writer.write(burst)
            await writer.drain()
            got = b""
            while True:                                   # read until the server hangs up
                chunk = await asyncio.wait_for(reader.read(4096), 5)
                if not chunk:
                    break
                got += chunk
            writer.close()
            assert len(codec_bin.unframe(got)[0]) <= 5
        finally:
            task.cancel()
    asyncio.run(go())
