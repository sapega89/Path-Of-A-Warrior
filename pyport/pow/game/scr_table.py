"""al.java - string table (.scr) reader. Literal port."""
from pow.game.res_reader import ResReader


def _read_utf(buf: bytes) -> str:
    """DataInputStream.readUTF (modified UTF-8: 2-byte length, then UTF-8)."""
    n = (buf[0] << 8) | buf[1]
    return bytes(buf[2:2 + n]).decode("utf-8", errors="replace")


class ScrTable:
    def __init__(self, path):  # al.java:7-9
        self.data = ResReader.read(path)

    def get(self, index):  # al.java:11-29
        i = 2 + index * 2
        j_ = self.data[i] & 0xFF | (self.data[i + 1] & 0xFF) << 8
        k = self.data[i + 2] & 0xFF | (self.data[i + 3] & 0xFF) << 8
        str_ = None
        try:
            m = k - j_
            utf = bytearray(m + 2)
            utf[0] = m >> 8 & 0xFF
            utf[1] = m & 0xFF
            utf[2:2 + m] = self.data[j_:j_ + m]
            if len(self.data[j_:j_ + m]) != m or m < 0:
                raise IndexError  # System.arraycopy bounds
            str_ = _read_utf(utf)
        except Exception:
            pass
        return str_

    def free(self):  # al.java:31-33
        self.data = None
