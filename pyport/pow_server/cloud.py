"""PORT-EXTRA (asked by Andrey): the single player's saves kept on the server.

The phone kept the game only in its RecordStores; the port keeps them in ~/.path_of_a_warrior
(desktop) or localStorage (browser), so a hero stayed on one computer / one browser. This
server keeps a copy of the save stores per account (the Gamevil Live / Multiplayer accounts:
UserID + password), and pow/game/cloud_save.py on the client sends every save here and takes
the newer copy back when the game starts on another device.

Path /save of the standalone server (ws://host:28200/save), one JSON text message each way:

    C->S {"op": "login", "id": "ANDREY", "pwd": "1234"}
    S->C {"op": "login", "ok": true}  /  {"op": "login", "ok": false, "err": "password"}
    C->S {"op": "get"}
    S->C {"op": "get", "ok": true, "stores": {name: {"rev": n, "at": ms, "records": [b64, ..]}}}
    C->S {"op": "put", "store": name, "base": n, "at": ms, "records": [b64, ..]}
    S->C {"op": "put", "ok": true, "store": name, "rev": n + 1}
         {"op": "put", "ok": false, "err": "conflict", "store": name, "current": {...}}

`base` is the revision the client last saw: a device that missed another device's save gets
"conflict" with the server's copy and decides (cloud_save.py). No anti-cheat (Andrey's
decision): the server keeps what the client sends.
"""
import base64
import binascii
import json
import re

STORES = ("gamevil_pow_data", "gamevil_pow_env")   # the hero and the Options
MAX_STORE = 64 * 1024        # bytes of all records of one store
MAX_RECORDS = 16
MAX_MESSAGE = 128 * 1024     # one text message (base64 + JSON)

_ID_RE = re.compile(r"^[A-Z]{4,12}$")
_PWD_RE = re.compile(r"^[0-9]{4,12}$")


class CloudServer:
    def __init__(self, storage):
        self.storage = storage

    def connect(self, send):
        """send(text) writes one message to the client."""
        return CloudSession(self, send)


class CloudSession:
    def __init__(self, server, send):
        self.server = server
        self._send = send
        self.user = None
        self.closed = False

    def send(self, **msg):
        if not self.closed:
            self._send(json.dumps(msg))

    def close(self):
        self.closed = True

    def receive(self, text):
        if self.closed:
            return None
        try:
            msg = json.loads(text)
        except (ValueError, TypeError):
            return self.send(op="?", ok=False, err="bad message")
        if not isinstance(msg, dict):
            return self.send(op="?", ok=False, err="bad message")
        op = msg.get("op")
        handler = {"login": self.on_login, "get": self.on_get, "put": self.on_put}.get(op)
        if handler is None:
            return self.send(op=str(op), ok=False, err="unknown op")
        if op != "login" and self.user is None:
            return self.send(op=op, ok=False, err="login first")
        handler(msg)

    def on_login(self, msg):
        uid, pwd = msg.get("id"), msg.get("pwd")
        st = self.server.storage
        if not (isinstance(uid, str) and isinstance(pwd, str)
                and _ID_RE.match(uid) and _PWD_RE.match(pwd)):
            return self.send(op="login", ok=False, err="bad id")
        if not st.has_account(uid):
            # accounts are made by the Gamevil Live registration (530) or the MP login (278)
            return self.send(op="login", ok=False, err="no account")
        if not st.check_password(uid, pwd):
            return self.send(op="login", ok=False, err="password")
        self.user = uid
        self.send(op="login", ok=True)

    def on_get(self, msg):
        stores = {k: v for k, v in self.server.storage.saves_get(self.user).items() if k in STORES}
        self.send(op="get", ok=True, stores=stores)

    def on_put(self, msg):
        store, base, at, records = msg.get("store"), msg.get("base"), msg.get("at"), msg.get("records")
        if store not in STORES:
            return self.send(op="put", ok=False, err="bad store", store=str(store))
        if not (isinstance(base, int) and isinstance(at, int) and isinstance(records, list)
                and len(records) <= MAX_RECORDS and all(isinstance(r, str) for r in records)):
            return self.send(op="put", ok=False, err="bad message", store=store)
        try:
            size = sum(len(base64.b64decode(r, validate=True)) for r in records)
        except (binascii.Error, ValueError):
            return self.send(op="put", ok=False, err="bad message", store=store)
        if size > MAX_STORE:
            return self.send(op="put", ok=False, err="too big", store=store)
        ok, entry = self.server.storage.save_put(self.user, store, base, at, records)
        if ok:
            return self.send(op="put", ok=True, store=store, rev=entry["rev"])
        self.send(op="put", ok=False, err="conflict", store=store, current=entry)
