"""«Похід»: the missions.

A march in E minor, 84 beats a minute, 32 bars (91 s), dark and steady rather than loud,
so that it does not tire over a long mission. The kettle drums (litavry) and the low
strings' gallop (one long, two short) run all through; the men's choir comes in on bar 5,
the bandura from bar 9 and with the tune, played tremolo, from bar 13. The tune turns to
A minor and to the Phrygian F (bars 21-28, the choir opens to "a" and the cellos double it),
then four bars of drums and strings lead back to the start.
"""

import numpy as np

from mix import Loop
from score import Meter, choir, drone, hz, pluck
import synth

METER = Meter(84, 4)
BARS = 32
LUFS = -22.0
SIXTEENTH = 0.25

HARMONY = (["Em"] * 4 + ["Em", "Em", "F", "Em"] + ["Em", "C", "D", "B"]
           + ["Em", "Em", "C", "C", "D", "D", "B", "B"]
           + ["Am", "Am", "Em", "Em", "F", "F", "B", "B"]
           + ["Em", "Em", "F", "B"])
ROOT = {"Em": "E2", "F": "F2", "C": "C2", "D": "D2", "B": "B1", "Am": "A1"}
VOICES = {  # the choir, from the bass up
    "Em": ["E3", "B3", "E4", "G4"], "F": ["F3", "C4", "F4", "A4"], "C": ["E3", "C4", "E4", "G4"],
    "D": ["D3", "A3", "D4", "F#4"], "B": ["F#3", "B3", "D#4", "F#4"], "Am": ["E3", "A3", "C4", "E4"],
}
STRUM = {"Em": ["E3", "B3", "E4", "G4"], "C": ["C3", "G3", "C4", "E4"],
         "D": ["D3", "A3", "D4", "F#4"], "B": ["B2", "F#3", "B3", "D#4"]}
KETTLE = [(0, 1.0, "E2"), (3, 0.4, "E2"), (4, 0.75, "B1"), (7, 0.4, "E2"), (8, 0.9, "E2"),
          (11, 0.45, "E2"), (12, 0.7, "B1"), (14, 0.5, "E2"), (15, 0.45, "E2")]
GALLOP = [(0, 1.0), (2, 0.6), (3, 0.7)]  # in each beat, sixteenths: one long, two short
THEME = [  # bars 13..28, four beats each
    [("E4", 1), ("G4", 1), ("B4", 1.5), ("A4", 0.5)],
    [("G4", 1), ("F#4", 0.5), ("G4", 0.5), ("E4", 2)],
    [("E4", 1), ("G4", 1), ("C5", 1.5), ("B4", 0.5)],
    [("A4", 1), ("G4", 0.5), ("A4", 0.5), ("E4", 2)],
    [("F#4", 1), ("A4", 1), ("D5", 1.5), ("C5", 0.5)],
    [("B4", 1), ("A4", 0.5), ("B4", 0.5), ("F#4", 2)],
    [("D#4", 1), ("F#4", 1), ("B4", 1.5), ("A4", 0.5)],
    [("G4", 1), ("F#4", 1), ("D#4", 1), ("B3", 1)],
    [("A4", 1), ("C5", 1), ("E5", 1.5), ("D5", 0.5)],
    [("C5", 1), ("B4", 0.5), ("C5", 0.5), ("A4", 2)],
    [("G4", 1), ("B4", 1), ("E5", 1.5), ("D5", 0.5)],
    [("B4", 1), ("A4", 0.5), ("B4", 0.5), ("G4", 2)],
    [("A4", 1), ("C5", 1), ("F5", 1), ("E5", 0.5), ("D5", 0.5)],
    [("C5", 1), ("A4", 1), ("F4", 2)],
    [("F#4", 1), ("A4", 1), ("B4", 1), ("D#5", 1)],
    [("B4", 2), ("A4", 0.5), ("G4", 0.5), ("F#4", 1)],
]


def render(rng):
    loop = Loop(METER.length(BARS), rng, room_t60=2.6)
    drone(loop, ["E2", "B2"], rng, gain=0.11)
    loop.add(synth.wind(METER.length(BARS) + 1, rng), 0, gain=0.08, room=0.2)
    loop.add(synth.bell(hz("E4"), rng, velocity=0.5), METER.at(29), gain=0.6, pan=0.3, room=0.5,
             far=0.7)
    for bar, chord in enumerate(HARMONY, start=1):
        drums(loop, bar, rng)
        gallop(loop, bar, ROOT[chord], rng)
        if bar >= 5:
            vowel = "a" if 21 <= bar <= 28 else ("u" if bar >= 29 else "o")
            loud = 0.19 if bar < 13 else (0.32 if vowel == "a" else 0.24)
            choir(loop, METER.at(bar) - 0.2, METER.at(1, 4) + 0.2, VOICES[chord], rng,
                  vowel=vowel, singers=2, gain=loud, attack=0.6, release=0.9)
        if 9 <= bar <= 12:
            for k, name in enumerate(STRUM[chord]):
                pluck(loop, METER.at(bar) + 0.03 * k, name, rng, 0.7, gain=0.8, pan=-0.2)
    at = METER.at(13)
    for bar_notes in THEME:
        for name, beats in bar_notes:
            tremolo(loop, at, beats * METER.beat, name, rng)
            at += beats * METER.beat
    at = METER.at(21)
    for bar_notes in THEME[8:]:
        for name, beats in bar_notes:
            low = hz(name) / 2
            note = synth.bowed(low, beats * METER.beat * 0.95, rng, velocity=0.8, attack=0.06,
                               release=0.25, vib=10.0)
            loop.add(note, at, gain=0.1, pan=0.25, room=0.4)
            at += beats * METER.beat
    return loop.render()


def drums(loop, bar, rng):
    """The kettle drums all through; the tulumbas on the downbeat from bar 9 (and on beat 3
    in bars 21-28); the frame drum's backbeat from bar 5; a roll into the start in bar 32."""
    pattern = KETTLE
    if bar == BARS:
        pattern = [(s, 0.35 + 0.04 * s, "E2") for s in range(16)]
    calm = 0.75 if bar >= 29 and bar < BARS else 1.0
    for step, loud, name in pattern:
        sound = synth.drum("litavra", rng, velocity=loud * rng.uniform(0.9, 1.05) * calm,
                           tune=hz(name) / 82.4)
        loop.add(sound, METER.at(bar, step * SIXTEENTH) + rng.normal(0, 0.005), gain=0.55,
                 pan=-0.25, room=0.3)
    if 9 <= bar <= 28:
        beats = (0, 2) if bar >= 21 else (0,)
        for beat in beats:
            loop.add(synth.drum("tulumbas", rng, velocity=0.85), METER.at(bar, beat), gain=0.7,
                     room=0.3)
    if 5 <= bar < 29:
        for step, loud in ((4, 0.7), (6, 0.25), (12, 0.75), (14, 0.25), (15, 0.2)):
            sound = synth.drum("bubon", rng, velocity=loud * rng.uniform(0.85, 1.1))
            loop.add(sound, METER.at(bar, step * SIXTEENTH) + rng.normal(0, 0.006), gain=0.3,
                     pan=0.35, room=0.25)


def gallop(loop, bar, root, rng):
    """The low strings, the root and its octave, one long and two short in every beat."""
    soft = 0.7 if bar >= 29 else 1.0
    for beat in range(4):
        for step, loud in GALLOP:
            at = METER.at(bar, beat + step * SIXTEENTH)
            length = 0.16 if step == 0 else 0.08
            for octave, pan in ((0, -0.15), (12, 0.15)):
                f = hz(root) * 2 ** (octave / 12)
                note = synth.bowed(f, length, rng, velocity=loud * soft * rng.uniform(0.85, 1.0),
                                   attack=0.008, release=0.12, vib=0.0)
                loop.add(note, at + rng.normal(0, 0.004), gain=0.22, pan=pan, room=0.25)


def tremolo(loop, at, length, name, rng):
    """The bandura's tremolo: the string struck again and again, in thirty-seconds, a
    short note just once."""
    stroke = METER.beat / 8
    if length < METER.beat:
        pluck(loop, at, name, rng, 0.75, gain=0.7, pan=0.15, ring=1.2)
        return
    count = int(round(length / stroke))
    swell = np.sin(np.linspace(0.3, np.pi - 0.3, count))
    for i in range(count):
        v = 0.35 + 0.25 * swell[i] + (0.15 if i == 0 else 0.0)
        pluck(loop, at + i * stroke, name, rng, v, gain=0.7, pan=0.15, ring=0.5)
