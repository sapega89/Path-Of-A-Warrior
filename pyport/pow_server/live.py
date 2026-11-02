"""Gamevil Live of the single-player game: the "online shop" (PHASE_7, server side).

The single player's Gamevil Live (as.java / m.java, analysis/03 §1.8, §5) talked to
ur.gamevil.net:28230: a market where players sold items to each other (Trade), a Warehouse of
100 slots, a Safe for gold, a Gift List, server-kept Exp/Fame and a backup of the hero
(Management). That server is lost; this one speaks the same protocol, so the ported screens
work as they did. Accounts are the multiplayer ones (the original registered the UserID here
and the MP game let in only IDs registered in POW single).

Frame: u16 LE length (these 2 bytes included) + payload. C->S payload = u16 opcode + fields,
S->C = u16 opcode+1, s8 status (1 = OK, < 0 = error shown by as.b(int)), fields. Field layouts
are those as.n() writes and as.a(ab) reads (as.java 453-990); see the handlers below.

Made up (the server logic is lost, analysis/03 §5.5):
- the NPC stock: Normal / Special items regenerated every NPC_REFRESH seconds, and the Rare
  Silk Towel 502 and Emperor's Seal 504 always on sale (decision D3: offline every one of the
  149 recipes must be craftable, PHASE_7);
- prices: e.b(z) of the single player times a factor, 502 / 504 from config.LIVE_PRICE;
- tax TAX_PERCENT (ht[4]) taken from what the seller gets, the rest goes to the seller's Safe.
"""
import random
import re
import struct
import time

import config
from pow_server import codec_bin
from pow_server.loot import _read_arr

TAX_PERCENT = 10              # ht[4], shown in "Enter your selling price. N% of total ..."
GIFT_TAX_PERCENT = 0          # ht[5] (the Gift menu is not in this client)
WAREHOUSE = 100               # as.gw
BACKPACK = 25                 # cz.Y
MAX_SALES = 5                 # gamestr 27 "Item sales are limited up to 5 per user"
PAGE = 20                     # lots per page (as.gz)
NPC_REFRESH = 3600            # seconds between new NPC stock
MAX_GOLD = 999999999          # 9 digits of the price / amount fields
ELIXIRS = range(434, 438)     # U(): "Not possible for sale"

_ID_RE = re.compile(r"^[A-Z]{4,12}$")
_PWD_RE = re.compile(r"^[0-9]{4,12}$")

# as.gF: the kinds of every category in the Buy menu (a representative item id per kind)
KINDS = (
    (116, 121, 126, 101, 106, 111, 131, 136, 156, 161, 181, 146, 151),
    (331, 324, 322, 301, 308, 302, 341, 350, 357, 363, 370, 380, 415),
    tuple(range(501, 519)),
)

_data = None


def data():
    """kibo / sungbo / shinki rows by item id."""
    global _data
    if _data is None:
        _data = {}
        for base, name in ((101, "kibo.arr"), (301, "sungbo.arr"), (501, "shinki.arr")):
            for r, row in enumerate(_read_arr(name)):
                _data[base + r] = row
    return _data


def category(item_id):
    return 2 if item_id > 500 else 1 if item_id > 300 else 0


def kind(item_id):
    """The Buy-menu kind: column 7 of kibo / sungbo (the icon frame, as.U() 1421-1430), id-501
    for Rare."""
    return item_id - 501 if item_id > 500 else data()[item_id][7]


def base_item(item_id, rng=None):
    """z of a fresh item: kibo = base (+ 0..spread with rng, like ag.k(id, 1)), sungbo / shinki
    stats as they are."""
    row = data()[item_id]
    it = {"id": item_id, "f": 0, "atk": 0, "def": 0, "hp": 0, "mp": 0}
    keys = ("atk", "def", "hp", "mp")
    if item_id < 300:
        it[keys[row[2]]] = row[3] + (rng.randint(0, row[4]) if rng else 0)
    else:
        for k, v in zip(keys, row[2:6]):
            it[k] = v
    return it


def max_enchant(item_id):
    if item_id < 300:
        return data()[item_id][5]
    if item_id < 500:
        return data()[item_id][6]
    return 0


def enchant(it, n, rng):
    """e.a(z, n) (e.java 2628-2668): n successful enchants."""
    odds = (30, 25, 20, 15, 9, 1)
    for _ in range(n):
        j, acc, b = rng.randint(0, 100), 0, 0
        while b < 5:
            acc += odds[b]
            if j < acc:
                break
            b += 1
        mult = (b + 5) * 10
        for k in ("atk", "def", "hp", "mp"):
            if it[k] > 0:
                it[k] += max(1, (it[k] * mult // 10 + 50) // 100)
        it["f"] += 1
    return it


def sp_price(it):
    """e.b(z) (e.java 2817-2830): the single player's shop price of an item."""
    i = it["id"]
    if i < 300:
        return data()[i][6] + it["atk"] * 100 + it["def"] * 100 + it["hp"] // 5 * 100 + it["mp"] // 3 * 100
    if i < 500:
        k = 800 if data()[i][6] == 0 else 400
        return it["atk"] * k + it["def"] * k + it["hp"] // 5 * k + it["mp"] // 3 * k
    return data()[i][6]


# --- payload reader / writer ---------------------------------------------------------------
class Reader:
    """ab.java: a() s8, b() s16, c() s32, a(n) fixed string."""

    def __init__(self, data):
        self.d, self.p = data, 0

    def take(self, fmt):
        n = struct.calcsize(fmt)
        if self.p + n > len(self.d):
            raise ValueError("short message")
        v = struct.unpack_from(fmt, self.d, self.p)
        self.p += n
        return v[0] if len(v) == 1 else v

    def s(self, n):
        raw = self.take("%ds" % n)
        return raw.split(b"\0")[0].decode("latin-1")


def _item_bytes(it, serial=None):
    """{u16 id, [u16 serial], u8 f, 4 x u16} as 768 / 769 carry it."""
    if serial is None:
        return struct.pack("<HB4H", it["id"], it["f"], it["atk"], it["def"], it["hp"], it["mp"])
    return struct.pack("<HHB4H", it["id"], serial, it["f"], it["atk"], it["def"], it["hp"], it["mp"])


def _item_read(r, with_serial):
    if with_serial:
        iid, serial, f, a, d, h, m = r.take("<HHB4H")
    else:
        iid, f, a, d, h, m = r.take("<HB4H")
        serial = None
    return {"id": iid, "f": f, "atk": a, "def": d, "hp": h, "mp": m}, serial


def _str(s, n):
    return s.encode("latin-1", "replace")[:n].ljust(n, b"\0")


class LiveServer:
    def __init__(self, storage, *, rng=None, clock=time.time, notices=()):
        self.storage = storage
        self.rng = rng or random.Random()
        self.clock = clock
        self.notices = [list(p)[:4] for p in notices]

    def connect(self, send):
        return LiveSession(self, send)

    # --- documents in storage ---------------------------------------------------------
    def user(self, uid):
        u = self.storage.live_get("user:" + uid)
        if u is None:
            u = {"safe": 0, "warehouse": [], "serial": 0, "sold": [], "gifts": [],
                 "fame": 0, "exp": 0, "backup": None}
        return u

    def save_user(self, uid, u):
        self.storage.live_put("user:" + uid, u)

    def market(self):
        m = self.storage.live_get("market")
        if m is None:
            m = {"next": 1, "lots": [], "npc_at": None}
        if m["npc_at"] is None or self.clock() - m["npc_at"] >= NPC_REFRESH:
            self._restock(m)
            self.save_market(m)       # or every read would roll another stock with the same lot ids
        return m

    def save_market(self, m):
        self.storage.live_put("market", m)

    def _restock(self, m):
        """New NPC stock: a few items of every Normal / Special kind at enchant 0..4, two
        random Rare ones, and 502 / 504 that never run out."""
        rng = self.rng
        lots = [x for x in m["lots"] if x["seller"]]
        by_kind = {}
        for iid in data():
            if iid in ELIXIRS:
                continue
            by_kind.setdefault((category(iid), kind(iid)), []).append(iid)

        def add(it, factor, forever=False, price=None):
            p = price if price is not None else max(1, int(sp_price(it) * factor))
            lots.append({"id": m["next"], "seller": "", "item": it, "price": min(p, MAX_GOLD),
                         "forever": forever})
            m["next"] += 1

        for cat, lo, hi in ((0, 1.2, 2.0), (1, 1.0, 1.6)):
            for k in range(len(KINDS[cat])):
                ids = by_kind.get((cat, k), [])
                for _ in range(4 if cat == 0 else 2):
                    if not ids:
                        break
                    iid = rng.choice(ids)
                    it = base_item(iid, rng)
                    enchant(it, min(max_enchant(iid), rng.choice((0, 0, 0, 1, 1, 2, 3, 4))), rng)
                    add(it, rng.uniform(lo, hi))
        rares = [i for i in range(501, 519) if i not in config.LIVE_PRICE]
        for iid in rng.sample(rares, 2):
            add(base_item(iid), rng.uniform(1.0, 1.3))
        for iid, price in config.LIVE_PRICE.items():
            add(base_item(iid), 1, forever=True, price=price)
        m["lots"], m["npc_at"] = lots, self.clock()


class LiveSession:
    def __init__(self, server, send):
        self.server = server
        self._send = send
        self.user = None
        self.closed = False
        self.gold = 0                  # cz.E as the last 768 / answer said
        self.backpack = {}             # serial -> item (the backpack the client sent in 768)
        self.notice_page = 0
        self.page = None               # (cat, kind, enchant, [lot ids], start) of the last 787
        self.last_seen = server.clock()

    def send(self, op, st=1, body=b""):
        self._send(codec_bin.frame(struct.pack("<Hb", op, st) + body))

    def close(self):
        self.closed = True

    def idle_seconds(self):
        return self.server.clock() - self.last_seen

    def receive(self, payload):
        self.last_seen = self.server.clock()
        if len(payload) < 2:
            return
        op = payload[0] | payload[1] << 8
        r = Reader(payload[2:])
        h = getattr(self, "op_%d" % op, None)
        if h is None:
            return self.send(op + 1, -1)
        if op != 530 and self.user is None:
            return self.send(op + 1, -1)
        try:
            h(r)
        except ValueError:
            self.send(op + 1, -26)

    # --- helpers --------------------------------------------------------------
    def _u(self):
        return self.server.user(self.user)

    def _save(self, u):
        self.server.save_user(self.user, u)

    @staticmethod
    def _serial(u):
        u["serial"] = u["serial"] % 60000 + 1
        return u["serial"]

    def _new_bp_serial(self):
        s = 1000
        while s in self.backpack:
            s += 1
        return s

    # --- 530 login / registration ------------------------------------------------
    def op_530(self, r):
        """{UserID[12], password[16], "1501", u32, u32} -> {u8, u8, u8 result}: 0 = new
        account (gamestr 48), 2 = welcome back (44); status -1 + result 1 = another password
        (43), -49 = the ID cannot be used (54)."""
        uid, pwd = r.s(12), r.s(16)
        st = self.server.storage
        if not _ID_RE.match(uid) or not _PWD_RE.match(pwd):
            return self.send(531, -49, b"\0\0\3")
        if st.has_account(uid):
            if not st.check_password(uid, pwd):
                return self.send(531, -1, b"\0\0\1")
            result = 2
        else:
            st.create_account(uid, pwd)
            result = 0
        self.user = uid
        self.send(531, 1, bytes([0, 0, result]))

    # --- 512 status, 516 notices, 518 sale list, 520 gift list ----------------------
    def op_512(self, r):
        u = self._u()
        body = struct.pack("<BBBB5IBB", 1 if self.server.notices else 0, 1 if u["sold"] else 0,
                           1 if u["gifts"] else 0, 0, 0, 0, 0, 0, 0, TAX_PERCENT, GIFT_TAX_PERCENT)
        self.send(513, 1, body)

    def op_516(self, r):
        pages = self.server.notices
        if not pages:
            return self.send(517, -11)
        page = pages[self.notice_page % len(pages)]
        self.notice_page += 1
        lines = (list(page) + [""] * 4)[:4]
        more = 1 if self.notice_page < len(pages) else 0
        if not more:
            self.notice_page = 0
        self.send(517, 1, b"".join(_str(x, 16) for x in lines) + bytes([more]))

    def op_518(self, r):
        u = self._u()
        sold, u["sold"] = u["sold"][:PAGE], u["sold"][PAGE:]
        self._save(u)
        body = bytes([len(sold)]) + b"".join(struct.pack("<HBI", s["item"]["id"], s["item"]["f"], s["price"])
                                             for s in sold)
        self.send(519, 1, body)

    def op_520(self, r):
        """The gifts already wait in the Warehouse (put there by give_gift); this lists them."""
        u = self._u()
        gifts, u["gifts"] = u["gifts"][:5], u["gifts"][5:]
        self._save(u)
        body = bytes([len(gifts)]) + b"".join(_str(g["from"], 8) + _item_bytes(g["item"]) for g in gifts)
        self.send(521, 1, body + bytes([1 if u["gifts"] else 0]))

    # --- 258 / 260 Exp and Fame kept on the server ------------------------------
    def op_258(self, r):
        u = self._u()
        self.send(259, 1, struct.pack("<II", u["fame"], u["exp"]))
        u["fame"] = u["exp"] = 0
        self._save(u)

    def op_260(self, r):
        self.send(261, 1)

    # --- 768 sync: the client's gold and backpack -> Safe and Warehouse --------------
    def op_768(self, r):
        self.gold = max(0, min(MAX_GOLD, r.take("<i")))   # the client's word, as in the original
        n = r.take("<B")
        self.backpack = {}
        for _ in range(n):
            it, serial = _item_read(r, True)
            self.backpack[serial] = it
        u = self._u()
        wh = u["warehouse"]
        body = struct.pack("<iB", u["safe"], len(wh)) + b"".join(_item_bytes(w["item"], w["serial"]) for w in wh)
        self.send(769, 1, body)

    # --- 832 Safe -----------------------------------------------------------------
    def op_832(self, r):
        """{u8 0 = to the Safe / 1 = out of it, u32 amount} -> {u32 gold, u32 safe}."""
        d, amount = r.take("<Bi")
        u = self._u()
        if amount <= 0 or (d == 0 and amount > self.gold) or (d == 1 and amount > u["safe"]):
            return self.send(833, -18)
        if (d == 0 and u["safe"] + amount > MAX_GOLD) or (d == 1 and self.gold + amount > MAX_GOLD):
            return self.send(833, -18)    # 9 digits, and the u32 fields stay in range
        if d == 0:
            self.gold, u["safe"] = self.gold - amount, u["safe"] + amount
        else:
            self.gold, u["safe"] = self.gold + amount, u["safe"] - amount
        self._save(u)
        self.send(833, 1, struct.pack("<ii", self.gold, u["safe"]))

    # --- 816 Warehouse ------------------------------------------------------------
    def op_816(self, r):
        """{u8 0 = backpack -> warehouse / 1 = back, u16 serial} -> {u16 new serial}."""
        d, serial = r.take("<BH")
        u = self._u()
        wh = u["warehouse"]
        if d == 0:
            it = self.backpack.get(serial)
            if it is None:
                return self.send(817, -26)
            if len(wh) >= WAREHOUSE:
                return self.send(817, -15)
            del self.backpack[serial]
            new = self._serial(u)
            wh.append({"serial": new, "item": it})
        else:
            w = next((w for w in wh if w["serial"] == serial), None)
            if w is None:
                return self.send(817, -26)
            if len(self.backpack) >= BACKPACK:
                return self.send(817, -1)
            wh.remove(w)
            new = self._new_bp_serial()
            self.backpack[new] = w["item"]
        self._save(u)
        self.send(817, 1, struct.pack("<H", new))

    # --- 784 / 786 / 788 Buy -------------------------------------------------------
    def _lots(self, m, cat, k, ench=None):
        return [x for x in m["lots"] if category(x["item"]["id"]) == cat and kind(x["item"]["id"]) == k
                and (ench is None or cat == 2 or x["item"]["f"] == ench) and x["seller"] != self.user]

    def op_784(self, r):
        """{cat+1, cat+1, kind+1, ...} -> 10 x u8: lots for sale at enchant 0..9."""
        _, cat, k = r.take("<BBB")
        lots = self._lots(self.server.market(), cat - 1, k - 1)
        counts = [0] * 10
        for x in lots:
            counts[min(9, x["item"]["f"])] += 1
        self.page = None
        self.send(785, 1, bytes(min(99, c) for c in counts))

    def op_786(self, r):
        """{cat+1, kind+1, enchant, u32 lot under the cursor, ...} -> u8 n, n x {u32 lot,
        u16 id, u32 price, u8 f, 4 x u16}. The client keeps the page number (gS += gT) and
        sends only the lot under the cursor: on the top row it asks for the page before, on
        the bottom row for the next one (as.Y()), otherwise for the first."""
        cat, k, ench, cursor = r.take("<BBBi")
        cat, k = cat - 1, k - 1
        m = self.server.market()
        lots = sorted(self._lots(m, cat, k, ench), key=lambda x: (x["price"], x["id"]))
        start = 0
        p = self.page
        if p is not None and p[:3] == (cat, k, ench) and cursor in p[3]:
            pos = p[3].index(cursor)
            if pos >= PAGE - 5:
                start = p[4] + PAGE
            elif pos < 5:
                start = p[4] - PAGE
            else:
                start = p[4]
        if start < 0 or start >= len(lots):
            return self.send(787, -11)
        page = lots[start:start + PAGE]
        self.page = (cat, k, ench, [x["id"] for x in page], start)
        body = bytes([len(page)]) + b"".join(struct.pack("<iHi", x["id"], x["item"]["id"], x["price"])
                                             + _item_bytes(x["item"])[2:] for x in page)
        self.send(787, 1, body)

    def op_788(self, r):
        """{u32 lot, u8 0 = backpack / 1 = warehouse, ...} -> {u16 serial, u32 gold, u32 safe}.
        The seller gets the price minus TAX_PERCENT in the Safe and a line in the Sale List."""
        lot_id, dest = r.take("<iB")
        m = self.server.market()
        lot = next((x for x in m["lots"] if x["id"] == lot_id), None)
        if lot is None:
            return self.send(789, -12)
        if lot["seller"] == self.user:
            return self.send(789, -22)
        if lot["price"] > self.gold:
            return self.send(789, -18)
        u = self._u()
        if dest == 1 and len(u["warehouse"]) >= WAREHOUSE:
            return self.send(789, -15)
        if dest == 0 and len(self.backpack) >= BACKPACK:
            return self.send(789, -15)
        it = dict(lot["item"])
        if not lot["forever"]:
            m["lots"].remove(lot)
        self.server.save_market(m)
        if lot["seller"]:
            su = self.server.user(lot["seller"])
            su["safe"] = min(MAX_GOLD, su["safe"] + lot["price"] - lot["price"] * TAX_PERCENT // 100)
            su["sold"].append({"item": it, "price": lot["price"]})
            self.server.save_user(lot["seller"], su)
            u = self._u()
        self.gold -= lot["price"]
        if dest == 1:
            serial = self._serial(u)
            u["warehouse"].append({"serial": serial, "item": it})
        else:
            serial = self._new_bp_serial()
            self.backpack[serial] = it
        self._save(u)
        self.send(789, 1, struct.pack("<Hii", serial, self.gold, u["safe"]))

    # --- 800 Sell / 802 Price Info / 864 my lots / 866 Cancel ----------------------
    def op_800(self, r):
        """{u8 0 = from the backpack / 1 = from the warehouse, u16 serial, u32 price}."""
        src, serial, price = r.take("<BHi")
        m = self.server.market()
        if sum(1 for x in m["lots"] if x["seller"] == self.user) >= MAX_SALES:
            return self.send(801, -16)
        if price <= 0 or price > MAX_GOLD:
            return self.send(801, -2)
        u = self._u()
        if src == 0:
            it = self.backpack.get(serial)
        else:
            w = next((w for w in u["warehouse"] if w["serial"] == serial), None)
            it = w and w["item"]
        if it is None or it["id"] in ELIXIRS or it["id"] < 100:
            return self.send(801, -26 if it is None else -2)
        if src == 0:
            del self.backpack[serial]
        else:
            u["warehouse"].remove(w)
            self._save(u)
        m["lots"].append({"id": m["next"], "seller": self.user, "item": it, "price": price, "forever": False})
        m["next"] += 1
        self.server.save_market(m)
        self.send(801, 1)

    def op_802(self, r):
        """{cat+1, kind+1, ...} -> u8 n, n x {u16 id, u32 price, u8 f, 4 x u16}: what the
        market asks for this kind now (cheapest first)."""
        cat, k = r.take("<BB")
        lots = sorted(self._lots(self.server.market(), cat - 1, k - 1), key=lambda x: x["price"])[:PAGE]
        if not lots:
            return self.send(803, -11)
        body = bytes([len(lots)]) + b"".join(struct.pack("<Hi", x["item"]["id"], x["price"])
                                             + _item_bytes(x["item"])[2:] for x in lots)
        self.send(803, 1, body)

    def op_864(self, r):
        mine = [x for x in self.server.market()["lots"] if x["seller"] == self.user][:PAGE]
        if not mine:
            return self.send(865, -11)
        body = bytes([len(mine)]) + b"".join(struct.pack("<iHi", x["id"], x["item"]["id"], x["price"])
                                             + _item_bytes(x["item"])[2:] for x in mine)
        self.send(865, 1, body)

    def op_866(self, r):
        """{u32 lot, u8 0 = back to the backpack / 1 = to the warehouse} -> {u16 serial};
        -12 = it was sold meanwhile."""
        lot_id, dest = r.take("<iB")
        m = self.server.market()
        lot = next((x for x in m["lots"] if x["id"] == lot_id and x["seller"] == self.user), None)
        if lot is None:
            return self.send(867, -12)
        u = self._u()
        if dest == 1 and len(u["warehouse"]) >= WAREHOUSE:
            return self.send(867, -15)
        m["lots"].remove(lot)
        self.server.save_market(m)
        if dest == 1:
            serial = self._serial(u)
            u["warehouse"].append({"serial": serial, "item": lot["item"]})
            self._save(u)
        else:
            serial = self._new_bp_serial()
            self.backpack[serial] = lot["item"]
        self.send(867, 1, struct.pack("<H", serial))

    # --- 256 / 262 Management: Save / Load User Data ------------------------------
    def op_256(self, r):
        u = self._u()
        u["backup"] = r.d.hex()
        self._save(u)
        self.send(257, 1)

    def op_262(self, r):
        """263 reads what 256 wrote without cz.s/t/u/v (the item bonuses, 4 x u16 after cz.J,
        bytes 22..30): as.java 476-490 vs 698-708."""
        b = self._u()["backup"]
        if not b:
            return self.send(263, -4)
        raw = bytes.fromhex(b)
        self.send(263, 1, raw[:22] + raw[30:])


def give_gift(storage, uid, sender, item):
    """Put an item in a player's Warehouse with a Gift List line (e.g. multiplayer loot)."""
    srv = LiveServer(storage)
    u = srv.user(uid)
    if len(u["warehouse"]) >= WAREHOUSE:
        return False
    serial = LiveSession._serial(u)
    u["warehouse"].append({"serial": serial, "item": item})
    u["gifts"].append({"from": sender[:8], "item": item})
    srv.save_user(uid, u)
    return True
