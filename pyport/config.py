"""Settings of the Python port (spike version; registry of flags = PHASE_1 task 1.8)."""
import os
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# Where the original resources (PNG, .scr, .arr, ...) are read from.
# Desktop: the repository root (pyport/..). Browser build: assets are copied next to main.py.
RES_ROOT = os.environ.get("POW_RES_ROOT") or (
    str(HERE.parent) if (HERE.parent / "0_font.png").exists() else str(HERE / "res")
)

# Phone screen (QVGA) and integer window scale (nearest neighbour).
SCREEN_W = 240
SCREEN_H = 320
SCALE = int(os.environ.get("POW_SCALE", "2"))  # 2 -> 480x640, 3 -> 720x960

# Where RecordStores are written on the desktop (browser uses localStorage).
SAVE_DIR = os.environ.get("POW_SAVE_DIR") or str(pathlib.Path.home() / ".path_of_a_warrior")

# Decompiler artifacts fixed on purpose (PHASE_1 §3). True = fixed (default).
DECOMP_FIX = {
    "F6": True,  # e.java menu navigation: `cM[1]=cM[1]+1; if (cM[1]+1 >= cN)` -> `if (++cM[1] >= cN)`
    "F8": True,  # ag.L(): switch cases without break -> separate branches (always on, no literal mode)
    "F9": True,  # l.a(String): `s = s + 1; l[s] = ...` -> `l[s++] = ...` (proposed, see pyport/README.md)
    "F10": True,  # lost parentheses `a * b % c` -> `a * (b % c)`: ag.f(int,int) name grid, ag.a(..Image..) digits
    "F12": True,  # ag.h(int,int,int) gold amount: mangled do/continue loop never draws a digit
    "F11": True,  # e.T(int) stat cursor: decompiled `a(.., bool, bool, bool)` = colour 0x010101 -> 255,255,255
}

# Re-raise exceptions inside the game loop (Java would print "--run:" and continue).
DEBUG = os.environ.get("POW_DEBUG", "1") == "1"

# NotPorted (a screen of a later phase): True = crash, False = popup + back to the menu.
STRICT = os.environ.get("POW_STRICT", "0") == "1"

# SPIKE-ONLY: create a minimal save on first start so Continue opens the Game Menu without
# going through New Game. Off by default since hero creation is ported; POW_DEMO_SAVE=1 or
# main.py --demo turns it on.
DEMO_SAVE = os.environ.get("POW_DEMO_SAVE", "0") == "1"
