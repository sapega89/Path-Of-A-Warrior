"""javax.microedition.media.control.VolumeControl -> pygame.mixer gain.

PORT-EXTRA (config.VOLUME_CURVE): VolumeControl.setLevel(0..100) on a phone is a loudness
scale, while pygame's set_volume() is a plain amplitude factor. The music is mastered at full
scale, so with level / 100 the Options steps 25 / 50 / 75 sound almost as loud as 100.
The square of the level makes each step a clear change: 25 -> -24 dB, 50 -> -12 dB, 75 -> -5 dB.
"""
import config


def gain(level):
    """VolumeControl level 0..100 -> pygame volume 0.0..1.0."""
    v = max(0, min(100, level)) / 100.0
    return v * v if config.VOLUME_CURVE else v
