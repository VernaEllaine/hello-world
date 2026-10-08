"""Build docs/index.html (the GitHub Pages version) from web/tutor.html.

web/tutor.html is written as a Claude artifact, which gets its <!doctype>,
<head> and <body> added when it is published. GitHub Pages serves files as-is,
so this wraps the same page in a full document.

Run from the repository root:  python web/build_pages.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "web" / "tutor.html"
TARGET = ROOT / "docs" / "index.html"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Practise German or French by talking with a tutor who corrects your grammar.">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0C0C0C" media="(prefers-color-scheme: dark)">
<style>*, *::before, *::after { box-sizing: border-box; } body { margin: 0; }</style>
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
    print(f"Wrote {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
