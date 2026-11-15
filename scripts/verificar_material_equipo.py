#!/usr/bin/env python3
"""Verifica la edición didáctica en cualquier clon, sin muestras ni Ghidra."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify():
    checked = 0
    for line in (ROOT / 'equipo/SHA256SUMS').read_text().splitlines():
        expected, relative = line.split('  ', 1)
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError(f'Ruta fuera del repositorio: {relative}')
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Hash distinto: {relative}')
        checked += 1
    index = json.loads((ROOT / 'equipo/indice.json').read_text())
    functions = 0
    for person in index['participantes']:
        path = (ROOT / 'equipo' / person['carpeta'] / 'codigo.md').resolve()
        if not path.is_relative_to(ROOT / 'equipo'):
            raise ValueError('Carpeta fuera del material del equipo')
        text = path.read_text()
        blocks = re.findall(r'```c\n(.*?)```', text, re.DOTALL)
        for block, entry in zip(blocks, person['funciones'], strict=True):
            if hashlib.sha256(block.encode()).hexdigest() != entry['bloque_publicado_sha256']:
                raise ValueError(f'Transcripción distinta: {person["participante"]} {entry["direccion"]}')
            if f'id="f-{entry["direccion"]}"' not in text:
                raise ValueError(f'Falta ancla de función: {entry["direccion"]}')
            functions += 1
    if len(index['participantes']) != 4 or functions != 16 or checked == 0:
        raise ValueError('Edición incompleta: se esperan cuatro participantes y 16 funciones')
    print(f'OK: {checked} archivos; cuatro participantes; {functions} transcripciones coherentes.')
    print('Verifica integridad editorial; no demuestra ejecución, procedencia histórica ni cumplimiento NIST.')


if __name__ == '__main__':
    try:
        verify()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        sys.exit(f'ERROR: {exc}')
