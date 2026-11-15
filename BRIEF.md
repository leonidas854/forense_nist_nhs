---
trabajo: forense_nist_nhs
titulo: 'WannaCry en el NHS: laboratorio forense con NIST CSF 2.0'
materia: Informática Forense
idioma: es
modalidad: 'Equipo de 8 estudiantes (Defensa oral: 2 expositores principales)'
docente: null
entrega: null
entregables:
  - archivo: README.md
    tipo: md
  - archivo: docs/laboratorio.md
    tipo: md
  - archivo: docs/informe-forense.md
    tipo: md
  - archivo: docs/roles-equipo-8.md
    tipo: md
  - archivo: docs/guion-exposicion.md
    tipo: md
  - archivo: docs/diapositivas.md
    tipo: md
  - archivo: docs/preguntas-defensa.md
    tipo: md
  - archivo: docs/matriz-nist.csv
    tipo: csv
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
  - repositorio privado creado en leonidas854 y cambios sincronizados (git pull)
  - fuentes oficiales descargadas con URL y SHA-256
  - configuración Vagrant y VirtualBox preparada y aislada para Windows 10
  - herramientas de análisis descargadas y fijadas con manifiesto
  - organización del equipo de 8 peritos y matriz RACI formalizada
  - guion minuto a minuto de defensa oral estructurado para 2 expositores
  - diapositivas proyectables completas en formato Marp / Markdown
  - banco de 20 preguntas difíciles del tribunal evaluador con respuestas sustentadas
  - informe pericial académico maestro completo redactado en estilo APA 7
  - matriz retrospectiva de NIST CSF 2.0 y NIST IR 8374r1 ampliada
  - suite de pruebas de aislamiento y validación de laboratorio superada
---

# Qué me están pidiendo

«realizar en mi github privado de leonidas un repositorio privado y descarga todo par poder trabajar mi idea es sobre vagrant trabajar, en virtualbox, este caso de estudio es para la materia de forense... quiero que tomes en cuenta que es en grupo de 8, ya la mayoria este en este repo es para exponer tambien esto, haz pull a todo el proyecto para seguir trabajando... solo dos expondran este tema, entonces empecemos desde la base que debo escoger para poder avanzar».

# Qué quiero que salga

Repositorio integral de investigación y peritaje forense para el caso de estudio de WannaCry en el National Health Service (NHS), con mapeo retrospectivo a NIST CSF 2.0 y NIST IR 8374 Rev. 1, análisis de código en Ghidra, entorno de laboratorio aislado en Vagrant/VirtualBox, paquete completo para la defensa oral (guion de 2 expositores, diapositivas y banco de preguntas del tribunal) e informe académico maestro respaldado por los 8 integrantes.

# Contexto y decisiones

- 2026-11-11: usuario confirma Windows 10 e ISO y licencia propias.
- Cuenta autenticada: leonidas854; repositorio: forense_nist_nhs.
- Equipo: 8 integrantes; 2 expositores en la defensa oral (Expositor 1: Marco, Caso NHS, GV, ID, PR; Expositor 2: Laboratorio, Ghidra, Memoria, Disco, DE, RS, RC).
- Base de malware elegida: Muestra canónica original de WanaCrypt0r 2.0 (SHA-256 `ed01eb...`, ~3.51 MB) analizada estáticamente en Ghidra 12.2.
- Laboratorio sin red (8 NICs none), carpetas compartidas, portapapeles ni arrastrar/soltar.
- Fuentes públicas y herramientas oficiales descargadas con URL y SHA-256 fijados.
- Preservación estricta de la cadena de custodia y distinción entre datos históricos e hipótesis de laboratorio.

# Pendientes académicos

- Incorporación de nombres y apellidos definitivos de los 8 estudiantes en las carátulas.
- Fecha y horario de la defensa fijados por la cátedra.
