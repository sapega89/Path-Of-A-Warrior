"""Java integer semantics (spike subset; full version = PHASE_1 task 1.2)."""


def i8(x: int) -> int:
    """(byte)x"""
    x &= 0xFF
    return x - 0x100 if x & 0x80 else x


def i16(x: int) -> int:
    """(short)x"""
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x


def i32(x: int) -> int:
    """(int)x"""
    x &= 0xFFFFFFFF
    return x - 0x100000000 if x & 0x80000000 else x


def i64(x: int) -> int:
    """(long)x"""
    x &= 0xFFFFFFFFFFFFFFFF
    return x - 0x10000000000000000 if x & 0x8000000000000000 else x


def idiv(a: int, b: int) -> int:
    """Java int division: truncates toward zero."""
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def imod(a: int, b: int) -> int:
    """Java %: the sign follows the dividend."""
    return a - idiv(a, b) * b


def ushr32(x: int, n: int) -> int:
    """x >>> n for int."""
    return i32((x & 0xFFFFFFFF) >> (n & 31))

