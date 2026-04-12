# Agent notes

This repository is a **static CV site**: Jinja2 templates plus JSON data plus static assets produce HTML and files under `dist/`.

## Build

From the repository root:

```bash
./build.sh
```

The package is defined in [`pyproject.toml`](pyproject.toml); dependencies are declared there (`staticjinja`). [requirements.txt](requirements.txt) pins an editable install (`-e .`) for local development.

Equivalent: activate a venv, `pip install -r requirements.txt`, then `staticvita` (or `python -m staticvita`). To build from this repo with a **fixed project root** independent of cwd, use `python scripts/build.py` after an editable install.

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

Implementation details (search path, output path, globals injection, static copy) live in [`staticvita/builder.py`](staticvita/builder.py) and the CLI in [`staticvita/cli.py`](staticvita/cli.py).

For human-oriented documentation, see [README.md](README.md).

## Priorities when changing the generator

Keep **design requirements**, **search engine optimization (SEO)**, **CV parsing / ATS friendliness** (see below), and **accessibility** (including line-mode browsers such as Lynx) in mind for every change.

When those goals conflict, resolve them in this order:

1. **Design** first.
2. **SEO** and **CV parser optimization** (ATS, resume matchers such as Jobscan-style tools, AI-assisted screening that ingests page text) **together, as equals**—if SEO and CV parsing pull in different directions, **document the tradeoff** in PRs or here rather than silently favoring one.
3. **Accessibility** last among these priorities.

Document other notable tradeoffs in PRs or here.

## CV parsing / ATS

Many applications are filtered by **ATS (Applicant Tracking System)** parsers, **resume–job match tools** (e.g. Jobscan), or **AI assistants** that extract plain text from a CV. This site’s CV is the built **`cv.html`** page and its **`site.json`** source—not a separate PDF upload—so keep that output **machine-readable** as well as human-readable.

- **Content:** Roles, skills, summaries, and bullets in `data/site.json` are what parsers see; use **plain text** for facts and keywords you want matched. Do not rely on images, icons, or hidden text for critical terms (the profile avatar is decorative; body copy matters).
- **Markup:** In `templates/cv.html`, favor **semantic, stable structure** (sections, headings, lists, normal links) so extraction order stays predictable. Changes here should not regress Lynx or screen-reader usability when avoidable—overlap with accessibility is usually high.

## Accessibility and progressive enhancement

- **No-JS baseline:** All meaningful content and navigation must work with JavaScript disabled. JS is only for theme preference (`static/theme.js`).
- **Theme control:** The theme toggle is **hidden by default** in CSS and only shown when `theme.js` runs and adds the class `js` on `<html>`, so users do not see a non-functional control without JS.
- **Tradeoffs:** If design, SEO, CV parsing, and accessibility cannot all be fully satisfied, follow the **Priorities** order above. Example of balancing an icon-only visual with text-browser usability: use `aria-label` plus a `.visually-hidden` text label where needed (header nav, profile social links) so screen readers and Lynx get real link text—`aria-label` alone is often ignored in line-mode browsers.
- **Images and icons:** Use non-empty, appropriate `alt` on `<img>` (see `profile.avatar_alt` in `data/README.md` for the profile image). Decorative Font Awesome icons use `aria-hidden="true"`; put the accessible name on the parent control (`aria-label` on `<a>` / the theme button).
- **HTML quality:** Keep templates producing **valid, semantic HTML** (landmarks, headings, `lang`). After template changes, run `./build.sh` and fix issues.

## Text browsers (e.g. Lynx)

The site should remain usable in line-mode browsers: links and headings must be meaningful. The default layout prioritizes a compact icon header; for icon-only links, use `.visually-hidden` link text (CSS-hidden in graphical browsers) so Lynx still shows a name, and keep `aria-label` on the control for redundancy.
