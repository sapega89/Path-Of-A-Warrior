"""FrameWriter (e.java): writes a request frame (same as SP u.java).

Generated once from pyport/mp_java/e.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import _arraycopy, _js, i8, ushr32



class FrameWriter(object):

    def __init__(self, outputStream):  # e.java:15
        self.stream = None
        self.buf = ByteArrayOutputStream()  # noqa: F821 - never constructed: NetThread writes the frames
        self.length = 0
        self.frame = None
        self.unused = [0] * (4)
        self.stream = DataOutputStream(outputStream)  # noqa: F821
        self.unused[0] = 0
        self.unused[1] = 1
        self.unused[2] = 117
        self.unused[3] = 126

    def close(self):  # e.java:23
        try:
            if self.buf is not None:
                self.buf.close()
            if self.stream is not None:
                self.stream.close()
            return
        except Exception:
            return

    def write_short(self, n2):  # e.java:38
        self.buf.write(i8(((ushr32(n2, 0) & 0xFF))))
        self.buf.write(i8(((ushr32(n2, 8) & 0xFF))))

    def write_byte(self, by):  # e.java:43
        self.buf.write(by)

    def write_int(self, n2):  # e.java:47
        self.buf.write(i8(((ushr32(n2, 0) & 0xFF))))
        self.buf.write(i8(((ushr32(n2, 8) & 0xFF))))
        self.buf.write(i8(((ushr32(n2, 16) & 0xFF))))
        self.buf.write(i8(((ushr32(n2, 24) & 0xFF))))

    def write_string(self, string, n2):  # e.java:54
        byArray = bytearray(string.encode('latin-1', 'replace'))
        n3 = 0
        while n3 < n2:
            if n3 < len(byArray):
                self.buf.write(byArray[n3])
            else:
                self.buf.write(0)
            n3 = n3 + 1

    def send(self):  # e.java:67
        try:
            n2 = 0
            byArray = self.buf.toByteArray()
            self.buf.reset()
            self.length = len(byArray)
            n3 = (self.length + 2)
            self.frame = [0] * (n3)
            self.frame[0] = i8(((ushr32(n3, 0) & 0xFF)))
            self.frame[1] = i8(((ushr32(n3, 8) & 0xFF)))
            _arraycopy(byArray, 0, self.frame, 2, self.length)
            n2 = (2 + self.length)
            self.stream.write(self.frame, 0, n2)
            self.stream.flush()
            print(_js("SEND DATA :  "), end='')
            n4 = 0
            while n4 < n2:
                print(_js(_js(_js(_js(_js(_js(_js("[", n4), "]"), ((self.frame[n4] & 0xFF))), "'"), chr(((((32) & 0xFFFF) if (self.frame[n4] == 0) else ((self.frame[n4]) & 0xFFFF))))), "' ")), end='')
                n4 = n4 + 1
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
    from pow_mp.frame_reader import FrameReader
