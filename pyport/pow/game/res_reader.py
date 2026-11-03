"""j.java - resource reader. Literal port."""
from pow.midp import resources


class ResReader:
    @staticmethod
    def a(paramString):  # j.java:4-19
        # getResourceAsStream + read loop; on any exception returns null
        data = resources.read(paramString)
        return None if data is None else bytearray(data)
