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
local/host-tools/bin/python - <<'PY'
from pathlib import Path
import json
import pycdlib

items = json.loads(Path('config/descargas.lock.json').read_text())
files = [Path(x['archivo']) for x in items if x['archivo'].startswith('descargas/')]
files += [Path('config/sysmon-lab.xml'), Path('config/SHA256SUMS'), Path('docs/laboratorio.md')]
iso = pycdlib.PyCdlib()
iso.new(interchange_level=3, joliet=3, vol_ident='NHS_TOOLS')
for i, path in enumerate(files):
    iso.add_file(str(path), iso_path=f'/F{i:04d}.BIN;1', joliet_path='/'+path.name)
iso.write('local/herramientas.iso.part')
iso.close()
Path('local/herramientas.iso.part').replace('local/herramientas.iso')
print('Creada local/herramientas.iso; herramientas originales, sin autorun.')
PY
