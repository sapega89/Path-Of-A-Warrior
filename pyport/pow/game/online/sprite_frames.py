"""SP2 sprite frames (the byte version of the single player's SP3).

    u8 n ; n x {u8 srcX, u8 srcY, s8 w, s8 h, s8 anchorX, s8 anchorY}     (06 §5.1)
"""
from pow.game.online.res_reader import ResReader


def _s8(v):
    return v - 256 if v > 127 else v


class SpriteFrames:
    def __init__(self, path):
        self.data = ResReader.read(path)
        self.count = _s8(self.data[0])
        self.src_x = [0] * self.count          # short[] srcX
        self.src_y = [0] * self.count          # short[] srcY
        self.w = [0] * self.count          # byte[] w
        self.h = [0] * self.count          # byte[] h
        self.anchor_x = [0] * self.count          # byte[] anchorX
        self.anchor_y = [0] * self.count          # byte[] anchorY
        for i in range(self.count):
            self.src_x[i] = self.data[1 + 6 * i] & 0xFF
            self.src_y[i] = self.data[2 + 6 * i] & 0xFF
            self.w[i] = _s8(self.data[3 + 6 * i])
            self.h[i] = _s8(self.data[4 + 6 * i])
            self.anchor_x[i] = _s8(self.data[5 + 6 * i])
            self.anchor_y[i] = _s8(self.data[6 + 6 * i])

    def free(self):
        self.data = None
        self.src_x = None
        self.src_y = None
        self.w = None
        self.h = None
        self.anchor_x = None
        self.anchor_y = None
