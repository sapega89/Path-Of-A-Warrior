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

PORT-EXTRA: the single player's saves (pow_server/cloud.py) are at the path /save
(ws://host:28200/save), JSON text messages, on the same accounts.

PORT-EXTRA (asked by Andrey): security settings (pow_server/security.py): limits on wrong
passwords, new accounts, connections and messages per address; --origin lets in only the pages
of the game; --require-tls refuses to start without TLS (--cert/--key, or --behind-proxy when a
proxy such as nginx / Caddy does TLS and adds X-Forwarded-For).
"""
import argparse
import asyncio
import logging
import ssl

from pow_server import cloud, codec_bin, security
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


def peer_address(ws, behind_proxy=False):
    """The client's address: the socket's, or behind a proxy the last X-Forwarded-For entry (the
    one the proxy added; earlier ones come from the client and can be made up)."""
    if behind_proxy:
        headers = getattr(getattr(ws, "request", None), "headers", None)
        fwd = headers.get("X-Forwarded-For") if headers is not None else None
        if fwd:
            return fwd.split(",")[-1].strip()
    addr = getattr(ws, "remote_address", None)
    return addr[0] if isinstance(addr, (tuple, list)) and addr else None


async def handle_ws(server, ws, peer=None, meter=None):
    out = asyncio.Queue()
    session = server.connect(out.put_nowait)
    session.peer = peer
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
                payloads, _rest = codec_bin.unframe(data)
            except codec_bin.CodecError:
                break
            if meter is not None and not all(meter.allow() for _ in payloads):
                log.info("ws %s: too many messages", peer)   # every frame counts, not the message
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


async def handle_text(server, ws, peer=None, meter=None):
    """/save: one JSON text message per frame (pow_server/cloud.py)."""
    out = asyncio.Queue()
    session = server.connect(out.put_nowait)
    session.peer = peer

    async def writer():
        while True:
            await ws.send(await out.get())

    task = asyncio.ensure_future(writer())
    try:
        async for data in ws:
            if not isinstance(data, str) or len(data) > cloud.MAX_MESSAGE:
                break
            if meter is not None and not meter.allow():
                break
            session.receive(data)
        while not out.empty():
            await ws.send(out.get_nowait())
    except Exception as ex:                     # connection dropped
        log.info("save ws: %r", ex)
    finally:
        session.close()
        task.cancel()


async def handle_tcp(server, reader, writer, guard=None):
    peer = (writer.get_extra_info("peername") or (None,))[0]
    if guard is not None and not guard.open_connection(peer):
        writer.close()
        return
    session = server.connect(writer.write)
    session.peer = peer
    meter = guard.message_meter() if guard is not None else None
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
            if meter is not None and not all(meter.allow() for _ in payloads):
                break                              # too many messages
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
        if guard is not None:
            guard.close_connection(peer)


async def serve(host="0.0.0.0", port=28200, db="mp_server.sqlite", tcp_port=None, legacy=False,
                ssl_context=None, ready=None, notices=(), bots=(), match_wait=None,
                live_tcp_port=None, server_bots=True, guard=None, origins=None, behind_proxy=False):
    """guard: security.Guard (None = the default limits); origins: the page addresses
    allowed to connect (None = any; clients without an Origin header, the desktop game, are
    always let in)."""
    from websockets.asyncio.server import serve as ws_serve
    if legacy:
        log.warning("--legacy: the session token is not checked (anyone who knows a UserID "
                    "can log in with 262); use it only for the original jar on a private network")
    guard = guard or security.Guard()
    server = GameServer(Storage(db), require_token=not legacy, notices=notices)
    if match_wait is not None:
        server.match_wait = match_wait
    if server_bots:                             # PORT-EXTRA: someone to Challenge when alone
        server.add_bots()
    live = LiveServer(server.storage, notices=notices)
    saves = cloud.CloudServer(server.storage)
    for s in (server, live, saves):
        s.guard = guard
    background = []                             # tasks that live as long as serve()

    async def route(ws):
        peer = peer_address(ws, behind_proxy)
        if not guard.open_connection(peer):
            log.info("ws %s: too many connections", peer)
            await ws.close(1008, "too many connections")
            return
        try:
            path = getattr(getattr(ws, "request", None), "path", "") or ""
            meter = guard.message_meter()
            if path.startswith("/save"):
                await handle_text(saves, ws, peer, meter)
            else:
                await handle_ws(live if path.startswith("/live") else server, ws, peer, meter)
        finally:
            guard.close_connection(peer)
    if bots:
        from pow_server.bot import Bot
        bots = [Bot(server, name) for name in bots]

        async def pump():
            while True:
                for bot in bots:
                    bot.pump()
                await asyncio.sleep(0.2)
        background.append(asyncio.ensure_future(pump()))   # kept alive with serve

    async def tick():                           # matchmaking: a Duel that waited gets a CPU
        while True:
            server.tick()
            await asyncio.sleep(1)
    background.append(asyncio.ensure_future(tick()))       # kept alive with serve
    allowed = None if not origins else [*origins, None]   # None: no Origin header (desktop game)
    async with ws_serve(route, host, port, origins=allowed,
                        max_size=cloud.MAX_MESSAGE, ssl=ssl_context) as wss:
        tcp = None
        if tcp_port is not None:
            tcp = await asyncio.start_server(lambda r, w: handle_tcp(server, r, w, guard), host, tcp_port)
        live_tcp = None
        if live_tcp_port is not None:
            live_tcp = await asyncio.start_server(lambda r, w: handle_tcp(live, r, w, guard), host,
                                                  live_tcp_port)
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
    ap.add_argument("--no-server-bots", action="store_true",
                    help="no server bots (BLADE, RAVEN, TIGER, SHADOW, IRONFIST) to Challenge")
    ap.add_argument("--match-wait", type=float, default=None, metavar="SEC",
                    help="how long a Duel waits for a live opponent before a CPU (default 60)")
    ap.add_argument("--live-tcp-port", type=int, default=None,
                    help="raw TCP Gamevil Live for the original single-player jar (was 28230)")
    ap.add_argument("--cert", help="TLS certificate (PEM): the server speaks wss://")
    ap.add_argument("--key", help="TLS private key (PEM)")
    sec = ap.add_argument_group("security (PORT-EXTRA, pow_server/security.py)")
    sec.add_argument("--require-tls", action="store_true",
                     help="refuse to start without TLS: --cert/--key, or --behind-proxy")
    sec.add_argument("--behind-proxy", action="store_true",
                     help="a TLS proxy (nginx / Caddy) in front: the address is X-Forwarded-For")
    sec.add_argument("--origin", action="append", default=[], metavar="URL",
                     help="a page allowed to connect, e.g. https://pow.example (repeat; default any)")
    sec.add_argument("--login-fails", type=int, default=security.LOGIN_FAILS, metavar="N",
                     help="wrong passwords for one UserID / address before a block (default %(default)s)")
    sec.add_argument("--login-window", type=float, default=security.LOGIN_WINDOW, metavar="SEC",
                     help="... counted within this time (default %(default)s)")
    sec.add_argument("--login-block", type=float, default=security.LOGIN_BLOCK, metavar="SEC",
                     help="how long the block lasts (default %(default)s)")
    sec.add_argument("--new-accounts", type=int, default=security.NEW_ACCOUNTS, metavar="N",
                     help="new accounts from one address per hour (default %(default)s)")
    sec.add_argument("--max-connections", type=int, default=security.MAX_CONNECTIONS, metavar="N",
                     help="open connections from one address (default %(default)s)")
    sec.add_argument("--max-messages", type=int, default=security.MAX_MESSAGES, metavar="N",
                     help="messages per second on one connection, then it is closed (default %(default)s)")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    ctx = None
    if a.cert:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.load_cert_chain(a.cert, a.key)
    if a.require_tls and ctx is None and not a.behind_proxy:
        ap.error("--require-tls: give --cert/--key, or --behind-proxy when a proxy does TLS")
    if a.require_tls and (a.tcp_port or a.live_tcp_port):
        ap.error("--require-tls: the raw TCP ports have no TLS")
    guard = security.Guard(login_fails=a.login_fails, login_window=a.login_window,
                           login_block=a.login_block, new_accounts=a.new_accounts,
                           max_connections=a.max_connections, max_messages=a.max_messages)
    try:
        asyncio.run(serve(a.host, a.port, a.db, a.tcp_port, a.legacy, ctx, bots=a.bot,
                          match_wait=a.match_wait, live_tcp_port=a.live_tcp_port,
                          server_bots=not a.no_server_bots, guard=guard,
                          origins=a.origin or None, behind_proxy=a.behind_proxy))
    except KeyboardInterrupt:
        pass
