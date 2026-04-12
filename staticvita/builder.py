from __future__ import annotations

import json
import shutil
from contextlib import ExitStack
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from staticjinja import Site

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


def _ensure_out_under_project(project_root: Path, out_dir: Path) -> Path:
    out_resolved = out_dir.resolve()
    proj_resolved = project_root.resolve()
    try:
        out_resolved.relative_to(proj_resolved)
    except ValueError as e:
        raise ValueError(
            f"output directory must be inside project root ({proj_resolved}): {out_resolved}"
        ) from e
    return out_resolved


def _resolve_template_dir(project_root: Path, stack: ExitStack) -> Path:
    local = project_root / "templates"
    if local.is_dir():
        return local.resolve()
    from importlib.resources import as_file, files

    try:
        bundled = files("staticvita") / "templates"
        if bundled.is_dir():
            return Path(stack.enter_context(as_file(bundled)))
    except ModuleNotFoundError:
        pass
    # Editable install from a source checkout: templates/ live next to staticvita/.
    pkg_dir = Path(__file__).resolve().parent
    checkout = pkg_dir.parent / "templates"
    if checkout.is_dir():
        return checkout.resolve()
    raise RuntimeError(
        f"missing templates directory: {local} "
        "(install staticvita from a wheel, or keep templates/ in the project, "
        "or run from a package source checkout)"
    )


def _copy_static_assets(project_root: Path, dist_static: Path, stack: ExitStack) -> None:
    dist_static.mkdir(parents=True, exist_ok=True)
    from importlib.resources import as_file, files

    copied_base = False
    try:
        bundled = files("staticvita") / "static"
        if bundled.is_dir():
            src = Path(stack.enter_context(as_file(bundled)))
            shutil.copytree(src, dist_static, dirs_exist_ok=True)
            copied_base = True
    except ModuleNotFoundError:
        pass

    if not copied_base:
        pkg_dir = Path(__file__).resolve().parent
        checkout = pkg_dir.parent / "static"
        if checkout.is_dir():
            shutil.copytree(checkout, dist_static, dirs_exist_ok=True)

    proj_static = project_root / "static"
    if proj_static.is_dir():
        shutil.copytree(proj_static, dist_static, dirs_exist_ok=True)


def build_site(
    project_root: Path,
    data_path: Path,
    out_dir: Path | None = None,
) -> None:
    """Load JSON from data_path, render templates into out_dir, copy static, write SEO files."""
    project_root = project_root.resolve()
    out_dir = (project_root / "dist") if out_dir is None else Path(out_dir)
    out_dir = _ensure_out_under_project(project_root, out_dir)

    if not data_path.is_file():
        raise FileNotFoundError(f"missing data file: {data_path}")
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON in {data_path}: {e}") from e

    out_dir.mkdir(parents=True, exist_ok=True)

    with ExitStack() as stack:
        template_dir = _resolve_template_dir(project_root, stack)
        site = Site.make_site(
            searchpath=str(template_dir),
            outpath=str(out_dir),
            env_globals=data,
        )
        site.render()
        _copy_static_assets(project_root, out_dir / "static", stack)

    write_seo_files(data, out_dir)
