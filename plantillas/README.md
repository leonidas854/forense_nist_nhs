# Plantillas vacías para registros reales

Las cinco plantillas CSV mantienen únicamente sus encabezados. Copiarlas a una
carpeta bajo `local/` o `evidencias/` antes de rellenarlas; ambas están excluidas
de Git. No introducir datos reales en estas plantillas versionadas.

La revisión del 15/11/2026 retiró filas que afirmaban adquisiciones de RAM,
EVTX, traspasos y timestamps no respaldados por artefactos presentes. Se
preservaron los antecedentes en `local/revision-nist/antecedentes/plantillas/`.
No se consideran una cadena de custodia válida ni resultados de laboratorio.

No inventar registros para alcanzar un número mínimo. Un campo desconocido
debe quedar expresamente indicado. En la timeline, una fecha documental sin
hora no se convierte en un timestamp UTC ficticio. Mantener la precisión y
zona de la fuente; un campo UTC puede quedar vacío cuando no se pueda convertir.

Consultar [la guía de comprobación](../docs/guia-comprobacion-nist.md) y
[la matriz de evaluación](../docs/matriz-nist.csv). La matriz sí contiene
análisis académico; los originales, registros y resultados completos son locales.
