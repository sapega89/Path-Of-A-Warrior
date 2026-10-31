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
    "F13": True,  # ag.y(): start position written to cz.a[1] while the map reads cz.a[0]
    "F14": True,  # c.i(): `k = aw[i]` read before the wall check -> aw[-1]; step with ar.c()'s new direction
    "F15": True,  # ag.a(byte[],int) "(..)" macro: chained `i2[1] = i3[1] = a(..,')')` decompiled as two calls
    "F16": True,  # c.b(4 ints): enemy start position written to ex.a[1] while ar reads ex.a[0] (fresh slot)
    "F17": True,  # lost parentheses: c.a(5 ints) room index `(ce+4)/7 * (W/7)`, c.a(int) rooms `(W/7) * (H/7)`
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

# PORT-EXTRA (debug / tests): POW_NO_ENEMIES=1 = the map without enemies (rooms with a general
# stay closed), POW_NO_COMBAT=1 = the attack / skill / potion keys do nothing on the map.
# Both off by default: the game has its combat (phase 4).
NO_ENEMIES = os.environ.get("POW_NO_ENEMIES", "0") == "1"
NO_COMBAT = os.environ.get("POW_NO_COMBAT", "0") == "1"

# PORT-EXTRA (PC controls): the hero walks only while a direction key / the mouse button is
# held (the phone had no key release: a tap started walking and the next tap stopped).
# POW_HOLD_TO_MOVE=0 = the phone way. tools/shot.py uses 0 (scenarios press keys like a phone).
HOLD_TO_MOVE = os.environ.get("POW_HOLD_TO_MOVE", "1") == "1"

# PORT-EXTRA (temporary, asked by the player): the Normal-difficulty auto-aim (ar.f(): before a hit
# the hero turns to the nearest enemy) also on Hard. Gold and EXP of Hard stay as they are.
# POW_AUTO_AIM_HARD=0 = the original (no auto-aim on Hard). tools/shot.py uses 0.
AUTO_AIM_HARD = os.environ.get("POW_AUTO_AIM_HARD", "1") == "1"

# PORT-EXTRA: POW_CHEAT=1 turns on the original developers' cheat, the JAD/manifest property
# GAMEVIL_CHEAT: TRUE (ag.java:626, ag.bi): loading a save sets gold to 555000 (ag.java:2179);
# a new hero gets 500000 gold, 2000 in every stat and all skills (ag.java:916, 3260).
CHEAT = os.environ.get("POW_CHEAT", "0") == "1"
# PORT-EXTRA: POW_GOLD=N - after a save is loaded the hero has N gold (nothing else changes).
GOLD = int(os.environ["POW_GOLD"]) if os.environ.get("POW_GOLD", "").isdigit() else None
