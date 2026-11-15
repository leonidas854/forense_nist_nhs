#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
sha256sum -c config/SHA256SUMS
if [ ! -x local/host-tools/bin/python ]; then
  python3 -m venv local/host-tools
fi
if ! local/host-tools/bin/python -c 'import pycdlib' 2>/dev/null; then
  local/host-tools/bin/python -m pip install 'pycdlib==1.14.0'
fi
local/host-tools/bin/python scripts/build-tools-iso.py
