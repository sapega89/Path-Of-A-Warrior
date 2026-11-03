"""Loot of the multiplayer battles (PHASE_9 task 9.9): items of the single-player tables.

The original server chose the loot; only its name reached the MP client (1032 char[15], drawn
with "Loot!!!", g:5122-5124), and the item itself went to the single player through Gamevil
Live (Gift List 520 / Warehouse, analysis/03 §5.2). That server is lost, so the rates here are
made up. What is not: the items and their stats come from the single-player tables, and the
Special (301-437) and Rare (501-518) ones are what the single player cannot get offline except
by Combine (analysis/03 §1.2). Our client puts the item into the single-player backpack
(pow_mp/sp_bridge.add_item); 1032 carries it as PORT-EXTRA.
"""
import pathlib

import config

NORMAL_TIER_LEVEL = (1, 10, 25, 45, 70)   # ae.w: the 5 tiers of every kind of kibo.arr
STORY_ONLY = {502}                         # Silk Towel: the ending-2 reward, never a drop
_tables = None


class Item:
    __slots__ = ("atk", "def_", "hp", "id", "level", "mp", "name", "spread", "stat")

    def __init__(self, item_id, name, level, atk=0, def_=0, hp=0, mp=0, spread=0, stat=None):
        self.id, self.name, self.level = item_id, name, level
        self.atk, self.def_, self.hp, self.mp = atk, def_, hp, mp
        self.spread, self.stat = spread, stat

    def roll(self, rng):
        """The record z {id, atk, def, hp, mp} of one drop: a Normal item gets base + 0..spread
        on its stat like a drop in the single player (ag.k(id, 1))."""
        stats = [self.atk, self.def_, self.hp, self.mp]
        if self.stat is not None:
            stats[self.stat] += rng.randint(0, self.spread)
        return {"id": self.id, "name": self.name[:15], "atk": stats[0], "def": stats[1],
                "hp": stats[2], "mp": stats[3]}


def _read_arr(name):
    """d.java: u8 column count, the column widths, then fixed-size rows (little-endian)."""
    data = (pathlib.Path(config.RES_ROOT) / name).read_bytes()
    n = data[0]
    widths = list(data[1:1 + n])
    size = sum(widths)
    body = data[1 + n:]
    rows = []
    for r in range(len(body) // size):
        row, off = [], r * size
        for i, w in enumerate(widths):
            cell = body[off:off + w]
            row.append(cell.split(b"\0")[0].decode("latin-1").strip() if i == 0
                       else int.from_bytes(cell, "little"))
            off += w
        rows.append(row)
    return rows


def tables():
    """{"normal": [...], "special": [...], "rare": [...]} of Item."""
    global _tables
    if _tables is None:
        normal = []
        # kibo.arr: name, type, stat (0 ATK 1 DEF 2 HP 3 MP), base, spread, maxEnch, price, icon
        for r, (name, _, stat, base, spread, *_) in enumerate(_read_arr("kibo.arr")):
            stats = [0, 0, 0, 0]
            stats[stat] = base
            normal.append(Item(101 + r, name, NORMAL_TIER_LEVEL[r % 5], *stats, spread=spread, stat=stat))
        # sungbo.arr: name, type, atk, def, hp, mp, maxEnch, icon, reqLv
        special = [Item(301 + r, row[0], row[8], *row[2:6]) for r, row in enumerate(_read_arr("sungbo.arr"))]
        # shinki.arr: name, type, atk, def, hp, mp, price, reqLv
        rare = [Item(501 + r, row[0], row[7], *row[2:6]) for r, row in enumerate(_read_arr("shinki.arr"))
                if 501 + r not in STORY_ONLY]
        _tables = {"normal": normal, "special": special, "rare": rare}
    return _tables


CONSUMABLES = ("Red Potion (S)", "Red Potion (M)", "Red Potion (L)", "Blue Potion(S)",
               "Blue Potion(M)", "Blue Potion(L)", "H.M.Potion(S)", "H.M.Potion(M)",
               "H.M.Potion(M)", "Powerful Bomb", "Handy Dynamite")   # ae.aN, ids 1..11 (sic)

# ar.P(type) (ar.java:2055-2079): 0 soldier, 1 general, 2 boss
DROP_CHANCE = (5, 10, 20)          # % that something drops
EQUIP_CHANCE = (10, 30, 60)        # % of a drop that is equipment (else a consumable 1..11)
TIER_LEVELS = (69, 44, 24, 9, 0)   # hero level above -> the row of TIER_ODDS
TIER_ODDS = ((0, 0, 33, 77, 100), (5, 30, 55, 80, 100), (30, 60, 90, 100, 100),
             (40, 80, 100, 100, 100), (80, 100, 100, 100, 100))
# not in the single player (Special and Rare came only from Combine and Gamevil Live): the
# share of the equipment drops that is Special / Rare instead of Normal - made up
SPECIAL_SHARE, RARE_SHARE = 20, 2


def sp_drop(rng, level, kind):
    """The item id ar.P(kind) drops for a hero of `level`, or 0 (the gold bag of P() is left
    out: the battle pays gold anyway)."""
    if rng.randrange(100) >= DROP_CHANCE[kind]:
        return 0
    if rng.randrange(100) >= EQUIP_CHANCE[kind]:
        return rng.randrange(11) + 1
    row = next(i for i, lv in enumerate(TIER_LEVELS) if level > lv or lv == 0)
    if row == 0 and config.DROPS_AFTER_69:   # PORT-EXTRA: above Lv69 the odds of Lv45-69
        row = 1
    r = rng.randrange(100)
    tier = next(t for t, odds in enumerate(TIER_ODDS[row]) if r < odds)
    return 101 + tier + 5 * rng.randrange(20)


def _pick(rng, items, level, reach):
    """A Special / Rare item the hero can use soon: required level up to level + reach, the
    closest more often."""
    pool = [it for it in items if it.level <= level + reach] or [min(items, key=lambda it: it.level)]
    weights = [1 + max(0, 40 - abs(level - it.level)) for it in pool]
    return rng.choices(pool, weights)[0]


def item(rng, item_id):
    """1032 loot for an item id: {"id", "name", "atk", "def", "hp", "mp"}."""
    if item_id < 100:
        return {"id": item_id, "name": CONSUMABLES[item_id - 1], "atk": 0, "def": 0, "hp": 0, "mp": 0}
    t = tables()
    table = t["normal"] if item_id < 300 else t["special"] if item_id < 500 else t["rare"]
    return next(it for it in table if it.id == item_id).roll(rng)


def roll(rng, level, kills):
    """The loot of one battle: one ar.P() roll per foe beaten (kinds 0 soldier / 1 general /
    2 boss), the best item kept; equipment can come out Special or Rare. None = nothing."""
    best = 0
    for kind in kills:
        got = sp_drop(rng, level, kind)
        if got > 100:
            r = rng.randrange(100)
            if r < RARE_SHARE:
                got = _pick(rng, tables()["rare"], level, 25).id
            elif r < RARE_SHARE + SPECIAL_SHARE:
                got = _pick(rng, tables()["special"], level, 15).id
        best = max(best, got)
    return item(rng, best) if best else None
