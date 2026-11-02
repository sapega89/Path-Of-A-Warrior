"""The multiplayer character as the server keeps it (PHASE_9 tasks 9.3, 9.14).

What the client sees of it: 263 (profile), 514 (fighter in a room), 1288 (attributes),
1290 (skills), 1297 (records), 1299 (exp / fame / gold). Atk and Def never reach the battle
screen, only 1288 (06 §4).

Until task 9.10 (import from the single-player save) a new account gets default_character():
a level-1 hero with the first skill learned. These numbers are placeholders, not the original.
"""
import dataclasses

from pow_server import messages as M

SKILL_IDS = tuple(range(3, 14))        # MP skill codes 3..13 = SP as.gG (06 §3.1)


# Grade index 0..9 = l.eL {"D+", "C-", ..., "A+"}
GRADES = ("D+", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+")


@dataclasses.dataclass
class Character:
    user_id: str
    name: str = ""                     # display name, 8 chars max (1280)
    face: int = 0                      # hero 0..3 (SP aB)
    weapon: int = 0                    # 0 long / 1 short -> sprwp1/2, sprsword1/2
    level: int = 1
    wins: int = 0
    losses: int = 0
    hp: int = 40                       # a new single-player hero (ag.aw) with its 5
    hp_bonus: int = 0
    mp: int = 10                       # free points in ATK 2 / DEF 1 / HP 2
    mp_bonus: int = 0
    atk: int = 7
    atk_bonus: int = 0
    def_: int = 5
    def_bonus: int = 0
    skills: dict = dataclasses.field(default_factory=lambda: {3: 1, 11: 1})   # Wind, Devil Soul (ag.java new game)
    slots: list = dataclasses.field(default_factory=lambda: [3, 11, 99, 99])
    quote_start: str = "Prepare yourself!"
    quote_win: str = "Too easy."
    mp_exp: int = 0
    mp_fame: int = 0
    gold: int = 0                      # "Gold In Server"
    duel_grade: int = 0
    mission_grade: int = 0
    invitation: int = 1                # Options -> Invitation: 0 Deny, 1 Accept (288/290)
    notices_seen: int = 0              # version of the notices last shown to this player
    sp_linked: bool = False            # the hero comes from the single-player save (9.10)
    sp_progress: int = 0               # single-player missions done (dy bits), for missions later

    # --- what goes on the wire -------------------------------------------------
    def max_hp(self):
        return self.hp + self.hp_bonus

    def max_mp(self):
        return self.mp + self.mp_bonus

    def skill_cost(self, skill):
        """0..100 gauge cost from the single player's MP rule (sp_rules.skill_cost)."""
        from pow_server import sp_rules
        return sp_rules.skill_cost(skill, self.skills.get(skill, 1), self.max_mp())

    def profile(self, notices=0):
        """263 body."""
        return {
            "name": self.name or self.user_id[:8], "face": self.face, "level": self.level,
            "wins": self.wins, "losses": self.losses, "hp": self.max_hp(),
            "weapon": self.weapon, "slots": list(self.slots),
            "quote_start": self.quote_start, "quote_win": self.quote_win,
            "skill_cost": [self.skill_cost(i) for i in SKILL_IDS], "notices": notices,
        }

    def fighter(self, slot):
        """514 body: this character entering a room at slot 0..3."""
        return {
            "slot": slot, "name": self.name or self.user_id[:8], "level": self.level,
            "wins": self.wins, "losses": self.losses, "hp": self.max_hp(),
            "weapon": self.weapon, "face": self.face,
            "quote_start": self.quote_start, "quote_win": self.quote_win,
        }

    def attributes(self):
        """1288 body."""
        return {"hp": self.hp, "hp_bonus": self.hp_bonus, "mp": self.mp, "mp_bonus": self.mp_bonus,
                "atk": self.atk, "atk_bonus": self.atk_bonus, "def": self.def_, "def_bonus": self.def_bonus}

    def skill_list(self):
        """1290 body (at most 11 rows, 06 §2.4)."""
        return {"skills": [{"id": i, "level": self.skills[i]} for i in SKILL_IDS if i in self.skills]}

    def to_json(self):
        d = dataclasses.asdict(self)
        d["skills"] = {str(k): v for k, v in self.skills.items()}
        return d

    @classmethod
    def from_json(cls, d):
        d = dict(d)
        d["skills"] = {int(k): v for k, v in d.get("skills", {}).items()}
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


def apply_sp_hero(ch, msg):
    """262 PORT-EXTRA: the hero of the single-player save replaces the SP-side fields, like the
    original "Save User Data" (opcode 256) did. MP-only data (name, quotes, wins, exp, fame,
    gold, grades) stays. Returns False when the message carries no usable hero."""
    if msg.get("sp") != 1 or msg.get("_short") or not 1 <= msg.get("sp_level", 0) <= 255:
        return False
    if msg.get("sp_hp", 0) <= 0:
        return False
    ch.level = msg["sp_level"]
    ch.hp, ch.mp = msg["sp_hp"], msg["sp_mp"]
    ch.atk, ch.def_ = msg["sp_atk"], msg["sp_def"]
    ch.hp_bonus, ch.mp_bonus = msg["sp_hp_bonus"], msg["sp_mp_bonus"]
    ch.atk_bonus, ch.def_bonus = msg["sp_atk_bonus"], msg["sp_def_bonus"]
    ch.face, ch.weapon = msg["sp_face"] & 3, msg["sp_weapon"] & 1
    first = not ch.sp_linked
    ch.skills = {i + 3: lvl for i, lvl in enumerate(msg["sp_skills"]) if lvl > 0}
    kept = [s for s in ch.slots if s in ch.skills]      # slots set in the MP menu (1291) stay
    sp_slots = valid_slots(ch, list(msg["sp_slots"]))
    if first and sp_slots is not None:                  # the first import takes the SP ones
        kept = [s for s in sp_slots if s != M.EMPTY_SKILL]
    ch.slots = (kept + [M.EMPTY_SKILL] * 4)[:4]
    ch.sp_progress = msg["sp_progress"]
    ch.sp_linked = True
    return True


def default_character(user_id):
    """A new hero (ag.aw, 5 points in ATK 2 / DEF 1 / HP 2) wearing the shop's level-1 kit."""
    from pow_server.sp_rules import shop_kit
    kit = shop_kit(1)
    return Character(user_id=user_id, atk_bonus=kit["atk"], def_bonus=kit["def"], hp_bonus=kit["hp"])


def valid_slots(ch, slots):
    """1291: four ids, learned skills first, the rest 99; no duplicates (g:1655-1671)."""
    if len(slots) != 4:
        return None
    out, seen = [], set()
    for s in slots:
        if s == M.EMPTY_SKILL:
            continue
        if s not in ch.skills or s in seen:
            return None
        seen.add(s)
        out.append(s)
    return out + [M.EMPTY_SKILL] * (4 - len(out))
