# Fuentes conservadas

Descargadas de los organismos emisores. El manifiesto
[`config/descargas.lock.json`](../config/descargas.lock.json) registra URL inicial,
URL final, fecha, tamaño, SHA-256 y páginas. Se comprobó que eran PDF legibles,
no respuestas HTML; la extracción de texto queda local en `fuentes/texto/`.

| Archivo | Edición y función |
|---|---|
| [NIST.CSWP.29.pdf](NIST.CSWP.29.pdf) | CSF 2.0, 26-02-2024; resultados y categorías |
| [NIST.IR.8374r1.pdf](NIST.IR.8374r1.pdf) | Revisión 1 final, junio de 2026; perfil de ransomware |
| [NIST.SP.800-61r3.pdf](NIST.SP.800-61r3.pdf) | Revisión 3 final, abril de 2025; respuesta a incidentes |
| [NIST.SP.800-86.pdf](NIST.SP.800-86.pdf) | Agosto de 2006; sección 3: recolección, examen, análisis e informe |
| [NAO-WannaCry-NHS.pdf](NAO-WannaCry-NHS.pdf) | HC 414, PDF revisado con portada del 25-04-2018, 35 páginas |
| [NHS-lessons-learned-2018.pdf](NHS-lessons-learned-2018.pdf) | William Smart / DHSC / NHS, febrero de 2018; 42 páginas |

El PDF NAO conserva metadatos internos con la palabra `Summary`, pero el archivo
descargado tiene 35 páginas, apartados y apéndices: no es el resumen breve enlazado
por separado en la web. Se conserva intacto, con su hash y la fecha de su portada.

La conversación de Gemini se conserva solo localmente en
`fuentes/contexto/conversacion-gemini.txt`, excluida de Git. No es bibliografía
ni evidencia del ataque. Las herramientas y PDFs mantienen sus condiciones de uso.

## Referencias de partida

La fuente SP 800-86 se añadió el 15/11/2026. Su URL, tamaño y SHA-256 están en
[`config/fuentes-forense.lock.json`](../config/fuentes-forense.lock.json),
sin modificar el manifiesto anterior ni reemplazar PDFs originales.

- Kent, K., Chevalier, S., Grance, T., & Dang, H. (2006). *Guide to integrating
  forensic techniques into incident response* (NIST SP 800-86).
  https://doi.org/10.6028/NIST.SP.800-86

- National Institute of Standards and Technology. (2024). *The NIST Cybersecurity
  Framework (CSF) 2.0* (NIST CSWP 29). https://doi.org/10.6028/NIST.CSWP.29
- Souppaya, M., Barker, W. C., Fisher, W., & Kent, K. (2026). *Ransomware Risk
  Management: A Cybersecurity Framework 2.0 Community Profile* (NIST IR 8374 Rev. 1).
  https://doi.org/10.6028/NIST.IR.8374r1
- Nelson, A., Rekhi, S., Souppaya, M., & Scarfone, K. (2025). *Incident Response
  Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0
  Community Profile* (NIST SP 800-61 Rev. 3). https://doi.org/10.6028/NIST.SP.800-61r3
- National Audit Office. (2018). *Investigation: WannaCry cyber attack and the NHS*
  (HC 414; edición revisada del informe publicado inicialmente en 2017).
  [Página institucional](https://www.nao.org.uk/reports/investigation-wannacry-cyber-attack-and-the-nhs/).
- Smart, W. (2018). *Lessons learned review of the WannaCry Ransomware Cyber Attack*.
  Department of Health and Social Care / NHS England / NHS Improvement.
  [PDF institucional](https://www.england.nhs.uk/aac/wp-content/uploads/2018/02/lessons-learned-review-wannacry-ransomware-cyber-attack-cio-review.pdf).

Estas referencias identifican las ediciones conservadas. El formato final se
adaptará a la norma que indique el docente.
