"""The POW Multiplayer server: sessions and the menu-side messages (PHASE_9 tasks 9.13, 9.14, 9.18).

Pure Python, no pygame and no I/O: a transport (pow_server/ws_server.py, or the in-game
LocalTransport of pow_mp/net/transport.py) hands every received frame payload to
Session.receive() and writes the frames the session passes to its `send` callback.

Done here: login 278/262 (+ PORT-EXTRA session token), duplicate login (280), notices
258/259, Options 288-291, Character 1280-1299, Ranking 1293/1300, keepalive.
Battles: 1-on-1 Duel against a CPU fighter (512 mode 0 -> 513, 514, 1024; 1025/1026,
1027/1028 per round; 1025 after the end -> 1032), resolved in pow_server/battle.py.
Not yet: 2v2, missions and Challenge - 512 mode 1/2 and 768 answer "too many users" (-11).
"""
import random
import re
import time

from pow_server import battle as B, codec_bin, messages as M
from pow_server.model import apply_sp_hero, default_character, valid_slots
from pow_server.storage import open_storage

_ID_RE = re.compile(r"^[A-Z]{4,12}$")          # Login screen: A-Z, 4..12 (g:4888-4926)
_PWD_RE = re.compile(r"^[0-9]{4,12}$")         # password: digits, 4..12 (g:4930-4990)
_NAME_RE = re.compile(r"^[A-Za-z0-9]{1,8}$")   # Display Name: A-Z / a-z keyboard (g:2820-2866)
_QUOTE_RE = re.compile(r"^[ -~]{1,20}$")       # quotes: 1..20 printable characters


class GameServer:
    def __init__(self, storage=None, *, require_token=True, auto_register=True,
                 notices=(), notices_version=1, clock=time.monotonic, rng=None):
        """require_token: 262 must carry the token of the last 278 (PORT-EXTRA). False lets the
        original jar in, which logs in again with 262 and its UserID only (06 §2.3).
        auto_register: a 278 with an unknown UserID creates the account. The original only let
        in IDs registered in POW single ("Save User Data"); that bridge is task 9.10.
        notices: pages of 4 lines (16 characters each) shown once after login (258/259)."""
        self.storage = storage or open_storage()
        self.require_token = require_token
        self.auto_register = auto_register
        self.notices = [list(p)[:4] for p in notices]
        self.notices_version = notices_version
        self.clock = clock
        self.rng = rng or random.Random()
        self.online = {}               # user id -> Session

    def connect(self, send):
        """A new connection. send(frame_bytes) writes to the client; returns the Session."""
        return Session(self, send)


class Session:
    def __init__(self, server, send):
        self.server = server
        self._send = send
        self.user = None               # user id after a good 262
        self.char = None
        self.closed = False
        self.last_seen = server.clock()
        self.close_after_send = False  # 279 OK: the client hangs up itself and comes back with 262
        self.battle = None             # pow_server.battle.Battle while in a room
        self.slot = 0                  # my slot in it

    # --- I/O -----------------------------------------------------------------
    def send(self, op, **fields):
        if not self.closed:
            self._send(codec_bin.encode(op, fields, to_client=True))

    def receive(self, payload):
        """One frame payload from the client (the length prefix already removed)."""
        if self.closed:
            return
        self.last_seen = self.server.clock()
        try:
            msg = codec_bin.decode(payload, from_client=True)
        except codec_bin.CodecError:
            return
        handler = _HANDLERS.get(msg["op"])
        if handler is None:
            return                     # unknown opcodes are ignored, like the client does
        if self.user is None and msg["op"] not in (M.LOGIN, M.LOGIN_FIRST, M.KEEPALIVE):
            return                     # not logged in
        handler(self, msg)

    def close(self):
        if self.closed:
            return
        self.closed = True
        if self.battle is not None and not self.battle.over:
            # "Exit Battle" (RSK -> Yes) hangs up and logs in again (g:2990-2997): a loss
            self.battle.fighters[self.slot].hp = 0
            B.duel_rewards(self.char, self.battle, self.slot, self.server.rng)
            self.save()
        self.battle = None
        if self.user and self.server.online.get(self.user) is self:
            del self.server.online[self.user]

    def idle_seconds(self):
        return self.server.clock() - self.last_seen

    def save(self):
        self.server.storage.save(self.char)

    # --- login ---------------------------------------------------------------
    def on_login_first(self, msg):     # 278 -> 279
        uid, pwd, st = msg.get("id", ""), msg.get("pwd", ""), self.server.storage
        if msg.get("_short") or not _ID_RE.match(uid) or not _PWD_RE.match(pwd):
            return self.send(M.LOGIN_FIRST_ANS, st=-1, reason=M.REASON_OTHER)
        if not st.has_account(uid):
            if not self.server.auto_register:
                return self.send(M.LOGIN_FIRST_ANS, st=-1, reason=M.REASON_NO_ID)
            st.create_account(uid, pwd)
            st.save(default_character(uid))
        elif not st.check_password(uid, pwd):
            return self.send(M.LOGIN_FIRST_ANS, st=-1, reason=M.REASON_BAD_PASSWORD)
        self.send(M.LOGIN_FIRST_ANS, st=1, token=st.new_token(uid))

    def on_login(self, msg):           # 262 -> 263
        uid, st = msg.get("id", ""), self.server.storage
        if not _ID_RE.match(uid) or not st.has_account(uid):
            return self.send(M.LOGIN_ANS, st=M.LOGIN_NOT_REGISTERED)
        if self.server.require_token and not st.check_token(uid, msg.get("token", "")):
            return self.send(M.LOGIN_ANS, st=M.LOGIN_BAD_TOKEN)
        old = self.server.online.get(uid)
        if old is not None and old is not self:
            old.send(M.KICKED)         # "Another player has connected using your UserID"
            old.close()
        self.user = uid
        self.char = st.load(uid) or default_character(uid)
        if apply_sp_hero(self.char, msg):        # PORT-EXTRA: the single-player hero (9.10)
            self.save()
        self.server.online[uid] = self
        pages = 0
        if self.server.notices and self.char.notices_seen < self.server.notices_version:
            pages = len(self.server.notices)   # marked seen when the last page is delivered
        self.send(M.LOGIN_ANS, st=1, **self.char.profile(notices=pages))

    def on_notice(self, msg):          # 258 -> 259 (page 1, 2, ...)
        page = msg.get("page", 0)
        pages = self.server.notices
        if not 1 <= page <= len(pages):
            return self.send(M.NOTICE_ANS, st=-1)
        self.send(M.NOTICE_ANS, st=1, lines=[s[:16] for s in pages[page - 1]],
                  remaining=len(pages) - page)
        if page == len(pages) and self.char.notices_seen < self.server.notices_version:
            self.char.notices_seen = self.server.notices_version   # all pages reached the client
            self.save()

    def on_keepalive(self, msg):       # 39327: nothing to answer
        pass

    # --- options ---------------------------------------------------------------
    def on_options(self, msg):         # 288 -> 289
        self.send(M.OPTIONS_ANS, st=1, invitation=self.char.invitation)

    def on_options_set(self, msg):     # 290 -> 291
        v = msg.get("invitation")
        if v not in (0, 1):
            return self.send(M.OPTIONS_SET_ANS, st=-1)
        self.char.invitation = v
        self.save()
        self.send(M.OPTIONS_SET_ANS, st=1)

    # --- character ---------------------------------------------------------------
    def on_name(self, msg):            # 1280 -> 1281
        name = msg.get("name", "")
        if not _NAME_RE.match(name):
            return self.send(M.NAME_SET_ANS, st=M.ERR_NOT_ACCEPTABLE)
        if self.server.storage.name_taken(name, self.user):
            return self.send(M.NAME_SET_ANS, st=M.ERR_NAME_EXISTS)
        self.char.name = name
        self.save()
        self.send(M.NAME_SET_ANS, st=1)

    def _quote(self, msg, field, answer):
        q = msg.get("quote", "")
        if not _QUOTE_RE.match(q):
            return self.send(answer, st=M.ERR_NOT_ACCEPTABLE)
        setattr(self.char, field, q)
        self.save()
        self.send(answer, st=1)

    def on_quote_start(self, msg):     # 1282 -> 1283
        self._quote(msg, "quote_start", M.QUOTE_START_ANS)

    def on_quote_win(self, msg):       # 1284 -> 1285
        self._quote(msg, "quote_win", M.QUOTE_WIN_ANS)

    def on_attributes(self, msg):      # 1287 -> 1288
        self.send(M.ATTRIBUTES_ANS, st=1, **self.char.attributes())

    def on_skills(self, msg):          # 1289 -> 1290
        self.send(M.SKILLS_ANS, st=1, **self.char.skill_list())

    def on_skill_slots(self, msg):     # 1291 -> 1292
        slots = valid_slots(self.char, msg.get("slots", []))
        if slots is None:
            return self.send(M.SKILL_SLOTS_ANS, st=-1)
        self.char.slots = slots
        self.save()
        self.send(M.SKILL_SLOTS_ANS, st=1)

    def on_records(self, msg):         # 1296 -> 1297
        c = self.char
        self.send(M.RECORDS_ANS, st=1, fame=c.mp_fame, duel_grade=c.duel_grade,
                  mission_grade=c.mission_grade)

    def on_exp_fame_gold(self, msg):   # 1298 -> 1299
        c = self.char
        self.send(M.EXP_FAME_GOLD_ANS, st=1, exp=c.mp_exp, fame=c.mp_fame, gold=c.gold)

    # --- ranking -----------------------------------------------------------------
    def _table(self, cat):
        """Everyone sorted by the category value (1 Fame, 2 Duel, 3 Mission), best first."""
        key = {1: "mp_fame", 2: "duel_grade", 3: "mission_grade"}[cat]
        chars = self.server.storage.all_characters()
        chars.sort(key=lambda c: (-getattr(c, key), c.user_id))
        return [(i + 1, c.user_id, getattr(c, key)) for i, c in enumerate(chars)]

    def on_rank_mine(self, msg):       # 1300 -> 1301
        cat = msg.get("cat")
        if cat not in (1, 2, 3):
            return self.send(M.RANK_MINE_ANS, st=-1)
        for rank, uid, value in self._table(cat):
            if uid == self.user:
                return self.send(M.RANK_MINE_ANS, st=1, rank=rank, value=value)
        self.send(M.RANK_MINE_ANS, st=-1)

    def on_rank_list(self, msg):       # 1293 -> 1294; code = (cat+1)*10 + (sub+1)
        code = msg.get("code", 0)
        cat, sub = code // 10 - 1, code % 10 - 1
        if cat not in (0, 1, 2) or sub not in (0, 1):
            return self.send(M.RANK_LIST_ANS, st=-1)
        table = self._table(cat + 1)
        if sub == 0:                   # Top Rankers
            rows = table[:3]
        else:                          # Ranks Near Me: me in the middle when possible
            me = next((i for i, r in enumerate(table) if r[1] == self.user), 0)
            start = max(0, min(me - 1, len(table) - 3))
            rows = table[start:start + 3]
        # exactly 3 rows: the client keeps them in arrays of 3 and always draws 3 boxes
        # (06 §2.4, g:612-622); a missing row would be a null name. Empty rows pad the list.
        rows = [{"rank": r, "id": u, "value": v} for r, u, v in rows]
        rows += [{"rank": 0, "id": "", "value": 0}] * (3 - len(rows))
        self.send(M.RANK_LIST_ANS, st=1, rows=rows)

    # --- rooms and battles ----------------------------------------------------------
    def on_match(self, msg):           # 512 -> 513, 514 per other fighter, 1024
        if msg.get("mode") != 0 or self.battle is not None:
            return self.send(M.MATCH_ANS, st=-11)   # cw8 "Too many users online": 2v2 / missions later
        rng = self.server.rng
        me = B.from_character(self.char, 0)
        foe = B.cpu_fighter(rng, me, 1)
        self.battle, self.slot = B.Battle(rng, [me, foe], mode=0), 0
        # 513 before 514: O() clears the fighter list (06 §2.6); the client adds itself from 263
        self.send(M.MATCH_ANS, st=1, bg=self.battle.bg, slot=0, mode=0, unk=0)
        self.send(M.ROOM_JOIN, st=1, **foe.wire())
        self.send(M.ALL_READY, st=1)

    def on_round_ready(self, msg):     # 1025 -> 1026 next round, or 1032 when it is over
        b = self.battle
        if b is None:
            return
        if not b.over:
            return self.send(M.ROUND_START, st=1, bar_speed=0)
        res = B.duel_rewards(self.char, b, self.slot, self.server.rng)
        self.battle = None
        self.save()
        rank = next((r for r, uid, _ in self._table(2) if uid == self.user), 0)
        self.send(M.BATTLE_END, st=1, rank=rank, **res)

    def on_turn(self, msg):            # 1027 -> 1028
        b = self.battle
        if b is None or b.over:
            return
        turn = b.resolve({self.slot: (msg.get("target", 1), msg.get("action", 1), msg.get("hit", 20))})
        self.send(M.TURN_RESULT, st=1, **turn)

    def on_invite(self, msg):          # 768 -> 769
        self.send(M.INVITE_ANS, st=-11)


_HANDLERS = {
    M.LOGIN_FIRST: Session.on_login_first,
    M.LOGIN: Session.on_login,
    M.NOTICE: Session.on_notice,
    M.KEEPALIVE: Session.on_keepalive,
    M.OPTIONS: Session.on_options,
    M.OPTIONS_SET: Session.on_options_set,
    M.NAME_SET: Session.on_name,
    M.QUOTE_START: Session.on_quote_start,
    M.QUOTE_WIN: Session.on_quote_win,
    M.ATTRIBUTES: Session.on_attributes,
    M.SKILLS: Session.on_skills,
    M.SKILL_SLOTS: Session.on_skill_slots,
    M.RECORDS: Session.on_records,
    M.EXP_FAME_GOLD: Session.on_exp_fame_gold,
    M.RANK_MINE: Session.on_rank_mine,
    M.RANK_LIST: Session.on_rank_list,
    M.MATCH: Session.on_match,
    M.ROUND_READY: Session.on_round_ready,
    M.TURN: Session.on_turn,
    M.INVITE: Session.on_invite,
}
