"""Headless runs of the scenarios compared with the committed screenshots (task 0.7).

The committed PNGs in pyport/shots/ are the port's own output (regression baseline).
When reference screenshots from KEmulator are available they go to pyport/shots_ref/
and tools/compare_ref.py reports the difference.
"""
import pathlib

import pygame
import pytest

from conftest import ROOT

SCEN = ROOT / "tools" / "scenarios"


def _run(name, out):
    import os
    import subprocess
    import sys
    env = dict(os.environ, POW_STRICT="1")          # a NotPorted path fails the test
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "shot.py"), str(SCEN / (name + ".keys")),
                        "--out", str(out)], capture_output=True, text=True, timeout=300, env=env)
    assert r.returncode == 0, r.stderr


@pytest.mark.parametrize("name", ["title", "gamemenu", "mouse", "newgame", "newgame_mouse",
                                  "options_help", "management", "menus_mouse"])
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


def test_blacksmith_runs(tmp_path):
    """The Blacksmith stock and the enchant result use ag.C(int) = the time-seeded ag.by Random, so its
    screenshots differ from run to run: only check that every step runs and every shot exists."""
    out = tmp_path / "blacksmith"
    _run("blacksmith", out)
    base = ROOT / "shots" / "blacksmith"
    assert sorted(p.name for p in base.glob("*.png")) == sorted(p.name for p in out.glob("*.png"))
