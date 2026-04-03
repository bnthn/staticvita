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

## Accessibility and progressive enhancement

- **No-JS baseline:** All meaningful content and navigation must work with JavaScript disabled. JS is only for theme preference (`static/theme.js`).
- **Theme control:** The theme toggle is **hidden by default** in CSS and only shown when `theme.js` runs and adds the class `js` on `<html>`, so users do not see a non-functional control without JS.
- **Design vs accessibility:** When the intended visual design conflicts with an accessibility or text-browser improvement, **follow the design** and document any tradeoff in PRs or here. Example: icon-only controls use `aria-label` plus a `.visually-hidden` text label when needed (header nav, profile social links) so screen readers and Lynx get real link text—`aria-label` alone is often ignored in line-mode browsers.
- **Images and icons:** Use non-empty, appropriate `alt` on `<img>` (see `profile.avatar_alt` in `data/README.md` for the profile image). Decorative Font Awesome icons use `aria-hidden="true"`; put the accessible name on the parent control (`aria-label` on `<a>` / the theme button).
- **HTML quality:** Keep templates producing **valid, semantic HTML** (landmarks, headings, `lang`). After template changes, run `./build.sh` and fix issues; CI may run `html5validator` on `dist/`.

## Text browsers (e.g. Lynx)

The site should remain usable in line-mode browsers: links and headings must be meaningful. The default layout prioritizes a compact icon header; for icon-only links, use `.visually-hidden` link text (CSS-hidden in graphical browsers) so Lynx still shows a name, and keep `aria-label` on the control for redundancy.
