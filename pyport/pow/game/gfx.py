"""x.java - the single drawing gateway of the game. Literal port.

Every drawing call of the game goes through these static methods.
Overloaded Java names get a signature suffix (see pyport/NAMES.md).
"""
from pow.midp.jint import i32, ushr32


class Gfx:
    b = None   # private static Graphics b;          x.java:5
    c = 0      # saved clip x                        x.java:7
    d = 0
    e = 0
    f = 0
    g = 0      # current clip x                      x.java:15
    h = 0
    i = 0
    j = 0
    k = None   # private static g k;  (current font)  x.java:23
    a = None   # static int[] a;      (CRC table)    x.java:25

    @staticmethod
    def a_G(paramGraphics):  # x.java:27-33
        Gfx.b = paramGraphics
        Gfx.g = Gfx.b.getClipX()
        Gfx.h = Gfx.b.getClipY()
        Gfx.i = Gfx.b.getClipWidth()
        Gfx.j = Gfx.b.getClipHeight()

    @staticmethod
    def a_IIII(paramInt1, paramInt2, paramInt3, paramInt4):  # x.java:35-45
        Gfx.c = Gfx.g
        Gfx.d = Gfx.h
        Gfx.e = Gfx.i
        Gfx.f = Gfx.j
        Gfx.g = paramInt1
        Gfx.h = paramInt2
        Gfx.i = paramInt3
        Gfx.j = paramInt4
        Gfx.b.clipRect(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def a_v():  # x.java:47-53
        Gfx.g = Gfx.c
        Gfx.h = Gfx.d
        Gfx.i = Gfx.e
        Gfx.j = Gfx.f
        Gfx.b.setClip(Gfx.c, Gfx.d, Gfx.e, Gfx.f)

    @staticmethod
    def a_MII(paramImage, paramInt1, paramInt2):  # x.java:55-57
        Gfx.b.drawImage(paramImage, paramInt1, paramInt2, 20)

    @staticmethod
    def a_MIII(paramImage, paramInt1, paramInt2, paramInt3):  # x.java:59-61
        Gfx.b.drawImage(paramImage, paramInt1, paramInt2, paramInt3)

    @staticmethod
    def a_MIIIIII(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # x.java:63-67
        Gfx.b.clipRect(paramInt1, paramInt2, paramInt3, paramInt4)
        Gfx.b.drawImage(paramImage, paramInt1 - paramInt5, paramInt2 - paramInt6, 20)
        Gfx.b.setClip(Gfx.g, Gfx.h, Gfx.i, Gfx.j)

    @staticmethod
    def a_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:69-72
        Gfx.b.setColor(paramInt5)
        Gfx.b.drawRect(paramInt1, paramInt2, paramInt3 - 1, paramInt4 - 1)

    @staticmethod
    def b_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:74-77
        Gfx.b.setColor(paramInt5)
        Gfx.b.fillRect(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def c_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:79-82
        Gfx.b.setColor(paramInt5)
        Gfx.b.drawLine(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def a_Lg(paramg):  # x.java:84-86
        Gfx.k = paramg

    @staticmethod
    def a_ACIIIII(paramArrayOfchar, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:88-102
        if (paramInt5 & 0x1) != 0:
            paramInt3 -= Gfx.k.a_ACII(paramArrayOfchar, paramInt1, paramInt2) // 2  # width >= 0: // == Java /
        elif (paramInt5 & 0x8) != 0:
            paramInt3 -= Gfx.k.a_ACII(paramArrayOfchar, paramInt1, paramInt2)
        i = paramInt1 + paramInt2
        j = paramInt3
        for k in range(paramInt1, i):
            c = paramArrayOfchar[k]
            m = Gfx.k.a_C(c)
            Gfx.k.a_CII(c, j, paramInt4)
            j += m

    @staticmethod
    def a_TIII(paramString, paramInt1, paramInt2, paramInt3):  # x.java:104-106
        Gfx.a_ACIIIII(list(paramString), 0, len(paramString), paramInt1, paramInt2, paramInt3)

    @staticmethod
    def b_v():  # x.java:108-122  (CRC-32 table, polynomial 0xEDB88320)
        Gfx.a = [0] * 256
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
            Gfx.a[b] = i

    @staticmethod
    def a_ABII(paramArrayOfbyte, paramInt1, paramInt2):  # x.java:124-129  (CRC-32)
        if Gfx.a is None:
            Gfx.b_v()
        i = -1
        while True:
            paramInt2 -= 1
            if paramInt2 < 0:
                break
            # Java: a[(i ^ bytes[p++]) & 0xFF] ^ i >>> 8 ; the byte is signed but only & 0xFF matters
            i = i32(Gfx.a[(i ^ paramArrayOfbyte[paramInt1]) & 0xFF] ^ ushr32(i, 8))
            paramInt1 += 1
        return (i ^ 0xFFFFFFFF) & 0xFFFFFFFF

    # x.java:131-173: static initializer builds two byte arrays and throws them away (dead code).
