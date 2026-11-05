"""(asked by Andrey): the server's security settings (python -m pow_server --help).

The original server is lost; these limits are the port's own. One Guard is shared by
the three servers of serve() (multiplayer /, Live /live, saves /save), so a guessing
player cannot move to another path.

- Logins: LOGIN_FAILS wrong passwords for one UserID, or from one address, within LOGIN_WINDOW
  seconds block that UserID / address for LOGIN_BLOCK seconds. A blocked login is answered as a
  wrong password (no hint that the guess was right).
- New accounts: at most NEW_ACCOUNTS per address in NEW_ACCOUNTS_WINDOW seconds.
- Connections: at most MAX_CONNECTIONS open at once from one address (ws_server.py).
- Messages: at most MAX_MESSAGES per second on one connection, then it is closed (ws_server.py).

The address is the connection's own, or the last X-Forwarded-For entry (the proxy's) when the server runs
behind a TLS proxy (--behind-proxy). Without an address (tests, bots) only the per-UserID
limit counts.
"""
import time
from collections import defaultdict, deque

LOGIN_FAILS = 5
LOGIN_WINDOW = 600.0
LOGIN_BLOCK = 300.0
NEW_ACCOUNTS = 5
NEW_ACCOUNTS_WINDOW = 3600.0
MAX_CONNECTIONS = 10
MAX_MESSAGES = 30


class Guard:
    def __init__(self, *, login_fails=LOGIN_FAILS, login_window=LOGIN_WINDOW, login_block=LOGIN_BLOCK,
                 new_accounts=NEW_ACCOUNTS, new_accounts_window=NEW_ACCOUNTS_WINDOW,
                 max_connections=MAX_CONNECTIONS, max_messages=MAX_MESSAGES, clock=time.monotonic):
        self.login_fails = login_fails
        self.login_window = login_window
        self.login_block = login_block
        self.new_accounts = new_accounts
        self.new_accounts_window = new_accounts_window
        self.max_connections = max_connections
        self.max_messages = max_messages
        self.clock = clock
        self._fails = defaultdict(deque)      # ("id", uid) / ("ip", addr) -> times of wrong passwords
        self._blocked = {}                    # same keys -> blocked until
        self._created = defaultdict(deque)    # addr -> times of new accounts
        self.connections = defaultdict(int)   # addr -> open connections

    @staticmethod
    def _keys(uid, peer):
        keys = [("id", uid)]
        if peer:
            keys.append(("ip", peer))
        return keys

    def _trim(self, q, window):
        now = self.clock()
        while q and now - q[0] > window:
            q.popleft()

    # --- logins ----------------------------------------------------------------------
    def login_blocked(self, uid, peer=None):
        now = self.clock()
        for k in self._keys(uid, peer):
            until = self._blocked.get(k)
            if until is not None:
                if now < until:
                    return True
                del self._blocked[k]
        return False

    def login_result(self, uid, peer, ok):
        """After a password check: a right one clears the UserID's count."""
        if ok:
            self._fails.pop(("id", uid), None)
            return
        now = self.clock()
        for k in self._keys(uid, peer):
            q = self._fails[k]
            q.append(now)
            self._trim(q, self.login_window)
            if len(q) >= self.login_fails:
                self._blocked[k] = now + self.login_block
                q.clear()

    def check_password(self, storage, uid, pwd, peer=None):
        """storage.check_password behind the limits."""
        if self.login_blocked(uid, peer):
            return False
        ok = storage.check_password(uid, pwd)
        self.login_result(uid, peer, ok)
        return ok

    # --- new accounts ---------------------------------------------------------------------
    def may_create(self, peer):
        if not peer:
            return True
        q = self._created[peer]
        self._trim(q, self.new_accounts_window)
        if len(q) >= self.new_accounts:
            return False
        q.append(self.clock())
        return True

    # --- connections ----------------------------------------------------------------------
    def open_connection(self, peer):
        """False: too many connections from this address already."""
        if not peer:
            return True
        if self.connections[peer] >= self.max_connections:
            return False
        self.connections[peer] += 1
        return True

    def close_connection(self, peer):
        if peer and self.connections.get(peer, 0) > 0:
            self.connections[peer] -= 1
            if not self.connections[peer]:
                del self.connections[peer]

    def message_meter(self):
        return MessageMeter(self.max_messages, self.clock)


class MessageMeter:
    """Messages of one connection: allow() is False once more than `per_second` came in the
    last second."""

    def __init__(self, per_second, clock):
        self.per_second = per_second
        self.clock = clock
        self.times = deque()

    def allow(self):
        now = self.clock()
        self.times.append(now)
        while self.times and now - self.times[0] > 1.0:
            self.times.popleft()
        return len(self.times) <= self.per_second


def check_password(server, session, uid, pwd):
    """The password check of a session: through server.guard when the server has one."""
    guard = getattr(server, "guard", None)
    if guard is None:
        return server.storage.check_password(uid, pwd)
    return guard.check_password(server.storage, uid, pwd, getattr(session, "peer", None))


def may_create(server, session):
    guard = getattr(server, "guard", None)
    return guard is None or guard.may_create(getattr(session, "peer", None))
