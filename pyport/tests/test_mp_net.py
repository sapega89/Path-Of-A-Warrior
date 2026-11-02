"""PHASE_9: the transports. WebSocket and the TCP gateway against a real server on localhost."""
import asyncio

import pytest

from pow_mp.net.transport import LocalTransport, WebSocketTransport, make_transport
from pow_server import codec_bin, messages as M
from pow_server.server import GameServer


def enc(op, **f):
    return codec_bin.encode(op, f, to_client=False)


def dec(payloads):
    return [codec_bin.decode(p, from_client=False) for p in payloads]


def test_make_transport():
    assert isinstance(make_transport("local"), LocalTransport)
    assert isinstance(make_transport("ws://localhost:1"), WebSocketTransport)


def test_local_transport_login():
    t = LocalTransport(GameServer())
    t.open()
    t.send(enc(M.LOGIN_FIRST, id="LOCAL", pwd="1234", ver="0111"))
    tok = dec(t.poll())[0]["token"]
    t.close()
    t.open()
    t.send(enc(M.LOGIN, id="LOCAL", ver="0111", token=tok))
    assert dec(t.poll())[0]["st"] == 1


async def _wait(cond, timeout=5.0):
    end = asyncio.get_running_loop().time() + timeout
    while not cond():
        if asyncio.get_running_loop().time() > end:
            raise TimeoutError
        await asyncio.sleep(0.01)


def test_websocket_and_tcp_end_to_end():
    pytest.importorskip("websockets")
    from pow_server.ws_server import serve

    async def run():
        ready = asyncio.get_running_loop().create_future()
        task = asyncio.ensure_future(serve("127.0.0.1", 0, ":memory:", tcp_port=0, ready=ready))
        server, (ws_port, tcp_port) = await asyncio.wait_for(ready, 5)
        try:
            t = WebSocketTransport("ws://127.0.0.1:%d" % ws_port)
            t.open()
            await _wait(lambda: t.connected)
            t.send(enc(M.LOGIN_FIRST, id="WEBUSER", pwd="5678", ver="0111"))
            got = []
            await _wait(lambda: got.extend(dec(t.poll())) or got)
            tok = got[0]["token"]
            t.close()
            t.open()
            await _wait(lambda: t.connected)
            t.send(enc(M.LOGIN, id="WEBUSER", ver="0111", token=tok))
            t.send(enc(M.ATTRIBUTES))
            got = []
            await _wait(lambda: got.extend(dec(t.poll())) or len(got) >= 2)
            assert got[0]["op"] == 263 and got[0]["st"] == 1 and got[1]["op"] == 1288
            t.close()

            # raw TCP with the original framing (the jar's way); the server is not --legacy,
            # so a 262 without a token is refused, which is what this server must do
            r, w = await asyncio.open_connection("127.0.0.1", tcp_port)
            w.write(enc(M.LOGIN, id="WEBUSER", ver="0111"))
            await w.drain()
            n = int.from_bytes(await r.readexactly(2), "little")
            msg = codec_bin.decode(await r.readexactly(n - 2), from_client=False)
            assert msg == {"op": 263, "st": M.LOGIN_BAD_TOKEN}
            w.close()

            # a dropped server -> the transport says failed
            t2 = WebSocketTransport("ws://127.0.0.1:1")
            t2.open()
            await _wait(lambda: t2.failed, 15)
        finally:
            task.cancel()

    asyncio.run(run())
