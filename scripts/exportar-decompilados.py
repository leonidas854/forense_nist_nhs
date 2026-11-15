#!/usr/bin/env python3
"""Exporta funciones seleccionadas por MCP, sin ejecutar ni modificar muestras."""
import asyncio
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    '24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c':
        ['00408140', '00408090', '00407f20', '00407c40', '00407ce0', '00407480'],
    'ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa':
        ['00401dab', '00401fe7', '00401064', '004014a6'],
    'ec138352c4726fa3b6706b30bf4692252f818108c8066e8518920dd9823a34bb':
        ['180001014', '1800010f8', '1800011a4'],
    'b9c5d4339809e0ad9a00d4d3dd26fdf44a32819a54abf846bb9b560d81391c25':
        ['00401bb0', '00401b50', '00401a90'],
}


async def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = ROOT / 'local/exportaciones-ghidra' / stamp
    output.mkdir(parents=True)
    index = ['# Decompilaciones seleccionadas\n',
             'Salida literal del Decompiler; no código original ni registro de ejecución.\n']
    async with streamable_http_client('http://127.0.0.1:8765/mcp') as (read, write, *_):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool('list_project_binaries', {})
            programs = result.model_dump(mode='json', by_alias=True)['structuredContent']['programs']
            for digest, targets in TARGETS.items():
                matches = [p for p in programs if
                           p['metadata'].get('Executable SHA256', '').lower() == digest]
                if len(matches) != 1:
                    raise ValueError(f'Se requiere una muestra identificada inequívocamente: {digest}')
                args = {'binary_name': matches[0]['name'], 'name_or_address': targets}
                result = await session.call_tool('decompile_function', args)
                raw = result.model_dump(mode='json', by_alias=True)
                folder = output / digest[:8]
                folder.mkdir()
                (folder / 'respuesta.json').write_text(json.dumps({
                    'utc': datetime.now(timezone.utc).isoformat(), 'sha256': digest,
                    'tool': 'decompile_function', 'arguments': args, 'response': raw,
                }, ensure_ascii=False, indent=2) + '\n')
                if raw.get('isError'):
                    raise RuntimeError(f'MCP falló; respuesta conservada en {folder}')
                for address, function in zip(targets, raw['structuredContent']['result'], strict=True):
                    if function.get('error'):
                        raise RuntimeError(function['error'])
                    path = folder / (address + '.c')
                    path.write_text(function['code'])
                    index.append(f'- {digest[:8]}: [{function["name"]}]({digest[:8]}/{path.name})')
    (output / 'LEEME.md').write_text('\n'.join(index) + '\n')
    files = sorted(p for p in output.rglob('*') if p.is_file())
    (output / 'SHA256SUMS').write_text(''.join(
        f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output)}\n' for p in files))
    print(output)


if __name__ == '__main__':
    asyncio.run(main())
