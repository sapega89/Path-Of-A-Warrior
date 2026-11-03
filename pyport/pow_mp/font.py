"""Font (j.java): the bitmap font 0_font.png, recoloured by a PLTE patch.

Generated once from pyport/mp_java/j.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import Image, _js, i8



class Font(object):

    def __init__(self, path, glyph_w, glyph_h, space_w, color):  # j.java:16
        self.image = None
        self.glyph_w = 0
        self.glyph_h = 0
        self.space_w = 0
        self.plte_offset = 0
        self.glyph_w = glyph_w
        self.glyph_h = glyph_h
        self.space_w = space_w
        try:
            png = ResReader.read(path)
            red = i8((((color >> 16) & 0xFF)))
            green = i8((((color >> 8) & 0xFF)))
            blue = i8(((color & 0xFF)))
            i = 0
            while i < 100:
                if (((png[i] == 80) and (png[(i + 1)] == 76)) and (png[(i + 2)] == 84)) and (png[(i + 3)] == 69):
                    self.plte_offset = i
                    break
                i = i + 1
            if ((png[(self.plte_offset + 4)] != red) or (png[(self.plte_offset + 5)] != green)) or (png[(self.plte_offset + 6)] != blue):
                png[(self.plte_offset + 4)] = red
                png[(self.plte_offset + 5)] = green
                png[(self.plte_offset + 6)] = blue
                crc = Gfx.crc32(png, self.plte_offset, 10)
                png[(self.plte_offset + 10)] = i8((((crc >> 24) & 0xFF)))
                png[(self.plte_offset + 11)] = i8((((crc >> 16) & 0xFF)))
                png[(self.plte_offset + 12)] = i8((((crc >> 8) & 0xFF)))
                png[(self.plte_offset + 13)] = i8(((crc & 0xFF)))
            self.image = Image.createImage(png, 0, len(png))
            return
        except Exception:
            print(_js(_js("font fail : ", path)))
            return

    def draw_char(self, ch, x, y):  # j.java:53
        if ch == 32:
            return
        Gfx.draw_image_part(self.image, x, y, self.glyph_w, self.glyph_h, (Font.glyph_index(ch) * self.glyph_w), 0)

    @staticmethod
    def glyph_index(ch):  # j.java:60
        index = 0
        if (ch >= 65) and (ch <= 90):
            index = (32 + ((ch - 65)))
        elif (ch >= 97) and (ch <= 122):
            index = (64 + ((ch - 97)))
        elif (ch >= 48) and (ch <= 57):
            index = (15 + ((ch - 48)))
        elif ch == 33:
            index = 0
        elif ch == 34:
            index = 1
        elif ch == 35:
            index = 2
        elif ch == 36:
            index = 3
        elif ch == 37:
            index = 4
        elif ch == 38:
            index = 5
        elif ch == 39:
            index = 6
        elif ch == 40:
            index = 7
        elif ch == 41:
            index = 8
        elif ch == 42:
            index = 9
        elif ch == 43:
            index = 10
        elif ch == 44:
            index = 11
        elif ch == 45:
            index = 12
        elif ch == 46:
            index = 13
        elif ch == 47:
            index = 14
        elif ch == 58:
            index = 25
        elif ch == 59:
            index = 26
        elif ch == 60:
            index = 27
        elif ch == 61:
            index = 28
        elif ch == 62:
            index = 29
        elif ch == 63:
            index = 30
        elif ch == 64:
            index = 31
        elif ch == 91:
            index = 58
        elif ch == 93:
            index = 60
        elif ch == 94:
            index = 61
        elif ch == 95:
            index = 62
        elif ch == 96:
            index = 63
        elif ch == 123:
            index = 90
        elif ch == 124:
            index = 91
        elif ch == 125:
            index = 92
        elif ch == 126:
            index = 93
        elif ch == 32:
            index = 99
        return index

    def char_width(self, ch):  # j.java:136
        if ch == 32:
            return self.space_w
        return ((self.glyph_w + 1) - 0)

    def chars_width(self, chars, start, count):  # j.java:143
        width = 0
        end = (start + count)
        i = start
        while i < end:
            width = (width + self.char_width(chars[i]))
            i = i + 1
        return width

    def string_width(self, text):  # j.java:154
        chars = [ord(_c) for _c in text]
        return self.chars_width(chars, 0, len(chars))


def _static_init():
    pass


def _late_imports():
    global ResReader, Gfx, FrameWriter, FrameReader
    from pow_mp.res_reader import ResReader
    from pow_mp.gfx import Gfx
    from pow_mp.frame_writer import FrameWriter
    from pow_mp.frame_reader import FrameReader
