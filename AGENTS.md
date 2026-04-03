# Agent notes

This repository is a **static CV site**: Jinja2 templates plus JSON data plus static assets produce HTML and files under `dist/`.

## Build

From the repository root:

```bash
./build.sh
```

Equivalent: activate a venv, `pip install -r requirements.txt`, then `python build.py`.

## Where to edit

| Purpose | Path |
|---------|------|
| Structured content (profile, CV sections, links) | `data/site.json` |
| HTML / layout | `templates/` |
| CSS, JS, images | `static/` |

## Do not edit

- **`dist/`** — Generated output. It is recreated on build. Never treat files under `dist/` as the source of truth or apply durable fixes only there.

Implementation details (search path, output path, globals injection, static copy) live in `build.py`.

For human-oriented documentation, see [README.md](README.md).
