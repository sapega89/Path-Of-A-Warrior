"""Browser build (PHASE_0 task 0.8): stage code + original resources, then run pygbag.

    python pyport/tools/build_web.py            # -> pyport/build/web-src (+ pygbag --build)
    python -m pygbag pyport/build/web-src       # dev server on http://localhost:8000

pygbag packs one folder, so the resources from the repository root are copied into
web-src/res/ (config.RES_ROOT falls back to ./res when ../0_font.png does not exist).
"""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PY = ROOT / "pyport"
OUT = PY / "build" / "web-src"
RES_GLOBS = ["*.png", "*.scr", "*.arr", "*.MAP", "*.SP3", "*.bin", "*.ft2", "*.pal"]


def stage():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for f in ("main.py", "config.py"):
        shutil.copy2(PY / f, OUT / f)
    for pkg in ("pow", "pow_mp", "pow_server"):
        shutil.copytree(PY / pkg, OUT / pkg, ignore=shutil.ignore_patterns("__pycache__"))
    # multiplayer resources (PHASE_9): config.MP_RES_ROOT falls back to ./res_mp
    shutil.copytree(PY / "assets_mp", OUT / "res_mp")
    shutil.copytree(PY / "assets", OUT / "assets")
    res = OUT / "res"
    res.mkdir()
    n = 0
    for g in RES_GLOBS:
        for p in ROOT.glob(g):
            shutil.copy2(p, res / p.name)
            n += 1
    (res / "META-INF").mkdir()
    shutil.copy2(ROOT / "META-INF" / "MANIFEST.MF", res / "META-INF" / "MANIFEST.MF")
    print("staged %d resource files -> %s" % (n, OUT))


if __name__ == "__main__":
    stage()
    if "--no-pygbag" not in sys.argv:
        sys.exit(subprocess.call([sys.executable, "-m", "pygbag", "--build", "--ume_block", "0", str(OUT)]))
