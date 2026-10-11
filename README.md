# staticvita 🪪

A lightweight yet customizable static site generator built on [staticjinja](https://github.com/staticjinja/staticjinja), designed to generate a link tree and CV from JSON data. The focus is on a minimal footprint and producing output that is accessible to both machines (such as search engines and CV parsers) and assistive technologies like screen readers.

**Demo:** [bnthn.github.io/staticvita](https://bnthn.github.io/staticvita)

<p><img alt="Links page, light mode on the top left and dark mode on the bottom right" src="screenshots/links.png" width="31%"> <img alt="Top of the CV page in light mode" src="screenshots/cv_light_top.png" width="31%"> <img alt="Bottom of the CV page in dark mode" src="screenshots/cv_dark_bottom.png" width="31%"></p>

## Requirements

- Python 3.9+

## Install

```bash
pip install staticvita
```

## Build a site

Run `staticvita` in a project directory. If `site.json` is missing, the command writes [site.example.json](site.example.json) and [avatar.example.svg](avatar.example.svg) when those are not already there, then stops. Copy or rename them to `site.json` and `avatar.svg`, then run `staticvita` again. That reads `site.json` and writes the site to `dist/`.

Field reference: [SITE.md](SITE.md).

Stock templates and base styles ship in the package. A `templates/` directory in the project replaces them. A project `static/` directory is merged on top of the packaged assets.

```bash
staticvita                      # site.json → dist/
staticvita -i site.json         # ./site.json, else data/site.json
staticvita -C /path/to/project  # build that directory
```

Open `dist/index.html` in a browser, or serve the `dist/` directory with any static file server.

### This repository

From a clone, at the repository root:

```bash
./build.sh
```

That creates a local virtual environment at `venv/` if needed, installs the package, copies `site.example.json` to `site.json` when that file is missing, copies `avatar.example.svg` to `avatar.svg` when no avatar image is present, and runs `staticvita`.

## Contributing

Development notes are in [CONTRIBUTING.md](CONTRIBUTING.md).
