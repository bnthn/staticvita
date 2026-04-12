#!/usr/bin/env python3
"""Build using the repository root as project root (independent of current working directory)."""

import sys
from pathlib import Path

from staticvita.builder import build_site
from staticvita.cli import resolve_data_path


def main() -> None:
    # scripts/ -> repo root
    root = Path(__file__).resolve().parent.parent
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
