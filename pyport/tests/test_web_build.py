"""The browser build: pygbag refuses to pack a WAV without an OGG of the same name."""
import importlib.util
import pathlib

import config
from pow_mp.player_pool import PlayerPool

PY = pathlib.Path(__file__).resolve().parents[1]


def _build_web(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("build_web", PY / "tools" / "build_web.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "OUT", tmp_path / "web-src")
    return mod


def test_every_multiplayer_wav_has_an_ogg():
    wavs = sorted((PY / "assets_mp").glob("*.wav"))
    assert wavs
    assert [w.name for w in wavs if not w.with_suffix(".ogg").exists()] == []


def test_the_browser_build_has_no_wav(tmp_path, monkeypatch):
    mod = _build_web(tmp_path, monkeypatch)
    mod.stage()
    out = tmp_path / "web-src"
    assert [str(p.relative_to(out)) for p in out.rglob("*") if p.suffix.lower() in (".wav", ".mp3", ".aiff")] == []
    assert (out / "res_mp" / "snd0.ogg").exists()


def test_the_multiplayer_effects_play_the_ogg_without_the_wav(tmp_path, monkeypatch):
    (tmp_path / "snd3.ogg").write_bytes(b"")
    monkeypatch.setattr(config, "MP_RES_ROOT", str(tmp_path))
    assert PlayerPool._path("/snd3.wav") == tmp_path / "snd3.ogg"
    (tmp_path / "snd3.wav").write_bytes(b"")
    assert PlayerPool._path("/snd3.wav") == tmp_path / "snd3.wav"      # the desktop: the original WAV
    assert PlayerPool._path("/snd1.mid") == tmp_path / "snd1.mid"
