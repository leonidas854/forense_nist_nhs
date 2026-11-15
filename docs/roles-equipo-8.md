# Estructura del Equipo de Peritaje Forense (8 Integrantes)
## Caso WannaCry en el NHS con NIST CSF 2.0 · Modalidad de 2 Expositores

Este documento formaliza la organización técnica, la asignación de responsabilidades y la justificación metodológica de la división de trabajo para el equipo de **8 estudiantes** en la materia de Informática Forense.

---

## 1. Justificación de la Modalidad de Defensa (2 Expositores)

De acuerdo a las pautas de presentación académica y gestión de tiempo (bloques de 20 a 30 minutos), el equipo designa a **dos expositores principales** para defender el trabajo ante el tribunal docente, respaldados integralmente por los seis investigadores restantes:

- **Expositor 1 (Enfoque Estratégico, Prevención y Contexto):** Expone la introducción institucional, la cadena de custodia pericial, los hechos históricos certificados del NHS (NAO 2018), el vector de entrada y las tres primeras funciones de NIST CSF 2.0 (**Govern**, **Identify**, **Protect**).
- **Expositor 2 (Enfoque Técnico, Ingeniería Inversa y Respuesta):** Expone la arquitectura de laboratorio aislado, la ingeniería inversa estática en Ghidra 12.2 (Kill Switch y dropper), la evidencia en logs/memoria/disco y las tres funciones restantes de NIST CSF 2.0 (**Detect**, **Respond**, **Recover**), culminando con lecciones aprendidas.
- **Equipo de Soporte y Tribunal (Integrantes 3 al 8):** Cada uno es especialista temático en su área técnica y participa activamente en la ronda de preguntas y respuestas difíciles ante el tribunal docente.

---

## 2. Asignación de Roles Técnicos Individuales

| Nº | Rol Pericial | Nombre (Estudiante) | Función Principal | Especialidad en NIST CSF 2.0 | Rol en Exposición |
|---|---|---|---|---|---|
| **1** | **Perito Coordinador & Custodio Líder** | *Estudiante 1 (Por asignar)* | Gestión del caso, aseguramiento de cadena de custodia, marco legal y gobernanza general. | **GOVERN (GV)**: Políticas de parches, roles de autoridad y cumplimiento. | **Expositor 1** (Apertura y Gobernanza) |
| **2** | **Auditor de Infraestructura & Activos** | *Estudiante 2 (Por asignar)* | Mapeo de topología hospitalaria, dispositivos clínicos embebidos (XP/7) e inventario del NHS. | **IDENTIFY (ID)**: Gestión de activos físicos/software y superficie de ataque. | Especialista en preguntas de infraestructura |
| **3** | **Especialista en Protección & Redes** | *Estudiante 3 (Por asignar)* | Análisis del protocolo SMBv1, arquitectura de red N3, mitigación MS17-010 y segmentación. | **PROTECT (PR)**: Mantenimiento de software según riesgo y control de acceso. | Especialista en preguntas de parches y SMB |
| **4** | **Analista de Monitorización & Logs** | *Estudiante 4 (Por asignar)* | Auditoría de Event Logs de Windows (`System.evtx`, `Security.evtx`) y diseño de reglas Sysmon. | **DETECT (DE)**: Detección de creación de servicios (7045) y procesos (4688). | Especialista en preguntas de logs y eventos |
| **5** | **Ingeniero Inverso de Malware** | *Estudiante 5 (Por asignar)* | Decompilación en Ghidra 12.2, análisis del Kill Switch (`InternetOpenUrlA`), dropper PE y strings. | **RESPOND (RS.AN-03)**: Análisis de causa raíz y lógica de ejecución del malware. | **Expositor 2** (Técnica y Respuesta) |
| **6** | **Analista Forense de Memoria Volátil** | *Estudiante 6 (Por asignar)* | Triage de RAM con Volatility 3, WinPmem RC2, análisis de procesos inyectados (`tasksche.exe`). | **RESPOND (RS.AN / RS.MI)**: Contención de incidente y preservación de artefactos volátiles. | Especialista en preguntas de RAM y Volatility |
| **7** | **Analista de Sistema de Archivos & Disco** | *Estudiante 7 (Por asignar)* | Análisis de tabla `$MFT`, entropía de cifrado `.WNCRY`, y detección del sabotaje `vssadmin`. | **RESPOND (RS.AN-06 / RS.AN-07)**: Integridad de datos, notas de rescate y antiforense. | Especialista en preguntas de MFT y copias sombra |
| **8** | **Auditor de Recuperación & Lecciones** | *Estudiante 8 (Por asignar)* | Evaluación de planes de contingencia, costos (£92M), lecciones aprendidas (NHS 2018) y recomendaciones. | **RECOVER (RC)**: Validación de respaldos (RC.RP) y restauración de servicios críticos. | Especialista en preguntas de recuperación e impacto |

---

## 3. Matriz de Responsabilidades RACI

> **Convención RACI:**
> - **R (Responsible):** Quien realiza directamente la tarea técnica o redacta el contenido.
> - **A (Accountable):** Quien aprueba y responde por la calidad y rigor pericial del entregable.
> - **C (Consulted):** Quien aporta información técnica o retroalimentación especializada.
> - **I (Informed):** Quien debe estar al tanto del avance y resultados.

| Tarea / Entregable | Integrante 1 (Coord/GV) | Integrante 2 (Infra/ID) | Integrante 3 (Red/PR) | Integrante 4 (Logs/DE) | Integrante 5 (Ghidra/RS) | Integrante 6 (RAM/RS) | Integrante 7 (Disco/RS) | Integrante 8 (Recov/RC) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1. Definición de Alcance y Cadena Custodia** | **A / R** | C | C | I | C | C | C | I |
| **2. Fuentes Oficiales (NAO y NHS 2018)** | C | **R** | C | I | I | I | I | **A / R** |
| **3. Configuración y Aislamiento de Laboratorio (Vagrant)** | **A** | C | **R** | C | **R** | C | C | I |
| **4. Análisis Estático en Ghidra (Kill Switch / Dropper)** | I | I | C | C | **A / R** | C | C | I |
| **5. Adquisición y Triage de Memoria (Volatility 3 / WinPmem)** | I | I | I | C | C | **A / R** | C | I |
| **6. Auditoría de Logs (.evtx) y Reglas Sysmon** | I | I | C | **A / R** | C | I | C | I |
| **7. Análisis de Sistema de Archivos ($MFT y vssadmin)** | I | I | I | C | C | C | **A / R** | C |
| **8. Mapeo Integral NIST CSF 2.0 y NIST IR 8374r1** | **A / R** | **R** | **R** | **R** | **R** | **R** | **R** | **A / R** |
| **9. Redacción del Informe Forense Maestro** | **A / R** | **R** | **R** | **R** | **R** | **R** | **R** | **A / R** |
| **10. Preparación de Diapositivas Proyectables** | **A / R** | C | C | C | **A / R** | C | C | C |
| **11. Ensayos del Guion de Defensa Oral (2 Oradores)** | **A / R** | I | I | I | **A / R** | I | I | I |
| **12. Simulacro de Preguntas Difíciles del Tribunal** | C | **R** | **R** | **R** | C | **R** | **R** | **R** |

---

## 4. Desglose Operativo para la Defensa Oral

### Bloque 1: Expositor 1 (Minutos 0:00 a 12:00)
- **Min 0:00 - 2:30:** Carátula institucional, presentación del equipo de 8 peritos, delimitación del caso de estudio (12 de mayo de 2017) y principios de cadena de custodia.
- **Min 2:30 - 5:30:** Realidad histórica del NHS según auditoría oficial de la NAO (80 trusts de 236 afectados, 6.912 citas canceladas identificadas vs >19.000 estimadas, costo de £92M) y corrección de mitos comunes (no fue phishing, reclasificación de 81 a 80 trusts).
- **Min 5:30 - 8:30:** Topología hospitalaria, red N3/HSCN sin segmentar, dispositivos médicos legados con Windows XP/7 y fallo en la función **Identify (ID.AM-01, ID.RA-01)**.
- **Min 8:30 - 12:00:** Autopsia del vector de propagación: el puerto 445 (SMBv1), vulnerabilidad MS17-010 (EternalBlue), alertas ignoradas de CareCERT y fallo en la función **Govern (GV.OV-01, GV.RR-02)** y **Protect (PR.PS-02, PR.IR-01)**. Transición al Expositor 2.

### Bloque 2: Expositor 2 (Minutos 12:00 a 24:00)
- **Min 12:00 - 14:00:** Arquitectura del laboratorio forense aislado en Linux con Vagrant 2.4.9 y VirtualBox 7.2 (8 adaptadores de red desconectados, verificación por script `check_isolation.py`).
- **Min 14:00 - 17:30:** **Ingeniería Inversa Estática en Ghidra 12.2 (RS.AN-03):** Decompilación de la función `WinMain`, llamada a `InternetOpenUrlA` al Kill Switch, registro del servicio `mssecsvc2.0`, extracción del recurso oculto `.rsrc/R` (`tasksche.exe`) y explicación forense de por qué los hospitales con proxy se infectaron pese al Kill Switch activo.
- **Min 17:30 - 20:30:** **Correlación de Artefactos Forenses de Windows:**
  - *Detección (DE.CM-01, DE.AE-03):* Evento `System.evtx` ID 7045 (instalación de servicio), `Security.evtx` ID 4688 / Sysmon ID 1 (ejecución de procesos).
  - *Memoria Volátil (RS.AN):* Análisis con Volatility 3 de inyección de procesos y extracción con WinPmem.
  - *Sistema de Archivos y Antiforense (RS.AN-06):* Sabotaje con `vssadmin delete shadows /all /quiet`, tabla `$MFT` y cifrado masivo `.WNCRY`.
- **Min 20:30 - 24:00:** Mapeo de la función **Recover (RC.RP, RC.CO)**, balance de lecciones aprendidas oficiales del informe Smart (DHSC 2018), conclusiones periciales y cierre formal de la exposición.

### Bloque 3: Ronda de Preguntas del Tribunal (Minutos 24:00 a 30:00)
- Los Expositores 1 y 2 lideran la respuesta apoyados por los especialistas técnicos (Integrantes 3 al 8) según el área de la pregunta:
  - *Pregunta sobre parches/red:* Responde Integrante 3.
  - *Pregunta sobre logs/Sysmon:* Responde Integrante 4.
  - *Pregunta sobre memoria RAM/Volatility:* Responde Integrante 6.
  - *Pregunta sobre MFT/vssadmin:* Responde Integrante 7.
  - *Pregunta sobre costos/lecciones:* Responde Integrante 8.

---

## 5. Bitácora de Registro de Trabajo del Equipo

Esta bitácora respalda ante la cátedra la participación de cada uno de los 8 peritos en la construcción del proyecto:

| Fecha | Integrante(s) | Módulo / Componente | Descripción de la Actividad Realizada | Evidencia Generada |
|---|---|---|---|---|
| **2026-11-11** | Int. 1 y Int. 2 | Gestión y Fuentes | Descarga y verificación SHA-256 de informes oficiales NAO, NHS y NIST (CSWP 29, IR 8374r1, SP 800-61r3). | `config/descargas.lock.json`, `fuentes/` |
| **2026-11-11** | Int. 1 y Int. 3 | Laboratorio Base | Configuración de Vagrantfile con comunicador `none`, validación de 8 NIC deshabilitadas y scripts de test. | `lab`, `scripts/check_isolation.py`, `tests/` |
| **2026-11-12** | Int. 4 y Int. 6 | Herramientas Forenses | Descarga y empaquetado en ISO de Ghidra 12.2, JDK 25, Volatility 3, WinPmem RC2 y Sysinternals. | `local/herramientas.iso`, `descargas/` |
| **2026-11-13** | Int. 5 y Int. 7 | Metodología Técnica | Definición de pasos para decompilación en Ghidra, extracción de recurso PE y auditoría de eventos de Windows. | `docs/metodologia.md`, plantillas CSV |
| **2026-11-14** | Int. 1 y Int. 8 | Mapeo NIST | Mapeo retrospectivo de fallos del NHS a las 6 funciones de CSF 2.0 y lecciones aprendidas. | `docs/matriz-nist.csv`, `docs/caso-nhs.md` |
| **2026-11-15** | Todo el Equipo | Entrega y Exposición | Redacción del informe forense integral, diapositivas de defensa oral, guion de 2 expositores y banco de preguntas. | `docs/informe-forense.md`, `docs/diapositivas.md`, `docs/guion-exposicion.md` |

