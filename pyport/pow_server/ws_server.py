"""The standalone server (PHASE_9 tasks 9.20-9.23).

    python -m pow_server                          # ws://0.0.0.0:28200, data in mp_server.sqlite
    python -m pow_server --port 8765 --db x.sqlite --tcp-port 28200 --legacy

WebSocket: one binary message = one whole frame (u16 length + payload), exactly the bytes the
original sent over TCP. The browser can only open WebSockets (pygbag), the desktop client uses
the same, so there is one protocol for both. Behind https the page needs wss://: put the
server behind a TLS proxy (nginx / Caddy) or pass --cert/--key.

--tcp-port: optional raw TCP gateway with the original framing, for the original jar in an
emulator with GAMEVIL_SERVER/GAMEVIL_PORT pointed here (task 9.23, untested with the real jar).
The jar logs in again with a 262 without a token, so this needs --legacy (no token check).

Gamevil Live of the single player (pow_server/live.py) is on the same port at the path /live
(ws://host:28200/live), and with --live-tcp-port on raw TCP for the original single-player jar
(its GAMEVIL_PORT was 28230). It shares the accounts with the multiplayer server.
"""
import argparse
import asyncio
import logging
import ssl

from pow_server import codec_bin
from pow_server.live import LiveServer
from pow_server.server import GameServer
from pow_server.storage import Storage

log = logging.getLogger("pow_server")

IDLE_TIMEOUT = 300.0     # seconds without any frame (the client sends a keepalive every ~10-13 s)
MAX_FRAME = 4096


async def _idle_watch(session, close):
    while not session.closed:
        await asyncio.sleep(5)
        if session.idle_seconds() > IDLE_TIMEOUT:
            await close()
            return


async def handle_ws(server, ws):
    out = asyncio.Queue()
    session = server.connect(out.put_nowait)
    peer = getattr(ws, "remote_address", None)
    log.info("ws connect %s", peer)

    async def writer():
        while True:
            data = await out.get()
            await ws.send(data)

    async def close():
        await ws.close()

    tasks = [asyncio.ensure_future(writer()), asyncio.ensure_future(_idle_watch(session, close))]
    try:
        async for data in ws:
            if isinstance(data, str) or len(data) > MAX_FRAME:
                break
            try:
                payloads, rest = codec_bin.unframe(data)
            except codec_bin.CodecError:
                break
            for p in payloads:
                session.receive(p)
            if session.closed:
                break
        while not out.empty():                 # flush answers to the last frame
            await ws.send(out.get_nowait())
    except Exception as ex:                     # connection dropped
        log.info("ws %s: %r", peer, ex)
    finally:
        session.close()
        for t in tasks:
            t.cancel()
        log.info("ws disconnect %s (%s)", peer, session.user)


async def handle_tcp(server, reader, writer):
    session = server.connect(writer.write)
    buf = b""

    async def close():
        writer.close()

    watch = asyncio.ensure_future(_idle_watch(session, close))
    try:
        while not session.closed:
            chunk = await reader.read(4096)
            if not chunk:
                break
            buf += chunk
            payloads, buf = codec_bin.unframe(buf)
            for p in payloads:
                session.receive(p)
            await writer.drain()
            if len(buf) > MAX_FRAME:
                break
    except (codec_bin.CodecError, ConnectionError):
        pass
    finally:
        session.close()
        watch.cancel()
        writer.close()


async def serve(host="0.0.0.0", port=28200, db="mp_server.sqlite", tcp_port=None, legacy=False,
                ssl_context=None, ready=None, notices=(), bots=(), match_wait=None,
                live_tcp_port=None):
    from websockets.asyncio.server import serve as ws_serve
    server = GameServer(Storage(db), require_token=not legacy, notices=notices)
    if match_wait is not None:
        server.match_wait = match_wait
    live = LiveServer(server.storage, notices=notices)

    def route(ws):
        path = getattr(getattr(ws, "request", None), "path", "") or ""
        return handle_ws(live if path.startswith("/live") else server, ws)
    if bots:
        from pow_server.bot import Bot
        bots = [Bot(server, name) for name in bots]

        async def pump():
            while True:
                for bot in bots:
                    bot.pump()
                await asyncio.sleep(0.2)
        pumper = asyncio.ensure_future(pump())  # noqa: F841 (kept alive with serve)

    async def tick():                           # matchmaking: a Duel that waited gets a CPU
        while True:
            server.tick()
            await asyncio.sleep(1)
    ticker = asyncio.ensure_future(tick())      # noqa: F841 (kept alive with serve)
    async with ws_serve(route, host, port,
                        max_size=MAX_FRAME, ssl=ssl_context) as wss:
        tcp = None
        if tcp_port is not None:
            tcp = await asyncio.start_server(lambda r, w: handle_tcp(server, r, w), host, tcp_port)
        live_tcp = None
        if live_tcp_port is not None:
            live_tcp = await asyncio.start_server(lambda r, w: handle_tcp(live, r, w), host, live_tcp_port)
        ports = [s.getsockname()[1] for s in wss.sockets]
        for t in (tcp, live_tcp):
            if t:
                ports += [s.getsockname()[1] for s in t.sockets]
        log.info("POW Multiplayer server on %s ports %s", host, ports)
        if ready is not None:
            ready.set_result((server, ports))
        try:
            await asyncio.Future()
        finally:
            for t in (tcp, live_tcp):
                if t:
                    t.close()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m pow_server", description=__doc__.split("\n")[0])
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=28200, help="WebSocket port")
    ap.add_argument("--db", default="mp_server.sqlite", help="SQLite file (:memory: = nothing kept)")
    ap.add_argument("--tcp-port", type=int, default=None, help="raw TCP gateway for the original jar")
    ap.add_argument("--legacy", action="store_true", help="no session token check (original jar)")
    ap.add_argument("--bot", action="append", default=[], metavar="ID",
                    help="keep a scripted player online that accepts every Challenge (A-Z, 4-12)")
    ap.add_argument("--match-wait", type=float, default=None, metavar="SEC",
                    help="how long a Duel waits for a live opponent before a CPU (default 60)")
    ap.add_argument("--live-tcp-port", type=int, default=None,
                    help="raw TCP Gamevil Live for the original single-player jar (was 28230)")
    ap.add_argument("--cert")
    ap.add_argument("--key")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    ctx = None
    if a.cert:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(a.cert, a.key)
    try:
        asyncio.run(serve(a.host, a.port, a.db, a.tcp_port, a.legacy, ctx, bots=a.bot,
                          match_wait=a.match_wait, live_tcp_port=a.live_tcp_port))
    except KeyboardInterrupt:
        pass
