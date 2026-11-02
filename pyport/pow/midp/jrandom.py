"""java.util.Random - exact 48-bit LCG (spike: nextInt/nextInt(n); full tests = PHASE_1 1.3)."""
import os
import time

from pow.midp.jint import i32

_MULT = 0x5DEECE66D
_MASK = (1 << 48) - 1


class Random:
    _uniq = 8682522807148012

    def __init__(self, seed=None):
        if seed is None:
            Random._uniq = (Random._uniq * 181783497276652981) & 0xFFFFFFFFFFFFFFFF
            # PORT-EXTRA (tests): POW_SEED replaces the clock, so the headless scenarios
            # (tools/shot.py sets it to 1) give the same enemies and hits on every run
            fixed = os.environ.get("POW_SEED")
            seed = Random._uniq ^ (int(fixed) if fixed else time.time_ns())
        self.setSeed(seed)

    def setSeed(self, seed):
        self.seed = (seed ^ _MULT) & _MASK

    def next(self, bits):
        self.seed = (self.seed * _MULT + 0xB) & _MASK
        return i32(self.seed >> (48 - bits))

    def nextInt(self, n=None):
        if n is None:
            return self.next(32)
        if n <= 0:
            raise ValueError("n must be positive")
        if (n & -n) == n:
            return i32((n * (self.next(31) & 0x7FFFFFFF)) >> 31)
        while True:
            bits = self.next(31) & 0x7FFFFFFF
            val = bits % n
            if bits - val + (n - 1) < (1 << 31):
                return val
