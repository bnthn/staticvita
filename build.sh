#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x venv/bin/python ]] || ! venv/bin/python -c 'import sys' 2>/dev/null; then
  rm -rf venv
  python3 -m venv venv
fi

venv/bin/python -m pip install -q -e .
venv/bin/python -m staticvita "$@"
