"""Image.createImage for the MP jar: same as pow.midp.graphics.Image, but a resource path is
read from the MP resources (config.MP_RES_ROOT)."""
from pow.midp.graphics import Image as _Image
from pow.game.online.res_reader import ResReader


class Image(_Image):
    __slots__ = ()

    @staticmethod
    def createImage(*args):
        if len(args) == 1 and isinstance(args[0], str):
            data = ResReader.read(args[0])
            if data is None:
                raise OSError("resource not found: " + args[0])
            return _Image.createImage(bytes(x & 0xFF for x in data), 0, len(data))
        if len(args) == 3 and isinstance(args[0], list):
            data = bytes(x & 0xFF for x in args[0])
            return _Image.createImage(data, args[1], args[2])
        return _Image.createImage(*args)
