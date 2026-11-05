"""The hero of the single player on the multiplayer screens: one game, one hero.

The login (262) carries the fields the server plays with (level, HP / MP / ATK / DEF, the item
bonuses, the face and the weapon, the skills and their slots, the mission progress) straight
from the hero in memory (hero()). What the battles earn (1032: gold, fame, exp, loot) waits
here (keep_rewards) for Live.after_multiplayer, which pays the hero when the screens are left.
"""

# single-player skill index -> skill code; the multiplayer knows the codes 3..13
SKILL_CODES = (3, 4, 5, 9, 10, 11, 12, 13, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21)
MP_SKILLS = tuple(range(3, 14))
EMPTY_SLOT = 99

pending = []                    # [{"gold", "fame", "exp", "loot": [(id, atk, def, hp, mp)]}]


def keep_rewards(gold, fame, exp, item=None):
    pending.append({"gold": gold, "fame": fame, "exp": exp, "loot": [item] if item else []})


def take_rewards():
    """What the battles earned since the last call (online_session.leave)."""
    out, pending[:] = list(pending), []
    return out


def weapon_type(item_id):
    """0 long, 1 short: 1 for the ids 101-115 (Blades / Pikes), else 0 (the starting sword
    below 100, Claymores / Swords / Axes 116-130)."""
    return 1 if 101 <= item_id <= 115 else 0


def hero():
    """The fields of the login the server uses, from the hero in memory; None without a hero."""
    from pow.game.game_canvas import GameCanvas
    h = GameCanvas.hero
    if h is None or h.level <= 0:
        return None
    worn = [it for it in h.equipped if it is not None and it.id != 0]
    bonus = [sum(getattr(it, k) for it in worn) for k in ("attack", "defense", "hp", "mp")]
    skills = [0] * len(MP_SKILLS)
    for idx, lvl in enumerate(h.skill_levels[:len(SKILL_CODES)]):
        code = SKILL_CODES[idx]
        if lvl > 0 and code in MP_SKILLS:
            skills[code - 3] = lvl
    slots = []
    for v in h.hotkeys:
        if v >= 12 and v - 12 < len(SKILL_CODES) and SKILL_CODES[v - 12] in MP_SKILLS and len(slots) < 4:
            slots.append(SKILL_CODES[v - 12])
    weapon = h.equipped[0].id if h.equipped and h.equipped[0] is not None else 0
    progress = bin(GameCanvas.missions_done & ((1 << 64) - 1)).count("1")
    return {
        "level": h.level, "hp": h.base_hp, "mp": h.base_mp, "atk": h.base_attack, "def": h.base_defense,
        "atk_bonus": bonus[0], "def_bonus": bonus[1], "hp_bonus": bonus[2], "mp_bonus": bonus[3],
        "face": h.head & 3, "weapon": weapon_type(weapon), "skills": skills,
        "slots": slots + [EMPTY_SLOT] * (4 - len(slots)), "progress": min(255, progress),
    }
