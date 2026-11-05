"""Class.getResourceAsStream: resources live in the project root (same names as in the original)."""
import pathlib

import config


def root() -> pathlib.Path:
    return pathlib.Path(config.RES_ROOT)


# (pow/game/rebrand.py): images with "Live" redrawn as "Live"
REBRAND_DIR = pathlib.Path(__file__).resolve().parents[2] / "assets" / "rebrand"
REBRAND_IMAGES = ("txt_b.png", "txt_m.png")


def read(path: str):
    """'/name.ext' -> bytes, or None when missing ( returns null)."""
    p = root() / path.lstrip("/")
    if config.REBRAND and path.lstrip("/") in REBRAND_IMAGES:
        p = REBRAND_DIR / path.lstrip("/")
    try:
        with open(p, "rb") as fh:
            return fh.read()
    except OSError:
        return None

