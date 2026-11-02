"""al.java - string table (.scr) reader. Literal port."""
from pow.game.res_reader import ResReader


def _read_utf(buf: bytes) -> str:
    """DataInputStream.readUTF (modified UTF-8: 2-byte length, then UTF-8)."""
    n = (buf[0] << 8) | buf[1]
    return bytes(buf[2:2 + n]).decode("utf-8", errors="replace")


class ScrTable:
    def __init__(self, paramString):  # al.java:7-9
        self.a = ResReader.a(paramString)

    def a_I(self, paramInt):  # al.java:11-29
        i = 2 + paramInt * 2
        j_ = self.a[i] & 0xFF | (self.a[i + 1] & 0xFF) << 8
        k = self.a[i + 2] & 0xFF | (self.a[i + 3] & 0xFF) << 8
        str_ = None
        try:
            m = k - j_
            arrayOfByte = bytearray(m + 2)
            arrayOfByte[0] = m >> 8 & 0xFF
            arrayOfByte[1] = m & 0xFF
            arrayOfByte[2:2 + m] = self.a[j_:j_ + m]
            if len(self.a[j_:j_ + m]) != m or m < 0:
                raise IndexError  # System.arraycopy bounds
            str_ = _read_utf(arrayOfByte)
        except Exception:
            pass
        return str_

    def a_v(self):  # al.java:31-33
        self.a = None
