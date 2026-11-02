"""System.currentTimeMillis / Thread.sleep with a switchable virtual clock.

Real mode (PC, browser): wall clock.
Virtual mode (headless screenshots, tests): time only moves when sleep() is called,
so a scenario "N ticks" is fully deterministic.
"""
import time

_virtual = False
_now_ms = 0


def use_virtual_clock(start_ms: int = 1_000_000) -> None:
    global _virtual, _now_ms
    _virtual = True
    _now_ms = start_ms


def is_virtual() -> bool:
    return _virtual


def currentTimeMillis() -> int:
    if _virtual:
        return _now_ms
    return int(time.time() * 1000)


def advance(ms: int) -> None:
    """Move the virtual clock (the async loop sleeps for real separately)."""
    global _now_ms
    if _virtual:
        _now_ms += int(ms)


def sleep(ms: int) -> None:
    """Thread.sleep for code outside the main loop (e.g. ag.f(300))."""
    if _virtual:
        advance(ms)
    else:
        time.sleep(ms / 1000.0)
