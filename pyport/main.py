"""Entry point for the PC and for the browser (pygbag needs `asyncio.run(main())` here).

    python pyport/main.py            # window 480x640 (POW_SCALE=3 -> 720x960)
    python -m pygbag build/web       # browser, see tools/build_web.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config  # noqa: E402
from pow.midp import display  # noqa: E402


def rms_selftest():
    """Task 0.8: proves that RecordStore survives a restart / page reload.
    Uses its own store, so the game's data is not touched. Look for the line in the
    console (browser: F12): the number must grow by 1 after every reload."""
    from pow.midp.rms import RecordStore
    try:
        rs = RecordStore.openRecordStore("pow_selftest", True)
        if rs.getNumRecords() == 0:
            rs.addRecord(bytearray(4), 0, 4)
        rec = rs.getRecord(1)
        n = int.from_bytes(rec, "little") + 1
        rs.setRecord(1, bytearray(n.to_bytes(4, "little")), 0, 4)
        back = int.from_bytes(RecordStore.openRecordStore("pow_selftest", False).getRecord(1), "little")
        print("RMS selftest: launch #%d, read back %d -> %s (%s)" % (n, back, "OK" if back == n else "FAIL", sys.platform))
    except Exception as ex:
        print("RMS selftest: FAIL", repr(ex))


async def main():
    display.init(headless=os.environ.get("SDL_VIDEODRIVER") == "dummy")
    rms_selftest()
    from pow.game.Main import Main
    midlet = Main()
    await midlet.startApp()


if __name__ == "__main__":
    asyncio.run(main())
