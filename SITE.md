# Site data (`site.json`)

The build reads JSON (default `site.json` in the project directory) and passes it to the templates. Top-level keys are `profile`, `links`, `cv`, and optionally `seo`, `imprint`, and `plugins`.

Use valid JSON (double quotes, no trailing commas). Then run `staticvita` again.

`dist/` is deleted and written again on every successful build.

## Images

`profile.avatar` is a path relative to the JSON file, such as `avatar.example.svg` or `photos/portrait.png`. The file is copied to `dist/static/images/<filename>` and served as `/static/images/…`. When `seo.base_url` is set, that picture is also `og:image`.

The example JSON sets `"avatar": "avatar.example.svg"`. That file is in the repository and in the package. If it is absent beside the JSON, the build uses the packaged copy. Any other missing path stops the build before `dist/` is cleared. Omit `avatar` or leave it empty to show initials.

## `profile` (object)

Used on `index.html` and `cv.html`.

| Field | Type | Notes |
|--------|------|--------|
| `given_name` | string | Titles and headings. |
| `family_name` | string | Titles and headings. |
| `header_title` | string or omit | Site header link. Empty uses `given_name` and `family_name`. |
| `avatar` | string or omit | See Images. |
| `avatar_alt` | string or omit | `alt` text. Default: `Portrait of {given_name} {family_name}`, or `Profile picture` if both names are empty. |
| `subtitle` | string or omit | Tagline under the name. |
| `email` | string or omit | `mailto:` link on the CV. |
| `location` | string or omit | Shown on the CV. |
| `summary` | string or omit | Intro paragraph on the CV. |

## `links` (array)

Used on the links page. Use `[]` when there are no links.

| Field | Type | Notes |
|--------|------|--------|
| `label` | string | Accessible name for the icon link. |
| `url` | string | Full URL. |
| `fa_class` | string or omit | Font Awesome 7 classes, e.g. `fa-brands fa-github`. Names: [fontawesome.com/icons](https://fontawesome.com/icons). Omitted: generic link icon. |

## `cv` (object)

Used on `cv.html`. Omit a key or use `[]` to hide that section.

Put keywords and job titles in these strings. The page exposes them as plain text. Experience bullets and `cv.skills.entries` are the main places to match a job description. Do not put must-match phrases only in images.

### `cv.experience` (array)

| Field | Type | Notes |
|--------|------|--------|
| `role` | string | Job title. |
| `organization` | string | Company or employer. |
| `start` | string | Shown as-is (e.g. `2021-03`). |
| `end` | string, `null`, or omit | Missing or `null` shows “present”. |
| `bullets` | array of strings or omit | Optional list. |

### `cv.education` (array)

| Field | Type | Notes |
|--------|------|--------|
| `degree` | string | Degree name. |
| `institution` | string | School or university. |
| `year` | string or omit | Shown after the institution. |
| `bullets` | array of strings or omit | Optional list. |

### `cv.skills` (array)

| Field | Type | Notes |
|--------|------|--------|
| `category` | string | Group heading (e.g. “Languages”). |
| `entries` | array of strings | Comma-separated. |

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

When `base_url` is set, the build writes canonical and Open Graph tags, Person JSON-LD on the home page, `sitemap.xml`, and `robots.txt`. Leave `base_url` empty to skip those (for a local `file://` preview).

| Field | Type | Notes |
|--------|------|--------|
| `base_url` | string or omit | Public origin without a trailing slash (e.g. `https://yoursite.example`). |
| `meta_description_home` | string or omit | Home page. Default: `profile.summary`. |
| `meta_description_cv` | string or omit | CV page. Default: `profile.summary`. |
| `meta_description_imprint` | string or omit | Imprint page. Default: `imprint.intro`, truncated. Empty intro emits nothing. |

## `imprint` (object, optional)

Footer link on every page, and optional text on `imprint.html`. Omit the key or set `url` to `""` to hide the link.

| Field | Type | Notes |
|--------|------|--------|
| `url` | string | `imprint.html`, or a full `https://…` URL (`rel="noopener noreferrer"`). |
| `label` | string or omit | Link text. Default: **Impressum**. |
| `page_title` | string or omit | Title and heading. Default: `label`, then **Impressum**. |
| `intro` | string or omit | Lead paragraph. |
| `sections` | array or omit | Each item: optional `heading`, optional `paragraphs` (array of strings). |

## `plugins` (object, optional)

Build-time effects. HTML and CSS only. Styles are in `static/plugin.css`, loaded after `style.css`. Unknown values are ignored.

| Field | Type | Allowed values | Notes |
|--------|------|----------------|--------|
| `headertitle` | string or omit | `contract-vowels` | Header link: vowels stay collapsed until the header is hovered. `aria-label` is the full string (`profile.header_title`). |
| `avatar` | string or omit | `float-on-hover` | Home page. Hover scales and tilts the portrait, adds shadow or a glow in the accent hue, and a gloss. |
| `accent` | string or omit | `blue`, `green`, `red`, `yellow`, `orange`, `purple`, `mint`, `brown` | Link color and the faint hue of background, text, borders, and social buttons. `blue`, omitted, or unknown keeps the default palette. Other values keep that lightness and change the hue. |

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

`site.example.json` at the repository root is a filled-in example.
