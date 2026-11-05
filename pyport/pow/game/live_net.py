"""v.java / u.java / b.java / ab.java - the network of Live (PHASE_7). Port with a
replaced transport.

v.java was a Thread that opened socket://POW_SERVER:POW_PORT (the original host, port 28230),
read frames in its run() loop and called s.a(ab) for each (s = the as instance); u.java
wrote a request into a buffer and sent it with the u16 length in front; b.java read one
frame; ab.java reads the fields of an answer. The server is lost (pow_server/live.py speaks
the same protocol), and the port has no threads: pump() does what run() did, once per frame
from as.i(), and the socket is a transport of pow_mp/net/transport.py chosen by
config.LIVE_SERVER ("local" = the server inside the game, or ws(s)://host:port/live).
The connect host / port of a(String, int) are kept but not used.
"""
import struct

import config


class LiveAnswer:  # ab.java: one answer, read field by field (little-endian)
    def __init__(self, data):  # ab.java:6-8
        self.data = data
        self.pos = 0

    def read_s8(self):  # ab.java:10-12  (s8)
        v = self.data[self.pos]
        self.pos += 1
        return v - 256 if v > 127 else v

    def read_s16(self):  # ab.java:14-18  (s16)
        v = self.data[self.pos] | self.data[self.pos + 1] << 8
        self.pos += 2
        return v - 65536 if v > 32767 else v

    def read_s32(self):  # ab.java:20-26  (s32)
        v = struct.unpack_from("<i", self.data, self.pos)[0]
        self.pos += 4
        return v

    def read_string(self, size):  # ab.java:28-37  (fixed-size string, up to the first 0)
        if self.data[self.pos] == 0:
            self.pos += size
            return ""
        b = 0
        while b < size and self.data[self.pos + b] != 0:
            b += 1
        s = bytes(self.data[self.pos:self.pos + b]).decode("latin-1")
        self.pos += size
        return s


class LiveNet:  # v.java
    conn = None        # StreamConnection -> the transport
    listener = None        # s: the listener (as)
    idle = True        # no request half-written
    unused = 0
    connected = False       # connected
    running = True        # the thread runs
    connect_requested = False       # connect requested
    waiting = False       # connected and waiting for answers (the 30 s timeout of as.m() counts)
    _buf = bytearray()   # u.b (ByteArrayOutputStream)

    def __init__(self):  # v.java:155-160
        LiveNet.idle = True
        LiveNet.connected = False
        LiveNet.running = True
        LiveNet.connect_requested = False
        self.host = None
        self.port = 0
        self._connecting = False

    def setPriority(self, p):
        pass

    def start(self):
        pass

    def set_address(self, host, port):  # v.java:33-37
        self.host = host
        self.port = port
        LiveNet.connect_requested = True

    def close(self):  # v.java:39-53  (close)
        LiveNet.connected = False
        if LiveNet.conn is not None:
            LiveNet.conn.close()
            LiveNet.conn = None
        self._connecting = False
        LiveNet._buf = bytearray()

    def open(self):  # v.java:55-68  (open; the result comes on a later pump())
        from pow_mp.net.transport import make_live_transport
        try:
            LiveNet.conn = make_live_transport(config.LIVE_SERVER)
            LiveNet.conn.open()
            self._connecting = True
        except Exception as ex:
            print("Live: connect failed:", repr(ex))
            LiveNet.listener.on_connection_failed()

    @staticmethod
    def set_listener(listener):  # v.java:70-72
        LiveNet.listener = listener

    def pump(self):  # v.java:74-100  run(), one step per game frame
        if not LiveNet.running:
            return
        if LiveNet.connect_requested:
            LiveNet.connect_requested = False
            self.open()
        t = LiveNet.conn
        if t is None:
            return
        if self._connecting:
            if t.connected:
                self._connecting = False
                LiveNet.connected = True
                LiveNet.listener.on_connected()
                LiveNet.waiting = True
            elif t.failed:
                self._connecting = False
                LiveNet.listener.on_connection_failed()
                return
            else:
                return
        if not LiveNet.connected:
            return
        for p in t.poll():
            try:
                LiveNet.listener.on_answer(LiveAnswer(p))
            except Exception as ex:          # run(): catch (Exception) -> d.e()
                if config.DEBUG:
                    raise
                print("Live: bad answer:", repr(ex))
                LiveNet.listener.on_connection_failed()
                return
            if LiveNet.conn is not t:                 # the answer closed the connection
                return
        if t.failed or not t.connected:      # IOException in b.b() -> d.e()
            LiveNet.listener.on_connection_failed()

    def begin_request(self, opcode):  # v.java:111-118  (start a request: the opcode)
        if LiveNet.connected:
            LiveNet.idle = False
            LiveNet._buf = bytearray(struct.pack("<H", opcode & 0xFFFF))

    @staticmethod
    def write_short(value):  # v.java:120-123
        if LiveNet.connected:
            LiveNet._buf += struct.pack("<H", value & 0xFFFF)

    @staticmethod
    def write_byte(value):  # v.java:125-128
        if LiveNet.connected:
            LiveNet._buf.append(value & 0xFF)

    @staticmethod
    def write_int(value):  # v.java:130-133
        if LiveNet.connected:
            LiveNet._buf += struct.pack("<I", value & 0xFFFFFFFF)

    @staticmethod
    def write_bool(value):  # v.java:135-138
        if LiveNet.connected:
            LiveNet._buf.append(1 if value else 0)

    @staticmethod
    def write_string(text, size):  # v.java:140-143  (fixed-size string padded with 0)
        if LiveNet.connected:
            raw = text.encode("latin-1", "replace")
            LiveNet._buf += raw[:size].ljust(size, b"\0")

    def send_request(self):  # v.java:145-148 + u.java:73-99  (u16 length + the request)
        data = bytes(LiveNet._buf)
        LiveNet._buf = bytearray()
        if LiveNet.conn is not None and LiveNet.connected:
            LiveNet.conn.send(struct.pack("<H", len(data) + 2) + data)
        LiveNet.idle = True
