"""Options volume -> pygame gain (pow/midp/media.py, PORT-EXTRA config.VOLUME_CURVE)."""
from conftest import ROOT  # noqa: F401  (sets sys.path and the dummy drivers)


def test_gain_curve(monkeypatch):
    import config
    from pow.midp.media import gain
    monkeypatch.setattr(config, "VOLUME_CURVE", True)
    assert [gain(v) for v in (0, 25, 50, 75, 100)] == [0.0, 0.0625, 0.25, 0.5625, 1.0]
    assert gain(-5) == 0.0 and gain(150) == 1.0
    monkeypatch.setattr(config, "VOLUME_CURVE", False)
    assert gain(25) == 0.25


def test_saved_volume_used_on_first_sound(tmp_path, monkeypatch):
    """gamevil_pow_env (load_options) -> volume -> Sound.play_now -> PlayerPool: the first sound."""
    import config
    from pow.game.game_canvas import GameCanvas
    from pow.game.player_pool import PlayerPool
    from pow.game.sound import Sound
    monkeypatch.setattr(config, "SAVE_DIR", str(tmp_path))
    monkeypatch.setattr(config, "VOLUME_CURVE", True)
    monkeypatch.setattr(GameCanvas, "volume", 50)
    monkeypatch.setattr(GameCanvas, "speed", 1)
    GameCanvas.save_options()
    monkeypatch.setattr(GameCanvas, "volume", 0)
    monkeypatch.setattr(GameCanvas, "save_pos", 0)
    GameCanvas.load_options()
    assert GameCanvas.volume == 50
    monkeypatch.setattr(Sound, "players", PlayerPool(17, 1, True, True))
    snd = Sound.__new__(Sound)
    snd.play_now(0, True)
    assert Sound.players.players[0] is not None and abs(Sound.players.players[0].get_volume() - 0.25) < 0.01
    Sound.stop_all()


def test_mp_volume_applies_to_playing_sound():
    """c.java a(int): setLevel also on the Player that is playing now."""
    from pow.midp.media import gain
    from pow_mp.player_pool import PlayerPool
    pool = PlayerPool(4, 1, True, True)
    assert pool.load("/snd3.wav", 3)
    pool.play(3, True)
    pool.set_volume(40)
    assert abs(pool.snd[3].get_volume() - gain(40)) < 0.01
    pool.stop()
