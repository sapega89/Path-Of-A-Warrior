"""PHASE_9: the server's menu-side messages (login, character, ranking, options)."""
import random

import pytest

from pow_server import codec_bin, messages as M
from pow_server.server import GameServer


class Client:
    """A fake client: sends C->S messages, keeps the decoded S->C ones."""
    def __init__(self, server):
        self.got = []
        self.session = server.connect(lambda f: self.got.extend(
            codec_bin.decode(p, from_client=False) for p in codec_bin.unframe(f)[0]))

    def ask(self, op, **fields):
        self.got.clear()
        frame = codec_bin.encode(op, fields, to_client=False)
        self.session.receive(codec_bin.unframe(frame)[0][0])
        return self.got[-1] if self.got else None


def login(server, uid="ANDREY", pwd="1234"):
    first = Client(server)
    ans = first.ask(M.LOGIN_FIRST, id=uid, pwd=pwd, ver=M.GAME_VER)
    assert ans["op"] == 279 and ans["st"] == 1 and len(ans["token"]) == 16
    first.session.close()                      # the client hangs up after 279 (g:1912-1920)
    c = Client(server)
    prof = c.ask(M.LOGIN, id=uid, ver=M.GAME_VER, token=ans["token"])
    assert prof["op"] == 263 and prof["st"] == 1
    return c, prof


@pytest.fixture(params=["sqlite", "memory"])
def server(request):
    from pow_server.storage import MemoryStorage, Storage
    st = Storage() if request.param == "sqlite" else MemoryStorage()
    return GameServer(st, notices=[["Welcome to the", "new server!"], ["Page two"]],
                      rng=random.Random(7), match_wait=0)


def test_login_creates_account_and_profile(server):
    c, prof = login(server)
    assert prof["name"] == "ANDREY" and prof["level"] == 1 and prof["slots"] == [3, 11, 99, 99]
    assert prof["notices"] == 2
    page = c.ask(M.NOTICE, page=1)
    assert page["lines"][:2] == ["Welcome to the", "new server!"] and page["remaining"] == 1
    assert c.ask(M.NOTICE, page=2)["remaining"] == 0
    _, again = login(server)
    assert again["notices"] == 0               # notices are shown once


def test_notices_survive_a_dropped_connection(server):
    c, prof = login(server)
    assert prof["notices"] == 2
    c.ask(M.NOTICE, page=1)
    c.session.close()                          # dropped before the last page
    c, prof = login(server)
    assert prof["notices"] == 2
    c.ask(M.NOTICE, page=1)
    c.ask(M.NOTICE, page=2)
    _, prof = login(server)
    assert prof["notices"] == 0


def test_login_errors(server):
    login(server)
    c = Client(server)
    assert c.ask(M.LOGIN_FIRST, id="ANDREY", pwd="9999", ver="0111")["reason"] == M.REASON_BAD_PASSWORD
    assert c.ask(M.LOGIN_FIRST, id="ab", pwd="1234", ver="0111")["st"] != 1
    assert c.ask(M.LOGIN, id="NOBODY", ver="0111")["st"] == M.LOGIN_NOT_REGISTERED
    assert c.ask(M.LOGIN, id="ANDREY", ver="0111")["st"] == M.LOGIN_BAD_TOKEN       # no token
    assert c.ask(M.LOGIN, id="ANDREY", ver="0111", token="0" * 16)["st"] == M.LOGIN_BAD_TOKEN
    assert c.ask(M.ATTRIBUTES) is None         # not logged in: ignored


def test_no_auto_register():
    s = GameServer(auto_register=False)
    assert Client(s).ask(M.LOGIN_FIRST, id="ANDREY", pwd="1234", ver="0111")["reason"] == M.REASON_NO_ID


def test_legacy_login_without_token():
    s = GameServer(require_token=False)
    login(s)
    assert Client(s).ask(M.LOGIN, id="ANDREY", ver="0111")["st"] == 1


def test_second_login_kicks_the_first(server):
    a, _ = login(server)
    b, _ = login(server)
    assert a.got[-1]["op"] == M.KICKED and a.session.closed and not b.session.closed
    assert server.online["ANDREY"] is b.session


def test_display_name_and_quotes(server):
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "OLGA")
    assert a.ask(M.NAME_SET, name="Warrior")["st"] == 1
    assert b.ask(M.NAME_SET, name="WARRIOR")["st"] == M.ERR_NAME_EXISTS
    assert b.ask(M.NAME_SET, name="bad name")["st"] == M.ERR_NOT_ACCEPTABLE
    assert a.ask(M.QUOTE_START, quote="Fight me!")["st"] == 1
    assert a.ask(M.QUOTE_WIN, quote="")["st"] == M.ERR_NOT_ACCEPTABLE
    _, prof = login(server, "ANDREY")
    assert prof["name"] == "Warrior" and prof["quote_start"] == "Fight me!"


def test_character_screens(server):
    c, _ = login(server)
    att = c.ask(M.ATTRIBUTES)
    assert att["op"] == 1288 and att["hp"] > 0
    sk = c.ask(M.SKILLS)
    assert sk["n"] == 2 and sk["skills"] == [{"id": 3, "level": 1}, {"id": 11, "level": 1}]
    assert c.ask(M.SKILL_SLOTS, slots=[99, 3, 99, 99])["st"] == 1
    assert c.ask(M.SKILL_SLOTS, slots=[4, 99, 99, 99])["st"] != 1      # not learned
    assert c.ask(M.SKILL_SLOTS, slots=[3, 3, 99, 99])["st"] != 1       # twice
    assert c.ask(M.RECORDS)["op"] == 1297
    assert c.ask(M.EXP_FAME_GOLD)["gold"] == 0


def test_options(server):
    c, _ = login(server)
    assert c.ask(M.OPTIONS)["invitation"] == 1
    assert c.ask(M.OPTIONS_SET, invitation=0)["st"] == 1
    assert c.ask(M.OPTIONS)["invitation"] == 0
    assert c.ask(M.OPTIONS_SET, invitation=5)["st"] != 1


def test_ranking(server):
    fame = {"AAAA": 5, "BBBB": 50, "CCCC": 20, "DDDD": 1, "EEEE": 9}
    clients = {}
    for uid, f in fame.items():
        clients[uid], _ = login(server, uid)
        clients[uid].session.char.mp_fame = f
        clients[uid].session.save()
    me = clients["EEEE"]
    assert me.ask(M.RANK_MINE, cat=1) == {"op": 1301, "st": 1, "rank": 3, "value": 9}
    top = me.ask(M.RANK_LIST, code=11, page=1)       # Fame, Top Rankers
    assert [r["id"] for r in top["rows"]] == ["BBBB", "CCCC", "EEEE"]
    near = clients["DDDD"].ask(M.RANK_LIST, code=12, page=1)   # Fame, Ranks Near Me (last)
    assert [r["rank"] for r in near["rows"]] == [3, 4, 5]
    assert me.ask(M.RANK_LIST, code=99, page=1)["st"] != 1


def test_ranking_always_three_rows(server):
    """The client draws 3 boxes whatever arrives, so a short table is padded (g:612-622)."""
    c, _ = login(server, "SOLO")
    rows = c.ask(M.RANK_LIST, code=21, page=1)["rows"]
    assert [r["id"] for r in rows] == ["SOLO", "", ""]


def test_unknown_match_mode(server):
    c, _ = login(server)
    assert c.ask(M.MATCH, mode=3) == {"op": 513, "st": -11}


def _duel(c, action=0, hit=88, rounds=60, mode=0):
    """Play a duel to the end with one action; returns (513, first 514, every 1028, 1032)."""
    c.ask(M.MATCH, mode=mode)
    room, fighter = c.got[0], c.got[1]
    turns = []
    for _ in range(rounds):
        ans = c.ask(M.ROUND_READY)
        if ans["op"] == M.BATTLE_END:
            return room, fighter, turns, ans
        assert ans["op"] == M.ROUND_START and ans["st"] == 1
        turns.append(c.ask(M.TURN, target=1, action=action, hit=hit))
    raise AssertionError("the duel did not end in %d rounds" % rounds)


def test_duel_vs_cpu(server):
    c, prof = login(server)
    room, fighter, turns, end = _duel(c)
    assert room["op"] == 513 and room["st"] == 1 and room["slot"] == 0 and room["mode"] == 0
    assert fighter["op"] == 514 and fighter["slot"] == 1
    assert 30 <= fighter["face"] <= 33                      # CPU fighter (g:2197-2206)
    assert 3 <= len(turns) <= 40
    for t in turns:
        assert t["op"] == 1028 and t["st"] == 1 and 1 <= len(t["records"]) <= 2
        for r in t["records"]:
            assert r["action"] not in (1, 2)                # stances never get a record
            assert 0 <= r["actor_mp"] <= 100 and r["actor_hp"] >= 0
    last = turns[-1]["records"][-1]
    assert last["target_hp"] == 0 or last["actor_hp"] == 0 or any(
        r["target_hp"] == 0 for t in turns[-1:] for r in t["records"])
    assert end["op"] == 1032 and end["win"] in (0, 1)
    assert (end["loot"] == "NONE") == (end["item_id"] == 0)
    ch = server.storage.load("ANDREY")
    assert (ch.wins, ch.losses) == ((1, 0) if end["win"] else (0, 1))
    assert c.session.battle is None
    c.ask(M.MATCH, mode=0)                                  # a new duel can start
    assert [m["op"] for m in c.got] == [513, 514, 1024] and c.got[0]["st"] == 1


def test_duel_attacking_with_perfect_hits_usually_wins(server):
    wins = 0
    for i in range(6):
        c, _ = login(server, "PLAYER" + "ABCDEF"[i])
        wins += _duel(c, hit=100)[3]["win"]
    assert wins >= 4


def test_leaving_a_duel_counts_as_a_loss(server):
    c, _ = login(server)
    c.ask(M.MATCH, mode=0)
    c.ask(M.ROUND_READY)
    c.session.close()                    # Exit Battle: the client hangs up (g:2990-2997)
    ch = server.storage.load("ANDREY")
    assert (ch.wins, ch.losses) == (0, 1)
    c2, prof = login(server)
    assert prof["losses"] == 1
    c2.ask(M.MATCH, mode=0)
    assert c2.got[0]["st"] == 1


def test_turn_without_a_battle_is_ignored(server):
    c, _ = login(server)
    assert c.ask(M.TURN, target=1, action=0, hit=50) is None
    assert c.ask(M.ROUND_READY) is None


def test_garbage_is_ignored(server):
    c = Client(server)
    c.session.receive(b"\x01")
    c.session.receive(b"\x39\x30")              # unknown opcode
    assert c.got == []


def test_storage_survives_restart(tmp_path):
    from pow_server.storage import Storage
    db = str(tmp_path / "mp.sqlite")
    s = GameServer(Storage(db))
    c, _ = login(s)
    c.ask(M.NAME_SET, name="Keep")
    s2 = GameServer(Storage(db))
    _, prof = login(s2)
    assert prof["name"] == "Keep"


def test_duel_2v2(server):
    c, _ = login(server)
    c.ask(M.MATCH, mode=1)
    assert [m["op"] for m in c.got] == [513, 514, 514, 514, 1024]
    assert c.got[0]["mode"] == 1 and c.got[0]["slot"] == 0
    assert sorted(m["slot"] for m in c.got[1:4]) == [1, 2, 3]
    assert len({m["name"] for m in c.got[1:4]}) == 3
    c.session.battle = None
    room, fighter, turns, end = _duel(c, mode=1, hit=100, rounds=80)
    assert room["mode"] == 1
    assert any(len(t["records"]) > 2 for t in turns)       # four fighters act in one round
    for t in turns:
        assert len(t["records"]) <= 4
    assert end["op"] == 1032


def test_2v2_ends_when_i_fall(server):
    """The client goes to 103 when its own HP is 0 (g:683-684): the server must answer 1032."""
    c, _ = login(server)
    c.ask(M.MATCH, mode=1)
    b = c.session.battle
    b.fighters[0].hp = 0
    end = c.ask(M.ROUND_READY)
    assert end["op"] == 1032 and b.over


def _mission(c, hit=100, rounds=200):
    """Solo Mission to the end: returns (stage infos, 1031 count, 1032)."""
    c.ask(M.MATCH, mode=2)
    ops = [m["op"] for m in c.got]
    assert ops[:4] == [513, 514, 514, 514] and ops[4] == 1037
    assert c.got[0]["mode"] == 2
    faces = [m["face"] for m in c.got[1:4]]
    assert faces.count(10) == 2 and 30 <= faces[0] <= 33   # an ally, two monsters (spr_mon)
    infos, stage_ends = [c.got[4]], 0
    assert c.ask(M.STAGE_INTRO_DONE)["op"] == 1024
    for _ in range(rounds):
        ans = c.ask(M.ROUND_READY)
        if ans["op"] == M.BATTLE_END:
            return infos, stage_ends, ans
        if ans["op"] == M.STAGE_END:
            stage_ends += 1
            c.ask(M.STAGE_NEXT)
            assert [m["op"] for m in c.got] == [514, 514, 1037]
            infos.append(c.got[-1])
            assert c.ask(M.STAGE_INTRO_DONE)["op"] == 1024
            continue
        assert ans["op"] == M.ROUND_START
        foes = [s for s, f in c.session.battle.fighters.items() if f.team == 1 and f.alive]
        c.ask(M.TURN, target=foes[0], action=0, hit=hit)
    raise AssertionError("the mission did not end")


def test_solo_mission(server):
    c, _ = login(server)
    infos, stage_ends, end = _mission(c)
    stages = infos[0]["stages"]
    assert stages == 2 and [i["stage"] for i in infos] == list(range(1, len(infos) + 1))
    assert end["op"] == 1032
    ch = server.storage.load("ANDREY")
    assert (ch.wins, ch.losses) == (0, 0)                    # missions do not count (g:2313)
    if end["win"]:
        assert stage_ends == stages - 1 and ch.mission_grade == end["grade"] > 0
    assert ch.gold == end["gold"] and c.session.battle is None


def test_mission_stages_follow_single_player_progress():
    from pow_server import battle as B
    assert [B.mission_stages(p) for p in (0, 6, 12, 100)] == [2, 3, 4, 6]


# --- Challenge and Invite An Ally: two players (768 / 769 / 770) ---------------------------
def _pair(server, mode):
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    b.got.clear()
    ans = a.ask(M.INVITE, mode=mode, id="BORYS")
    assert ans is not None and a.got[0]["op"] == M.INVITE_ANS and a.got[0]["st"] == 1
    assert b.got[0]["op"] == M.INVITED and b.got[0]["st"] == 1
    return a, b


def _ops(c):
    return [m["op"] for m in c.got]


def test_invite_errors(server):
    a, _ = login(server, "ANDREY")
    assert a.ask(M.INVITE, mode=0, id="ANDREY")["st"] == -12     # "You cannot invite yourself."
    assert a.ask(M.INVITE, mode=0, id="NOBODY")["st"] == -4      # "Unregistered user!"
    b, _ = login(server, "BORYS")
    b.session.close()
    assert a.ask(M.INVITE, mode=0, id="BORYS")["st"] == -3       # "The user is not online."
    b, _ = login(server, "BORYS")
    b.ask(M.OPTIONS_SET, invitation=0)
    assert a.ask(M.INVITE, mode=0, id="BORYS")["st"] == -16      # "Your invitation is denied"
    b.ask(M.OPTIONS_SET, invitation=1)
    b.ask(M.MATCH, mode=0)
    assert a.ask(M.INVITE, mode=0, id="BORYS")["st"] == -5       # busy: "cannot be replied"
    assert a.ask(M.INVITE, mode=7, id="BORYS")["st"] == -1


def _play(a, b, rounds=120):
    """Both players attack until both get 1032; returns (every 1028 of a, a's 1032, b's 1032)."""
    turns, ends = [], {}
    for _ in range(rounds):
        for c in (a, b):
            if c in ends:
                continue
            pushed = [m for m in c.got if m["op"] == M.BATTLE_END]
            if pushed:                                         # 1032 pushed while waiting
                ends[c] = pushed[0]
                continue
            ans = c.ask(M.ROUND_READY)
            if ans is None:
                continue                                       # fallen: waiting for 1032
            if ans["op"] == M.BATTLE_END:
                ends[c] = ans
        for c in (a, b):
            if c in ends:
                continue
            for m in c.got:                                     # 1032 pushed while waiting
                if m["op"] == M.BATTLE_END:
                    ends[c] = m
        if len(ends) == 2:
            return turns, ends[a], ends[b]
        live = [c for c in (a, b) if c not in ends and c.got and c.got[-1]["op"] == M.ROUND_START]
        for i, c in enumerate(live):
            room = c.session.room
            foes = [s for s, f in room.battle.fighters.items()
                    if f.alive and f.team != c.session.slot % 2]
            other = live[1 - i] if len(live) == 2 else None
            if other is not None:
                other.got.clear()
            ans = c.ask(M.TURN, target=foes[0], action=0, hit=100)
            if i == 0 and len(live) == 2:
                assert ans is None                              # waits for the other player
            else:
                assert ans["op"] == M.TURN_RESULT
                if other is not None:
                    assert other.got[-1] == ans                 # the same round for both
                turns.append(ans)
    raise AssertionError("no end in %d rounds" % rounds)


def test_challenge_1v1_between_players(server):
    a, b = _pair(server, 0)
    assert _ops(a) == [769, 514, 1024] and _ops(b) == [770, 514, 1024]
    assert a.got[0]["slot"] == 0 and b.got[0]["slot"] == 1 and a.got[0]["bg"] == b.got[0]["bg"]
    assert a.got[1]["slot"] == 1 and a.got[1]["name"] == "BORYS" and a.got[1]["face"] < 10
    assert b.got[1]["slot"] == 0 and b.got[1]["name"] == "ANDREY"
    turns, ea, eb = _play(a, b)
    assert {ea["win"], eb["win"]} == {0, 1} and turns
    ca, cb = server.storage.load("ANDREY"), server.storage.load("BORYS")
    assert ca.wins + cb.wins == 1 and ca.losses + cb.losses == 1
    assert a.session.room is None and b.session.room is None
    a.ask(M.MATCH, mode=0)
    assert a.got[0]["st"] == 1                                  # free for the next battle


def test_challenge_2v2_each_player_with_a_cpu_ally(server):
    a, b = _pair(server, 1)
    assert _ops(a) == [769, 514, 514, 514, 1024] and _ops(b) == [770, 514, 514, 514, 1024]
    fs = a.session.room.battle.fighters
    assert not fs[0].cpu and not fs[1].cpu and fs[2].cpu and fs[3].cpu
    turns, ea, eb = _play(a, b, rounds=200)
    assert {ea["win"], eb["win"]} == {0, 1}


def test_leaving_a_challenge(server):
    a, b = _pair(server, 0)
    a.ask(M.ROUND_READY)
    b.ask(M.ROUND_READY)
    assert a.ask(M.TURN, target=1, action=0, hit=50) is None
    a.got.clear()
    b.session.close()                                           # B hangs up mid-round
    assert a.got and a.got[-1]["op"] == M.TURN_RESULT and a.got[-1]["records"] == []
    end = a.ask(M.ROUND_READY)
    assert end["op"] == M.BATTLE_END and end["win"] == 1
    assert server.storage.load("BORYS").losses == 1


def test_invite_an_ally_to_a_mission(server):
    a, b = _pair(server, 2)
    assert _ops(a)[:4] == [769, 514, 514, 514] and _ops(a)[-1] == 1037
    assert b.got[0]["slot"] == 2 and _ops(b)[-1] == 1037
    assert a.ask(M.STAGE_INTRO_DONE) is None                    # waits for the ally's intro
    b.got.clear()
    assert a.got == [] and b.ask(M.STAGE_INTRO_DONE)["op"] == 1024
    stage_ends = 0
    for _ in range(200):
        for c in (a, b):
            if c.session.room is None:
                continue
            ans = c.ask(M.ROUND_READY)
            if ans and ans["op"] == M.STAGE_END:
                stage_ends += 1
        live = [c for c in (a, b) if c.got and c.got[-1]["op"] == M.ROUND_START]
        staged = [c for c in (a, b) if c.got and c.got[-1]["op"] == M.STAGE_END]
        ends = [c for c in (a, b) if any(m["op"] == M.BATTLE_END for m in c.got)]
        if ends and all(c.session.room is None for c in (a, b)):
            break
        if staged:
            for c in staged:
                c.got.clear()
            for c in staged:
                c.session.receive(codec_bin.unframe(codec_bin.encode(M.STAGE_NEXT, {}, to_client=False))[0][0])
            for c in staged:
                assert _ops(c) == [514, 514, 1037]
                c.got.clear()
            for c in staged:
                c.session.receive(codec_bin.unframe(codec_bin.encode(M.STAGE_INTRO_DONE, {}, to_client=False))[0][0])
            assert all(_ops(c) == [1024] for c in staged)
            continue
        for c in live:
            room = c.session.room
            foes = [s for s, f in room.battle.fighters.items() if f.alive and f.team == 1]
            c.ask(M.TURN, target=foes[0], action=0, hit=100)
    else:
        raise AssertionError("the mission did not end")
    assert a.session.room is None and b.session.room is None
    ca, cb = server.storage.load("ANDREY"), server.storage.load("BORYS")
    assert ca.gold > 0 or cb.gold > 0
    assert (ca.wins, ca.losses, cb.wins, cb.losses) == (0, 0, 0, 0)
    assert stage_ends >= 2                                      # both players past stage 1


def test_bot_accepts_and_plays(server):
    from pow_server.bot import Bot
    bot = Bot(server, "RIVAL")
    a, _ = login(server, "ANDREY")
    a.ask(M.INVITE, mode=0, id="RIVAL")
    assert a.got[0]["op"] == M.INVITE_ANS and a.got[0]["st"] == 1
    for _ in range(200):
        bot.pump()
        if a.got and a.got[-1]["op"] == M.BATTLE_END:
            break
        ans = a.ask(M.ROUND_READY)
        if ans["op"] == M.ROUND_START:
            a.ask(M.TURN, target=1, action=0, hit=100)
            bot.pump()
    assert a.got[-1]["op"] == M.BATTLE_END and len(bot.results) == 1
    assert bot.results[0]["win"] != a.got[-1]["win"]
    with pytest.raises(ValueError):
        Bot(server, "RIVAL", pwd="9999")                       # the ID is taken


# --- matchmaking (9.15) -------------------------------------------------------------------
class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


def _mm_server(clock):
    from pow_server.storage import MemoryStorage
    return GameServer(MemoryStorage(), rng=random.Random(3), clock=clock)


def _set_level(server, c, level):
    c.session.char.level = level


def test_two_players_in_the_queue_meet():
    clock = Clock()
    server = _mm_server(clock)
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    assert a.ask(M.MATCH, mode=0) is None                       # "Searching for opponent"
    assert server.queue == [a.session]
    clock.t += 20
    server.tick()
    assert a.got == []                                          # still waiting
    b.ask(M.MATCH, mode=0)
    ra = [m for m in a.got if m["op"] == M.MATCH_ANS][0]
    rb = [m for m in b.got if m["op"] == M.MATCH_ANS][0]
    assert ra["st"] == rb["st"] == 1 and ra["mode"] == rb["mode"] == 0
    assert (ra["slot"], rb["slot"]) == (0, 1) and ra["bg"] == rb["bg"]
    assert [m["op"] for m in a.got] == [513, 514, 1024] and [m["op"] for m in b.got] == [513, 514, 1024]
    assert a.session.room is b.session.room and server.queue == []
    turns, ea, eb = _play(a, b)
    assert ea["win"] != eb["win"]
    ca, cb = server.storage.load("ANDREY"), server.storage.load("BORYS")
    assert ca.wins + cb.wins == 1 and ca.losses + cb.losses == 1


def test_queue_waits_a_minute_then_a_cpu():
    clock = Clock()
    server = _mm_server(clock)
    a, _ = login(server, "ANDREY")
    a.ask(M.MATCH, mode=0)
    clock.t += 59
    server.tick()
    assert a.got == [] and a.session.room is None
    clock.t += 1
    server.tick()
    assert [m["op"] for m in a.got] == [513, 514, 1024] and a.session.room is not None
    assert server.queue == [] and a.session.room.players == {0: a.session}


def test_queue_matches_by_level_and_mode():
    clock = Clock()
    server = _mm_server(clock)
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    c, _ = login(server, "CHUCK")
    _set_level(server, a, 30)
    _set_level(server, b, 45)                                   # 15 levels apart
    _set_level(server, c, 31)
    a.ask(M.MATCH, mode=0)
    b.ask(M.MATCH, mode=0)
    assert server.queue == [a.session, b.session]               # too far for the first half
    c.ask(M.MATCH, mode=1)
    assert len(server.queue) == 3                               # 2:2 does not meet 1:1
    clock.t += 30                                               # half the wait: 20 levels
    d, _ = login(server, "DMITRO")
    _set_level(server, d, 46)
    d.ask(M.MATCH, mode=0)
    assert a.session.room is d.session.room is not None         # the oldest waiter first
    assert server.queue == [b.session, c.session]


def test_two_vs_two_from_the_queue_adds_cpu_allies():
    clock = Clock()
    server = _mm_server(clock)
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    a.ask(M.MATCH, mode=1)
    b.ask(M.MATCH, mode=1)
    room = a.session.room
    assert room is b.session.room and sorted(room.battle.fighters) == [0, 1, 2, 3]
    assert sorted(room.human_slots) == [0, 1]


def test_leaving_the_queue_and_busy_while_queued():
    clock = Clock()
    server = _mm_server(clock)
    a, _ = login(server, "ANDREY")
    b, _ = login(server, "BORYS")
    a.ask(M.MATCH, mode=0)
    assert b.ask(M.INVITE, mode=0, id="ANDREY")["st"] == -5     # searching: busy
    assert a.ask(M.MATCH, mode=0) == {"op": 513, "st": -11}     # one search at a time
    a.session.close()
    assert server.queue == []
    b.ask(M.MATCH, mode=0)
    assert b.session.room is None and server.queue == [b.session]


def test_mission_never_waits():
    server = _mm_server(Clock())
    a, _ = login(server, "ANDREY")
    a.ask(M.MATCH, mode=2)
    assert a.session.room is not None and server.queue == []


def test_hanging_up_after_the_last_blow_still_counts(server):
    c, _ = login(server)
    c.ask(M.MATCH, mode=0)
    c.ask(M.ROUND_READY)
    c.session.room.battle.fighters[0].hp = 0     # I fell in the last 1028 ...
    c.session.close()                            # ... and hang up before 1025 -> 1032
    assert server.storage.load("ANDREY").losses == 1


def test_the_quitter_counts_as_beaten(server):
    a, b = _pair(server, 0)
    a.ask(M.ROUND_READY)
    b.ask(M.ROUND_READY)
    b.session.close()
    end = a.ask(M.ROUND_READY)
    assert end["win"] == 1 and end["fame"] > 0 and end["exp"] > 0


def test_relogin_as_another_id_leaves_no_stale_online_entry(server):
    c, _ = login(server, "ANDREY")
    first = Client(server)
    tok = first.ask(M.LOGIN_FIRST, id="BORYS", pwd="5555", ver=M.GAME_VER)["token"]
    first.session.close()
    assert c.ask(M.LOGIN, id="BORYS", ver=M.GAME_VER, token=tok)["st"] == 1
    assert "ANDREY" not in server.online and server.online["BORYS"] is c.session


def test_no_invite_while_queued():
    server = _mm_server(Clock())
    a, _ = login(server, "ANDREY")
    login(server, "BORYS")
    a.ask(M.MATCH, mode=0)
    assert a.ask(M.INVITE, mode=0, id="BORYS")["st"] == -1
    assert a.session.room is None


# --- PORT-EXTRA: server bots (bots when nobody is online) -----------------------------------
def test_server_bots_can_be_challenged_alone(server):
    server.add_bots()
    server.add_bots()                                  # a restart finds the same accounts
    a, prof = login(server, "ANDREY")
    a.ask(M.INVITE, mode=0, id="BLADE")
    assert _ops(a)[:3] == [M.INVITE_ANS, M.ROOM_JOIN, M.ALL_READY] and a.got[0]["st"] == 1
    bot = a.got[1]
    assert bot["name"] == "Blade" and 30 <= bot["face"] <= 33
    assert abs(bot["level"] - prof["level"]) <= 2      # about my level
    for _ in range(80):
        ans = a.ask(M.ROUND_READY)
        if ans["op"] == M.BATTLE_END:
            break
        a.ask(M.TURN, target=1, action=0, hit=88)
    assert ans["op"] == M.BATTLE_END
    ch = server.storage.load("ANDREY")
    assert ch.wins + ch.losses == 1


def test_server_bot_as_an_ally_and_in_2v2(server):
    server.add_bots()
    a, _ = login(server, "ANDREY")
    a.ask(M.INVITE, mode=2, id="RAVEN")                # Invite An Ally to a mission
    assert a.got[0]["op"] == M.INVITE_ANS and a.got[0]["mode"] == 2
    joins = [m for m in a.got if m["op"] == M.ROOM_JOIN]
    assert any(m["name"] == "Raven" and m["slot"] == 2 for m in joins)
    assert a.got[-1]["op"] == M.STAGE_INFO
    a.session.close()
    a, _ = login(server, "ANDREY")
    a.ask(M.INVITE, mode=1, id="TIGER")                # Challenge 2:2
    joins = {m["slot"]: m["name"] for m in a.got if m["op"] == M.ROOM_JOIN}
    assert sorted(joins) == [1, 2, 3] and joins[1] == "Tiger"
    assert len(set(joins.values())) == 3


def test_server_bots_in_ranking_and_locked(server):
    server.add_bots()
    a, _ = login(server, "ANDREY")
    top = a.ask(M.RANK_LIST, code=11)["rows"]          # Top Rankers by Fame
    assert [r["id"] for r in top] == ["BLADE", "RAVEN", "TIGER"]
    c = Client(server)                                 # nobody can log in as a bot
    assert c.ask(M.LOGIN_FIRST, id="BLADE", pwd="0000", ver=M.GAME_VER)["st"] == -1


def test_server_bots_skip_a_players_id(server):
    login(server, "BLADE")                             # a player got there first
    server.add_bots()
    assert "BLADE" not in server.bots and "RAVEN" in server.bots
    assert not server.storage.load("BLADE").bot
