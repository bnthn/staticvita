#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x venv/bin/python ]] || ! venv/bin/python -c 'import sys' 2>/dev/null; then
  echo "build.sh: creating virtual environment (venv/)..."
  rm -rf venv
  python3 -m venv venv
fi

# Install once; pip builds in an isolated env and fetches the build backend
# (hatchling) from the network, which is slow and can look like a hang.
# Delete venv/ to force a reinstall (e.g. after changing dependencies).
# Query the installed distribution, not an import: the source dir is on cwd.
if ! venv/bin/python -c 'import importlib.metadata as m; m.version("staticvita")' 2>/dev/null; then
  echo "build.sh: installing staticvita and dependencies (one-time)..."
  venv/bin/python -m pip install --disable-pip-version-check --no-input -e .
fi

if [[ ! -f site.json ]]; then
  cp site.example.json site.json
fi
has_avatar=0
for ext in svg png jpg jpeg webp gif avif; do
  if [[ -f "avatar.${ext}" ]]; then
    has_avatar=1
    break
  fi
done
if [[ "$has_avatar" -eq 0 ]]; then
  cp avatar.example.svg avatar.svg
fi

echo "build.sh: building site into dist/..."
venv/bin/python -m staticvita "$@"
