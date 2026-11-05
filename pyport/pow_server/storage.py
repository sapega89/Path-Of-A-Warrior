"""Accounts and characters in SQLite (PHASE_9 task 9.14). ":memory:" for the in-game server
and the tests, a file for the standalone server; the data then survives a restart."""
import hashlib
import hmac
import json
import os
import secrets
import threading

try:
    import sqlite3
except ImportError:          # a Python build without sqlite3 (maybe the browser): MemoryStorage
    sqlite3 = None

from pow_server.model import Character

PBKDF2_ROUNDS = 60000

_SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY, salt BLOB NOT NULL, pw_hash BLOB NOT NULL, token TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS characters (
    id TEXT PRIMARY KEY REFERENCES accounts(id), display_name TEXT UNIQUE, data TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS live (
    key TEXT PRIMARY KEY, data TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS saves (
    id TEXT NOT NULL REFERENCES accounts(id), store TEXT NOT NULL, rev INTEGER NOT NULL,
    at INTEGER NOT NULL, data TEXT NOT NULL, PRIMARY KEY (id, store)
);
"""


def _pbkdf2_sha256(password, salt, rounds):
    """PBKDF2-HMAC-SHA256 with a 32-byte key, the same bytes as hashlib.pbkdf2_hmac. 
    the Python of the browser build (pygbag) has no hashlib.pbkdf2_hmac (no OpenSSL), and the
    server inside the page logs players in with it."""
    inner, outer = hashlib.sha256(), hashlib.sha256()
    if len(password) > inner.block_size:
        password = hashlib.sha256(password).digest()
    password = password.ljust(inner.block_size, b"\0")
    inner.update(bytes(b ^ 0x36 for b in password))
    outer.update(bytes(b ^ 0x5C for b in password))

    def prf(msg):
        i, o = inner.copy(), outer.copy()
        i.update(msg)
        o.update(i.digest())
        return o.digest()
    u = prf(salt + b"\0\0\0\1")
    acc = int.from_bytes(u, "big")
    for _ in range(rounds - 1):
        u = prf(u)
        acc ^= int.from_bytes(u, "big")
    return acc.to_bytes(len(u), "big")


def hash_password(password, salt):
    pw = password.encode("ascii", "replace")
    if hasattr(hashlib, "pbkdf2_hmac"):
        return hashlib.pbkdf2_hmac("sha256", pw, salt, PBKDF2_ROUNDS)
    return _pbkdf2_sha256(pw, salt, PBKDF2_ROUNDS)


class Storage:
    def __init__(self, path=":memory:"):
        self.path = path
        self.db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self.lock = threading.Lock()
        self.db.executescript(_SCHEMA)

    # --- accounts ------------------------------------------------------------
    def has_account(self, user_id):
        return self._one("SELECT 1 FROM accounts WHERE id=?", user_id) is not None

    def create_account(self, user_id, password):
        salt = os.urandom(16)
        token = secrets.token_hex(8)
        with self.lock:
            self.db.execute("INSERT INTO accounts VALUES (?,?,?,?)",
                            (user_id, salt, hash_password(password, salt), token))
        return token

    def check_password(self, user_id, password):
        row = self._one("SELECT salt, pw_hash FROM accounts WHERE id=?", user_id)
        return row is not None and hmac.compare_digest(hash_password(password, row[0]), row[1])

    def new_token(self, user_id):
        """A fresh session token after every 278 (the older one stops working)."""
        token = secrets.token_hex(8)
        with self.lock:
            self.db.execute("UPDATE accounts SET token=? WHERE id=?", (token, user_id))
        return token

    def check_token(self, user_id, token):
        row = self._one("SELECT token FROM accounts WHERE id=?", user_id)
        return row is not None and bool(token) and hmac.compare_digest(row[0], token)

    # --- characters ----------------------------------------------------------
    def load(self, user_id):
        row = self._one("SELECT data FROM characters WHERE id=?", user_id)
        return None if row is None else Character.from_json(json.loads(row[0]))

    def save(self, ch):
        with self.lock:
            self.db.execute(
                "INSERT INTO characters VALUES (?,?,?) ON CONFLICT(id) DO UPDATE SET "
                "display_name=excluded.display_name, data=excluded.data",
                (ch.user_id, ch.name.upper() or None, json.dumps(ch.to_json())))

    def name_taken(self, name, user_id):
        row = self._one("SELECT id FROM characters WHERE display_name=?", name.upper())
        return row is not None and row[0] != user_id

    def all_characters(self):
        with self.lock:
            rows = self.db.execute("SELECT data FROM characters").fetchall()
        return [Character.from_json(json.loads(r[0])) for r in rows]

    # --- Gamevil Live (pow_server/live.py): JSON documents by key ---------------
    def live_get(self, key):
        row = self._one("SELECT data FROM live WHERE key=?", key)
        return None if row is None else json.loads(row[0])

    def live_put(self, key, value):
        with self.lock:
            self.db.execute("INSERT INTO live VALUES (?,?) ON CONFLICT(key) DO UPDATE SET "
                            "data=excluded.data", (key, json.dumps(value)))

    # --- single-player saves kept on the server (pow_server/cloud.py) -------
    def saves_get(self, user_id):
        """{store: {"rev", "at", "records"}} of one account."""
        with self.lock:
            rows = self.db.execute("SELECT store, rev, at, data FROM saves WHERE id=?",
                                   (user_id,)).fetchall()
        return {r[0]: {"rev": r[1], "at": r[2], "records": json.loads(r[3])} for r in rows}

    def save_put(self, user_id, store, base, at, records):
        """Writes the store when `base` is its current revision (0 = none yet). Returns
        (True, new entry) or (False, the current entry) when another device wrote it first."""
        with self.lock:
            row = self.db.execute("SELECT rev, at, data FROM saves WHERE id=? AND store=?",
                                  (user_id, store)).fetchone()
            rev = row[0] if row else 0
            if base != rev:
                return False, {"rev": rev, "at": row[1], "records": json.loads(row[2])}
            entry = {"rev": rev + 1, "at": at, "records": records}
            self.db.execute("INSERT INTO saves VALUES (?,?,?,?,?) ON CONFLICT(id, store) DO UPDATE "
                            "SET rev=excluded.rev, at=excluded.at, data=excluded.data",
                            (user_id, store, rev + 1, at, json.dumps(records)))
        return True, entry

    def _one(self, sql, *args):
        with self.lock:
            return self.db.execute(sql, args).fetchone()


class MemoryStorage:
    """The same interface without sqlite3; nothing is kept after the process ends."""

    def __init__(self, path=":memory:"):
        self.accounts = {}       # id -> [salt, hash, token]
        self.chars = {}          # id -> json dict
        self.live = {}           # key -> json text (Gamevil Live)
        self.saves = {}          # (id, store) -> {"rev", "at", "records"}

    def has_account(self, user_id):
        return user_id in self.accounts

    def create_account(self, user_id, password):
        salt = os.urandom(16)
        self.accounts[user_id] = [salt, hash_password(password, salt), secrets.token_hex(8)]
        return self.accounts[user_id][2]

    def check_password(self, user_id, password):
        a = self.accounts.get(user_id)
        return a is not None and hmac.compare_digest(hash_password(password, a[0]), a[1])

    def new_token(self, user_id):
        self.accounts[user_id][2] = secrets.token_hex(8)
        return self.accounts[user_id][2]

    def check_token(self, user_id, token):
        a = self.accounts.get(user_id)
        return a is not None and bool(token) and hmac.compare_digest(a[2], token)

    def load(self, user_id):
        d = self.chars.get(user_id)
        return None if d is None else Character.from_json(json.loads(d))

    def save(self, ch):
        self.chars[ch.user_id] = json.dumps(ch.to_json())

    def name_taken(self, name, user_id):
        return any(Character.from_json(json.loads(d)).name.upper() == name.upper() and uid != user_id
                   for uid, d in self.chars.items())

    def all_characters(self):
        return [Character.from_json(json.loads(d)) for d in self.chars.values()]

    def live_get(self, key):
        d = self.live.get(key)
        return None if d is None else json.loads(d)

    def live_put(self, key, value):
        self.live[key] = json.dumps(value)

    def saves_get(self, user_id):
        return {st: dict(e) for (uid, st), e in self.saves.items() if uid == user_id}

    def save_put(self, user_id, store, base, at, records):
        cur = self.saves.get((user_id, store))
        rev = cur["rev"] if cur else 0
        if base != rev:
            return False, dict(cur)
        self.saves[(user_id, store)] = entry = {"rev": rev + 1, "at": at, "records": list(records)}
        return True, dict(entry)


def open_storage(path=":memory:"):
    return Storage(path) if sqlite3 is not None else MemoryStorage(path)
