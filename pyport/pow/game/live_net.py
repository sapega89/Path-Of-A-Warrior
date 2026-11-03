"""v.java / u.java / b.java / ab.java - the network of Gamevil Live (PHASE_7). Port with a
replaced transport.

v.java was a Thread that opened socket://GAMEVIL_SERVER:GAMEVIL_PORT (ur.gamevil.net:28230),
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
    def __init__(self, paramArrayOfbyte):  # ab.java:6-8
        self.a = paramArrayOfbyte
        self.b = 0

    def a_v(self):  # ab.java:10-12  (s8)
        v = self.a[self.b]
        self.b += 1
        return v - 256 if v > 127 else v

    def b_v(self):  # ab.java:14-18  (s16)
        v = self.a[self.b] | self.a[self.b + 1] << 8
        self.b += 2
        return v - 65536 if v > 32767 else v

    def c_v(self):  # ab.java:20-26  (s32)
        v = struct.unpack_from("<i", self.a, self.b)[0]
        self.b += 4
        return v

    def a_I(self, paramInt):  # ab.java:28-37  (fixed-size string, up to the first 0)
        if self.a[self.b] == 0:
            self.b += paramInt
            return ""
        b = 0
        while b < paramInt and self.a[self.b + b] != 0:
            b += 1
        s = bytes(self.a[self.b:self.b + b]).decode("latin-1")
        self.b += paramInt
        return s


class LiveNet:  # v.java
    a = None        # StreamConnection -> the transport
    d = None        # s: the listener (as)
    f = True        # no request half-written
    g = 0
    h = False       # connected
    i = True        # the thread runs
    j = False       # connect requested
    m = False       # connected and waiting for answers (the 30 s timeout of as.m() counts)
    _buf = bytearray()   # u.b (ByteArrayOutputStream)

    def __init__(self):  # v.java:155-160
        LiveNet.f = True
        LiveNet.h = False
        LiveNet.i = True
        LiveNet.j = False
        self.k = None
        self.l = 0
        self._connecting = False

    def setPriority(self, p):
        pass

    def start(self):
        pass

    def a_TI(self, paramString, paramInt):  # v.java:33-37
        self.k = paramString
        self.l = paramInt
        LiveNet.j = True

    def a_v(self):  # v.java:39-53  (close)
        LiveNet.h = False
        if LiveNet.a is not None:
            LiveNet.a.close()
            LiveNet.a = None
        self._connecting = False
        LiveNet._buf = bytearray()

    def c_v(self):  # v.java:55-68  (open; the result comes on a later pump())
        from pow_mp.net.transport import make_live_transport
        try:
            LiveNet.a = make_live_transport(config.LIVE_SERVER)
            LiveNet.a.open()
            self._connecting = True
        except Exception as ex:
            print("Gamevil Live: connect failed:", repr(ex))
            LiveNet.d.e_v()

    @staticmethod
    def a_Ls(params):  # v.java:70-72
        LiveNet.d = params

    def pump(self):  # v.java:74-100  run(), one step per game frame
        if not LiveNet.i:
            return
        if LiveNet.j:
            LiveNet.j = False
            self.c_v()
        t = LiveNet.a
        if t is None:
            return
        if self._connecting:
            if t.connected:
                self._connecting = False
                LiveNet.h = True
                LiveNet.d.f_v()
                LiveNet.m = True
            elif t.failed:
                self._connecting = False
                LiveNet.d.e_v()
                return
            else:
                return
        if not LiveNet.h:
            return
        for p in t.poll():
            try:
                LiveNet.d.a_Lab(LiveAnswer(p))
            except Exception as ex:          # run(): catch (Exception) -> d.e()
                if config.DEBUG:
                    raise
                print("Gamevil Live: bad answer:", repr(ex))
                LiveNet.d.e_v()
                return
            if LiveNet.a is not t:                 # the answer closed the connection
                return
        if t.failed or not t.connected:      # IOException in b.b() -> d.e()
            LiveNet.d.e_v()

    def a_I(self, paramInt):  # v.java:111-118  (start a request: the opcode)
        if LiveNet.h:
            LiveNet.f = False
            LiveNet._buf = bytearray(struct.pack("<H", paramInt & 0xFFFF))

    @staticmethod
    def a_S(paramShort):  # v.java:120-123
        if LiveNet.h:
            LiveNet._buf += struct.pack("<H", paramShort & 0xFFFF)

    @staticmethod
    def a_B(paramByte):  # v.java:125-128
        if LiveNet.h:
            LiveNet._buf.append(paramByte & 0xFF)

    @staticmethod
    def b_I(paramInt):  # v.java:130-133
        if LiveNet.h:
            LiveNet._buf += struct.pack("<I", paramInt & 0xFFFFFFFF)

    @staticmethod
    def a_Z(paramBoolean):  # v.java:135-138
        if LiveNet.h:
            LiveNet._buf.append(1 if paramBoolean else 0)

    @staticmethod
    def b_TI(paramString, paramInt):  # v.java:140-143  (fixed-size string padded with 0)
        if LiveNet.h:
            raw = paramString.encode("latin-1", "replace")
            LiveNet._buf += raw[:paramInt].ljust(paramInt, b"\0")

    def b_v(self):  # v.java:145-148 + u.java:73-99  (u16 length + the request)
        data = bytes(LiveNet._buf)
        LiveNet._buf = bytearray()
        if LiveNet.a is not None and LiveNet.h:
            LiveNet.a.send(struct.pack("<H", len(data) + 2) + data)
        LiveNet.f = True
