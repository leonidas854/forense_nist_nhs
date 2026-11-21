# Entrega académica: WannaCry y NHS

Edición del 20 de noviembre de 2026. Autoría colectiva de los ocho autores del
informe aportado. Los capítulos se organizan por componente, sin reparto nominal
de tareas ni atribución de análisis individuales no acreditados.

## Documentos para estudiar y entregar

- [Informe general en PDF](INFORME_GENERAL_NIST_NHS.pdf): problema, método,
  reconstrucción histórica, resultados, valoración NIST y conclusiones.
- [Parte práctica en PDF](PARTE_PRACTICA_NIST_GHIDRA.pdf): laboratorio, lectura
  por capas, cuatro análisis, diagramas, 16 transcripciones y ejercicios.
- [Informe general editable](INFORME_GENERAL_NIST_NHS.docx).
- [Parte práctica editable](PARTE_PRACTICA_NIST_GHIDRA.docx).

Fuentes editables: [informe general](informe_general.md),
[parte práctica](parte_practica.md) y [análisis por componente](analisis/).
Los cuatro análisis se integran completos en la parte práctica; sus archivos
individuales permiten estudiar cada mecanismo por separado.

## Alcance de la entrega

Investigación documental del NHS de Inglaterra y análisis estático de componentes
locales. NIST SP 800-86 organiza recolección, examen, análisis e informe.
CSF 2.0 se aplica retrospectivamente; no se declara certificación ni auditoría
completa del NHS. El documento es final para ese alcance, con límites explícitos:
no hay ejecución de WannaCry, adquisición forense hospitalaria
ni interpretación exhaustiva de las 1.755 funciones reconocidas.

Se incorporó una copia aislada del Windows 10 existente del usuario y se comprobó
su escritorio y versión. Las herramientas y ejercicios dentro del invitado aún
requieren comprobación; véase [estado del laboratorio](estado_laboratorio.md).

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
