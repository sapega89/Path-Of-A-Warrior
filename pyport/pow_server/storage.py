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
"""


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("ascii", "replace"), salt, PBKDF2_ROUNDS)


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

    def _one(self, sql, *args):
        with self.lock:
            return self.db.execute(sql, args).fetchone()


class MemoryStorage:
    """The same interface without sqlite3; nothing is kept after the process ends."""

    def __init__(self, path=":memory:"):
        self.accounts = {}       # id -> [salt, hash, token]
        self.chars = {}          # id -> json dict

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


def open_storage(path=":memory:"):
    return Storage(path) if sqlite3 is not None else MemoryStorage(path)
