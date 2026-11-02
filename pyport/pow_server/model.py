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

# MP cost of skills 3..13 on the 0..100 MP scale, sent in 263 (cI). Server-side and lost
# with the original server: placeholders until the turn resolver is balanced (task 9.6).
SKILL_COST = {3: 30, 4: 40, 5: 40, 6: 60, 7: 40, 8: 60, 9: 40, 10: 70, 11: 50, 12: 50, 13: 80}

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
    hp: int = 100
    hp_bonus: int = 0
    mp: int = 50
    mp_bonus: int = 0
    atk: int = 10
    atk_bonus: int = 0
    def_: int = 10
    def_bonus: int = 0
    skills: dict = dataclasses.field(default_factory=lambda: {3: 1})   # skill id -> level
    slots: list = dataclasses.field(default_factory=lambda: [3, 99, 99, 99])
    quote_start: str = "Prepare yourself!"
    quote_win: str = "Too easy."
    mp_exp: int = 0
    mp_fame: int = 0
    gold: int = 0                      # "Gold In Server"
    duel_grade: int = 0
    mission_grade: int = 0
    invitation: int = 1                # Options -> Invitation: 0 Deny, 1 Accept (288/290)
    notices_seen: int = 0              # version of the notices last shown to this player

    # --- what goes on the wire -------------------------------------------------
    def max_hp(self):
        return self.hp + self.hp_bonus

    def profile(self, notices=0):
        """263 body."""
        return {
            "name": self.name or self.user_id[:8], "face": self.face, "level": self.level,
            "wins": self.wins, "losses": self.losses, "hp": self.max_hp(),
            "weapon": self.weapon, "slots": list(self.slots),
            "quote_start": self.quote_start, "quote_win": self.quote_win,
            "skill_cost": [SKILL_COST[i] for i in SKILL_IDS], "notices": notices,
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


def default_character(user_id):
    return Character(user_id=user_id)


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
