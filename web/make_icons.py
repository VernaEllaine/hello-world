"""Draw the Tandem app icons: an amber German "ö" and a cobalt French "ô" whose rings
interlock (two languages, two wheels of a tandem), on a deep charcoal background.

Run from the repository root:  python web/make_icons.py
Writes PNGs to docs/icons/. Needs Pillow (pip install pillow).
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "icons"

S = 2048                                   # draw large, scale down for smooth edges
BG_CENTER, BG_EDGE = (40, 42, 48), (10, 11, 13)
AMBER = ((255, 196, 102), (236, 120, 48))   # gradient: top-left -> bottom-right
COBALT = ((150, 172, 255), (78, 98, 240))
R, W, GAP = 320, 96, 440                  # ring radius (mid-stroke), thickness, centre distance
CY = S / 2 + 120                           # rings sit a little low to leave room for the accents


def gradient(c0, c1):
    """Diagonal gradient image from c0 (top-left) to c1 (bottom-right)."""
    g = Image.linear_gradient("L").rotate(45, expand=True).resize((S, S))
    return Image.composite(Image.new("RGB", (S, S), c1), Image.new("RGB", (S, S), c0), g)


def ring_mask(cx, cy, grow=0):
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    o, i = R + W / 2 + grow, R - W / 2 - grow
    d.ellipse((cx - o, cy - o, cx + o, cy + o), fill=255)
    d.ellipse((cx - i, cy - i, cx + i, cy + i), fill=0)
    return m


def background():
    bg = Image.new("RGB", (S, S), BG_EDGE)
    glow = Image.new("L", (S, S), 0)
    ImageDraw.Draw(glow).ellipse((S * 0.08, S * 0.02, S * 0.92, S * 0.86), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(S * 0.12))
    return Image.composite(Image.new("RGB", (S, S), BG_CENTER), bg, glow)


def draw_art():
    """The letters on a transparent layer."""
    lx, rx = S / 2 - GAP / 2, S / 2 + GAP / 2
    art = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    amber_fill, cobalt_fill = gradient(*AMBER).convert("RGBA"), gradient(*COBALT).convert("RGBA")

    amber_m, cobalt_m = ring_mask(lx, CY), ring_mask(rx, CY)
    art.paste(amber_fill, (0, 0), amber_m)
    art.paste(cobalt_fill, (0, 0), cobalt_m)            # cobalt over amber at the bottom crossing

    # Amber over cobalt at the top crossing (the only crossing above the centre line),
    # cut with a thin gap so the over/under reads cleanly.
    top = Image.new("L", (S, S), 0)
    ImageDraw.Draw(top).rectangle((0, 0, S, CY), fill=255)
    gap = ImageChops.multiply(ring_mask(lx, CY, grow=16), top)
    art.paste((0, 0, 0, 0), (0, 0), gap)
    art.paste(amber_fill, (0, 0), ImageChops.multiply(amber_m, top))
    art.paste(cobalt_fill, (0, 0), ImageChops.multiply(ImageChops.subtract(cobalt_m, ring_mask(lx, CY, grow=16)), top))

    # Accents: umlaut dots over the amber ring, a circumflex over the cobalt one
    accents = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(accents)
    ring_top = CY - R - W / 2
    dot = W * 0.58
    for dx in (-105, 105):
        x, y = lx + dx, ring_top - 120
        d.ellipse((x - dot, y - dot, x + dot, y + dot), fill=255)
    t = int(W * 0.8)
    apex, left_end, right_end = (rx + 10, ring_top - 205), (rx - 100, ring_top - 95), (rx + 120, ring_top - 95)
    d.line([left_end, apex, right_end], fill=255, width=t, joint="curve")
    for x, y in (left_end, apex, right_end):
        d.ellipse((x - t / 2, y - t / 2, x + t / 2, y + t / 2), fill=255)
    amber_acc = Image.new("L", (S, S), 0)
    ImageDraw.Draw(amber_acc).rectangle((0, 0, S / 2, S), fill=255)
    art.paste(amber_fill, (0, 0), ImageChops.multiply(accents, amber_acc))
    art.paste(cobalt_fill, (0, 0), ImageChops.multiply(accents, ImageChops.invert(amber_acc)))
    return art


def draw_icon(scale=1.0):
    """scale < 1 shrinks the letters toward the centre (for Android 'maskable' icons)."""
    art = draw_art()
    # soft shadow lifts the letters off the background
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    shadow.putalpha(art.getchannel("A").filter(ImageFilter.GaussianBlur(40)).point(lambda a: a * 0.55))
    shadow = shadow.transform((S, S), Image.AFFINE, (1, 0, 0, 0, 1, -24))
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    layer.alpha_composite(shadow)
    layer.alpha_composite(art)
    if scale != 1.0:
        size = int(S * scale)
        small = layer.resize((size, size), Image.LANCZOS)
        layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        layer.alpha_composite(small, ((S - size) // 2, (S - size) // 2))
    img = background().convert("RGBA")
    img.alpha_composite(layer)
    return img.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    full = draw_icon()
    for name, size in [("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512), ("favicon-32.png", 32)]:
        full.resize((size, size), Image.LANCZOS).save(OUT / name, optimize=True)
    draw_icon(scale=0.8).resize((512, 512), Image.LANCZOS).save(OUT / "icon-maskable-512.png", optimize=True)
    print("Wrote icons to", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
