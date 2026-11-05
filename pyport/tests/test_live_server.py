"""PHASE_7: the Gamevil Live server of the single player (pow_server/live.py), driven with the
byte layouts as.n() writes and as.a(ab) reads."""
import random
import struct

import pytest

from pow_server import codec_bin
from pow_server.live import TAX_PERCENT, LiveServer, give_gift
from pow_server.storage import MemoryStorage, Storage


class Client:
    def __init__(self, server):
        self.got = []
        self.s = server.connect(lambda f: self.got.extend(codec_bin.unframe(f)[0]))

    def ask(self, op, body=b""):
        self.got.clear()
        self.s.receive(struct.pack("<H", op) + body)
        p = self.got[-1]
        rop, st = struct.unpack_from("<Hb", p)
        assert rop == op + 1
        return st, p[3:]


def login(server, uid="ANDREY", pwd="1234"):
    c = Client(server)
    st, body = c.ask(530, uid.encode().ljust(12, b"\0") + pwd.encode().ljust(16, b"\0") + b"1501" + bytes(8))
    return c, st, body


def item(iid, f=0, atk=5, def_=0, hp=0, mp=0):
    return struct.pack("<HB4H", iid, f, atk, def_, hp, mp)


def sync(c, gold, items):
    """768: gold and the backpack."""
    body = struct.pack("<iB", gold, len(items))
    for n, it in enumerate(items):
        body += it[:2] + struct.pack("<H", n + 1) + it[2:]
    st, ans = c.ask(768, body)
    assert st == 1
    safe, n = struct.unpack_from("<iB", ans)
    wh = [struct.unpack_from("<HHB4H", ans, 5 + 13 * i) for i in range(n)]
    return safe, wh


@pytest.fixture(params=["sqlite", "memory"])
def server(request):
    st = Storage() if request.param == "sqlite" else MemoryStorage()
    return LiveServer(st, rng=random.Random(5), notices=[["Hello", "", "", ""], ["Page 2"]])


def test_login_registers_then_welcomes_back(server):
    _, st, body = login(server)
    assert st == 1 and body[2] == 0                     # gamestr 48 "registered"
    _, st, body = login(server)
    assert st == 1 and body[2] == 2                     # 44 "Welcome back!"
    _, st, body = login(server, pwd="9999")
    assert st == -1 and body[2] == 1                    # 43 another password
    _, st, _ = login(server, uid="ab")
    assert st == -49


def test_requests_need_a_login(server):
    c = Client(server)
    assert c.ask(512)[0] == -1


def test_status_and_notices(server):
    c, _, _ = login(server)
    st, body = c.ask(512)
    notices, sold, gifts = body[0], body[1], body[2]
    assert (notices, sold, gifts) == (1, 0, 0) and body[24] == TAX_PERCENT
    st, body = c.ask(516)
    assert st == 1 and body[:5] == b"Hello" and body[64] == 1       # one more page
    st, body = c.ask(516)
    assert body[:6] == b"Page 2" and body[64] == 0


def test_safe_and_warehouse(server):
    c, _, _ = login(server)
    safe, wh = sync(c, 1000, [item(116), item(121)])
    assert safe == 0 and wh == []
    st, body = c.ask(832, struct.pack("<Bi", 0, 400))                # to the Safe
    assert st == 1 and struct.unpack("<ii", body) == (600, 400)
    assert c.ask(832, struct.pack("<Bi", 1, 401))[0] == -18          # more than is there
    st, body = c.ask(816, struct.pack("<BH", 0, 2))                   # backpack slot 2 -> warehouse
    assert st == 1
    wserial = struct.unpack("<H", body)[0]
    c2, _, _ = login(server)
    safe, wh = sync(c2, 600, [item(116)])
    assert safe == 400 and len(wh) == 1 and wh[0][0] == 121 and wh[0][1] == wserial
    st, body = c2.ask(816, struct.pack("<BH", 1, wserial))            # and back
    assert st == 1 and sync(c2, 600, [])[1] == []


def test_npc_market_always_sells_502_and_504(server):
    c, _, _ = login(server)
    sync(c, 20000, [])
    st, counts = c.ask(784, bytes([3, 3, 4]) + bytes(12))             # Rare, kind 3 = 504
    assert st == 1 and counts[0] >= 1
    st, body = c.ask(786, bytes([3, 4, 0]) + struct.pack("<i", 0) + bytes(7))
    assert st == 1 and body[0] >= 1
    lot, iid, price = struct.unpack_from("<iHi", body, 1)
    assert iid == 504 and price == 5000
    for left in (15000, 10000):
        st, body = c.ask(788, struct.pack("<iB", lot, 0) + bytes(6))
        assert st == 1 and struct.unpack("<Hii", body)[1:] == (left, 0)
    st, body = c.ask(786, bytes([3, 2, 0]) + struct.pack("<i", 0) + bytes(7))
    assert struct.unpack_from("<iHi", body, 1)[1:] == (502, 3000)


def test_normal_market_has_enchant_levels_and_pages(server):
    c, _, _ = login(server)
    sync(c, 0, [])
    found = 0
    for k in range(13):
        st, counts = c.ask(784, bytes([1, 1, k + 1]) + bytes(12))
        assert st == 1 and len(counts) == 10
        found += sum(counts)
    assert found == 13 * 4
    assert c.ask(788, struct.pack("<iB", 999999, 0) + bytes(6))[0] == -12      # sold out


def test_sell_buy_between_players_pays_the_seller_into_the_safe(server):
    a, _, _ = login(server, "ANDREY")
    sync(a, 0, [item(121, f=2, atk=9)])
    assert a.ask(800, struct.pack("<BHi", 0, 1, 7000))[0] == 1
    st, body = a.ask(864)
    assert st == 1 and body[0] == 1
    b, _, _ = login(server, "BORYS", "5555")
    sync(b, 8000, [])
    kind = 1                                                          # 121 is kind 1 of Normal
    st, counts = b.ask(784, bytes([1, 1, kind + 1]) + bytes(12))
    assert counts[2] >= 1
    st, body = b.ask(786, bytes([1, kind + 1, 2]) + struct.pack("<i", 0) + bytes(7))
    lots = [struct.unpack_from("<iHi", body, 1 + 17 * i) for i in range(body[0])]
    mine = next(x for x in lots if x[2] == 7000)
    st, body = b.ask(788, struct.pack("<iB", mine[0], 0) + bytes(6))
    assert st == 1 and struct.unpack("<Hii", body)[1] == 1000
    a2, _, _ = login(server, "ANDREY")
    st, body = a2.ask(512)
    assert body[1] == 1                                                # something was sold
    st, body = a2.ask(518)
    assert body[0] == 1 and struct.unpack_from("<HBI", body, 1) == (121, 2, 7000)
    safe, _ = sync(a2, 0, [])
    assert safe == 7000 - 7000 * TAX_PERCENT // 100
    assert a2.ask(864)[0] == -11


def test_max_five_sales_and_cancel(server):
    a, _, _ = login(server)
    sync(a, 0, [item(116 + i) for i in range(6)])
    for s in range(1, 6):
        assert a.ask(800, struct.pack("<BHi", 0, s, 100))[0] == 1
    assert a.ask(800, struct.pack("<BHi", 0, 6, 100))[0] == -16
    st, body = a.ask(864)
    lot = struct.unpack_from("<i", body, 1)[0]
    st, body = a.ask(866, struct.pack("<iB", lot, 1))                 # back into the warehouse
    assert st == 1
    assert len(sync(a, 0, [])[1]) == 1
    assert a.ask(866, struct.pack("<iB", lot, 1))[0] == -12


def test_save_and_load_user_data(server):
    a, _, _ = login(server)
    assert a.ask(262)[0] == -4
    body = bytes(range(22)) + b"STUVWXYZ" + b"rest"
    assert a.ask(256, body)[0] == 1
    st, back = a.ask(262)
    assert st == 1 and back == bytes(range(22)) + b"rest"


def test_gift_lands_in_the_warehouse(server):
    a, _, _ = login(server)
    assert give_gift(server.storage, "ANDREY", "RIVAL", {"id": 504, "f": 0, "atk": 0, "def": 0, "hp": 0, "mp": 0})
    _st, body = a.ask(512)
    assert body[2] == 1
    _st, body = a.ask(520)
    assert body[0] == 1 and body[1:6] == b"RIVAL" and struct.unpack_from("<H", body, 9)[0] == 504
    assert len(sync(a, 0, [])[1]) == 1


def test_npc_stock_is_kept_between_reads(server):
    assert server.market()["lots"] == server.market()["lots"]


def test_safe_stays_within_nine_digits(server):
    from pow_server.live import MAX_GOLD
    c, _, _ = login(server)
    sync(c, 2 ** 31 - 1, [])                                        # a client that lies
    assert c.ask(832, struct.pack("<Bi", 0, MAX_GOLD))[0] == 1
    sync(c, MAX_GOLD, [])
    assert c.ask(832, struct.pack("<Bi", 0, 1))[0] == -18
    assert sync(c, 0, [])[0] == MAX_GOLD
