"""FrameReader: reads a frame from the stream.
"""
from pow.game.online.rt import DataInputStream, _js, i32


class FrameReader:

    def __init__(self, input_stream):
        self.stream = None
        self.length = 0
        self.header = [0] * (1024)
        self.stream = DataInputStream(input_stream)
        self.length = (-1)

    def close(self):
        try:
            if self.stream is not None:
                self.stream.close()
            return
        except Exception:
            return

    def read_frame(self):
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
    from pow.game.online.answer import Answer
