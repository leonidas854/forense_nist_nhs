# Entrega académica: WannaCry y NHS

Edición del 21 de noviembre de 2026. Autoría colectiva de los ocho autores del
informe aportado. Los capítulos se organizan por componente, sin reparto nominal
de tareas ni atribución de análisis individuales no acreditados.

## Documentos para estudiar y entregar

- [Informe general en PDF](INFORME_GENERAL_NIST_NHS.pdf): problema, método,
  qué es WannaCry como familia, ransomware y gusano; reconstrucción histórica,
  resultados, valoración NIST y conclusiones.
- [Parte práctica en PDF](PARTE_PRACTICA_NIST_GHIDRA.pdf): laboratorio, lectura
  por capas OSI, cuatro análisis, recursos, catálogo de 16 funciones,
  revisión offline con Wireshark de una captura externa coincidente por hash,
  diagramas, transcripciones, ejercicios y defensa oral.
- [Informe general editable](INFORME_GENERAL_NIST_NHS.docx).
- [Parte práctica editable](PARTE_PRACTICA_NIST_GHIDRA.docx).

Fuentes editables: [informe general](informe_general.md),
[parte práctica](parte_practica.md) y [análisis por componente](analisis/).
Los cuatro análisis se integran completos en la parte práctica; sus archivos
individuales permiten estudiar cada mecanismo por separado.

Ruta de estudio de esta revisión:

1. [OSI, operaciones locales y recursos](enfoque_osi.md): sección 4 del PDF.
2. Capítulos 6–9: Listing, decompilado y razonamiento de cada componente.
3. [Catálogo de las 16 funciones](catalogo_funciones.md): sección 10, entradas,
   condiciones, objetos utilizados, continuación y evidencia faltante.
4. [Guion y preguntas para la exposición](guion_exposicion_osi.md): sección 13,
   ensayo de 20 minutos y respuestas justificadas.

La captura externa es de un laboratorio de terceros, no del NHS ni de esta VM.
Además, se hizo un intento de abrir la muestra en un clon enlazado aislado;
Windows lo rechazó con un mensaje de virus/software potencialmente no deseado.
No se recuperó un evento que identifique el motor o la firma. No se desactivó la
protección, no hubo detonación y no se observó impacto local. La captura y las
imágenes permanecen fuera de Git; el [suplemento](ejecucion_controlada_bloqueada.md)
registra el resultado y sus límites.

Los BPMN de los capítulos 6–9 se presentan en páginas apaisadas, con piscinas y
carriles para separar decisiones del código, llamadas de Windows y comprobaciones
forenses. Las rutas largas se dividen en etapas y se explican junto a cada figura;
se especifican condiciones, resultado de cada rama y qué evidencia externa haría
falta para confirmar el efecto. La edición práctica actual tiene 105 páginas.

La revisión amplía la explicación del material conservado; no añade una sesión
Ghidra ni una detonación efectiva de WannaCry. El original aportado continúa intacto.

## Alcance de la entrega

Investigación documental del NHS de Inglaterra y análisis estático de componentes
locales. NIST SP 800-86 organiza recolección, examen, análisis e informe.
CSF 2.0 se aplica retrospectivamente; no se declara certificación ni auditoría
completa del NHS. El documento es final para ese alcance, con límites explícitos:
no hay ejecución efectiva de WannaCry, adquisición forense hospitalaria
ni interpretación exhaustiva de las 1.755 funciones reconocidas.

Se incorporó una copia aislada del Windows 10 existente del usuario y se comprobó
su escritorio y versión. Se completó una práctica benigna de integridad, restauración y proceso; las
herramientas descargadas todavía requieren validación dentro del invitado; véase [estado del laboratorio](estado_laboratorio.md).

El PDF y DOCX aportados en la raíz se preservan sin cambios. Su revisión y los
criterios de incorporación están en [revisión del antecedente](revision_antecedente.md).
Los binarios, proyectos Ghidra y registros originales permanecen fuera de Git.
Los decompilados son transcripciones didácticas, no código fuente compilable.

## Reproducibilidad

Desde la raíz del repositorio:

```bash
python3 scripts/generar_entrega_nist.py
python3 scripts/verificar_entrega_nist.py
python3 scripts/verificar_material_equipo.py
python3 scripts/verificar_caso_nist.py
```

El generador usa Python 3, ReportLab, python-docx, Markdown, BeautifulSoup,
svglib, las fuentes DejaVu y Graphviz (`dot`). Las versiones utilizadas se
registran en `construccion.json`. No descarga paquetes ni abre las muestras.
Las figuras son vectoriales, en blanco y negro, con texto explicativo contiguo.
El contraste negro/blanco es 21:1; los estados se distinguen por palabras y formas.
Los documentos impresos tienen una única presentación; no se afirma accesibilidad
PDF/UA ni una auditoría de lectores de pantalla.

`SHA256SUMS` identifica los archivos de esta edición. Una modificación editorial
requiere regenerar documentos y manifiesto; no se alteran los locks de descargas
ni las fuentes originales. [Trazabilidad](trazabilidad.json) distingue hashes de
entrada, fuentes, transcripciones y resultados editoriales.

La [práctica ejecutada en Windows](practica_windows_realizada.md) documenta
resultados observados con datos ficticios, sin ejecutar WannaCry. El script
reproducible está en [scripts/windows/prueba_benigna.ps1](../scripts/windows/prueba_benigna.ps1).
