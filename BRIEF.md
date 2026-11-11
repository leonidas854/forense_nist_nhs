---
trabajo: forense_nist_nhs
titulo: 'WannaCry en el NHS: laboratorio forense con NIST CSF 2.0'
materia: Informática Forense
idioma: es
docente: null
entrega: null
entregables:
  - archivo: README.md
    tipo: md
  - archivo: docs/laboratorio.md
    tipo: md
fuentes:
  web_permitida: true
  citas: obligatorias
  estilo_cita: APA
  obligatorias: [fuentes/NIST.CSWP.29.pdf, fuentes/NIST.IR.8374r1.pdf, fuentes/NHS-lessons-learned-2018.pdf]
imagenes:
  usar: false
prohibido:
  - inventar resultados de laboratorio o atribuir evidencias propias al NHS
  - subir claves, contraseñas, discos virtuales o muestras de malware a GitHub
terminado:
  - repositorio privado creado en leonidas854 y cambios publicados
  - fuentes oficiales descargadas con URL y SHA-256
  - configuración Vagrant y VirtualBox preparada para Windows 10
  - herramientas de análisis descargadas o impedimentos concretos registrados
  - guía de inicio y plantillas de evidencias disponibles
  - validaciones realizadas y límites pendientes documentados
---

# Qué me están pidiendo

«realizar en mi github privado de leonidas un repositorio privado y descarga todo par poder trabajar mi idea es sobre vagrant trabajar, en virtualbox, este caso de estudio es para la materia de forense».

# Qué quiero que salga

Repositorio de trabajo y laboratorio inicial para estudiar WannaCry en el NHS,
aplicar retrospectivamente NIST CSF 2.0 y documentar análisis estático con Ghidra
y evidencias forenses de Windows. Esta fase prepara el proyecto; no es el informe
académico final ni acredita una ejecución de WannaCry.

# Contexto y decisiones

- 2026-11-11: usuario confirma Windows 10 e ISO y licencia propias.
- Cuenta autenticada: leonidas854; repositorio: forense_nist_nhs.
- Material pegado de Gemini: contexto de trabajo, no fuente verificable.
- Laboratorio inicialmente sin red, carpetas compartidas, portapapeles ni arrastrar/soltar.
- Fuentes públicas y herramientas oficiales se descargan. Binarios grandes quedan
  locales con manifiesto; documentos y configuración se versionan.
- Esta preparación no incluye detonación automática ni atribuye una muestra moderna al NHS.

# Pendientes académicos

Enunciado literal del docente, rúbrica, fecha, extensión y formato del informe.
No bloquean la preparación del repositorio solicitada.
