# Caso NHS: base documental y precauciones de interpretación

La reconstrucción con identificadores H-01 a H-09 está en el
[informe corregido](informe-forense.md#4-reconstrucción-de-lo-ocurrido).
El método para comprobar cada afirmación está en la
[guía NIST](guia-comprobacion-nist.md).

## Hechos que sí sustentan las fuentes

El incidente comenzó el **12 de mayo de 2017**. El PDF revisado de la NAO que
se conserva aquí tiene portada del **25 de abril de 2018** y reporta al menos
**80 de 236 trusts** afectados. Su página web todavía muestra **81**.
El informe de lecciones aprendidas explica la reclasificación de 81 a 80 en
su nota 3. No son cifras intercambiables sin mencionar la edición.
[NAO, informe](../fuentes/NAO-WannaCry-NHS.pdf),
[NHS/DHSC, revisión](../fuentes/NHS-lessons-learned-2018.pdf).

La NAO distingue **6.912 citas identificadas como canceladas** de una estimación
de **más de 19.000** cancelaciones totales. Documenta deficiencias en verificación
del cumplimiento de avisos y en ensayos locales de respuesta. Estas son bases
para discutir gobernanza y preparación, no resultados obtenidos en nuestra VM.
[NAO, resumen y apartado 1](../fuentes/NAO-WannaCry-NHS.pdf).

## Correcciones al texto de Gemini

- La edición final de IR 8374 Rev. 1 está confirmada. La ficha y portada muestran
  **Karen Kent** entre los autores; copia los autores de la edición descargada.
  [Ficha oficial](https://csrc.nist.gov/pubs/ir/8374/r1/final).
- No se ha establecido aquí la identidad del primer equipo infectado, una ruta
  única de entrada ni la propagación concreta por N3. Las afirmaciones del texto
  pegado sobre esos puntos requieren evidencia específica antes de citarse.
- NHS §2.3 considera **probable** la entrada inicial por SMB vulnerable expuesto,
  en vez del phishing supuesto inicialmente. NAO resumen 12 documenta propagación
  por internet, incluida N3, y no por NHSmail. Esto no revela cada salto entre hosts.
- La historia del proxy y el dominio de interrupción se mantiene como hipótesis
  a comprobar, no como hallazgo probado en todos los hospitales.
- Una etiqueta de MalwareBazaar, una fecha reciente o el tamaño del fichero no
  demuestran que una muestra sea idéntica a la que afectó al NHS.
- La revisión estática comprobada se realizó en Linux con Ghidra; la VM Windows
  no está registrada en este anfitrión. No se ejecutaron los binarios.
- Ghidra aporta análisis de comportamiento potencial. Un resultado estático no
  demuestra que ese comportamiento haya ocurrido en un equipo concreto.

## Cómo se usará NIST

CSF 2.0 se publicó en 2024: el mapeo del incidente de 2017 es **retrospectivo**.
Es un marco de resultados de gestión de riesgo, no un procedimiento de
adquisición forense ni una certificación de cumplimiento.
[NIST CSWP 29](../fuentes/NIST.CSWP.29.pdf).

La [matriz](matriz-nist.csv) es una propuesta de trabajo. Separa documento
histórico, control propuesto y evidencia que todavía debemos obtener. En
particular, RS.AN-06 se refiere al registro de actuaciones de investigación;
RS.AN-07 cubre datos/metadatos, integridad y procedencia. No conviene etiquetar
automáticamente toda extracción de archivos como RS.AN-06.

## Pregunta inicial

¿Cómo pueden correlacionarse los hallazgos estáticos y los artefactos de un
laboratorio Windows con los fallos y respuestas documentados en el caso NHS,
usando las seis funciones de CSF 2.0 sin confundir evidencia histórica con
evidencia experimental?

El informe responde dentro del alcance documental y estático comprobado. La
rúbrica del docente puede añadir requisitos; cualquier adquisición o práctica
dinámica adicional debe figurar como pendiente hasta disponer de sus resultados.
