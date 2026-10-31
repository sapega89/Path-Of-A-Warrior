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


@pytest.mark.parametrize("name", ["title", "gamemenu", "mouse"])
def test_scenario_matches_baseline(name, tmp_path):
    import subprocess
    import sys
    out = tmp_path / name
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "shot.py"), str(SCEN / (name + ".keys")),
                        "--out", str(out)], capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    base = ROOT / "shots" / name
    names = sorted(p.name for p in base.glob("*.png"))
    assert names == sorted(p.name for p in out.glob("*.png"))
    for n in names:
        a = pygame.image.load(str(base / n))
        b = pygame.image.load(str(out / n))
        assert pygame.image.tobytes(a, "RGB") == pygame.image.tobytes(b, "RGB"), n
