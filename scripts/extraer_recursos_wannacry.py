#!/usr/bin/env python3
"""Extrae recursos por sus límites PE; nunca ejecuta las muestras.

Requiere pefile del entorno MCP. Conserva originales, escribe sólo bajo local/
y registra relaciones padre/hijo, offsets, tamaños y hashes de cada derivado.
"""
import hashlib
import io
import json
import re
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pefile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "local/ghidra/extraidos"
HASHES = (
    "24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c",
    "ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa",
    "ec138352c4726fa3b6706b30bf4692252f818108c8066e8518920dd9823a34bb",
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def preserve(path, data):
    if path.exists() and path.read_bytes() != data:
        raise ValueError(f"Se rechaza sobrescribir un derivado distinto: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(data)
        path.chmod(0o600)


def extract():
    records = []
    for expected in HASHES:
        original = (ROOT / "wannacry" / (expected + ".exe")).read_bytes()
        if digest(original) != expected:
            raise ValueError(f"Hash incorrecto: {expected}")
        pe = pefile.PE(data=original)
        for kind in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            resource_type = str(kind.name or kind.id)
            if resource_type not in {"R", "XIA", "W"}:
                continue
            for entry in kind.directory.entries:
                for language in entry.directory.entries:
                    desc = language.data.struct
                    offset = pe.get_offset_from_rva(desc.OffsetToData)
                    data = pe.get_data(desc.OffsetToData, desc.Size)
                    if len(data) != desc.Size or original[offset:offset+desc.Size] != data:
                        raise ValueError("Recurso truncado o límites incompatibles")
                    target = OUTPUT / expected[:8] / f"{resource_type}_{entry.id}_{language.id}.bin"
                    preserve(target, data)
                    records.append(dict(parent=expected, resource=resource_type, id=entry.id,
                                        language=language.id, offset=offset, bytes=len(data),
                                        sha256=digest(data), path=str(target.relative_to(ROOT))))
                    if resource_type == "R" and digest(data) != HASHES[1]:
                        raise ValueError("R/1831 no coincide con ed01...")
                    if resource_type == "W":
                        size = struct.unpack_from("<I", data)[0]
                        if not 64 <= size <= len(data)-4:
                            raise ValueError("Longitud declarada W fuera de límites")
                        child = data[4:4+size]
                        pefile.PE(data=child)  # comprueba MZ y PE, no sólo una firma MZ
                        child_path = target.with_name("W_101_contenido.exe")
                        preserve(child_path, child)
                        records.append(dict(parent=digest(data), offset=4, bytes=size,
                                            sha256=digest(child), path=str(child_path.relative_to(ROOT)),
                                            method="longitud uint32 LE del recurso; validar en decompilación"))
                    if resource_type == "XIA":
                        password = re.search(rb"WNcry@[^\x00]{4}", original)
                        if password is None:
                            raise ValueError("No se encontró la contraseña interna")
                        with zipfile.ZipFile(io.BytesIO(data)) as archive:
                            if sum(i.file_size for i in archive.infolist()) > 100_000_000:
                                raise ValueError("ZIP excede el límite de extracción")
                            for info in archive.infolist():
                                if info.is_dir():
                                    continue
                                base = target.parent / "paquete"
                                path = (base / info.filename).resolve()
                                if not path.is_relative_to(base.resolve()):
                                    raise ValueError("Ruta ZIP fuera del destino")
                                child = archive.read(info, pwd=password.group())
                                preserve(path, child)
                                records.append(dict(parent=digest(data), member=info.filename,
                                                    bytes=len(child), sha256=digest(child),
                                                    path=str(path.relative_to(ROOT))))
    manifest = OUTPUT / "manifiesto.json"
    manifest.write_text(json.dumps({"utc": datetime.now(timezone.utc).isoformat(),
                                    "method": "extracción estática; sin ejecución",
                                    "records": records}, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(records)} derivados registrados: {manifest}")


if __name__ == "__main__":
    extract()
