#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -x venv/bin/python ]]; then
  python3 -m venv venv
  venv/bin/pip install -r requirements.txt
fi

venv/bin/python build.py
