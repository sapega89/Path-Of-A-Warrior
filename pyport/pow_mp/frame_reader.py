"""FrameReader (d.java): reads a frame from the stream.

Generated once from pyport/mp_java/d.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import DataInputStream, _js, i32


class FrameReader:

    def __init__(self, input_stream):  # d.java:13
        self.stream = None
        self.length = 0
        self.header = [0] * (1024)
        self.stream = DataInputStream(input_stream)
        self.length = (-1)

    def close(self):  # d.java:18
        try:
            if self.stream is not None:
                self.stream.close()
            return
        except Exception:
            return

    def read_frame(self):  # d.java:30
        body = None
        self.header[0] = 0
        self.header[1] = 0
        self.stream.read(self.header, 0, 2)
        self.length = (i32((((self.header[0] & 0xFF))) << (0)) | i32((((self.header[1] & 0xFF))) << (8)))
        body = [0] * (self.length - 2)
        self.stream.readFully(body, 0, len(body))
        print(_js("RECV DATA :  "), end="")
        i = 0
        while i < len(body):
            print(_js(_js(_js(_js(_js(_js(_js("[", i), "]"), (body[i] & 0xFF)), "'"), chr(((32) & 0xFFFF) if (body[i] <= 47) else ((body[i]) & 0xFFFF))), "' ")), end="")
            i = i + 1
        print(_js(""))
        answer = Answer(body)
        self.length = (-1)
        return answer


def _static_init():
    pass


def _late_imports():
    global Answer
    from pow_mp.answer import Answer
