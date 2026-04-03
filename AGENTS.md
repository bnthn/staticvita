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
| Schema / field docs for `site.json` (keep in sync with templates) | `data/README.md` |
| HTML / layout | `templates/` |
| CSS, JS, images | `static/` (base styles `static/style.css`; optional `site.json` plugin styles `static/plugin.css`, linked from `_base.html`) |

When you change **`templates/`** in ways that affect which JSON fields exist, how they are used, or optional vs required behavior, or when you change the **`data/site.json`** shape or conventions, update **`data/README.md`** so it stays accurate.

## Do not edit

- **`dist/`** — Generated output. It is recreated on build. Never treat files under `dist/` as the source of truth or apply durable fixes only there.

## JavaScript

Keep client-side **JavaScript minimal**. Prefer **static HTML/CSS** and build-time Jinja for layout and visual effects. The theme toggle (`static/theme.js`) is the intended small exception.

Implementation details (search path, output path, globals injection, static copy) live in `build.py`.

For human-oriented documentation, see [README.md](README.md).
