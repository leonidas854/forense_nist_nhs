---
trabajo: forense_nist_nhs
titulo: 'WannaCry en el NHS: laboratorio forense con NIST CSF 2.0'
materia: Informática Forense
idioma: es
modalidad: 'Ocho autores confirmados; cuatro componentes documentados sin etiquetas individuales'
docente: null
entrega: null
entregables:
  - archivo: docs/plan-trabajo-equipo-4.md
    tipo: md
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
  - fuentes oficiales conservadas y hashes comprobados; SP 800-86 añadida con manifiesto complementario
  - proyecto Ghidra MCP con siete programas autoanalizados y conclusiones estáticas delimitadas
  - informe académico corregido con separación de hechos históricos, observaciones e hipótesis
  - guía de comprobación basada en SP 800-86 y matriz retrospectiva de 20 resultados CSF 2.0
  - plantillas vacías; registros anteriores no respaldados preservados localmente como antecedentes
  - verificador de integridad y referencias; no constituye certificación NIST
---

# Qué me están pidiendo

«realizar en mi github privado de leonidas un repositorio privado y descarga todo par poder trabajar mi idea es sobre vagrant trabajar, en virtualbox, este caso de estudio es para la materia de forense... quiero que tomes en cuenta que es en grupo de 8, ya la mayoria este en este repo es para exponer tambien esto, haz pull a todo el proyecto para seguir trabajando... solo dos expondran este tema, entonces empecemos desde la base que debo escoger para poder avanzar».

# Qué quiero que salga

**Actualización de alcance, 20/11/2026:** entrega nueva en `entrega_nist/`, con
informe general y parte práctica PDF/Word. El usuario mantiene los ocho autores
del PDF aportado y solicita quitar el reparto por etiquetas individuales de la
nueva entrega. Autorizó una copia aislada de su VM «Windows 10»: se creó
`forense-nhs-win10-copia`, se comprobó escritorio y winver (Pro 1903, 18362.356)
y se apagó. La original y la VM vacía anterior de Vagrant se conservan.
Se completó después una práctica benigna de integridad, restauración de texto
ficticio y proceso, con PowerShell y Bloc de notas. La validación de paquetes
descargados dentro del invitado sigue pendiente. No se ejecutó WannaCry.
Véase `docs/windows10-copia-aislada.md`. Los párrafos siguientes son antecedentes.

**Actualización de alcance, 15/11/2026:** cuatro personas desarrollarán el análisis
estático de 24d004, ed01, u.wnry y ec1383, contrastado con fuentes históricas y
mapeado retrospectivamente a NIST CSF 2.0. Plan vigente:
`docs/plan-trabajo-equipo-4.md`. Windows 10 será una estación de análisis y
simulación benigna, sin ejecución de WannaCry. La descripción de ocho integrantes
que sigue se conserva como antecedente y requiere reconciliación de entregables.

Repositorio integral de investigación y peritaje forense para el caso de estudio de WannaCry en el National Health Service (NHS), con mapeo retrospectivo a NIST CSF 2.0 y NIST IR 8374 Rev. 1, análisis de código en Ghidra, entorno de laboratorio aislado en Vagrant/VirtualBox, paquete completo para la defensa oral (guion de 2 expositores, diapositivas y banco de preguntas del tribunal) e informe académico maestro respaldado por los 8 integrantes.

# Contexto y decisiones

- 2026-11-11: usuario confirma Windows 10 e ISO y licencia propias.
- Cuenta autenticada: leonidas854; repositorio: forense_nist_nhs.
- Equipo: 8 integrantes; 2 expositores en la defensa oral (Expositor 1: Marco, Caso NHS, GV, ID, PR; Expositor 2: Laboratorio, Ghidra, Memoria, Disco, DE, RS, RC).
- Capas comprobadas el 15/11/2026: `24d004...` contiene el kill switch y R/1831; ese recurso coincide con `ed01eb...` (~3.51 MB), que contiene XIA/2058. Proyecto nuevo en Ghidra 12.2 DEV mediante MCP; ver `docs/ghidra-mcp.md`.
- Configuración prevista del laboratorio: sin red (8 NICs none), comparticiones, portapapeles ni arrastrar/soltar. VM creada y apagada en un registro VirtualBox/IPC propio; aislamiento real comprobado. Sin Windows instalado.
- Fuentes públicas y herramientas oficiales descargadas con URL y SHA-256 fijados.
- Preservación estricta de la cadena de custodia y distinción entre datos históricos e hipótesis de laboratorio.

# Pendientes académicos

- Ejecutar el plan de cuatro personas; asignar nombres/revisores y fecha de entrega.
- Instalar Windows solo cuando se retome esa fase: box y VM vacías preparadas, herramientas descargadas y DVD conectado; ISO Windows sin configurar por indicación del usuario.
- Informe y matriz reconciliados. Falta adaptar diapositivas, guion, preguntas y dashboard anteriores a `docs/informe-forense.md`; no utilizarlos como conclusiones verificadas.
- Documentar procedencia previa de muestras y responsable humano; adquirir artefactos de Windows sólo si la rúbrica lo requiere y el entorno está comprobado.
- Incorporación de nombres y apellidos definitivos de los 8 estudiantes en las carátulas.
- Fecha y horario de la defensa fijados por la cátedra.

## Preparación local del 15/11/2026

Descargas originales verificadas (11/11), DVD de herramientas/lecturas generado,
exportación MCP de 16 funciones y VM aislada preparada. Detalle reproducible:
`docs/materiales-preparados.md`. No se instalaron Windows ni herramientas en el invitado.
