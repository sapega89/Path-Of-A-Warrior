"""Answer (k.java): one server answer, read field by field (little-endian).

Generated once from pyport/mp_java/k.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import _inc_post, _jstring, _jtrim, i16, i32



class Answer(object):

    def __init__(self, byArray):  # k.java:8
        self.data = None
        self.pos = 0
        self.data = byArray

    def read_s8(self):  # k.java:12
        return self.data[_inc_post(self, 'pos', 1)]

    def read_s16(self):  # k.java:16
        by = self.data[_inc_post(self, 'pos', 1)]
        by2 = self.data[_inc_post(self, 'pos', 1)]
        return i16(((i32((((by & 0xFF))) << (0)) | i32((((by2 & 0xFF))) << (8)))))

    def read_s32(self):  # k.java:22
        by = self.data[_inc_post(self, 'pos', 1)]
        by2 = self.data[_inc_post(self, 'pos', 1)]
        by3 = self.data[_inc_post(self, 'pos', 1)]
        by4 = self.data[_inc_post(self, 'pos', 1)]
        return (((i32((((by & 0xFF))) << (0)) | i32((((by2 & 0xFF))) << (8))) | i32((((by3 & 0xFF))) << (16))) | i32((((by4 & 0xFF))) << (24)))

    def read_string(self, n2):  # k.java:30
        if self.data[self.pos] == 0:
            self.pos = (self.pos + n2)
            return ""
        n3 = 0
        while n3 < n2:
            if self.data[(self.pos + n3)] == 0:
                break
            n3 = n3 + 1
        string = _jstring(self.data, self.pos, n3)
        self.pos = (self.pos + n2)
        return _jtrim(string)


def _static_init():
    pass


def _late_imports():
    pass
