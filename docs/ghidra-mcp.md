# Trabajar en Ghidra mediante MCP

Preparación comprobada el **15 de noviembre de 2026** en el anfitrión Linux.
Proyecto local: `local/ghidra/proyectos/WannaCry_NHS.gpr`.
Los binarios, proyectos, capturas, respuestas MCP y derivados se conservan fuera
de Git. El proyecto es independiente del proyecto anterior `boat`.

## Abrir y consultar

Desde la raíz del repositorio, cuando la instancia actual esté cerrada:

```bash
./scripts/ghidra-mcp.sh
```

Abre Ghidra y sirve MCP en `http://127.0.0.1:8765/mcp`, exclusivamente en
loopback del anfitrión. No abrir una segunda instancia sobre el mismo proyecto.
Cerrar Ghidra guardando los programas al terminar. Si el puerto está ocupado,
comprobar primero `ss -ltn '( sport = :8765 )'` y la ventana existente.

El servidor `ghidra` quedó registrado en la configuración local de Codex con
`codex mcp add ghidra --url http://127.0.0.1:8765/mcp`. En esta sesión se usó
un cliente Python del protocolo MCP para importar, consultar, decompilar,
anotar, guardar y navegar en la GUI. Las herramientas de un servidor añadido
pueden requerir volver a abrir la sesión para aparecer en su catálogo.
El cliente de terminal permite trabajar directamente mientras tanto:

```bash
PYTHON=local/ghidra/herramientas/pyghidra-mcp/.venv/bin/python
"$PYTHON" scripts/ghidra_mcp_consulta.py tools
"$PYTHON" scripts/ghidra_mcp_consulta.py list_project_binaries
"$PYTHON" scripts/ghidra_mcp_consulta.py list_open_programs
"$PYTHON" scripts/ghidra_mcp_consulta.py get_gui_context
"$PYTHON" scripts/ghidra_mcp_consulta.py save
```

Para una decompilación reproducible:

```bash
"$PYTHON" scripts/ghidra_mcp_consulta.py decompile_function \
  '{"binary_name":"/24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c.exe-e88954","name_or_address":"00408140"}' \
  --output local/ghidra/resultados/consulta-killswitch.json
```

Los nombres del proyecto incluyen un sufijo SHA-1 añadido por el puente MCP;
usar los nombres exactos de `list_project_binaries`. Para imports externos,
emplear la dirección de su entrada IAT al consultar referencias. La resolución
de nombres externos, incluso calificados, falló en este puente; para ajustar
prototipos funcionaron las direcciones `EXTERNAL:` de `search_symbols_by_name`.
Un resultado vacío
con un nombre sin calificar no demuestra ausencia de esa API.

## Recorrido de lectura

| Programa | Qué revisar |
|---|---|
| `24d004…exe-e88954` | `Comprobar_KillSwitch`, `Crear_Servicio_mssecsvc`, `Extraer_Recurso_R_1831`, `Comprobar_Conexion_445` |
| `ed01eb…exe-5ff465` | `Extraer_Paquete_XIA_2058`, `Preparar_Paquete_Y_Permisos` |
| `ec1383…exe-a0366d` | `Extraer_Recurso_W_101`, `Crear_Proceso_Carga` |
| `W_101_contenido.exe-32b201` | PE delimitado dentro de W/101; comparar con 24d004, sin asumir que son idénticos |
| `u.wnry-45356a` | Cadena de sabotaje y referencias en `004066fe` y `0040670c` |
| `taskdl.exe-47a9ad`, `taskse.exe-be5d62` | Auxiliares importados y autoanalizados; interpretación detallada pendiente |

En CodeBrowser, usar **G** para ir a una dirección, **Window → Decompiler**
para ver pseudocódigo, **Symbol Tree → Functions** para los nombres en español
y **Window → Defined Strings** para las cadenas. Los nombres y comentarios
son aportes del analista; no son símbolos originales recuperados.

El resumen técnico está en [analisis-ghidra-codigo.md](analisis-ghidra-codigo.md).
El material completo de esta sesión está en `local/ghidra/LEEME.md`,
`local/ghidra/resultados/` y `local/ghidra/extraidos/manifiesto.json`.
`t.wnry` se conserva como dato cifrado; no se importa como una DLL en claro.

## Instalación y procedencia

Se reutilizó `/opt/ghidra`: **12.2 DEV**, compilación del 10 de noviembre de
2026, con el Java 27 ya instalado. No se equipara esta instalación con el
ZIP 12.2 PUBLIC fijado en `config/descargas.lock.json`, que no se modificó.
El registro complementario es `config/ghidra-mcp-host.lock.json`.

Se instaló [PyGhidra-MCP de clearbluejar](https://github.com/clearbluejar/pyghidra-mcp/tree/f367da41568e6ef5d967c63b56bf640b1a46c3c2)
en el commit `f367da41568e6ef5d967c63b56bf640b1a46c3c2`, con su `uv.lock`.
Este puente admite GUI y consultas MCP sobre el mismo proceso de Ghidra.
Se reemplazó PyGhidra 3.0.2 del lock por la rueda **3.2.0 incluida en la
instalación de Ghidra**, y se añadió `pefile==2024.8.26` para extraer recursos.
Las dependencias efectivas están en `local/ghidra/resultados/dependencias.txt`.

Para reconstruir el entorno en esta misma máquina si falta:

```bash
git clone https://github.com/clearbluejar/pyghidra-mcp.git local/ghidra/herramientas/pyghidra-mcp
git -C local/ghidra/herramientas/pyghidra-mcp checkout --detach f367da41568e6ef5d967c63b56bf640b1a46c3c2
uv sync --frozen --no-dev --python 3.13 --project local/ghidra/herramientas/pyghidra-mcp
uv pip install --python local/ghidra/herramientas/pyghidra-mcp/.venv/bin/python \
  /opt/ghidra/Ghidra/Features/PyGhidra/pypkg/dist/pyghidra-3.2.0-py3-none-any.whl \
  pefile==2024.8.26
```

El adaptador `scripts/ghidra_mcp_servidor.py` pasa expresamente la ruta de un
proyecto existente al lanzador y guarda cada programa además del proyecto.
Chroma mantiene los índices locales, con telemetría desactivada por upstream;
en el primer indexado descargó su modelo ONNX MiniLM. Los binarios no se
enviaron a servicios de análisis. `search_strings` y `search_code` pueden
informar que el índice aún no está listo aunque el autoanálisis haya acabado.
Las consultas por direcciones, símbolos, bytes y decompilación no requieren
esperar a toda la indexación semántica.

## Extracción y límites

```bash
local/ghidra/herramientas/pyghidra-mcp/.venv/bin/python scripts/extraer_recursos_wannacry.py
```

Verifica los tres hashes originales, recorre la tabla de recursos PE,
comprueba tamaños y extrae el ZIP sin ejecutar archivos. Conserva los
originales y rechaza sobrescribir derivados distintos. El manifiesto registra
padres, offsets o miembros ZIP, tamaños y SHA-256: **40 derivados** en esta
sesión. No usar cortes basados solamente en la primera firma `MZ`.

Se ejecutó análisis estático. No se detonó malware, no se instaló Windows ni
se capturó RAM. El mapeo a NIST es retrospectivo. Ningún archivo local demuestra
por sí mismo qué ocurrió en un hospital concreto del NHS.

Validación: 15 pruebas unitarias correctas y `./lab validate` correcto.
En aquella comprobación, `python3 scripts/check_isolation.py` falló por ausencia de la VM registrada
llamada `forense-nhs-win10` en este anfitrión. No se alteró la configuración
de red ni las comparticiones de VirtualBox.

La preparación posterior del mismo día creó la VM y comprobó su aislamiento;
quedó apagada y sin Windows instalado. Estado vigente en [verificacion.md](verificacion.md).
