# Estado Comprobado · 15 de noviembre de 2026
## Caso WannaCry en el NHS con NIST CSF 2.0 · Paquete de Defensa Oral, Datos Forenses y Dashboard HTML

## 1. Preparación y Entregables Completados

- **Repositorio y Sincronización:** Cuenta `leonidas854`, repositorio `forense_nist_nhs`. `git pull` ejecutado confirmando sincronización plena con `origin/main`.
- **Organización del Equipo de 8 Peritos:** Estructura formalizada en `docs/roles-equipo-8.md`, con matriz RACI, asignación temática de las 6 funciones de NIST CSF 2.0 y justificación metodológica de la división pericial.
- **Defensa Oral para 2 Expositores:** Guion palabra por palabra en `docs/guion-exposicion.md` (24 minutos de ponencia + 6 min de preguntas), con transiciones, énfasis pericial y distribución de preguntas difíciles entre los 8 especialistas.
- **Diapositivas Proyectables:** Presentación en formato Marp/Markdown en `docs/diapositivas.md` (22 diapositivas técnicas con cronología, diagramas de arquitectura, tablas comparativas de la NAO, código decompilado y lecciones de resiliencia).
- **Banco de Preguntas del Tribunal:** 20 preguntas desafiantes con respuestas sustentadas en código, comandos y auditorías oficiales en `docs/preguntas-defensa.md`.
- **Informe Forense Maestro:** Redacción completa del dictamen pericial académico en `docs/informe-forense.md`, bajo normas APA 7 y con citas cruzadas a los informes de la NAO (2018), DHSC (2018), NIST CSWP 29 (2024), NIST IR 8374 Rev. 1 (2026) y NIST SP 800-61 Rev. 3 (2025).
- **Cuadro de Mando Interactivo HTML (NIST CSF 2.0):** Implementado en `docs/dashboard-forense-nist.html`, permitiendo navegación visual interactiva de las 6 funciones, visor de código decompilado en Ghidra, línea de tiempo interactiva con buscador, inventario de evidencias con verificación de hashes y matriz RACI del equipo.
- **Ingeniería Inversa Estática en Ghidra:** Documentación exhaustiva en `docs/analisis-ghidra-codigo.md` (mapa de memoria, decompilación de `WinMain`, Kill Switch, `CreateServiceA`, dropper `.rsrc/R`, sabotaje `vssadmin` y criptografía híbrida AES-128 + RSA-2048) complementada con el script pericial `scripts/analisis-ghidra-pe.py`.
- **Poblado Exhaustivo de Plantillas Forenses:**
  - `plantillas/inventario-evidencias.csv`: 10 evidencias formales (EVI-001 a EVI-010) con tamaño y SHA-256 verificado.
  - `plantillas/cadena-custodia.csv`: 10 registros de trazabilidad, traspaso, análisis y sellado.
  - `plantillas/bitacora.csv`: 14 registros de actividades periciales, comandos ejecutados, snapshots y tiempos UTC.
  - `plantillas/hallazgos.csv`: 12 hallazgos técnicos correlacionados con las categorías del NIST CSF 2.0.
  - `plantillas/timeline.csv`: 17 hitos cronológicos estructurados desde marzo de 2017 hasta 2026.
- **Skills del Proyecto Instaladas (`npx skills`):** 5 skills integradas en `.agents/skills/`: `attack-tree-construction`, `diagram-design`, `security-best-practices`, `security-threat-model`, `threat-mitigation-mapping`.
- **Matriz Retrospectiva NIST CSF 2.0:** Ampliada en `docs/matriz-nist.csv` con asignación individual de roles, preguntas de trabajo, fuentes primarias y evidencias de laboratorio.
- **Laboratorio Aislado:** Estación de trabajo Windows 10 x64 gestionada mediante Vagrant 2.4.9 y VirtualBox 7.2 con comunicador `none` y 8 tarjetas de red deshabilitadas.
- **Herramientas de Análisis:** Imagen ISO montada como DVD de solo lectura (`local/herramientas.iso`) con Ghidra 12.2, OpenJDK 25, Volatility 3 fijado en commit `881e970`, WinPmem RC2, Sysinternals y Wireshark 4.6.9.

---

## 2. Comprobaciones Técnicas Automatizadas

| Comprobación | Comando | Resultado Comprobado |
|---|---|---|
| **Pruebas de aislamiento pericial** | `python3 -m unittest discover -s tests -v` | **5/5 pruebas correctas** (Rechazo de NICs activas, carpetas compartidas y escape de red). |
| **Validación de Vagrantfile** | `./lab validate` | **Correcto** (Comunicador `none_communicator` experimental validado). |
| **Inspección real del hipervisor** | `python3 scripts/check_isolation.py` | **Correcto** (8 NIC desactivadas; sin carpetas compartidas, clipboard, drag/drop ni VRDE). |
| **Integridad de descargas** | `sha256sum -c config/SHA256SUMS` | **11/11 archivos coincidentes** con hashes de descarga congelados. |
| **Integridad de CSVs poblados** | `python3 -c "import csv, glob; ..."` | **5/5 CSVs válidos** y completamente poblados de datos. |
| **Script pericial de inspección PE** | `python3 scripts/analisis-ghidra-pe.py --help` | **Ejecución limpia y sin dependencias externas**. |
| **Skills instaladas en el proyecto** | `npx skills ls` | **5 skills activas** en `.agents/skills/`. |
| **Sincronización remota** | `git pull` | **Already up to date**. |

---

## 3. Delimitación y Límites de la Pericia

- **Distinción entre Fuentes:** El informe preserva la separación estricta entre la **auditoría histórica certificada** del NHS/NAO, las **observaciones de ingeniería inversa estática** en Ghidra 12.2 y las **evidencias de laboratorio en la máquina virtual**.
- **Ética de no detonación:** No se ha ejecutado una detonación destructiva de malware con salida a internet. El comportamiento del Kill Switch y del dropper se determinó formalmente mediante desensamblado estático en Ghidra.
- **Preservación de Git:** Ninguna clave, contraseña privada, muestra viva ni disco virtual ha sido incorporado a Git, respetando estrictamente `AGENTS.md` y `BRIEF.md`.

---

## 4. Estado de los Entregables y Pendientes Académicos

| Entregable | Archivo | Estado |
|---|---|:---:|
| **Informe Forense Maestro** | `docs/informe-forense.md` | **COMPLETO** |
| **Organización Equipo 8** | `docs/roles-equipo-8.md` | **COMPLETO** |
| **Guion 2 Expositores** | `docs/guion-exposicion.md` | **COMPLETO** |
| **Diapositivas Marp** | `docs/diapositivas.md` | **COMPLETO** |
| **Banco de Preguntas** | `docs/preguntas-defensa.md` | **COMPLETO** |
| **Dashboard Interactivo HTML** | `docs/dashboard-forense-nist.html` | **COMPLETO** |
| **Análisis de Código Ghidra** | `docs/analisis-ghidra-codigo.md` | **COMPLETO** |
| **Script Pericial PE** | `scripts/analisis-ghidra-pe.py` | **COMPLETO** |
| **Plantillas CSV Pobladas** | `plantillas/*.csv` | **COMPLETO (5/5)** |
| **Skills Instaladas** | `.agents/skills/` | **COMPLETO (5 skills)** |
| **Matriz NIST CSF 2.0** | `docs/matriz-nist.csv` | **COMPLETO** |
| **Guía de Laboratorio** | `docs/laboratorio.md` | **COMPLETO** |
| **Metadatos y Alcance** | `BRIEF.md` / `README.md` | **COMPLETO** |
| **Nombres del Grupo** | Nombres de los estudiantes | Reemplazar nombres reales en carátulas |
