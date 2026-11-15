#!/usr/bin/env python3
"""Comprueba integridad y referencias del caso; no certifica cumplimiento NIST."""
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = (
    "24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c",
    "ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa",
    "ec138352c4726fa3b6706b30bf4692252f818108c8066e8518920dd9823a34bb",
)


def check_file(root, relative, expected_hash, expected_size=None):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        return {"archivo": str(relative), "estado": "ERROR", "motivo": "Ruta fuera del caso"}
    result = {"archivo": str(relative), "sha256_esperado": expected_hash}
    if not path.is_file():
        return {**result, "estado": "PENDIENTE", "motivo": "Archivo ausente"}
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    matches = actual == expected_hash and (expected_size is None or len(data) == expected_size)
    return {**result, "sha256_observado": actual, "bytes": len(data),
            "estado": "VERIFICADO" if matches else "ERROR"}


def validate_matrix(rows, valid_codes):
    errors = []
    prefixes = {r.get("subcategoria", "").split(".")[0] for r in rows}
    if prefixes != {"GV", "ID", "PR", "DE", "RS", "RC"}:
        errors.append("La selección debe cubrir las seis funciones de CSF 2.0")
    seen = set()
    required = ("id", "subcategoria", "fuente_localizador", "criterio_comprobacion",
                "estado_historico", "estado_local", "limitacion")
    for row in rows:
        if not all(row.get(key, "").strip() for key in required):
            errors.append(f"Fila incompleta: {row.get('id')}")
        if row.get("id") in seen:
            errors.append(f"Identificador duplicado: {row.get('id')}")
        seen.add(row.get("id"))
        if row.get("subcategoria") not in valid_codes:
            errors.append(f"Subcategoría no encontrada en CSF 2.0: {row.get('subcategoria')}")
        if row.get("estado_local") not in {"PARCIAL", "PENDIENTE", "NO_APLICA"}:
            errors.append(f"Estado local no sustentado por este caso: {row.get('id')}")
    return errors


def main():
    checks, errors = [], []
    sources = json.loads((ROOT / "config/descargas.lock.json").read_text())
    sources += json.loads((ROOT / "config/fuentes-forense.lock.json").read_text())
    for source in sources:
        if source["archivo"].endswith(".pdf"):
            checks.append(check_file(ROOT, source["archivo"], source["sha256"], source["bytes"]))
    for digest in SAMPLES:
        checks.append(check_file(ROOT, f"wannacry/{digest}.exe", digest))
    manifest = ROOT / "local/ghidra/extraidos/manifiesto.json"
    if manifest.exists():
        records = json.loads(manifest.read_text())["records"]
        if not records:
            errors.append("El manifiesto no contiene derivados para verificar")
        for item in records:
            checks.append(check_file(ROOT, item["path"], item["sha256"], item["bytes"]))
    else:
        checks.append({"archivo": str(manifest.relative_to(ROOT)), "estado": "PENDIENTE"})
    with (ROOT / "docs/matriz-nist.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    try:
        text = subprocess.check_output(
            ["pdftotext", "-layout", str(ROOT / "fuentes/NIST.CSWP.29.pdf"), "-"], text=True)
        codes = set(re.findall(r"\b(?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}-\d{2}\b", text))
        errors += validate_matrix(rows, codes)
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"No se pudo comprobar el catálogo CSF: {exc}")
    for path in (ROOT / "plantillas").glob("*.csv"):
        with path.open(newline="") as stream:
            if list(csv.DictReader(stream)):
                errors.append(f"La plantilla debe estar vacía; guardar registros reales en local/: {path.name}")
    tracked = subprocess.check_output(
        ["git", "ls-files", "--", "local", "wannacry", "evidencias"], cwd=ROOT, text=True)
    if tracked.strip():
        errors.append("Git contiene archivos de carpetas reservadas para evidencias")
    for directory in ("local/", "wannacry/", "evidencias/"):
        if subprocess.run(["git", "check-ignore", "-q", directory], cwd=ROOT).returncode:
            errors.append(f"Falta exclusión de Git: {directory}")
    failed = any(c["estado"] == "ERROR" for c in checks) or bool(errors)
    missing = any(c["estado"] == "PENDIENTE" for c in checks)
    result = {
        "observado_utc": datetime.now(timezone.utc).isoformat(),
        "alcance": "Integridad de archivos presentes y códigos de la matriz; no fecha de adquisición ni cumplimiento NIST",
        "estado": "ERROR" if failed else ("PARCIAL" if missing else "VERIFICADO"),
        "archivos": checks, "filas_matriz": len(rows), "errores": errors,
        "limitaciones": ["No prueba procedencia anterior de las muestras ni vínculo con un host del NHS",
                         "No comprueba una ejecución, una captura de memoria o una restauración",
                         "No valida semánticamente por sí solo los hallazgos ni la cadena de custodia"],
    }
    folder = ROOT / "local/revision-nist"
    folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = folder / f"comprobacion-{timestamp}.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"{result['estado']}: {len(checks)} archivos; {len(rows)} filas de matriz. {target}")
    for error in errors:
        print(error)
    return 1 if failed else (2 if missing else 0)


if __name__ == "__main__":
    raise SystemExit(main())
