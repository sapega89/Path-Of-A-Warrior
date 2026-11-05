"""Class.getResourceAsStream: resources live in the project root (same names as in the original)."""
import pathlib

import config


def root() -> pathlib.Path:
    return pathlib.Path(config.RES_ROOT)


def read(path: str):
    """'/name.ext' -> bytes, or None when missing ( returns null)."""
    p = root() / path.lstrip("/")
    try:
        with open(p, "rb") as fh:
            return fh.read()
    except OSError:
        return None

