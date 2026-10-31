"""d.java - fixed-width data table (.arr: kibo, sungbo, shinki, ...). Literal port."""
from pow.game.j import j


class d:
    def __init__(self, paramString):  # d.java:12-34
        self.a = None   # column widths
        self.b = None   # column offsets (stored as byte, read with & 0xFF)
        self.c = None   # rows
        self.d = 0      # row size
        try:
            data = j.a(paramString)
            i = data[0]
            self.a = bytearray(data[1:1 + i])
            self.b = bytearray(i)
            self.c = bytearray(data[1 + i:])
            k = 0
            for b in range(i):
                self.b[b] = k & 0xFF
                k += self.a[b] & 0xFF
            self.d = k
        except Exception:
            return

    def a_II(self, paramInt1, paramInt2):  # d.java:36-45  (little-endian unsigned cell)
        i = 0
        try:
            j_ = self.a[paramInt2] & 0xFF
            k = paramInt1 * self.d + (self.b[paramInt2] & 0xFF)
            if k < 0 or paramInt2 < 0 or paramInt1 < 0:
                raise IndexError  # Java arrays throw on negative indices
            for b in range(j_):
                i |= (self.c[k + b] & 0xFF) << b * 8
        except Exception:
            pass
        return i

    def b_II(self, paramInt1, paramInt2):  # d.java:47-49
        off = paramInt1 * self.d + (self.b[paramInt2] & 0xFF)
        return bytes(self.c[off:off + (self.a[paramInt2] & 0xFF)]).decode("latin-1").strip(_TRIM)

    def a_v(self):  # d.java:51-55
        self.a = None
        self.b = None
        self.c = None


# Java String.trim() strips every char <= ' ' (the .arr names are padded with '\0', which
# Python's str.strip() keeps and the font draws as '!')
_TRIM = "".join(map(chr, range(33)))
