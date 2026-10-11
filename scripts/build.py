#!/usr/bin/env python3
"""Build using the repository root as project root (independent of current working directory)."""

import shutil
import sys
from pathlib import Path

from staticvita.builder import build_site
from staticvita.cli import resolve_data_path


def _copy_examples_if_missing(root: Path) -> None:
    """Demo entry point: materialize a gitignored site.json from the example."""
    site = root / "site.json"
    if not site.is_file():
        shutil.copy2(root / "site.example.json", site)


def main() -> None:
    # scripts/ -> repo root
    root = Path(__file__).resolve().parent.parent
    _copy_examples_if_missing(root)
    try:
        data_path = resolve_data_path(root, None)
        build_site(root, data_path, out_dir=root / "dist")
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
