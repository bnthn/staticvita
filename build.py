#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from staticjinja import Site

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "site.json"
STATIC_SRC = ROOT / "static"
DIST_STATIC = ROOT / "dist" / "static"
DIST = ROOT / "dist"

HTML_PAGES = ("index.html", "cv.html", "imprint.html")


def _normalized_base_url(seo) -> str:
    raw = ((seo or {}).get("base_url") or "").strip()
    return raw[:-1] if raw.endswith("/") else raw


def write_seo_files(data: dict, dist: Path) -> None:
    """Write sitemap.xml and robots.txt when seo.base_url is set; remove them otherwise."""
    base = _normalized_base_url(data.get("seo"))
    sitemap_path = dist / "sitemap.xml"
    robots_path = dist / "robots.txt"
    if not base:
        for path in (sitemap_path, robots_path):
            if path.is_file():
                path.unlink()
        return
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in HTML_PAGES:
        loc = f"{base}/{page}"
        lines.append(f"  <url><loc>{xml_escape(loc)}</loc></url>")
    lines.append("</urlset>")
    sitemap_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    robots_path.write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n",
        encoding="utf-8",
    )


def main() -> None:
    if not DATA_PATH.is_file():
        print(f"error: missing data file: {DATA_PATH}", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON in {DATA_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

    site = Site.make_site(
        searchpath=str(ROOT / "templates"),
        outpath=str(ROOT / "dist"),
        env_globals=data,
    )
    site.render()

    if STATIC_SRC.is_dir():
        shutil.copytree(STATIC_SRC, DIST_STATIC, dirs_exist_ok=True)

    write_seo_files(data, DIST)


if __name__ == "__main__":
    main()
