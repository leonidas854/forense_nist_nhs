#!/usr/bin/env bash
# Abre el proyecto local y el MCP únicamente en loopback del anfitrión.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export GHIDRA_INSTALL_DIR="${GHIDRA_INSTALL_DIR:-/opt/ghidra}"
export JAVA_HOME_OVERRIDE="${JAVA_HOME_OVERRIDE:-/usr/lib/jvm/java-27-openjdk}"
export ANONYMIZED_TELEMETRY=False
PYTHON="$ROOT/local/ghidra/herramientas/pyghidra-mcp/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
    echo 'Falta el entorno local; consultar docs/ghidra-mcp.md.' >&2
    exit 1
fi
exec "$PYTHON" "$ROOT/scripts/ghidra_mcp_servidor.py" --gui \
    --transport streamable-http --host 127.0.0.1 --port 8765 \
    --project-path "$ROOT/local/ghidra/proyectos/WannaCry_NHS.gpr" "$@"
