"""g.java - bitmap font (0_font.png). Literal port.

The first palette entry of the PNG is replaced by the wanted colour and the PLTE CRC
is recomputed with x.a(byte[],int,int), exactly as on the phone.
"""
from pow.game.res_reader import ResReader
from pow.game.gfx import Gfx
from pow.midp.graphics import Image


class Font:
    plte_offset = 0  # private static int e = 0;   g.java:12 (offset of "PLTE")

    def __init__(self, paramString, paramInt1, paramInt2, paramInt3, paramInt4):  # g.java:14-44
        self.image = None          # Image
        self.glyph_w = paramInt1     # glyph width
        self.glyph_h = paramInt2     # glyph height
        self.space_w = paramInt3     # width of ' '
        try:
            arrayOfByte = ResReader.a(paramString)
            b1 = paramInt4 >> 16 & 0xFF
            b2 = paramInt4 >> 8 & 0xFF
            b3 = paramInt4 & 0xFF
            for b in range(100):
                if arrayOfByte[b] == 80 and arrayOfByte[b + 1] == 76 and arrayOfByte[b + 2] == 84 and arrayOfByte[b + 3] == 69:
                    Font.plte_offset = b
                    break
            e = Font.plte_offset
            if arrayOfByte[e + 4] != b1 or arrayOfByte[e + 5] != b2 or arrayOfByte[e + 6] != b3:
                arrayOfByte[e + 4] = b1
                arrayOfByte[e + 5] = b2
                arrayOfByte[e + 6] = b3
                l = Gfx.a_ABII(arrayOfByte, e, 10)
                arrayOfByte[e + 10] = l >> 24 & 0xFF
                arrayOfByte[e + 11] = l >> 16 & 0xFF
                arrayOfByte[e + 12] = l >> 8 & 0xFF
                arrayOfByte[e + 13] = l & 0xFF
            self.image = Image.createImage(arrayOfByte, 0, len(arrayOfByte))
        except Exception:
            return

    def a_v(self):  # g.java:46-48
        return self.glyph_h

    @staticmethod
    def b_v():  # g.java:50-52
        return 9

    @staticmethod
    def c_v():  # g.java:54-56
        return 1

    def a_CII(self, paramChar, paramInt1, paramInt2):  # g.java:58-62
        if paramChar == ' ':
            return
        Gfx.a_MIIIIII(self.image, paramInt1, paramInt2, self.glyph_w, self.glyph_h, Font.b_C(paramChar) * self.glyph_w, 0)

    @staticmethod
    def b_C(paramChar):  # g.java:64-138  (glyph index in 0_font.png)
        i = 0
        c = ord(paramChar)
        if 'A' <= paramChar <= 'Z':
            i = 32 + c - 65
        elif 'a' <= paramChar <= 'z':
            i = 64 + c - 97
        elif '0' <= paramChar <= '9':
            i = 15 + c - 48
        else:
            i = _PUNCT.get(paramChar, 0)
        return i

    def a_C(self, paramChar):  # g.java:140-142
        return self.space_w if paramChar == ' ' else (self.glyph_w + 1 - 0)

    def a_ACII(self, paramArrayOfchar, paramInt1, paramInt2):  # g.java:144-150
        i = 0
        j_ = paramInt1 + paramInt2
        for k in range(paramInt1, j_):
            i += self.a_C(paramArrayOfchar[k])
        return i

    def a_T(self, paramString):  # g.java:152-155
        arrayOfChar = list(paramString)
        return self.a_ACII(arrayOfChar, 0, len(arrayOfChar))


# g.java:71-135 - the if/else chain for punctuation, as a table (same values, same default 0)
_PUNCT = {
    '!': 0, '"': 1, '#': 2, '$': 3, '%': 4, '&': 5, '\'': 6, '(': 7, ')': 8, '*': 9,
    '+': 10, ',': 11, '-': 12, '.': 13, '/': 14, ':': 25, ';': 26, '<': 27, '=': 28,
    '>': 29, '?': 30, '@': 31, '[': 58, ']': 60, '^': 61, '_': 62, '`': 63, '{': 90,
    '|': 91, '}': 92, '~': 93, ' ': 99,
}
