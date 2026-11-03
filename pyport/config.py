"""Settings of the Python port (spike version; registry of flags = PHASE_1 task 1.8)."""
import os
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# Where the original resources (PNG, .scr, .arr, ...) are read from.
# Desktop: the repository root (pyport/..). Browser build: assets are copied next to main.py.
RES_ROOT = os.environ.get("POW_RES_ROOT") or (
    str(HERE.parent) if (HERE.parent / "0_font.png").exists() else str(HERE / "res")
)

# Multiplayer (PHASE_9): resources of the MP jar, and where its server is.
# POW_MP_SERVER = "local" (the server runs inside the game) or ws(s)://host:port of
# `python -m pow_server`.
MP_RES_ROOT = os.environ.get("POW_MP_RES_ROOT") or (
    str(HERE / "assets_mp") if (HERE / "assets_mp").exists() else str(HERE / "res_mp")
)
MP_SERVER = os.environ.get("POW_MP_SERVER", "local")

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
    "F18": True,  # ar.Z(int): archer's arrow start written to eC.b[1] while ar.j()/ad() fly eC.b[0]
    "F19": True,  # l.e(27) reward popup after an ending: `i = i + 1; l[i] = ...` -> `l[i++] = ...`
    "F20": True,  # as.a(ab) (Gamevil Live): the answer status read into a local, gr never set -> gr = status
    "F11": True,  # e.T(int) stat cursor: decompiled `a(.., bool, bool, bool)` = colour 0x010101 -> 255,255,255
}

# ORIG-BUG: bugs of the original game itself (not of the decompiler), fixed on request. True =
# fixed, False = the original's behaviour. Each place is marked `# ORIG-BUG Bn`.
ORIG_BUG = {
    "B1": True,  # ag.J(id) 3424-3457: Rare items (501-518) read shinki.arr at row id-301 -> 0 stats
    "B2": True,  # ag.Y() level read from the save as a signed byte: Lv128+ comes back negative
    "B3": True,  # e.java 790-801 Visiting with 504 Emperor's Seal: the list fn[2] of all 44 generals
                 # is never filled (visitgen.arr)
    "B4": True,  # as.a(ab) 789 (Gamevil Live Buy into the Warehouse when the backpack is full):
                 # the item is put into cz.Y anyway, past slot 24 -> it goes into the Warehouse
    "B5": True,  # m.bp() Gamevil Live registration: 3 frames after CONFIRM "Network connection has
                 # failed" replaces the answer of the 531 -> the answer stops that count
}

# Gamevil Live of the single player (pow_server/live.py): "local" = the server inside the game
# (shares the accounts of the in-game multiplayer server), or ws(s)://host:28200/live.
LIVE_SERVER = os.environ.get("POW_LIVE_SERVER", "local")
# PORT-EXTRA (PHASE_7 D3): the NPC market always sells these Rare items at these prices (the
# data has 1 gold for both); without 502 / 504 only 71-82 of the 149 recipes can be crafted.
LIVE_PRICE = {502: 3000, 504: 5000}

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

# PORT-EXTRA (asked by the player): auto-hunt on the mission map (pow/game/autopilot.py). The hero
# walks to the nearest enemy, attacks, casts the skills on keys 1-5 and drinks the potions on * / #.
# Tab or a click on the bottom-left corner of the map turns it on and off; POW_AUTO_HUNT=1 = on
# from the start. Any key of the player pauses it for a moment.
AUTO_HUNT = os.environ.get("POW_AUTO_HUNT", "0") == "1"
