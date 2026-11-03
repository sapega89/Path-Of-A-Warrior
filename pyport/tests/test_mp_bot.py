"""The battle bot (pow_server/battle.py cpu_choice): CPU fighters and players on auto-battle."""
import random

from pow_server import battle as B
from pow_server.model import default_character


class FixedRng(random.Random):
    """random.Random whose timing bar always stops at `bar`."""

    def __init__(self, bar=100, seed=0):
        super().__init__(seed)
        self.bar = bar

    def choice(self, seq):
        return self.bar if seq is B.BAR_CHOICES else super().choice(seq)


def fighter(slot, hp=100, atk=30, def_=10, mp=0, skills=None, max_mp=40, **kw):
    skills = dict(skills or {})
    return B.Fighter(slot=slot, name="F%d" % slot, level=10, max_hp=100, atk=atk, def_=def_,
                     skills=skills, slots=list(skills), max_mp=max_mp, hp=hp, mp=mp, **kw)


def test_finishes_off_with_the_cheapest_killing_action():
    rng = FixedRng(100)
    me = fighter(0, mp=100, skills={B.WIND: 1, B.THUNDER: 1})
    foe = fighter(1, hp=40)                       # a full combo does (30 - 10) * 3 = 60
    assert B.cpu_choice(rng, me, [foe]) == (1, B.ATTACK, 100)
    foe.hp = 70                                   # only a skill kills: Wind 63 no, Thunder 76
    t, a, _ = B.cpu_choice(rng, me, [foe])
    assert (t, a) == (1, B.THUNDER)


def test_kills_the_foe_it_can_rather_than_the_weakest_looking():
    rng = FixedRng(100)
    me = fighter(0, mp=10)                        # I act first
    tank = fighter(1, hp=30, def_=25)             # 15 a combo: does not fall
    soft = fighter(3, hp=50)                      # 60 a combo: falls
    assert B.cpu_choice(rng, me, [tank, soft])[:2] == (3, B.ATTACK)


def test_defends_when_a_lethal_hit_comes_first():
    rng = FixedRng(100)
    me = fighter(0, hp=50, mp=0)                  # the foe acts first (more MP) and hits 60
    foe = fighter(1, hp=100, mp=50)
    assert B.cpu_choice(rng, me, [foe])[1] == B.DEFEND
    me.hp = 20                                    # even Defend (24) does not save me: Evade
    assert B.cpu_choice(rng, me, [foe])[1] == B.EVADE
    foe.skills, foe.slots = {B.THUNDER: 1}, [B.THUNDER]     # Thunder ignores Evade
    assert B.cpu_choice(rng, me, [foe])[1] == B.DEFEND


def test_attacks_first_when_it_kills_before_the_lethal_hit():
    rng = FixedRng(100)
    me = fighter(0, hp=50, mp=60)                 # I act first and my combo kills
    foe = fighter(1, hp=60, mp=10)
    assert B.cpu_choice(rng, me, [foe])[1] == B.ATTACK


def test_no_stance_twice_in_a_row():
    rng = FixedRng(100)
    me = fighter(0, hp=50, mp=0, last_action=B.DEFEND)
    foe = fighter(1, hp=100, mp=50)
    assert B.cpu_choice(rng, me, [foe])[1] not in (B.DEFEND, B.EVADE)


def test_heals_when_hp_is_below_the_damage_coming():
    rng = FixedRng(100)
    me = fighter(0, hp=50, mp=100, skills={B.HEAL_MED: 1, B.HEAL_MAX: 1}, max_mp=100)
    foe = fighter(1, hp=100, mp=0)                # I act first; the foe hits 60
    t, a, _ = B.cpu_choice(rng, me, [foe])
    assert t == 0 and a == B.HEAL_MED             # +20 is enough: the cheaper heal
    me.hp = 30
    assert B.cpu_choice(rng, me, [foe])[1] == B.HEAL_MAX
    foe.atk = 20                                  # 30 a round against my 90: no heal
    me.hp = 90
    assert B.cpu_choice(rng, me, [foe])[1] not in B.HEALS


def test_no_heal_when_winning_the_race_or_after_the_limit():
    rng = FixedRng(100)
    me = fighter(0, hp=50, mp=100, skills={B.HEAL_MED: 1}, max_mp=100)
    foe = fighter(1, hp=100, atk=40, mp=0)       # 90 a round: heal
    assert B.cpu_choice(rng, me, [foe])[1] == B.HEAL_MED
    me.heals = B.HEAL_LIMIT
    assert B.cpu_choice(rng, me, [foe])[1] != B.HEAL_MED
    me.heals = 0
    foe.atk = 25                                  # 45 a round, my 60 finish it in 2: hit on
    foe.hp = 61
    assert B.cpu_choice(rng, me, [foe])[1] == B.ATTACK


def test_heals_an_ally_in_danger():
    rng = FixedRng(100)
    me = fighter(0, mp=100, skills={B.HEAL_MAX: 1}, max_mp=100)
    ally = fighter(2, hp=25)
    foe = fighter(1, hp=100, mp=0)
    assert B.cpu_choice(rng, me, [foe], [me, ally])[:2] == (2, B.HEAL_MAX)


def test_skill_only_when_it_beats_attack_and_keeps_heal_mp():
    rng = FixedRng(100)
    foe = fighter(1, hp=200, def_=12)
    me = fighter(0, mp=100, skills={B.STORM: 1, B.THUNDER: 1})
    # Storm 57 < Thunder 76 against an Attack of 54: Thunder, the most damage a MP
    assert B.cpu_choice(rng, me, [foe])[1] == B.THUNDER
    me.skills, me.slots = {B.STORM: 1}, [B.STORM]
    foe.def_ = 10                                 # Storm 63 vs Attack 60: still worth it
    assert B.cpu_choice(rng, me, [foe])[1] == B.STORM
    me.atk = 10                                   # 1 a hit either way: Attack keeps the MP
    assert B.cpu_choice(rng, me, [foe])[1] == B.ATTACK
    me.atk = 30
    me.skills = {B.STORM: 1, B.HEAL_MAX: 1}
    me.slots = [B.STORM, B.HEAL_MAX]
    foe.atk = 20                                  # 30 a round: no heal needed yet
    me.hp, me.mp = 90, 100
    assert B.cpu_choice(rng, me, [foe])[1] == B.STORM
    foe.atk = 18                                  # 24 a round: no heal yet, but HP is low
    me.hp = 55                                    # the MP is kept for the heal
    me.mp = me.cost(B.HEAL_MAX) + me.cost(B.STORM) - 1
    assert B.cpu_choice(rng, me, [foe])[1] == B.ATTACK


def test_a_useless_soul_is_not_cast():
    rng = FixedRng(100)
    me = fighter(0, mp=100, skills={B.SOUL_DEVIL: 1})   # +1 ATK for one round
    foe = fighter(1, hp=300)
    assert B.cpu_choice(rng, me, [foe])[1] == B.ATTACK
    me.skills = {B.SOUL_DEVIL: 9}                        # +13 ATK for three rounds
    assert B.cpu_choice(rng, me, [foe])[1] == B.SOUL_DEVIL
    foe.hp = 50                                          # the fight is over next round
    assert B.cpu_choice(rng, me, [foe])[1] == B.ATTACK


def test_auto_battle_plays_for_the_player():
    rng = random.Random(5)
    me = fighter(0, hp=100, auto=True)
    foe = fighter(1, hp=40, cpu=True)
    bt = B.Battle(rng, [me, foe])
    turn = bt.resolve({})                         # no 1027 needed: no Defend by default
    assert turn["actions"][0] == B.ATTACK and turn["records"]
    me.auto = False
    me2 = fighter(0, hp=100)
    bt = B.Battle(rng, [me2, fighter(1, hp=40, cpu=True)])
    assert bt.resolve({0: (1, B.AUTO, 0)})["actions"][0] == B.ATTACK


def random_bot(rng, me, foes):
    """The bot before: random skills and stances."""
    target = min(foes, key=lambda f: f.hp).slot
    usable = [s for s in me.slots if me.can_use(s) and s not in B.HEALS]
    if usable and rng.random() < 0.6:
        return target, rng.choice(usable), 0
    r = rng.random()
    return target, B.ATTACK if r < 0.7 else B.DEFEND if r < 0.88 else B.EVADE, rng.choice(B.BAR_CHOICES)


def test_the_bot_beats_random_play_and_bot_duels_end():
    for lvl in (1, 10, 30, 60):
        ch = default_character("X")
        for _ in range(lvl - 1):
            B.level_up(ch)
        ch.skills = {B.WIND: 2, B.STORM: 1, B.THUNDER: 1, B.HEAL_MED: 1, B.SOUL_DEVIL: 1}
        ch.slots = list(ch.skills)
        rng = random.Random(lvl)
        wins = {"bot": 0, "random": 0}
        for side in wins:
            for _ in range(150):
                me = B.from_character(ch, 0)
                foe = B.cpu_fighter(rng, me, 1)
                foe.cpu = False                   # the foe plays the random bot
                bt = B.Battle(rng, [me, foe])
                while not bt.over and bt.round < 100:
                    mine = (B.cpu_choice(rng, me, bt.foes(me)) if side == "bot"
                            else random_bot(rng, me, bt.foes(me)))
                    bt.resolve({0: mine, 1: random_bot(rng, foe, bt.foes(foe))})
                assert bt.over
                wins[side] += bt.winner() == 0
        assert wins["bot"] > wins["random"] + 10, (lvl, wins)
        rounds = []
        for _ in range(60):                       # bot against bot: no endless stances
            me = B.from_character(ch, 0)
            me.auto = True
            bt = B.Battle(rng, [me, B.cpu_fighter(rng, me, 1)])
            while not bt.over and bt.round < 60:
                bt.resolve({})
            assert bt.over
            rounds.append(bt.round)
        assert sum(rounds) / len(rounds) <= 15, (lvl, rounds)


def test_a_one_off_skill_does_not_count_as_winning_the_race():
    rng = FixedRng(100)
    # Thunder kills in ~1 round but empties the gauge; on Attack the foe outlasts me: heal
    me = fighter(0, hp=60, atk=60, mp=60, skills={B.THUNDER: 9, B.HEAL_MED: 1}, max_mp=100)
    foe = fighter(1, hp=250, def_=55, atk=20, mp=0)   # Thunder 128, Attack 15; it hits 30
    assert B.cpu_choice(rng, me, [foe])[1] == B.HEAL_MED
