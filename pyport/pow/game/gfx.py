"""x.java - the single drawing gateway of the game. Literal port.

Every drawing call of the game goes through these static methods.
Overloaded Java names get a signature suffix (see pyport/NAMES.md).
"""
from pow.midp.jint import i32, ushr32


class Gfx:
    g = None   # private static Graphics b;          x.java:5
    saved_clip_x = 0      # saved clip x                        x.java:7
    saved_clip_y = 0
    saved_clip_w = 0
    saved_clip_h = 0
    clip_x = 0      # current clip x                      x.java:15
    clip_y = 0
    clip_w = 0
    clip_h = 0
    font = None   # private static g k;  (current font)  x.java:23
    crc_table = None   # static int[] a;      (CRC table)    x.java:25

    @staticmethod
    def a_G(paramGraphics):  # x.java:27-33
        Gfx.g = paramGraphics
        Gfx.clip_x = Gfx.g.getClipX()
        Gfx.clip_y = Gfx.g.getClipY()
        Gfx.clip_w = Gfx.g.getClipWidth()
        Gfx.clip_h = Gfx.g.getClipHeight()

    @staticmethod
    def a_IIII(paramInt1, paramInt2, paramInt3, paramInt4):  # x.java:35-45
        Gfx.saved_clip_x = Gfx.clip_x
        Gfx.saved_clip_y = Gfx.clip_y
        Gfx.saved_clip_w = Gfx.clip_w
        Gfx.saved_clip_h = Gfx.clip_h
        Gfx.clip_x = paramInt1
        Gfx.clip_y = paramInt2
        Gfx.clip_w = paramInt3
        Gfx.clip_h = paramInt4
        Gfx.g.clipRect(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def a_v():  # x.java:47-53
        Gfx.clip_x = Gfx.saved_clip_x
        Gfx.clip_y = Gfx.saved_clip_y
        Gfx.clip_w = Gfx.saved_clip_w
        Gfx.clip_h = Gfx.saved_clip_h
        Gfx.g.setClip(Gfx.saved_clip_x, Gfx.saved_clip_y, Gfx.saved_clip_w, Gfx.saved_clip_h)

    @staticmethod
    def a_MII(paramImage, paramInt1, paramInt2):  # x.java:55-57
        Gfx.g.drawImage(paramImage, paramInt1, paramInt2, 20)

    @staticmethod
    def a_MIII(paramImage, paramInt1, paramInt2, paramInt3):  # x.java:59-61
        Gfx.g.drawImage(paramImage, paramInt1, paramInt2, paramInt3)

    @staticmethod
    def a_MIIIIII(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # x.java:63-67
        Gfx.g.clipRect(paramInt1, paramInt2, paramInt3, paramInt4)
        Gfx.g.drawImage(paramImage, paramInt1 - paramInt5, paramInt2 - paramInt6, 20)
        Gfx.g.setClip(Gfx.clip_x, Gfx.clip_y, Gfx.clip_w, Gfx.clip_h)

    @staticmethod
    def a_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:69-72
        Gfx.g.setColor(paramInt5)
        Gfx.g.drawRect(paramInt1, paramInt2, paramInt3 - 1, paramInt4 - 1)

    @staticmethod
    def b_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:74-77
        Gfx.g.setColor(paramInt5)
        Gfx.g.fillRect(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def c_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:79-82
        Gfx.g.setColor(paramInt5)
        Gfx.g.drawLine(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def a_Lg(paramg):  # x.java:84-86
        Gfx.font = paramg

    @staticmethod
    def a_ACIIIII(paramArrayOfchar, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:88-102
        if (paramInt5 & 0x1) != 0:
            paramInt3 -= Gfx.font.a_ACII(paramArrayOfchar, paramInt1, paramInt2) // 2  # width >= 0: // == Java /
        elif (paramInt5 & 0x8) != 0:
            paramInt3 -= Gfx.font.a_ACII(paramArrayOfchar, paramInt1, paramInt2)
        i = paramInt1 + paramInt2
        j = paramInt3
        for k in range(paramInt1, i):
            c = paramArrayOfchar[k]
            m = Gfx.font.a_C(c)
            Gfx.font.a_CII(c, j, paramInt4)
            j += m

    @staticmethod
    def a_TIII(paramString, paramInt1, paramInt2, paramInt3):  # x.java:104-106
        Gfx.a_ACIIIII(list(paramString), 0, len(paramString), paramInt1, paramInt2, paramInt3)

    @staticmethod
    def b_v():  # x.java:108-122  (CRC-32 table, polynomial 0xEDB88320)
        Gfx.crc_table = [0] * 256
        for b in range(256):
            i = b
            b1 = 8
            while True:
                b1 -= 1
                if b1 < 0:
                    break
                if (i & 0x1) != 0:
                    i = i32(0xEDB88320 ^ ushr32(i, 1))
                    continue
                i = ushr32(i, 1)
            Gfx.crc_table[b] = i

    @staticmethod
    def a_ABII(paramArrayOfbyte, paramInt1, paramInt2):  # x.java:124-129  (CRC-32)
        if Gfx.crc_table is None:
            Gfx.b_v()
        i = -1
        while True:
            paramInt2 -= 1
            if paramInt2 < 0:
                break
            # Java: a[(i ^ bytes[p++]) & 0xFF] ^ i >>> 8 ; the byte is signed but only & 0xFF matters
            i = i32(Gfx.crc_table[(i ^ paramArrayOfbyte[paramInt1]) & 0xFF] ^ ushr32(i, 8))
            paramInt1 += 1
        return (i ^ 0xFFFFFFFF) & 0xFFFFFFFF

    # x.java:131-173: static initializer builds two byte arrays and throws them away (dead code).
