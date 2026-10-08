"""Draw the Tandem app icons: a white outlined speech bubble with a dot,
on a soft peach-to-rose gradient.

Run from the repository root:  python web/make_icons.py
Writes PNGs to docs/icons/. Needs Pillow (pip install pillow).
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "icons"

S = 2048                          # draw large, scale down for smooth edges
PEACH, ROSE = (255, 196, 140), (255, 120, 150)
WHITE = (255, 255, 255)


def background():
    """Diagonal gradient: peach at the top right, rose at the bottom left."""
    g = Image.linear_gradient("L").resize((S * 2, S * 2)).rotate(-35).crop((S // 2, S // 2, S // 2 + S, S // 2 + S))
    return Image.composite(Image.new("RGB", (S, S), ROSE), Image.new("RGB", (S, S), PEACH), g)


def bubble_mask(box, tail=True):
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    x0, y0, x1, y1 = box
    h = y1 - y0
    d.rounded_rectangle(box, radius=int(h * 0.42), fill=255)
    if tail:
        d.polygon([(x0 + h * 0.18, y1 - h * 0.30), (x0 + h * 0.58, y1 - 2), (x0 + h * 0.02, y1 + h * 0.22)], fill=255)
    return m


def mark(scale=1.0):
    """The white bubble outline and dot, centred; scale < 1 shrinks it (for Android 'maskable' icons)."""
    k = S / 1024 * scale
    off = S / 2 * (1 - scale)
    box = lambda x0, y0, x1, y1: (off + x0 * k, off + y0 * k, off + x1 * k, off + y1 * k)
    outline = ImageChops.subtract(bubble_mask(box(232, 300, 792, 700)), bubble_mask(box(286, 354, 738, 646), tail=False))
    ImageDraw.Draw(outline).ellipse(box(462, 450, 562, 550), fill=255)
    return outline


def draw_icon(scale=1.0):
    img = background()
    img.paste(WHITE, (0, 0), mark(scale))
    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    full = draw_icon()
    for name, size in [("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512), ("favicon-32.png", 32)]:
        full.resize((size, size), Image.LANCZOS).save(OUT / name, optimize=True)
    draw_icon(scale=0.8).resize((512, 512), Image.LANCZOS).save(OUT / "icon-maskable-512.png", optimize=True)
    print("Wrote icons to", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
