#!/usr/bin/env python3
"""Render an HTML page to a print-ready A4 PDF with headless Chrome.

Used by `make docs-pdf` to turn the mkdocs print-site page into one PDF.

Any Google Fonts webfonts the page links are downloaded and inlined as data
URIs first: headless Chrome does not reliably finish network font fetches
inside its virtual-time budget, and without inlining the PDF silently falls
back to Liberation/Noto. Pages that self-host their fonts (mkdocs-material
does) need no inlining and report so.

Usage:
    uv run python scripts/report/build_pdf.py site/print_page/index.html out.pdf
"""

import base64
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

UA = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}
# Only these subsets are needed; latin-ext carries the Lithuanian diacritics.
SUBSETS = {"latin", "latin-ext"}
CHROME_CANDIDATES = ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser")


def find_chrome() -> str:
    for name in CHROME_CANDIDATES:
        if path := shutil.which(name):
            return path
    sys.exit(f"No Chrome/Chromium found. Tried: {', '.join(CHROME_CANDIDATES)}")


FONT_LINK_RE = re.compile(r'<link[^>]+href="(https://fonts\.googleapis\.com/css2\?[^"]+)"[^>]*>')


def inline_fonts(html: str) -> str:
    """Replace every Google Fonts <link> with @font-face rules carrying data URIs."""
    links = FONT_LINK_RE.findall(html)
    if not links:
        print("  no Google Fonts link found - nothing to inline")
        return html

    faces, cache = [], {}
    for raw_url in links:
        css_url = raw_url.replace("&amp;", "&")
        css = urllib.request.urlopen(urllib.request.Request(css_url, headers=UA), timeout=60).read().decode()
        for subset, block in re.findall(r"/\*\s*([a-z0-9\-\[\] ]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.DOTALL):
            if subset.strip() not in SUBSETS:
                continue
            url_match = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", block)
            if not url_match:
                continue
            url = url_match.group(1)
            if url not in cache:
                cache[url] = base64.b64encode(
                    urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
                ).decode()
            # Swap only the URL - the block already carries its own format('woff2').
            faces.append(block.replace(url, f"data:font/woff2;base64,{cache[url]}"))

    if not faces:
        sys.exit("Fetched the font CSS but inlined no faces - aborting rather than shipping a fallback PDF.")

    print(f"  inlined {len(faces)} font faces from {len(cache)} files")
    style = "<style>\n/* webfonts inlined by build_pdf.py */\n" + "\n".join(faces) + "\n</style>\n"
    return FONT_LINK_RE.sub("", html).replace("</head>", style + "</head>")


def verify(pdf: Path) -> None:
    """Warn if the PDF fell back to system fonts (needs poppler's pdffonts)."""
    if not shutil.which("pdffonts"):
        return
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, check=False).stdout
    families = {re.sub(r"^[A-Z]+\+", "", line.split()[0]) for line in out.splitlines()[2:] if line.split()}
    if not families:
        print("  WARNING: the PDF embeds no fonts at all")
        return
    # These are the substitutes Chrome reaches for when a webfont did not load.
    fallbacks = sorted(f for f in families if f.startswith(("Liberation", "DejaVu", "NotoSans-", "NotoSansMono")))
    embedded = sorted(f for f in families if f not in fallbacks)
    if embedded:
        print(f"  fonts embedded: {', '.join(embedded[:6])}{' …' if len(embedded) > 6 else ''}")
    if not embedded:
        print(f"  WARNING: only fallback fonts present ({', '.join(fallbacks)}) - webfonts did not load")
    elif fallbacks:
        print(f"  note: fallback fonts also used for some glyphs ({', '.join(fallbacks)})")


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    source, target = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if not source.is_file():
        sys.exit(f"Source not found: {source}")

    print(f"Building {target.name} from {source.name}")
    html = inline_fonts(source.read_text())

    # Stage the rewritten HTML as a sibling of the original, not in a temp
    # directory: a built mkdocs page loads its CSS, JS and fonts through
    # relative paths, which only resolve from the source's own directory.
    staged = source.with_name(f"{source.stem}.print-tmp.html")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            staged.write_text(html)
            proc = subprocess.Popen(
                [
                    find_chrome(),
                    "--headless=new", "--disable-gpu", "--no-sandbox",
                    f"--user-data-dir={Path(tmp) / 'profile'}",
                    "--no-first-run", "--no-default-browser-check",
                    "--disable-extensions", "--disable-background-networking",
                    # Force the light colour scheme: otherwise a theme with a
                    # prefers-color-scheme palette prints its dark background.
                    "--blink-settings=preferredColorScheme=1",
                    "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    f"--print-to-pdf={target}", staged.as_uri(),
                ],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            # Chrome writes the PDF and then sometimes lingers instead of exiting.
            # The file is what matters, so reap our own instance rather than wait it out.
            try:
                proc.wait(timeout=90)
            except subprocess.TimeoutExpired:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
    finally:
        staged.unlink(missing_ok=True)

    if not target.is_file():
        sys.exit("Chrome produced no PDF.")
    print(f"  wrote {target} ({target.stat().st_size // 1024} KB)")
    verify(target)


if __name__ == "__main__":
    main()
