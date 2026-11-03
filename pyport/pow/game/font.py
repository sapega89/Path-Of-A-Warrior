"""g.java - bitmap font (0_font.png). Literal port.

The first palette entry of the PNG is replaced by the wanted colour and the PLTE CRC
is recomputed with x.a(byte[],int,int), exactly as on the phone.
"""
from pow.game.res_reader import ResReader
from pow.game.gfx import Gfx
from pow.midp.graphics import Image


class Font:
    plte_offset = 0  # private static int e = 0;   g.java:12 (offset of "PLTE")

    def __init__(self, path, glyph_w, glyph_h, space_w, color):  # g.java:14-44
        self.image = None          # Image
        self.glyph_w = glyph_w     # glyph width
        self.glyph_h = glyph_h     # glyph height
        self.space_w = space_w     # width of ' '
        try:
            png = ResReader.read(path)
            red = color >> 16 & 0xFF
            green = color >> 8 & 0xFF
            blue = color & 0xFF
            for b in range(100):
                if png[b] == 80 and png[b + 1] == 76 and png[b + 2] == 84 and png[b + 3] == 69:
                    Font.plte_offset = b
                    break
            plte = Font.plte_offset
            if png[plte + 4] != red or png[plte + 5] != green or png[plte + 6] != blue:
                png[plte + 4] = red
                png[plte + 5] = green
                png[plte + 6] = blue
                crc = Gfx.crc32(png, plte, 10)
                png[plte + 10] = crc >> 24 & 0xFF
                png[plte + 11] = crc >> 16 & 0xFF
                png[plte + 12] = crc >> 8 & 0xFF
                png[plte + 13] = crc & 0xFF
            self.image = Image.createImage(png, 0, len(png))
        except Exception:
            return

    def height(self):  # g.java:46-48
        return self.glyph_h

    @staticmethod
    def ascent():  # g.java:50-52
        return 9

    @staticmethod
    def gap():  # g.java:54-56
        return 1

    def draw_char(self, ch, x, y):  # g.java:58-62
        if ch == ' ':
            return
        Gfx.draw_image_part(self.image, x, y, self.glyph_w, self.glyph_h, Font.glyph_index(ch) * self.glyph_w, 0)

    @staticmethod
    def glyph_index(ch):  # g.java:64-138  (glyph index in 0_font.png)
        i = 0
        code = ord(ch)
        if 'A' <= ch <= 'Z':
            i = 32 + code - 65
        elif 'a' <= ch <= 'z':
            i = 64 + code - 97
        elif '0' <= ch <= '9':
            i = 15 + code - 48
        else:
            i = _PUNCT.get(ch, 0)
        return i

    def char_width(self, ch):  # g.java:140-142
        return self.space_w if ch == ' ' else (self.glyph_w + 1 - 0)

    def chars_width(self, chars, start, count):  # g.java:144-150
        i = 0
        end = start + count
        for pos in range(start, end):
            i += self.char_width(chars[pos])
        return i

    def string_width(self, text):  # g.java:152-155
        chars = list(text)
        return self.chars_width(chars, 0, len(chars))


# g.java:71-135 - the if/else chain for punctuation, as a table (same values, same default 0)
_PUNCT = {
    '!': 0, '"': 1, '#': 2, '$': 3, '%': 4, '&': 5, '\'': 6, '(': 7, ')': 8, '*': 9,
    '+': 10, ',': 11, '-': 12, '.': 13, '/': 14, ':': 25, ';': 26, '<': 27, '=': 28,
    '>': 29, '?': 30, '@': 31, '[': 58, ']': 60, '^': 61, '_': 62, '`': 63, '{': 90,
    '|': 91, '}': 92, '~': 93, ' ': 99,
}
