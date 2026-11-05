"""PORT-EXTRA (asked by Andrey): the single player's save kept on the server too.

The RecordStores stay where they were (files in config.SAVE_DIR / the browser's localStorage)
and the game reads and writes only them, as on the phone. This module sends every write of the
save stores (pow_server/cloud.py STORES: the hero and the Options) to the server path /save, and
takes the server's copy back when it is newer: start the game on another computer or browser,
and the hero is there.

The account is the Gamevil Live one: Game Menu > Gamevil Live > register (UserID + password,
kept in the store "gamevil_pow_regist", m.java:287-305). Without it nothing is sent. The server
is config.SAVE_SERVER ("auto" = the host of config.LIVE_SERVER when that is a ws(s):// server).

Which copy wins:
- game start (boot()): the newer one by the time of the save; the other one is kept in
  "<store>_backup" (a raw entry next to the stores);
- the first time this device logs in to an account (registration on a new device, or another
  UserID): the server's copy, if the server has one - that is what a player who registers on a
  second device wants. The hero loaded already is the old one, so the game restarts;
- while playing (another device saved meanwhile): this device's copy, the server's one is kept
  as the backup.

PORT-EXTRA (asked by Andrey) "server only" (config.SERVER_ONLY_SAVE, when there is a server):
the hero (SERVER_ONLY) is never kept on the device. It lives in memory (rms.memory_only), is
taken from the server before the game loads it and every save goes to the server. The game
starts only online: boot() waits for the server (main.py shows offline_screen.py meanwhile),
and the server's copy always wins at the start. A hero left on the device from before is moved
to the server (sent when the account has none there) and removed from the device once the
server has it.
"""
import asyncio
import base64
import hashlib
import json
import sys
import time
import urllib.parse

import config
from pow.midp import rms
from pow_server.cloud import STORES

META = "pow_cloud_meta"           # raw entry: {"user": UserID, "stores": {name: {rev, at, dirty}}}
REGIST = "gamevil_pow_regist"
SERVER_ONLY = ("gamevil_pow_data", "gamevil_pow_data_backup")   # kept only in memory + on the server
RETRY_MS = 10000                  # reconnect after a failed connection
STEP_SECONDS = 0.25
_TASKS = set()                    # running sync tasks (asyncio keeps only weak references)


def server_url():
    """config.SAVE_SERVER -> a ws(s):// URL, or None (server saves off)."""
    v = (config.SAVE_SERVER or "").strip()
    if v in ("", "off", "local"):
        return None
    if v == "auto":
        live = config.LIVE_SERVER or ""
        if not live.startswith(("ws://", "wss://")):
            return None
        u = urllib.parse.urlsplit(live)
        return urllib.parse.urlunsplit((u.scheme, u.netloc, "/save", "", ""))
    return v


def server_only():
    """The hero kept only on the server: config.SERVER_ONLY_SAVE and a server to keep it."""
    return bool(config.SERVER_ONLY_SAVE) and server_url() is not None


def use_memory_only():
    """rms keeps SERVER_ONLY in memory. The device's old copies are moved there (to be sent if
    the server has none); returns their names, to be removed from the device later."""
    found = []
    for name in SERVER_ONLY:
        text = rms.disk_load(name)
        if text is not None and name not in rms.memory:
            rms.memory[name] = text
            found.append(name)
    rms.memory_only.update(SERVER_ONLY)
    return found


def now_ms():
    return int(time.time() * 1000)


def read_login():
    """(UserID, password) of the Gamevil Live registration, or None."""
    raw = rms._load_raw(REGIST)
    if raw is None:
        return None
    try:
        recs = json.loads(raw)
        data = base64.b64decode(recs[0]) if recs else b""
    except (ValueError, IndexError):
        return None

    def text(b):
        return bytes(b).split(b"\0", 1)[0].decode("latin-1").strip()
    pwd, uid = text(data[0:12]), text(data[12:28])
    return (uid, pwd) if uid and pwd else None


def _digest(records):
    return hashlib.sha1(json.dumps(records).encode()).hexdigest()[:16]   # noqa: S324 (a change check, not security)


def _records(name):
    raw = rms._load_raw(name)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except ValueError:
        return None


class TextSocket:
    """A WebSocket of text messages with `websockets` on the desktop (like
    pow/midp/transport.py's WebSocketTransport, which is binary). The browser uses
    BrowserTextSocket."""

    def __init__(self, url):
        self.url = url
        self.connected = self.failed = False
        self.inbox = []
        self._ws = None
        self._out = None
        self._task = None

    def open(self):
        self._out = asyncio.Queue()
        self._task = asyncio.ensure_future(self._run())

    async def _run(self):
        try:
            from websockets.asyncio.client import connect
            async with connect(self.url, max_size=256 * 1024, open_timeout=10) as ws:
                self.connected = True

                async def sender():
                    while True:
                        await ws.send(await self._out.get())
                task = asyncio.ensure_future(sender())
                try:
                    async for data in ws:
                        if isinstance(data, str):
                            self.inbox.append(data)
                finally:
                    task.cancel()
        except asyncio.CancelledError:
            raise
        except Exception as ex:
            print("Server saves: connection failed:", repr(ex))
        self.connected, self.failed = False, True

    def send(self, text):
        if not self.connected:
            return
        self._out.put_nowait(text)

    def poll(self):
        out, self.inbox = self.inbox, []
        return out

    def close(self):
        if self._task is not None:
            self._task.cancel()
            self._task = None
        if self._ws is not None:
            try:
                self._ws.close()
            except Exception:
                pass
            self._ws = None
        self.connected = False


class BrowserTextSocket:
    """PORT-EXTRA: TextSocket of the browser build: the page's WebSocket (pow/midp/webws.py)."""

    def __init__(self, url):
        self.url = url
        self._ws = None

    @property
    def connected(self):
        return self._ws is not None and self._ws.connected

    @property
    def failed(self):
        return self._ws is not None and self._ws.failed

    def open(self):
        from pow.midp.webws import BrowserSocket
        self._ws = BrowserSocket(self.url, binary=False)

    def send(self, text):
        if self.connected:
            self._ws.send(str(text))

    def poll(self):
        if self._ws is None:
            return []
        return [m for m in self._ws.recv() if isinstance(m, str)]

    def close(self):
        if self._ws is not None:
            self._ws.close()
            self._ws = None


class CloudSync:
    """The client side; step() does one bit of work, run by run() / boot() on the game loop."""

    def __init__(self, url, make_socket=None, clock=now_ms, server_only=False):
        if make_socket is None:
            make_socket = BrowserTextSocket if sys.platform == "emscripten" else TextSocket
        self.url = url
        self.make_socket = make_socket
        self.clock = clock
        self.sock = None
        self.state = "idle"        # idle -> login -> get -> ready; "off" = wrong login, wait
        self.login = None          # (id, pwd) the connection logged in with
        self.retry_at = 0
        self.in_flight = {}        # store -> the "at" of the put sent
        self.applying = False      # writing the server's copy: not a change of this device
        self.started = False       # the game has loaded the hero (restart needed to change it)
        self.restart_requested = False
        self.server_only = server_only
        self.reachable = False     # server only, no account yet: the server answered
        self.purge = []            # server only: the device's old copies, removed once sent
        self.meta = self._load_meta()

    # --- local bookkeeping ---------------------------------------------------------
    @staticmethod
    def _load_meta():
        raw = rms._load_raw(META)
        try:
            m = json.loads(raw) if raw else {}
        except ValueError:
            m = {}
        m.setdefault("user", "")
        m.setdefault("stores", {})
        return m

    def _save_meta(self):
        rms._save_raw(META, json.dumps(self.meta))

    def _m(self, name):
        return self.meta["stores"].setdefault(name, {"rev": 0, "at": 0, "dirty": False})

    def on_write(self, name):
        """rms.on_write: a store was written on this device."""
        if self.applying:
            return
        if name in STORES:
            m = self._m(name)
            m["dirty"], m["at"] = True, max(self.clock(), m["at"] + 1)
            self._save_meta()
        elif name == REGIST and self.state == "off":
            self.state = "idle"            # a new registration: try that login

    # --- the connection ----------------------------------------------------------------
    def _drop(self, state="idle"):
        if self.sock is not None:
            self.sock.close()
        self.sock, self.state, self.in_flight = None, state, {}

    def step(self):
        login = read_login()
        if login is None:
            if self.sock is not None and self.login is not None:
                self._drop()               # the registration is gone
            if self.server_only and not self.reachable:
                self._probe()
            return
        if self.state == "off":
            if login == self.login:
                return
            self.state = "idle"
        if self.sock is not None and login != self.login:
            self._drop()                   # another account was registered on this device
        if self.sock is None:
            if self.clock() < self.retry_at:
                return
            self.login = login
            self.sock = self.make_socket(self.url)
            self.sock.open()
            self.state = "connecting"
        if self.sock.failed:
            self._drop()
            self.retry_at = self.clock() + RETRY_MS
            return
        if not self.sock.connected:
            return
        if self.state == "connecting":
            self.sock.send(json.dumps({"op": "login", "id": login[0], "pwd": login[1]}))
            self.state = "login"
        for text in self.sock.poll():
            try:
                self._answer(json.loads(text))
            except (ValueError, KeyError, TypeError) as ex:
                print(f"Server saves: bad answer {text[:80]!r} ({ex!r})")
            if self.sock is None:
                return
        if self.state == "ready":
            self._push()
            if self.purge and self.idle:
                for name in self.purge:    # the server has it now: off the device
                    rms.disk_delete(name)
                self.purge = []

    def _probe(self):
        """Server only, no account yet: is the server there? (The game starts only online.)"""
        if self.sock is None:
            if self.clock() < self.retry_at:
                return
            self.login = None
            self.sock = self.make_socket(self.url)
            self.sock.open()
            self.state = "probe"
        if self.sock.failed:
            self._drop()
            self.retry_at = self.clock() + RETRY_MS
        elif self.sock.connected:
            self.reachable = True
            self._drop()

    @property
    def online(self):
        """Server only: the game may start (the hero came from the server, or no account yet
        and the server is there)."""
        if read_login() is None:
            return self.reachable
        return self.state == "ready"

    def retry_now(self):
        """The player asked to try again (offline_screen.py)."""
        self.retry_at = 0
        if self.state == "off":
            self.state = "idle"
    def _answer(self, msg):
        op = msg.get("op")
        if op == "login":
            if not msg.get("ok"):
                print("Server saves: login refused ({})".format(msg.get("err")))
                return self._drop("off")
            self.sock.send(json.dumps({"op": "get"}))
            self.state = "get"
        elif op == "get" and msg.get("ok"):
            self._apply(msg["stores"], first=self.meta["user"] != self.login[0])
            self.state = "ready"
        elif op == "put":
            self._put_answer(msg)

    # --- taking the server's copy ----------------------------------------------------
    def _take(self, name, entry):
        """The server's copy replaces the local one (kept as <name>_backup). True when the
        records changed."""
        local = _records(name)
        changed = local != entry["records"]
        if changed:
            if local is not None:
                rms._save_raw(name + "_backup", json.dumps(local))
            self.applying = True
            try:
                rms._save_raw(name, json.dumps(entry["records"]))
            finally:
                self.applying = False
        self.meta["stores"][name] = {"rev": entry["rev"], "at": entry["at"], "dirty": False,
                                     "sum": _digest(entry["records"])}
        return changed

    def _apply(self, stores, first):
        changed = []
        if first:                          # a new account on this device: start from its revs
            self.meta["stores"] = {}
        for name in STORES:
            s, m = stores.get(name), self._m(name)
            local = _records(name)
            if local is not None and not m["dirty"] and m.get("sum") != _digest(local):
                # written while nothing watched it (server saves were off): a change of ours
                m["dirty"], m["at"] = True, max(self.clock(), m["at"] + 1)
            if s is None:                  # nothing on the server yet: send ours
                m["rev"], m["dirty"] = 0, local is not None
                continue
            if first or (self.server_only and name in SERVER_ONLY) or (
                    s["rev"] > m["rev"] and not (m["dirty"] and m["at"] > s["at"])):
                if self._take(name, s):
                    changed.append(name)
            elif s["rev"] > m["rev"]:      # ours is newer: keep it, overwrite the server's
                rms._save_raw(name + "_backup", json.dumps(s["records"]))
                m["rev"], m["dirty"] = s["rev"], True
            elif s["rev"] < m["rev"]:      # the server lost it (a new database): send ours again
                m["rev"], m["dirty"] = s["rev"], local is not None
        self.meta["user"] = self.login[0]
        self._save_meta()
        if changed:
            print("Server saves: took the server's copy of", ", ".join(changed))
        if "gamevil_pow_data" in changed and self.started:
            self.request_restart()

    def request_restart(self):
        """The hero in memory is the old one: start the game again (main.py restart())."""
        self.restart_requested = True
        from pow.game.game_canvas import GameCanvas
        GameCanvas.running = False

    # --- sending ours ------------------------------------------------------------------
    def _push(self):
        for name in STORES:
            m = self.meta["stores"].get(name)
            if not m or not m["dirty"] or name in self.in_flight:
                continue
            records = _records(name)
            if records is None:
                m["dirty"] = False
                continue
            self.in_flight[name] = (m["at"], _digest(records))
            self.sock.send(json.dumps({"op": "put", "store": name, "base": m["rev"],
                                       "at": m["at"], "records": records}))

    def _put_answer(self, msg):
        name = msg.get("store")
        sent = self.in_flight.pop(name, None)
        m = self.meta["stores"].get(name)
        if m is None or sent is None:
            return
        if msg.get("ok"):
            m["rev"], m["sum"] = msg["rev"], sent[1]
            if m["at"] == sent[0]:         # not written again meanwhile
                m["dirty"] = False
        elif msg.get("err") == "conflict":
            # another device saved while this one played: this one's copy wins
            cur = msg["current"]
            rms._save_raw(name + "_backup", json.dumps(cur["records"]))
            m["rev"] = cur["rev"]
        else:
            print("Server saves: {} not saved ({})".format(name, msg.get("err")))
            m["dirty"] = False
        self._save_meta()

    @property
    def idle(self):
        """Nothing left to send."""
        return not self.in_flight and not any(m["dirty"] for m in self.meta["stores"].values())


sync = None


async def boot(timeout=4.0, offline_screen=None):
    """main.py, before the game loads the hero: take a newer copy from the server, then keep
    sending the saves in the background. Never blocks longer than `timeout`; server only: waits
    until online, `offline_screen(sync)` (offline_screen.py) is shown while the server is not
    there and comes back when it is."""
    global sync
    url = server_url()
    if url is None:
        return None
    only = server_only()
    sync = CloudSync(url, server_only=only)
    if only:
        sync.purge = use_memory_only()
    rms.on_write.append(sync.on_write)
    if only:
        while not await connect(sync):
            if offline_screen is None:
                break
            await offline_screen(sync)
    else:
        end = time.monotonic() + timeout
        while time.monotonic() < end and read_login() is not None:
            sync.step()
            if sync.state in ("ready", "off") or sync.retry_at:
                break
            await asyncio.sleep(0.05)
    sync.started = True
    task = asyncio.ensure_future(run(sync))
    _TASKS.add(task)                     # asyncio keeps only a weak reference to a task
    task.add_done_callback(_TASKS.discard)
    return sync


async def connect(s, timeout=10.0):
    """Server only: one try to get online. True when the game may start."""
    end = time.monotonic() + timeout
    s.retry_now()
    while time.monotonic() < end:
        s.step()
        if s.online:
            return True
        if s.state == "off" or s.retry_at:
            return False
        await asyncio.sleep(0.05)
    s._drop()
    return False


async def flush(timeout=3.0):
    """Before the game ends: let the last save reach the server."""
    if sync is None:
        return
    end = time.monotonic() + timeout
    while time.monotonic() < end and sync.sock is not None and not sync.idle:
        sync.step()
        await asyncio.sleep(0.05)


async def run(s):
    while True:
        try:
            s.step()
        except Exception as ex:            # never let the saves stop the game
            print(f"Server saves: {ex!r}")
        await asyncio.sleep(STEP_SECONDS)
