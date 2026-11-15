# Estado Comprobado · 15 de noviembre de 2026

## Diagramas y análisis general

- Añadidos [15 diagramas Mermaid](../equipo/DIAGRAMAS-Y-ANALISIS.md): cuatro
  generales y once distribuidos entre P1–P4. Separan contenido de los archivos,
  decisiones del código, secuencia histórica, método forense y consulta de ANY.RUN.
- Los flujos se contrastaron con las transcripciones y con el Listing conservado;
  las agrupaciones de condiciones y limitaciones se explican junto a cada diagrama.
  No se afirma cobertura de todas las funciones ni observación de una ejecución.
- El usuario aclaró que el HTTP 500 apareció en la página de ANY.RUN. Se documenta
  como información comunicada, sin informe dinámico aportado ni relación causal
  demostrada con la muestra o con el kill switch.
- Renderizado local correcto de los 15 diagramas, con Mermaid 11.12.0 y Chromium;
  salidas y registro de validación en `local/preparacion/diagramas/`.
  Esa dependencia local de comprobación no altera los manifiestos de herramientas
  del laboratorio. GitHub puede usar otra versión de Mermaid.
- Verificador editorial: 20 archivos y 16 transcripciones coherentes. Comprobados
  199 enlaces locales; cuerpos de pseudocódigo sin cambios respecto del commit anterior.
- No se modificó la VM, no se regeneró el DVD y no se ejecutaron muestras.

## Alcance de funciones y trabajo pendiente

- Consulta MCP a las 14:50:45 de America/La_Paz (18:50:45 UTC): 176 funciones en
  24d004…, 244 en ed01…, 1.070 en u.wnry y 265 en ec1383…; total 1.755.
  Son funciones reconocidas por el proyecto, no funciones interpretadas exhaustivamente.
- Registro original local: `local/preparacion/alcance-funciones-20261115185045.json`.
- [Guía nueva de alcance y ampliación](../equipo/ALCANCE-Y-AMPLIACION.md): motivos
  de selección, clases de rutinas, límites de los nombres, tres niveles de trabajo,
  prioridades P1–P4, criterios de cierre y relación metodológica con NIST.
- Añadida plantilla vacía de inventario y enlaces desde guías y cuadernos individuales.
  Se mantienen las 16 transcripciones anteriores, sin cambiar sus cuerpos.
- Verificación editorial: 15 archivos y 16 transcripciones coherentes; 135 enlaces
  locales comprobados y plantilla de inventario vacía de 17 columnas. Los cuerpos
  de pseudocódigo se cotejaron con el commit anterior sin diferencias.
- No se declara completado el inventario fila por fila, la clasificación de todas
  las funciones ni el análisis de todos los caminos. La documentación de una tarea
  pendiente no constituye su ejecución. No se cambió el laboratorio.


## Edición de lectura para los cuatro participantes

- Publicadas guías individuales y 16 transcripciones seleccionadas en
  [equipo/](../equipo/README.md), acompañadas de comentarios, direcciones,
  fragmentos de Listing, fuentes, preguntas y criterios de entrega/revisión.
- Los cuerpos proceden de la exportación MCP preservada de las 17:53 UTC;
  se normalizaron solo espacios finales y líneas vacías exteriores. Las notas
  editoriales están separadas del código. No se corrigieron tipos para compilarlo.
- `equipo/indice.json` registra identidades, direcciones y hashes de cada texto.
  `python3 scripts/verificar_material_equipo.py` comprueba esta edición en un
  clon sin muestras ni Ghidra. No sustituye la comprobación del binario original.
- Validación de la edición: 13 archivos y 16 transcripciones correctos; enlaces
  y anclas resueltos. Comprobador probado en copia sin evidencias: aceptó el
  material íntegro y rechazó un bloque alterado y un archivo ausente.
- Originales MCP/C, muestras, proyecto Ghidra y registros de evidencia siguen
  locales. No se modificó la VM ni se instaló Windows durante esta publicación.
- El DVD de 57 archivos corresponde a la preparación anterior; las nuevas
  carpetas del equipo se consultan desde el repositorio y no se declaran incluidas
  en esa imagen ya generada.

## Estado vigente: materiales y VM preparados, instalación aplazada

Esta sección sustituye los estados de VM ausente y descargas pendientes de las
revisiones anteriores conservadas abajo. No acredita Windows instalado.

- Descargados los seis paquetes Windows del manifiesto original; sus hashes y
  los cinco PDFs originales coinciden: **11/11**. SP 800-86 conserva su manifiesto
  complementario. No se modificaron los locks originales ni los PDFs anteriores.
- Volatility 3 descargado con el commit fijado; no validado dentro del invitado.
- DVD `local/herramientas.iso`: 57 archivos de herramientas, seis PDFs, guías,
  configuración y lecturas de Ghidra, más `INVENTARIO.json`. Sin muestras ejecutables.
  Manifiesto local y hash del DVD conservados en `local/preparacion/` y junto a la ISO.
- Exportación nueva por MCP de **16 funciones**, identificando cuatro programas por
  SHA-256, en `local/exportaciones-ghidra/20261115T175358527847Z/`.
  Incluye respuestas originales, pseudocódigo y hashes; no es código fuente original.
- Base vacía y box `nhs/windows10-installer` creadas. VM `forense-nhs-win10` creada
  mediante `./lab up --no-provision`, sin ISO Windows; se comprobó el arranque del
  hardware vacío y se apagó. El mensaje de Vagrant «ready» no implica Windows instalado.
- VM final **apagada**, 2 CPU, 4096 MiB, disco vacío de 64 GiB, DVD de herramientas
  en SATA 2; SATA 1 sin medio. La ISO Windows permanece sin configurar a petición
  del usuario. No se inició el instalador.
- Registro VirtualBox propio en `local/virtualbox/`, IPC exclusivo y discos bajo
  `local/vms/`. Las comparticiones globales del perfil habitual impedían el primer
  control; se solucionó separando el registro y el servidor IPC. Las otras tres VMs
  y sus comparticiones se conservaron. Usar `./scripts/vbox-lab.sh --gui`.
- **18/18 pruebas correctas**, `./lab validate` correcto y comprobación real del
  aislamiento aprobada: ocho NIC none, sin comparticiones, clipboard, drag/drop,
  USB ni VRDE. El comunicador none sigue siendo experimental.
- Verificador NIST: **49 archivos y 20 filas**, sin equivalencia a certificación.
- Logs y configuración real conservados localmente en `local/preparacion/`.
  Las evidencias, muestras, discos y claves quedan fuera de Git; la captura anterior
  se retiró del árbol versionado y se preservó localmente, sin reescribir el historial.

Pendiente: instalación de Windows, comprobación de herramientas en el invitado,
capturas forenses y prácticas del equipo. No se ejecutó WannaCry.
Guía de uso: [materiales preparados](materiales-preparados.md).


## Revisión NIST para la tarea

- Informe corregido, [guía de comprobación](guia-comprobacion-nist.md) y matriz
  de 20 filas con fuente, criterio, estado histórico, estado local y limitación.
- SP 800-86 añadida como guía del método forense; manifiesto complementario
  `config/fuentes-forense.lock.json`. Se preservó `config/descargas.lock.json`.
- `python3 scripts/verificar_caso_nist.py`: 49 archivos cotejados y códigos de
  las 20 filas encontrados en CSF 2.0. Son comprobaciones técnicas, no certificación.
- Se repitió por MCP la decompilación de `00408140`; respuesta conservada en
  `local/revision-nist/prueba-A-killswitch.json`.
- Las cinco plantillas CSV quedaron vacías de resultados. Los registros previos
  no acreditados se preservaron en `local/revision-nist/antecedentes/`.
- La suite actual tiene **16 pruebas correctas**. Se eliminaron requisitos de
  cantidades mínimas de supuestas evidencias; ahora se comprueba que las plantillas
  versionadas estén vacías y que el verificador rechace alteraciones y ausencias.
- El script heredado de HTML ahora informa que **no genera ni sincroniza** el
  dashboard. Su mensaje anterior de sincronización no estaba respaldado por código.
- Informe y matriz están reconciliados; presentación, guion, preguntas y dashboard
  siguen pendientes de adaptación. No se agregó una práctica de ejecución de malware.

Esta revisión documental precedió la preparación del laboratorio descrita al
inicio. En ese momento la VM estaba ausente; no hubo adquisición forense.

## Rectificación: comprobación en este anfitrión mediante Ghidra MCP

Esta sección prevalece sobre el inventario previo conservado más abajo.
La comprobación actual no respalda sus afirmaciones de instalación de Windows,
capturas, snapshots, integridad de descargas ausentes o aislamiento de una VM
activa. No se deben presentar esos registros anteriores como evidencia actual.

- Proyecto nuevo `local/ghidra/proyectos/WannaCry_NHS.gpr`, abierto por
  PyGhidra-MCP con siete programas importados y autoanalizados.
- Nueve funciones anotadas en español; consultas, decompilaciones, navegación
  y guardado comprobados mediante MCP local en `127.0.0.1:8765`.
- Tres hashes originales verificados; 40 derivados estáticos trazados en
  `local/ghidra/extraidos/manifiesto.json`. Sin ejecución de las muestras.
- Corrección: **24d004… contiene el kill switch y R/1831; ed01… es ese recurso
  y contiene XIA/2058**. El análisis anterior intercambiaba ambos papeles.
- Ghidra anfitrión **12.2 DEV**, Java 27 preexistente; versiones y procedencia
  del puente documentadas en `config/ghidra-mcp-host.lock.json`.
  No se modificaron el manifiesto anterior ni los PDFs originales.
- `python3 -m unittest discover -s tests -v`: **15/15 correctas**.
- `./lab validate`: **correcto**, con aviso experimental de none_communicator.
- `python3 scripts/check_isolation.py`: **no aprobado**; VirtualBox informa
  que no está registrada la VM `forense-nhs-win10` en este anfitrión.
- Muestras, derivados y proyecto excluidos de Git. Sin cambios de redes ni
  comparticiones de VirtualBox.

Guía vigente: [ghidra-mcp.md](ghidra-mcp.md).
Conclusiones vigentes: [analisis-ghidra-codigo.md](analisis-ghidra-codigo.md).
Informe, diapositivas, guion, dashboard y CSV anteriores quedan pendientes
de reconciliación; su mera existencia o validación sintáctica no acredita los
hechos que describen. La criptografía completa de t.wnry y el análisis dinámico
no se declaran completados.

## Inventario previo (conservar como antecedente, no como comprobación actual)

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
