"""PORT-EXTRA: the four heroes get their own base stats, and the attributes can be reset (respec).

In the original every hero starts with HP 30 / MP 10 / ATK 5 / DEF 4 (ag.aw, ag.java:3275-3284)
and the head (`Hero.head`, chosen on screen 6) is only a portrait. Here each head has its own
base stats. Every set is worth the same number of stat points as the original one (a point gives
HP +5 / MP +3 / ATK +1 / DEF +1, e.java:882-907), so no hero is stronger, only different.

Because of that, the points a hero has put into its stats (and the elixirs 434-437 it drank,
each worth one point) are always `spent_points()`, whatever head it has and even for a save made
before the heads differed. The reset puts the base stats back to the head's set and returns
those points as free ones (Management -> Attributes, left soft key RESET).

The multiplayer server keeps the same table (pow_server/sp_rules.HERO_BASES); a test checks
that the two stay equal.
"""

# HP, MP, ATK, DEF given by one stat point (e.java:882-907)
POINT_GAIN = (5, 3, 1, 1)

# (HP, MP, ATK, DEF) of a new hero per head; head 0 keeps the original numbers
BASE_STATS = (
    (30, 10, 5, 4),     # 0 blond: Warrior, balanced (the original hero)
    (40, 7, 3, 5),      # 1 helmet: Guardian, HP +2 pt, DEF +1 pt, MP -1 pt, ATK -2 pt
    (25, 16, 4, 4),     # 2 silver hair: Mystic, MP +2 pt, HP -1 pt, ATK -1 pt
    (25, 10, 7, 3),     # 3 red hair: Berserker, ATK +2 pt, HP -1 pt, DEF -1 pt
)
NAMES = ("Warrior", "Guardian", "Mystic", "Berserker")

# the price of a reset: gold per hero level, or one of these items from the backpack
RESPEC_GOLD_PER_LEVEL = 100
RESPEC_ITEMS = (434, 435, 436, 437)     # Rise Potion, Azure Potion, Falls Medicine, Forest Medicine


def base_stats(head):
    return BASE_STATS[head & 0x3]


def stats_line(head):
    hp, mp, atk, df = base_stats(head)
    return "HP%d MP%d ATK%d DEF%d" % (hp, mp, atk, df)


def spent_points(hero):
    """Stat points in the hero's base stats over its head's set (elixirs included)."""
    stats = (hero.base_hp, hero.base_mp, hero.base_attack, hero.base_defense)
    return max(0, sum((s - b) // g for s, b, g in zip(stats, base_stats(hero.head), POINT_GAIN, strict=True)))


def respec_gold(hero):
    return RESPEC_GOLD_PER_LEVEL * max(1, hero.level)


def respec_item_slot(hero):
    """Backpack index of the first item that pays for a reset, or -1."""
    for b, it in enumerate(hero.backpack):
        if it.id in RESPEC_ITEMS:
            return b
    return -1


def set_base_stats(hero):
    """The head's base stats, full HP / MP (what ag.aw did with the original numbers)."""
    hero.base_hp, hero.base_mp, hero.base_attack, hero.base_defense = base_stats(hero.head)
    hero.hp = hero.base_hp
    hero.mp = hero.base_mp


def respec(hero):
    """Base stats back to the head's set, the points become free ones. Returns the points."""
    n = spent_points(hero)
    set_base_stats(hero)
    hero.stat_points += n
    return n
