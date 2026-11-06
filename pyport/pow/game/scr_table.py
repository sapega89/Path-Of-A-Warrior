"""String table (.scr) reader."""
from pow.game.res_reader import ResReader


def _read_utf(buf: bytes) -> str:
    """DataInputStream.readUTF (modified UTF-8: 2-byte length, then UTF-8)."""
    n = (buf[0] << 8) | buf[1]
    return bytes(buf[2:2 + n]).decode("utf-8", errors="replace")


class ScrTable:
    def __init__(self, path):
        self.data = ResReader.read(path)

    def get(self, index):
        i = 2 + index * 2
        start = self.data[i] & 0xFF | (self.data[i + 1] & 0xFF) << 8
        end = self.data[i + 2] & 0xFF | (self.data[i + 3] & 0xFF) << 8
        str_ = None
        try:
            size = end - start
            utf = bytearray(size + 2)
            utf[0] = size >> 8 & 0xFF
            utf[1] = size & 0xFF
            utf[2:2 + size] = self.data[start:start + size]
            if len(self.data[start:start + size]) != size or size < 0:
                raise IndexError  # System.arraycopy bounds
            str_ = _read_utf(utf)
        except Exception:
            pass
        return str_

    def free(self):
        self.data = None
