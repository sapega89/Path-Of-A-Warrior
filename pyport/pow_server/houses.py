"""PORT-EXTRA (proposal 22, "clans as lord houses"), the server side: the houses' members and
their war bands.

A clan is the house of one of the game's lords (pow/house_data.py). The hero swears allegiance
in the single player (Management > House, pow/game/house.py); the multiplayer client sends that
oath and the loyalty with every login (the SP_HOUSE tail of 262, read from the same save as the
hero), and the server keeps the roll of every house. Players of one house can form a war band
(up to BAND_MAX players) for the co-op missions and the bosses; a band never mixes houses.

Kept in the storage's "live" documents ("houses"), so the standalone server keeps it in SQLite
and the in-game one in memory:
    {"members": {uid: {"house": lord, "loyalty": n, "name": str, "band": id or 0}},
     "bands": {"id": {"house": lord, "leader": uid, "members": [uid, ...]}}, "next": id}
"""
import pathlib

import config
from pow import house_data

BAND_MAX = 4              # the multiplayer rooms hold up to 4 fighters (2-on-2, missions)
DOC = "houses"

_houses = None


def houses():
    """[house_data.House] of the game data (the server reads the same files as the game)."""
    global _houses
    if _houses is None:
        root = pathlib.Path(config.RES_ROOT)
        try:
            _houses = house_data.build_houses((root / "mission.arr").read_bytes(),
                                              (root / "sideinfo.arr").read_bytes(),
                                              (root / "ruler.arr").read_bytes())
        except OSError:
            _houses = []
    return _houses


def house_of(lord):
    for h in houses():
        if h.lord == lord:
            return h
    return None


class HouseError(Exception):
    """A refused request; .code is the status the client gets."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


NO_HOUSE = -2             # the player swore to no lord
NO_BAND = -3              # no such band / not in a band
BAND_FULL = -4
OTHER_HOUSE = -5          # the band serves another lord
IN_BAND = -6              # already in a band


class HouseHall:
    def __init__(self, storage):
        self.storage = storage

    # --- the document ------------------------------------------------------------------
    def _load(self):
        d = self.storage.live_get(DOC)
        if d is None:
            d = {"members": {}, "bands": {}, "next": 1}
        return d

    def _save(self, d):
        self.storage.live_put(DOC, d)

    # --- oath (from the single-player save) ------------------------------------------------
    def set_oath(self, uid, lord, loyalty, name=""):
        """The oath the client sent at login. lord 0 (or not a house) = no house. A change of
        house leaves the old band."""
        d = self._load()
        m = d["members"].get(uid)
        if house_of(lord) is None:
            if m is not None:
                self._leave_band(d, uid)
                del d["members"][uid]
                self._save(d)
            return
        loyalty = max(0, min(house_data.LOYALTY_MAX, int(loyalty)))
        if m is None:
            m = d["members"][uid] = {"house": lord, "loyalty": loyalty, "name": name, "band": 0}
        elif m["house"] != lord:
            self._leave_band(d, uid)
            m["house"] = lord
        m["loyalty"] = loyalty
        if name:
            m["name"] = name
        self._save(d)

    def rename(self, uid, name):
        d = self._load()
        if uid in d["members"]:
            d["members"][uid]["name"] = name
            self._save(d)

    def member(self, uid):
        return self._load()["members"].get(uid)

    # --- what the houses look like -----------------------------------------------------
    def summary(self):
        """[(lord, members, total loyalty)] of every house, in lord order."""
        d = self._load()
        out = []
        for h in houses():
            ms = [m for m in d["members"].values() if m["house"] == h.lord]
            out.append((h.lord, len(ms), sum(m["loyalty"] for m in ms)))
        return out

    def roster(self, lord):
        """[(uid, name, loyalty, band)] of a house, the most loyal first."""
        d = self._load()
        rows = [(uid, m["name"] or uid[:8], m["loyalty"], m["band"])
                for uid, m in d["members"].items() if m["house"] == lord]
        rows.sort(key=lambda r: (-r[2], r[1]))
        return rows

    def bands(self, lord):
        """[(band id, leader uid, [member uids])] of a house."""
        d = self._load()
        return [(int(bid), b["leader"], list(b["members"]))
                for bid, b in sorted(d["bands"].items(), key=lambda kv: int(kv[0]))
                if b["house"] == lord]

    # --- war bands -----------------------------------------------------------------------
    def _member(self, d, uid):
        m = d["members"].get(uid)
        if m is None:
            raise HouseError(NO_HOUSE)
        return m

    def create_band(self, uid):
        d = self._load()
        m = self._member(d, uid)
        if m["band"]:
            raise HouseError(IN_BAND)
        bid = d["next"]
        d["next"] = bid + 1
        d["bands"][str(bid)] = {"house": m["house"], "leader": uid, "members": [uid]}
        m["band"] = bid
        self._save(d)
        return bid

    def join_band(self, uid, bid):
        d = self._load()
        m = self._member(d, uid)
        if m["band"]:
            raise HouseError(IN_BAND)
        b = d["bands"].get(str(bid))
        if b is None:
            raise HouseError(NO_BAND)
        if b["house"] != m["house"]:
            raise HouseError(OTHER_HOUSE)
        if len(b["members"]) >= BAND_MAX:
            raise HouseError(BAND_FULL)
        b["members"].append(uid)
        m["band"] = bid
        self._save(d)

    def leave_band(self, uid):
        d = self._load()
        m = self._member(d, uid)
        if not m["band"]:
            raise HouseError(NO_BAND)
        self._leave_band(d, uid)
        self._save(d)

    @staticmethod
    def _leave_band(d, uid):
        m = d["members"].get(uid)
        if m is None or not m["band"]:
            return
        key = str(m["band"])
        m["band"] = 0
        b = d["bands"].get(key)
        if b is None:
            return
        if uid in b["members"]:
            b["members"].remove(uid)
        if not b["members"]:
            del d["bands"][key]
        elif b["leader"] == uid:            # the most loyal one left leads
            b["leader"] = max(b["members"], key=lambda u: d["members"][u]["loyalty"])

    def band_of(self, uid):
        """(band id, leader, members) of the player's band, or None."""
        d = self._load()
        m = d["members"].get(uid)
        if m is None or not m["band"]:
            return None
        b = d["bands"][str(m["band"])]
        return m["band"], b["leader"], list(b["members"])
