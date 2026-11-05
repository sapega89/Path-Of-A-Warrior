"""n.java - resource reader of the MP jar. Literal port; reads from config.MP_RES_ROOT.

Returns a Java byte[]: a list of signed bytes (-128..127), so the generated code can store
(byte) values into it (j.java patches the font palette)."""
import pathlib

import config


class ResReader:
    @staticmethod
    def read(paramString):  # n.java:8-25
        try:
            with open(pathlib.Path(config.MP_RES_ROOT) / paramString.lstrip("/"), "rb") as fh:
                return [b - 256 if b > 127 else b for b in fh.read()]
        except OSError as ex:
            print("fail to read " + paramString + " e:" + str(ex))
            return None
