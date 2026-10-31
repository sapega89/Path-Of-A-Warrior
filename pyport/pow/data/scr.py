"""Stand-alone .scr loader (PHASE_0 task 0.5) for tools/tests - same rules as al.java:11-31.

Format: u16 LE count, then (count+1) x u16 LE offsets, then UTF-8 bytes.
String i = bytes[off[i]:off[i+1]]. Empty entries do NOT stop reading.
"""
import pathlib


def load(path) -> list:
    data = pathlib.Path(path).read_bytes()
    count = data[0] | data[1] << 8
    offs = [data[2 + 2 * i] | data[3 + 2 * i] << 8 for i in range(count + 1)]
    return [data[offs[i]:offs[i + 1]].decode("utf-8", errors="replace") for i in range(count)]
