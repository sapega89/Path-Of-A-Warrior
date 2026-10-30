"""Parse all *.SP2 sprite tables of POW Multiplayer and validate them against PNG sheets.

Format per a.java: b[0] = frame count (signed byte); then per frame 6 bytes:
  srcX u8, srcY u8, w s8, h s8, anchorX s8, anchorY s8
Usage: python3 -I sp2_parse.py <jar_dir>
"""
import os
import sys
import glob
from PIL import Image, ImageOps


def parse(path):
    data = open(path, 'rb').read()
    n = data[0] if data[0] < 128 else data[0] - 256
    frames = []
    for i in range(n):
        o = 1 + 6 * i
        sx, sy = data[o], data[o + 1]
        w, h, ax, ay = [b if b < 128 else b - 256 for b in data[o + 2:o + 6]]
        frames.append((sx, sy, w, h, ax, ay))
    return n, len(data), frames


def sheet_for(base, jar):
    # a.java naming: <name>.png / <name>_r.png with <name>_basic|_skill1|_skill2.SP2 or <name>.SP2
    for suf in ('_basic', '_skill1', '_skill2'):
        if base.endswith(suf):
            base = base[: -len(suf)]
    return base, os.path.join(jar, base + '.png'), os.path.join(jar, base + '_r.png')


def main(jar):
    files = sorted(glob.glob(os.path.join(jar, '*.SP2')))
    print('files', len(files))
    summary = {}
    for p in files:
        name = os.path.basename(p)[:-4]
        n, size, frames = parse(p)
        ok_size = size == 1 + 6 * n
        base, png, rpng = sheet_for(name, jar)
        sizes = {}
        bad = 0
        mirror_ok = None
        for label, path in (('L', png), ('R', rpng)):
            if os.path.exists(path):
                im = Image.open(path)
                sizes[label] = im.size
                for (sx, sy, w, h, ax, ay) in frames:
                    if w <= 0 or h <= 0:
                        continue
                    if sx + w > im.size[0] or sy + h > im.size[1]:
                        bad += 1
        # check whether _r.png is per-frame mirror of .png (same srcX/srcY, each cell flipped)
        if 'L' in sizes and 'R' in sizes:
            L = Image.open(png).convert('RGBA')
            R = Image.open(rpng).convert('RGBA')
            cell_mirror = 0
            whole_mirror = L.size == R.size and ImageOps.mirror(L).tobytes() == R.tobytes()
            tested = 0
            for (sx, sy, w, h, ax, ay) in frames:
                if w <= 0 or h <= 0:
                    continue
                tested += 1
                a = L.crop((sx, sy, sx + w, sy + h))
                b = R.crop((sx, sy, sx + w, sy + h))
                if ImageOps.mirror(a).tobytes() == b.tobytes():
                    cell_mirror += 1
            mirror_ok = (cell_mirror, tested, whole_mirror)
        summary[name] = (n, size, ok_size, sizes, bad, mirror_ok)
        print(f"{name:22s} n={n:3d} bytes={size:4d} sizeOK={ok_size} sheets={sizes} out_of_bounds={bad} "
              f"mirror(cell_ok/tested, whole_sheet_flip)={mirror_ok}")
        if name in ('sprbody_basic', 'spr_mon', 'spreff3'):
            for i, fr in enumerate(frames):
                print('   ', i, fr)
    # ranges
    allw = []
    for p in files:
        allw += parse(p)[2]
    print('srcX max', max(f[0] for f in allw), 'srcY max', max(f[1] for f in allw))
    print('w range', min(f[2] for f in allw), max(f[2] for f in allw),
          'h range', min(f[3] for f in allw), max(f[3] for f in allw))
    print('anchorX range', min(f[4] for f in allw), max(f[4] for f in allw),
          'anchorY range', min(f[5] for f in allw), max(f[5] for f in allw))
    print('zero-size frames', sum(1 for f in allw if f[2] <= 0 or f[3] <= 0))


if __name__ == '__main__':
    main(sys.argv[1])
