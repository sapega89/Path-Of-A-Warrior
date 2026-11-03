"""Battles on the server (PHASE_9 tasks 9.5-9.7): 1-on-1 Duel against a CPU fighter.

The client only shows what the server decides (06 §3.3): it sends one 1027 {target, action,
hit%} per round and plays the records of 1028 back. Everything here - turn order, damage,
evasion, MP, skill effects, the CPU, rewards - was computed by the lost Gamevil server, so
the numbers come from the single-player game where it has them (pow_server/sp_rules.py: hero
stats, soldiers, damage ATK - DEF, skills, heals, souls, rewards); the rest is ours and says
so. Pure Python, the random source is passed in so that tests are repeatable.

Slots (06 §2.6): slot % 2 is the team (0 left, 1 right), slot // 2 the row; 1v1 uses 0 and 1.
Actions: 0 Attack, 1 Defend, 2 Evade, 3..13 skills (l.eK). Defend and Evade are stances: they
never produce a record of their own, a record with action 1 would hang the client (06 §2.5).
"""
import dataclasses

from pow_server import sp_rules as R

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
SKILL_HIT = 70                           # skills skip the timing bar (aS = 0)
# Attack = the single player's 3-hit combo (the 3rd hit knocks back, ar.java:505-506); the bar
# decides how many of the three land (made up: the single player has no timing bar)
COMBO_HITS = ((88, 3), (52, 2), (0, 1))

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
    monster: bool = False                 # face 10 in 514: spr_mon, attacks only
    wins: int = 0
    losses: int = 0
    quote_start: str = ""
    quote_win: str = ""
    hp: int = 0
    mp: int = 0
    stance: int = ATTACK
    buffs: dict = dataclasses.field(default_factory=dict)   # "atk"/"def" -> [bonus, turns]
    general: bool = False                 # worth 2L when beaten, a soldier L (ar.java:1663-1698)
    build: dict = None                    # where the hero's stat points went (CPU fighters copy it)
    max_mp: int = 10                      # the hero's MP in the single player (skill costs)
    keep_name: bool = False               # a server bot (server.py): its name is its UserID

    def __post_init__(self):
        self.hp = self.hp or self.max_hp

    @property
    def team(self):
        return self.slot % 2

    @property
    def alive(self):
        return self.hp > 0

    def bonus(self, stat):
        b = self.buffs.get(stat)
        return b[0] if b else 0

    def cost(self, skill):
        """Gauge cost of a skill: its single-player MP share of this hero's MP (sp_rules)."""
        return R.skill_cost(skill, self.skills.get(skill, 1), self.max_mp)

    def can_use(self, skill):
        return skill in self.slots and skill in self.skills and self.mp >= self.cost(skill)

    def wire(self):
        """514 body (06 §2.4): a CPU fighter is sent as face + 30 (g:2197-2206)."""
        return {
            "slot": self.slot, "name": self.name[:8], "level": self.level, "wins": self.wins,
            "losses": self.losses, "hp": self.max_hp, "weapon": self.weapon,
            "face": MONSTER_FACE if self.monster else self.face + (30 if self.cpu else 0),
            "quote_start": self.quote_start,
            "quote_win": self.quote_win, "cr": 0, "alt_name": self.name[:8],
        }


def from_character(ch, slot):
    return Fighter(slot=slot, name=ch.name or ch.user_id[:8], level=ch.level,
                   max_hp=ch.max_hp(), atk=ch.atk + ch.atk_bonus, def_=ch.def_ + ch.def_bonus,
                   skills=dict(ch.skills), slots=[s for s in ch.slots if s in ch.skills],
                   face=ch.face, weapon=ch.weapon, wins=ch.wins, losses=ch.losses,
                   quote_start=ch.quote_start, quote_win=ch.quote_win,
                   build=hero_build(ch), general=True,     # a hero beaten counts like a general
                   max_mp=ch.max_mp())


def hero_build(ch):
    """The stat points of a hero: its base stats over a new hero's (ag.aw), per point gain."""
    b = R.HERO_BASE
    return {"atk": max(0, ch.atk - b["atk"]), "def": max(0, ch.def_ - b["def"]),
            "hp": max(0, (ch.hp - b["hp"]) // R.POINT_GAIN["hp"]),
            "mp": max(0, (ch.mp - b["mp"]) // R.POINT_GAIN["mp"])}


BUILDS = ({"atk": 2, "def": 1, "hp": 2}, {"atk": 3, "def": 1, "hp": 1},
          {"atk": 1, "def": 2, "hp": 2}, {"atk": 2, "def": 2, "hp": 1})


def cpu_fighter(rng, me, slot, ally=False):
    """A CPU fighter: a single-player hero of about my level, its points spent like mine, in the
    shop's kit of its level - like a hero of this server without a single-player save. A hero
    from the single player brings its own gear. The original: within 20 levels, decided by
    the server."""
    level = max(1, me.level + rng.randint(-2, 1) - (1 if ally else 0))
    # the points go about where mine went: with damage = ATK - DEF (at least 1) a random build
    # can out-DEF the other side's ATK and the duel never ends
    build = dict(me.build) if me.build and sum(me.build.values()) else dict(rng.choice(BUILDS))
    stat = rng.choice(("atk", "def", "hp"))
    build[stat] = build.get(stat, 0) + max(1, sum(build.values()) // 10)
    st = R.hero_stats(level, build)
    # the skills are mine too (a new hero knows Wind Slasher and Devil Soul, ag.java new game;
    # more and higher levels come only from Visiting in the single player)
    skills = dict(me.skills) or {WIND: 1, SOUL_DEVIL: 1}
    slots = [x for x in me.slots if x in skills] or list(skills)[:4]
    q = rng.choice(CPU_QUOTES)
    kit = R.shop_kit(level)
    return Fighter(slot=slot, name=rng.choice(CPU_NAMES), level=level, max_hp=st["hp"] + kit["hp"],
                   atk=st["atk"] + kit["atk"], def_=st["def"] + kit["def"],
                   skills=skills, slots=slots, face=rng.randrange(4),
                   weapon=rng.randrange(2), cpu=True, wins=rng.randrange(5 * level + 1),
                   losses=rng.randrange(5 * level + 1), quote_start=q[0], quote_win=q[1],
                   general=True, build=build, max_mp=st["mp"])


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
        self.beaten = []                   # fighters knocked out, in order (rewards)

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

    def new_wave(self, foes, rest=0.35):
        """Mission: the next stage's foes replace team 1; my team keeps its MP and buffs and
        gets back `rest` of its max HP (the living ones; the client shows the HP of the first
        record of the next round, 06 §3.3)."""
        self.fighters = {s: f for s, f in self.fighters.items() if f.team == 0}
        for f in self.fighters.values():
            if f.alive:
                f.hp = min(f.max_hp, f.hp + int(f.max_hp * rest))
        for f in foes:
            self.fighters[f.slot] = f

    def finish(self, max_rounds=60):
        """Let the CPU fighters play the rest (the human side has no one left to choose)."""
        while not self.over and max_rounds > 0:
            self.resolve({})
            max_rounds -= 1

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
            f.mp -= f.cost(action)
        if action in HEALS:
            t.hp = min(t.max_hp, t.hp + R.heal(action, t.max_hp, f.skills.get(action, 1)))
            if action == HEAL_MAX:
                f.mp = min(MP_MAX, f.mp + 20)
        elif action in SOULS:
            a, d, ticks = R.soul(action, f.atk, f.def_, f.skills.get(action, 1))
            turns = ticks // 50 + 1                       # 50 ticks ~ one round (made up)
            for ally in self.fighters.values():           # the aura covers the team (06 §3.3)
                if ally.alive and ally.team == f.team:
                    if a:
                        ally.buffs["atk"] = [a, turns]
                    if d:
                        ally.buffs["def"] = [d, turns]
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
        """Damage of one action, one number for all its hits; returns targetRes. One hit is
        ATK + A - DEF - B, at least 1 (ar.java:293-316); a skill adds ATK*lvl/aU to every hit."""
        if t.stance == EVADE and action != THUNDER and self.rng.random() < EVADE_CHANCE:
            return RES_EVADED
        atk = f.atk + f.bonus("atk")
        one = atk - t.def_ - t.bonus("def")
        if action == ATTACK:
            hits = next(n for bar, n in COMBO_HITS if hit >= bar)
        else:
            one += R.skill_bonus(action, f.atk, f.skills.get(action, 1))
            hits = R.SKILL_HITS[action]
        dmg = max(1, one) * hits
        if t.stance == DEFEND:
            dmg = max(1, int(dmg * DEFEND_FACTOR))
        t.hp = max(0, t.hp - dmg)
        t.mp = min(MP_MAX, t.mp + MP_HIT)
        if not t.alive:
            self.beaten.append(t)
        return RES_HIT


# --- rewards (1032) -------------------------------------------------------------
GRADE_TOP = 9                            # l.eL: D+ .. A+


# where a hero without a single-player save puts its 3 points a level (the multiplayer client has
# no screen for it): 14 ATK, 4 DEF, 12 HP in every 30 points. With damage ATK - DEF and the
# shop's DEF-heavy kit, a hero that grows ATK and DEF alike hits its like for 1-3 and a duel
# lasts 30 rounds; this keeps it at 6-9 (made up, tools: the balance runs in the tests)
POINT_ORDER = "ADHAHAHADHAHAHAADHAHAHADHAHAHA"


def _level_up(ch):
    """A hero without a single-player save levels up here by exp.arr, +3 points a level
    (POINT_ORDER); an imported hero levels up in the single player, which gets the exp
    (pow_mp/sp_bridge)."""
    while not ch.sp_linked and ch.mp_exp >= R.exp_to_next(ch.level):
        ch.mp_exp -= R.exp_to_next(ch.level)
        level_up(ch)


def level_up(ch):
    """One level of a hero without a single-player save: 3 points, and the shop's kit of the
    new level (sp_rules.shop_kit)."""
    ch.level += 1
    kit = R.shop_kit(ch.level)
    ch.atk_bonus, ch.def_bonus, ch.hp_bonus = kit["atk"], kit["def"], kit["hp"]
    for k in range(R.POINTS_PER_LEVEL):
        stat = POINT_ORDER[((ch.level - 2) * R.POINTS_PER_LEVEL + k) % len(POINT_ORDER)]
        if stat == "A":
            ch.atk += R.POINT_GAIN["atk"]
        elif stat == "D":
            ch.def_ += R.POINT_GAIN["def"]
        else:
            ch.hp += R.POINT_GAIN["hp"]


def _pay(ch, gold, fame, exp):
    ch.gold += gold
    ch.mp_fame += fame
    ch.mp_exp += exp
    _level_up(ch)


def _dy(battle, team):
    """dY of the foes `team` beat: L for a soldier, 2L for a general (ar.java:1663-1698)."""
    return sum(R.kill_value(f.level, f.general) for f in battle.beaten if f.team != team)


def duel_rewards(ch, battle, my_slot, rng):
    """Apply the result of a finished duel (1v1 or 2v2) to the character; returns the 1032
    fields (rank is filled in by the caller). A fighter beaten counts as a general killed in
    the single player: Fame dY, EXP 2 dY (c.java:1616-1641), and the gold bag of a kill
    without a drop, 20 gold at 25 % (ar.java:2075-2077). A loss pays nothing, like a death
    in the single player."""
    me = battle.fighters[my_slot]
    win = battle.winner() == me.team
    if win:
        dy = _dy(battle, me.team)
        fame, exp = dy, 2 * dy
        gold = sum(20 for f in battle.beaten if f.team != me.team and rng.random() < 0.25)
        # grades are the multiplayer's own (l.eL D+..A+): HP left and a quick win (made up)
        grade = min(GRADE_TOP, me.hp * 10 // me.max_hp + (2 if battle.round <= 5 else 0))
        ch.wins += 1
        ch.duel_grade = min(GRADE_TOP, ch.duel_grade + 1)
    else:
        grade = gold = fame = exp = 0
        ch.losses += 1
        ch.duel_grade = max(0, ch.duel_grade - 1)
    _pay(ch, gold, fame, exp)
    return {"win": 1 if win else 0, "gold": gold, "grade": grade, "fame": fame, "exp": exp,
            "loot": "NONE"}


# --- missions (512 mode 2, Solo Mission) -----------------------------------------
# Lost with the server: titles, waves, monsters, rewards. The client only knows one monster
# sprite (spr_mon, face 10 in 514) that can attack but has no skill animations (06 §2.4).
MISSION_TITLES = ("Dark Forest", "Old Ruins", "Bandit Pass", "Cursed Swamp", "Iron Keep",
                  "Bone Valley", "Frozen Gate", "Lost Temple")
MONSTER_NAMES = ("Goblin", "Ghoul", "Orc", "Troll", "Imp", "Wraith", "Ogre", "Lizard")
MONSTER_FACE = 10


def mission_stages(progress):
    """Stages of a Solo Mission: "the number of stages ... will vary depending on POW Single
    Player mission progress" (l.eD): 2 without a single-player save, up to 6."""
    return 2 + min(4, progress // 6)


SOLDIER_KINDS = (0, 0, 1, 2)           # swordsmen more often than archers and squads


def monster(rng, me, slot, stage, stages):
    """A monster is a single-player soldier (c.java:1017-1039): its level around mine."""
    level = R.soldier_level(rng, me.level)
    st = R.soldier_stats(rng.choice(SOLDIER_KINDS), level)
    return Fighter(slot=slot, name=rng.choice(MONSTER_NAMES), level=level, max_hp=st["hp"],
                   atk=st["atk"], def_=st["def"], skills={}, slots=[], face=0, weapon=0,
                   cpu=True, monster=True)


def mission_wave(rng, me, stage, stages):
    """The foes of one stage at slots 1 and 3: soldiers; the last stage has a CPU fighter, the
    mission's boss."""
    foes = [monster(rng, me, 1, stage, stages), monster(rng, me, 3, stage, stages)]
    if stage == stages:
        foes[0] = cpu_fighter(rng, me, 1)
    return foes


def mission_gold_rate(stages):
    """h of sideinfo.arr (3..15) for 2..6 stages."""
    return 3 * (stages - 1)


def mission_rewards(ch, battle, my_slot, rng, cleared, stages):
    """1032 for a mission (bz 2): no wins/losses (g:2313). Accomplished: the single player's
    mission end (c.java:1603, 1616-1641), Fame dY, EXP 2 (dY + dY/20 in time), gold h * 150.
    Failed: nothing, like "Mission fail!" in the single player."""
    me = battle.fighters[my_slot]
    win = cleared == stages
    if win:
        dy = _dy(battle, me.team)
        fame, exp, gold = R.mission_end(dy, battle.round <= 6 * stages, mission_gold_rate(stages))
        # grade: the multiplayer's own (made up): stages and HP left
        grade = min(GRADE_TOP, 3 + stages // 2 + me.hp * 4 // max(1, me.max_hp))
        ch.mission_grade = max(ch.mission_grade, grade)
    else:
        grade = gold = fame = exp = 0
    _pay(ch, gold, fame, exp)
    return {"win": 1 if win else 0, "gold": gold, "grade": grade, "fame": fame, "exp": exp,
            "loot": "NONE"}
