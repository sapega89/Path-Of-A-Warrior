"""Numbers of the single-player game the multiplayer battles use (Andrey: "the balance from the
offline game"). Sources: analysis/02 §2.3-2.9 and 03 §2; the lines of the Java are given at
every rule. What the single player does not have (the timing bar, Defend / Evade, the MP gauge
of the multiplayer client, grades) stays in battle.py and is marked there as made up.
"""
import pathlib

import config

# --- the hero ----------------------------------------------------------------------------
# ag.aw() (ag.java:3275-3284): a new hero; 5 free points, +3 per level (e.java:2877-2878);
# a point gives HP +5 / MP +3 / ATK +1 / DEF +1 (e.java:882-907)
HERO_BASE = {"atk": 5, "def": 4, "hp": 30, "mp": 10}
POINTS_START, POINTS_PER_LEVEL = 5, 3
POINT_GAIN = {"atk": 1, "def": 1, "hp": 5, "mp": 3}


def hero_stats(level, build):
    """ATK / DEF / HP / MP of a hero of `level` whose points went by `build` {stat: share}."""
    points = POINTS_START + POINTS_PER_LEVEL * (level - 1)
    total = sum(build.values())
    out = dict(HERO_BASE)
    given = 0
    for i, (stat, share) in enumerate(build.items()):
        n = points - given if i == len(build) - 1 else points * share // total
        out[stat] += n * POINT_GAIN[stat]
        given += n
    return out


_exp = None


def exp_to_next(level):
    """exp.arr (e.java:3547-3560): EXP from level L to L+1; u16 then 199 u32."""
    global _exp
    if _exp is None:
        data = (pathlib.Path(config.RES_ROOT) / "exp.arr").read_bytes()
        _exp = [int.from_bytes(data[2 + 4 * i:6 + 4 * i], "little") for i in range(199)]
    return _exp[min(max(level, 1), 199) - 1]


# --- foes --------------------------------------------------------------------------------
# soldiers, c.a(int,int) (c.java:1017-1039): t 0 swordsman, 1 archer, 2 squad
SOLDIER_BASE = (3, 2, 3)
SOLDIER_MULT = (100, 100, 150)
SOLDIER_HP = (7, 5, 7)


def soldier_level(rng, lp):
    if lp < 21:
        return max(1, lp + rng.randint(0, 4) - 2)
    if lp < 41:
        return lp + rng.randint(0, 8) - 3
    return lp + rng.randint(0, 15) - 5


def soldier_stats(t, level):
    return {"atk": (SOLDIER_BASE[t] + level) * SOLDIER_MULT[t] // 100, "def": level - 1,
            "hp": SOLDIER_HP[t] + 3 * level}


# --- skills --------------------------------------------------------------------------------
# multiplayer code -> single-player skill index (as.gG, as.java:84-86)
SP_INDEX = {3: 0, 4: 1, 5: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 7, 6: 8, 7: 9, 8: 10}
# ar.e(int) (ar.java:743-756): MP a skill takes in the single player, base + (level - 1) * inc,
# indexed by the single-player skill id - 12
SKILL_MP_BASE = (5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 10, 5, 6, 7, 9, 12, 20, 20, 20)
SKILL_MP_INC = (3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 5, 3, 4, 5, 5, 6, 5, 5, 5)


def skill_mp(skill, level):
    """MP of a multiplayer skill (3..13) at `level` in the single player."""
    i = SP_INDEX[skill]
    return SKILL_MP_BASE[i] + (max(1, level) - 1) * SKILL_MP_INC[i]


def skill_cost(skill, level, max_mp):
    """The cost on the multiplayer's 0..100 MP gauge: the share of the hero's MP the skill takes
    in the single player (Wind Slasher Lv1 = 5 MP of a new hero's 10 -> 50). The original
    server sent these in 263 (cI) and they are lost; above the hero's MP -> a full gauge."""
    return max(1, min(100, -(-100 * skill_mp(skill, level) // max(1, max_mp))))


# ae.aU (ae.java:246-248): an attack skill adds ATK * level / aU to every hit (ar.java:301-316)
AU = (20, 20, 20, 0, 0, 0, 0, 0, 30, 25, 20)
# hit frames of the player's skill animations (c.java:1920-2126): Wind f3-5, Storm f5-7,
# Thunder f2,4,6,8, Tide the odd frames of 12, Wave f5, Tidal f6
SKILL_HITS = {3: 3, 4: 3, 5: 4, 6: 6, 7: 1, 8: 1}


def skill_bonus(skill, atk, level):
    au = AU[SP_INDEX[skill]]
    return atk * level // au if au else 0


def heal(skill, max_hp, level):
    """Medium Heal maxHP * (4 + lvl) / 25, Maximum Heal maxHP * (9 + lvl) / 20 (02 §2.5)."""
    return max_hp * (4 + level) // 25 if skill == 9 else max_hp * (9 + level) // 20


def soul(skill, atk, def_, level):
    """(ATK bonus, DEF bonus, ticks): Devil Soul A = max(1, ATK*lvl/20), Guardian Soul
    B = max(1, DEF*lvl/20), Arch angel Soul A = ATK*lvl/25, B = DEF*lvl/25; 50/100/150 ticks
    for lvl < 4 / < 8 / more (02 §2.5)."""
    ticks = 50 if level < 4 else 100 if level < 8 else 150
    if skill == 11:
        return max(1, atk * level // 20), 0, ticks
    if skill == 12:
        return 0, max(1, def_ * level // 20), ticks
    return atk * level // 25, def_ * level // 25, ticks


# --- rewards -------------------------------------------------------------------------------
# ar.ab() (ar.java:1663-1698): dY += L for a soldier, 2L for a general; at the end of a mission
# (c.java:1603, 1616-1641) Fame += dY, EXP = (dY + bonus) * 2 (Normal), bonus = dY / 20 in time,
# gold = h * 150 with h the mission's gold multiplier (sideinfo.arr, 3..15)


def kill_value(level, general):
    return 2 * level if general else level


def mission_end(dy, in_time, h):
    """(fame, exp, gold) of a mission accomplished on Normal."""
    return dy, (dy + (dy // 20 if in_time else 0)) * 2, h * 150


# --- gear of a hero without a single-player save --------------------------------------------
# kibo.arr types: 0 / 1 weapons (ATK), 2 helmet, 3 armour (DEF), 4 gauntlets, 5 boots, 6 belt (HP)
KIT = ((0, 0), (2, 1), (3, 1), (4, 2), (5, 2), (6, 2))   # (type, stat) one item each


def shop_kit(level):
    """{"atk", "def", "hp"} of the best Normal items of each kind that a hero of `level` can buy
    (the Blacksmith's tiers 10/25/45/70, base stat): what a hero of this server without a
    single-player save, and a CPU fighter, wears."""
    from pow_server import loot
    if level < loot.NORMAL_TIER_LEVEL[1]:
        # a new hero starts with 0 gold and the Iron Claymore (116, base ATK 1, ag.java new
        # game); the kit counts from the second tier on
        return {"atk": 1, "def": 0, "hp": 0}
    tier = sum(1 for lv in loot.NORMAL_TIER_LEVEL if level >= lv) - 1
    rows = loot._read_arr("kibo.arr")
    out = {"atk": 0, "def": 0, "hp": 0}
    for typ, stat in KIT:
        best = max((row[3] for r, row in enumerate(rows)
                    if r % 5 == tier and row[1] == typ and row[2] == stat), default=0)
        out[("atk", "def", "hp")[stat]] += best
    return out
