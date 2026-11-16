"""«Дума»: the title, the main menu and the talk in the story.

A kobzar's lament in D, 60 beats a minute, 20 bars (80 s): the lira holds D and A all
through, the bandura goes round the chords, a distant bell opens it. From bar 5 the sopilka
weeps in the Ukrainian Dorian mode (D E F G# A B C: the raised fourth that sobs), from bar 9
the men hum the chords under it and the tulumbas beats like a slow heart; the last four bars
are the bandura alone again, back to the start.
"""

from mix import Loop
from score import Meter, bandura, choir, drone, hz, sopilka
import synth

METER = Meter(60, 4)
BARS = 20
LUFS = -21.0

CHORDS = {  # from the bass up
    "Dm": ["D2", "A2", "D3", "A3", "D4", "F4"],
    "E": ["E2", "B2", "E3", "B3", "E4", "G#4"],
    "F": ["F2", "C3", "F3", "C4", "F4", "A4"],
    "Am": ["A1", "E2", "A2", "E3", "A3", "C4"],
}
HARMONY = ["Dm", "Dm", "F", "Dm", "Dm", "Dm", "E", "Dm", "Dm", "E", "F", "Am",
           "Dm", "E", "Am", "E", "Dm", "F", "Dm", "E"]
SPARSE = [(0, (0, 2), 1.0), (1, (3, 4), 0.6), (2, 1, 0.7), (2.5, 5, 0.5), (3, 4, 0.6)]
FLOWING = [(0, (0, 2), 1.0), (0.5, 3, 0.55), (1, 4, 0.6), (1.5, 5, 0.6), (2, 1, 0.75),
           (2.5, 5, 0.5), (3, 4, 0.55), (3.5, 3, 0.5)]
HUM = {"Dm": ["F3", "A3", "D4"], "E": ["E3", "G#3", "B3"], "F": ["F3", "A3", "C4"],
       "Am": ["E3", "A3", "C4"]}
LAMENT = [  # bars 5..16, four beats each
    [("A4", 2, "B4"), ("B4", 0.5), ("A4", 0.5), ("F4", 1)],
    [("E4", 1.5), ("F4", 0.5), ("D4", 2)],
    [("E4", 0.5), ("G#4", 0.5), ("B4", 1.5), ("A4", 0.5), ("G#4", 1)],
    [("A4", 1), ("F4", 0.5), ("E4", 0.5), ("D4", 2)],
    [("D5", 1.5, "E5"), ("C5", 0.5), ("A4", 1), ("F4", 1)],
    [("G#4", 1.5), ("A4", 0.5), ("B4", 1), ("G#4", 1)],
    [("A4", 1.5), ("C5", 0.5), ("A4", 1), ("F4", 1)],
    [("E4", 3), (None, 1)],
    [("A4", 1), ("D5", 1, "E5"), ("C5", 0.5), ("B4", 0.5), ("A4", 1)],
    [("G#4", 1.5), ("F4", 0.5), ("E4", 1), ("G#4", 1)],
    [("A4", 1), ("E4", 1), ("C5", 1), ("B4", 1)],
    [("G#4", 0.5), ("A4", 0.5), ("G#4", 0.5), ("F4", 0.5), ("E4", 2)],
]


def render(rng):
    loop = Loop(METER.length(BARS), rng, room_t60=3.6)
    drone(loop, ["D2", "A2"], rng, gain=0.14)
    loop.add(synth.wind(METER.length(BARS) + 1, rng), 0, gain=0.12, room=0.2)
    for at, loud in ((METER.at(1), 0.55), (METER.at(13), 0.45)):
        loop.add(synth.bell(hz("D4"), rng, velocity=loud), at, gain=0.6, pan=-0.3, room=0.5,
                 far=0.7)
    for bar, name in enumerate(HARMONY, start=1):
        pattern = FLOWING if 5 <= bar <= 16 else SPARSE
        bandura(loop, METER, bar, pattern, CHORDS[name], rng, velocity=0.42, gain=1.4,
                pan=-0.1)
    for i in range(0, len(LAMENT), 2):
        sopilka(loop, METER, 5 + i, LAMENT[i] + LAMENT[i + 1], rng, gain=0.34, pan=0.15)
    for bar in range(9, 17):
        name = HARMONY[bar - 1]
        choir(loop, METER.at(bar) - 0.3, METER.at(1, 4) + 0.3, HUM[name], rng, vowel="u",
              gain=0.13 if bar < 13 else 0.17)
        for beat, loud in ((0, 0.5), (0.45, 0.3)):
            loop.add(synth.drum("tulumbas", rng, velocity=loud), METER.at(bar, beat), gain=0.7,
                     room=0.3)
    return loop.render()
