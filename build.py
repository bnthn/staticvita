#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path

from staticjinja import Site

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "site.json"
STATIC_SRC = ROOT / "static"
DIST_STATIC = ROOT / "dist" / "static"


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


if __name__ == "__main__":
    main()
