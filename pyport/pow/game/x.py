"""x.java - the single drawing gateway of the game. Literal port.

Every drawing call of the game goes through these static methods.
Overloaded Java names get a signature suffix (see pyport/README.md, tools/java_names.txt).
"""
from pow.midp.jint import i32, ushr32


class x:
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
        x.b = paramGraphics
        x.g = x.b.getClipX()
        x.h = x.b.getClipY()
        x.i = x.b.getClipWidth()
        x.j = x.b.getClipHeight()

    @staticmethod
    def a_IIII(paramInt1, paramInt2, paramInt3, paramInt4):  # x.java:35-45
        x.c = x.g
        x.d = x.h
        x.e = x.i
        x.f = x.j
        x.g = paramInt1
        x.h = paramInt2
        x.i = paramInt3
        x.j = paramInt4
        x.b.clipRect(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def a_v():  # x.java:47-53
        x.g = x.c
        x.h = x.d
        x.i = x.e
        x.j = x.f
        x.b.setClip(x.c, x.d, x.e, x.f)

    @staticmethod
    def a_MII(paramImage, paramInt1, paramInt2):  # x.java:55-57
        x.b.drawImage(paramImage, paramInt1, paramInt2, 20)

    @staticmethod
    def a_MIII(paramImage, paramInt1, paramInt2, paramInt3):  # x.java:59-61
        x.b.drawImage(paramImage, paramInt1, paramInt2, paramInt3)

    @staticmethod
    def a_MIIIIII(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6):  # x.java:63-67
        x.b.clipRect(paramInt1, paramInt2, paramInt3, paramInt4)
        x.b.drawImage(paramImage, paramInt1 - paramInt5, paramInt2 - paramInt6, 20)
        x.b.setClip(x.g, x.h, x.i, x.j)

    @staticmethod
    def a_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:69-72
        x.b.setColor(paramInt5)
        x.b.drawRect(paramInt1, paramInt2, paramInt3 - 1, paramInt4 - 1)

    @staticmethod
    def b_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:74-77
        x.b.setColor(paramInt5)
        x.b.fillRect(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def c_IIIII(paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:79-82
        x.b.setColor(paramInt5)
        x.b.drawLine(paramInt1, paramInt2, paramInt3, paramInt4)

    @staticmethod
    def a_Lg(paramg):  # x.java:84-86
        x.k = paramg

    @staticmethod
    def a_ACIIIII(paramArrayOfchar, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5):  # x.java:88-102
        if (paramInt5 & 0x1) != 0:
            paramInt3 -= x.k.a_ACII(paramArrayOfchar, paramInt1, paramInt2) // 2  # width >= 0: // == Java /
        elif (paramInt5 & 0x8) != 0:
            paramInt3 -= x.k.a_ACII(paramArrayOfchar, paramInt1, paramInt2)
        i = paramInt1 + paramInt2
        j = paramInt3
        for k in range(paramInt1, i):
            c = paramArrayOfchar[k]
            m = x.k.a_C(c)
            x.k.a_CII(c, j, paramInt4)
            j += m

    @staticmethod
    def a_TIII(paramString, paramInt1, paramInt2, paramInt3):  # x.java:104-106
        x.a_ACIIIII(list(paramString), 0, len(paramString), paramInt1, paramInt2, paramInt3)

    @staticmethod
    def b_v():  # x.java:108-122  (CRC-32 table, polynomial 0xEDB88320)
        x.a = [0] * 256
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
            x.a[b] = i

    @staticmethod
    def a_ABII(paramArrayOfbyte, paramInt1, paramInt2):  # x.java:124-129  (CRC-32)
        if x.a is None:
            x.b_v()
        i = -1
        while True:
            paramInt2 -= 1
            if paramInt2 < 0:
                break
            # Java: a[(i ^ bytes[p++]) & 0xFF] ^ i >>> 8 ; the byte is signed but only & 0xFF matters
            i = i32(x.a[(i ^ paramArrayOfbyte[paramInt1]) & 0xFF] ^ ushr32(i, 8))
            paramInt1 += 1
        return (i ^ 0xFFFFFFFF) & 0xFFFFFFFF

    # x.java:131-173: static initializer builds two byte arrays and throws them away (dead code).
