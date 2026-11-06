"""Limits per address: open connections, new guest accounts, messages per second on a
connection. The address is the socket's, or behind a TLS proxy the last X-Forwarded-For entry."""
import time
from collections import defaultdict, deque

MAX_CONNECTIONS = 10
NEW_ACCOUNTS = 5
NEW_ACCOUNTS_WINDOW = 3600.0
MAX_MESSAGES = 20  # per second


class Guard:
    def __init__(self, clock=time.monotonic, max_connections=MAX_CONNECTIONS,
                 new_accounts=NEW_ACCOUNTS, max_messages=MAX_MESSAGES):
        self.clock = clock
        self.max_connections = max_connections
        self.new_accounts = new_accounts
        self.max_messages = max_messages
        self.open = defaultdict(int)
        self.created = defaultdict(deque)

    def open_connection(self, peer):
        if peer is not None and self.open[peer] >= self.max_connections:
            return False
        self.open[peer] += 1
        return True

    def close_connection(self, peer):
        self.open[peer] -= 1
        if self.open[peer] <= 0:
            del self.open[peer]

    def may_create(self, peer):
        """One more new account from this address (counted when allowed)."""
        if peer is None:
            return True
        q = self.created[peer]
        now = self.clock()
        while q and now - q[0] > NEW_ACCOUNTS_WINDOW:
            q.popleft()
        if len(q) >= self.new_accounts:
            return False
        q.append(now)
        return True

    def meter(self):
        return Meter(self.max_messages, self.clock)


class Meter:
    """At most `per_second` messages in any second."""

    def __init__(self, per_second, clock):
        self.per_second = per_second
        self.clock = clock
        self.times = deque()

    def allow(self):
        now = self.clock()
        while self.times and now - self.times[0] >= 1.0:
            self.times.popleft()
        if len(self.times) >= self.per_second:
            return False
        self.times.append(now)
        return True


def peer_address(ws, behind_proxy=False):
    if behind_proxy:
        headers = getattr(getattr(ws, "request", None), "headers", None)
        fwd = headers.get("X-Forwarded-For") if headers is not None else None
        if fwd:
            return fwd.split(",")[-1].strip()
    addr = getattr(ws, "remote_address", None)
    return addr[0] if isinstance(addr, (tuple, list)) and addr else None
