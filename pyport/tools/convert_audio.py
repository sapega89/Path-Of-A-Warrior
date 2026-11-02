"""Convert the original sounds to OGG for pygame / the browser (spike version of PHASE_1 1.6).

    snd0-2.mid -> FluidSynth + FluidR3_GM.sf2 -> WAV -> OGG (music)
    snd3-16.wav -> OGG (effects)

Needs: fluidsynth, a GM soundfont (apt: fluidsynth fluid-soundfont-gm), ffmpeg.
Output goes to pyport/assets/audio/ and is committed, so players do not need these tools.
"""
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "pyport" / "assets" / "audio"
SF2 = pathlib.Path("/usr/share/sounds/sf2/FluidR3_GM.sf2")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("failed: %s\n%s" % (" ".join(map(str, cmd)), r.stderr[-2000:]))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for n in range(3):
            wav = pathlib.Path(tmp) / ("snd%d.wav" % n)
            run(["fluidsynth", "-ni", "-g", "0.8", "-r", "22050", "-F", str(wav), str(SF2), str(ROOT / ("snd%d.mid" % n))])
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-c:a", "libvorbis", "-q:a", "2",
                 str(OUT / ("snd%d.ogg" % n))])
    for n in range(3, 17):
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(ROOT / ("snd%d.wav" % n)), "-c:a", "libvorbis", "-q:a", "3",
             str(OUT / ("snd%d.ogg" % n))])
    for p in sorted(OUT.glob("*.ogg")):
        print("%-10s %6d bytes" % (p.name, p.stat().st_size))


if __name__ == "__main__":
    main()
