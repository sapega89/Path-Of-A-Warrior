"""FrameWriter (e.java): writes a request frame (same as SP u.java).

Generated once from pyport/mp_java/e.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import _arraycopy, _js, i8, ushr32



class FrameWriter(object):

    def __init__(self, outputStream):  # e.java:15
        self.a = None
        self.b = ByteArrayOutputStream()  # noqa: F821 - never constructed: NetThread writes the frames
        self.c = 0
        self.d = None
        self.e = [0] * (4)
        self.a = DataOutputStream(outputStream)  # noqa: F821
        self.e[0] = 0
        self.e[1] = 1
        self.e[2] = 117
        self.e[3] = 126

    def a_v(self):  # e.java:23
        try:
            if self.b is not None:
                self.b.close()
            if self.a is not None:
                self.a.close()
            return
        except Exception:
            return

    def a_I(self, n2):  # e.java:38
        self.b.write(i8(((ushr32(n2, 0) & 0xFF))))
        self.b.write(i8(((ushr32(n2, 8) & 0xFF))))

    def a_B(self, by):  # e.java:43
        self.b.write(by)

    def b_I(self, n2):  # e.java:47
        self.b.write(i8(((ushr32(n2, 0) & 0xFF))))
        self.b.write(i8(((ushr32(n2, 8) & 0xFF))))
        self.b.write(i8(((ushr32(n2, 16) & 0xFF))))
        self.b.write(i8(((ushr32(n2, 24) & 0xFF))))

    def a_TI(self, string, n2):  # e.java:54
        byArray = bytearray(string.encode('latin-1', 'replace'))
        n3 = 0
        while n3 < n2:
            if n3 < len(byArray):
                self.b.write(byArray[n3])
            else:
                self.b.write(0)
            n3 = n3 + 1

    def b_v(self):  # e.java:67
        try:
            n2 = 0
            byArray = self.b.toByteArray()
            self.b.reset()
            self.c = len(byArray)
            n3 = (self.c + 2)
            self.d = [0] * (n3)
            self.d[0] = i8(((ushr32(n3, 0) & 0xFF)))
            self.d[1] = i8(((ushr32(n3, 8) & 0xFF)))
            _arraycopy(byArray, 0, self.d, 2, self.c)
            n2 = (2 + self.c)
            self.a.write(self.d, 0, n2)
            self.a.flush()
            print(_js("SEND DATA :  "), end='')
            n4 = 0
            while n4 < n2:
                print(_js(_js(_js(_js(_js(_js(_js("[", n4), "]"), ((self.d[n4] & 0xFF))), "'"), chr(((((32) & 0xFFFF) if (self.d[n4] == 0) else ((self.d[n4]) & 0xFFFF))))), "' ")), end='')
                n4 = n4 + 1
            print(_js(""))
            self.c = 0
            self.d = None
            return
        except Exception:
            return


def _static_init():
    pass


def _late_imports():
    global FrameReader
    from pow_mp.frame_reader import FrameReader
