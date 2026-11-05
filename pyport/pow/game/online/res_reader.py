"""Resource reader of the multiplayer; reads from config.MP_RES_ROOT.

Returns a list of signed bytes (-128..127)."""
import pathlib

import config


class ResReader:
    @staticmethod
    def read(paramString):
        try:
            with open(pathlib.Path(config.MP_RES_ROOT) / paramString.lstrip("/"), "rb") as fh:
                return [b - 256 if b > 127 else b for b in fh.read()]
        except OSError as ex:
            print("fail to read " + paramString + " e:" + str(ex))
            return None
