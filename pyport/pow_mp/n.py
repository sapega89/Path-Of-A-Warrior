"""n.java - resource reader of the MP jar. Literal port; reads from config.MP_RES_ROOT."""
import pathlib

import config


class n:
    @staticmethod
    def a(paramString):  # n.java:8-25
        try:
            with open(pathlib.Path(config.MP_RES_ROOT) / paramString.lstrip("/"), "rb") as fh:
                return bytearray(fh.read())
        except OSError as ex:
            print("fail to read " + paramString + " e:" + str(ex))
            return None
