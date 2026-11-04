"""PORT-EXTRA: the chat of the online game (pow_server/chat.py): lobby, order, private."""
import random

import pytest

from pow_server import chat
from pow_server import messages as M
from pow_server.server import GameServer
from tests.test_mp_server import Clock, login


@pytest.fixture(params=["sqlite", "memory"])
def server(request):
    from pow_server.storage import MemoryStorage, Storage
    st = Storage() if request.param == "sqlite" else MemoryStorage()
    clock = Clock()
    srv = GameServer(st, rng=random.Random(7), match_wait=0, clock=clock)
    srv.test_clock = clock
    return srv


def _pushes(c):
    return [(m["channel"], m["peer"], m["id"], m["text"]) for m in c.got if m["op"] == M.CHAT_PUSH]


def _say(server, c, channel, text, peer=""):
    server.test_clock.t += 5                   # past the rate limit
    return _send(c, channel, text, peer)


def _send(c, channel, text, peer=""):
    """1811 (the pushes of 1812 follow it)."""
    c.ask(M.CHAT_SEND, channel=channel, peer=peer, text=text)
    return next(m for m in c.got if m["op"] == M.CHAT_SEND_ANS)


def test_lobby_reaches_everyone_online_and_keeps_history(server):
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    b.got.clear()
    ans = _say(server, a, chat.LOBBY, "Hello all")
    assert ans["op"] == M.CHAT_SEND_ANS and ans["st"] == 1
    assert _pushes(a) == [(0, "", "ANDREY", "Hello all")]          # the writer too
    assert _pushes(b) == [(0, "", "ANDREY", "Hello all")]
    c, _ = login(server, "CYRIL")
    hist = c.ask(M.CHAT_READ, channel=chat.LOBBY, peer="")
    assert hist["st"] == 1 and [(r["id"], r["name"], r["text"]) for r in hist["rows"]] == [
        ("ANDREY", "ANDREY", "Hello all")]


def test_history_keeps_the_last_messages(server):
    a, _ = login(server, "ANDREY")
    for i in range(chat.HISTORY + 5):
        _say(server, a, chat.LOBBY, "line %d" % i)
    rows = a.ask(M.CHAT_READ, channel=chat.LOBBY, peer="")["rows"]
    assert len(rows) == chat.HISTORY and rows[-1]["text"] == "line %d" % (chat.HISTORY + 4)


def test_bad_text_rude_words_and_rate_limit(server):
    a, _ = login(server, "ANDREY")
    assert _say(server, a, chat.LOBBY, "   ")["st"] == M.ERR_NOT_ACCEPTABLE
    assert _say(server, a, chat.LOBBY, "back\\slash")["st"] == M.ERR_NOT_ACCEPTABLE
    _send(a, chat.LOBBY, "Shit happens")
    assert _pushes(a)[-1][3] == "**** happens"
    assert _send(a, chat.LOBBY, "again")["st"] == M.ERR_TOO_FAST
    for _ in range(5):
        server.test_clock.t += 2
        assert _send(a, chat.LOBBY, "x")["st"] == 1
    server.test_clock.t += 2                  # 6 in 20 s already
    assert _send(a, chat.LOBBY, "x")["st"] == M.ERR_TOO_FAST


def test_order_chat_only_for_members_and_unread_after_login(server):
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    c, _ = login(server, "CYRIL")
    assert _say(server, a, chat.ORDER, "hi")["st"] == M.ERR_NO_ORDER
    assert a.ask(M.CHAT_READ, channel=chat.ORDER, peer="")["st"] == M.ERR_NO_ORDER
    a.ask(M.ORDER_CREATE, name="WOLVES")
    b.ask(M.ORDER_JOIN, name="WOLVES")
    b.session.close()
    c.got.clear()
    assert _say(server, a, chat.ORDER, "Mission at nine")["st"] == 1
    assert _say(server, a, chat.ORDER, "Bring potions")["st"] == 1
    assert _pushes(c) == []                                        # not a member
    b, _ = login(server, "BORYS")
    unread = [m for m in b.got if m["op"] == M.CHAT_UNREAD]
    assert unread and unread[0]["order"] == 2 and unread[0]["private"] == 0
    rows = b.ask(M.CHAT_READ, channel=chat.ORDER, peer="")["rows"]
    assert [r["text"] for r in rows] == ["Mission at nine", "Bring potions"]
    b.session.close()
    b, _ = login(server, "BORYS")
    assert not [m for m in b.got if m["op"] == M.CHAT_UNREAD]     # read now


def test_a_new_order_starts_a_new_chat(server):
    a, _ = login(server, "ANDREY")
    a.ask(M.ORDER_CREATE, name="WOLVES")
    _say(server, a, chat.ORDER, "old news")
    a.ask(M.ORDER_LEAVE)
    b, _ = login(server, "BORYS")
    b.ask(M.ORDER_CREATE, name="WOLVES")
    assert b.ask(M.CHAT_READ, channel=chat.ORDER, peer="")["rows"] == []


def test_private_messages_offline_unread_and_peers(server):
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    assert _say(server, a, chat.PRIVATE, "hi", peer="ANDREY")["st"] == M.ERR_SELF
    assert _say(server, a, chat.PRIVATE, "hi", peer="NOBODY")["st"] == M.ERR_NO_PLAYER
    b.got.clear()
    assert _say(server, a, chat.PRIVATE, "Duel?", peer="BORYS")["st"] == 1
    assert _pushes(a) == [(2, "BORYS", "ANDREY", "Duel?")]
    assert _pushes(b) == [(2, "ANDREY", "ANDREY", "Duel?")]
    b.session.close()
    _say(server, a, chat.PRIVATE, "Where are you?", peer="BORYS")
    b, _ = login(server, "BORYS")
    unread = next(m for m in b.got if m["op"] == M.CHAT_UNREAD)
    assert unread["private"] == 2 and unread["order"] == 0
    peers = b.ask(M.CHAT_PEERS)["rows"]
    assert [(p["id"], p["unread"], p["online"]) for p in peers] == [("ANDREY", 2, 1)]
    hist = b.ask(M.CHAT_READ, channel=chat.PRIVATE, peer="andrey")
    assert hist["peer"] == "ANDREY" and [r["text"] for r in hist["rows"]] == ["Duel?", "Where are you?"]
    assert b.ask(M.CHAT_PEERS)["rows"][0]["unread"] == 0
    assert a.ask(M.CHAT_PEERS)["rows"][0]["unread"] == 0          # my own messages are read


def test_server_bot_answers_in_private(server):
    server.add_bots()
    a, _ = login(server, "ANDREY")
    _say(server, a, chat.PRIVATE, "Hello", peer="BLADE")
    got = _pushes(a)
    assert got[0] == (2, "BLADE", "ANDREY", "Hello")
    assert got[1][:3] == (2, "BLADE", "BLADE") and got[1][3] in chat.BOT_LINES
    assert [(p["id"], p["online"]) for p in a.ask(M.CHAT_PEERS)["rows"]] == [("BLADE", 1)]


def test_scripted_bot_answers_in_private(server):
    from pow_server.bot import Bot
    bot = Bot(server, "RIVAL")
    a, _ = login(server, "ANDREY")
    _say(server, a, chat.PRIVATE, "Hello", peer="RIVAL")
    server.test_clock.t += 5
    a.got.clear()
    bot.pump()
    assert _pushes(a)[0][:3] == (2, "RIVAL", "RIVAL")


def test_the_original_client_gets_no_pushes(server):
    server.require_token = False
    from tests.test_mp_server import Client
    old = Client(server)
    old.ask(M.LOGIN_FIRST, id="OLDJAR", pwd="1234", ver=M.GAME_VER)
    old = Client(server)
    assert old.ask(M.LOGIN, id="OLDJAR", ver=M.GAME_VER)["st"] == 1
    a, _ = login(server, "ANDREY")
    old.got.clear()
    _say(server, a, chat.LOBBY, "hello")
    assert _pushes(old) == []


def test_clean():
    assert chat.clean("  ok  ") == "ok"
    assert chat.clean("x" * 41) is None
    assert chat.clean("Привіт") is None
    assert chat.clean("SUKA blyat") == "**** ****t"


def test_client_wraps_long_messages():
    from pow_mp.mp_canvas_chat import wrap

    class Font:
        @staticmethod
        def string_width(text):
            return 6 * len(text)

    lines = wrap(Font, "RIVAL", "Hi TEST, fancy a fight at the castle?", 120)
    texts = ["".join(t for t, _ in line) for line in lines]
    assert texts == ["RIVAL: Hi TEST,", "fancy a fight at the", "castle?"]
    assert all(len(t) * 6 <= 120 for t in texts)
    assert lines[0][0] == ("RIVAL:", None)
    assert ["".join(t for t, _ in ln) for ln in wrap(Font, "A", "x" * 30, 60)] == ["A:", "x" * 10, "x" * 10, "x" * 10]


def test_client_forgets_the_last_accounts_chat_on_login():
    import os
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    from pow_mp.mp_canvas import MpCanvas
    MpCanvas.chat_unread = [3, 2, 1]
    MpCanvas.chat_rows = {(0, ""): [("A", "A", "hi")]}
    MpCanvas.chat_loaded = {(0, "")}
    MpCanvas.chat_reset()
    assert MpCanvas.chat_unread == [0, 0, 0] and MpCanvas.chat_rows == {} and MpCanvas.chat_loaded == set()
