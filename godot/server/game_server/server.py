"""One connection's session: it reads requests (protocol.py) and answers them."""
import json
import logging

from game_server import protocol
from game_server.protocol import ProtocolError

log = logging.getLogger("game_server")
NAME = "mercenarys-path"


class Session:
    def __init__(self, storage, guard, peer=None):
        self.storage = storage
        self.guard = guard
        self.peer = peer
        self.account = None
        self.rev = 0  # the hero's revision the game has

    def handle(self, text):
        """The answer (JSON text) to one request."""
        request_id = None
        try:
            msg = protocol.parse(text)
            request_id = msg["id"]
            handler = getattr(self, "on_" + msg["type"], None)
            if handler is None:
                raise ProtocolError("unknown")
            return handler(msg)
        except ProtocolError as ex:
            if request_id is None:
                request_id = _request_id(text)
            return protocol.error(request_id, ex.code)

    def on_hello(self, msg):
        return protocol.answer(msg, server=NAME, v=protocol.VERSION)

    def on_guest_login(self, msg):
        device = msg.get("device")
        if not isinstance(device, str) or not protocol.DEVICE_MIN <= len(device) <= protocol.DEVICE_MAX:
            raise ProtocolError("bad")
        if not self.storage.has_device(device) and not self.guard.may_create(self.peer):
            raise ProtocolError("limit")
        account, token, new = self.storage.guest(device)
        self.account = account
        log.info("guest %s%s", account, " (new)" if new else "")
        return protocol.answer(msg, account=account, token=token)

    def on_login(self, msg):
        if not self.storage.check_token(msg.get("account"), msg.get("token")):
            raise ProtocolError("login")
        self.account = msg["account"]
        return protocol.answer(msg, account=self.account)

    def _need_login(self):
        if self.account is None:
            raise ProtocolError("auth")

    def on_hero_get(self, msg):
        self._need_login()
        hero, rev = self.storage.hero(self.account)
        return protocol.answer(msg, hero=hero, rev=rev)

    def on_hero_put(self, msg):
        self._need_login()
        hero, rev = msg.get("hero"), msg.get("rev")
        if not isinstance(hero, dict) or type(rev) is not int:
            raise ProtocolError("bad")
        if len(json.dumps(hero)) > protocol.MAX_HERO:
            raise ProtocolError("too_big")
        new_rev = self.storage.put_hero(self.account, hero, rev)
        if new_rev is None:
            raise ProtocolError("stale")
        return protocol.answer(msg, rev=new_rev)


def _request_id(text):
    """The id of a request that could not be read, when it has one (for the error answer)."""
    try:
        raw = json.loads(text)
    except (ValueError, TypeError):
        return None
    return raw.get("id") if isinstance(raw, dict) and type(raw.get("id")) is int else None
