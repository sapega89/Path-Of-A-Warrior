"""Settings of the Python port (spike version; registry of flags = PHASE_1 task 1.8)."""
import os
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# Where the original resources (PNG, .scr, .arr, ...) are read from.
# Desktop: the repository root (pyport/..). Browser build: assets are copied next to main.py.
RES_ROOT = os.environ.get("POW_RES_ROOT") or (
    str(HERE.parent) if (HERE.parent / "0_font.png").exists() else str(HERE / "res")
)

# Multiplayer (PHASE_9): resources of the multiplayer, and where its server is.
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

# Live of the single player (pow_server/live.py): "local" = the server inside the game
# (shares the accounts of the in-game multiplayer server), or ws(s)://host:28200/live.
LIVE_SERVER = os.environ.get("POW_LIVE_SERVER", "local")
# : the single player's save also kept on the server
# (pow/game/cloud_save.py, pow_server/cloud.py) for the Live account. "auto" = the
# server of LIVE_SERVER at the path /save when LIVE_SERVER is ws(s)://; "off"; or a
# ws(s)://host:28200/save URL. Browser: index.html?save=...
SAVE_SERVER = os.environ.get("POW_SAVE_SERVER", "auto")
# : "always online". Continue and New Game log in to Live
# with the registered account at once, in the background, and the connection stays for the whole
# game (pow/game/live_online.py); a hero without an account is offered the registration once. Game
# Menu > Live / Warehouse opens without the "Connect to Live?" question, and
# Management (Save / Load User Data) is gone: there is one hero, kept on the server by cloud_save.
# Without the server the game plays as before. POW_ALWAYS_ONLINE=0 = the original (connect on every
# Live, disconnect on leaving it). tools/shot.py uses 0.
ALWAYS_ONLINE = os.environ.get("POW_ALWAYS_ONLINE", "1") == "1"
# : the hero's save only on the server (pow/game/cloud_save.py
# SERVER_ONLY), never on the device, and the game starts only online: without the server a
# "No connection" screen (pow/game/offline_screen.py), and a hero must have an account (the
# registration cannot be skipped). Only with a server (SAVE_SERVER); the in-game "local"
# server keeps the save on the device as before. POW_SERVER_ONLY_SAVE=0 = the save on the
# device too, the game starts offline.
SERVER_ONLY_SAVE = os.environ.get("POW_SERVER_ONLY_SAVE", "1") == "1"
# (PHASE_7 D3): the NPC market always sells these Rare items at these prices (the
# data has 1 gold for both); without 502 / 504 only 71-82 of the 149 recipes can be crafted.
LIVE_PRICE = {502: 3000, 504: 5000}

# Re-raise exceptions inside the game loop (the original would print "--run:" and continue).
DEBUG = os.environ.get("POW_DEBUG", "1") == "1"


# SPIKE-ONLY: create a minimal save on first start so Continue opens the Game Menu without
# going through New Game. Off by default since hero creation is ported; POW_DEMO_SAVE=1 or
# main.py --demo turns it on.
DEMO_SAVE = os.environ.get("POW_DEMO_SAVE", "0") == "1"

# (debug / tests): POW_NO_ENEMIES=1 = the map without enemies (rooms with a general
# stay closed), POW_NO_COMBAT=1 = the attack / skill / potion keys do nothing on the map.
# Both off by default: the game has its combat (phase 4).
NO_ENEMIES = os.environ.get("POW_NO_ENEMIES", "0") == "1"
NO_COMBAT = os.environ.get("POW_NO_COMBAT", "0") == "1"

# (PC controls): the hero walks only while a direction key / the mouse button is
# held (the phone had no key release: a tap started walking and the next tap stopped).
# POW_HOLD_TO_MOVE=0 = the phone way. tools/shot.py uses 0 (scenarios press keys like a phone).
HOLD_TO_MOVE = os.environ.get("POW_HOLD_TO_MOVE", "1") == "1"

# (temporary, asked by the player): the Normal-difficulty auto-aim (ar.f: before a hit
# the hero turns to the nearest enemy) also on Hard. Gold and EXP of Hard stay as they are.
# POW_AUTO_AIM_HARD=0 = the original (no auto-aim on Hard). tools/shot.py uses 0.
AUTO_AIM_HARD = os.environ.get("POW_AUTO_AIM_HARD", "1") == "1"

# (like Dragon Nest): a strip above the HUD frame with the 5 belt slots (keys Z X C V B
# or a click) and the 5 skill slots (keys 1-5 or a click; grey without the MP), see
# pow/game/skill_bar.py. POW_SKILL_BAR=0 = the original HUD (only * and # in combat).
# tools/shot.py uses 0 so the baseline screenshots stay the original's.
SKILL_BAR = os.environ.get("POW_SKILL_BAR", "1") == "1"
# the Skills menu shows a card (level, MP, damage, strikes, heal / buff, next level)
# instead of the one-line strip. POW_SKILL_CARD=0 = the original strip. tools/shot.py uses 0.
SKILL_CARD = os.environ.get("POW_SKILL_CARD", "1") == "1"

# POW_CHEAT=1 turns on the original developers' cheat, the JAD/manifest property
# POW_CHEAT: TRUE: loading a save sets gold to 555000;
# a new hero gets 500000 gold, 2000 in every stat and all skills.
CHEAT = os.environ.get("POW_CHEAT", "0") == "1"

# : Options volume steps on a loudness curve (pow/midp/media.py):
# pygame volume = (level / 100) ** 2, so "I" / "II" / "III" are clearly quieter than "IIII".
# POW_VOLUME_CURVE=0 = level / 100, as before.
VOLUME_CURVE = os.environ.get("POW_VOLUME_CURVE", "1") == "1"
# POW_GOLD=N - after a save is loaded the hero has N gold (nothing else changes).
GOLD = int(os.environ["POW_GOLD"]) if os.environ.get("POW_GOLD", "").isdigit() else None

# : a bigger backpack and Warehouse. The original had 25 backpack
# cells and 100 Warehouse cells. The backpack beyond 25 is saved in an
# extra block after the original save (game_canvas.save_game), so old saves load with the new cells
# empty. Both must be multiples of 5 (grids of 5 columns); the Warehouse count goes in one byte.
BACKPACK_SIZE = 45     # 3 pages of 3 rows in the Inventory
WAREHOUSE_SIZE = 200

# : ar.P above Lv69 switches to a drop row
# without the two lowest tiers (Lv1 and Lv10 gear never drop). True = above Lv69 the drops keep
# the odds of Lv45-69; False = the original.
DROPS_AFTER_69 = True

# : auto-hunt on the mission map (pow/game/autopilot.py). The hero
# walks to the nearest enemy, attacks, casts the skills on keys 1-5 and drinks the potions on * / #.
# Tab, F or a click on the AUTO button (bottom-left corner of the map) turns it on and off; POW_AUTO_HUNT=1 = on
# from the start. Any key of the player pauses it for a moment.
AUTO_HUNT = os.environ.get("POW_AUTO_HUNT", "0") == "1"
# The AUTO button is always drawn (grey = off) on the map and in Multiplayer battles, so the
# mode can be found; F and the right stick of a gamepad toggle it too. POW_AUTO_BUTTON=0 = only
# while it is on (tools/shot.py and tools/mp_shot.py, for the original screenshots).
AUTO_BUTTON = os.environ.get("POW_AUTO_BUTTON", "1") == "1"

# : the description of an item / skill / potion (Blacksmith,
# Gear, Inventory, Skills, Assign Items; not Live, whose grids leave no room) in a box as wide as the screen, in up to
# WIDE_DESC_LINES lines, instead of the narrow strip whose one line runs by. A longer text
# grows the box, up to WIDE_DESC_MAX_LINES lines (nothing runs by; the rest is cut).
# POW_WIDE_DESC=0 = the original strip.
WIDE_DESC = os.environ.get("POW_WIDE_DESC", "1") == "1"
WIDE_DESC_LINES = 3
WIDE_DESC_MAX_LINES = 5

# : full screen. F11 or Alt+Enter switch it, and so does
# Options > Screen; the choice is remembered (RecordStore "pow_display"). POW_FULLSCREEN=1 / 0
# forces it at start.
FULLSCREEN = {"1": True, "0": False}.get(os.environ.get("POW_FULLSCREEN", ""))
# the Screen row (full screen / window) in Options of the menu and of the pause.
SCREEN_OPTION = os.environ.get("POW_SCREEN_OPTION", "1") == "1"

# : a gamepad / joystick on the PC works as the phone keys
# (pow/midp/gamepad.py: stick and d-pad = arrows, A = OK, B = BACK, X Y LB RB LT = skills,
# RT = *, L3 = #, R3 = AUTO, Start = PAUSE; right stick = belt slots Z X C V on the map). POW_GAMEPAD=0
# turns it off.
GAMEPAD = os.environ.get("POW_GAMEPAD", "1") == "1"

# : on-screen keyboards of the Live registration
# (pow/game/key_grid.py): the UserID grid gets a row of digits and the password screen a row
# 0..9 + OK, so a gamepad (or the mouse) can type them. POW_REG_KEYBOARD=0 = the original
# (letters only, the password from the number keys). tools/shot.py uses 0 (baseline screenshots).
REG_KEYBOARD = os.environ.get("POW_REG_KEYBOARD", "1") == "1"

# : the soft-key captions name the key of the last device used:
# "Q:CONFIRM" / "ESC:BACK" after the keyboard, "SEL:CONFIRM" / "B:BACK" after the gamepad
# (pow/midp/canvas.py input_source). POW_KEY_HINTS=0 = the plain captions; tools/shot.py uses 0.
KEY_HINTS = os.environ.get("POW_KEY_HINTS", "1") == "1"

# : in what the player sees, no name, logo or site of the original
# publisher, and "Live" instead of the name of its online service (pow/game/rebrand.py). 0 = as in the original.
REBRAND = os.environ.get("POW_REBRAND", "1") == "1"
