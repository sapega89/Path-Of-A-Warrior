"""Where the MP client's frames go (PHASE_9 §3): the replacement of h.java's socket.

h.java opened socket://GAMEVIL_SERVER:GAMEVIL_PORT in its own thread and called g.a(k) for
every frame. Here the game loop calls poll() once per tick and gets the payloads received
since the last call (frame length removed, opcode first), and send() takes a whole frame
(what e.b() wrote). Two implementations with the same interface:

- LocalTransport: the server runs inside the game (9a: bots, no network).
- WebSocketTransport: ws:// or wss:// to `python -m pow_server` (9b). Desktop: the
  `websockets` package on the game's asyncio loop. Browser (pygbag): the page's JS WebSocket.
  The browser path is NOT tested yet (PHASE_9 risk "WebSocket in pygbag": spike in the next PR).

make_transport(config.MP_SERVER) picks one: "local" or a ws(s):// URL.
"""
import asyncio
import collections
import sys

from pow_server import codec_bin


class Transport:
    connected = False   # h.j
    failed = False      # connect failed or the connection dropped (-> g.g(n) in the client)

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
            if sys.platform != "emscripten":
                os.makedirs(config.SAVE_DIR, exist_ok=True)
                path = os.path.join(config.SAVE_DIR, "mp_local.sqlite")
            rng = None
            if os.environ.get("POW_SEED"):        # headless runs (tools/mp_shot.py) repeat exactly
                import random
                rng = random.Random(int(os.environ["POW_SEED"]))
            cls._server = GameServer(open_storage(path), rng=rng)
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
        if sys.platform == "emscripten":
            self._open_browser()
        else:
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

    # --- browser: the page's WebSocket through pygbag's `platform.window` -------
    def _open_browser(self):
        import platform as pf    # pygbag replaces the stdlib module with the JS bridge
        ws = pf.window.WebSocket.new(self.url)
        ws.binaryType = "arraybuffer"

        def on_open(ev):
            self.connected = True

        def on_message(ev):
            arr = pf.window.Uint8Array.new(ev.data)
            self.inbox.extend(codec_bin.unframe(bytes(arr.to_py() if hasattr(arr, "to_py") else arr))[0])

        def on_close(ev):
            self.connected = False
            self.failed = True

        ws.onopen, ws.onmessage, ws.onclose, ws.onerror = on_open, on_message, on_close, on_close
        self._ws = ws

    def send(self, frame):
        if not self.connected:
            return
        if sys.platform == "emscripten":
            import platform as pf
            self._ws.send(pf.window.Uint8Array.new(list(frame)))
        else:
            self._out.put_nowait(frame)

    def poll(self):
        out = list(self.inbox)
        self.inbox.clear()
        return out

    def close(self):
        if self._task is not None:
            self._task.cancel()
            self._task = None
        if self._ws is not None and sys.platform == "emscripten":
            try:
                self._ws.close()
            except Exception:
                pass
        self._ws = None
        self.connected = False


def make_transport(where):
    if not where or where == "local":
        return LocalTransport()
    return WebSocketTransport(where)
