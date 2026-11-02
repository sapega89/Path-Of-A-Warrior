"""Battles on the server (PHASE_9 tasks 9.5-9.7): 1-on-1 Duel against a CPU fighter.

The client only shows what the server decides (06 §3.3): it sends one 1027 {target, action,
hit%} per round and plays the records of 1028 back. Everything here - turn order, damage,
evasion, MP, skill effects, the CPU, rewards - was computed by the lost Gamevil server, so
the numbers are ours (06 §6.1 "Доведеться вигадати"). Pure Python, the random source is
passed in so that tests are repeatable.

Slots (06 §2.6): slot % 2 is the team (0 left, 1 right), slot // 2 the row; 1v1 uses 0 and 1.
Actions: 0 Attack, 1 Defend, 2 Evade, 3..13 skills (l.eK). Defend and Evade are stances: they
never produce a record of their own, a record with action 1 would hang the client (06 §2.5).
"""
import dataclasses

from pow_server.model import SKILL_COST

ATTACK, DEFEND, EVADE = 0, 1, 2
WIND, STORM, THUNDER, TIDE, WAVE, TIDAL = 3, 4, 5, 6, 7, 8
HEAL_MED, HEAL_MAX, SOUL_DEVIL, SOUL_GUARD, SOUL_ARCH = 9, 10, 11, 12, 13
ENEMY_SKILLS = (WIND, STORM, THUNDER, TIDE, WAVE, TIDAL)
HEALS = (HEAL_MED, HEAL_MAX)
SOULS = (SOUL_DEVIL, SOUL_GUARD, SOUL_ARCH)

RES_HIT, RES_EVADED = 1, 2               # targetRes in 1028
MP_MAX = 100
MP_ATTACK, MP_HIT, MP_STANCE = 20, 10, 15
EVADE_CHANCE = 0.45
DEFEND_FACTOR = 0.4
SKILL_HIT = 70                           # skills skip the timing bar (aS = 0): a fixed "good" hit
BUFF_TURNS = 3
# damage multiplier of the attack skills: 3 / 6 strikes are drawn, one number is shown (06 §3.4)
SKILL_POWER = {WIND: 1.6, STORM: 1.3, THUNDER: 1.3, TIDE: 2.4, WAVE: 1.2, TIDAL: 1.2}

CPU_NAMES = ("Garrick", "Selene", "Borin", "Kaida", "Ulric", "Mirena", "Dorn", "Ysolde",
             "Thane", "Rowan", "Brakka", "Liora")
CPU_QUOTES = (("En garde!", "Too slow."), ("Face me!", "As expected."),
              ("Show me your blade", "Train harder."), ("Here I come!", "Victory is mine!"))


@dataclasses.dataclass
class Fighter:
    slot: int
    name: str
    level: int
    max_hp: int
    atk: int
    def_: int
    skills: dict                          # skill id -> level
    slots: list                           # skills the fighter can use (263 bE / 1291)
    face: int = 0
    weapon: int = 0
    cpu: bool = False
    wins: int = 0
    losses: int = 0
    quote_start: str = ""
    quote_win: str = ""
    hp: int = 0
    mp: int = 0
    stance: int = ATTACK
    buffs: dict = dataclasses.field(default_factory=dict)   # "atk"/"def" -> [factor, turns]

    def __post_init__(self):
        self.hp = self.hp or self.max_hp

    @property
    def team(self):
        return self.slot % 2

    @property
    def alive(self):
        return self.hp > 0

    def factor(self, stat):
        b = self.buffs.get(stat)
        return 1.0 + (b[0] if b else 0.0)

    def can_use(self, skill):
        return skill in self.slots and skill in self.skills and self.mp >= SKILL_COST[skill]

    def wire(self):
        """514 body (06 §2.4): a CPU fighter is sent as face + 30 (g:2197-2206)."""
        return {
            "slot": self.slot, "name": self.name[:8], "level": self.level, "wins": self.wins,
            "losses": self.losses, "hp": self.max_hp, "weapon": self.weapon,
            "face": self.face + (30 if self.cpu else 0), "quote_start": self.quote_start,
            "quote_win": self.quote_win, "cr": 0, "alt_name": self.name[:8],
        }


def from_character(ch, slot):
    return Fighter(slot=slot, name=ch.name or ch.user_id[:8], level=ch.level,
                   max_hp=ch.max_hp(), atk=ch.atk + ch.atk_bonus, def_=ch.def_ + ch.def_bonus,
                   skills=dict(ch.skills), slots=[s for s in ch.slots if s in ch.skills],
                   face=ch.face, weapon=ch.weapon, wins=ch.wins, losses=ch.losses,
                   quote_start=ch.quote_start, quote_win=ch.quote_win)


def cpu_fighter(rng, level, slot):
    """A CPU opponent within 2 levels of the player (the original: ±20, decided by the server)."""
    level = max(1, level + rng.randint(-2, 1))
    pool = [WIND, STORM, THUNDER, HEAL_MED, TIDE, SOUL_DEVIL, WAVE, SOUL_GUARD, HEAL_MAX]
    n = min(len(pool), 1 + level // 3)
    skills = {s: max(1, level // 4) for s in pool[:n]}
    q = rng.choice(CPU_QUOTES)
    return Fighter(slot=slot, name=rng.choice(CPU_NAMES), level=level,
                   max_hp=100 + 12 * level, atk=10 + 2 * level, def_=8 + 2 * level,
                   skills=skills, slots=list(skills)[:4], face=rng.randrange(4),
                   weapon=rng.randrange(2), cpu=True, wins=rng.randrange(5 * level + 1),
                   losses=rng.randrange(5 * level + 1), quote_start=q[0], quote_win=q[1])


def cpu_choice(rng, me, foes):
    """(target slot, action, hit%) for a CPU fighter."""
    target = min(foes, key=lambda f: f.hp).slot
    if me.hp * 100 < me.max_hp * 35:
        for s in (HEAL_MAX, HEAL_MED):
            if me.can_use(s):
                return me.slot, s, 0
    usable = [s for s in me.slots if me.can_use(s) and s not in HEALS]
    if usable and rng.random() < 0.6:
        return target, rng.choice(usable), 0
    r = rng.random()
    action = ATTACK if r < 0.7 else DEFEND if r < 0.88 else EVADE
    return target, action, rng.choice((40, 52, 64, 76, 76, 88, 88, 100))


def battle_background(rng):
    """Room byte `by` (06 §3.3): bits 6-7 sky, 4-5 ground 0..3, 0-1 foreground 0..3.
    Sky is always 0 (day): the night branch of W() measures dj[6], which only the day branch
    loads, so sky 1 is a NullPointerException in the original client too (g:5560-5575)."""
    return (rng.randrange(4) << 4) | rng.randrange(4)


class Battle:
    def __init__(self, rng, fighters, mode=0):
        self.rng = rng
        self.mode = mode
        self.fighters = {f.slot: f for f in fighters}
        self.round = 0
        self.bg = battle_background(rng)

    # --- state --------------------------------------------------------------
    def team_alive(self, team):
        return any(f.alive and f.team == team for f in self.fighters.values())

    @property
    def over(self):
        return not (self.team_alive(0) and self.team_alive(1))

    def winner(self):
        """The team still standing (None while both stand or none does)."""
        alive = [t for t in (0, 1) if self.team_alive(t)]
        return alive[0] if len(alive) == 1 else None

    def foes(self, f):
        return [g for g in self.fighters.values() if g.alive and g.team != f.team]

    # --- one round ------------------------------------------------------------
    def resolve(self, choices):
        """choices: slot -> (target, action, hit%) for the human fighters; the CPU picks for
        itself. Returns the 1028 message fields."""
        self.round += 1
        plan = {}
        for f in self.fighters.values():
            if not f.alive:
                continue
            if f.cpu:
                plan[f.slot] = cpu_choice(self.rng, f, self.foes(f))
            else:
                plan[f.slot] = self._validate(f, choices.get(f.slot, (f.slot, DEFEND, 20)))
        for slot, (_, action, _) in plan.items():
            self.fighters[slot].stance = action
        actions = [plan[s][1] if s in plan else 0 for s in range(4)]
        # higher MP acts first (06 §2.5); ties are random
        order = sorted(plan, key=lambda s: (-self.fighters[s].mp, self.rng.random()))
        records = []
        for slot in order:
            f = self.fighters[slot]
            target, action, hit = plan[slot]
            if not f.alive or self.over:
                continue
            if action in (DEFEND, EVADE):
                f.mp = min(MP_MAX, f.mp + MP_STANCE)
                continue
            rec = self._act(f, target, action, hit)
            if rec:
                records.append(rec)
        for f in self.fighters.values():
            for b in list(f.buffs.values()):
                b[1] -= 1
            f.buffs = {k: b for k, b in f.buffs.items() if b[1] > 0}
            f.stance = ATTACK
        return {"actions": actions, "records": records}

    def _validate(self, f, choice):
        target, action, hit = choice
        hit = max(0, min(100, hit))
        if action in (DEFEND, EVADE, ATTACK):
            return target, action, hit
        if not f.can_use(action):          # not learned, not in a slot or not enough MP
            return target, ATTACK, 20
        return target, action, SKILL_HIT

    def _target(self, f, target, action):
        if action in HEALS:
            t = self.fighters.get(target)
            return t if t and t.alive and t.team == f.team else f
        if action in SOULS:
            return f
        t = self.fighters.get(target)
        if t and t.alive and t.team != f.team:
            return t
        foes = self.foes(f)
        return min(foes, key=lambda g: g.hp) if foes else None

    def _act(self, f, target, action, hit):
        t = self._target(f, target, action)
        if t is None:
            return None
        rec = {"actor": f.slot, "action": action, "target": t.slot, "result": RES_HIT,
               "has2nd": 0, "flags": 0}
        if action >= WIND:
            f.mp -= SKILL_COST[action]
        if action in HEALS:
            lvl = f.skills.get(action, 1)
            amount = t.max_hp * ((4 if action == HEAL_MED else 8) + lvl) // 25
            t.hp = min(t.max_hp, t.hp + amount)
            if action == HEAL_MAX:
                f.mp = min(MP_MAX, f.mp + 20)
        elif action in SOULS:
            lvl = f.skills.get(action, 1)
            boost = 0.2 + 0.02 * lvl
            stats = {SOUL_DEVIL: ("atk",), SOUL_GUARD: ("def",), SOUL_ARCH: ("atk", "def")}[action]
            for ally in self.fighters.values():           # the aura covers the team (06 §3.3)
                if ally.alive and ally.team == f.team:
                    for st in stats:
                        ally.buffs[st] = [boost if action != SOUL_ARCH else boost * 0.75,
                                          BUFF_TURNS + 1]
        else:
            rec["result"] = self._strike(f, t, action, hit)
            f.mp = min(MP_MAX, f.mp + (MP_ATTACK if action == ATTACK else 0))
            if action == TIDAL:
                others = [g for g in self.foes(f) if g is not t]
                if others:
                    t2 = others[0]
                    res2 = self._strike(f, t2, action, hit)
                    rec.update(has2nd=1, target2=t2.slot, result2=res2, target2_hp=t2.hp,
                               target2_mp=t2.mp)
        rec.update(actor_hp=f.hp, actor_mp=f.mp, target_hp=t.hp, target_mp=t.mp)
        if t is f:
            rec.update(target_hp=f.hp, target_mp=f.mp)
        return rec

    def _strike(self, f, t, action, hit):
        """Damage of one blow (one number, even for 3 / 6 strikes); returns targetRes."""
        if t.stance == EVADE and action != THUNDER and self.rng.random() < EVADE_CHANCE:
            return RES_EVADED
        atk = f.atk * f.factor("atk")
        dfn = 0 if action == STORM else t.def_ * t.factor("def")
        power = SKILL_POWER.get(action, 1.0)
        dmg = atk * (0.5 + hit / 100.0) * 1.3 * power * self.rng.uniform(0.9, 1.1) - dfn * 0.5
        if t.stance == DEFEND and action != STORM:
            dmg *= DEFEND_FACTOR
        dmg = max(1, int(round(dmg)))
        t.hp = max(0, t.hp - dmg)
        t.mp = min(MP_MAX, t.mp + MP_HIT)
        if action == WAVE:
            t.buffs["atk"] = [-0.2, BUFF_TURNS + 1]
        return RES_HIT


# --- rewards (1032) -------------------------------------------------------------
GRADE_TOP = 9                            # l.eL: D+ .. A+


def duel_rewards(ch, battle, my_slot, rng):
    """Apply the result of a finished duel to the character; returns the 1032 fields
    (rank is filled in by the caller, it needs the whole table)."""
    me = battle.fighters[my_slot]
    foe = next(f for f in battle.fighters.values() if f.team != me.team)
    win = battle.winner() == me.team
    if win:
        grade = min(GRADE_TOP, me.hp * 10 // me.max_hp + (2 if battle.round <= 5 else 0))
        gold = 40 + 10 * foe.level + rng.randrange(20)
        exp, fame = 20 + 5 * foe.level, 10 + foe.level
        ch.wins += 1
        ch.duel_grade = min(GRADE_TOP, ch.duel_grade + 1)
    else:
        grade = 0
        gold, exp, fame = 0, 5 + foe.level, -min(5, ch.mp_fame)
        ch.losses += 1
        ch.duel_grade = max(0, ch.duel_grade - 1)
    ch.gold += gold
    ch.mp_fame += fame
    ch.mp_exp += exp
    while ch.mp_exp >= ch.level * 100:                 # level up: placeholders like the rest
        ch.mp_exp -= ch.level * 100
        ch.level += 1
        ch.hp += 10
        ch.atk += 2
        ch.def_ += 2
    return {"win": 1 if win else 0, "gold": gold, "grade": grade, "fame": fame, "exp": exp,
            "loot": "NONE"}
