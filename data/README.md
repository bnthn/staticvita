# Site data (`site.json`)

The build reads **`site.json`** in this directory (`build.py` loads it and passes the whole object into the Jinja environment). Top-level keys become template variables: `profile`, `links`, and `cv`.

Use valid JSON (double quotes, no trailing commas). After editing, run `./build.sh` from the repository root.

## `profile` (object)

Used on the links page (`index.html`) and the CV page (`cv.html`).

| Field | Type | Notes |
|--------|------|--------|
| `given_name` | string | Shown in titles and headings. |
| `family_name` | string | Shown in titles and headings. |
| `avatar` | string or omit | Path **relative to `static/`** (e.g. `images/avatar.svg`). If omitted or empty, initials are shown from the name. |
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
  }
}
```

See the checked-in **`site.json`** in this folder for a full example.
