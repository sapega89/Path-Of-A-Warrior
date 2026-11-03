"""j.java - resource reader. Literal port."""
from pow.midp import resources


class ResReader:
    @staticmethod
    def read(path):  # j.java:4-19
        # getResourceAsStream + read loop; on any exception returns null
        data = resources.read(path)
        return None if data is None else bytearray(data)
