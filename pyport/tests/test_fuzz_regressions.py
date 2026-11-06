"""Random key sequences that once crashed the game loop (-B8); each must now run to the end."""
import os
import subprocess
import sys

import pytest
from conftest import ROOT

FUZZ = ROOT / "tests" / "fuzz"


@pytest.mark.parametrize("name", sorted(p.stem for p in FUZZ.glob("*.keys")))
def test_random_keys_do_not_crash(name, tmp_path):
    env = dict(os.environ, POW_DEBUG="1")   # an exception in the game loop fails the run
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "shot.py"), str(FUZZ / (name + ".keys")),
                        "--out", str(tmp_path)], capture_output=True, text=True, check=False, timeout=300, env=env)
    assert r.returncode == 0, r.stderr[-2000:]
