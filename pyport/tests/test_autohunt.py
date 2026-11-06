"""auto-hunt (pow/game/autopilot.py) on the real game loop: tools/scenarios/autohunt.keys
turns it on in the first mission and checks with `expect` steps that it kills, drinks the HP potion
without MP, casts the heal with MP and clears rooms one after another."""
import os
import subprocess
import sys

import pytest
from conftest import ROOT


@pytest.mark.parametrize("name", ["autohunt", "autohunt_belt"])
def test_autohunt_scenario(tmp_path, name):
    env = dict(os.environ, POW_DEBUG="1")
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "shot.py"),
                        str(ROOT / "tools" / "scenarios" / (name + ".keys")), "--out", str(tmp_path)],
                       capture_output=True, text=True, check=False, timeout=300, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.count("expect ") == 5, r.stdout


def test_autohunt_is_off_by_default_and_toggles():
    from pow.game.autopilot import Autopilot
    from pow.game.game_canvas import GameCanvas
    Autopilot.reset()
    assert not Autopilot.on and Autopilot.tick() is None and Autopilot.direction is None
    GameCanvas.key_down(GameCanvas, -100)          # Tab / the AUTO corner
    assert Autopilot.on
    Autopilot.player_key()
    assert Autopilot.manual > 0
    GameCanvas.key_down(GameCanvas, -100)
    assert not Autopilot.on


def test_auto_keys_tab_f_and_the_right_stick():
    import pygame

    from pow.midp import canvas, gamepad
    assert canvas.KEYMAP[pygame.K_TAB] == canvas.KEYMAP[pygame.K_f] == -100
    assert gamepad.CONTROLLER_BUTTONS[pygame.CONTROLLER_BUTTON_RIGHTSTICK] == -100
    assert gamepad.JOYSTICK_BUTTONS[9] == -100


def test_the_auto_button_is_shown_while_off(tmp_path):
    """POW_AUTO_BUTTON=1 (the game's default): the grey AUTO button is on the map with the
    auto-hunt off, so a player can find it; a click on it turns the auto-hunt on."""
    scen = tmp_path / "btn.keys"
    src = (ROOT / "tools" / "scenarios" / "autohunt.keys").read_text(encoding="utf-8")
    head = src[:src.index("auto on")]
    scen.write_text("env POW_AUTO_BUTTON=1\n" + head + "wait 40\nshot off\nclick 20 312\nwait 40\n"
                    "shot on\nexpect kills >= 1\n", encoding="utf-8")
    env = dict(os.environ, POW_DEBUG="1", POW_AUTO_BUTTON="1")
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "shot.py"), str(scen), "--out",
                        str(tmp_path / "out")], capture_output=True, text=True, check=False, timeout=300, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    import pygame
    shots = sorted((tmp_path / "out").glob("*.png"))
    off = pygame.image.load(str(shots[-2]))
    on = pygame.image.load(str(shots[-1]))
    corner = lambda img: [img.get_at((x, 312))[:3] for x in range(4, 44)]   # noqa: E731
    assert corner(off) != [(0, 0, 0)] * 40           # something (the grey AUTO) is drawn
    assert corner(off) != corner(on)                 # grey -> white


def test_gives_up_on_an_enemy_it_comes_no_closer_to(monkeypatch):
    """An archer up on a wall: the hero goes to and fro at a corner below him and comes no
    closer. Each way around is longer than the one before (8, 16, 24, 32 ticks); after the
    fourth the autopilot leaves him alone in this room, and goes for him again in another."""
    from pow.game.autopilot import Autopilot
    from pow.game.game_canvas import GameCanvas
    from pow.game.structs import Point

    def actor(x, y):
        a = type("Actor", (), {})()
        a.pos = [Point(), Point()]
        a.pos[0].x, a.pos[0].y = x, y
        a.action = [1, 1]
        return a

    Autopilot.reset()
    monkeypatch.setattr(GameCanvas, "cell", 1)
    hero, archer = actor(306, 128), actor(363, 74)
    keys = []
    for t in range(600):
        if not Autopilot._hunted([archer]):
            break
        keys.append(Autopilot._walk(hero, archer))
        hero.pos[0].x = 312 if t % 2 == 0 else 306     # to and fro, never closer
    assert Autopilot._out_of_reach == [archer]
    runs, n = [], 1
    for a, b in zip(keys, keys[1:]):
        if a == b:
            n += 1
            continue
        if n >= 8:
            runs.append(n // 8)
        n = 1
    assert runs == [1, 2, 3, 4]
    assert keys[-1] is None                            # given up: no direction held
    monkeypatch.setattr(GameCanvas, "cell", 2)
    assert Autopilot._hunted([archer]) == [archer]
    Autopilot.reset()
