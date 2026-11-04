"""The POW Multiplayer server: sessions and the menu-side messages (PHASE_9 tasks 9.13, 9.14, 9.18).

Pure Python, no pygame and no I/O: a transport (pow_server/ws_server.py, or the in-game
LocalTransport of pow_mp/net/transport.py) hands every received frame payload to
Session.receive() and writes the frames the session passes to its `send` callback.

Done here: login 278/262 (+ PORT-EXTRA session token), duplicate login (280), notices
258/259, Options 288-291, Character 1280-1299, Ranking 1293/1300, keepalive.
Battles (Room below, resolved in pow_server/battle.py): Duel 1-on-1 / 2-on-2 against CPU
fighters and Solo Mission (512 mode 0/1/2 -> 513, 514, 1024 or 1037), Challenge 1:1 / 2:2 and
Invite An Ally between two players (768 -> 769 to me, 770 to the other player); 1025/1026,
1027/1028 per round; stages 1031/1036/1037/1038; 1025 after the end -> 1032.

PORT-EXTRA (asked by Andrey: bots when nobody is online): server bots (add_bots). They are
accounts nobody can log in to, always "online" with Invitation: Accept, listed in the Ranking,
so a player alone on the server can Challenge one or Invite one as an ally by its UserID. A bot
fights as a CPU fighter of about the inviter's level (battle.cpu_fighter) under its own name.
"""
import random
import re
import time

from pow_server import battle as B
from pow_server import codec_bin, loot, orders
from pow_server import messages as M
from pow_server.model import apply_sp_hero, default_character, valid_slots
from pow_server.storage import open_storage

MATCH_WAIT = 60                                # Andrey: a whole minute for a live opponent
MATCH_LEVELS = (10, 20)                        # level reach at first / after half the wait
# PORT-EXTRA: the standalone server's bots (UserID, display name, Ranking Fame / grades)
DEFAULT_BOTS = (("BLADE", "Blade", 900), ("RAVEN", "Raven", 600), ("TIGER", "Tiger", 400),
                ("SHADOW", "Shadow", 250), ("IRONFIST", "Ironfist", 100))
_ID_RE = re.compile(r"^[A-Z]{4,12}$")          # Login screen: A-Z, 4..12 (g:4888-4926)
_PWD_RE = re.compile(r"^[0-9]{4,12}$")         # password: digits, 4..12 (g:4930-4990)
_NAME_RE = re.compile(r"^[A-Za-z0-9]{1,8}$")   # Display Name: A-Z / a-z keyboard (g:2820-2866)
_QUOTE_RE = re.compile(r"^[ -~]{1,20}$")       # quotes: 1..20 printable characters


class GameServer:
    def __init__(self, storage=None, *, require_token=True, auto_register=True,
                 notices=(), notices_version=1, clock=time.monotonic, rng=None,
                 match_wait=MATCH_WAIT):
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
        self.match_wait = match_wait   # seconds a Duel waits for a live opponent, then a CPU
        self.queue = []                # [Session] waiting in 512 (oldest first)
        self.bots = {}                 # PORT-EXTRA: UserID -> Character of a server bot

    # --- PORT-EXTRA: server bots ---------------------------------------------------------
    def add_bots(self, bots=DEFAULT_BOTS):
        """Makes (or finds) the bot accounts. An ID a player already owns is skipped."""
        import secrets
        st = self.storage
        for uid, name, fame in bots:
            ch = st.load(uid) if st.has_account(uid) else None
            if ch is None and st.has_account(uid):
                continue
            if ch is not None and not ch.bot:
                continue                           # a player's account
            if ch is None:
                st.create_account(uid, "".join(secrets.choice("0123456789") for _ in range(12)))
                ch = default_character(uid)
                ch.bot = True
                ch.name, ch.mp_fame = ("" if st.name_taken(name, uid) else name), fame
                ch.duel_grade = ch.mission_grade = min(9, fame // 100)
                ch.wins, ch.losses = fame // 10, fame // 25
                ch.quote_start, ch.quote_win = "Nobody else? Fight me!", "Come back stronger."
                st.save(ch)
            self.bots[uid] = ch

    def bot_fighter(self, uid, me, slot, ally):
        """A bot entering a room: a CPU fighter of about my level, with the bot's name."""
        ch = self.bots[uid]
        f = B.cpu_fighter(self.rng, me, slot, ally=ally)
        f.name, f.keep_name = ch.name or uid[:8], True
        f.wins, f.losses = ch.wins, ch.losses
        f.quote_start, f.quote_win = ch.quote_start, ch.quote_win
        return f

    # --- matchmaking (9.15) ----------------------------------------------------------
    def find_opponent(self, s, mode):
        """A player waiting for the same kind of duel near my level: within MATCH_LEVELS, the
        range opening to the original's 20 levels once they have waited half the time."""
        now = self.clock()
        for other in self.queue:
            if other is s or other.closed or other.queued_mode != mode:
                continue
            reach = MATCH_LEVELS[1] if now - other.queued_at >= self.match_wait / 2 else MATCH_LEVELS[0]
            if abs(other.char.level - s.char.level) <= reach:
                return other
        return None

    def tick(self):
        """Called about once a second by the transport: a duel that waited match_wait gets a
        CPU fighter."""
        now = self.clock()
        for s in list(self.queue):
            if s.closed:
                self.queue.remove(s)
            elif now - s.queued_at >= self.match_wait:
                self.queue.remove(s)
                s.start_vs_cpu(s.queued_mode)

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
        self.room = None               # Room while in a battle
        self.queued_mode = None        # 512 mode while waiting for an opponent
        self.queued_at = 0
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
        if self in self.server.queue:
            self.server.queue.remove(self)
        if self.room is not None:      # a duel left is a loss, a mission left earns nothing
            room, self.room = self.room, None
            room.leave(self)
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
        if self.user and self.user != uid and self.server.online.get(self.user) is self:
            del self.server.online[self.user]   # a second 262 as another UserID on this session
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
    def _battle_end(self, room):
        """1032 with my own rewards, and out of the room."""
        b, m = room.battle, room.mission
        if m:
            stood = any(b.fighters[k].alive for k in room.human_slots)
            cleared = m["stage"] - (0 if stood and not b.team_alive(1) else 1)
            res = B.mission_rewards(self.char, b, self.slot, self.server.rng, cleared, m["stages"])
            cat = 3
        else:
            res = B.duel_rewards(self.char, b, self.slot, self.server.rng)
            cat = 2
        # loot (9.9): one single-player drop roll per foe beaten, ar.P() kinds 0 soldier /
        # 1 general / 2 boss; mission monsters are soldiers, the fighter of the last stage a boss
        if m:
            kills = [0, 0] * min(cleared, m["stages"] - 1) + ([2, 0] if cleared == m["stages"] else [])
        else:
            kills = [1] * sum(1 for f in b.fighters.values() if f.team != self.slot % 2) if res["win"] else []
        got = loot.roll(self.server.rng, self.char.level, kills)
        if got:
            res.update(loot=got["name"], item_id=got["id"], item_atk=got["atk"],
                       item_def=got["def"], item_hp=got["hp"], item_mp=got["mp"])
        room.players.pop(self.slot, None)
        self.room = None
        self.save()
        rank = next((r for r, uid, _ in self._table(cat) if uid == self.user), 0)
        self.send(M.BATTLE_END, st=1, rank=rank, **res)

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

    # --- PORT-EXTRA: orders (pow_server/orders.py) -------------------------------------
    def _my_order(self):
        """My order document; a stale Character.order (the order is gone) is cleared."""
        doc = orders.get(self.server.storage, self.char.order)
        if doc is None or self.user not in doc["members"]:
            if self.char.order:
                self.char.order = ""
                self.save()
            return None
        return doc

    def on_order_info(self, msg):      # 1792 -> 1793
        doc = self._my_order()
        if doc is None:
            return self.send(M.ORDER_INFO_ANS, st=1, name="", rows=[])
        st, online, rows = self.server.storage, self.server.online, []
        for uid in doc["members"]:
            ch = self.char if uid == self.user else st.load(uid)
            if ch is None:
                continue
            s = online.get(uid)
            rows.append({"id": uid, "name": ch.name or uid[:8], "level": ch.level,
                         "online": int(s is not None and not s.closed)})
        rows.sort(key=lambda r: (r["id"] != self.user, not r["online"]))   # me, online, others
        self.send(M.ORDER_INFO_ANS, st=1, name=doc["name"], rows=rows[:orders.MAX_MEMBERS])

    def _order_enter(self, msg, answer, fn):
        if self._my_order() is not None:
            return self.send(answer, st=M.ERR_ORDER_IN)
        name = (msg.get("name") or "").upper()
        res = fn(self.server.storage, name, self.user)
        if res == 1:
            self.char.order = name
            self.save()
        self.send(answer, st=res)

    def on_order_create(self, msg):    # 1794 -> 1795
        self._order_enter(msg, M.ORDER_CREATE_ANS, orders.create)

    def on_order_join(self, msg):      # 1796 -> 1797
        self._order_enter(msg, M.ORDER_JOIN_ANS, orders.join)

    def on_order_leave(self, msg):     # 1798 -> 1799
        if self.char.order:
            orders.leave(self.server.storage, self.char.order, self.user)
            self.char.order = ""
            self.save()
        self.send(M.ORDER_LEAVE_ANS, st=1)

    # --- rooms and battles ----------------------------------------------------------
    @property
    def battle(self):
        return self.room.battle if self.room else None

    @battle.setter
    def battle(self, value):           # tests: None drops the room
        if value is not None:
            raise ValueError("only None (drop the room) can be set")
        self.room = None

    @property
    def mission(self):
        return self.room.mission if self.room else None

    def on_match(self, msg):           # 512 -> 513, 514 per other fighter, 1024 (mission: 1037)
        """A Duel (mode 0 / 1) waits up to match_wait seconds for a player near my level (the
        client shows "Searching for opponent" until 513 comes, 06 §2.6), then gets a CPU
        fighter; a Solo Mission (2) starts at once with a CPU ally."""
        mode = msg.get("mode")
        if mode not in (0, 1, 2) or self.room is not None or self in self.server.queue:
            return self.send(M.MATCH_ANS, st=-11)
        if mode == 2 or self.server.match_wait <= 0:
            return self.start_vs_cpu(mode)
        other = self.server.find_opponent(self, mode)
        if other is None:
            self.queued_mode, self.queued_at = mode, self.server.clock()
            self.server.queue.append(self)
            return None
        self.server.queue.remove(other)
        rng = self.server.rng
        first = B.from_character(other.char, 0)      # the one who waited takes the left side
        second = B.from_character(self.char, 1)
        fighters = [first, second]
        if mode == 1:
            fighters += [B.cpu_fighter(rng, first, 2, ally=True), B.cpu_fighter(rng, second, 3, ally=True)]
        Room(self.server, mode, fighters, {0: other, 1: self}, answer=M.MATCH_ANS).start()

    def start_vs_cpu(self, mode):
        rng = self.server.rng
        me = B.from_character(self.char, 0)
        # slot % 2 = team, slot // 2 = row (06 §2.6): 1v1 uses 0/1, 2v2 and missions add an
        # ally at 2 and a second foe at 3
        if mode == 2:
            others = [B.cpu_fighter(rng, me, 2, ally=True)]
        else:
            others = [B.cpu_fighter(rng, me, 1)]
            if mode == 1:
                others += [B.cpu_fighter(rng, me, 2, ally=True), B.cpu_fighter(rng, me, 3)]
        Room(self.server, mode, [me, *others], {0: self}, self.char.sp_progress).start()

    def on_invite(self, msg):          # 768 -> 769 to me, 770 pushed to the other player
        """Challenge 1:1 / 2:2 (bz 0/1, the other player is the foe) and Invite An Ally (bz 2,
        the other player fights the mission next to me). No Accept/Deny dialog in the client:
        Options > Invitation decides (06 §2.6). Errors as the client shows them (g:2110-2146):
        -3 not online, -4 unregistered, -5 cannot be replied (busy), -12 yourself, -16 denied."""
        mode, uid = msg.get("mode"), msg.get("id", "")
        if mode not in (0, 1, 2, M.INVITE_TEAM) or self.room is not None or self in self.server.queue:
            return self.send(M.INVITE_ANS, st=-1)    # busy: in a battle or waiting for a Duel
        if uid == self.user:
            return self.send(M.INVITE_ANS, st=-12)
        if not self.server.storage.has_account(uid):
            return self.send(M.INVITE_ANS, st=-4)
        live = self.server.online.get(uid)
        them = live.char if live is not None and live.char is not None else self.server.storage.load(uid)
        if mode == M.INVITE_TEAM and not orders.same_order(self.server.storage, self.char, them):
            return self.send(M.INVITE_ANS, st=M.ERR_NOT_MEMBER)
        if uid in self.server.bots and uid not in self.server.online:
            return self._invite_bot(mode, uid)
        other = self.server.online.get(uid)
        if other is None or other.closed or other.char is None:
            return self.send(M.INVITE_ANS, st=-3)
        if other.room is not None or other in self.server.queue:
            return self.send(M.INVITE_ANS, st=-5)
        if not other.char.invitation:
            return self.send(M.INVITE_ANS, st=-16)
        if mode == M.INVITE_TEAM:
            return self._invite_team(other)
        rng = self.server.rng
        me = B.from_character(self.char, 0)
        them = B.from_character(other.char, 2 if mode == 2 else 1)
        fighters = [me, them]
        if mode == 1:                  # each player gets a CPU ally
            fighters += [B.cpu_fighter(rng, me, 2, ally=True), B.cpu_fighter(rng, them, 3, ally=True)]
        progress = max(self.char.sp_progress, other.char.sp_progress)
        Room(self.server, mode, fighters, {0: self, them.slot: other}, progress).start()

    def _invite_team(self, other):
        """PORT-EXTRA (orders): the order member fights next to me (slots 0 and 2) against two
        CPU fighters, each of about the level of the player it faces. On the wire and on the
        server it is a 2-on-2 Duel (mode 1): the clients, rewards and a player leaving work as
        in any 2-on-2."""
        rng = self.server.rng
        me = B.from_character(self.char, 0)
        them = B.from_character(other.char, 2)
        fighters = [me, them, B.cpu_fighter(rng, me, 1), B.cpu_fighter(rng, them, 3)]
        Room(self.server, 1, fighters, {0: self, 2: other}).start()

    def _invite_bot(self, mode, uid):
        """PORT-EXTRA: Challenge / Invite An Ally a server bot. The same room as against the
        CPU (start_vs_cpu), the bot in the invited player's place."""
        srv, rng = self.server, self.server.rng
        me = B.from_character(self.char, 0)
        bot = srv.bot_fighter(uid, me, 2 if mode == 2 else 1, ally=mode == 2)
        fighters = [me, bot]
        if mode == 1:
            fighters += [B.cpu_fighter(rng, me, 2, ally=True), B.cpu_fighter(rng, me, 3)]
        Room(srv, mode, fighters, {0: self}, self.char.sp_progress, answer=M.INVITE_ANS).start()

    def on_stage_intro_done(self, msg):    # 1038 -> 1024 once every player has seen the intro
        if self.room is not None:
            self.room.intro_done(self)

    def on_stage_next(self, msg):          # 1036 -> 514 per new foe, 1037
        if self.room is not None:
            self.room.stage_next(self)

    def on_round_ready(self, msg):     # 1025 -> 1026 next round, 1031 next stage or 1032 the end
        if self.room is not None:
            self.room.round_ready(self)

    def on_turn(self, msg):            # 1027 -> 1028 once every player has chosen
        if self.room is not None:
            self.room.turn(self, (msg.get("target", 1), msg.get("action", 1), msg.get("hit", 20)))


class Room:
    """One battle and the players in it (one for the games against the CPU, two for Challenge
    and Invite An Ally). The server waits for the 1027 of every player still fighting before it
    resolves the round, and sends the same 1028 to all of them. A player who has fallen waits
    in 103 for 1032 (g:683-684) while the others fight on. The client gives itself a time limit
    to choose (ba = 10, then Defend, g:488-493), so only a dropped connection can stall a round:
    the transport closes an idle session and the round goes on without it."""

    def __init__(self, server, mode, fighters, players, progress=0, answer=None):
        self.server = server
        self.answer = answer           # the opening message for everyone (513 for a match)
        self.mode = mode
        self.players = dict(players)   # slot -> Session, the humans still connected
        self.human_slots = set(players)
        rng = server.rng
        self.mission = None
        if mode == 2:
            stages = B.mission_stages(progress)
            self.mission = {"title": rng.choice(B.MISSION_TITLES), "stages": stages, "stage": 1}
            fighters = fighters + B.mission_wave(rng, self._strongest(fighters), 1, stages)
        self._name_cpus(fighters)
        self.battle = B.Battle(rng, fighters, mode=mode)
        self.turns = {}                # slot -> (target, action, hit) of this round
        self.waiting_end = set()       # fallen players whose client waits for 1032
        self.ready = set()             # players past 104 (1036) or the stage intro (1038)
        self.stage_bg = None

    @staticmethod
    def _strongest(fighters):
        humans = [f for f in fighters if not f.cpu] or fighters
        return max(humans, key=lambda f: (f.max_hp, f.atk))

    def _name_cpus(self, fighters, keep=()):
        """No two CPU fighters share a name, nor a player's (monsters keep theirs). `keep`:
        fighters already in the battle, whose names stay and are taken."""
        taken = {f.name for f in fighters if not f.cpu or f.keep_name} | {f.name for f in keep}
        cpus = [f for f in fighters if f.cpu and not f.monster and not f.keep_name]
        names = [n for n in B.CPU_NAMES if n not in taken]
        for f, name in zip(cpus, self.server.rng.sample(names, len(cpus)), strict=True):
            f.name = name

    def start(self):
        b = self.battle
        for slot, s in self.players.items():
            s.room, s.slot = self, slot
            # 513 (or 769 / 770) before 514: O() clears the fighter list (06 §2.6); the client
            # adds itself from 263
            op = self.answer or (M.MATCH_ANS if len(self.players) == 1 else
                                 (M.INVITE_ANS if slot == 0 else M.INVITED))
            s.send(op, st=1, bg=b.bg, slot=slot, mode=self.mode, unk=0)
            for f in b.fighters.values():
                if f.slot != slot:
                    s.send(M.ROOM_JOIN, st=1, **f.wire())
            if self.mission:
                self._stage_info(s)    # -> 91, the client answers 1038 -> 1024
            else:
                s.send(M.ALL_READY, st=1)

    # --- who is still playing -------------------------------------------------------
    def fighting(self):
        """Slots of the connected players whose fighter stands."""
        return {slot for slot in self.players if self.battle.fighters[slot].alive}

    def _stage_info(self, s):
        m = self.mission
        s.send(M.STAGE_INFO, st=1, title=m["title"][:14], stages=m["stages"], stage=m["stage"])

    def _mission_left(self):
        """Another stage follows the cleared one."""
        m, b = self.mission, self.battle
        return bool(m) and b.team_alive(0) and not b.team_alive(1) and m["stage"] < m["stages"]

    # --- messages -----------------------------------------------------------------
    def intro_done(self, s):           # 1038
        if not self.mission or s.slot not in self.fighting():
            return
        self.ready.add(s.slot)
        self._release_intro()

    def _release_intro(self):
        if self.mission and self.ready and self.ready >= self.fighting():
            for slot in sorted(self.ready & self.fighting()):
                self.players[slot].send(M.ALL_READY, st=1)
            self.ready.clear()

    def stage_next(self, s):           # 1036
        if not self._mission_left() or s.slot not in self.fighting():
            return
        self.ready.add(s.slot)
        self._release_stage()

    def _release_stage(self):
        # the client clears the old foes when it sends 1036 (g:943-962), so the new 514s go out
        # once every player has sent it
        if not (self._mission_left() and self.ready and self.ready >= self.fighting()):
            return
        self.ready.clear()
        m, b = self.mission, self.battle
        m["stage"] += 1
        self.stage_bg = None
        mine = [f for f in b.fighters.values() if f.team == 0]
        foes = B.mission_wave(self.server.rng, self._strongest(mine), m["stage"], m["stages"])
        self._name_cpus(foes, keep=mine)   # the clients know the names of mine: only the new
        b.new_wave(foes)
        for slot in sorted(self.fighting()):
            s = self.players[slot]
            for f in foes:
                s.send(M.ROOM_JOIN, st=1, **f.wire())
            self._stage_info(s)

    def turn(self, s, choice):         # 1027
        if s.slot not in self.fighting():
            return None
        if self.battle.over:           # the other side hung up while I was choosing
            return s.send(M.TURN_RESULT, st=1, actions=[0] * 4, records=[])
        self.turns[s.slot] = choice
        self._resolve_if_ready()

    def _resolve_if_ready(self):
        playing = self.fighting()
        if not self.turns or not (self.battle.over or set(self.turns) >= playing):
            return None
        if self.battle.over:           # someone hung up: answer those who already chose
            for slot in sorted(self.turns):
                self.players[slot].send(M.TURN_RESULT, st=1, actions=[0] * 4, records=[])
            self.turns.clear()
            return self._flush_end()
        turn = self.battle.resolve({k: v for k, v in self.turns.items() if k in playing})
        self.turns.clear()
        for slot in sorted(playing):
            self.players[slot].send(M.TURN_RESULT, st=1, **turn)
        self._flush_end()

    def round_ready(self, s):          # 1025
        b, me = self.battle, self.battle.fighters[s.slot]
        if not b.over and me.alive:
            return s.send(M.ROUND_START, st=1, bar_speed=0)
        if me.alive and self._mission_left():
            if self.stage_bg is None:
                self.stage_bg = b.bg = B.battle_background(self.server.rng)
            return s.send(M.STAGE_END, st=1, bg=self.stage_bg)   # -> 104 "Stage N Complete!", 1036
        self.waiting_end.add(s.slot)
        self._flush_end()

    def _flush_end(self):
        """1032 to the fallen players once nobody is left to play on: then the CPU fighters
        left fight it out here (the client of a fallen player stops, g:683-684)."""
        if not self.waiting_end or self.fighting() - self.waiting_end:
            return                     # someone still plays on (a next stage too)
        b = self.battle
        b.finish()
        for slot in sorted(self.waiting_end):
            self.players[slot]._battle_end(self)
        self.waiting_end.clear()

    def leave(self, s):
        """A player hung up ("Exit Battle" hangs up and logs in again, g:2990-2997)."""
        slot = s.slot
        if self.players.get(slot) is not s:
            return
        del self.players[slot]
        self.turns.pop(slot, None)
        self.ready.discard(slot)
        self.waiting_end.discard(slot)
        b, f = self.battle, self.battle.fighters[slot]
        if not b.over and not self.mission:
            if self.players and self.mode == 1:
                f.cpu = True           # the team plays on, a CPU takes the fighter over
            else:
                f.hp = 0
                if f not in b.beaten:  # the one who stayed beat them: Fame / EXP / gold
                    b.beaten.append(f)
            B.duel_rewards(s.char, b, slot, self.server.rng)   # a duel left is a loss
            s.save()
        elif not self.mission:
            # the duel is over but this player hung up before 1025 -> 1032 (s is still in
            # players, so _battle_end has not run): the result counts all the same, a loss too
            B.duel_rewards(s.char, b, slot, self.server.rng)
            s.save()
        elif self.mission:
            f.cpu = True               # the ally fights on; the mission left earns nothing
        if self.players:
            self._resolve_if_ready()
            self._release_intro()
            self._release_stage()
            self._flush_end()

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
    M.STAGE_NEXT: Session.on_stage_next,
    M.STAGE_INTRO_DONE: Session.on_stage_intro_done,
    M.INVITE: Session.on_invite,
    M.ORDER_INFO: Session.on_order_info,
    M.ORDER_CREATE: Session.on_order_create,
    M.ORDER_JOIN: Session.on_order_join,
    M.ORDER_LEAVE: Session.on_order_leave,
}
