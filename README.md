# staticvita 🪪

A small static site generator to create a link tree and CV from JSON. It aims for a minimal footprint and for output that reads well to machines (search engines, CV parsers) and to assistive technologies such as screen readers.

**Demo:** [bnthn.github.io/staticvita](https://bnthn.github.io/staticvita)

<p><img alt="Links page, light mode on the top left and dark mode on the bottom right" src="screenshots/links.png" width="31%"> <img alt="Top of the CV page in light mode" src="screenshots/cv_light_top.png" width="31%"> <img alt="Bottom of the CV page in dark mode" src="screenshots/cv_dark_bottom.png" width="31%"></p>

## Requirements

- Python 3.9+

## Install

```bash
pip install staticvita
```

## Build a site

Run `staticvita` in a project directory. By default it reads `data/site.json` and writes the site to `dist/`.

Stock templates and base styles ship in the package. A `templates/` directory in the project replaces them. A project `static/` directory is merged on top of the packaged assets.

```bash
staticvita
staticvita -i site.ben.json    # tries ./site.ben.json then data/site.ben.json
staticvita -i data/site.ben.json
staticvita -C /path/to/project -i data/site.json
staticvita -h
staticvita --version
```

Open `dist/index.html` in a browser, or serve the `dist/` directory with any static file server.

### This repository

From a clone, at the repository root:

```bash
./build.sh
```

That creates a local virtual environment at `venv/` if needed, installs the package, and runs `staticvita` on this repo’s `data/site.json`.

## What to edit

| What to change | Where |
|----------------|--------|
| Copy, profile, links, experience, education, etc. | [data/site.json](data/site.json) |
| Profile picture / user images | `data/` (e.g. `data/images/avatar.svg`; copied into `dist/static/`) |
| Page structure and markup | [templates/](templates/) |
| Styles, scripts | [static/](static/) |

`data/site.json` supplies profile, links, and CV sections to every template. Other non-JSON files in `data/` are copied into `dist/static/`. `dist/` is generated on each build.

Contributor notes, including how the package is built and published, are in [CONTRIBUTING.md](CONTRIBUTING.md).
