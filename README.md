# jinja-cv

A small static site generator for a personal CV or resume. [Jinja2](https://jinja.palletsprojects.com/) templates are rendered with data from JSON; CSS, JavaScript, and images are copied into the build output.

## What it does

- **[data/site.json](data/site.json)** supplies globals (profile, links, CV sections) to every template.
- **[templates/](templates/)** holds HTML templates (for example `index.html`, `cv.html`, and partials such as `_base.html`).
- **[static/](static/)** holds assets that are copied to `dist/static/` after HTML is generated.

The build script writes everything under **[dist/](dist/)**, which is generated output only.

## Requirements

- Python 3

## Build the site

From the repository root:

```bash
./build.sh
```

This creates a local virtual environment at `venv/` if needed, installs dependencies from [requirements.txt](requirements.txt), and runs [build.py](build.py).

Alternatively:

```bash
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python build.py
```

Open [dist/index.html](dist/index.html) in a browser, or serve the `dist/` directory with any static file server.

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

To change how the site is built (dependencies, paths, copy steps), edit [build.py](build.py), [build.sh](build.sh), or [requirements.txt](requirements.txt) deliberately. The `venv/` directory is local and is not part of the project’s source layout.

For guidance aimed at automated coding assistants, see [AGENTS.md](AGENTS.md).
