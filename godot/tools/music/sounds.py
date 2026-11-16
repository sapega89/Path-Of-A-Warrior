"""Makes the game's sound effects in code, with the instruments of synth.py, into
godot/client/assets/sound/sfx_<n>.wav (n is the number the game plays them by, MapSim.sound).

    pip install numpy scipy
    python godot/tools/music/sounds.py              # all of them
    python godot/tools/music/sounds.py 3 15         # just these

Nothing is recorded: a hit is a falling thump with a burst of noise, steel is a few
inharmonic partials that ring off fast, a whoosh is noise through a moving band, a blast is a
boom under noise that darkens, a chime is a small bell, the horns are a sawtooth through a
lowpass. The same seed makes the same files every time.
"""

import argparse
import pathlib
import sys
import wave

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import synth  # noqa: E402
from synth import RATE, bandpass, decay, fade, highpass, lowpass, noise, samples  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[2] / "client" / "assets" / "sound"
SEED = 3016


def _t(n):
    return np.arange(n) / RATE


def sweep(start_hz, end_hz, seconds, curve=2.0):
    """A sine whose pitch falls (or rises) from start_hz to end_hz, fast at first."""
    n = samples(seconds)
    k = np.linspace(0.0, 1.0, n) ** (1.0 / curve)
    hz = start_hz + (end_hz - start_hz) * k
    return np.sin(2 * np.pi * np.cumsum(hz) / RATE)


def thump(start_hz, end_hz, seconds, t60):
    n = samples(seconds)
    return sweep(start_hz, end_hz, seconds) * decay(n, t60)


def burst(seconds, t60, rng, low=None, high=None):
    """Noise that dies away, through a lowpass and / or a highpass."""
    n = samples(seconds)
    x = noise(n, rng)
    if high is not None:
        x = highpass(x, high)
    if low is not None:
        x = lowpass(x, low)
    return x * decay(n, t60)


def steel(partials, seconds, rng):
    """Struck steel: (hz, amplitude, t60) partials, each a hair out of tune with itself."""
    n = samples(seconds)
    t = _t(n)
    y = np.zeros(n)
    for hz, amp, t60 in partials:
        for split in (-0.002, 0.002):
            phase = rng.uniform(0, 2 * np.pi)
            y += amp * 0.5 * np.sin(2 * np.pi * hz * (1 + split) * t + phase) * decay(n, t60)
    return y


def moving_band(x, start_hz, mid_hz, end_hz, q, steps=48):
    """x through a band-pass whose middle goes start -> mid -> end, a piece at a time."""
    n = x.size
    out = np.zeros(n)
    edges = np.linspace(0, n, steps + 1).astype(int)
    for i in range(steps):
        k = 2.0 * i / max(1, steps - 1)
        if k < 1.0:
            hz = start_hz + (mid_hz - start_hz) * k
        else:
            hz = mid_hz + (end_hz - mid_hz) * (k - 1.0)
        a, b = edges[i], edges[i + 1]
        pad = min(a, samples(0.01))
        piece = bandpass(x[a - pad:b], hz, q)
        out[a:b] = piece[pad:]
    return out


def horn(hz, seconds, rng, bright=1800.0, attack=0.04, release=0.25):
    """A low brass note: a sawtooth with a little vibrato through a lowpass."""
    n = samples(seconds)
    freq = np.full(n, float(hz)) * synth.vibrato(n, 5.0, 12.0, 0.15, rng)
    y = lowpass(synth.saw(freq, rng), bright, order=2)
    return y * fade(n, attack, release)


def crackle(seconds, density, rng):
    """Sparse clicks, as wood bursting in a fire."""
    n = samples(seconds)
    y = np.zeros(n)
    hits = rng.random(n) < density / RATE
    y[hits] = rng.uniform(-1, 1, hits.sum())
    return highpass(y, 1500)


def mixdown(parts, seconds):
    n = samples(seconds)
    y = np.zeros(n)
    for start, part, gain in parts:
        a = samples(start)
        b = min(n, a + part.size)
        y[a:b] += part[: b - a] * gain
    return y


# ---- the effects -----------------------------------------------------------------------


def hit(rng):
    """3: a blow lands (on an enemy, a barrel, from a scroll)."""
    s = 0.18
    return mixdown(
        [
            (0, thump(150, 55, s, 0.07), 1.0),
            (0, burst(0.06, 0.025, rng, low=2600, high=500), 0.8),
        ],
        s,
    )


def hurt(rng):
    """4: the hero is hit, or a fire scroll bursts on an enemy."""
    s = 0.28
    grunt_n = samples(0.16)
    grunt = synth.formants(
        synth.saw(np.linspace(170, 115, grunt_n), rng), [(520, 90, 0), (1150, 140, -6)]
    ) * decay(grunt_n, 0.1)
    return mixdown(
        [
            (0, thump(115, 42, s, 0.12), 1.0),
            (0, burst(0.1, 0.05, rng, low=900), 0.7),
            (0.01, grunt, 0.35),
        ],
        s,
    )


def room_clear(rng):
    """5: the room is clear: three horn notes rise, the last one stays."""
    s = 1.4
    notes = [(0.0, 146.8, 0.24), (0.16, 174.6, 0.24), (0.32, 220.0, 1.0)]
    parts = [(at, horn(hz, length, rng, release=0.5), 0.6) for at, hz, length in notes]
    parts.append((0.32, horn(293.7, 1.0, rng, bright=1400, release=0.6), 0.3))
    parts.append((0, synth.drum("bubon", rng, 0.7)[: samples(s)], 0.5))
    return mixdown(parts, s)


def mission_lost(rng):
    """6: the hero falls: three low notes sink under a drum."""
    s = 1.7
    notes = [(0.0, 220.0, 0.4), (0.35, 174.6, 0.4), (0.7, 146.8, 1.0)]
    parts = [(at, horn(hz, length, rng, bright=900, release=0.6), 0.6) for at, hz, length in notes]
    parts.append((0, synth.drum("tulumbas", rng, 0.9)[: samples(s)], 0.8))
    return mixdown(parts, s)


def whoosh(rng):
    """7: a blade or a dash cuts the air."""
    s = 0.32
    n = samples(s)
    air = lowpass(moving_band(noise(n, rng), 500, 2400, 900, 2.2), 4500)
    return air * fade(n, 0.09, 0.2)


def chime(rng):
    """8: a potion, a heal, the volume being set: two small bell notes."""
    s = 0.85
    return mixdown(
        [
            (0, synth.bell(659.3, rng, 0.8, 0.85), 0.55),
            (0.11, synth.bell(987.8, rng, 0.8, 0.74), 0.45),
        ],
        s,
    )


def blast(rng):
    """9: a big blow: a boom under noise that darkens, with sparks."""
    s = 1.35
    n = samples(s)
    rumble = noise(n, rng)
    dark = np.zeros(n)
    for i, hz in enumerate(np.geomspace(4000, 260, 24)):
        a, b = i * n // 24, (i + 1) * n // 24
        pad = min(a, samples(0.01))
        dark[a:b] = lowpass(rumble[a - pad:b], hz)[pad:]
    return mixdown(
        [
            (0, thump(85, 28, s, 0.55), 1.0),
            (0, dark * decay(n, 0.8), 0.8),
            (0.02, crackle(0.6, 40, rng) * decay(samples(0.6), 0.4), 0.4),
        ],
        s,
    )


def cast(rng):
    """11: a skill is called up: a shimmer that rises."""
    s = 1.15
    n = samples(s)
    y = np.zeros(n)
    for detune in (0.995, 1.0, 1.006):
        y += sweep(260 * detune, 880 * detune, s, curve=0.8)
    y *= 0.5 + 0.5 * np.sin(2 * np.pi * np.linspace(5, 13, n) * _t(n))
    air = lowpass(highpass(noise(n, rng), 2500), 7000) * np.linspace(0.0, 1.0, n) ** 2
    return (y * 0.3 + air * 0.08) * fade(n, 0.35, 0.3)


def buff(rng):
    """12: a buff takes hold: a low chord swells under a ring."""
    s = 1.2
    n = samples(s)
    chord = sum(
        horn(hz, s, rng, bright=1300, attack=0.3, release=0.6) for hz in (73.4, 110.0, 146.8)
    )
    ring = synth.bell(587.3, rng, 0.6, s) * 0.25
    return chord * 0.35 + ring * fade(n, 0.2, 0.5)


def fire(rng):
    """13: fire flares up: a roar that opens, with crackle."""
    s = 0.8
    n = samples(s)
    roar = lowpass(moving_band(noise(n, rng), 300, 1600, 700, 0.9), 4500)
    return mixdown(
        [
            (0, roar * fade(n, 0.06, 0.45), 1.0),
            (0, crackle(s, 70, rng) * fade(n, 0.05, 0.4), 0.5),
            (0, thump(70, 40, 0.4, 0.2), 0.4),
        ],
        s,
    )


def thunder(rng):
    """14: lightning: a crack, then a rumble that rolls."""
    s = 1.45
    n = samples(s)
    crack = burst(0.08, 0.03, rng, low=6000, high=1800)
    roll = lowpass(np.cumsum(noise(n, rng)) * 0.02, 220, order=2)
    roll = highpass(roll, 30)
    roll *= decay(n, 1.1) * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * _t(n)) ** 2)
    roll /= max(1e-9, np.abs(roll).max())
    return mixdown([(0, crack, 0.6), (0.03, roll, 1.0)], s)


## The partials of a sabre: (hz, amplitude, t60 s).
SABRE = [(1180, 1.0, 0.11), (1760, 0.7, 0.08), (2710, 0.5, 0.06), (3950, 0.3, 0.04)]


def sabre(rng):
    """15: a sabre strikes: steel rings off fast."""
    s = 0.24
    return mixdown(
        [
            (0, steel(SABRE, s, rng), 0.7),
            (0, burst(0.03, 0.01, rng, low=7000, high=2500), 0.4),
            (0, thump(160, 80, 0.1, 0.04), 0.4),
        ],
        s,
    )


def heavy(rng):
    """16: a heavy blow (a pike, a block, a skill that throws back)."""
    s = 0.34
    return mixdown(
        [
            (0, steel([(610, 1.0, 0.16), (950, 0.6, 0.12), (1520, 0.4, 0.08)], s, rng), 0.6),
            (0, thump(95, 38, s, 0.14), 1.0),
            (0, burst(0.05, 0.02, rng, low=3000, high=400), 0.5),
        ],
        s,
    )


EFFECTS = {
    3: hit,
    4: hurt,
    5: room_clear,
    6: mission_lost,
    7: whoosh,
    8: chime,
    9: blast,
    11: cast,
    12: buff,
    13: fire,
    14: thunder,
    15: sabre,
    16: heavy,
}
## The peak of each, dBFS: the short hits a little under the big ones.
PEAK_DB = {3: -3, 4: -3, 7: -4, 8: -4, 15: -4, 16: -3}


def write_wav(path, mono):
    pcm = (np.clip(mono, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(pcm.tobytes())


def build(n, out):
    y = EFFECTS[n](np.random.default_rng(SEED + n))
    y = y * fade(y.size, 0.001, 0.01)
    y *= 10 ** (PEAK_DB.get(n, -1.5) / 20) / max(1e-9, np.abs(y).max())
    write_wav(out / f"sfx_{n}.wav", y)
    print(f"sfx_{n}.wav: {y.size / RATE:.2f} s, {EFFECTS[n].__doc__.split(': ', 1)[1]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "numbers", nargs="*", type=int, help="of %s (all when none)" % sorted(EFFECTS)
    )
    parser.add_argument("--out", type=pathlib.Path, default=OUT)
    args = parser.parse_args()
    unknown = [n for n in args.numbers if n not in EFFECTS]
    if unknown:
        parser.error("no such effect: %s" % unknown)
    args.out.mkdir(parents=True, exist_ok=True)
    for n in args.numbers or sorted(EFFECTS):
        build(n, args.out)


if __name__ == "__main__":
    main()
