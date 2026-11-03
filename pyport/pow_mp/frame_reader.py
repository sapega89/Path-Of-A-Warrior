"""FrameReader (d.java): reads a frame from the stream.

Generated once from pyport/mp_java/d.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import DataInputStream, _js, i32



class FrameReader(object):

    def __init__(self, inputStream):  # d.java:13
        self.stream = None
        self.length = 0
        self.header = [0] * (1024)
        self.stream = DataInputStream(inputStream)
        self.length = (-1)

    def close(self):  # d.java:18
        try:
            if self.stream is not None:
                self.stream.close()
            return
        except Exception:
            return

    def read_frame(self):  # d.java:30
        byArray = None
        self.header[0] = 0
        self.header[1] = 0
        self.stream.read(self.header, 0, 2)
        self.length = (i32((((self.header[0] & 0xFF))) << (0)) | i32((((self.header[1] & 0xFF))) << (8)))
        byArray = [0] * ((self.length - 2))
        self.stream.readFully(byArray, 0, len(byArray))
        print(_js("RECV DATA :  "), end='')
        n2 = 0
        while n2 < len(byArray):
            print(_js(_js(_js(_js(_js(_js(_js("[", n2), "]"), ((byArray[n2] & 0xFF))), "'"), chr(((((32) & 0xFFFF) if (byArray[n2] <= 47) else ((byArray[n2]) & 0xFFFF))))), "' ")), end='')
            n2 = n2 + 1
        print(_js(""))
        k2 = Answer(byArray)
        self.length = (-1)
        return k2


def _static_init():
    pass


def _late_imports():
    global Answer
    from pow_mp.answer import Answer
