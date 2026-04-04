#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x venv/bin/python ]]; then
  python3 -m venv venv
fi

venv/bin/pip install -q -e .
venv/bin/jinja-cv
