"""hang / crash log for the desktop.

If the game loop stops ticking for HANG_SECONDS (an endless loop somewhere in the game code:
the window stops responding and Windows closes it), Python's faulthandler writes the stack of
the stuck code to <SAVE_DIR>/hang.log. A hard crash (segfault inside SDL) and an uncaught
exception are written there too. The log shows the file and line where the game hung.

Off in the browser (no threads there). POW_WATCHDOG=0 turns it off.
"""
import faulthandler
import os
import sys
import time
import traceback

import config

HANG_SECONDS = 10

_file = None
path = None


def start():
    global _file, path
    if _file is not None or sys.platform == "emscripten" or os.environ.get("POW_WATCHDOG", "1") != "1":
        return
    try:
        os.makedirs(config.SAVE_DIR, exist_ok=True)
        path = os.path.join(config.SAVE_DIR, "hang.log")
        _file = open(path, "a", encoding="utf-8")  # noqa: SIM115 (the log stays open for the whole run)
        _file.write("\n=== start {}, Python {} ===\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), sys.version.split()[0]))
        _file.flush()
        faulthandler.enable(file=_file, all_threads=True)
    except Exception as ex:   # never stop the game because of the log
        print("watchdog: off:", ex)
        _file = None


def tick():
    """Called once per game tick: re-arms the hang timer."""
    if _file is not None:
        faulthandler.dump_traceback_later(HANG_SECONDS, repeat=True, file=_file)


def log_exception():
    if _file is not None:
        _file.write("--- exception {} ---\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        traceback.print_exc(file=_file)
        _file.flush()


def stop():
    if _file is not None:
        faulthandler.cancel_dump_traceback_later()
