"""The multiplayer battles on the single player's numbers (pow_server/sp_rules.py)."""
import random

from pow_server import battle as B
from pow_server import sp_rules as R
from pow_server.model import default_character


def test_hero_and_level_table():
    assert R.hero_stats(1, {"atk": 2, "def": 1, "hp": 2}) == {"atk": 7, "def": 5, "hp": 40, "mp": 10}
    assert sum(R.hero_stats(20, {"atk": 1, "hp": 1}).values()) - sum(R.HERO_BASE.values()) > 0
    assert [R.exp_to_next(x) for x in (1, 10, 20, 41, 100)] == [50, 1040, 4080, 18245, 463400]


def test_soldiers_like_the_single_player():
    # c.java:1017-1039, analysis/02 §2.3: swordsman 4/0/10, archer 3/0/8, squad 6/0/10 at L1
    assert [tuple(R.soldier_stats(t, 1).values()) for t in range(3)] == [(4, 0, 10), (3, 0, 8), (6, 0, 10)]
    rng = random.Random(1)
    assert all(1 <= R.soldier_level(rng, 5) <= 7 for _ in range(200))


def test_skills_heals_souls():
    assert R.skill_bonus(B.WIND, 40, 2) == 4 and R.skill_bonus(B.TIDE, 60, 1) == 2
    assert R.heal(B.HEAL_MED, 100, 1) == 20 and R.heal(B.HEAL_MAX, 100, 1) == 50
    assert R.soul(B.SOUL_DEVIL, 40, 30, 1) == (2, 0, 50)
    assert R.soul(B.SOUL_GUARD, 40, 30, 8) == (0, 12, 150)
    assert R.soul(B.SOUL_ARCH, 50, 25, 5) == (10, 5, 100)


def test_damage_is_atk_minus_def_per_hit():
    rng = random.Random(3)
    a = B.Fighter(slot=0, name="A", level=1, max_hp=100, atk=20, def_=5, skills={}, slots=[])
    b = B.Fighter(slot=1, name="B", level=1, max_hp=100, atk=20, def_=8, skills={}, slots=[])
    bt = B.Battle(rng, [a, b])
    assert bt._strike(a, b, B.ATTACK, 100) == B.RES_HIT and b.hp == 100 - 12 * 3   # full combo
    bt._strike(a, b, B.ATTACK, 20)
    assert b.hp == 64 - 12                                                        # one hit
    b.def_ = 50
    bt._strike(a, b, B.ATTACK, 60)
    assert b.hp == 52 - 2                                                         # at least 1 a hit


def test_new_hero_and_level_up():
    ch = default_character("X")
    assert (ch.atk, ch.def_, ch.hp, ch.mp, ch.atk_bonus) == (7, 5, 40, 10, 1)
    assert ch.skills == {3: 1, 11: 1} and ch.slots[:2] == [3, 11]
    ch.mp_exp = 50 + 104 + 5
    B._level_up(ch)
    assert ch.level == 3 and ch.mp_exp == 5
    assert ch.atk + ch.def_ + (ch.hp - 40) // 5 == 7 + 5 + 6


def test_cpu_fighter_mirrors_my_hero_and_duels_stay_short():
    for lvl in (1, 10, 30, 60):
        ch = default_character("X")
        for _ in range(lvl - 1):
            B.level_up(ch)
        rng = random.Random(lvl)
        wins = rounds = 0
        for _ in range(60):
            me = B.from_character(ch, 0)
            foe = B.cpu_fighter(rng, me, 1)
            assert foe.skills == me.skills and abs(foe.level - lvl) <= 2
            bt = B.Battle(rng, [me, foe])
            while not bt.over:
                t, a, h = B.cpu_choice(rng, me, bt.foes(me))
                bt.resolve({0: (t, a, 100 if a == B.ATTACK else h)})
            wins += bt.winner() == 0
            rounds += bt.round
        assert wins >= 35 and rounds / 60 <= 12, (lvl, wins, rounds / 60)


def test_rewards_follow_the_single_player():
    rng = random.Random(1)
    ch = default_character("X")
    me = B.from_character(ch, 0)
    foe = B.cpu_fighter(rng, me, 1)
    bt = B.Battle(rng, [me, foe])
    foe.hp = 0
    bt.beaten.append(foe)
    res = B.duel_rewards(ch, bt, 0, rng)
    assert res["win"] == 1 and res["fame"] == 2 * foe.level and res["exp"] == 4 * foe.level
    assert res["gold"] in (0, 20)
    lost = default_character("Y")
    me2 = B.from_character(lost, 0)
    bt2 = B.Battle(rng, [me2, B.cpu_fighter(rng, me2, 1)])
    me2.hp = 0
    assert B.duel_rewards(lost, bt2, 0, rng)["exp"] == 0 and lost.losses == 1
    assert R.mission_end(100, True, 9) == (100, 210, 1350)
    assert R.mission_end(100, False, 9) == (100, 200, 1350)
