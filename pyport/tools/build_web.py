"""Browser build (PHASE_0 task 0.8): stage code + original resources, then run pygbag.

    python pyport/tools/build_web.py            # -> pyport/build/web-src (+ pygbag --build,
                                                #    + guide.html and its link on the page)
    python -m pygbag pyport/build/web-src       # dev server on http://localhost:8000
    python pyport/tools/build_web.py --mp       # POW Multiplayer -> pyport/build/web-mp-src
        page?server=ws://host:28200 talks to `python -m pow_server`, without it the server
        runs inside the page (nothing kept after a reload)

pygbag packs one folder, so the resources from the repository root are copied into
web-src/res/ (config.RES_ROOT falls back to ./res when ../0_font.png does not exist).
"""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PY = ROOT / "pyport"
MP = "--mp" in sys.argv
OUT = PY / "build" / ("web-mp-src" if MP else "web-src")
RES_GLOBS = ["*.png", "*.scr", "*.arr", "*.MAP", "*.SP3", "*.bin", "*.ft2", "*.pal"]


def stage():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for f in ("main.py", "mp_main.py", "config.py"):   # mp_main: Main Menu > Multiplayer
        shutil.copy2(PY / f, OUT / f)
    if MP:                                  # pygbag starts main.py: the multiplayer one
        shutil.copy2(PY / "mp_main.py", OUT / "main.py")
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


GUIDE_LINK = ('<a href="guide.html" target="_blank" style="position:fixed;right:8px;bottom:8px;z-index:9999;'
              'font:14px sans-serif;color:#fff;background:#2747a8;padding:6px 10px;border-radius:6px;'
              'text-decoration:none">Довідник воїна</a>')


def add_guide(site):
    """The players' guide (web/guide.html: items, recipes, secrets) next to the game, and a link
    to it on the game page. Only into the built site: inside the game package it would only
    make the download bigger."""
    shutil.copy2(PY / "web" / "guide.html", site / "guide.html")
    page = site / "index.html"
    if page.exists():
        html = page.read_text(encoding="utf-8")
        end = html.rfind("</body>")         # the last one: a script of the page may hold the text
        if 'href="guide.html"' in html:
            pass
        elif end < 0:
            print("guide: no </body> in", page, "- the link is not added")
        else:
            page.write_text(html[:end] + GUIDE_LINK + "\n" + html[end:], encoding="utf-8")
    print("guide ->", site / "guide.html")


if __name__ == "__main__":
    stage()
    if "--no-pygbag" not in sys.argv:
        rc = subprocess.call([sys.executable, "-m", "pygbag", "--build", "--ume_block", "0", str(OUT)])
        if rc == 0 and not MP:
            add_guide(OUT / "build" / "web")
        sys.exit(rc)
