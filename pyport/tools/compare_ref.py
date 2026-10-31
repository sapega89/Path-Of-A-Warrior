"""Compare the port's screenshots with reference screenshots from KEmulator.

    python pyport/tools/compare_ref.py pyport/shots/title pyport/shots_ref/title

Reference files must have the same names as the port's shots (e.g. 05_title.png).
A reference may be any integer multiple of 240x320 (KEmulator zoom); it is reduced with
nearest-neighbour first. Prints the share of differing pixels and writes *_diff.png
(red = different) next to the reference.
"""
import pathlib
import sys

from PIL import Image, ImageChops


def compare(port_dir, ref_dir):
    port_dir, ref_dir = pathlib.Path(port_dir), pathlib.Path(ref_dir)
    worst = 0.0
    for ref in sorted(ref_dir.glob("*.png")):
        if ref.stem.endswith("_diff"):
            continue
        mine = port_dir / ref.name
        if not mine.exists():
            print("%-32s no port shot" % ref.name)
            continue
        a = Image.open(mine).convert("RGB")
        b = Image.open(ref).convert("RGB")
        if b.size != a.size:
            b = b.resize(a.size, Image.NEAREST)
        diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 24 else 0)
        share = sum(1 for v in diff.getdata() if v) / (a.size[0] * a.size[1])
        worst = max(worst, share)
        red = Image.new("RGB", a.size, (255, 0, 0))
        Image.composite(red, a, diff).save(ref.with_name(ref.stem + "_diff.png"))
        print("%-32s %6.2f %% pixels differ" % (ref.name, 100 * share))
    return worst


if __name__ == "__main__":
    compare(sys.argv[1], sys.argv[2])
