#!/usr/bin/env python3
"""DVD local: herramientas fijadas, fuentes, guías y lecturas; sin muestras PE."""
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import pycdlib

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    'plan-trabajo-equipo-4.md', 'guia-capas-decompilado-desensamblado.md',
    'recorrido-ghidra-explicado.md', 'informe-forense.md',
    'guia-comprobacion-nist.md', 'analisis-ghidra-codigo.md',
    'ghidra-mcp.md', 'laboratorio.md', 'materiales-preparados.md', 'matriz-nist.csv',
]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def collect():
    files = []
    for lock in ['config/descargas.lock.json', 'config/fuentes-forense.lock.json']:
        files.append(Path(lock))
        for item in json.loads((ROOT / lock).read_text()):
            p = ROOT / item['archivo']
            if digest(p) != item['sha256']:
                raise ValueError(f'Hash distinto del manifiesto: {p.name}')
            files.append(Path(item['archivo']))
    files += [Path('docs') / name for name in DOCS]
    files += [Path('config/SHA256SUMS'), Path('config/sysmon-lab.xml')]
    # Exportaciones de texto, nunca muestras, discos ni proyectos mutables.
    for folder in ['local/decompilados-ghidra', 'local/ec1383-detalle']:
        files += [p.relative_to(ROOT) for p in (ROOT / folder).rglob('*')
                  if p.is_file() and (p.suffix in {'.c', '.md', '.json'} or p.name == 'SHA256SUMS')]
    return sorted(set(files))


def main():
    files = collect()
    records = [{'archivo': str(p), 'bytes': (ROOT / p).stat().st_size,
                'sha256': digest(ROOT / p)} for p in files]
    manifest = json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
                           'alcance': 'Herramientas originales y material de lectura; sin malware ejecutable',
                           'archivos': records}, ensure_ascii=False, indent=2).encode()
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, vol_ident='NHS_TOOLS')
    dirs = {Path('.'): ''}
    parents = sorted({parent for p in files for parent in p.parents if parent != Path('.')},
                     key=lambda p: (len(p.parts), str(p)))
    for i, p in enumerate(parents):
        dirs[p] = dirs[p.parent] + f'/D{i:04d}'
        iso.add_directory(iso_path=dirs[p], joliet_path='/' + p.as_posix())
    for i, p in enumerate(files):
        iso.add_file(str(ROOT / p), iso_path=dirs[p.parent] + f'/F{i:04d}.BIN;1',
                     joliet_path='/' + p.as_posix())
    data = io.BytesIO(manifest)
    iso.add_fp(data, len(manifest), iso_path='/INVENTAR.JSON;1', joliet_path='/INVENTARIO.json')
    target = ROOT / 'local/herramientas.iso'
    tmp = target.with_suffix('.iso.part')
    iso.write(str(tmp))
    iso.close()
    tmp.replace(target)
    (ROOT / 'local/preparacion/kit-manifiesto.json').parent.mkdir(parents=True, exist_ok=True)
    (ROOT / 'local/preparacion/kit-manifiesto.json').write_bytes(manifest)
    target.with_suffix('.iso.sha256').write_text(f'{digest(target)}  herramientas.iso\n')
    print(f'{target}: {len(files)} archivos; manifiesto y SHA-256 guardados')


if __name__ == '__main__':
    main()
