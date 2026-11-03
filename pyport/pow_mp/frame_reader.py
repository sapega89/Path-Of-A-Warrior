"""FrameReader (d.java): reads a frame from the stream.

Generated once from pyport/mp_java/d.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import DataInputStream, _js, i32



class FrameReader(object):

    def __init__(self, inputStream):  # d.java:13
        self.a = None
        self.b = 0
        self.c = [0] * (1024)
        self.a = DataInputStream(inputStream)
        self.b = (-1)

    def a_v(self):  # d.java:18
        try:
            if self.a is not None:
                self.a.close()
            return
        except Exception:
            return

    def b_v(self):  # d.java:30
        byArray = None
        self.c[0] = 0
        self.c[1] = 0
        self.a.read(self.c, 0, 2)
        self.b = (i32((((self.c[0] & 0xFF))) << (0)) | i32((((self.c[1] & 0xFF))) << (8)))
        byArray = [0] * ((self.b - 2))
        self.a.readFully(byArray, 0, len(byArray))
        print(_js("RECV DATA :  "), end='')
        n2 = 0
        while n2 < len(byArray):
            print(_js(_js(_js(_js(_js(_js(_js("[", n2), "]"), ((byArray[n2] & 0xFF))), "'"), chr(((((32) & 0xFFFF) if (byArray[n2] <= 47) else ((byArray[n2]) & 0xFFFF))))), "' ")), end='')
            n2 = n2 + 1
        print(_js(""))
        k2 = Answer(byArray)
        self.b = (-1)
        return k2


def _static_init():
    pass


def _late_imports():
    global Answer
    from pow_mp.answer import Answer
