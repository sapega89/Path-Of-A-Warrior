"""Contact sheet of a shots folder: python pyport/tools/sheet.py pyport/shots/title out.png"""
import pathlib
import sys

from PIL import Image, ImageDraw


def sheet(folder, out, cols=5, scale=1):
    files = sorted(p for p in pathlib.Path(folder).glob("*.png") if not p.name.startswith("tick_"))
    w, h = 240 * scale, 320 * scale
    rows = (len(files) + cols - 1) // cols
    im = Image.new("RGB", (cols * (w + 6), rows * (h + 20)), (40, 40, 40))
    d = ImageDraw.Draw(im)
    for n, f in enumerate(files):
        x, y = (n % cols) * (w + 6), (n // cols) * (h + 20)
        im.paste(Image.open(f).convert("RGB").resize((w, h), Image.NEAREST), (x, y + 18))
        d.text((x + 2, y + 3), f.stem, fill=(255, 255, 0))
    im.save(out)


if __name__ == "__main__":
    sheet(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 5)
