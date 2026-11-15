# Informe académico de informática forense: WannaCry y el NHS

**Revisión:** 15 de noviembre de 2026. **Equipo:** ocho estudiantes; nombres pendientes.
**Alcance:** estudio documental del NHS de Inglaterra y examen estático de muestras locales.
**Estado:** informe sustentado dentro de ese alcance; sin peritaje de equipos originales del NHS.

## 1. Pregunta y conclusión principal

**¿Qué ocurrió en el NHS, qué mecanismos podemos comprobar en las muestras y qué
resultados de NIST ayudan a explicar las deficiencias y proponer verificaciones?**

El 12 de mayo de 2017, WannaCry ocasionó infecciones y también interrupciones
preventivas en organizaciones del NHS. La edición revisada de la NAO diferencia
**80 trusts afectados: 34 infectados y 46 no infectados pero con interrupciones**.
La afectación no equivale siempre a cifrado. La vulnerabilidad de sistemas sin
parchear, la exposición de red y las dificultades de preparación y coordinación
explican el riesgo documentado. No se conoce aquí el primer equipo infectado
ni una cadena completa de eventos por hospital. [NAO, 2018, resumen 4–12,
PDF pp. 8–12](../fuentes/NAO-WannaCry-NHS.pdf).

El laboratorio aporta una comprobación distinta: se verificaron las relaciones
entre recursos PE y la lógica del kill switch en muestras locales mediante Ghidra.
Eso explica comportamiento potencial del malware; no convierte los archivos
locales en evidencia adquirida de los hospitales.

## 2. Qué significa aplicar NIST en esta tarea

| Documento | Uso concreto | Lo que no permite afirmar |
|---|---|---|
| NIST SP 800-86 (2006), sección 3 | Recolección, examen, análisis e informe | Que se realizó una adquisición que no existe |
| NIST CSF 2.0 / CSWP 29 (2024), apéndice A | Relacionar resultados de Govern, Identify, Protect, Detect, Respond y Recover | Una certificación o incumplimiento jurídico retroactivo |
| NIST SP 800-61 Rev. 3 (2025) | Relacionar respuesta a incidentes y gestión del riesgo | Que el NHS utilizaba esa edición en 2017 |
| NIST IR 8374 Rev. 1 (2026) | Priorizar resultados del CSF frente al ransomware | Que toda subcategoría del CSF aparece en el perfil o fue comprobada aquí |

La aplicación de CSF 2.0 y de las revisiones de 2025/2026 es **retrospectiva**.
SP 800-86 aporta una guía técnica de forense desde la perspectiva de TI; no es
una receta exhaustiva ni un certificado de admisibilidad. Se siguen las
[publicaciones conservadas](../fuentes/README.md), sin afirmar aplicación de
ISO/IEC 27037, cuyo texto no fue objeto de esta revisión.

## 3. Fuentes y regla de valoración

Cada afirmación pertenece a una clase:

- **H — histórica:** afirmación atribuida a NAO o NHS/DHSC, con localizador.
- **L — local:** bytes, código o resultados efectivamente examinados en este equipo.
- **I — inferencia:** explicación compatible con H o L que necesita corroboración.
- **P — pendiente:** comprobación que todavía no tiene evidencia suficiente.

Un resultado «documentado» significa que la fuente lo expresa, no que el equipo
lo haya reconstruido con discos o logs del NHS. «No evaluado» no significa
«control ausente». «Parcial» no equivale a un porcentaje de cumplimiento.
La confianza se limita a la proposición: alta para una coincidencia de bytes
comprobada, no necesariamente para la atribución histórica del archivo.

Fuentes principales: PDF NAO revisado, portada de 25/04/2018; revisión de William
Smart de febrero de 2018; publicaciones NIST; tres muestras locales identificadas
por hash y sus derivados. Los PDF se verifican contra manifiestos. La procedencia
previa de las muestras y su fecha de descarga no están acreditadas por los hashes.
No hay imagen de disco, RAM, EVTX ni PCAP adquiridos de un equipo del NHS.

## 4. Reconstrucción de lo ocurrido

| ID | Momento o asunto | Hecho documentado y localizador | Precisión necesaria |
|---|---|---|---|
| H-01 | Antes del ataque | Microsoft publicó el parche el 14/03/2017; NHS Digital difundió avisos. NHS nota 21; NAO §2.5 | Publicar un parche no demuestra que se instaló |
| H-02 | Preparación | No había mecanismo formal para evaluar aplicación local de avisos antes del 12/05. NAO §2.10, PDF p.21 | No implica que ninguna organización tuviera controles |
| H-03 | 12/05/2017 | WannaCry afectó al NHS en un ataque mundial. NAO resumen 1–2, PDF p.6 | El NHS no fue necesariamente el objetivo exclusivo |
| H-04 | Entrada y propagación | NHS §2.3, PDF p.10, considera probable una entrada por SMB vulnerable expuesto; NAO resumen 12, PDF p.12, documenta propagación por internet, incluida N3, y no por NHSmail | Mantener «probable» para la entrada; no inventar host inicial ni ruta exacta |
| H-05 | Equipos | La mayoría de dispositivos infectados identificados usaba Windows 7 soportado pero sin parchear; XP era minoritario. NAO resumen 12 y §2.5 | No atribuir todo el incidente a Windows XP |
| H-06 | Impacto | 80/236 trusts afectados; 34 infectados y 46 con interrupciones. Otras 603 organizaciones de atención primaria y del NHS infectadas, incluidas 595 consultas de medicina general. NAO resumen 5, PDF p.8 | No llamar hospitales a todas estas unidades ni sumar categorías solapadas |
| H-07 | Asistencia | 6.912 citas identificadas como canceladas; estimación de más de 19.000. NAO resumen 6, PDF p.10 | No son dos recuentos observados ni un total exacto |
| H-08 | Tarde/noche del 12/05 | La activación del kill switch limitó el impacto posterior. NHS §2.4; NAO resumen 8 | No descifró por sí mismo los archivos ya afectados |
| H-09 | 13–19/05 | Hubo coordinación EPRR y reinstalación/parcheo de prácticas infectadas. NHS §§2.10–2.16: 95% al 17/05 y resto al 19/05 | Estas cifras tienen ese alcance; no describen recuperación de cada hospital |

La diferencia **81/80** corresponde a ediciones y reclasificaciones: la web de la
NAO conserva 81 y el PDF revisado usa 80. NHS nota 3, PDF p.5, explica la revisión.
No se atribuye sin fuente el cambio a una única causa concreta. Tampoco se suman
los 21 trusts adicionales que contactaron el dominio como infecciones probadas:
la NAO contempla contacto posterior al kill switch o actividad de seguridad.

NHS Digital informó a la NAO que creía que no se habían comprometido o robado
datos de pacientes (resumen 5). Es una declaración de la fuente, no una prueba
forense propia de ausencia absoluta de exfiltración. Esta revisión no cuantifica
costes económicos ni atribución criminal por carecer de análisis específico de
esas afirmaciones dentro del expediente utilizado.

## 5. Procedimiento aplicado al material local

**Recolección/preservación:** se identificaron archivos ya presentes, se
recalcularon hashes y se preservaron originales. El momento de esta comprobación
no se presenta como fecha de adquisición original. Los registros anteriores que
afirmaban capturas o traspasos no demostrados fueron apartados en
`local/revision-nist/antecedentes/`. La custodia antes de esta revisión sigue
pendiente de documentación.

**Examen:** Ghidra 12.2 DEV y PyGhidra-MCP importaron y autoanalizaron siete
programas. Se examinaron cabeceras, recursos, referencias, desensamblado y
pseudocódigo. El extractor recorrió la tabla de recursos y verificó CRC del ZIP;
no ejecutó sus miembros. Se contrastó el kill switch con ensamblado y se
corrigieron tipos de tres APIs WinINet para reducir errores de decompilación.

**Análisis:** se contrastaron hipótesis contra recursos, hashes y ramas del código;
se separó la interpretación estática de la causalidad histórica. El registro
completo permanece bajo `local/ghidra/`, excluido de Git.

**Informe:** se documentaron resultados, limitaciones y comprobaciones pendientes.
La [guía práctica](guia-comprobacion-nist.md) permite repetir la revisión y la
[matriz](matriz-nist.csv) contiene 20 relaciones con criterios de comprobación.

## 6. Hallazgos locales y su alcance

| ID | Observación comprobada | Soporte local | Conclusión admitida / límite |
|---|---|---|---|
| L-01 | SHA-256 coincide con los nombres de los tres originales | Comprobación de archivos y manifiesto | Identidad de bytes; no origen NHS |
| L-02 | R/1831 de 24d004… coincide con ed01… | Tabla PE, offset 204.964, 3.514.368 bytes y hash | Relación contenedor/componente comprobada |
| L-03 | 24d004…, VA 00408140, compara con cero el handle de InternetOpenUrlA; rama cero llama 00408090 | `killswitch-asm.json` y `killswitch-final-decompilado.json` | Lógica de la muestra; no se contactó el dominio ni se probó un proxy hospitalario |
| L-04 | 24d004…, VA 00407c40, crea mssecsvc2.0; VA 00407480 contiene 0x1bd y llamadas de sockets | Proyecto Ghidra y decompilaciones | Candidatos para detección; no evento 7045 ni conexión 445 observados |
| L-05 | ed01… contiene ZIP XIA/2058; u.wnry extraído contiene cadena de sabotaje y referencias | Manifiesto de 40 derivados y `sabotaje-asm.json` | Presencia y referencia al comando; no borrado demostrado |
| L-06 | ec1383…, VA 180001014, escribe W/101 desde recurso+4 con longitud del primer DWORD | Decompilación y PE extraído con SHA-256 93db4b… | No hay descifrado en esa rutina; no acredita por sí solo DoublePulsar ni procedencia Dionaea |

Identificadores completos, direcciones y límites adicionales:
[análisis de Ghidra](analisis-ghidra-codigo.md). El SHA-256 de una muestra y el
hash de una respuesta MCP son controles distintos. Un proyecto mutable de
Ghidra debe guardarse antes de registrar una versión de sus resultados.

## 7. Valoración retrospectiva con NIST CSF 2.0

**Govern:** H-02 sustenta revisar GV.OV-01 y el seguimiento de avisos. La
coordinación documentada motiva GV.RR-02. No se deriva una calificación de todos
los responsables del NHS desde un único incidente.

**Identify:** inventario y vulnerabilidades son preguntas de ID.AM-01 e ID.RA-01.
No se dispone de inventario individual del NHS. El inventario de muestras local
no equivale a inventario de dispositivos clínicos.

**Protect:** H-01/H-05 sustentan PR.PS-02; la exposición documentada y L-04 motivan
PR.IR-01. L-05 hace relevante PR.DS-11, pero no demuestra que todos los respaldos
del NHS fueran cifrados. IR 8374r1 recomienda respaldos protegidos y probados.

**Detect:** DE.CM-01, DE.CM-09 y DE.AE-03 requieren datos de monitorización y
correlación. El código orienta qué buscar; los EVTX/PCAP necesarios no están
presentes. No se declara comprobada una regla de detección.

**Respond:** RS.AN-03 organiza el análisis causal; RS.AN-06 exige trazabilidad de
actuaciones y RS.AN-07 trata los datos/metadatos, integridad y procedencia. Los
hashes comprobados no reparan la procedencia previa desconocida. RS.AN-08 exige
precisión en el alcance; RS.MI-01 corresponde a contención, no a ejecutar Volatility.

**Recover:** RC.RP-03 verifica respaldos antes de usarlos; RC.RP-05 comprueba los
activos y la operación después. RC.CO-03 trata comunicaciones de recuperación;
las lecciones aprendidas se relacionan aquí con ID.IM-03. Una ISO de herramientas
no es una prueba de respaldo o restauración.

La matriz no asigna porcentajes, niveles de madurez ni una certificación: su
cobertura es una selección académica de resultados relevantes, no todo el Core.

## 8. Hipótesis, alternativas y límites

- **I-01:** una salida HTTP restringida podría influir en la rama del kill switch.
  Para atribuirlo a un hospital harían falta versión de muestra, configuración,
  DNS/proxy/firewall y tiempos. No se concluye que explique todos los casos.
- **I-02:** un evento 7045 con el servicio observado sería consistente con la
  instalación, pero se debe correlacionar ruta, hash, host y procesos. El nombre
  solo puede ser imitado; la ausencia del evento también admite retención insuficiente.
- **I-03:** la presencia de comandos contra respaldos indica capacidad de sabotaje;
  su éxito requiere evidencia de ejecución y del estado de las copias.
- **P-01:** VM `forense-nhs-win10` creada, apagada y con aislamiento comprobado
  en la preparación posterior del 15/11/2026. Windows sigue sin instalarse;
  véase `docs/verificacion.md`. El arranque de hardware vacío no acredita un sistema operativo.
- **P-02:** no se hicieron detonación, adquisición de RAM, examen de MFT o
  reconstrucción completa de t.wnry. No son requisitos para afirmar los hallazgos
  estáticos presentes, pero sí limitan el alcance del estudio.

## 9. Conclusión para la defensa

La documentación permite explicar un incidente de ransomware con propagación
automática y consecuencias asistenciales, agravado por exposición técnica y
problemas de preparación. El análisis propio comprueba capas y decisiones del
código, sin reconstruir un hospital real. NIST permite formular qué registrar,
qué examinar y qué resultados de gestión deberían verificarse; no añade evidencia
que no existe. La aportación forense defendible es la relación trazable entre
**pregunta, fuente, procedimiento, observación, interpretación y límite**.

## Referencias

- Kent, K., Chevalier, S., Grance, T., & Dang, H. (2006). *Guide to integrating forensic techniques into incident response* (NIST SP 800-86). https://doi.org/10.6028/NIST.SP.800-86
- National Institute of Standards and Technology. (2024). *The NIST Cybersecurity Framework (CSF) 2.0* (NIST CSWP 29). https://doi.org/10.6028/NIST.CSWP.29
- Nelson, A., Rekhi, S., Souppaya, M., & Scarfone, K. (2025). *Incident response recommendations and considerations for cybersecurity risk management: A CSF 2.0 community profile* (NIST SP 800-61 Rev. 3). https://doi.org/10.6028/NIST.SP.800-61r3
- Souppaya, M., Barker, W. C., Fisher, W., & Kent, K. (2026). *Ransomware risk management: A Cybersecurity Framework 2.0 community profile* (NIST IR 8374 Rev. 1). https://doi.org/10.6028/NIST.IR.8374r1
- National Audit Office. (2018). *Investigation: WannaCry cyber attack and the NHS* (HC 414; PDF revisado con portada de 25 de abril de 2018). [Documento conservado](../fuentes/NAO-WannaCry-NHS.pdf).
- Smart, W. (2018). *Lessons learned review of the WannaCry ransomware cyber attack*. Department of Health and Social Care. [Documento conservado](../fuentes/NHS-lessons-learned-2018.pdf).
