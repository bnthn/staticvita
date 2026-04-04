# jinja-cv

A small static site generator for a personal CV or resume. [Jinja2](https://jinja.palletsprojects.com/) templates are rendered with data from JSON; CSS, JavaScript, and images are copied into the build output.

## What it does

- **[data/site.json](data/site.json)** supplies globals (profile, links, CV sections) to every template.
- **[templates/](templates/)** holds HTML templates (for example `index.html`, `cv.html`, and partials such as `_base.html`).
- **[static/](static/)** holds assets that are copied to `dist/static/` after HTML is generated.

The build writes everything under **[dist/](dist/)**, which is generated output only.

## Requirements

- Python 3.9+

## Build the site (this repository)

From the repository root:

```bash
./build.sh
```

This creates a local virtual environment at `venv/` if needed, installs the package in editable mode (`pip install -e .` per [requirements.txt](requirements.txt)), and runs **`jinja-cv`**.

Alternatively:

```bash
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
jinja-cv
```

Use a different JSON file (paths are relative to the project root, i.e. current directory by default):

```bash
jinja-cv -i site.ben.json    # tries ./site.ben.json then data/site.ben.json
jinja-cv -i data/site.ben.json
```

Build from another directory as project root:

```bash
jinja-cv -C /path/to/project -i data/site.json
```

Show help and version:

```bash
jinja-cv -h
jinja-cv --version
```

### Repo-local build (cwd-independent)

To build using this repository as the project root **regardless of your shell’s current directory** (same as before a top-level `build.py` existed):

```bash
python scripts/build.py
```

(Requires the package importable, e.g. after `pip install -e .`.)

### Module invocation

```bash
python -m jinja_cv
```

Open [dist/index.html](dist/index.html) in a browser, or serve the `dist/` directory with any static file server.

## Install from PyPI (when published)

```bash
pip install jinja-cv
```

Then run `jinja-cv` in a directory that contains your `data/` JSON (and optional `templates/` / `static/` overrides). Stock templates and base static ship in the package; a project `static/` directory is merged on top.

## Publishing to PyPI (maintainers)

Use a separate output directory so wheel/sdist files are not mixed into the static site’s `dist/` (used for Pages, etc.):

```bash
pip install build twine
python -m build --outdir python-dist
twine upload python-dist/*
```

## Customizing content

| What to change | Where |
|----------------|--------|
| Copy, profile, links, experience, education, etc. | [data/site.json](data/site.json) |
| Page structure and markup | [templates/](templates/) |
| Styles, scripts, images | [static/](static/) |

## Contributing

Edit **source** only:

- `data/` — structured site and CV data
- `templates/` — Jinja HTML
- `static/` — assets served as-is (after copy)

**Do not hand-edit `dist/`.** It is overwritten on every build and must not be treated as the source of truth for changes.

To change how the site is built, edit [jinja_cv/](jinja_cv/) (builder and CLI), [pyproject.toml](pyproject.toml), [build.sh](build.sh), or [requirements.txt](requirements.txt) deliberately. The `venv/` directory is local and is not part of the project’s source layout.

For guidance aimed at automated coding assistants, see [AGENTS.md](AGENTS.md).
