"""Writing the notes down: note names, bars and beats, and the parts every tune shares
(a bandura pattern over chords, a sopilka phrase, the choir, the drone)."""

import numpy as np

import synth
from mix import spread

STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(name):
    """"A4" -> 69, "G#3" -> 56, "Bb2" -> 46."""
    step = STEPS[name[0]]
    rest = name[1:]
    while rest and rest[0] in "#b":
        step += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return step + 12 * (int(rest) + 1)


def hz(name):
    return 440.0 * 2 ** ((midi(name) - 69) / 12)


class Meter:
    """Where bar b (from 1), beat x (from 0) falls, in seconds."""

    def __init__(self, bpm, beats):
        self.beat = 60.0 / bpm
        self.beats = beats

    def at(self, bar, beat=0.0):
        return ((bar - 1) * self.beats + beat) * self.beat

    def length(self, bars):
        return self.at(bars + 1)


def bandura(loop, meter, bar, pattern, chord, rng, velocity=0.55, gain=1.0, pan=0.0, room=0.3):
    """One bar of the bandura: pattern rows are (beat, chord tone index or indices,
    loudness), chord is the bar's notes from the bass up. The strings are let ring, the
    bass ones longest; two strings struck together are rolled a little, low to high."""
    for beat, tones, loud in pattern:
        tones = tones if isinstance(tones, tuple) else (tones,)
        for k, tone in enumerate(tones):
            pluck(loop, meter.at(bar, beat) + 0.018 * k, chord[tone], rng, velocity * loud,
                  gain=gain, pan=pan, room=room)


def pluck(loop, at, name, rng, velocity, gain=1.0, pan=0.0, room=0.3, ring=None):
    """One bandura string struck at `at` (a little early or late, as a hand is)."""
    low = midi(name) < 52
    v = velocity * rng.uniform(0.88, 1.08)
    sound = synth.pluck(hz(name), ring or (4.5 if low else 3.0), rng, velocity=v,
                        bright=0.3 + 0.35 * min(1.0, velocity * 1.4))
    loop.add(sound, at + rng.normal(0, 0.008), gain=gain, pan=pan + (midi(name) - 57) / 60,
             room=room)


def sopilka(loop, meter, bar, notes, rng, gain=1.0, pan=0.1, room=0.4, far=0.0):
    """A phrase from bar `bar`: notes are (name or None for a rest, beats) or
    (name, beats, grace note). A note shorter than 0.6 s is slurred to the next one; a
    longer one is tongued."""
    played = []
    t = 0.0
    for note in notes:
        name, length = note[0], note[1] * meter.beat
        if name is not None:
            at = t
            if len(note) > 2:
                played.append((at, 0.07, hz(note[2])))
                at += 0.07
            gap = 0.0 if length < 0.6 else 0.09
            played.append((at, t + length - at - gap, hz(name)))
        t += length
    loop.add(synth.flute(played, rng), meter.at(bar), gain=gain, pan=pan, room=room, far=far)


def choir(loop, at, length, chord, rng, vowel="u", singers=3, gain=1.0, room=0.5,
          attack=0.8, release=1.2):
    """The men's choir holding a chord: each note sung by a few men, a little apart in
    pitch and in time."""
    voices = []
    for name in chord:
        for _ in range(singers):
            late = rng.uniform(0, 0.08)
            v = synth.voice(hz(name) * synth.cents(rng.normal(0, 7)), length, rng, vowel=vowel,
                            velocity=rng.uniform(0.8, 1.0), attack=attack, release=release)
            voices.append(np.concatenate([np.zeros(synth.samples(late)), v]))
    rng.shuffle(voices)
    loop.add(spread(voices), at, gain=gain / np.sqrt(len(chord)), room=room)


def drone(loop, names, rng, gain=1.0, piece=24.0, overlap=6.0, room=0.35):
    """The lira's drone on `names` all through the loop: long bowed notes, each one
    fading into the next."""
    length = loop.n / synth.RATE
    pieces = max(2, int(np.ceil(length / (piece - overlap))))
    step = length / pieces
    for k, name in enumerate(names):
        for i in range(pieces):
            note = synth.bowed(hz(name), step, rng, velocity=1.0, attack=overlap, release=overlap,
                               vib=3.0, body="lira")
            loop.add(note, i * step, gain=gain, pan=-0.15 if k == 0 else 0.15, room=room)
