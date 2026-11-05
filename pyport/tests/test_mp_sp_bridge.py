"""The hero of the single player on the multiplayer screens: the login carries him from memory,
the server plays with him."""
import pytest

from pow.game.online import sp_bridge as S
from pow_server import codec_bin
from pow_server import messages as M
from pow_server.server import GameServer
from pow_server.storage import MemoryStorage


@pytest.fixture
def hero(monkeypatch):
    """A level-12 hero in memory: a weapon with +5 ATK, a helmet with +3 DEF +10 HP, Wind 3,
    Medium Heal 2, a fire skill 5; Wind and Medium Heal on the hotkeys; 3 mission bits."""
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import Hero, Item
    h = Hero()
    h.level, h.base_attack, h.base_defense, h.base_hp, h.base_mp = 12, 40, 30, 250, 90
    h.gold, h.fame, h.exp, h.head = 1000, 50, 7, 2
    h.equipped = [Item() for _ in range(9)]
    h.equipped[0].id, h.equipped[0].attack = 118, 5
    h.equipped[1].id, h.equipped[1].defense, h.equipped[1].hp = 131, 3, 10
    for idx, lvl in {0: 3, 3: 2, 11: 5}.items():
        h.skill_levels[idx] = lvl
    h.hotkeys = [12 + 0, 12 + 3, 0, 0, 0]
    monkeypatch.setattr(GameCanvas, "hero", h)
    monkeypatch.setattr(GameCanvas, "missions_done", 0b1011)
    return h


def test_hero_from_memory(hero):
    h = S.hero()
    assert (h["level"], h["hp"], h["mp"], h["atk"], h["def"]) == (12, 250, 90, 40, 30)
    assert (h["atk_bonus"], h["def_bonus"], h["hp_bonus"], h["mp_bonus"]) == (5, 3, 10, 0)
    assert h["face"] == 2 and h["weapon"] == 0 and h["progress"] == 3
    assert h["skills"] == [3, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]       # Wind (3), Medium Heal (9); 14+ unknown
    assert h["slots"] == [3, 9, 99, 99]
    hero.equipped[0].id = 103                                    # War Blade: short
    assert S.hero()["weapon"] == 1


def test_no_hero_no_fields(monkeypatch):
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import Hero
    monkeypatch.setattr(GameCanvas, "hero", Hero())
    assert S.hero() is None


def test_rewards_wait_for_the_single_player():
    S.pending.clear()
    S.keep_rewards(20, 3, 120)
    S.keep_rewards(0, 0, 50, (150, 7, 0, 0, 0))
    assert S.take_rewards() == [{"gold": 20, "fame": 3, "exp": 120, "loot": []},
                                {"gold": 0, "fame": 0, "exp": 50, "loot": [(150, 7, 0, 0, 0)]}]
    assert S.take_rewards() == []


def _login(server, extra):
    out = []
    sess = server.connect(lambda f: out.extend(codec_bin.decode(p, from_client=False)
                                               for p in codec_bin.unframe(f)[0]))
    sess.receive(codec_bin.unframe(codec_bin.encode(M.LOGIN_FIRST, {"id": "HERO", "pwd": "1234",
                                                                     "ver": M.GAME_VER}, to_client=False))[0][0])
    tok = out[-1]["token"]
    sess.close()
    out.clear()
    sess = server.connect(lambda f: out.extend(codec_bin.decode(p, from_client=False)
                                               for p in codec_bin.unframe(f)[0]))
    msg = dict({"id": "HERO", "ver": M.GAME_VER, "token": tok}, **extra)
    sess.receive(codec_bin.unframe(codec_bin.encode(M.LOGIN, msg, to_client=False))[0][0])
    return sess, out


def test_server_takes_the_hero_from_login(hero):
    server = GameServer(MemoryStorage())
    fields = S.hero()
    _sess, out = _login(server, dict({"sp": 1}, **{"sp_" + k: v for k, v in fields.items()}))
    prof = out[-1]
    assert prof["st"] == 1 and prof["level"] == 12 and prof["hp"] == 260 and prof["face"] == 2
    assert prof["slots"] == [3, 9, 99, 99]
    ch = server.storage.load("HERO")
    assert ch.sp_linked and ch.atk == 40 and ch.atk_bonus == 5 and ch.skills == {3: 3, 9: 2}
    assert ch.sp_progress == 3


def test_login_without_a_hero_keeps_the_default_hero():
    server = GameServer(MemoryStorage())
    _sess, out = _login(server, {"sp": 0})
    assert out[-1]["level"] == 1 and not server.storage.load("HERO").sp_linked


def test_slots_chosen_in_multiplayer_survive_the_next_login(hero):
    server = GameServer(MemoryStorage())
    extra = dict({"sp": 1}, **{"sp_" + k: v for k, v in S.hero().items()})
    sess, out = _login(server, extra)
    ch = server.storage.load("HERO")
    ch.slots = [9, 3, 99, 99]                       # 1291 from the Skills screen
    server.storage.save(ch)
    sess.close()
    sess, out = _login(server, extra)
    assert out[-1]["slots"] == [9, 3, 99, 99]
