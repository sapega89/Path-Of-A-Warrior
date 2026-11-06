"""The messages between the game and the server: one JSON object per WebSocket text message.

Every request has "type", "id" (the client's number, given back in the answer) and "v" (the
protocol version). The answer has the same "id", "type" + "_ok", or "type": "error" with a
"code". A client of another version gets "error" "update" (the game says: update the game).

    hello       {}                          -> hello_ok {server, v}
    guest_login {device}                    -> guest_login_ok {account, token}
    login       {account, token}            -> login_ok {account}
    hero_get    {}                          -> hero_get_ok {hero, rev}   (hero null when none)
    hero_put    {hero, rev}                 -> hero_put_ok {rev}        error "stale" when rev is old
"""
import json

VERSION = 1
MAX_MESSAGE = 64 * 1024
MAX_HERO = 48 * 1024
DEVICE_MIN, DEVICE_MAX = 16, 64

ERRORS = ("bad", "update", "unknown", "login", "auth", "stale", "too_big", "limit")


class ProtocolError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def parse(text):
    """A request: a JSON object with a text "type", an int "id" and the right "v"."""
    if not isinstance(text, str) or len(text) > MAX_MESSAGE:
        raise ProtocolError("too_big")
    try:
        msg = json.loads(text)
    except ValueError:
        raise ProtocolError("bad") from None
    if not isinstance(msg, dict) or not isinstance(msg.get("type"), str) or type(msg.get("id")) is not int:
        raise ProtocolError("bad")
    if msg.get("v") != VERSION:
        raise ProtocolError("update")
    return msg


def answer(request, **fields):
    out = {"type": request["type"] + "_ok", "id": request["id"]}
    out.update(fields)
    return json.dumps(out, separators=(",", ":"))


def error(request_id, code):
    return json.dumps({"type": "error", "id": request_id, "code": code}, separators=(",", ":"))
