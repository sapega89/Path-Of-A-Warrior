"""Makes the game's music: three tunes, composed in the files next to this one and played by
the instruments of synth.py, into godot/client/assets/music/<name>.ogg.

    pip install numpy scipy        # and ffmpeg on the PATH
    python godot/tools/music/build.py              # all three
    python godot/tools/music/build.py duma         # just one
    python godot/tools/music/build.py --wav DIR    # also the .wav files, to listen to

Each tune is a loop: its end runs into its start, so the game plays it round and round.
The same seed makes the same file every time.
"""

import argparse
import pathlib
import sys
import tempfile

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import duma  # noqa: E402
import mix  # noqa: E402
import plavni  # noqa: E402
import pokhid  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[2] / "client" / "assets" / "music"
TUNES = {"duma": duma, "pokhid": pokhid, "plavni": plavni}
SEED = 1648


def build(name, out, wav_dir):
    tune = TUNES[name]
    stereo = mix.master(tune.render(np.random.default_rng(SEED)), tune.LUFS)
    with tempfile.TemporaryDirectory() as tmp:
        wav = pathlib.Path(wav_dir or tmp) / f"{name}.wav"
        mix.write_wav(wav, stereo)
        mix.write_ogg(out / f"{name}.ogg", wav)
    seconds = stereo.shape[1] / mix.RATE
    top = 20 * np.log10(np.abs(stereo).max())
    print(f"{name}: {seconds:.1f} s, {mix.loudness(stereo):.1f} LUFS, peak {top:.1f} dBFS")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("names", nargs="*", help="of " + ", ".join(TUNES) + " (all when none)")
    parser.add_argument("--out", type=pathlib.Path, default=OUT)
    parser.add_argument("--wav", type=pathlib.Path, help="also keep the .wav files here")
    args = parser.parse_args()
    unknown = [n for n in args.names if n not in TUNES]
    if unknown:
        parser.error("no such tune: " + ", ".join(unknown))
    args.out.mkdir(parents=True, exist_ok=True)
    if args.wav:
        args.wav.mkdir(parents=True, exist_ok=True)
    for name in args.names or TUNES:
        build(name, args.out, args.wav)


if __name__ == "__main__":
    main()
