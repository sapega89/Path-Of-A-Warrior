"""The instruments: each function returns one note (or one phrase) as mono samples at RATE.

Nothing here is recorded: the bandura is a plucked delay line (Karplus-Strong), the strings,
the lira and the voices are a sawtooth through resonances, the sopilka a few sines with
breath, the bells and the drums decaying partials, the wind filtered noise. mix.py places
the notes in stereo and adds the room.
"""

import numpy as np
from scipy import signal

RATE = 44100


def samples(seconds):
    return max(0, int(round(seconds * RATE)))


def cents(c):
    return 2.0 ** (c / 1200.0)


# --- filters ---------------------------------------------------------------------------


def lowpass(x, hz, order=2):
    b, a = signal.butter(order, min(hz, RATE * 0.45) / (RATE / 2), "low")
    return signal.lfilter(b, a, x)


def highpass(x, hz, order=2):
    b, a = signal.butter(order, hz / (RATE / 2), "high")
    return signal.lfilter(b, a, x)


def bandpass(x, hz, q):
    """A resonance at hz whose peak is 0 dB (RBJ band-pass)."""
    w = 2 * np.pi * hz / RATE
    alpha = np.sin(w) / (2 * q)
    b = [alpha, 0.0, -alpha]
    a = [1 + alpha, -2 * np.cos(w), 1 - alpha]
    return signal.lfilter(b, a, x)


def peak(x, hz, q, db):
    """Lifts (or cuts) a band round hz by db (RBJ peaking filter)."""
    big = 10 ** (db / 40)
    w = 2 * np.pi * hz / RATE
    alpha = np.sin(w) / (2 * q)
    b = [1 + alpha * big, -2 * np.cos(w), 1 - alpha * big]
    a = [1 + alpha / big, -2 * np.cos(w), 1 - alpha / big]
    return signal.lfilter(b, a, x)


def formants(x, table):
    """x through parallel resonances: table rows are (hz, bandwidth hz, gain dB)."""
    out = np.zeros_like(x)
    for hz, width, db in table:
        out += bandpass(x, hz, hz / width) * 10 ** (db / 20)
    return out


# --- shapes over time ------------------------------------------------------------------


def drift(n, rate, rng):
    """A smooth random curve in -1..1 that changes about `rate` times a second."""
    points = max(2, int(n / RATE * rate) + 2)
    knots = rng.uniform(-1, 1, points + 1)
    x = np.linspace(0, points - 1, n, endpoint=False) if n else np.zeros(0)
    i = x.astype(int)
    f = (1 - np.cos(np.pi * (x - i))) / 2
    return knots[i] * (1 - f) + knots[i + 1] * f


def fade(n, attack, release):
    """1 in the middle, rising over `attack` and falling over the last `release` seconds."""
    env = np.ones(n)
    a = min(n, samples(attack))
    r = min(n - a, samples(release))
    if a:
        env[:a] = (1 - np.cos(np.linspace(0, np.pi, a))) / 2
    if r:
        env[n - r:] *= (1 + np.cos(np.linspace(0, np.pi, r))) / 2
    return env


def decay(n, t60):
    """Falls by 60 dB in t60 seconds."""
    return np.exp(-6.91 * np.arange(n) / (t60 * RATE))


def vibrato(n, rate, depth_cents, onset, rng):
    """Pitch factor per sample: a vibrato that grows in after `onset` seconds, slightly
    uneven in speed and depth, as a player's is."""
    t = np.arange(n) / RATE
    speed = rate * (1 + 0.08 * drift(n, 0.7, rng))
    phase = 2 * np.pi * np.cumsum(speed) / RATE + rng.uniform(0, 2 * np.pi)
    grow = np.clip((t - onset) / 0.4, 0, 1) if onset > 0 else np.ones(n)
    depth = depth_cents * (1 + 0.25 * drift(n, 0.5, rng)) * grow
    return cents(depth * np.sin(phase))


# --- sources ---------------------------------------------------------------------------


def saw(freq, rng):
    """A band-limited sawtooth (PolyBLEP) following freq, an array of Hz per sample."""
    dt = freq / RATE
    t = (np.cumsum(dt) + rng.uniform(0, 1)) % 1.0
    y = 2 * t - 1
    lo = t < dt
    x = t[lo] / dt[lo]
    y[lo] -= 2 * x - x * x - 1
    hi = t > 1 - dt
    x = (t[hi] - 1) / dt[hi]
    y[hi] -= x * x + 2 * x + 1
    return y


def sines(freq, parts, rng):
    """Sum of harmonics following freq: parts are (harmonic number, amplitude)."""
    phase = 2 * np.pi * np.cumsum(freq) / RATE + rng.uniform(0, 2 * np.pi)
    out = np.zeros_like(freq)
    for k, amp in parts:
        out += amp * np.sin(k * phase)
    return out


def noise(n, rng):
    return rng.standard_normal(n)


# --- the instruments -------------------------------------------------------------------


def pluck(hz, ring, rng, velocity=0.8, bright=0.5, t60=None, spot=0.12):
    """A bandura string: rings for `ring` seconds, then is damped. Brighter when struck
    harder; the low strings ring longer."""
    period = RATE / hz - 0.5
    delay = int(period)
    frac = period - delay
    if t60 is None:
        t60 = float(np.clip(6.0 * (110 / hz) ** 0.4, 2.0, 8.0))
    g = 10 ** (-3.0 / (t60 * hz))
    taps = g * np.array([0.5 * (1 - frac), 0.5, 0.5 * frac])
    n = samples(ring + 0.15)
    burst = lowpass(rng.uniform(-1, 1, delay), 500 + 7000 * bright * velocity, 1)
    spot_at = max(1, int(spot * delay))
    burst[spot_at:] -= burst[:-spot_at].copy()
    burst -= burst.mean()
    y = np.zeros(n + delay + 2)
    y[delay + 2:delay + 2 + delay] = burst[: min(delay, n)]
    for start in range(delay + 2, n + delay + 2, delay):
        end = min(start + delay, n + delay + 2)
        y[start:end] += taps[0] * y[start - delay:end - delay] + taps[1] * y[
            start - delay - 1:end - delay - 1
        ] + taps[2] * y[start - delay - 2:end - delay - 2]
    y = y[delay + 2:]
    click = lowpass(noise(samples(0.004), rng), 3000) * 0.08
    y[: click.size] += click
    y = peak(y, 210, 1.4, 4.0)
    y = peak(y, 480, 1.8, 2.5)
    y = lowpass(y, 6500)
    y *= fade(n, 0.0, 0.15)
    return y * velocity / max(1e-9, np.abs(y).max())


def bowed(hz, length, rng, velocity=0.7, attack=0.25, release=0.6, vib=8.0, body="cello"):
    """A bowed low string (or the lira's drone with body="lira"), `length` seconds plus
    its release."""
    n = samples(length + release)
    freq = hz * vibrato(n, 5.0, vib, 0.3, rng) * cents(2.5 * drift(n, 0.4, rng))
    x = saw(freq, rng)
    if body == "lira":
        x = x * (1 + 0.05 * np.sin(2 * np.pi * 5.3 * np.arange(n) / RATE))
        x = formants(x, [(320, 120, 0), (900, 250, -3), (2100, 500, -8)]) + 0.15 * x
        x = lowpass(x, 2600)
    else:
        x = peak(x, 260, 1.5, 6)
        x = peak(x, 520, 2.0, 3)
        x = peak(x, 2800, 1.2, 2)
        x = lowpass(x, 1800 + 2200 * velocity)
    x += bandpass(noise(n, rng), 2500, 0.8) * 0.015
    x *= fade(n, attack, release) * (1 + 0.12 * drift(n, 1.5, rng))
    return x * velocity / max(1e-9, np.abs(x).max())


VOWELS = {  # a bass singer's formants: (Hz, bandwidth Hz, gain dB)
    "a": [(600, 90, 0), (1040, 100, -7), (2250, 160, -9), (2450, 170, -9), (2750, 190, -20)],
    "o": [(400, 70, 0), (750, 110, -11), (2400, 150, -21), (2600, 170, -20), (2900, 170, -40)],
    "u": [(330, 70, 0), (600, 110, -20), (2400, 150, -32), (2675, 170, -28), (2950, 170, -36)],
}


def voice(hz, length, rng, vowel="o", velocity=0.7, attack=0.4, release=0.8):
    """One male singer holding a vowel."""
    n = samples(length + release)
    t = np.arange(n) / RATE
    scoop = cents(-25 * np.exp(-t / 0.08))
    freq = hz * scoop * vibrato(n, rng.uniform(4.8, 5.8), 20, 0.35, rng)
    freq *= cents(5 * drift(n, 0.5, rng))
    x = lowpass(saw(freq, rng), 900, 1)
    x += lowpass(noise(n, rng), 4000) * 0.04
    y = formants(x, VOWELS[vowel]) + 0.04 * x
    y *= fade(n, attack, release) * (1 + 0.1 * drift(n, 2.5, rng))
    return y * velocity / max(1e-9, np.abs(y).max())


def flute(notes, rng, velocity=0.7, breath=0.06):
    """The sopilka playing a phrase: notes are (start s, length s, Hz) from the phrase's
    start. A note that begins less than 0.06 s after the one before is slurred to it (the
    pitch glides, the sound goes on); a longer gap is a new breath."""
    end = max(s + d for s, d, _ in notes) + 0.3
    n = samples(end)
    freq = np.full(n, notes[0][2])
    amp = np.zeros(n)
    t = np.arange(n) / RATE
    for i, (start, length, hz) in enumerate(notes):
        slur_in = i > 0 and start - sum(notes[i - 1][:2]) < 0.06
        slur_out = i + 1 < len(notes) and notes[i + 1][0] - (start + length) < 0.06
        a = samples(start)
        b = samples(notes[i + 1][0]) if slur_out else samples(start + length)
        freq[a:b] = hz
        if slur_in:
            prev = notes[i - 1][2]
            glide = min(b - a, samples(0.045))
            freq[a:a + glide] = prev * (hz / prev) ** np.linspace(0, 1, glide)
        else:
            freq[a:b] *= cents(-30 * np.exp(-(t[a:b] - start) / 0.05))
        env = fade(b - a, 0.0 if slur_in else 0.05, 0.0 if slur_out else 0.06)
        if slur_in:
            env *= 1 - 0.15 * np.exp(-(t[a:b] - start) / 0.03)
        amp[a:b] = env * (1 + 0.12 * np.sin(np.linspace(0, np.pi, b - a)))
        freq[a:b] *= vibrato(b - a, 5.2, 18, 0.3 if length > 0.5 else 9.0, rng)
    amp = lowpass(amp, 40)
    tone = sines(freq, [(1, 1.0), (2, 0.28), (3, 0.12), (4, 0.04)], rng)
    air = bandpass(noise(n, rng), 2000, 0.7) * breath * (0.4 + amp)
    y = tone * amp + air * (amp > 0.01)
    return lowpass(y, 7000) * velocity / max(1e-9, np.abs(y).max())


BELL = [  # partials of a minor-third bell from its strike note: (ratio, amplitude, t60 s)
    (0.5, 0.55, 14), (1.0, 0.45, 9), (1.2, 0.6, 7), (1.5, 0.22, 5), (2.0, 1.0, 4.5),
    (2.5, 0.35, 3.0), (2.67, 0.28, 2.6), (3.0, 0.22, 2.2), (4.0, 0.14, 1.6), (5.33, 0.08, 1.1),
]


def bell(hz, rng, velocity=0.8, length=10.0):
    """A church bell whose strike note is hz; the pairs of close partials beat slowly."""
    n = samples(length)
    t = np.arange(n) / RATE
    y = np.zeros(n)
    for ratio, amp, t60 in BELL:
        f = hz * ratio
        if f > RATE * 0.4:
            continue
        for split in (-0.0006, 0.0006):
            y += amp * 0.5 * np.sin(2 * np.pi * f * (1 + split) * t + rng.uniform(0, 6.3)) * decay(
                n, t60
            )
    strike = lowpass(noise(samples(0.03), rng), 3500) * decay(samples(0.03), 0.02)
    y[: strike.size] += strike * 0.3
    y *= fade(n, 0.002, 1.0)
    return y * velocity / max(1e-9, np.abs(y).max())


DRUMS = {  # modes of a drum head: (ratio, amplitude, t60 s), its pitch and skin noise
    "tulumbas": {"hz": 52, "modes": [(1, 1.0, 1.1), (1.59, 0.35, 0.6), (2.14, 0.22, 0.45),
                                     (2.3, 0.15, 0.35), (2.65, 0.1, 0.3)],
                 "skin": (300, 0.9, 0.06), "bend": 0.25},
    "litavra": {"hz": 82.4, "modes": [(1, 1.0, 1.6), (1.5, 0.5, 1.2), (1.99, 0.3, 0.9),
                                      (2.44, 0.18, 0.6), (2.9, 0.1, 0.4)],
                "skin": (700, 0.5, 0.04), "bend": 0.05},
    "bubon": {"hz": 150, "modes": [(1, 1.0, 0.35), (1.59, 0.5, 0.22), (2.14, 0.3, 0.15)],
              "skin": (1200, 0.6, 0.05), "bend": 0.08},
}


def drum(kind, rng, velocity=0.8, tune=1.0):
    """One stroke on a drum: the big tulumbas, the kettle drum (litavra) or the frame
    drum (bubon); a harder stroke bends the pitch more at first."""
    spec = DRUMS[kind]
    hz = spec["hz"] * tune
    n = samples(max(t for _, _, t in spec["modes"]) + 0.1)
    t = np.arange(n) / RATE
    bend = 1 + spec["bend"] * velocity * np.exp(-t / 0.04)
    y = np.zeros(n)
    for ratio, amp, t60 in spec["modes"]:
        phase = 2 * np.pi * np.cumsum(hz * ratio * bend) / RATE
        y += amp * np.sin(phase + rng.uniform(0, 6.3)) * decay(n, t60 * (0.8 + 0.3 * velocity))
    skin_hz, skin_amp, skin_t = spec["skin"]
    skin = bandpass(noise(n, rng), skin_hz, 0.9) * decay(n, skin_t) * skin_amp
    y += skin * (0.5 + velocity)
    y *= fade(n, 0.0015, 0.05)
    return y * velocity / max(1e-9, np.abs(y).max())


def wind(length, rng, level=1.0, bands=(180, 300, 500, 800, 1300, 2100)):
    """Wind over open ground: noise in a few bands whose loudness drifts, in gusts."""
    n = samples(length)
    base = lowpass(noise(n, rng), 3000, 1)
    gust = 0.55 + 0.45 * drift(n, 0.08, rng)
    y = np.zeros(n)
    for hz in bands:
        swell = (0.5 + 0.5 * drift(n, rng.uniform(0.1, 0.25), rng)) ** 2
        y += bandpass(base, hz, 1.3) * swell * (300 / hz) ** 0.4
    y *= gust
    return y * level / max(1e-9, np.abs(y).max())


def reeds(length, rng, level=1.0):
    """Reeds rustling: high noise that flutters faster than the wind."""
    n = samples(length)
    hiss = bandpass(noise(n, rng), 4500, 0.9)
    flutter = np.clip(0.5 + 0.7 * drift(n, 7.0, rng), 0, None) * (0.5 + 0.5 * drift(n, 0.12, rng))
    y = hiss * flutter**2
    return y * level / max(1e-9, np.abs(y).max())
