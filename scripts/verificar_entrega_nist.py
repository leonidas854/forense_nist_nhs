#!/usr/bin/env python3
"""Comprueba integridad editorial, autoría y cobertura sin abrir malware."""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'entrega_nist'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    checked = 0
    listed = set()
    for line in (OUT / 'SHA256SUMS').read_text().splitlines():
        expected, rel = line.split('  ', 1)
        path = (OUT / rel).resolve()
        if not path.is_relative_to(OUT):
            raise ValueError(f'Ruta fuera de entrega: {rel}')
        if sha(path) != expected:
            raise ValueError(f'Archivo modificado o ausente: {rel}')
        listed.add(path)
        checked += 1
    actual = {p.resolve() for p in OUT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS'}
    if actual != listed:
        raise ValueError('El manifiesto no cubre exactamente los archivos de la entrega')

    trace = json.loads((OUT / 'trazabilidad.json').read_text())
    for group in ('originales_preservados', 'fuentes_nist_historicas', 'entradas_editoriales'):
        for item in trace[group]:
            path = ROOT / item['archivo']
            # Los originales aportados son locales; un clon puede no tenerlos.
            if group == 'originales_preservados' and not path.exists():
                print('NO DISPONIBLE EN ESTE CLON:', item['archivo'])
                continue
            if sha(path) != item['sha256']:
                raise ValueError(f'Entrada alterada: {item["archivo"]}')

    authors = json.loads((OUT / 'autores.json').read_text())['autores']
    if len(authors) != 8 or len(set(authors)) != 8:
        raise ValueError('Se esperan ocho autores distintos')
    code_index = json.loads((OUT / 'construccion.json').read_text())['transcripciones']
    source = (OUT / 'lectura_completa/parte_practica.md').read_text()
    blocks = re.findall(r'```c\n(.*?)```', source, re.S)
    if len(blocks) != 16 or len(code_index) != 16:
        raise ValueError('Se esperan 16 transcripciones')
    for block, item in zip(blocks, code_index, strict=True):
        if hashlib.sha256(block.encode()).hexdigest() != item['sha256_texto']:
            raise ValueError(f'Cuerpo alterado: {item["direccion"]}')

    for src, name in [('informe_general.md', 'INFORME_GENERAL_NIST_NHS'),
                      ('parte_practica.md', 'PARTE_PRACTICA_NIST_GHIDRA')]:
        md = (OUT / 'lectura_completa' / src).read_text()
        if '{{' in md or re.search(r'\bP[1-4]\b', md):
            raise ValueError('Marcador pendiente o reparto individual en el informe')
        reader = PdfReader(OUT / (name + '.pdf'))
        pages = [p.extract_text() for p in reader.pages]
        text = '\n'.join(pages)
        for author in authors:
            if author not in pages[0]:
                raise ValueError(f'Autor ausente en portada PDF: {author}')
        for required in ['SP 800-86', 'CSF 2.0', '24d004', 'ed01', 'u.wnry', 'ec1383', 'ANY.RUN']:
            if required not in text:
                raise ValueError(f'Falta contenido {required}: {name}')
        for i, page in enumerate(pages):
            if len(page.strip()) < 100:
                raise ValueError(f'Página casi vacía: {name}, {i+1}')
            if '\ufffd' in page or '\x00' in page:
                raise ValueError(f'Carácter de sustitución: {name}, {i+1}')
        word = Document(OUT / (name + '.docx'))
        word_text = '\n'.join(p.text for p in word.paragraphs)
        for author in authors:
            if author not in word_text:
                raise ValueError(f'Autor ausente en Word: {author}')
        if re.search(r'\bP[1-4]\b', text + word_text):
            raise ValueError('Reparto individual presente en los documentos finales')
        print(f'OK: {name}; {len(pages)} páginas PDF; ocho autores; Word legible')

    for path in OUT.rglob('*.md'):
        for url in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            if url.startswith(('https://', 'http://', '#')):
                continue
            target = (path.parent / url.split('#')[0]).resolve()
            if not target.exists():
                raise ValueError(f'Enlace local roto: {path.name} -> {url}')
    with (OUT / 'matriz_nist_entrega.csv').open() as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 20 or len({r['id'] for r in rows}) != 20:
        raise ValueError('Matriz incompleta')
    print(f'OK: {checked} archivos; 16 cuerpos íntegros; 20 resultados NIST; enlaces locales resueltos')
    print('Comprobación editorial: no acredita ejecución, procedencia NHS ni certificación NIST.')


if __name__ == '__main__':
    try:
        verify()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        sys.exit(f'ERROR: {exc}')
