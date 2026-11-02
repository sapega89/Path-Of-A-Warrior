"""h.java - the network thread. Hand-written replacement over pow_mp/net/transport.py.

h.java opened socket://GAMEVIL_SERVER:GAMEVIL_PORT in its own thread, read frames with d.b()
and called g.a(k) for each, sleeping 100 ms after every frame; writing went through e.java
(a byte buffer) and h.b() sent it. Here the game loop calls h.tick() once per frame: it
connects when asked, delivers at most one received frame (like the 100 ms sleep did) and
reports a dropped connection the way h.run() did (g.g(1..3)).

Where it connects: config.MP_SERVER ("local" = the server inside the game, or ws(s)://...),
not the manifest's GAMEVIL_SERVER (dead).

PORT-EXTRA (pow_server/messages.py): the token of 279 is kept in RMS "pow_mp_token" and
appended to every 262; a 263 with status -3 (token refused) forgets it and the saved UserID,
so the next start shows the Login screen. After the token every 262 carries the hero of the
single-player save (task 9.10, pow_mp/sp_bridge.py), and a 1032 (battle end) adds its gold,
fame and exp to that save.
"""
import struct

import config
from pow.midp.rms import RecordStore
from pow_mp.net.transport import make_transport

TOKEN_STORE = "pow_mp_token"


class h:
    a = 0          # opcode of the last received frame (h.java:12)
    b = None       # StreamConnection -> the transport
    e = None       # the game (g)
    g = True       # free to start a new message (h.a(int) waits for it)
    h = 0          # frames since the last traffic (keepalive counter of g.d())
    i = 0
    j = False      # connected
    k = True       # thread running
    l = False      # connect requested
    _buf = None
    _inbox = []
    _token = None

    def __init__(self):  # h.java:29
        h.g = True
        h.j = False
        h.k = True
        h.l = False
        self.m = None
        self.n = 0

    def setPriority(self, p):
        pass

    def start(self):
        pass

    def a_TI(self, string, n2):  # h.java:36  connect to (host, port)
        self.m = string
        self.n = n2
        h.l = True

    @staticmethod
    def a_v():  # h.java:42  close
        h.h = 0
        h.j = False
        if h.b is not None:
            h.b.close()
        h.b = None

    @staticmethod
    def a_Lg(g2):  # h.java:84
        h.e = g2

    # --- the thread's loop, one step per game frame ------------------------------
    @staticmethod
    def tick():
        from pow_mp._gen.k import k
        if h.l:
            h.l = False
            if h.b is None:
                h.b = make_transport(config.MP_SERVER)
            h.b.open()
            h._connecting = True
        t = h.b
        if t is None:
            return
        if getattr(h, "_connecting", False):
            if t.connected:
                h._connecting = False
                h.h = 0
                h.j = True
                h.e.l_v()                       # h.c(): connected -> g.l() sends 278 / 262
            elif t.failed:
                h._connecting = False
                h.e.g_I(0)
            return
        if not h.j:
            return
        h._inbox.extend(t.poll())
        if h._inbox:
            payload = h._inbox.pop(0)
            h._port_extra_in(payload)
            data = [b - 256 if b > 127 else b for b in payload]   # Java bytes are signed
            if len(data) < 2:
                h.e.g_I(3)
                return
            h.a = (data[0] & 0xFF) | (data[1] & 0xFF) << 8
            try:
                h.e.a_Lk(k(data))
            except IndexError:                  # a short frame: the client failed with g(3)
                h.e.g_I(3)
            h.h = 0
        elif not t.connected:
            h.e.g_I(2)                          # IOException in h.run()

    # --- sending (e.java's buffer) --------------------------------------------------------
    def a_I(self, n2):  # h.java:131  start a message with opcode n2
        if h.j:
            h.g = False
            h._buf = bytearray(struct.pack("<H", n2 & 0xFFFF))

    @staticmethod
    def a_B(by):  # h.java:141
        if h.j and h._buf is not None:
            h._buf.append(by & 0xFF)

    @staticmethod
    def b_I(n2):  # h.java:147  s32
        if h.j and h._buf is not None:
            h._buf += struct.pack("<I", n2 & 0xFFFFFFFF)

    @staticmethod
    def b_TI(string, n2):  # h.java:153  fixed string
        if h.j and h._buf is not None:
            raw = (string or "").encode("latin-1", "replace")[:n2]
            h._buf += raw + b"\0" * (n2 - len(raw))

    @staticmethod
    def b_v():  # h.java:159  send
        h.h = 0
        buf, h._buf = h._buf, None
        h.g = True
        if buf is None or h.b is None:
            return
        if struct.unpack_from("<H", buf)[0] == 262:      # PORT-EXTRA: session token + SP hero
            tok = (h.token() or "").encode("ascii")[:16]
            buf += tok + b"\0" * (16 - len(tok))
            buf += h._sp_hero()
        h.b.send(struct.pack("<H", len(buf) + 2) + bytes(buf))

    # --- PORT-EXTRA: the session token -------------------------------------------------
    @staticmethod
    def token():
        if h._token is None:
            try:
                rs = RecordStore.openRecordStore(TOKEN_STORE, False)
                h._token = bytes(rs.getRecord(1)).decode("ascii", "replace").rstrip("\0")
            except Exception:
                h._token = ""
        return h._token

    @staticmethod
    def _save_token(tok):
        h._token = tok
        data = bytearray(tok.encode("ascii", "replace")[:16].ljust(16, b"\0"))
        try:
            rs = RecordStore.openRecordStore(TOKEN_STORE, True)
            if rs.getNumRecords() == 0:
                rs.addRecord(data, 0, len(data))
            else:
                rs.setRecord(1, data, 0, len(data))
        except Exception as ex:
            print("token not saved:", ex)

    @staticmethod
    def _sp_hero():
        """The SP_HERO tail of 262 (pow_server/messages.py); sp = 0 without a single-player save."""
        from pow_mp import sp_bridge
        from pow_server import codec_bin, messages as M
        hero = sp_bridge.hero(sp_bridge.read_save())
        msg = {"sp": 0} if hero is None else dict({"sp": 1}, **{"sp_" + k: v for k, v in hero.items()})
        buf = bytearray()
        try:
            codec_bin._encode_fields(buf, M.SP_HERO, msg)
        except Exception:
            buf = bytearray()
            codec_bin._encode_fields(buf, M.SP_HERO, {"sp": 0})
        return bytes(buf)

    @staticmethod
    def _port_extra_in(payload):
        if len(payload) < 3:
            return
        op, st = struct.unpack_from("<Hb", payload)
        if op == 1032 and st == 1 and len(payload) >= 12:   # win u8, gold s16, grade u8, fame s16, exp s16
            from pow_mp import sp_bridge
            gold, _, fame, exp = struct.unpack_from("<hBhh", payload, 4)
            sp_bridge.add_rewards(gold, fame, exp)
        if op == 279 and st == 1 and len(payload) >= 19:
            h._save_token(payload[3:19].split(b"\0")[0].decode("ascii", "replace"))
        elif op == 263 and st == -3:
            h._save_token("")
            try:                                     # forget the saved UserID: Login next time
                rs = RecordStore.openRecordStore("pow_mp_save", False)
                rec = bytearray(rs.getRecord(1))
                rec[2:28] = bytes(26)
                rs.setRecord(1, rec, 0, len(rec))
            except Exception:
                pass
