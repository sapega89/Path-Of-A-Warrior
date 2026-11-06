"""Accounts and heroes in SQLite (":memory:" for the tests, a file on the server).

A guest account belongs to a device: the game makes a random device key once and logs in with
it; the server gives back the account and a token for later logins. Only hashes of the device
key and of the token are kept."""
import hashlib
import hmac
import json
import secrets
import sqlite3
import threading
import time

_SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY, device_hash TEXT UNIQUE, token_hash TEXT NOT NULL, created INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS heroes (
    account TEXT PRIMARY KEY REFERENCES accounts(id), rev INTEGER NOT NULL,
    saved INTEGER NOT NULL, data TEXT NOT NULL
);
"""


def _hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Storage:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self.lock = threading.Lock()
        self.db.executescript(_SCHEMA)

    def has_device(self, device):
        return self.db.execute("SELECT 1 FROM accounts WHERE device_hash=?", (_hash(device),)).fetchone() is not None

    def guest(self, device):
        """The account of a device (a new one the first time) and a fresh token: (account, token, new)."""
        token = secrets.token_hex(16)
        with self.lock:
            row = self.db.execute("SELECT id FROM accounts WHERE device_hash=?", (_hash(device),)).fetchone()
            if row is not None:
                self.db.execute("UPDATE accounts SET token_hash=? WHERE id=?", (_hash(token), row[0]))
                return row[0], token, False
            account = "g" + secrets.token_hex(8)
            self.db.execute("INSERT INTO accounts VALUES (?,?,?,?)",
                            (account, _hash(device), _hash(token), int(time.time())))
            return account, token, True

    def check_token(self, account, token):
        row = self.db.execute("SELECT token_hash FROM accounts WHERE id=?", (account,)).fetchone()
        return row is not None and isinstance(token, str) and hmac.compare_digest(row[0], _hash(token))

    def hero(self, account):
        """(hero, rev): the saved hero (None when none) and its revision (0 when none)."""
        row = self.db.execute("SELECT data, rev FROM heroes WHERE account=?", (account,)).fetchone()
        return (json.loads(row[0]), row[1]) if row else (None, 0)

    def put_hero(self, account, hero, rev):
        """Saves over revision `rev` (what the game last loaded or saved). Returns the new
        revision, or None when the hero was saved from somewhere else since."""
        data = json.dumps(hero, separators=(",", ":"))
        with self.lock:
            row = self.db.execute("SELECT rev FROM heroes WHERE account=?", (account,)).fetchone()
            now = row[0] if row else 0
            if rev != now:
                return None
            self.db.execute("INSERT OR REPLACE INTO heroes VALUES (?,?,?,?)",
                            (account, now + 1, int(time.time()), data))
            return now + 1
