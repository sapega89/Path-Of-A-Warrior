"""Gfx (i.java): drawing helpers, clip, text, CRC-32 for the font PLTE patch.

Generated once from pyport/mp_java/i.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import i32, idiv, ushr32



class Gfx(object):
    b = None  # i.java:12 Graphics
    c = 0  # i.java:13 int
    d = 0  # i.java:14 int
    e = 0  # i.java:15 int
    f = 0  # i.java:16 int
    g = None  # i.java:17 j
    a = None  # i.java:18 int[]

    @staticmethod
    def a_G(graphics):  # i.java:20
        Gfx.b = graphics
        Gfx.c = Gfx.b.getClipX()
        Gfx.d = Gfx.b.getClipY()
        Gfx.e = Gfx.b.getClipWidth()
        Gfx.f = Gfx.b.getClipHeight()

    @staticmethod
    def a_MIIIIII(image, n2, n3, n4, n5, n6, n7):  # i.java:28
        Gfx.b.clipRect(n2, n3, n4, n5)
        Gfx.b.drawImage(image, (n2 - n6), (n3 - n7), 20)
        Gfx.b.setClip(Gfx.c, Gfx.d, Gfx.e, Gfx.f)

    @staticmethod
    def a_IIIII(n2, n3, n4, n5, n6):  # i.java:34
        Gfx.b.setColor(n6)
        Gfx.b.fillRect(n2, n3, n4, n5)

    @staticmethod
    def a_Lj(j2):  # i.java:39
        Gfx.g = j2

    @staticmethod
    def a_ACIIIII(cArray, n2, n3, n4, n5, n6):  # i.java:43
        if ((n6 & 1)) != 0:
            n4 = (n4 - idiv(Gfx.g.a_ACII(cArray, n2, n3), 2))
        elif ((n6 & 8)) != 0:
            n4 = (n4 - Gfx.g.a_ACII(cArray, n2, n3))
        n7 = (n2 + n3)
        n8 = n4
        n9 = n2
        while n9 < n7:
            c2 = cArray[n9]
            n10 = Gfx.g.a_C(c2)
            Gfx.g.a_CII(c2, n8, n5)
            n8 = (n8 + n10)
            n9 = n9 + 1

    @staticmethod
    def a_TIII(string, n2, n3, n4):  # i.java:61
        Gfx.a_ACIIIII([ord(_c) for _c in string], 0, len(string), n2, n3, n4)

    @staticmethod
    def a_GTIII(graphics, string, n2, n3, n4):  # i.java:65
        graphics2 = Gfx.b
        Gfx.b = graphics
        Gfx.a_ACIIIII([ord(_c) for _c in string], 0, len(string), n2, n3, n4)
        Gfx.b = graphics2

    @staticmethod
    def a_v():  # i.java:72
        Gfx.a = [0] * (256)
        n2 = 0
        while n2 < 256:
            n3 = n2
            n4 = 8
            while (n4 := i32(n4 + -1)) >= 0:
                if ((n3 & 1)) != 0:
                    n3 = (-306674912 ^ ushr32(n3, 1))
                    continue
                n3 = ushr32(n3, 1)
            Gfx.a[n2] = n3
            n2 = n2 + 1

    @staticmethod
    def a_ABII(byArray, n2, n3):  # i.java:90
        if Gfx.a is None:
            Gfx.a_v()
        n4 = (-1)
        while (n3 := i32(n3 + -1)) >= 0:
            n4 = (Gfx.a[(((n4 ^ byArray[((n2 := i32(n2 + 1)) - 1)])) & 0xFF)] ^ ushr32(n4, 8))
        return (((~n4)) & 0xFFFFFFFF)


def _static_init():
    byArray = [(-119), 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82, 0, 0, 0, 0, 0, 0, 0, 0, 8, 3, 0, 0, 0]
    byArray2 = [0, 0, 0, 0, 73, 69, 78, 68, (-82), 66, 96, (-126)]


def _late_imports():
    global Draw, Font, FrameWriter, FrameReader, MpCanvas
    from pow_mp.draw import Draw
    from pow_mp.font import Font
    from pow_mp.frame_writer import FrameWriter
    from pow_mp.frame_reader import FrameReader
    from pow_mp.mp_canvas import MpCanvas
