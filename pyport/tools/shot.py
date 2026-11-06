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
    account ID PWD  TEST-ONLY: register the Live UserID / password on this device
    include FILE    the steps of another .keys file of this folder (e.g. _enter.keys: into the
                    multiplayer screens, Live > Multiplayer, logged in, on their Main Menu)
    key NAME N      the key N times, one per tick
    until S[,S] [MAX]  wait until the multiplayer screens are in one of the states S
    goto_if S[,S] LABEL / label LABEL / key_if S[,S] KEY   branch on their state
    watch S NAME [FRAMES]   one shot FRAMES after the state S is first entered
    digits 1234     the number keys, one per tick; type TEXT   the PC keyboard into a text box
    bot_invite MODE / bot_order NAME [N] / bot_chat CHANNEL [TO] TEXT   the in-game server's
                    bot RIVAL invites TEST (0/1 Challenge, 2 mission), creates an order, chats
    mp_online ID    TEST-ONLY: stop unless ID is logged in on the in-game multiplayer server
    logins N        TEST-ONLY: stop with an error if the game sent more than N background logins
    online yes|no   TEST-ONLY: stop with an error unless the background login (ALWAYS_ONLINE) is that
    gold N          TEST-ONLY: set the hero's gold (ag.cz.E) to N, to try the Blacksmith
    generals N      TEST-ONLY: befriend the first N generals of the table (10, 30, 50... points)
                    and allow one visit (cz.S = 1), as after a mission
    hero F N        TEST-ONLY: set the hero's field ag.cz.F to N (p = HP, r = MP, w = ATK, x = DEF)
    skill S ID      TEST-ONLY: learn skill ID (12..30) and put it on skill key slot S (0..4 = 1 3 7 9 0)
    potion K ID N   TEST-ONLY: put N potions of kind ID on the quick slot K (0 = *, 1 = # )
    auto on|off     auto-hunt (pow/game/autopilot.py) on / off
    expect F OP N   TEST-ONLY: stop with an error unless the hero's field F OP N (OP: >= <= == > <)
    skilllv ID LV   TEST-ONLY: set the level of skill ID (12..30) to LV
    belt S ID N     TEST-ONLY: put N items of kind ID on belt slot S (0..4 = keys Z X C V B)
    win             TEST-ONLY: win the accepted mission now (c.d(1), as the combat would)
    env NAME=VALUE  (first lines only) set an environment variable before the game reads config,
                    e.g. env POW_NO_ENEMIES=1 for the map without enemies
    save zero       (first line only, after env) start with a minimal 965-byte save in RecordStore
                    "pow_data" so that Main Menu -> Continue opens the Game Menu
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
os.environ.setdefault("POW_ALWAYS_ONLINE", "0")   # Live as in the original: connect on entry
os.environ.setdefault("POW_SERVER_ONLY_SAVE", "0")   # the save on the device (no server in the scenarios)
os.environ.setdefault("POW_SKILL_CARD", "0")  # the original description strip of Skills
os.environ.setdefault("POW_REG_KEYBOARD", "0")   # the original registration grid (env line to turn on)
os.environ.setdefault("POW_KEY_HINTS", "0")   # plain soft-key captions (env line to turn on)


def parse(path):
    path = pathlib.Path(path)
    steps = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        cmd, _, arg = line.partition(" ")
        if cmd.lower() == "include":           # include other.keys (same folder)
            steps += parse(path.parent / arg.strip())
        else:
            steps.append((cmd.lower(), arg.strip()))
    return steps


def make_zero_save():
    """Smallest save U accepts: length != 0, name 'HERO', everything else 0."""
    from pow.midp.rms import RecordStore
    data = bytearray(965)
    data[0] = 965 & 0xFF
    data[1] = 965 >> 8
    data[2:10] = b"HERO    "
    rs = RecordStore.openRecordStore("pow_data", True)
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

    state = {"frame": 0, "i": 0, "wait": 0, "n": 0, "last": None, "queue": [], "until": None,
             "watch": {}}
    saved = []

    def on_frame(screen):
        state["frame"] += 1
        state["last"] = screen.copy()
        if every:
            pygame.image.save(screen, str(out / ("tick_%04d.png" % state["frame"])))
        if state["watch"]:                  # the multiplayer screens: a shot once a state is reached
            w = state["watch"].get(_mp_state())
            if w and not w["done"]:
                w["seen"] += 1
                if w["seen"] > w["delay"]:
                    w["done"] = True
                    state["n"] += 1
                    name = "%02d_%s.png" % (state["n"], w["name"])
                    pygame.image.save(screen, str(out / name))
                    saved.append(name)
        if state["queue"]:                  # keys / typed characters, one per tick
            item = state["queue"].pop(0)
            if isinstance(item, tuple):
                _mp_canvas().text_input(item[1])
            else:
                Midlet.canvas.keyPressed(item)
            return
        if state["until"] is not None:
            states, left = state["until"]
            if _mp_state() not in states and left > 0:
                state["until"] = (states, left - 1)
                return
            if _mp_state() not in states:
                raise SystemExit("until %s: still in state %s" % (states, _mp_state()))
            state["until"] = None
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
            if cmd == "key":                    # key NAME [COUNT]
                name, _, count = arg.partition(" ")
                code = KEYNAMES[name.upper()]
                Midlet.canvas.keyPressed(code)
                state["queue"] = [code] * (int(count or 1) - 1)
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
            if cmd == "account":           # TEST-ONLY: account ID PWD - the Live registration
                uid, pwd = arg.split()
                from pow.midp.rms import RecordStore
                rec = bytearray(28)
                rec[0:len(pwd)] = pwd.encode()
                rec[12:12 + len(uid)] = uid.encode()
                rs = RecordStore.openRecordStore("pow_regist", True)
                if rs.getNumRecords() == 0:
                    rs.addRecord(rec, 0, 28)
                rs.setRecord(1, rec, 0, 28)
                continue
            if cmd == "logins":            # TEST-ONLY: logins N - stop if more than N background
                from pow.game.live_online import Online
                if Online.attempts > int(arg):
                    raise SystemExit(f"logins {arg}: {Online.attempts} sent")
                print(f"logins {arg}: {Online.attempts}")
                continue
            if cmd == "online":            # TEST-ONLY: online yes|no - stop unless the background
                from pow.game.live_online import Online
                if Online.logged_in != (arg == "yes"):
                    raise SystemExit(f"online {arg}: logged_in is {Online.logged_in}")
                print(f"online {arg}: ok")
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
                GameCanvas.boss_fight = 1                  # the mission's general was met on the map
                GameCanvas.scene.finish_mission(1)               # what the combat calls on victory
                continue
            if cmd == "generals":
                from pow.game.arr_table import ArrTable
                from pow.game.menus import Menus
                tab = ArrTable("/" + GameCanvas.scr_data.get(52))
                for b1 in range(int(arg)):
                    Menus.add_friendship(tab.get_int(b1, 0), 10 + 20 * b1)
                GameCanvas.hero.live_registered = 1
                continue
            if cmd == "shot":
                state["n"] += 1
                name = "%02d_%s.png" % (state["n"], arg)
                pygame.image.save(state["last"], str(out / name))
                saved.append(name)
                continue
            # --- the multiplayer screens (Live > Multiplayer) ---
            if cmd == "watch":                  # watch STATE NAME [FRAMES]: shot once, FRAMES in
                mp_state, _, rest = arg.partition(" ")
                name, _, delay = rest.partition(" ")
                state["watch"][int(mp_state)] = {"name": name, "delay": int(delay or 0), "seen": 0,
                                                  "done": False}
                continue
            if cmd == "label":
                continue
            if cmd == "goto_if":                # goto_if STATE[,STATE...] LABEL
                states, _, label = arg.partition(" ")
                if _mp_state() in {int(x) for x in states.split(",")}:
                    state["i"] = steps.index(("label", label.strip())) + 1
                continue
            if cmd == "key_if":                 # key_if STATE[,STATE...] KEY: press only there
                states, _, name = arg.partition(" ")
                if _mp_state() in {int(x) for x in states.split(",")}:
                    Midlet.canvas.keyPressed(KEYNAMES[name.strip().upper()])
                    state["wait"] = 1
                    return
                continue
            if cmd == "until":                  # until STATE[,STATE...] [MAX_FRAMES]
                states, _, limit = arg.partition(" ")
                state["until"] = ({int(x) for x in states.split(",")}, int(limit or 3000))
                return
            if cmd == "digits":                 # digits 1234: the number keys, one per tick
                state["queue"] = [48 + int(ch) for ch in arg]
                return
            if cmd == "type":                   # type TEXT: the PC keyboard (Canvas.text_input)
                state["queue"] = [("text", ch) for ch in arg]
                return
            if cmd == "bot_invite":             # bot_invite MODE: the first bot invites TEST
                from pow.midp.transport import LocalTransport
                LocalTransport._bots[0].invite("TEST", int(arg or 0))
                continue
            if cmd == "bot_order":              # bot_order NAME [N]: the first bot creates an order
                from pow.midp.transport import LocalTransport
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
                from pow.midp.transport import LocalTransport
                from pow_server import messages as M
                channel, _, text = arg.partition(" ")
                peer = ""
                if channel == "2":
                    peer, _, text = text.partition(" ")
                bot = LocalTransport._bots[0]
                bot.session.chat_rate.times.clear()
                bot._send(M.CHAT_SEND, channel=int(channel), peer=peer, text=text)
                continue
            if cmd == "mp_online":              # TEST-ONLY: mp_online ID - stop unless ID is logged in
                from pow.midp.transport import LocalTransport
                srv = LocalTransport._server
                if srv is None or arg not in srv.online or not srv.storage.has_account(arg):
                    raise SystemExit(f"mp_online {arg}: not logged in on the in-game server")
                print(f"mp_online {arg}: ok")
                continue
            raise SystemExit(f"unknown step: {cmd} {arg}")
        GameCanvas.running = False

    def _mp_canvas():
        return GameCanvas.online.mp if GameCanvas.online is not None else Midlet.canvas

    def _mp_state():
        """The state of the multiplayer screens, None outside them."""
        if GameCanvas.online is None:
            return None
        from pow.game.online.mp_canvas import MpCanvas
        return MpCanvas.state

    display.frame_hooks.append(on_frame)
    midlet = Midlet()
    asyncio.run(midlet.startApp())
    display.frame_hooks.remove(on_frame)
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
