"""Headless screenshots (PHASE_0 task 0.7).

    python pyport/tools/shot.py pyport/tools/scenarios/title.keys [--out DIR] [--every]

Runs the real game loop with SDL_VIDEODRIVER=dummy and a virtual clock (time moves only by
the loop's own sleeps, so 1 tick = 120 ms in menus, exactly like ag.run). A scenario is a
list of steps, one per line:

    wait N          run N ticks (frames)
    key NAME        press a phone key before the next tick: UP DOWN LEFT RIGHT FIRE
                    LSOFT RSOFT(=BACK) 0-9 STAR POUND
    click X Y       left mouse click at screen pixel (X, Y) (0..239, 0..319)
    wheel up|down   mouse wheel over the screen
    rclick          right mouse button (= BACK)
    shot NAME       save the last frame as NN_NAME.png
    gold N          TEST-ONLY: set the hero's gold (ag.cz.E) to N, to try the Blacksmith
    generals N      TEST-ONLY: befriend the first N generals of the table (10, 30, 50... points)
                    and allow one visit (cz.S = 1), as after a mission
    hero F N        TEST-ONLY: set the hero's field ag.cz.F to N (p = HP, r = MP, w = ATK, x = DEF)
    skill S ID      TEST-ONLY: learn skill ID (12..30) and put it on skill key slot S (0..4 = 1 3 7 9 0)
    potion K ID N   TEST-ONLY: put N potions of kind ID on the quick slot K (0 = *, 1 = #)
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
os.environ.setdefault("POW_SEED", "1")   # Random() without the clock: repeatable runs


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
    from pow.midp.canvas import KEYNAMES

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
    from pow.game.Main import Main
    from pow.game.ag import ag

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
                Main.b.keyPressed(KEYNAMES[arg.upper()])
                state["wait"] = 1          # the key is consumed on the next tick
                return
            if cmd in ("click", "wheel", "rclick"):
                if cmd == "click":
                    cx, cy = map(int, arg.split())
                    Main.b.click(cx, cy)
                elif cmd == "wheel":
                    Main.b.click(0, 0, "wheel_" + arg.lower())
                else:
                    Main.b.click(0, 0, "back")
                state["wait"] = max(1, len(Main.b.key_queue))   # queued keys go 1 per tick
                return
            if cmd == "gold":
                ag.cz.E = int(arg)
                continue
            if cmd == "hero":              # TEST-ONLY: hero FIELD N, e.g. hero p 1 (HP), hero w 99 (ATK)
                field, val = arg.split()
                setattr(ag.cz, field, int(val))
                continue
            if cmd == "skill":             # TEST-ONLY: skill SLOT ID - learn skill ID (12..30) on key slot
                slot, sid = map(int, arg.split())
                if ag.cz.W[sid - 12] == 0:
                    ag.cz.W[sid - 12] = 1
                ag.cz.V[slot] = sid
                continue
            if cmd == "potion":            # TEST-ONLY: potion KEY ID N - N potions ID on * (KEY 0) or # (1)
                key, pid, cnt = map(int, arg.split())
                z = ag.cz.Z[ag.cz.aa[key]]
                z.a = pid
                z.b = cnt
                continue
            if cmd == "win":
                ag.cr = 1                  # the mission's general was met on the map (c.java:986)
                ag.bd.d_I(1)               # what the combat calls on victory (c.java:1516)
                continue
            if cmd == "generals":
                from pow.game.d import d
                from pow.game.e import e
                tab = d("/" + ag.bE.a_I(52))
                for b1 in range(int(arg)):
                    e.b_II(tab.a_II(b1, 0), 10 + 20 * b1)
                ag.cz.S = 1
                continue
            if cmd == "shot":
                state["n"] += 1
                name = "%02d_%s.png" % (state["n"], arg)
                pygame.image.save(state["last"], str(out / name))
                saved.append(name)
                continue
            raise SystemExit("unknown step: %s %s" % (cmd, arg))
        ag.gh = False

    display.frame_hooks.append(on_frame)
    asyncio.run(Main().startApp())
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
