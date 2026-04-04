from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jinja_cv import __version__
from jinja_cv.builder import build_site


def resolve_data_path(project: Path, input_arg: str | None) -> Path:
    """Resolve site JSON path relative to project (see package docs for bare filename rules)."""
    project = project.resolve()
    if input_arg is None:
        default_path = project / "data" / "site.json"
        if not default_path.is_file():
            raise FileNotFoundError(f"missing data file: {default_path}")
        return default_path

    p = Path(input_arg)
    if p.is_absolute():
        if not p.is_file():
            raise FileNotFoundError(f"missing data file: {p}")
        return p

    if p.parent != Path("."):
        target = (project / p).resolve()
        if not target.is_file():
            raise FileNotFoundError(f"missing data file: {target}")
        return target

    candidates = [project / p.name, project / "data" / p.name]
    for target in candidates:
        if target.is_file():
            return target
    tried = ", ".join(str(c) for c in candidates)
    raise FileNotFoundError(f"missing data file: tried {tried}")


def _parse(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="jinja-cv",
        description="Build static HTML from Jinja templates and site JSON.",
    )
    parser.add_argument(
        "-C",
        "--project",
        type=Path,
        default=Path.cwd(),
        help="project root (templates/, static/, data/); default: current directory",
    )
    parser.add_argument(
        "-i",
        "--input",
        default=None,
        metavar="FILE",
        help="site JSON file; default: data/site.json. Bare name tries ./FILE then data/FILE",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=Path("dist"),
        metavar="DIR",
        help="output directory relative to project; default: dist",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse(argv)
    project = args.project.resolve()
    try:
        data_path = resolve_data_path(project, args.input)
        out_dir = project / args.out
        build_site(project, data_path, out_dir=out_dir)
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
