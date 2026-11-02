"""a.java - SP2 sprite frames (the byte version of the single player's SP3). Literal port.

    u8 n ; n x {u8 srcX, u8 srcY, s8 w, s8 h, s8 anchorX, s8 anchorY}     (06 §5.1)
"""
from pow_mp.n import n


def _s8(v):
    return v - 256 if v > 127 else v


class a:
    def __init__(self, string):  # a.java:14-33
        self.b = n.a(string)
        self.a = _s8(self.b[0])
        self.c = [0] * self.a          # short[] srcX
        self.d = [0] * self.a          # short[] srcY
        self.e = [0] * self.a          # byte[] w
        self.f = [0] * self.a          # byte[] h
        self.g = [0] * self.a          # byte[] anchorX
        self.h = [0] * self.a          # byte[] anchorY
        for n2 in range(self.a):
            self.c[n2] = self.b[1 + 6 * n2] & 0xFF
            self.d[n2] = self.b[2 + 6 * n2] & 0xFF
            self.e[n2] = _s8(self.b[3 + 6 * n2])
            self.f[n2] = _s8(self.b[4 + 6 * n2])
            self.g[n2] = _s8(self.b[5 + 6 * n2])
            self.h[n2] = _s8(self.b[6 + 6 * n2])

    def a_v(self):  # a.java:35-44
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
