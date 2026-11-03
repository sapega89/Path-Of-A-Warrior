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
    def draw_image_part(image, x, y, w, h, src_x, src_y):  # i.java:28
        Gfx.g.clipRect(x, y, w, h)
        Gfx.g.drawImage(image, (x - src_x), (y - src_y), 20)
        Gfx.g.setClip(Gfx.clip_x, Gfx.clip_y, Gfx.clip_w, Gfx.clip_h)

    @staticmethod
    def fill_rect(x, y, w, h, color):  # i.java:34
        Gfx.g.setColor(color)
        Gfx.g.fillRect(x, y, w, h)

    @staticmethod
    def set_font(font):  # i.java:39
        Gfx.font = font

    @staticmethod
    def draw_chars(chars, start, count, x, y, anchor):  # i.java:43
        if ((anchor & 1)) != 0:
            x = (x - idiv(Gfx.font.chars_width(chars, start, count), 2))
        elif ((anchor & 8)) != 0:
            x = (x - Gfx.font.chars_width(chars, start, count))
        end = (start + count)
        pen_x = x
        i = start
        while i < end:
            ch = chars[i]
            ch_w = Gfx.font.char_width(ch)
            Gfx.font.draw_char(ch, pen_x, y)
            pen_x = (pen_x + ch_w)
            i = i + 1

    @staticmethod
    def draw_string(text, x, y, anchor):  # i.java:61
        Gfx.draw_chars([ord(_c) for _c in text], 0, len(text), x, y, anchor)

    @staticmethod
    def draw_string_on(graphics, text, x, y, anchor):  # i.java:65
        saved_g = Gfx.g
        Gfx.g = graphics
        Gfx.draw_chars([ord(_c) for _c in text], 0, len(text), x, y, anchor)
        Gfx.g = saved_g

    @staticmethod
    def make_crc_table():  # i.java:72
        Gfx.crc_table = [0] * (256)
        i = 0
        while i < 256:
            crc = i
            bit = 8
            while (bit := i32(bit + -1)) >= 0:
                if ((crc & 1)) != 0:
                    crc = (-306674912 ^ ushr32(crc, 1))
                    continue
                crc = ushr32(crc, 1)
            Gfx.crc_table[i] = crc
            i = i + 1

    @staticmethod
    def crc32(data, pos, count):  # i.java:90
        if Gfx.crc_table is None:
            Gfx.make_crc_table()
        crc = (-1)
        while (count := i32(count + -1)) >= 0:
            crc = (Gfx.crc_table[(((crc ^ data[((pos := i32(pos + 1)) - 1)])) & 0xFF)] ^ ushr32(crc, 8))
        return (((~crc)) & 0xFFFFFFFF)


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
