"""Headless screenshots of the MP client (PHASE_9), like tools/shot.py for the single player.

    python pyport/tools/mp_shot.py pyport/tools/scenarios/mp_login.keys [--out DIR] [--every]

Steps: wait N | key NAME [COUNT] (UP DOWN LEFT RIGHT FIRE LSOFT RSOFT 0-9 STAR POUND) |
       shot NAME | include FILE | digits 1234 (number keys one per tick) | # comment
The server runs inside the game (POW_MP_SERVER=local) with a fresh temporary save folder.
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
os.environ.setdefault("POW_MP_SERVER", "local")


def parse(path):
    path = pathlib.Path(path)
    steps = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            cmd, _, arg = line.partition(" ")
            if cmd.lower() == "include":           # include other.keys (same folder)
                steps += parse(path.parent / arg.strip())
            else:
                steps.append((cmd.lower(), arg.strip()))
    return steps


def run(steps, out, every=False, save_dir=None):
    import pygame
    import config
    from pow.midp import display, system
    from pow.midp.canvas import KEYNAMES

    own = save_dir is None
    save_dir = save_dir or tempfile.mkdtemp(prefix="pow_mp_rms_")
    config.SAVE_DIR = save_dir
    for mod in [m for m in sys.modules if m == "pow_mp" or m.startswith("pow_mp.")]:
        del sys.modules[mod]           # fresh statics every run, like a new JVM
    from pow_mp.net.transport import LocalTransport
    LocalTransport._server = None
    out = pathlib.Path(out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    system.use_virtual_clock()
    display.init(headless=True)
    from pow_mp.Main import Main
    midlet = Main()
    steps = list(steps)
    st = {"frame": 0, "i": 0, "wait": 0, "n": 0, "last": None, "queue": []}
    saved = []

    def on_frame(screen):
        st["frame"] += 1
        st["last"] = screen.copy()
        if every:
            pygame.image.save(screen, str(out / ("tick_%04d.png" % st["frame"])))
        if st["queue"]:
            Main.b.keyPressed(st["queue"].pop(0))
            return
        if st["wait"] > 0:
            st["wait"] -= 1
            if st["wait"] > 0:
                return
        while st["i"] < len(steps):
            cmd, arg = steps[st["i"]]
            st["i"] += 1
            if cmd == "wait":
                st["wait"] = int(arg)
                return
            if cmd == "key":                     # key NAME [COUNT]
                name, _, count = arg.partition(" ")
                code = KEYNAMES[name.upper()]
                Main.b.keyPressed(code)
                st["queue"] = [code] * (int(count or 1) - 1)
                st["wait"] = 1
                return
            if cmd == "digits":
                st["queue"] = [48 + int(ch) for ch in arg]
                return
            if cmd == "shot":
                st["n"] += 1
                name = "%02d_%s.png" % (st["n"], arg)
                pygame.image.save(st["last"], str(out / name))
                saved.append(name)
                continue
            raise SystemExit("unknown step: %s %s" % (cmd, arg))
        midlet.destroyed = True

    display.frame_hooks.append(on_frame)
    try:
        asyncio.run(midlet.startApp())
    finally:
        display.frame_hooks.remove(on_frame)
        if own:
            shutil.rmtree(save_dir, ignore_errors=True)
    return saved, st["frame"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario")
    ap.add_argument("--out", default=None)
    ap.add_argument("--every", action="store_true")
    a = ap.parse_args()
    out = a.out or str(HERE.parent / "shots" / pathlib.Path(a.scenario).stem)
    saved, frames = run(parse(a.scenario), out, a.every)
    print("%d frames, %d shots -> %s" % (frames, len(saved), out))


if __name__ == "__main__":
    main()
