"""javax.microedition.lcdui.Image / Graphics on top of pygame.

Only what x.java uses (PHASE_0 task 0.3): drawImage (anchors), clipRect/setClip,
fillRect, drawRect, drawLine, setColor, getClip*.  No drawRegion/transforms -
the game never calls them.
"""
import io
import os
import sys

import pygame

from pow.midp import resources

# Graphics anchors
HCENTER = 1
VCENTER = 2
LEFT = 4
RIGHT = 8
TOP = 16
BOTTOM = 32
BASELINE = 64

_IS_WEB = sys.platform == "emscripten"
_TMP_PNG = "/tmp/pow_image.png"   # noqa: S108 (browser build only: the emscripten in-memory FS)


def _load_png(data, hint):
    """PNG bytes -> Surface. pygbag's pygame cannot decode from a file object
    ("can't access resource on platform"), only from a path, so in the browser the
    bytes go through a temporary file in the in-memory FS."""
    if _IS_WEB:
        with open(_TMP_PNG, "wb") as fh:
            fh.write(data)
        try:
            return pygame.image.load(_TMP_PNG)
        finally:
            try:
                os.remove(_TMP_PNG)
            except OSError:
                pass
    return pygame.image.load(io.BytesIO(data), hint)


class Image:
    __slots__ = ("mutable", "surface")

    def __init__(self, surface, mutable=False):
        self.surface = surface
        self.mutable = mutable

    @staticmethod
    def _prepare(surface):
        # convert_alpha needs a display; headless runs create a dummy one.
        if pygame.display.get_init() and pygame.display.get_surface() is not None:
            return surface.convert_alpha()
        return surface

    @staticmethod
    def createImage(*args):
        """createImage(String) | createImage(byte[], off, len) | createImage(w, h)."""
        if len(args) == 1 and isinstance(args[0], str):
            data = resources.read(args[0])
            if data is None:
                raise OSError("resource not found: " + args[0])
            return Image(Image._prepare(_load_png(data, args[0])))
        if len(args) == 3 and isinstance(args[0], (bytes, bytearray)):
            data, off, ln = args
            return Image(Image._prepare(_load_png(bytes(data[off:off + ln]), "x.png")))
        if len(args) == 2:
            w, h = args
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill((255, 255, 255, 255))  # MIDP: a new mutable image is white
            return Image(s, mutable=True)
        raise TypeError("createImage" + repr(args))

    def getWidth(self):
        return self.surface.get_width()

    def getHeight(self):
        return self.surface.get_height()

    def getGraphics(self):
        if not self.mutable:
            raise RuntimeError("IllegalStateException: immutable image")
        return Graphics(self.surface)


class Graphics:
    def __init__(self, surface):
        self.surface = surface
        self.color = 0
        self._rgb = (0, 0, 0)
        self.cx, self.cy = 0, 0
        self.cw, self.ch = surface.get_width(), surface.get_height()
        self._apply_clip()

    # --- clip -------------------------------------------------------------
    def _apply_clip(self):
        w = max(0, self.cw)
        h = max(0, self.ch)
        self.surface.set_clip(pygame.Rect(self.cx, self.cy, w, h))

    def getClipX(self):
        return self.cx

    def getClipY(self):
        return self.cy

    def getClipWidth(self):
        return self.cw

    def getClipHeight(self):
        return self.ch

    def setClip(self, x, y, w, h):
        self.cx, self.cy, self.cw, self.ch = x, y, w, h
        self._apply_clip()

    def clipRect(self, x, y, w, h):
        x1 = max(self.cx, x)
        y1 = max(self.cy, y)
        x2 = min(self.cx + self.cw, x + w)
        y2 = min(self.cy + self.ch, y + h)
        self.cx, self.cy = x1, y1
        self.cw, self.ch = max(0, x2 - x1), max(0, y2 - y1)
        self._apply_clip()

    # --- colour / primitives ---------------------------------------------------
    def setColor(self, rgb):
        self.color = rgb & 0xFFFFFF
        self._rgb = ((rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF)

    def fillRect(self, x, y, w, h):
        if w <= 0 or h <= 0:
            return
        self.surface.fill(self._rgb, pygame.Rect(x, y, w, h))

    def drawRect(self, x, y, w, h):
        # MIDP: outline covers (w+1) x (h+1) pixels
        if w < 0 or h < 0:
            return
        if w == 0 or h == 0:
            self.drawLine(x, y, x + w, y + h)
            return
        pygame.draw.rect(self.surface, self._rgb, pygame.Rect(x, y, w + 1, h + 1), 1)

    def drawLine(self, x1, y1, x2, y2):
        pygame.draw.line(self.surface, self._rgb, (x1, y1), (x2, y2), 1)

    def drawImage(self, img, x, y, anchor):
        if img is None:
            raise RuntimeError("NullPointerException: drawImage(null)")
        w, h = img.getWidth(), img.getHeight()
        if anchor == 0:
            anchor = TOP | LEFT
        if anchor & HCENTER:
            x -= w // 2
        elif anchor & RIGHT:
            x -= w
        if anchor & VCENTER:
            y -= h // 2
        elif anchor & BOTTOM:
            y -= h
        self.surface.blit(img.surface, (x, y))
