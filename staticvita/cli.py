from __future__ import annotations

import argparse
import shutil
import sys
from contextlib import ExitStack
from pathlib import Path

from staticvita import __version__
from staticvita.builder import IMAGE_SUFFIXES, build_site

EXAMPLE_SITE = "site.example.json"
EXAMPLE_AVATAR = "avatar.example.svg"


def _bundled_example_file(name: str, stack: ExitStack) -> Path | None:
    """Return a real path to a packaged example file, or the source checkout copy."""
    from importlib.resources import as_file, files

    try:
        bundled = files("staticvita") / "example" / name
        if bundled.is_file():
            return Path(stack.enter_context(as_file(bundled)))
    except ModuleNotFoundError:
        pass

    checkout = Path(__file__).resolve().parent.parent / name
    if checkout.is_file():
        return checkout
    return None


def _has_avatar_image(project: Path) -> bool:
    names = {f"avatar{suffix}" for suffix in IMAGE_SUFFIXES}
    for path in project.iterdir():
        if path.is_file() and path.name.lower() in names:
            return True
    return False


def ensure_example_files(project: Path) -> list[str]:
    """Copy starter files into the project root when their real counterparts are missing.

    Writes site.example.json when site.json is absent, and avatar.example.svg
    when no avatar image is present. Existing files are left in place.
    Returns the filenames that were created.
    """
    project = project.resolve()
    needed: list[str] = []
    if not (project / "site.json").is_file() and not (project / EXAMPLE_SITE).is_file():
        needed.append(EXAMPLE_SITE)
    if not _has_avatar_image(project) and not (project / EXAMPLE_AVATAR).is_file():
        needed.append(EXAMPLE_AVATAR)
    if not needed:
        return []

    created: list[str] = []
    with ExitStack() as stack:
        sources: list[tuple[str, Path]] = []
        for name in needed:
            src = _bundled_example_file(name, stack)
            if src is None:
                raise FileNotFoundError(f"missing example data file: {name}")
            sources.append((name, src))
        for name, src in sources:
            dest = project / name
            if src.resolve() != dest.resolve():
                shutil.copy2(src, dest)
            created.append(name)
    return created


def _print_example_note(project: Path, created: list[str]) -> None:
    if created:
        print("wrote " + " and ".join(created))
    pending: list[str] = []
    if not (project / "site.json").is_file():
        pending.append(f"{EXAMPLE_SITE} to site.json")
    if not _has_avatar_image(project):
        pending.append(f"{EXAMPLE_AVATAR} to avatar.svg")
    if not pending:
        return
    if len(pending) == 2:
        action = (
            f"copy or rename {EXAMPLE_SITE} to site.json and "
            f"{EXAMPLE_AVATAR} to avatar.svg"
        )
    else:
        action = "copy or rename " + pending[0]
    print(action + ", then run staticvita again")


def resolve_data_path(project: Path, input_arg: str | None) -> Path:
    """Resolve site JSON path relative to project (see package docs for bare filename rules)."""
    project = project.resolve()
    if input_arg is None:
        default_path = project / "site.json"
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
        prog="staticvita",
        description="Build static HTML from Jinja templates and site JSON.",
    )
    parser.add_argument(
        "-C",
        "--project",
        type=Path,
        default=Path.cwd(),
        help="project root (templates/, static/, site.json); default: current directory",
    )
    parser.add_argument(
        "-i",
        "--input",
        default=None,
        metavar="FILE",
        help="site JSON file; default: site.json. Bare name tries ./FILE then data/FILE",
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
    created: list[str] = []
    try:
        if args.input is None:
            created = ensure_example_files(project)
            if not (project / "site.json").is_file():
                _print_example_note(project, created)
                return
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
    if created:
        print("wrote " + " and ".join(created))


if __name__ == "__main__":
    main()
