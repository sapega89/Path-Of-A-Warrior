"""Headless screenshots of the MP client (PHASE_9), like tools/shot.py for the single player.

    python pyport/tools/mp_shot.py pyport/tools/scenarios/mp_login.keys [--out DIR] [--every]

Steps: wait N | key NAME [COUNT] (UP DOWN LEFT RIGHT FIRE LSOFT RSOFT 0-9 STAR POUND) |
       shot NAME | include FILE |
       until STATE[,STATE] [MAX] (g.cY, the client state of 06 §1.2) |
       goto_if STATE[,STATE] LABEL | label LABEL | key_if STATE[,STATE] KEY |
       watch STATE NAME [FRAMES] (one shot FRAMES after first entering STATE) | digits 1234 (number keys one per tick) |
       bot_invite MODE (the scripted player RIVAL invites TEST: 0/1 Challenge, 2 mission) |
       bot_order NAME [N] (RIVAL creates the order NAME; N offline members MEMBERA.. join it) |
       bot_chat CHANNEL [TO] TEXT (RIVAL writes in the chat: 0 lobby, 1 order, 2 private to TO) |
       type TEXT (a PC keyboard types TEXT, one character per tick, into the chat's text box) |
       # comment
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
os.environ["POW_CHEAT"] = "0"   # a POW_CHEAT=1 left in the shell (500000 gold, all skills) breaks every baseline
os.environ.setdefault("POW_AUTO_BUTTON", "0")   # the AUTO button only while on (original screenshots)
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
    from pow_mp.midlet import Midlet
    midlet = Midlet()
    steps = list(steps)
    st = {"frame": 0, "i": 0, "wait": 0, "n": 0, "last": None, "queue": [], "until": None,
          "watch": {}}
    saved = []

    def on_frame(screen):
        st["frame"] += 1
        st["last"] = screen.copy()
        if every:
            pygame.image.save(screen, str(out / ("tick_%04d.png" % st["frame"])))
        if st["watch"]:
            from pow_mp.mp_canvas import MpCanvas
            w = st["watch"].get(MpCanvas.state)
            if w and not w["done"]:
                w["seen"] += 1
                if w["seen"] > w["delay"]:
                    w["done"] = True
                    st["n"] += 1
                    name = "%02d_%s.png" % (st["n"], w["name"])
                    pygame.image.save(screen, str(out / name))
                    saved.append(name)
        if st["queue"]:
            item = st["queue"].pop(0)
            if isinstance(item, tuple):          # ("text", char): typed on a PC keyboard
                Midlet.canvas.text_input(item[1])
            else:
                Midlet.canvas.keyPressed(item)
            return
        if st["until"] is not None:
            states, left = st["until"]
            from pow_mp.mp_canvas import MpCanvas
            if MpCanvas.state not in states and left > 0:
                st["until"] = (states, left - 1)
                return
            if MpCanvas.state not in states:
                raise SystemExit("until %s: still in state %d" % (states, MpCanvas.state))
            st["until"] = None
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
                Midlet.canvas.keyPressed(code)
                st["queue"] = [code] * (int(count or 1) - 1)
                st["wait"] = 1
                return
            if cmd == "watch":                   # watch STATE NAME [FRAMES]: shot once, FRAMES in
                state, _, rest = arg.partition(" ")
                name, _, delay = rest.partition(" ")
                st["watch"][int(state)] = {"name": name, "delay": int(delay or 0), "seen": 0,
                                           "done": False}
                continue
            if cmd == "label":
                continue
            if cmd == "goto_if":                 # goto_if STATE[,STATE...] LABEL
                states, _, label = arg.partition(" ")
                from pow_mp.mp_canvas import MpCanvas
                if MpCanvas.state in {int(x) for x in states.split(",")}:
                    st["i"] = steps.index(("label", label.strip())) + 1
                continue
            if cmd == "key_if":                  # key_if STATE[,STATE...] KEY: press only there
                states, _, name = arg.partition(" ")
                from pow_mp.mp_canvas import MpCanvas
                if MpCanvas.state in {int(x) for x in states.split(",")}:
                    Midlet.canvas.keyPressed(KEYNAMES[name.strip().upper()])
                    st["wait"] = 1
                    return
                continue
            if cmd == "until":                   # until STATE[,STATE...] [MAX_FRAMES]
                states, _, limit = arg.partition(" ")
                st["until"] = ({int(x) for x in states.split(",")}, int(limit or 3000))
                return
            if cmd == "bot_invite":              # bot_invite MODE: the first bot invites TEST
                from pow_mp.net.transport import LocalTransport
                LocalTransport._bots[0].invite("TEST", int(arg or 0))
                continue
            if cmd == "bot_order":               # bot_order NAME: the first bot creates an order
                from pow_mp.net.transport import LocalTransport
                from pow_server import messages as M
                from pow_server import orders
                from pow_server.model import default_character
                name, _, fill = arg.partition(" ")
                LocalTransport._bots[0]._send(M.ORDER_CREATE, name=name)
                srv = LocalTransport._server
                doc = orders.get(srv.storage, name)
                for i in range(int(fill or 0)):
                    uid = "MEMBER" + chr(65 + i)
                    srv.storage.create_account(uid, "0000")
                    ch = default_character(uid)
                    ch.level, ch.order = 1 + 3 * i, name
                    srv.storage.save(ch)
                    doc["members"].append(uid)
                srv.storage.live_put("order:" + name, doc)
                continue
            if cmd == "bot_chat":                # bot_chat CHANNEL [TO] TEXT
                from pow_mp.net.transport import LocalTransport
                from pow_server import messages as M
                channel, _, text = arg.partition(" ")
                peer = ""
                if channel == "2":
                    peer, _, text = text.partition(" ")
                bot = LocalTransport._bots[0]
                bot.session.chat_rate.times.clear()
                bot._send(M.CHAT_SEND, channel=int(channel), peer=peer, text=text)
                continue
            if cmd == "type":                    # type TEXT: the PC keyboard (Canvas.text_input)
                st["queue"] = [("text", ch) for ch in arg]
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
            raise SystemExit(f"unknown step: {cmd} {arg}")
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
