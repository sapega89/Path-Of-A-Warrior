"""«Плавні»: the camp on the marsh and its menus, the world map and the pictures of the story.

Night on the marsh in A minor, a slow 6/8 (46 dotted quarters a minute), 32 bars (83 s):
the bandura rocks alone over a quiet drone, wind and reeds; a bell far away on bar 9; from
bar 17 a sopilka across the water, ending on the E major chord of the harmonic minor that
pulls back to the start. The men hum under bars 13-16 and 29-32.
"""

from mix import Loop
from score import Meter, bandura, choir, drone, hz, sopilka
import synth

METER = Meter(138, 6)  # a beat is an eighth
BARS = 32
LUFS = -23.0

CHORDS = {  # from the bass up
    "Am": ["A1", "E2", "A2", "E3", "A3", "C4"],
    "G": ["G1", "D2", "G2", "D3", "G3", "B3"],
    "F": ["F2", "C3", "F3", "A3", "C4", "F4"],
    "C": ["C2", "G2", "C3", "G3", "C4", "E4"],
    "Dm": ["D2", "A2", "D3", "A3", "D4", "F4"],
    "E": ["E2", "B2", "E3", "B3", "E4", "G#4"],
}
HARMONY = [c for c in ["Am", "Am", "G", "Am", "F", "C", "Dm", "E",
                       "Am", "G", "F", "E", "Dm", "Am", "F", "E"] for _ in range(2)]
ROCK = [(0, (0, 2), 1.0), (1, 3, 0.55), (2, 4, 0.6), (3, (1, 5), 0.75), (4, 4, 0.5), (5, 3, 0.5)]
ANSWER = [(0, 2, 0.8), (1, 3, 0.5), (2, 5, 0.6), (3, 4, 0.65), (4, 3, 0.5), (5, 1, 0.5)]
HUM = {"Dm": ["F3", "A3", "D4"], "E": ["E3", "G#3", "B3"], "F": ["F3", "A3", "C4"]}
SONG = [  # bars 17..28, six eighths each
    [("E5", 3), ("D5", 1), ("C5", 1), ("B4", 1)],
    [("C5", 2), ("B4", 1), ("A4", 3)],
    [("B4", 2), ("C5", 1), ("D5", 3, "E5")],
    [("C5", 1), ("B4", 1), ("A4", 1), ("G4", 3)],
    [("A4", 3), ("C5", 2), ("A4", 1)],
    [("G4", 1), ("F4", 1), ("G4", 1), ("A4", 3)],
    [("G#4", 3), ("B4", 2), ("D5", 1)],
    [("C5", 1), ("B4", 1), ("A4", 1), ("G#4", 3)],
    [("F4", 2), ("A4", 1), ("D5", 3, "E5")],
    [("C5", 1), ("B4", 1), ("A4", 1), ("F4", 3)],
    [("E4", 2), ("A4", 1), ("C5", 2), ("B4", 1)],
    [("A4", 6, "B4")],
]


def render(rng):
    length = METER.length(BARS)
    loop = Loop(length, rng, room_t60=3.2)
    drone(loop, ["A1", "E2"], rng, gain=0.11)
    loop.add(synth.wind(length + 1, rng), 0, gain=0.17, room=0.2)
    loop.add(synth.reeds(length + 1, rng), 0, gain=0.085, pan=0.2, room=0.15)
    loop.add(synth.bell(hz("A4"), rng, velocity=0.4), METER.at(9), gain=0.75, pan=0.5, room=0.6,
             far=0.9)
    for bar, name in enumerate(HARMONY, start=1):
        pattern = ROCK if bar % 2 else ANSWER
        bandura(loop, METER, bar, pattern, CHORDS[name], rng, velocity=0.5, gain=1.2)
    for i in range(0, len(SONG), 2):
        sopilka(loop, METER, 17 + i, SONG[i] + SONG[i + 1], rng, gain=0.19, pan=0.3, far=0.45)
    for bar in list(range(13, 17)) + list(range(29, 33)):
        name = HARMONY[bar - 1]
        if name in HUM:
            choir(loop, METER.at(bar) - 0.2, METER.at(1, 6) + 0.2, HUM[name], rng, gain=0.12)
    return loop.render()
