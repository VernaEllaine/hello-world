"""Build docs/index.html (the GitHub Pages version) from web/tutor.html.

web/tutor.html is written as a Claude artifact, which gets its <!doctype>,
<head> and <body> added when it is published. GitHub Pages serves files as-is,
so this wraps the same page in a full document.

Run from the repository root:  python web/build_pages.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "web" / "tutor.html"
TARGET = ROOT / "docs" / "index.html"
MANIFEST = ROOT / "docs" / "manifest.webmanifest"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Practise German or French by talking with a tutor who corrects your grammar.">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0C0C0C" media="(prefers-color-scheme: dark)">
<!-- Home Screen app: name, icon, and full-screen launch -->
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Tandem">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<style>
  *, *::before, *::after { box-sizing: border-box; }
  body { margin: 0; }
  /* Full-screen on a phone: keep the header clear of the clock and notch */
  header { padding-top: calc(10px + env(safe-area-inset-top, 0px)) !important; padding-left: max(16px, env(safe-area-inset-left, 0px)) !important; padding-right: max(16px, env(safe-area-inset-right, 0px)) !important; }
</style>
</head>
<body>
"""

TAIL = """
</body>
</html>
"""


def main() -> None:
    TARGET.parent.mkdir(exist_ok=True)
    TARGET.write_text(HEAD + SOURCE.read_text(encoding="utf-8") + TAIL, encoding="utf-8")
    MANIFEST.write_text(json.dumps({
        "name": "Tandem – German & French tutor",
        "short_name": "Tandem",
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": "#FFFFFF",
        "theme_color": "#FFFFFF",
        "icons": [
            {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(ROOT)} and {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
