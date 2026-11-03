"""PHASE_0 tasks 0.3-0.5: shim, font, .scr."""
import zlib

import pygame
from conftest import ROOT

RES = ROOT.parent


def test_scr_counts():  # task 0.5 / PHASE_1 §6
    from pow.data import scr
    assert len(scr.load(RES / "uimenu.scr")) == 60
    assert len(scr.load(RES / "gamestr.scr")) == 71
    assert len(scr.load(RES / "text.scr")) == 72
    assert scr.load(RES / "uimenu.scr")[39] == "Buy Item|Sell Item|Enchant Item|Combine Items"


def test_al_matches_loader():  # al.java reads the same strings as the stand-alone loader
    from pow.data import scr
    from pow.game.scr_table import ScrTable
    ref = scr.load(RES / "uimenu.scr")
    a = ScrTable("/uimenu.scr")
    assert [a.get(i) for i in range(60)] == ref


def test_crc_is_crc32():  # x.java:108-129
    from pow.game.gfx import Gfx
    data = bytearray(b"PLTE\x01\x02\x03\x04\x05\x06\x07")
    assert Gfx.crc32(data, 0, 10) == zlib.crc32(bytes(data[:10]))


def test_java_ints():
    from pow.midp.jint import i8, i16, i32, idiv, imod, ushr32
    from pow.midp.jrandom import Random
    assert (i8(200), i16(40000), i32(2 ** 31)) == (-56, -25536, -2 ** 31)
    assert (idiv(-7, 2), imod(-7, 2)) == (-3, -1)
    assert ushr32(-1, 28) == 15
    assert Random(42).nextInt() == -1170105035


def test_font_widths_and_colours(display):  # task 0.4
    from pow.game.font import Font
    from pow.game.gfx import Gfx
    from pow.midp.graphics import Graphics
    colours = {"white": 16777215, "black": 0, "orange": 16400640, "grey": 6579300}
    surf = pygame.Surface((240, 100))
    for n, (name, rgb) in enumerate(colours.items()):
        f = Font("/0_font.png", 8, 17, 9, rgb)
        assert f.string_width("RESUME") == 6 * 9          # glyph 8 px + 1 px gap
        assert f.string_width("A B") == 9 + 9 + 9          # ' ' is 9 px wide (d)
        surf.fill((0, 128, 0))
        Gfx.set_graphics(Graphics(surf))
        Gfx.set_font(f)
        Gfx.draw_string("RESUME", 120, 10, 1)           # anchor 1 = HCENTER
        found = {tuple(surf.get_at((px, py)))[:3] for px in range(93, 147) for py in range(10, 27)}
        assert ((rgb >> 16) & 255, (rgb >> 8) & 255, rgb & 255) in found, name
        assert surf.get_at((92, 15))[:3] == (0, 128, 0)   # nothing left of the centred text


def test_clip_draw_restores_clip(display):  # x.java:63-67
    from pow.game.gfx import Gfx
    from pow.midp.graphics import Graphics, Image
    surf = pygame.Surface((240, 320))
    gr = Graphics(surf)
    Gfx.set_graphics(gr)
    img = Image.createImage(20, 20)
    Gfx.draw_image_part(img, 5, 5, 4, 4, 0, 0)
    assert (gr.getClipX(), gr.getClipY(), gr.getClipWidth(), gr.getClipHeight()) == (0, 0, 240, 320)
    assert surf.get_at((5, 5))[:3] == (255, 255, 255) and surf.get_at((9, 9))[:3] == (0, 0, 0)


def test_drawrect_is_w_plus_1(display):  # MIDP drawRect covers w+1 x h+1; x.a(5 ints) passes w-1
    from pow.game.gfx import Gfx
    from pow.midp.graphics import Graphics
    surf = pygame.Surface((50, 50))
    Gfx.set_graphics(Graphics(surf))
    Gfx.draw_rect(10, 10, 5, 5, 0xFFFFFF)
    assert surf.get_at((14, 14))[:3] == (255, 255, 255)
    assert surf.get_at((15, 15))[:3] == (0, 0, 0)


def test_rms_roundtrip(tmp_path, monkeypatch):  # task 0.8 (desktop side)
    import config
    from pow.midp.rms import RecordStore
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    rs = RecordStore.openRecordStore("gamevil_pow_env", True)
    data = bytearray([75, 2])
    rs.addRecord(data, 0, 2)
    assert RecordStore.openRecordStore("gamevil_pow_env", False).getRecord(1) == data


def test_rms_browser_branch(monkeypatch):  # task 0.8: the localStorage path, with a fake JS window
    import sys
    import types

    from pow.midp import rms

    store = {}

    class LS:
        def getItem(self, k):
            return store.get(k)

        def setItem(self, k, v):
            store[k] = v

        def removeItem(self, k):
            store.pop(k, None)

    fake = types.SimpleNamespace(window=types.SimpleNamespace(localStorage=LS()))
    monkeypatch.setitem(sys.modules, "platform", fake)
    monkeypatch.setattr(rms, "_IS_WEB", True)
    rs = rms.RecordStore.openRecordStore("gamevil_pow_data", True)
    rs.addRecord(bytearray(range(256)) * 4, 0, 965)
    again = rms.RecordStore.openRecordStore("gamevil_pow_data", False).getRecord(1)
    assert len(again) == 965 and again[:256] == bytearray(range(256))
    assert "rms_gamevil_pow_data" in store


def test_window_scale(monkeypatch):  # task 0.2: 240x320 x2 / x3, nearest neighbour
    import subprocess
    import sys
    code = (f"import os,sys;sys.path.insert(0,{str(ROOT)!r});import config;from pow.midp import display;"
            "display.init(headless=True);print(display.window.get_size())")
    for scale, size in (("2", "(480, 640)"), ("3", "(720, 960)")):
        env = dict(__import__("os").environ, POW_SCALE=scale)
        out = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=False).stdout
        assert size in out
