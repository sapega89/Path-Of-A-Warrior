"""PORT-EXTRA (asked by Andrey, 05.11.2026): no Gamevil in what the player sees.

The original shows Gamevil's name, logo, site and "Gamevil Live" in its menus, help and
texts. With config.REBRAND (on by default, POW_REBRAND=0 = as in the original):
- "Gamevil Live" / "GAMEVIL LIVE" reads "Live" / "LIVE" everywhere it is shown (the Game Menu
  labels txt_b.png / txt_m.png too: pyport/assets/rebrand, read by pow/midp/resources.py);
- the strings that only advertise Gamevil (site, e-mail, copyright, credits) are replaced;
- the logos (gamevil.png "(c) 2008 GAMEVIL INC." under the title, gamevillogo.png of the
  Multiplayer) are not drawn.
This module and pow_mp/consts.py are the only code that still holds the publisher's name: the
original strings it looks for (with config.REBRAND = False the game shows them as they were).
Code names, save stores (pow/midp/rms.py RENAMED) and manifest keys (POW_*) lost the name.
"""
import config

# (string table, index) -> what is shown instead (.scr files of the single player)
SCR = {
    ("help.scr", 10): "Try combining different items at the Blacksmith to find new ones.",
    ("help.scr", 37): "|Path of a Warrior|Imperial Blood",
    ("help.scr", 38): "| ",
    ("text.scr", 62): "Developer Team",
    ("gamestr.scr", 17): "2Connect to\\the server?",
}

SERVICE = "Gamevil Live"   # the name of the original online service, as m.java draws it

_WORDS = (("accessing the Gamevil Live", "going to Live"), ("GAMEVIL LIVE", "LIVE"),
          ("Gamevil Live", "Live"))


def enabled():
    return config.REBRAND


def text(s):
    """A shown string without "Gamevil Live" (any table, any screen)."""
    if not enabled() or not s:
        return s
    for old, new in _WORDS:
        s = s.replace(old, new)
    return s


def scr(path, index, s):
    """ScrTable.get(): the replacement of one entry of a .scr string table."""
    if not enabled() or s is None:
        return s
    name = path.rsplit("/", 1)[-1]
    return text(SCR.get((name, index), s))


# Multiplayer help pages: the last page of a topic sent the player to www.gamevil.com
_VISIT = ["Please visit", "www.gamevil.com", "for more", "information about"]
_VISIT_NEW = ["Have fun and", "good luck in", "your battles!", ""]


def mp_lines(lines):
    """pow_mp/consts.py text arrays: the same number of lines (pages keep their line counts)."""
    if not enabled():
        return lines
    out = list(lines)
    i = 0
    while i <= len(out) - len(_VISIT):
        if out[i:i + len(_VISIT)] == _VISIT:
            out[i:i + len(_VISIT) + 1] = _VISIT_NEW + [""]
            i += len(_VISIT) + 1
        else:
            i += 1
    out = ["" if ("gamevil.com" in x.lower()) else text(x) for x in out]
    return out
