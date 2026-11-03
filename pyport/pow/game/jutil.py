"""Java runtime helpers of the single player (System.arraycopy, (char) of a byte)."""
from pow.midp.jint import i8


def _arraycopy(src, srcPos, dest, destPos, length):
    """System.arraycopy (throws on a negative length or out-of-range, like Java)."""
    if length < 0 or srcPos < 0 or destPos < 0 or srcPos + length > len(src) or destPos + length > len(dest):
        raise IndexError("arraycopy %d %d %d" % (srcPos, destPos, length))
    dest[destPos:destPos + length] = src[srcPos:srcPos + length]


def _jchar(b):
    """(char) of a Java byte: sign-extended to 16 bits."""
    return i8(b) & 0xFFFF
