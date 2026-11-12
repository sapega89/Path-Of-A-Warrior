"""The mix of one tune: a loop of a fixed length that the notes are placed on.

The loop is a circle: a note that rings past the end goes on from the start, and the room
(the reverb) is a circular convolution, so the end of the file runs into its start without
a seam when the game loops it. A sound goes to the loop dry and, by its `room` amount, to
the reverb; `far` makes it distant (duller, quieter, more room).
"""

import subprocess
import wave

import numpy as np
from scipy import signal

from synth import RATE, decay, highpass, lowpass, noise, samples

TARGET_PEAK = 10 ** (-1.5 / 20)


class Loop:
    def __init__(self, seconds, rng, room_t60=3.0, room_tone=4500):
        self.n = samples(seconds)
        self.dry = np.zeros((2, self.n))
        self.send = np.zeros((2, self.n))
        self.rng = rng
        self.room_t60 = room_t60
        self.room_tone = room_tone

    def add(self, sound, at, gain=1.0, pan=0.0, room=0.25, far=0.0):
        """Places a mono or stereo sound at `at` seconds; pan -1 left .. 1 right."""
        if far > 0:
            sound = lowpass(sound, 7000 - 5000 * far, 1)
            gain *= 1 - 0.5 * far
            room = min(1.0, room + 0.6 * far)
        stereo = place(sound, pan) * gain
        self._wrap(self.dry, stereo * (1 - 0.5 * room - 0.4 * far), at)
        self._wrap(self.send, stereo * room, at)

    def _wrap(self, bus, sound, at):
        pos, done = samples(at) % self.n, 0
        while done < sound.shape[1]:
            take = min(sound.shape[1] - done, self.n - pos)
            bus[:, pos:pos + take] += sound[:, done:done + take]
            done += take
            pos = 0

    def render(self):
        """The finished loop, two channels."""
        ir = room_response(self.room_t60, self.room_tone, self.rng)
        wet = np.zeros_like(self.send)
        mixed = (self.send[0] + 0.3 * self.send[1], self.send[1] + 0.3 * self.send[0])
        for ch in range(2):
            wet[ch] = circular(mixed[ch], ir[ch], self.n)
        out = self.dry + wet
        return np.stack([circular_highpass(out[ch], 32) for ch in range(2)])


def place(sound, pan):
    """A mono sound panned with constant power, or a stereo one balanced by pan."""
    angle = (pan + 1) * np.pi / 4
    if sound.ndim == 1:
        return np.stack([sound * np.cos(angle), sound * np.sin(angle)]) * np.sqrt(2)
    return np.stack([sound[0] * np.cos(angle), sound[1] * np.sin(angle)]) * np.sqrt(2)


def spread(voices):
    """Stereo from mono voices spread evenly from left to right."""
    n = max(v.size for v in voices)
    out = np.zeros((2, n))
    for i, v in enumerate(voices):
        pan = 0.0 if len(voices) == 1 else -0.7 + 1.4 * i / (len(voices) - 1)
        out[:, : v.size] += place(v, pan)
    return out / np.sqrt(len(voices))


def room_response(t60, tone, rng):
    """A hall's impulse response for each ear: early echoes, then a diffuse tail that dulls
    as it fades (the high end dies three times faster than the low)."""
    n = samples(t60 * 1.3)
    t = np.arange(n) / RATE
    out = []
    for _ in range(2):
        hiss = noise(n, rng)
        low = lowpass(hiss, 700) * decay(n, t60)
        mid = (lowpass(hiss, tone) - lowpass(hiss, 700)) * decay(n, t60 * 0.6)
        high = (hiss - lowpass(hiss, tone)) * decay(n, t60 * 0.3)
        tail = (1.4 * low + mid + 0.3 * high) * np.clip((t - 0.02) / 0.06, 0, 1)
        for at, gain in ((0.011, 0.5), (0.019, 0.35), (0.027, 0.3), (0.041, 0.22), (0.053, 0.18)):
            tail[samples(at * rng.uniform(0.85, 1.15))] += gain * 6 * rng.choice((-1, 1))
        out.append(tail / np.sqrt(np.sum(tail**2)))
    return out


def circular(x, ir, n):
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir[:n], n), n)


def circular_highpass(x, hz):
    """The high-pass as if the loop had been playing before: run over two turns, keep the
    second."""
    return highpass(np.concatenate([x, x]), hz)[x.size:]


# --- loudness and files ----------------------------------------------------------------


def k_weighted(x):
    """The K-weighting of ITU-R BS.1770: a shelf up by 4 dB above 1.5 kHz and a high-pass
    at 38 Hz."""
    big = 10 ** (4.0 / 40)
    w = 2 * np.pi * 1681.97 / RATE
    alpha = np.sin(w) / 2 * np.sqrt(2)
    cw = np.cos(w)
    sq = 2 * np.sqrt(big) * alpha
    b = [big * ((big + 1) + (big - 1) * cw + sq), -2 * big * ((big - 1) + (big + 1) * cw),
         big * ((big + 1) + (big - 1) * cw - sq)]
    a = [(big + 1) - (big - 1) * cw + sq, 2 * ((big - 1) - (big + 1) * cw),
         (big + 1) - (big - 1) * cw - sq]
    y = signal.lfilter(b, a, x)
    b2, a2 = signal.butter(2, 38.13 / (RATE / 2), "high")
    return signal.lfilter(b2, a2, y)


def loudness(stereo):
    """Integrated loudness in LUFS (gated, as BS.1770-4)."""
    weighted = np.stack([k_weighted(ch) for ch in stereo])
    block, step = samples(0.4), samples(0.1)
    powers = np.array([
        np.sum(np.mean(weighted[:, i:i + block] ** 2, axis=1))
        for i in range(0, stereo.shape[1] - block, step)
    ])
    powers = powers[powers > 10 ** ((-70 + 0.691) / 10)]
    gate = 10 ** ((-0.691 + 10 * np.log10(np.mean(powers)) - 10 + 0.691) / 10)
    return -0.691 + 10 * np.log10(np.mean(powers[powers > gate]))


def master(stereo, lufs):
    """At `lufs` loudness, its peaks rounded off softly under -1.5 dBFS."""
    out = stereo * 10 ** ((lufs - loudness(stereo)) / 20)
    knee = TARGET_PEAK * 0.7
    over = np.abs(out) > knee
    soft = knee + (TARGET_PEAK - knee) * np.tanh((np.abs(out) - knee) / (TARGET_PEAK - knee))
    out[over] = np.sign(out[over]) * soft[over]
    return out


def write_wav(path, stereo):
    pcm = (np.clip(stereo.T, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(pcm.tobytes())


def write_ogg(path, wav_path, quality=5):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav_path), "-c:a", "libvorbis",
                    "-q:a", str(quality), str(path)], check=True)
