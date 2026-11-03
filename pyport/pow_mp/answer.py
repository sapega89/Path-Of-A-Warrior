"""Answer (k.java): one server answer, read field by field (little-endian).

Generated once from pyport/mp_java/k.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import _inc_post, _jstring, _jtrim, i16, i32



class Answer:

    def __init__(self, data):  # k.java:8
        self.data = None
        self.pos = 0
        self.data = data

    def read_s8(self):  # k.java:12
        return self.data[_inc_post(self, 'pos', 1)]

    def read_s16(self):  # k.java:16
        lo = self.data[_inc_post(self, 'pos', 1)]
        hi = self.data[_inc_post(self, 'pos', 1)]
        return i16(i32((((lo & 0xFF))) << (0)) | i32((((hi & 0xFF))) << (8)))

    def read_s32(self):  # k.java:22
        b0 = self.data[_inc_post(self, 'pos', 1)]
        b1 = self.data[_inc_post(self, 'pos', 1)]
        b2 = self.data[_inc_post(self, 'pos', 1)]
        b3 = self.data[_inc_post(self, 'pos', 1)]
        return (((i32((((b0 & 0xFF))) << (0)) | i32((((b1 & 0xFF))) << (8))) | i32((((b2 & 0xFF))) << (16))) | i32((((b3 & 0xFF))) << (24)))

    def read_string(self, size):  # k.java:30
        if self.data[self.pos] == 0:
            self.pos = (self.pos + size)
            return ""
        length = 0
        while length < size:
            if self.data[(self.pos + length)] == 0:
                break
            length = length + 1
        text = _jstring(self.data, self.pos, length)
        self.pos = (self.pos + size)
        return _jtrim(text)


def _static_init():
    pass


def _late_imports():
    pass
