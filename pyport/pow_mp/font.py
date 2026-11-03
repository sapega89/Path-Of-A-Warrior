"""Font (j.java): the bitmap font 0_font.png, recoloured by a PLTE patch.

Generated once from pyport/mp_java/j.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import Image, _js, i8



class Font(object):

    def __init__(self, string, n2, n3, n4, n5):  # j.java:16
        self.image = None
        self.glyph_w = 0
        self.glyph_h = 0
        self.space_w = 0
        self.plte_offset = 0
        self.glyph_w = n2
        self.glyph_h = n3
        self.space_w = n4
        try:
            byArray = ResReader.read(string)
            by = i8((((n5 >> 16) & 0xFF)))
            by2 = i8((((n5 >> 8) & 0xFF)))
            by3 = i8(((n5 & 0xFF)))
            n6 = 0
            while n6 < 100:
                if (((byArray[n6] == 80) and (byArray[(n6 + 1)] == 76)) and (byArray[(n6 + 2)] == 84)) and (byArray[(n6 + 3)] == 69):
                    self.plte_offset = n6
                    break
                n6 = n6 + 1
            if ((byArray[(self.plte_offset + 4)] != by) or (byArray[(self.plte_offset + 5)] != by2)) or (byArray[(self.plte_offset + 6)] != by3):
                byArray[(self.plte_offset + 4)] = by
                byArray[(self.plte_offset + 5)] = by2
                byArray[(self.plte_offset + 6)] = by3
                l2 = Gfx.crc32(byArray, self.plte_offset, 10)
                byArray[(self.plte_offset + 10)] = i8((((l2 >> 24) & 0xFF)))
                byArray[(self.plte_offset + 11)] = i8((((l2 >> 16) & 0xFF)))
                byArray[(self.plte_offset + 12)] = i8((((l2 >> 8) & 0xFF)))
                byArray[(self.plte_offset + 13)] = i8(((l2 & 0xFF)))
            self.image = Image.createImage(byArray, 0, len(byArray))
            None
            return
        except Exception:
            print(_js(_js("font fail : ", string)))
            return

    def draw_char(self, c2, n2, n3):  # j.java:53
        if c2 == 32:
            return
        Gfx.draw_image_part(self.image, n2, n3, self.glyph_w, self.glyph_h, (Font.glyph_index(c2) * self.glyph_w), 0)

    @staticmethod
    def glyph_index(c2):  # j.java:60
        n2 = 0
        if (c2 >= 65) and (c2 <= 90):
            n2 = (32 + ((c2 - 65)))
        elif (c2 >= 97) and (c2 <= 122):
            n2 = (64 + ((c2 - 97)))
        elif (c2 >= 48) and (c2 <= 57):
            n2 = (15 + ((c2 - 48)))
        elif c2 == 33:
            n2 = 0
        elif c2 == 34:
            n2 = 1
        elif c2 == 35:
            n2 = 2
        elif c2 == 36:
            n2 = 3
        elif c2 == 37:
            n2 = 4
        elif c2 == 38:
            n2 = 5
        elif c2 == 39:
            n2 = 6
        elif c2 == 40:
            n2 = 7
        elif c2 == 41:
            n2 = 8
        elif c2 == 42:
            n2 = 9
        elif c2 == 43:
            n2 = 10
        elif c2 == 44:
            n2 = 11
        elif c2 == 45:
            n2 = 12
        elif c2 == 46:
            n2 = 13
        elif c2 == 47:
            n2 = 14
        elif c2 == 58:
            n2 = 25
        elif c2 == 59:
            n2 = 26
        elif c2 == 60:
            n2 = 27
        elif c2 == 61:
            n2 = 28
        elif c2 == 62:
            n2 = 29
        elif c2 == 63:
            n2 = 30
        elif c2 == 64:
            n2 = 31
        elif c2 == 91:
            n2 = 58
        elif c2 == 93:
            n2 = 60
        elif c2 == 94:
            n2 = 61
        elif c2 == 95:
            n2 = 62
        elif c2 == 96:
            n2 = 63
        elif c2 == 123:
            n2 = 90
        elif c2 == 124:
            n2 = 91
        elif c2 == 125:
            n2 = 92
        elif c2 == 126:
            n2 = 93
        elif c2 == 32:
            n2 = 99
        return n2

    def char_width(self, c2):  # j.java:136
        if c2 == 32:
            return self.space_w
        return ((self.glyph_w + 1) - 0)

    def chars_width(self, cArray, n2, n3):  # j.java:143
        n4 = 0
        n5 = (n2 + n3)
        n6 = n2
        while n6 < n5:
            n4 = (n4 + self.char_width(cArray[n6]))
            n6 = n6 + 1
        return n4

    def string_width(self, string):  # j.java:154
        cArray = [ord(_c) for _c in string]
        return self.chars_width(cArray, 0, len(cArray))


def _static_init():
    pass


def _late_imports():
    global ResReader, Gfx, FrameWriter, FrameReader
    from pow_mp.res_reader import ResReader
    from pow_mp.gfx import Gfx
    from pow_mp.frame_writer import FrameWriter
    from pow_mp.frame_reader import FrameReader
