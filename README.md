# WannaCry en el NHS · Laboratorio y Peritaje Forense con NIST CSF 2.0

**Entrega vigente, 20/11/2026 — ocho autores, capítulos por componente:**
[informe general PDF](entrega_nist/INFORME_GENERAL_NIST_NHS.pdf) y
[parte práctica PDF](entrega_nist/PARTE_PRACTICA_NIST_GHIDRA.pdf).
La [carpeta de entrega](entrega_nist/README.md) incluye Word editables, fuentes,
cuatro análisis, diagramas y trazabilidad. Sustituye la organización por personas
de los cuadernos anteriores para la presentación final.

**Windows disponible:** se incorporó una [copia aislada del Windows 10 existente](docs/windows10-copia-aislada.md),
con escritorio y versión comprobados. La VM vacía anterior de Vagrant se conserva;
`./lab status` consulta esa VM, no la copia. La instalación y validación de
herramientas en el invitado siguen pendientes.

**Vista general y flujos:** [15 diagramas con análisis de los componentes, el caso
NHS y los límites de evidencia](equipo/DIAGRAMAS-Y-ANALISIS.md).

**Material para cada participante:** empieza en [equipo/README.md](equipo/README.md).
Incluye el reparto, **16 funciones decompiladas para lectura**, notas, fragmentos
de desensamblado, herramientas, ejercicios y entregables por persona. Se puede
leer directamente en GitHub o VS Code, sin instalar Windows ni disponer de muestras.
La [guía de alcance](equipo/ALCANCE-Y-AMPLIACION.md) explica las demás funciones,
los criterios de selección y cómo ampliar el análisis de los cuatro componentes.

**Plan previo para cuatro personas:** [elaboración, análisis, glosario, Windows 10 y exposición](docs/plan-trabajo-equipo-4.md).
Se conserva como antecedente; la entrega vigente mantiene ocho autores y organiza
los cuatro componentes sin etiquetas individuales. Las prácticas previstas son
análisis estático y simulación benigna. La VM original de preparación sigue vacía.
Consulta [materiales descargados y preparación](docs/materiales-preparados.md).

**Para entender el código abierto en Ghidra:** sigue el
[recorrido explicado](docs/recorrido-ghidra-explicado.md), con direcciones,
ejercicios y límites de las conclusiones.
Después continúa con la [guía de capas y comparación de código](docs/guia-capas-decompilado-desensamblado.md).

**Para realizar la tarea con NIST:** empieza por la
[guía de comprobación paso a paso](docs/guia-comprobacion-nist.md), lee el
[informe corregido](docs/informe-forense.md) y revisa las 20 filas de la
[matriz NIST](docs/matriz-nist.csv). SP 800-86 estructura el procedimiento
forense; CSF 2.0 aporta el mapeo retrospectivo. Ejecuta
`python3 scripts/verificar_caso_nist.py` para comprobar integridad y referencias.
Las plantillas están vacías de resultados: completar registros reales fuera de Git.
El dashboard, las diapositivas y el guion anteriores requieren reconciliación;
no utilizarlos como conclusiones verificadas de esta revisión.

**Revisión local del 15/11/2026:** proyecto Ghidra y MCP preparados;
abrir con `./scripts/ghidra-mcp.sh`. Consultar la
[guía de trabajo](docs/ghidra-mcp.md) y el
[análisis estático corregido](docs/analisis-ghidra-codigo.md).
Se corrigió la identificación de las capas 24d004… / ed01…; los entregables
académicos anteriores requieren reconciliación con estos hallazgos.
La VM `forense-nhs-win10` está registrada en el perfil aislado del proyecto:
[estado y límites comprobados](docs/verificacion.md).

Repositorio pericial para el estudio del caso **WannaCry en el National Health Service (NHS)** del Reino Unido (12 de mayo de 2017), desarrollado para la materia de **Informática Forense**. Integra análisis documental oficial (NAO y DHSC 2018), ingeniería inversa estática con Ghidra 12.2, correlación de artefactos de Windows y un mapeo retrospectivo riguroso a **NIST CSF 2.0** (NIST CSWP 29) y su perfil **NIST IR 8374 Rev. 1** (versión final de junio de 2026).

---

## Organización vigente: ocho autores, cuatro componentes

La nueva entrega conserva los ocho nombres del informe aportado y presenta
24d004…, ed01…, u.wnry y ec1383… por componente. La revisión es colectiva,
sin atribuir tareas individuales no acreditadas. Los cuadernos anteriores
conservan su organización y hashes como antecedentes de lectura.

---

## Documentación y Entregables Académicos

| Documento | Descripción y Uso | Enlace |
|---|---|:---:|
| **Informe Forense Maestro** | Informe académico corregido, con fuentes y límites; integración del nuevo plan pendiente. | [docs/informe-forense.md](docs/informe-forense.md) |
| **Plan del equipo de 4** | Reparto vigente, glosario, análisis, VM y exposición. | [docs/plan-trabajo-equipo-4.md](docs/plan-trabajo-equipo-4.md) |
| **Organización anterior de 8** | Antecedente; sustituida para esta etapa por el plan de cuatro. | [docs/roles-equipo-8.md](docs/roles-equipo-8.md) |
| **Guion de Exposición (2 Expositores)** | Diálogo estructurado minuto a minuto (24 min de ponencia + 6 min de preguntas) con transiciones. | [docs/guion-exposicion.md](docs/guion-exposicion.md) |
| **Diapositivas de Defensa Oral** | Presentación completa proyectable (compatible con Marp y Markdown) con diagramas y tablas. | [docs/diapositivas.md](docs/diapositivas.md) |
| **Banco de Preguntas del Tribunal** | 20 preguntas difíciles con respuestas fundamentadas en código, comandos y auditorías oficiales. | [docs/preguntas-defensa.md](docs/preguntas-defensa.md) |
| **Matriz NIST CSF 2.0** | CSV detallado con las 6 funciones mapeadas a fuentes históricas, evidencias y roles. | [docs/matriz-nist.csv](docs/matriz-nist.csv) |
| **Guía del Laboratorio Aislado** | Arquitectura de la VM Windows 10, instalación de herramientas por ISO y snapshots. | [docs/laboratorio.md](docs/laboratorio.md) |
| **Metodología Pericial** | Protocolo de Ghidra, Volatility 3, adquisición de RAM con WinPmem y cadena de custodia. | [docs/metodologia.md](docs/metodologia.md) |
| **Caso Histórico NHS** | Auditoría de cifras certificadas (NAO 2018), desmitificación del phishing y precisión de 80 trusts. | [docs/caso-nhs.md](docs/caso-nhs.md) |
| **Fuentes Oficiales y PDFs** | Seis documentos oficiales primarios, incluida la guía forense NIST SP 800-86. | [fuentes/README.md](fuentes/README.md) |

---

## Estación de Laboratorio Forense Aislada

La VM `forense-nhs-win10` está creada, apagada y comprobada: 2 CPU, 4 GiB RAM,
disco vacío de 64 GiB y DVD de herramientas conectado. **Windows no está
instalado**; la instalación queda aplazada por indicación del usuario.
La box inicial contiene hardware vacío. Para consultar el estado:

```bash
cd /home/leonidas/deveploment/forense_nist_nhs

# Consultar la estación preparada, sin arrancarla
./lab status

# Verificar aislamiento en tiempo real (8 NICs desactivadas, sin carpetas compartidas)
python3 scripts/check_isolation.py
```

* **Política prevista:** 8 adaptadores en modo `none`, comunicador `none_communicator`, portapapeles y Drag & Drop inhabilitados; comprobar el estado real antes de usar la VM.
* **Herramientas del invitado:** requieren comprobación dentro del invitado. El Ghidra utilizado aquí está en el anfitrión; consultar [su instalación comprobada](docs/ghidra-mcp.md).

---

## Verificación Automatizada del Proyecto

Para comprobar la integridad del repositorio, la configuración de Vagrant y el aislamiento:

```bash
# 1. Validar sintaxis del laboratorio y comunicador 'none'
./lab validate

# 2. Ejecutar la suite de pruebas unitarias de aislamiento
python3 -m unittest discover -s tests -v

# 3. Comprobar aislamiento del hipervisor
python3 scripts/check_isolation.py

# 4. Validar integridad criptográfica de descargas y herramientas
sha256sum -c config/SHA256SUMS
```

---

## Base Documental y Normativa

- **NIST CSF 2.0 (2024):** *The NIST Cybersecurity Framework 2.0* (NIST CSWP 29). [DOI oficial](https://doi.org/10.6028/NIST.CSWP.29).
- **NIST IR 8374 Rev. 1 (Final, junio 2026):** *Ransomware Risk Management: A CSF 2.0 Community Profile*. [DOI oficial](https://doi.org/10.6028/NIST.IR.8374r1).
- **National Audit Office (NAO, 2018):** *Investigation: WannaCry cyber attack and the NHS* (Report HC 414).
- **Department of Health and Social Care (DHSC, 2018):** *Lessons learned review of the WannaCry ransomware cyber attack*.
- **NIST SP 800-61 Rev. 3 (2025):** *Incident Response Recommendations and Considerations for Cybersecurity Risk Management*.
