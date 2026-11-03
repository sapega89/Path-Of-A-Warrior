"""a.java - SP2 sprite frames (the byte version of the single player's SP3). Literal port.

    u8 n ; n x {u8 srcX, u8 srcY, s8 w, s8 h, s8 anchorX, s8 anchorY}     (06 §5.1)
"""
from pow_mp.res_reader import ResReader


def _s8(v):
    return v - 256 if v > 127 else v


class SpriteFrames:
    def __init__(self, string):  # a.java:14-33
        self.data = ResReader.read(string)
        self.count = _s8(self.data[0])
        self.src_x = [0] * self.count          # short[] srcX
        self.src_y = [0] * self.count          # short[] srcY
        self.w = [0] * self.count          # byte[] w
        self.h = [0] * self.count          # byte[] h
        self.anchor_x = [0] * self.count          # byte[] anchorX
        self.anchor_y = [0] * self.count          # byte[] anchorY
        for n2 in range(self.count):
            self.src_x[n2] = self.data[1 + 6 * n2] & 0xFF
            self.src_y[n2] = self.data[2 + 6 * n2] & 0xFF
            self.w[n2] = _s8(self.data[3 + 6 * n2])
            self.h[n2] = _s8(self.data[4 + 6 * n2])
            self.anchor_x[n2] = _s8(self.data[5 + 6 * n2])
            self.anchor_y[n2] = _s8(self.data[6 + 6 * n2])

    def free(self):  # a.java:35-44
        self.data = None
        self.src_x = None
        self.src_y = None
        self.w = None
        self.h = None
        self.anchor_x = None
        self.anchor_y = None
