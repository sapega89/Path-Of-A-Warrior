"""FrameWriter: writes a request frame.
"""
from pow.game.online.rt import _arraycopy, _js, i8, ushr32


class FrameWriter:

    def __init__(self, output_stream):
        self.stream = None
        self.buf = ByteArrayOutputStream()  # noqa: F821 - never constructed: NetThread writes the frames
        self.length = 0
        self.frame = None
        self.unused = [0] * (4)
        self.stream = DataOutputStream(output_stream)  # noqa: F821
        self.unused[0] = 0
        self.unused[1] = 1
        self.unused[2] = 117
        self.unused[3] = 126

    def close(self):
        try:
            if self.buf is not None:
                self.buf.close()
            if self.stream is not None:
                self.stream.close()
            return
        except Exception:
            return

    def write_short(self, value):
        self.buf.write(i8(ushr32(value, 0) & 0xFF))
        self.buf.write(i8(ushr32(value, 8) & 0xFF))

    def write_byte(self, value):
        self.buf.write(value)

    def write_int(self, value):
        self.buf.write(i8(ushr32(value, 0) & 0xFF))
        self.buf.write(i8(ushr32(value, 8) & 0xFF))
        self.buf.write(i8(ushr32(value, 16) & 0xFF))
        self.buf.write(i8(ushr32(value, 24) & 0xFF))

    def write_string(self, text, size):
        raw = bytearray(text.encode("latin-1", "replace"))
        i = 0
        while i < size:
            if i < len(raw):
                self.buf.write(raw[i])
            else:
                self.buf.write(0)
            i = i + 1

    def send(self):
        try:
            sent = 0
            body = self.buf.toByteArray()
            self.buf.reset()
            self.length = len(body)
            frame_len = (self.length + 2)
            self.frame = [0] * (frame_len)
            self.frame[0] = i8(ushr32(frame_len, 0) & 0xFF)
            self.frame[1] = i8(ushr32(frame_len, 8) & 0xFF)
            _arraycopy(body, 0, self.frame, 2, self.length)
            sent = (2 + self.length)
            self.stream.write(self.frame, 0, sent)
            self.stream.flush()
            print(_js("SEND DATA :  "), end="")
            i = 0
            while i < sent:
                print(_js(_js(_js(_js(_js(_js(_js("[", i), "]"), (self.frame[i] & 0xFF)), "'"), chr(((32) & 0xFFFF) if (self.frame[i] == 0) else ((self.frame[i]) & 0xFFFF))), "' ")), end="")
                i = i + 1
            print(_js(""))
            self.length = 0
            self.frame = None
            return
        except Exception:
            return


def _static_init():
    pass


def _late_imports():
    global FrameReader
    from pow.game.online.frame_reader import FrameReader
