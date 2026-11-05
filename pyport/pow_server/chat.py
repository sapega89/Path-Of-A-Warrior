"""PORT-EXTRA (asked by Andrey): the chat of the online game.

Not in the original jar (its nearest thing is the 20-character quote of state 84). Three
channels:

    0 LOBBY    everyone online with the port's client
    1 ORDER    the members of my order (pow_server/orders.py)
    2 PRIVATE  two players; the other one may be offline and reads it later

A message is 1..MAX_TEXT printable ASCII characters (the client's bitmap font has no other
glyphs and no backslash). Rude words are starred (FILTER), and a player who writes too fast
gets ERR_TOO_FAST (RATE). Each conversation keeps its last HISTORY messages in the storage's
JSON documents (Storage.live_get / live_put):

    chat:lobby                     {"seq": N, "rows": [[uid, name, text], ...]}
    chat:order:<NAME>              the same, cleared when an order of that name is created
    chat:pm:<UID_A>:<UID_B>        the same, the two UserIDs sorted
    chat:me:<UID>                  {"order_seen": seq, "peers": [[uid, unread], ...]} newest first

The server pushes CHAT_PUSH to every online reader of the conversation (the writer too, so
the clients only ever append what the server sent), and CHAT_UNREAD after the login when
private or order messages wait. Pushes go only to the port's client (Session.port_client):
the original jar never asked for them.
"""
import re

LOBBY, ORDER, PRIVATE = 0, 1, 2
MAX_TEXT = 40
HISTORY = 30
MAX_PEERS = 20
RATE = ((1.5, 1), (20.0, 6))       # at most 1 message in 1.5 s and 6 in 20 s
TEXT_RE = re.compile(r"^[ -\[\]-~]+$")   # printable ASCII without the backslash
# starred whole or inside words, any case; Latin only, like the font
FILTER = re.compile(r"fuck|shit|bitch|cunt|dick|asshole|bastard|whore|slut|nigg|fagg|"
                    r"blya|blia|suka|pizd|khuy|xuy|huy|hui|ebat|yeba|mudak|pidor|pidar|gandon",
                    re.IGNORECASE)
# what the bots answer in private (a message to a bot gets one of these)
BOT_LINES = ("Ha! Fight me first.", "Not now, I am sharpening my sword.",
             "Challenge me and we will talk.", "Good luck out there!", "See you in the arena.",
             "Who sent you?", "I only speak with my blade.")


def clean(text):
    """The text as it will be shown, or None when it is not acceptable."""
    text = (text or "").strip()
    if not text or len(text) > MAX_TEXT or not TEXT_RE.match(text):
        return None
    return FILTER.sub(lambda m: "*" * len(m.group(0)), text)


def pm_key(a, b):
    x, y = sorted((a, b))
    return "chat:pm:%s:%s" % (x, y)


def order_key(name):
    return "chat:order:" + name


def history(storage, key):
    doc = storage.live_get(key)
    return doc or {"seq": 0, "rows": []}


def append(storage, key, uid, name, text):
    doc = history(storage, key)
    doc["seq"] += 1
    doc["rows"] = (doc["rows"] + [[uid, name, text]])[-HISTORY:]
    storage.live_put(key, doc)
    return doc


def clear(storage, key):
    storage.live_put(key, {"seq": 0, "rows": []})


def me_doc(storage, uid):
    doc = storage.live_get("chat:me:" + uid)
    return doc or {"order_seen": 0, "peers": []}


def put_me(storage, uid, doc):
    storage.live_put("chat:me:" + uid, doc)


def touch_peer(storage, uid, peer, unread):
    """Moves `peer` to the top of uid's conversations; unread: +1 (a new message) or 0 (read)."""
    doc = me_doc(storage, uid)
    old = next((p for p in doc["peers"] if p[0] == peer), None)
    count = 0 if not unread else (old[1] if old else 0) + 1
    doc["peers"] = ([[peer, min(count, 99)]] + [p for p in doc["peers"] if p[0] != peer])[:MAX_PEERS]
    put_me(storage, uid, doc)


def mark_peer_read(storage, uid, peer):
    doc = me_doc(storage, uid)
    for p in doc["peers"]:
        if p[0] == peer:
            p[1] = 0
    put_me(storage, uid, doc)


def unread(storage, uid, order_name):
    """(order, private) unread counts of a player."""
    doc = me_doc(storage, uid)
    order = 0
    if order_name:
        order = max(0, history(storage, order_key(order_name))["seq"] - doc["order_seen"])
    return min(order, 99), min(sum(p[1] for p in doc["peers"]), 99)


class RateLimit:
    """Timestamps of a session's last messages."""

    def __init__(self):
        self.times = []

    def allow(self, now):
        longest = max(w for w, _ in RATE)
        self.times = [t for t in self.times if now - t < longest]
        for window, most in RATE:
            if sum(1 for t in self.times if now - t < window) >= most:
                return False
        self.times.append(now)
        return True


def rows_out(rows):
    return [{"id": uid, "name": name, "text": text} for uid, name, text in rows]

