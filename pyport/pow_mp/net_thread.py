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

TOKEN_STORE = "pow_mp_token"   # noqa: S105 (the name of the RecordStore, not a secret)


class NetThread:
    last_opcode = 0          # opcode of the last received frame (h.java:12)
    conn = None       # StreamConnection -> the transport
    game = None       # the game (g)
    free = True       # free to start a new message (h.a(int) waits for it)
    idle_frames = 0          # frames since the last traffic (keepalive counter of g.d())
    unused = 0
    connected = False      # connected
    running = True       # thread running
    connect_requested = False      # connect requested
    _buf = None
    _inbox = []
    _token = None

    def __init__(self):  # h.java:29
        NetThread.free = True
        NetThread.connected = False
        NetThread.running = True
        NetThread.connect_requested = False
        self.host = None
        self.port = 0

    def setPriority(self, p):
        pass

    def start(self):
        pass

    def set_address(self, host, port):  # h.java:36  connect to (host, port)
        self.host = host
        self.port = port
        NetThread.connect_requested = True

    @staticmethod
    def close():  # h.java:42  close
        NetThread.idle_frames = 0
        NetThread.connected = False
        if NetThread.conn is not None:
            NetThread.conn.close()
        NetThread.conn = None

    @staticmethod
    def set_game(game):  # h.java:84
        NetThread.game = game

    # --- the thread's loop, one step per game frame ------------------------------
    @staticmethod
    def tick():
        from pow_mp.answer import Answer
        if NetThread.connect_requested:
            NetThread.connect_requested = False
            if NetThread.conn is None:
                NetThread.conn = make_transport(config.MP_SERVER)
            NetThread.conn.open()
            NetThread._connecting = True
        t = NetThread.conn
        if t is None:
            return
        if getattr(NetThread, "_connecting", False):
            if t.connected:
                NetThread._connecting = False
                NetThread.idle_frames = 0
                NetThread.connected = True
                NetThread.game.login()                       # h.c(): connected -> g.l() sends 278 / 262
            elif t.failed:
                NetThread._connecting = False
                NetThread.game.on_net_error(0)
            return
        if not NetThread.connected:
            return
        NetThread._inbox.extend(t.poll())
        if NetThread._inbox:
            payload = NetThread._inbox.pop(0)
            NetThread._port_extra_in(payload)
            data = [b - 256 if b > 127 else b for b in payload]   # Java bytes are signed
            if len(data) < 2:
                NetThread.game.on_net_error(3)
                return
            NetThread.last_opcode = (data[0] & 0xFF) | (data[1] & 0xFF) << 8
            try:
                NetThread.game.on_answer(Answer(data))
            except IndexError:                  # a short frame: the client failed with g(3)
                NetThread.game.on_net_error(3)
            NetThread.idle_frames = 0
        elif not t.connected:
            NetThread.game.on_net_error(2)                          # IOException in h.run()

    # --- sending (e.java's buffer) --------------------------------------------------------
    def begin(self, opcode):  # h.java:131  start a message with opcode n2
        if NetThread.connected:
            NetThread.free = False
            NetThread._buf = bytearray(struct.pack("<H", opcode & 0xFFFF))

    @staticmethod
    def write_byte(value):  # h.java:141
        if NetThread.connected and NetThread._buf is not None:
            NetThread._buf.append(value & 0xFF)

    @staticmethod
    def write_int(value):  # h.java:147  s32
        if NetThread.connected and NetThread._buf is not None:
            NetThread._buf += struct.pack("<I", value & 0xFFFFFFFF)

    @staticmethod
    def write_string(text, size):  # h.java:153  fixed string
        if NetThread.connected and NetThread._buf is not None:
            raw = (text or "").encode("latin-1", "replace")[:size]
            NetThread._buf += raw + b"\0" * (size - len(raw))

    @staticmethod
    def send():  # h.java:159  send
        NetThread.idle_frames = 0
        buf, NetThread._buf = NetThread._buf, None
        NetThread.free = True
        if buf is None or NetThread.conn is None:
            return
        if struct.unpack_from("<H", buf)[0] == 262:      # PORT-EXTRA: session token + SP hero
            tok = (NetThread.token() or "").encode("ascii")[:16]
            buf += tok + b"\0" * (16 - len(tok))
            buf += NetThread._sp_hero()
        NetThread.conn.send(struct.pack("<H", len(buf) + 2) + bytes(buf))

    # --- PORT-EXTRA: the session token -------------------------------------------------
    @staticmethod
    def token():
        if NetThread._token is None:
            try:
                rs = RecordStore.openRecordStore(TOKEN_STORE, False)
                NetThread._token = bytes(rs.getRecord(1)).decode("ascii", "replace").rstrip("\0")
            except Exception:
                NetThread._token = ""
        return NetThread._token

    @staticmethod
    def _save_token(tok):
        NetThread._token = tok
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
        from pow_server import codec_bin
        from pow_server import messages as M
        sp_bridge.add_item()                 # loot still waiting for a free backpack cell
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
            item = None
            if len(payload) >= 46:                          # PORT-EXTRA loot (9.9)
                item = struct.unpack_from("<Hhhhh", payload, 36)
                if not item[0]:
                    item = None
            if sp_bridge.embedded:                          # PORT-EXTRA: the hero is in memory
                sp_bridge.keep_rewards(gold, fame, exp, item)
                return
            sp_bridge.add_rewards(gold, fame, exp)
            if item:
                sp_bridge.add_item(*item)
        if op == 279 and st == 1 and len(payload) >= 19:
            NetThread._save_token(payload[3:19].split(b"\0")[0].decode("ascii", "replace"))
        elif op == 263 and st == -3:
            NetThread._save_token("")
            try:                                     # forget the saved UserID: Login next time
                rs = RecordStore.openRecordStore("pow_mp_save", False)
                rec = bytearray(rs.getRecord(1))
                rec[2:28] = bytes(26)
                rs.setRecord(1, rec, 0, len(rec))
            except Exception:
                pass
