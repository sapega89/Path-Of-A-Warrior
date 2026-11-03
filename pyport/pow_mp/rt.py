"""Runtime of the MP client (code first machine-translated from Java): Java semantics helpers
and the MIDP / java.* pieces the jar uses. Hand-written."""
from pow.midp import system  # noqa: F401
from pow.midp.canvas import Canvas as _Canvas  # noqa: F401
from pow.midp.graphics import Graphics  # noqa: F401
from pow.midp.jint import i8, i16, i32, i64, idiv, imod, ushr32  # noqa: F401
from pow.midp.jrandom import Random  # noqa: F401
from pow.midp.rms import RecordStore  # noqa: F401
from pow_mp.image import Image  # noqa: F401


def _js(*parts):
    """String.valueOf / string concatenation."""
    out = []
    for p in parts:
        if p is None:
            out.append("null")
        elif p is True:
            out.append("true")
        elif p is False:
            out.append("false")
        else:
            out.append(str(p))
    return "".join(out)


def _jtrim(s):
    """String.trim(): strips chars <= ' ' at both ends."""
    a, b = 0, len(s)
    while a < b and s[a] <= " ":
        a += 1
    while b > a and s[b - 1] <= " ":
        b -= 1
    return s[a:b]


def _jstring(data, off=0, ln=None):
    """new String(byte[], off, len) (ISO-8859-1 like the phones)."""
    if isinstance(data, str):
        return data
    if ln is None:
        ln = len(data) - off
    return bytes(x & 0xFF for x in data[off:off + ln]).decode("latin-1")


def _arraycopy(src, sp, dst, dp, n):
    dst[dp:dp + n] = src[sp:sp + n]


def _inc(obj, name, d):
    v = getattr(obj, name) + d
    setattr(obj, name, v)
    return v


def _inc_post(obj, name, d):
    v = getattr(obj, name)
    setattr(obj, name, v + d)
    return v


def _inci(arr, i, d):
    arr[i] += d
    return arr[i]


def _inci_post(arr, i, d):
    v = arr[i]
    arr[i] = v + d
    return v


def _set(obj, name, v):
    setattr(obj, name, v)
    return v


def _seti(arr, i, v):
    arr[i] = v
    return v


class ByteArrayInputStream:
    def __init__(self, data, off=0, ln=None):
        self.data = bytes(x & 0xFF for x in data[off:off + (len(data) - off if ln is None else ln)])
        self.pos = 0

    def close(self):
        pass


class DataInputStream:
    def __init__(self, stream):
        self.s = stream

    def readUTF(self):
        d, p = self.s.data, self.s.pos
        n = d[p] << 8 | d[p + 1]
        if p + 2 + n > len(d):
            raise EOFError("readUTF")
        self.s.pos = p + 2 + n
        return d[p + 2:p + 2 + n].decode("utf-8", "replace")

    def close(self):
        pass




__all__ = [k for k in list(globals()) if not k.startswith("__") and k not in ("_late",)]
