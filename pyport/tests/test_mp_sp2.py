"""PHASE_9 task 9.1: all 59 SP2 files of the multiplayer load, every frame lies on its sheet (06 §5.1)."""
import pathlib

import pygame

import config
from pow.game.online.sprite_frames import SpriteFrames

ROOT = pathlib.Path(config.MP_RES_ROOT)


def sheet_for(name):
    base = name.rsplit(".", 1)[0]
    for suffix in ("_basic", "_skill1", "_skill2"):
        base = base.replace(suffix, "")
    if base == "spreff3":                      # Soul aura: frames on spreff2 (06 §5.2)
        base = "spreff2"
    for cand in (base + ".png", base + "_r.png"):
        if (ROOT / cand).exists():
            return ROOT / cand
    raise AssertionError("no sheet for " + name)


def test_all_sp2():
    files = sorted(ROOT.glob("*.SP2"))
    assert len(files) == 59
    counts = {}
    for p in files:
        spr = SpriteFrames("/" + p.name)
        assert len(spr.data) == 1 + 6 * spr.count, p.name
        img = pygame.image.load(str(sheet_for(p.name)))
        w, h = img.get_size()
        for i in range(spr.count):
            assert spr.w[i] > 0 and spr.h[i] > 0, (p.name, i)
            assert spr.src_x[i] + spr.w[i] <= w and spr.src_y[i] + spr.h[i] <= h, (p.name, i)
        kind = p.name.rsplit("_", 1)[-1] if "_" in p.name else "single"
        counts.setdefault(kind, set()).add(spr.count)
        spr.free()
    assert counts["basic.SP2"] == {19} and counts["skill1.SP2"] == {47} and counts["skill2.SP2"] == {47}
