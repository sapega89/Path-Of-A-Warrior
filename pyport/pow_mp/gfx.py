"""Gfx (i.java): drawing helpers, clip, text, CRC-32 for the font PLTE patch.

Generated once from pyport/mp_java/i.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import i32, idiv, ushr32



class Gfx(object):
    g = None  # i.java:12 Graphics
    clip_x = 0  # i.java:13 int
    clip_y = 0  # i.java:14 int
    clip_w = 0  # i.java:15 int
    clip_h = 0  # i.java:16 int
    font = None  # i.java:17 j
    crc_table = None  # i.java:18 int[]

    @staticmethod
    def set_graphics(graphics):  # i.java:20
        Gfx.g = graphics
        Gfx.clip_x = Gfx.g.getClipX()
        Gfx.clip_y = Gfx.g.getClipY()
        Gfx.clip_w = Gfx.g.getClipWidth()
        Gfx.clip_h = Gfx.g.getClipHeight()

    @staticmethod
    def draw_image_part(image, n2, n3, n4, n5, n6, n7):  # i.java:28
        Gfx.g.clipRect(n2, n3, n4, n5)
        Gfx.g.drawImage(image, (n2 - n6), (n3 - n7), 20)
        Gfx.g.setClip(Gfx.clip_x, Gfx.clip_y, Gfx.clip_w, Gfx.clip_h)

    @staticmethod
    def fill_rect(n2, n3, n4, n5, n6):  # i.java:34
        Gfx.g.setColor(n6)
        Gfx.g.fillRect(n2, n3, n4, n5)

    @staticmethod
    def set_font(j2):  # i.java:39
        Gfx.font = j2

    @staticmethod
    def draw_chars(cArray, n2, n3, n4, n5, n6):  # i.java:43
        if ((n6 & 1)) != 0:
            n4 = (n4 - idiv(Gfx.font.chars_width(cArray, n2, n3), 2))
        elif ((n6 & 8)) != 0:
            n4 = (n4 - Gfx.font.chars_width(cArray, n2, n3))
        n7 = (n2 + n3)
        n8 = n4
        n9 = n2
        while n9 < n7:
            c2 = cArray[n9]
            n10 = Gfx.font.char_width(c2)
            Gfx.font.draw_char(c2, n8, n5)
            n8 = (n8 + n10)
            n9 = n9 + 1

    @staticmethod
    def draw_string(string, n2, n3, n4):  # i.java:61
        Gfx.draw_chars([ord(_c) for _c in string], 0, len(string), n2, n3, n4)

    @staticmethod
    def draw_string_on(graphics, string, n2, n3, n4):  # i.java:65
        graphics2 = Gfx.g
        Gfx.g = graphics
        Gfx.draw_chars([ord(_c) for _c in string], 0, len(string), n2, n3, n4)
        Gfx.g = graphics2

    @staticmethod
    def make_crc_table():  # i.java:72
        Gfx.crc_table = [0] * (256)
        n2 = 0
        while n2 < 256:
            n3 = n2
            n4 = 8
            while (n4 := i32(n4 + -1)) >= 0:
                if ((n3 & 1)) != 0:
                    n3 = (-306674912 ^ ushr32(n3, 1))
                    continue
                n3 = ushr32(n3, 1)
            Gfx.crc_table[n2] = n3
            n2 = n2 + 1

    @staticmethod
    def crc32(byArray, n2, n3):  # i.java:90
        if Gfx.crc_table is None:
            Gfx.make_crc_table()
        n4 = (-1)
        while (n3 := i32(n3 + -1)) >= 0:
            n4 = (Gfx.crc_table[(((n4 ^ byArray[((n2 := i32(n2 + 1)) - 1)])) & 0xFF)] ^ ushr32(n4, 8))
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
