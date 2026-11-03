"""PORT-EXTRA auto-hunt (pow/game/autopilot.py) on the real game loop: tools/scenarios/autohunt.keys
turns it on in the first mission and checks with `expect` steps that it kills, drinks the HP potion
without MP, casts the heal with MP and clears rooms one after another."""
import os
import subprocess
import sys

import pytest

from conftest import ROOT


@pytest.mark.parametrize("name", ["autohunt", "autohunt_belt"])
def test_autohunt_scenario(tmp_path, name):
    env = dict(os.environ, POW_STRICT="1")
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "shot.py"),
                        str(ROOT / "tools" / "scenarios" / (name + ".keys")), "--out", str(tmp_path)],
                       capture_output=True, text=True, timeout=300, env=env)
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
