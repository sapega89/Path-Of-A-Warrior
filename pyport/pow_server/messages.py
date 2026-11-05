"""Messages of POW Multiplayer with the original opcodes (PHASE_9 task 9.4).

Source: docs/analysis/06_multiplayer.md §2.4, checked against pyport/mp_java/:
the client writes in g.c(int) (g:1609-1704) and reads in g.a(k) (g:1888-2586).

Field kinds: "b" s8, "B" u8, "h" s16, "H" u16, "i" s32, int N = char[N] (zero padded).
(name, "list", count, sub) = repeated rows; count is a number or the name of a field read
before; sub is a kind (list of values) or a schema (list of dicts).
The client reads u16 with k.b() as a signed short, so "h"/"H" only differ in range checks.

fields are appended at the end: the original client ignores extra bytes, so a
server that sends them still talks to the original client (06 §6.2).
"""

# --- opcodes ---------------------------------------------------------------
LOGIN = 262                 # C->S char[12] id, char[4] ver (+ char[16] token)
LOGIN_ANS = 263
LOGIN_FIRST = 278           # C->S char[12] id, char[16] pwd, char[4] ver
LOGIN_FIRST_ANS = 279
KICKED = 280                # S->C push: another player connected with your UserID
NOTICE = 258
NOTICE_ANS = 259
OPTIONS = 288
OPTIONS_ANS = 289
OPTIONS_SET = 290
OPTIONS_SET_ANS = 291
MATCH = 512                 # C->S u8 mode (0 1v1, 1 2v2, 2 mission)
MATCH_ANS = 513
ROOM_JOIN = 514             # S->C push: a fighter enters the room
INVITE = 768
INVITE_ANS = 769
INVITED = 770               # S->C push: you were pulled into a room
ALL_READY = 1024            # S->C push
ROUND_READY = 1025          # C->S
ROUND_START = 1026
TURN = 1027                 # C->S u8 target slot, u8 action, u8 hit%
TURN_RESULT = 1028
STAGE_END = 1031
BATTLE_END = 1032
ROOM_LEAVE = 1035           # S->C push
STAGE_NEXT = 1036           # C->S
STAGE_INFO = 1037
STAGE_INTRO_DONE = 1038     # C->S
MATCH_CANCEL = 1286         # S->C push [guess] match not found / cancelled
NAME_SET = 1280
NAME_SET_ANS = 1281
QUOTE_START = 1282
QUOTE_START_ANS = 1283
QUOTE_WIN = 1284
QUOTE_WIN_ANS = 1285
ATTRIBUTES = 1287
ATTRIBUTES_ANS = 1288
SKILLS = 1289
SKILLS_ANS = 1290
SKILL_SLOTS = 1291
SKILL_SLOTS_ANS = 1292
RANK_LIST = 1293
RANK_LIST_ANS = 1294
RECORDS = 1296
RECORDS_ANS = 1297
EXP_FAME_GOLD = 1298
EXP_FAME_GOLD_ANS = 1299
RANK_MINE = 1300
RANK_MINE_ANS = 1301
SERVER_NOTICE = 1536        # S->C push
KEEPALIVE = 39327           # C->S, no body, no answer
# orders (pow_server/orders.py), opcodes the original never used
ORDER_INFO = 1792           # C->S -> 1793: my order, its members and who is online
ORDER_INFO_ANS = 1793
ORDER_CREATE = 1794         # C->S char[12] name
ORDER_CREATE_ANS = 1795
ORDER_JOIN = 1796           # C->S char[12] name
ORDER_JOIN_ANS = 1797
ORDER_LEAVE = 1798          # C->S
ORDER_LEAVE_ANS = 1799
# the chat (pow_server/chat.py); channel 0 lobby, 1 my order, 2 private (peer)
CHAT_READ = 1808            # C->S u8 channel, char[12] peer -> 1809: the last messages, marked read
CHAT_READ_ANS = 1809
CHAT_SEND = 1810            # C->S u8 channel, char[12] peer, char[40] text -> 1811
CHAT_SEND_ANS = 1811
CHAT_PUSH = 1812            # S->C push: a new message of a conversation I read
CHAT_PEERS = 1813           # C->S -> 1814: my private conversations, newest first
CHAT_PEERS_ANS = 1814
CHAT_UNREAD = 1815          # S->C push after the login: unread order / private messages
# 768 modes: 0 Challenge 1:1, 1 Challenge 2:2, 2 Invite An Ally (mission); 3: an
# order member fights a 2-on-2 duel on my side against two CPU fighters
INVITE_TEAM = 3

GAME_VER = "0111"           # GAMEVIL_GAME_VER of the MP manifest
EMPTY_SKILL = 99            # empty skill slot in 263 / 1291

# 263 status codes the client knows (g:1936-2002): -2 -> cw1 "register in POW single",
# -9 -> cw8 "too many users", anything else -> cw7 "network failure".
# -3: the session token is missing or wrong (the port's client goes back to Login).
LOGIN_NOT_REGISTERED = -2
LOGIN_BAD_TOKEN = -3
LOGIN_FULL = -9
# 279 reason (g:1921-1934): 0 -> cw14 id not registered, 1 -> cw15 wrong password, else cw0
REASON_NO_ID = 0
REASON_BAD_PASSWORD = 1
REASON_OTHER = 2
# 1281 / 1283 / 1285: -6 -> cw6 "name already exists", -49 / -15 -> cw5 "not acceptable"
ERR_NAME_EXISTS = -6
ERR_NOT_ACCEPTABLE = -49
# order answers (1795 / 1797 / 768 mode 3)
ERR_ORDER_NONE = -20        # no order with that name
ERR_ORDER_FULL = -21        # 30 members already
ERR_ORDER_IN = -22          # I am in an order already (create / join)
ERR_NOT_MEMBER = -23        # 768 mode 3: the player is not in my order
# chat answers (1809 / 1811)
ERR_TOO_FAST = -24          # too many messages in a short time
ERR_NO_ORDER = -25          # the order channel without an order
ERR_NO_PLAYER = -26         # private: no such UserID
ERR_SELF = -27              # private: a message to myself

# --- C->S schemas ------------------------------------------------------------
# tail of 262: the hero of the single-player save (task 9.10), what the original's
# Gamevil Live "Save User Data" sent with opcode 256. sp = 0: no save.
SP_HERO = (
    ("sp", "B"), ("sp_level", "B"), ("sp_hp", "H"), ("sp_mp", "H"), ("sp_atk", "H"), ("sp_def", "H"),
    ("sp_hp_bonus", "h"), ("sp_mp_bonus", "h"), ("sp_atk_bonus", "h"), ("sp_def_bonus", "h"),
    ("sp_face", "B"), ("sp_weapon", "B"), ("sp_skills", "list", 11, "B"), ("sp_slots", "list", 4, "B"),
    ("sp_progress", "B"),
)

C2S = {
    # token and the hero: , absent in the original
    LOGIN: (("id", 12), ("ver", 4), ("token", 16), *SP_HERO),
    LOGIN_FIRST: (("id", 12), ("pwd", 16), ("ver", 4)),
    256: (("id", 12), ("ver", 4)),                       # rudiment, same body as 262 (g:1635)
    NOTICE: (("page", "i"),),
    OPTIONS: (),
    OPTIONS_SET: (("invitation", "i"),),
    MATCH: (("mode", "B"),),
    INVITE: (("mode", "B"), ("id", 12)),
    ROUND_READY: (),
    TURN: (("target", "B"), ("action", "B"), ("hit", "B")),
    STAGE_NEXT: (),
    STAGE_INTRO_DONE: (),
    NAME_SET: (("name", 8),),
    QUOTE_START: (("quote", 20),),
    QUOTE_WIN: (("quote", 20),),
    ATTRIBUTES: (),
    SKILLS: (),
    SKILL_SLOTS: (("slots", "list", 4, "B"),),
    RANK_LIST: (("code", "B"), ("page", "i")),
    RECORDS: (),
    EXP_FAME_GOLD: (),
    RANK_MINE: (("cat", "B"),),
    KEEPALIVE: (),
    ORDER_INFO: (),
    ORDER_CREATE: (("name", 12),),
    ORDER_JOIN: (("name", 12),),
    ORDER_LEAVE: (),
    CHAT_READ: (("channel", "B"), ("peer", 12)),
    CHAT_SEND: (("channel", "B"), ("peer", 12), ("text", 40)),
    CHAT_PEERS: (),
}

# --- S->C schemas (after the status byte) -------------------------------------
_ROOM = (("bg", "B"), ("slot", "B"), ("mode", "B"), ("unk", "B"))


def _enc_turn(buf, msg):
    """1028 body (g:2247-2299), see 06 §2.5."""
    from pow_server.codec_bin import _put
    for a in ([*list(msg.get("actions", [])), 0, 0, 0, 0])[:4]:
        _put(buf, "B", a)
    recs = msg.get("records", [])
    if len(recs) > 4:
        raise ValueError("1028: at most 4 records (cK = byte[44])")
    _put(buf, "B", len(recs))
    for r in recs:
        for name, kind in _TURN_REC:
            _put(buf, kind, r.get(name, 0))
    _put(buf, "B", msg.get("unk", 0))
    for r in recs:
        if r.get("has2nd") == 1:
            for name, kind in _TURN_2ND:
                _put(buf, kind, r.get(name, 0))


def _dec_turn(data, pos, msg):
    from pow_server.codec_bin import _get
    acts = []
    for _ in range(4):
        v, pos = _get(data, pos, "B")
        acts.append(v)
    msg["actions"] = acts
    n, pos = _get(data, pos, "B")
    recs = []
    for _ in range(n):
        r = {}
        for name, kind in _TURN_REC:
            r[name], pos = _get(data, pos, kind)
        recs.append(r)
    msg["unk"], pos = _get(data, pos, "B")
    for r in recs:
        if r["has2nd"] == 1:
            for name, kind in _TURN_2ND:
                r[name], pos = _get(data, pos, kind)
    msg["records"] = recs
    return pos


_TURN_REC = (("actor", "B"), ("action", "B"), ("actor_hp", "h"), ("actor_mp", "B"),
             ("target", "B"), ("result", "B"), ("target_hp", "h"), ("target_mp", "B"),
             ("has2nd", "B"), ("flags", "B"))
_TURN_2ND = (("target2", "B"), ("result2", "B"), ("target2_hp", "h"), ("target2_mp", "B"))

# 263: 104 bytes (g:1936-1990)
PROFILE = (
    ("name", 8), ("face", "B"), ("level", "H"), ("wins", "i"), ("losses", "i"),
    ("hp", "H"), ("unk1", "H"), ("unk2", "H"), ("weapon", "B"),
    ("slots", "list", 4, "B"),
    ("quote_start", 20), ("quote_win", 20),
    ("skill_cost", "list", 11, "B"),            # MP cost of skills 3..13 (cI)
    ("aK", "B"), ("aL", "B"), ("aM", "B"), ("notices", "B"),
    ("unk3", 8), ("unk4", 8), ("unk5", "list", 3, "B"),
)

# 514: 72 bytes (g:2171-2226)
FIGHTER = (
    ("slot", "B"), ("name", 8), ("level", "H"), ("wins", "i"), ("losses", "i"), ("hp", "H"),
    ("weapon", "B"), ("face", "B"), ("quote_start", 20), ("quote_win", 20), ("cr", "B"),
    ("alt_name", 8),
)

_CHAT_ROW = (("id", 12), ("name", 8), ("text", 40))

S2C = {
    LOGIN_FIRST_ANS: (("token", 16),),          # the token for the next 262
    LOGIN_ANS: PROFILE,
    KICKED: (),
    NOTICE_ANS: (("lines", "list", 4, 16), ("remaining", "B")),
    SERVER_NOTICE: (("kind", "B"), ("lines", "list", 4, 16)),
    OPTIONS_ANS: (("invitation", "i"),),
    OPTIONS_SET_ANS: (),
    MATCH_ANS: _ROOM,
    INVITE_ANS: _ROOM,
    INVITED: _ROOM,
    ROOM_JOIN: FIGHTER,
    ROOM_LEAVE: (("slot", "B"),),
    STAGE_INFO: (("title", 14), ("stages", "B"), ("stage", "B")),
    ALL_READY: (),
    ROUND_START: (("bar_speed", "B"),),         # server-chosen speed (9a, 06 §6.2)
    TURN_RESULT: (("turn", "rest", _enc_turn, _dec_turn),),
    STAGE_END: (("bg", "B"),),
    BATTLE_END: (("win", "B"), ("gold", "h"), ("grade", "B"), ("fame", "h"), ("exp", "h"),
                 ("loot", 15), ("rank", "i"), ("unk1", "B"), ("unk2", "i"), ("unk3", "B"),
                 # the looted item for the single-player save (9.9), id 0 = none
                 ("item_id", "H"), ("item_atk", "h"), ("item_def", "h"), ("item_hp", "h"),
                 ("item_mp", "h")),
    MATCH_CANCEL: (),
    NAME_SET_ANS: (),
    QUOTE_START_ANS: (),
    QUOTE_WIN_ANS: (),
    ATTRIBUTES_ANS: (("hp", "h"), ("hp_bonus", "h"), ("mp", "h"), ("mp_bonus", "h"),
                     ("atk", "h"), ("atk_bonus", "h"), ("def", "h"), ("def_bonus", "h")),
    SKILLS_ANS: (("n", "B"), ("skills", "list", "n", (("id", "B"), ("level", "B")))),
    SKILL_SLOTS_ANS: (),
    # tail: the name of my order ("" = none), shown under Character > Records
    RECORDS_ANS: (("fame", "i"), ("duel_grade", "i"), ("mission_grade", "i"), ("order", 12)),
    EXP_FAME_GOLD_ANS: (("exp", "i"), ("fame", "i"), ("gold", "i")),
    RANK_MINE_ANS: (("rank", "i"), ("value", "i")),
    RANK_LIST_ANS: (("n", "B"), ("rows", "list", "n", (("rank", "i"), ("id", 12), ("value", "i")))),
    # name "" = in no order; rows: the leader, me, who is online, the others
    ORDER_INFO_ANS: (("name", 12), ("n", "B"),
                     ("rows", "list", "n", (("id", 12), ("name", 8), ("level", "H"), ("online", "B"),
                                            ("leader", "B")))),
    ORDER_CREATE_ANS: (),
    ORDER_JOIN_ANS: (),
    ORDER_LEAVE_ANS: (),
    # chat: rows oldest first; peer_name = the private peer's display name
    CHAT_READ_ANS: (("channel", "B"), ("peer", 12), ("peer_name", 8), ("n", "B"),
                    ("rows", "list", "n", _CHAT_ROW)),
    CHAT_SEND_ANS: (),
    CHAT_PUSH: (("channel", "B"), ("peer", 12), *_CHAT_ROW),
    CHAT_PEERS_ANS: (("n", "B"), ("rows", "list", "n", (("id", 12), ("name", 8), ("unread", "B"),
                                                       ("online", "B")))),
    CHAT_UNREAD: (("order", "B"), ("private", "B")),
}

# Error answers: only the status, except 279 which tells why (g:1921).
S2C_ERR = {LOGIN_FIRST_ANS: (("reason", "B"),)}

NAMES = {v: k for k, v in list(globals().items()) if k.isupper() and isinstance(v, int) and v >= 256}
