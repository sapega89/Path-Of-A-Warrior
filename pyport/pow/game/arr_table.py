"""d.java - fixed-width data table (.arr: kibo, sungbo, shinki, ...). Literal port."""
from pow.game.res_reader import ResReader


class ArrTable:
    def __init__(self, paramString):  # d.java:12-34
        self.widths = None   # column widths
        self.offsets = None   # column offsets (stored as byte, read with & 0xFF)
        self.rows = None   # rows
        self.row_size = 0      # row size
        try:
            data = ResReader.read(paramString)
            i = data[0]
            self.widths = bytearray(data[1:1 + i])
            self.offsets = bytearray(i)
            self.rows = bytearray(data[1 + i:])
            k = 0
            for b in range(i):
                self.offsets[b] = k & 0xFF
                k += self.widths[b] & 0xFF
            self.row_size = k
        except Exception:
            return

    def get_int(self, paramInt1, paramInt2):  # d.java:36-45  (little-endian unsigned cell)
        i = 0
        try:
            j_ = self.widths[paramInt2] & 0xFF
            k = paramInt1 * self.row_size + (self.offsets[paramInt2] & 0xFF)
            if k < 0 or paramInt2 < 0 or paramInt1 < 0:
                raise IndexError  # Java arrays throw on negative indices
            for b in range(j_):
                i |= (self.rows[k + b] & 0xFF) << b * 8
        except Exception:
            pass
        return i

    def get_string(self, paramInt1, paramInt2):  # d.java:47-49
        off = paramInt1 * self.row_size + (self.offsets[paramInt2] & 0xFF)
        return bytes(self.rows[off:off + (self.widths[paramInt2] & 0xFF)]).decode("latin-1").strip(_TRIM)

    def free(self):  # d.java:51-55
        self.widths = None
        self.offsets = None
        self.rows = None


# Java String.trim() strips every char <= ' ' (the .arr names are padded with '\0', which
# Python's str.strip() keeps and the font draws as '!')
_TRIM = "".join(map(chr, range(33)))
