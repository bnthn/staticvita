# Site data (`site.json`)

The build reads **`site.json`** in this directory (`build.py` loads it and passes the whole object into the Jinja environment). Top-level keys become template variables: `profile`, `links`, `cv`, optionally `seo`, optionally `imprint`, and optionally `plugins` (conventionally list `plugins` last in the file).

Use valid JSON (double quotes, no trailing commas). After editing, run `./build.sh` from the repository root.

## `profile` (object)

Used on the links page (`index.html`) and the CV page (`cv.html`).

| Field | Type | Notes |
|--------|------|--------|
| `given_name` | string | Shown in titles and headings. |
| `family_name` | string | Shown in titles and headings. |
| `header_title` | string or omit | If set to a non-empty string, used for the site header `<h1>` link on all pages instead of `given_name` + `family_name`. Omit or leave empty to use the name. |
| `avatar` | string or omit | Path **relative to `static/`** (e.g. `images/avatar.svg`). If omitted or empty, initials are shown from the name. |
| `avatar_alt` | string or omit | `alt` text for the profile `<img>`. If omitted, defaults to `Portrait of {given_name} {family_name}` or `Profile picture` if both names are empty. |
| `subtitle` | string or omit | Tagline under the name. |
| `email` | string or omit | Rendered as a `mailto:` link on the CV. |
| `location` | string or omit | Shown on the CV. |
| `summary` | string or omit | Intro paragraph on the CV. |

## `links` (array)

Used on the links page. Each item is an object:

| Field | Type | Notes |
|--------|------|--------|
| `label` | string | Accessible name / `aria-label` for the icon link. |
| `url` | string | Full URL. |
| `icon` | string or omit | Short name mapped to Font Awesome in `_icons.html`: `linkedin`, `github`, `gitlab`, `codeberg`. Anything else falls back to a generic link icon. |
| `fa_class` | string or omit | If set, used **instead of** `icon` for the `<i>` classes (Font Awesome 6), e.g. `fa-solid fa-code-branch`. |

Use an empty array `[]` if you have no social links.

## `cv` (object)

Used on `cv.html`. Each subsection is optional: omit the key or use an empty array to hide that section.

### `cv.experience` (array)

| Field | Type | Notes |
|--------|------|--------|
| `role` | string | Job title. |
| `organization` | string | Company or employer. |
| `start` | string | Shown as-is (e.g. `2021-03`). |
| `end` | string, `null`, or omit | If missing or `null`, the template shows “present”. |
| `bullets` | array of strings or omit | Optional bullet list. |

### `cv.education` (array)

| Field | Type | Notes |
|--------|------|--------|
| `degree` | string | e.g. degree name. |
| `institution` | string | School or university. |
| `year` | string or omit | Shown after the institution. |
| `bullets` | array of strings or omit | Optional bullet list. |

### `cv.skills` (array)

Each element:

| Field | Type | Notes |
|--------|------|--------|
| `category` | string | Group heading (e.g. “Languages”). |
| `entries` | array of strings | Rendered comma-separated. |

### `cv.projects` (array)

| Field | Type | Notes |
|--------|------|--------|
| `name` | string | Project title. |
| `url` | string or omit | If set, the name is a link. |
| `description` | string or omit | Shown under the name. |

### `cv.certifications` (array)

| Field | Type | Notes |
|--------|------|--------|
| `name` | string | Certification title. |
| `issuer` | string | Issuing organization. |
| `year` | string or omit | Shown after the issuer. |

## `seo` (object, optional)

Controls canonical URLs, Open Graph meta tags, optional **Person** JSON-LD on the home page, and—when `base_url` is set—generated **`sitemap.xml`** and **`robots.txt`** in `dist/` (written by `build.py` after HTML render). Omit the key or leave `base_url` empty to skip absolute URLs and sitemap generation (e.g. local `file://` preview); in that case any existing `dist/sitemap.xml` / `dist/robots.txt` from a previous build are removed.

| Field | Type | Notes |
|--------|------|--------|
| `base_url` | string or omit | Public site origin **without** a trailing slash (e.g. `https://yoursite.example`). Used for `link rel="canonical"`, `og:url`, JSON-LD `url`, and sitemap `loc` values. |
| `og_image` | string or omit | Open Graph image for link previews: either a full `https://…` (or `http://…`) URL, or a path **relative to `static/`** (e.g. `images/avatar.svg`), resolved against `base_url` as `/static/…`. |

Optional overrides for `meta name="description"`:

| Field | Type | Notes |
|--------|------|--------|
| `meta_description_home` | string or omit | Home page (`index.html`). If omitted, `profile.summary` is used when set. |
| `meta_description_cv` | string or omit | CV page. If omitted, `profile.summary` is used when set. |
| `meta_description_imprint` | string or omit | Imprint page. If omitted, `imprint.intro` is used (truncated); if that is empty, nothing is emitted. |

## `imprint` (object, optional)

Legal / provider identification link in the site footer on all pages, and optional content on `imprint.html`. Omit the key or set `url` to an empty string to hide the footer link entirely.

| Field | Type | Notes |
|--------|------|--------|
| `url` | string | Footer link `href`. Use a path such as `imprint.html` for the built-in page, or a full `https://…` URL if the legal text is hosted elsewhere. External URLs get `rel="noopener noreferrer"`. |
| `label` | string or omit | Footer link text. Defaults to **Impressum** if omitted. |
| `page_title` | string or omit | Document `<title>` prefix and main heading on `imprint.html`. Defaults to `label`, then **Impressum**. |
| `intro` | string or omit | Optional lead paragraph on `imprint.html`. |
| `sections` | array or omit | Each item: optional `heading` (string) and optional `paragraphs` (array of strings). Rendered as sections on `imprint.html`. |

## `plugins` (object, optional)

Optional presentation effects applied at build time (HTML/CSS only, no extra JavaScript). Omit the key or omit inner keys to keep default styling. Styles for these plugins live in **`static/plugin.css`** (loaded after `style.css`).

Effect values use **kebab-case** (e.g. `contract-vowels`). Unknown values are ignored (templates fall back to plain markup).

| Field | Type | Allowed values | Notes |
|--------|------|----------------|--------|
| `headertitle` | string or omit | `contract-vowels` | Site header `<h1>` link on all pages: vowels stay visually collapsed until the header bar is hovered; the link’s `aria-label` matches the same string shown in the header (see `profile.header_title`). |
| `avatar` | string or omit | `float-on-hover` | Home page (`index.html`) only: idle looks like the default avatar; on hover the disc scales slightly, tilts in 3D, gains layered shadow (light theme) or a soft white/blue glow (dark theme), plus a gloss overlay that rotates slightly with the pop. Pointer-based parallax is not available in pure CSS (would need a small script). |

## Minimal skeleton

```json
{
  "profile": {
    "given_name": "",
    "family_name": "",
    "subtitle": "",
    "email": "",
    "location": "",
    "summary": ""
  },
  "links": [],
  "cv": {
    "experience": [],
    "education": [],
    "skills": [],
    "projects": [],
    "certifications": []
  },
  "seo": {
    "base_url": ""
  },
  "plugins": {}
}
```

See the checked-in **`site.json`** in this folder for a full example (including optional `plugins` at the end).
