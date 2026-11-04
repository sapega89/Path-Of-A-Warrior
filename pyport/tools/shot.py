"""Headless screenshots (PHASE_0 task 0.7).

    python pyport/tools/shot.py pyport/tools/scenarios/title.keys [--out DIR] [--every]

Runs the real game loop with SDL_VIDEODRIVER=dummy and a virtual clock (time moves only by
the loop's own sleeps, so 1 tick = 120 ms in menus, exactly like ag.run). A scenario is a
list of steps, one per line:

    wait N          run N ticks (frames)
    key NAME        press a phone key before the next tick: UP DOWN LEFT RIGHT FIRE
                    LSOFT RSOFT(=BACK) 0-9 STAR POUND BELT1-BELT5 (Z X C V B)
    click X Y       left mouse click at screen pixel (X, Y) (0..239, 0..319)
    wheel up|down   mouse wheel over the screen
    rclick [X Y]    right mouse button (= BACK; at X Y on the map = attack toward X Y)
    mclick X Y      middle mouse button (on the map = skill key 1)
    hold KEY        press a direction key and keep it down (POW_HOLD_TO_MOVE=1: walk)
    release KEY     let the held key go
    mousedown X Y   left button pressed and held at X Y; mouseup = let it go
    shot NAME       save the last frame as NN_NAME.png
    multiplayer N NAME  (before the YES of Main Menu > Multiplayer) once the game has quit, run
                    the Multiplayer game as main.py does, N frames, and save the last as NN_NAME.png
    gold N          TEST-ONLY: set the hero's gold (ag.cz.E) to N, to try the Blacksmith
    generals N      TEST-ONLY: befriend the first N generals of the table (10, 30, 50... points)
                    and allow one visit (cz.S = 1), as after a mission
    hero F N        TEST-ONLY: set the hero's field ag.cz.F to N (p = HP, r = MP, w = ATK, x = DEF)
    skill S ID      TEST-ONLY: learn skill ID (12..30) and put it on skill key slot S (0..4 = 1 3 7 9 0)
    potion K ID N   TEST-ONLY: put N potions of kind ID on the quick slot K (0 = *, 1 = #)
    auto on|off     PORT-EXTRA auto-hunt (pow/game/autopilot.py) on / off
    expect F OP N   TEST-ONLY: stop with an error unless the hero's field F OP N (OP: >= <= == > <)
    skilllv ID LV   TEST-ONLY: set the level of skill ID (12..30) to LV
    belt S ID N     TEST-ONLY: put N items of kind ID on belt slot S (0..4 = keys Z X C V B)
    win             TEST-ONLY: win the accepted mission now (c.d(1), as the combat would)
    env NAME=VALUE  (first lines only) set an environment variable before the game reads config,
                    e.g. env POW_NO_ENEMIES=1 for the map without enemies
    save zero       (first line only, after env) start with a minimal 965-byte save in RecordStore
                    "gamevil_pow_data" so that Main Menu -> Continue opens the Game Menu
    # ...           comment

Random() is seeded with POW_SEED (default 1) instead of the clock, so runs repeat.
With --every, every tick is also saved as tick_NNNN.png.
"""
import argparse
import asyncio
import os
import pathlib
import shutil
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("POW_SCALE", "1")
os.environ.setdefault("POW_SEED", "1")
os.environ["POW_CHEAT"] = "0"   # a POW_CHEAT=1 left in the shell (500000 gold, all skills) breaks every baseline
os.environ.setdefault("POW_AUTO_BUTTON", "0")   # the AUTO button only while on (original screenshots)
os.environ.setdefault("POW_AUTO_AIM_HARD", "0")   # the original: no auto-aim on Hard
os.environ.setdefault("POW_HOLD_TO_MOVE", "0")   # keys are taps, as on the phone (env line to change)   # Random() without the clock: repeatable runs
os.environ.setdefault("POW_SKILL_BAR", "0")   # the original HUD (env line to turn the skill bar on)
os.environ.setdefault("POW_SKILL_CARD", "0")  # the original description strip of Skills


def parse(path):
    steps = []
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        cmd, _, arg = line.partition(" ")
        steps.append((cmd.lower(), arg.strip()))
    return steps


def make_zero_save():
    """Smallest save U() accepts: length != 0, name 'HERO', everything else 0 (ag.java:2126-2214)."""
    from pow.midp.rms import RecordStore
    data = bytearray(965)
    data[0] = 965 & 0xFF
    data[1] = 965 >> 8
    data[2:10] = b"HERO    "
    rs = RecordStore.openRecordStore("gamevil_pow_data", True)
    if rs.getNumRecords() == 0:
        rs.addRecord(data, 0, len(data))
    else:
        rs.setRecord(1, data, 0, len(data))


def run(scenario, out, every=False):
    steps = parse(scenario)
    while steps and steps[0][0] == "env":     # env NAME=VALUE lines first: before config is read
        k, _, v = steps[0][1].partition("=")
        os.environ[k] = v
        steps = steps[1:]
    import pygame

    import config
    from pow.midp import display, system
    from pow.midp.canvas import DIRECTION_KEYS, KEYNAMES

    save_dir = tempfile.mkdtemp(prefix="pow_rms_")
    config.SAVE_DIR = save_dir
    if steps and steps[0] == ("save", "zero"):
        make_zero_save()
        steps = steps[1:]
    out = pathlib.Path(out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    system.use_virtual_clock()
    display.init(headless=True)
    from pow.game.game_canvas import GameCanvas
    from pow.game.midlet import Midlet

    state = {"frame": 0, "i": 0, "wait": 0, "n": 0, "last": None}
    saved = []

    def on_frame(screen):
        state["frame"] += 1
        state["last"] = screen.copy()
        if every:
            pygame.image.save(screen, str(out / ("tick_%04d.png" % state["frame"])))
        if state["wait"] > 0:
            state["wait"] -= 1
            if state["wait"] > 0:
                return
        while state["i"] < len(steps):
            cmd, arg = steps[state["i"]]
            state["i"] += 1
            if cmd == "wait":
                state["wait"] = int(arg)
                return
            if cmd == "key":
                Midlet.canvas.keyPressed(KEYNAMES[arg.upper()])
                state["wait"] = 1          # the key is consumed on the next tick
                return
            if cmd in ("hold", "release"):     # a direction key held down / let go
                code = KEYNAMES[arg.upper()]
                if cmd == "hold":
                    Midlet.canvas.hold(code)
                    Midlet.canvas.keyPressed(code)
                    state["wait"] = 1
                    return
                Midlet.canvas.release(code)
                continue
            if cmd in ("mousedown", "mouseup"):  # left button held at X Y (walk) / let go
                if cmd == "mouseup":
                    Midlet.canvas.mouse_dir = None
                    continue
                cx, cy = map(int, arg.split())
                keys = Midlet.canvas.pointer(cx, cy, "click")
                Midlet.canvas.mouse_dir = keys[0] if len(keys) == 1 and keys[0] in DIRECTION_KEYS else None
                Midlet.canvas.key_queue.extend(keys)
                state["wait"] = max(1, len(Midlet.canvas.key_queue))
                return
            if cmd in ("click", "wheel", "rclick", "mclick"):
                if cmd == "click":
                    cx, cy = map(int, arg.split())
                    Midlet.canvas.click(cx, cy)
                elif cmd == "wheel":
                    Midlet.canvas.click(0, 0, "wheel_" + arg.lower())
                elif cmd == "mclick":
                    cx, cy = map(int, arg.split())
                    Midlet.canvas.click(cx, cy, "middle")
                elif arg:
                    cx, cy = map(int, arg.split())
                    Midlet.canvas.click(cx, cy, "rclick")
                else:
                    Midlet.canvas.click(0, 0, "back")
                state["wait"] = max(1, len(Midlet.canvas.key_queue))   # queued keys go 1 per tick
                return
            if cmd == "gold":
                GameCanvas.hero.gold = int(arg)
                continue
            if cmd == "hero":              # TEST-ONLY: hero FIELD N, e.g. hero hp 1, hero attack 99
                field, val = arg.split()
                if not hasattr(GameCanvas.hero, field):
                    raise SystemExit("unknown hero field: " + field)
                setattr(GameCanvas.hero, field, int(val))
                continue
            if cmd == "skill":             # TEST-ONLY: skill SLOT ID - learn skill ID (12..30) on key slot
                slot, sid = map(int, arg.split())
                if GameCanvas.hero.skill_levels[sid - 12] == 0:
                    GameCanvas.hero.skill_levels[sid - 12] = 1
                GameCanvas.hero.hotkeys[slot] = sid
                continue
            if cmd == "potion":            # TEST-ONLY: potion KEY ID N - N potions ID on * (KEY 0) or # (1)
                key, pid, cnt = map(int, arg.split())
                z = GameCanvas.hero.quick_slots[GameCanvas.hero.quick_keys[key]]
                z.item = pid
                z.count = cnt
                continue
            if cmd == "auto":
                from pow.game.autopilot import Autopilot
                if Autopilot.on != (arg.lower() == "on"):
                    Autopilot.toggle()
                continue
            if cmd == "expect":
                import operator
                field, op, val = arg.split()
                ops = {">=": operator.ge, "<=": operator.le, "==": operator.eq, ">": operator.gt,
                       "<": operator.lt}
                have = getattr(GameCanvas.hero, field)
                if not ops[op](have, int(val)):
                    raise SystemExit(f"expect {field} {op} {val}: it is {have}")
                print(f"expect {field} {op} {val}: {have}")
                continue
            if cmd == "skilllv":           # TEST-ONLY: skilllv ID LV - skill ID (12..30) at level LV
                sid, lv = map(int, arg.split())
                GameCanvas.hero.skill_levels[sid - 12] = lv
                continue
            if cmd == "belt":              # TEST-ONLY: belt SLOT ID N - N items ID on belt slot 0..4
                slot, pid, cnt = map(int, arg.split())
                z = GameCanvas.hero.quick_slots[slot]
                z.item = pid
                z.count = cnt
                continue
            if cmd == "win":
                GameCanvas.boss_fight = 1                  # the mission's general was met on the map (c.java:986)
                GameCanvas.scene.finish_mission(1)               # what the combat calls on victory (c.java:1516)
                continue
            if cmd == "generals":
                from pow.game.arr_table import ArrTable
                from pow.game.menus import Menus
                tab = ArrTable("/" + GameCanvas.scr_data.get(52))
                for b1 in range(int(arg)):
                    Menus.add_friendship(tab.get_int(b1, 0), 10 + 20 * b1)
                GameCanvas.hero.live_registered = 1
                continue
            if cmd == "multiplayer":       # multiplayer N NAME: after the game quits (Main Menu >
                state["mp"] = arg.split()      # Multiplayer > YES), N MP frames and shot NAME
                continue
            if cmd == "shot":
                state["n"] += 1
                name = "%02d_%s.png" % (state["n"], arg)
                pygame.image.save(state["last"], str(out / name))
                saved.append(name)
                continue
            raise SystemExit(f"unknown step: {cmd} {arg}")
        GameCanvas.running = False

    display.frame_hooks.append(on_frame)
    midlet = Midlet()
    asyncio.run(midlet.startApp())
    display.frame_hooks.remove(on_frame)
    if state.get("mp"):                    # main.py: the Multiplayer game in the same window
        if not midlet.to_multiplayer:
            raise SystemExit("multiplayer: the game did not ask for the Multiplayer game")
        import mp_main
        from pow_mp.midlet import Midlet as MPMain
        frames, name = int(state["mp"][0]), state["mp"][1]
        mp = {"left": frames}

        def mp_frame(screen):
            mp["left"] -= 1
            if mp["left"] <= 0:
                state["n"] += 1
                fn = "%02d_%s.png" % (state["n"], name)
                pygame.image.save(screen, str(out / fn))
                saved.append(fn)
                MPMain.canvas.midlet.destroyed = True     # its own Exit: main.py would restart the game

        display.frame_hooks.append(mp_frame)
        try:
            if asyncio.run(mp_main.play()) is not True:
                raise SystemExit("multiplayer: mp_main.play() did not return to the single player")
        finally:
            display.frame_hooks.remove(mp_frame)
    shutil.rmtree(save_dir, ignore_errors=True)
    return saved, state["frame"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario")
    ap.add_argument("--out", default=None)
    ap.add_argument("--every", action="store_true")
    a = ap.parse_args()
    out = a.out or str(HERE.parent / "shots" / pathlib.Path(a.scenario).stem)
    saved, frames = run(a.scenario, out, a.every)
    print("%d frames, %d shots -> %s" % (frames, len(saved), out))
    for s in saved:
        print("  ", s)


if __name__ == "__main__":
    main()
