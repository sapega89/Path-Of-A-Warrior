"""PORT-EXTRA (proposal 22, "clans as lord houses"): the houses of the lords, from the game data.

Pure Python (no pygame), shared by the single player (pow/game/house.py) and the server
(pow_server/houses.py). Nothing here is new art or new text: every name comes from the data
files of the original game.

- ruler.arr (edat 55): the 22 lords, 15 bytes each from byte 3 (name[14], portrait).
- mission.arr (edat 48): the campaigns (38-byte records from byte 10: name[30] .. [36] first
  mission in sideinfo.arr, [37] mission count), as ag.C() / e.bi() read them.
- sideinfo.arr (edat 50): 11 bytes per mission from byte 11: [0] the lord the hero serves
  (an.a, the ruler id), [5] the general he fights (an.f, 1-based id in general.arr; 0 none,
  >= 200 the story missions without a duel).
- general.arr (edat 46): d.java table, column 0 the general's name.

A house is a lord the hero can serve in a mission with a duel against a general. The generals he
fights for that lord serve the lord's enemies: they are the house's foes. The loyalty of a house
is cz.ak[lord - 1] (n.java), which the campaign already raises by 5 per mission won for that
lord (c.java:1516-1527, capped at 100) and which picks the ending.
"""

RULER_COUNT = 22
LOYALTY_MAX = 100
LOYALTY_TO_SWEAR = 5          # the lord must know the hero: one mission won for him


def _cstr(data, start, n):
    end = start
    while end < start + n and end < len(data) and data[end] != 0:
        end += 1
    return bytes(data[start:end]).decode("latin-1")


def ruler_names(ruler):
    """ruler.arr -> {lord id: name}."""
    out = {}
    for rid in range(1, RULER_COUNT + 1):
        off = 3 + (rid - 1) * 15
        if off + 14 > len(ruler):
            break
        out[rid] = _cstr(ruler, off, 14)
    return out


def ruler_portraits(ruler):
    """ruler.arr -> {lord id: portrait frame} (byte 14 of the record, e.bi())."""
    return {rid: ruler[17 + (rid - 1) * 15] for rid in range(1, RULER_COUNT + 1)
            if 17 + (rid - 1) * 15 < len(ruler)}


def general_names(general):
    """general.arr (d.java: u8 column count, widths, rows) -> [name of id 1, name of id 2, ...]."""
    n = general[0]
    widths = list(general[1:1 + n])
    size = sum(widths)
    body = general[1 + n:]
    return [_cstr(body, r * size, widths[0]) for r in range(len(body) // size)]


def missions(mission, sideinfo):
    """-> [(campaign id, lord id, general id)] for every mission of every campaign."""
    out = []
    c = 1
    while 38 * c + 10 + 38 <= len(mission):
        rec = 38 * c + 10
        first, count = mission[rec + 36], mission[rec + 37]
        if 0 < count <= 10:
            for m in range(count):
                off = 11 * (first + m) + 11
                if off + 11 > len(sideinfo):
                    break
                out.append((c, sideinfo[off], sideinfo[off + 5]))
        c += 1
    return out


class House:
    def __init__(self, lord, name, foes, portrait=0):
        self.lord = lord            # ruler id 1..22 (cz.ak index + 1)
        self.name = name            # "Lord Gabriel"
        self.foes = foes            # general ids (1-based) the hero fights for this lord
        self.portrait = portrait

    def __repr__(self):
        return "House(%d, %r, %r)" % (self.lord, self.name, self.foes)


def build_houses(mission, sideinfo, ruler):
    """The houses in the order of their lord ids, each with its foes in the order met."""
    names = ruler_names(ruler)
    portraits = ruler_portraits(ruler)
    foes = {}
    for _c, lord, gen in missions(mission, sideinfo):
        if not 1 <= lord <= RULER_COUNT or not 1 <= gen < 200:
            continue
        lst = foes.setdefault(lord, [])
        if gen not in lst:
            lst.append(gen)
    return [House(lord, names.get(lord, "Lord %d" % lord), foes[lord], portraits.get(lord, 0))
            for lord in sorted(foes)]


def foe_bonus_percent(loyalty):
    """Extra damage, in percent, the hero deals to a foe of his house: 5 at the oath, 15 at
    loyalty 100."""
    loyalty = max(0, min(LOYALTY_MAX, loyalty))
    return 5 + loyalty // 10


def oath_break(loyalty):
    """Loyalty left to a lord the hero leaves for another house."""
    return max(0, loyalty) // 2
