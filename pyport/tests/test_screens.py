"""Headless runs of the scenarios compared with the committed screenshots (task 0.7).

The committed PNGs in pyport/shots/ are the port's own output (regression baseline).
When reference screenshots from KEmulator are available they go to pyport/shots_ref/
and tools/compare_ref.py reports the difference.
"""

import pygame
import pytest
from conftest import ROOT

SCEN = ROOT / "tools" / "scenarios"

# tools/shot.py seeds every java.util.Random with POW_SEED=1 instead of the clock, so the enemy AI,
# the Blacksmith stock and the gifts of the generals repeat exactly: every shot is compared.


def _run(name, out):
    import os
    import subprocess
    import sys
    env = dict(os.environ, POW_DEBUG="1")   # an exception in the game loop fails the test
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "shot.py"), str(SCEN / (name + ".keys")),
                        "--out", str(out)], capture_output=True, text=True, check=False, timeout=300, env=env)
    assert r.returncode == 0, r.stderr


@pytest.mark.parametrize("name", ["title", "gamemenu", "mouse", "newgame", "newgame_mouse",
                                  "options_help", "management", "menus_mouse",
                                  "missions", "missions_mouse", "visiting",
                                  "map", "map_mouse", "combat", "combat_mouse", "victory", "blacksmith",
                                  "gamevil_live", "multiplayer", "skill_bar", "skill_card", "respec"])
def test_scenario_matches_baseline(name, tmp_path):
    out = tmp_path / name
    _run(name, out)
    base = ROOT / "shots" / name
    names = sorted(p.name for p in base.glob("*.png"))
    assert names == sorted(p.name for p in out.glob("*.png"))
    for n in names:
        a = pygame.image.load(str(base / n))
        b = pygame.image.load(str(out / n))
        assert pygame.image.tobytes(a, "RGB") == pygame.image.tobytes(b, "RGB"), n

