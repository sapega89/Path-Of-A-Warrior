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
    "B6": True,  # ar.java:179 pause menu: FIRE on the 5th slot of Items (cR.a == 2, cM[1] == 4) opens
                 # Help as the Help row of the list does; back in Items cN is 7 -> slots 6-7 -> AIOOBE
    "B7": True,  # e.java:2694-2707 Combine with < 3 items: popup 39 over a grid that keeps fK[8] / fK[18]
                 # of the last grid screen (Gamevil Live: 9 rows) -> af[34] -> AIOOBE
    "B8": True,  # ag.java:872-967 entering the map clears the enemy effect data (fn = null) but not its
                 # kind: a general that was mid-skill leaves kind 2 -> the next enemy reads fn[..] -> NPE
}

# Gamevil Live of the single player (pow_server/live.py): "local" = the server inside the game
# (shares the accounts of the in-game multiplayer server), or ws(s)://host:28200/live.
LIVE_SERVER = os.environ.get("POW_LIVE_SERVER", "local")
# PORT-EXTRA (asked by Andrey): the single player's save also kept on the server
# (pow/game/cloud_save.py, pow_server/cloud.py) for the Gamevil Live account. "auto" = the
# server of LIVE_SERVER at the path /save when LIVE_SERVER is ws(s)://; "off"; or a
# ws(s)://host:28200/save URL. Browser: index.html?save=...
SAVE_SERVER = os.environ.get("POW_SAVE_SERVER", "auto")
# PORT-EXTRA (PHASE_7 D3): the NPC market always sells these Rare items at these prices (the
# data has 1 gold for both); without 502 / 504 only 71-82 of the 149 recipes can be crafted.
LIVE_PRICE = {502: 3000, 504: 5000}

# Re-raise exceptions inside the game loop (Java would print "--run:" and continue).
DEBUG = os.environ.get("POW_DEBUG", "1") == "1"


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

# PORT-EXTRA (like Dragon Nest): a strip above the HUD frame with the 5 belt slots (keys Z X C V B
# or a click) and the 5 skill slots (keys 1-5 or a click; grey without the MP), see
# pow/game/skill_bar.py. POW_SKILL_BAR=0 = the original HUD (only * and # in combat).
# tools/shot.py uses 0 so the baseline screenshots stay the original's.
SKILL_BAR = os.environ.get("POW_SKILL_BAR", "1") == "1"
# PORT-EXTRA: the Skills menu shows a card (level, MP, damage, strikes, heal / buff, next level)
# instead of the one-line strip. POW_SKILL_CARD=0 = the original strip. tools/shot.py uses 0.
SKILL_CARD = os.environ.get("POW_SKILL_CARD", "1") == "1"

# PORT-EXTRA: POW_CHEAT=1 turns on the original developers' cheat, the JAD/manifest property
# GAMEVIL_CHEAT: TRUE (ag.java:626, ag.bi): loading a save sets gold to 555000 (ag.java:2179);
# a new hero gets 500000 gold, 2000 in every stat and all skills (ag.java:916, 3260).
CHEAT = os.environ.get("POW_CHEAT", "0") == "1"

# PORT-EXTRA (asked by the player): Options volume steps on a loudness curve (pow/midp/media.py):
# pygame volume = (level / 100) ** 2, so "I" / "II" / "III" are clearly quieter than "IIII".
# POW_VOLUME_CURVE=0 = level / 100, as before.
VOLUME_CURVE = os.environ.get("POW_VOLUME_CURVE", "1") == "1"
# PORT-EXTRA: POW_GOLD=N - after a save is loaded the hero has N gold (nothing else changes).
GOLD = int(os.environ["POW_GOLD"]) if os.environ.get("POW_GOLD", "").isdigit() else None

# PORT-EXTRA (asked by the player): a bigger backpack and Warehouse. The original had 25 backpack
# cells (cz.Y, 5x5 in 2 pages) and 100 Warehouse cells (as.gw). The backpack beyond 25 is saved in an
# extra block after the original save (game_canvas.save_game), so old saves load with the new cells
# empty. Both must be multiples of 5 (grids of 5 columns); the Warehouse count goes in one byte.
BACKPACK_SIZE = 45     # 3 pages of 3 rows in the Inventory
WAREHOUSE_SIZE = 200

# PORT-EXTRA (asked by the player): ar.P() (ar.java:2055-2078) above Lv69 switches to a drop row
# without the two lowest tiers (Lv1 and Lv10 gear never drop). True = above Lv69 the drops keep
# the odds of Lv45-69; False = the original.
DROPS_AFTER_69 = True

# PORT-EXTRA (asked by the player): auto-hunt on the mission map (pow/game/autopilot.py). The hero
# walks to the nearest enemy, attacks, casts the skills on keys 1-5 and drinks the potions on * / #.
# Tab, F or a click on the AUTO button (bottom-left corner of the map) turns it on and off; POW_AUTO_HUNT=1 = on
# from the start. Any key of the player pauses it for a moment.
AUTO_HUNT = os.environ.get("POW_AUTO_HUNT", "0") == "1"
# The AUTO button is always drawn (grey = off) on the map and in Multiplayer battles, so the
# mode can be found; F and the right stick of a gamepad toggle it too. POW_AUTO_BUTTON=0 = only
# while it is on (tools/shot.py and tools/mp_shot.py, for the original screenshots).
AUTO_BUTTON = os.environ.get("POW_AUTO_BUTTON", "1") == "1"

# PORT-EXTRA (asked by the player): the description of an item / skill / potion (Blacksmith,
# Gear, Inventory, Skills, Assign Items; not Gamevil Live, whose grids leave no room) in a box as wide as the screen, in up to
# WIDE_DESC_LINES lines, instead of the narrow strip whose one line runs by.
# POW_WIDE_DESC=0 = the original strip.
WIDE_DESC = os.environ.get("POW_WIDE_DESC", "1") == "1"
WIDE_DESC_LINES = 3

# PORT-EXTRA (asked by the player): full screen. F11 or Alt+Enter switch it, and so does
# Options > Screen; the choice is remembered (RecordStore "pow_display"). POW_FULLSCREEN=1 / 0
# forces it at start.
FULLSCREEN = {"1": True, "0": False}.get(os.environ.get("POW_FULLSCREEN", ""))
# PORT-EXTRA: the Screen row (full screen / window) in Options of the menu and of the pause.
SCREEN_OPTION = os.environ.get("POW_SCREEN_OPTION", "1") == "1"

# PORT-EXTRA (asked by the player): a gamepad / joystick on the PC works as the phone keys
# (pow/midp/gamepad.py: stick and d-pad = arrows, A = OK, B = BACK, X Y LB RB LT = skills,
# RT = *, L3 = #, R3 = AUTO, Start = PAUSE; right stick = belt slots Z X C V on the map). POW_GAMEPAD=0
# turns it off.
GAMEPAD = os.environ.get("POW_GAMEPAD", "1") == "1"
