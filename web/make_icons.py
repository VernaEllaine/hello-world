"""Draw the Tandem app icons: two interlocking rings, like the wheels of a tandem
(German amber, French cobalt) on a near-black background.

Run from the repository root:  python web/make_icons.py
Writes PNGs to docs/icons/. Needs Pillow (pip install pillow).
"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "icons"

BG = (17, 17, 17)
AMBER = (240, 160, 75)
COBALT = (124, 146, 255)
S = 2048          # draw large, scale down for smooth edges
R = 390           # ring radius (to the middle of the stroke)
W = 104           # ring thickness
GAP = 470         # distance between the two ring centres


def ring(color):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return layer, ImageDraw.Draw(layer)


def draw_icon(scale=1.0):
    """scale < 1 shrinks the artwork toward the centre (for Android 'maskable' icons)."""
    cx, cy = S / 2, S / 2
    left, right = (cx - GAP / 2, cy), (cx + GAP / 2, cy)

    def ring_layer(c, color):
        layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.ellipse((c[0] - R - W / 2, c[1] - R - W / 2, c[0] + R + W / 2, c[1] + R + W / 2), fill=color + (255,))
        d.ellipse((c[0] - R + W / 2, c[1] - R + W / 2, c[0] + R - W / 2, c[1] + R - W / 2), fill=(0, 0, 0, 0))
        return layer

    amber, cobalt = ring_layer(left, AMBER), ring_layer(right, COBALT)
    art = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    art.alpha_composite(amber)
    art.alpha_composite(cobalt)

    # Interlock: cobalt passes over amber at the bottom crossing (drawn above), and amber
    # passes over cobalt at the top crossing. The only crossing in the top half is that
    # one, so re-draw the amber ring there, with a thin background-coloured outline so
    # the over/under reads cleanly.
    e = 16
    over = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    od = ImageDraw.Draw(over)
    lx, ly = left
    od.ellipse((lx - R - W / 2 - e, ly - R - W / 2 - e, lx + R + W / 2 + e, ly + R + W / 2 + e), fill=BG + (255,))
    od.ellipse((lx - R + W / 2 + e, ly - R + W / 2 + e, lx + R - W / 2 - e, ly + R - W / 2 - e), fill=(0, 0, 0, 0))
    over.alpha_composite(amber)
    top_half = Image.new("L", (S, S), 0)
    ImageDraw.Draw(top_half).rectangle((0, 0, S, cy), fill=255)
    art.paste(over, (0, 0), Image.composite(over.getchannel("A"), Image.new("L", (S, S), 0), top_half))

    if scale != 1.0:
        size = int(S * scale)
        art = art.resize((size, size), Image.LANCZOS)
        canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        canvas.alpha_composite(art, ((S - size) // 2, (S - size) // 2))
        art = canvas
    img = Image.new("RGB", (S, S), BG)
    img.paste(art, (0, 0), art)
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
