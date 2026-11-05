"""Where the MP client's frames go (PHASE_9 §3): the replacement of's socket.

 opened socket://POW_SERVER:POW_PORT in its own thread and called g.a(k) for
every frame. Here the game loop calls poll() once per tick and gets the payloads received
since the last call (frame length removed, opcode first), and send() takes a whole frame
(what e.b() wrote). These implementations with the same interface:

- LocalTransport: the server runs inside the game (9a: bots, no network).
- WebSocketTransport: ws:// or wss:// to `python -m pow_server` (9b). Desktop: the
  `websockets` package on the game's asyncio loop.

make_transport(config.MP_SERVER) picks one: "local" or a ws(s):// URL.
"""
import asyncio
import collections

from pow_server import codec_bin


class Transport:
    connected = False
    failed = False  # connect failed or the connection dropped ( in the client)

    def open(self):
        """Start connecting; connected / failed tell the result on a later tick."""
        raise NotImplementedError

    def send(self, frame: bytes):
        raise NotImplementedError

    def poll(self):
        """Payloads received since the last call."""
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class LocalTransport(Transport):
    """The in-game server: one shared GameServer, a fresh Session per open()."""
    _server = None
    _bots = []

    def __init__(self, server=None):
        self.server = server
        self.session = None
        self.inbox = collections.deque()

    @classmethod
    def shared_server(cls):
        if cls._server is None:
            import os

            import config
            from pow_server.server import GameServer
            from pow_server.storage import open_storage
            path = ":memory:"
            os.makedirs(config.SAVE_DIR, exist_ok=True)
            path = os.path.join(config.SAVE_DIR, "mp_local.sqlite")
            rng = None
            if os.environ.get("POW_SEED"):        # headless runs (tools/shot.py) repeat exactly
                import random
                rng = random.Random(int(os.environ["POW_SEED"]))
            # the offline game has nobody to wait for: a Duel gets its CPU fighter at once
            kw = {}
            from pow.midp import system
            if system.is_virtual():              # headless runs: the chat's rate limit follows the game clock
                kw["clock"] = lambda: system.currentTimeMillis() / 1000
            cls._server = GameServer(open_storage(path), rng=rng, match_wait=0, **kw)
            # scripted players to Challenge / Invite in the offline game (pow_server/bot.py)
            from pow_server.bot import Bot
            names = os.environ.get("POW_MP_BOTS", "RIVAL").split(",")
            cls._bots = []
            for n in names:
                try:
                    cls._bots.append(Bot(cls._server, n.strip()))
                except Exception as ex:        # a taken ID with another password: no bot
                    print(f"MP bot {n!r} not started: {ex!r}")
        return cls._server

    def open(self):
        server = self.server or self.shared_server()
        self.inbox.clear()
        self.session = server.connect(self._deliver)
        self.connected, self.failed = True, False

    def _deliver(self, frame):
        payloads, _ = codec_bin.unframe(frame)
        self.inbox.extend(payloads)

    def send(self, frame):
        if not self.connected:
            return
        payloads, _ = codec_bin.unframe(frame)
        for p in payloads:
            self.session.receive(p)
        if self.session.closed:          # the server dropped us (e.g. 280 kicked)
            self.connected = False

    def poll(self):
        for bot in self._bots:
            bot.pump()
        server = self.server or self._server
        if getattr(server, "tick", None) is not None:
            server.tick()
        out = list(self.inbox)
        self.inbox.clear()
        return out

    def close(self):
        if self.session is not None:
            self.session.close()
        self.connected = False


class WebSocketTransport(Transport):
    def __init__(self, url):
        self.url = url
        self.inbox = collections.deque()
        self._ws = None
        self._task = None
        self._out = None

    def open(self):
        self.close()
        self.connected = self.failed = False
        self.inbox.clear()
        self._out = asyncio.Queue()
        self._task = asyncio.ensure_future(self._run_desktop())

    # --- desktop: websockets on the game loop ---------------------------------
    async def _run_desktop(self):
        try:
            from websockets.asyncio.client import connect
            async with connect(self.url, max_size=65536, open_timeout=10) as ws:
                self._ws = ws
                self.connected = True
                sender = asyncio.ensure_future(self._send_loop(ws))
                try:
                    async for data in ws:
                        if isinstance(data, bytes):
                            self.inbox.extend(codec_bin.unframe(data)[0])
                finally:
                    sender.cancel()
        except asyncio.CancelledError:
            raise
        except Exception as ex:
            print("MP connection failed:", repr(ex))
        self.connected = False
        self.failed = True

    async def _send_loop(self, ws):
        while True:
            await ws.send(await self._out.get())

    def send(self, frame):
        if not self.connected:
            return
        self._out.put_nowait(frame)

    def poll(self):
        out = list(self.inbox)
        self.inbox.clear()
        return out

    def close(self):
        if self._task is not None:
            self._task.cancel()
            self._task = None
        self._ws = None
        self.connected = False


def _ws_transport(url):
    return WebSocketTransport(url)


class LiveLocalTransport(LocalTransport):
    """Live of the single player (pow_server/live.py) inside the game, on the storage
    of the in-game multiplayer server: the same accounts, Warehouse and Safe."""
    _live = None

    @classmethod
    def shared_live(cls):
        if cls._live is None:
            import os

            from pow_server.live import LiveServer
            rng = None
            if os.environ.get("POW_SEED"):
                import random
                rng = random.Random(int(os.environ["POW_SEED"]))
            cls._live = LiveServer(LocalTransport.shared_server().storage, rng=rng)
        return cls._live

    def open(self):
        server = self.server or self.shared_live()
        self.inbox.clear()
        self.session = server.connect(self._deliver)
        self.connected, self.failed = True, False

    def poll(self):
        out = list(self.inbox)
        self.inbox.clear()
        return out


def make_live_transport(where):
    """config.LIVE_SERVER: "local" or ws(s)://host:port/live."""
    if not where or where == "local":
        return LiveLocalTransport()
    return _ws_transport(where)


def make_transport(where):
    if not where or where == "local":
        return LocalTransport()
    return _ws_transport(where)
