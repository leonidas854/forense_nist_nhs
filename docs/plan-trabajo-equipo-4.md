# Plan de elaboración y análisis: WannaCry, NHS y NIST CSF 2.0

**Paquetes individuales publicados:** [P1–P4: código, recorrido, herramientas y
entregables](../equipo/README.md). El plan define la secuencia; esas carpetas
contienen las 16 transcripciones seleccionadas que cada persona debe estudiar.
La [guía de alcance y ampliación](../equipo/ALCANCE-Y-AMPLIACION.md) aclara que
son el recorrido inicial de 1.755 funciones reconocidas, no una cobertura completa.
Incluye el siguiente trabajo de cada persona y los criterios para cerrar su alcance.

**Alcance acordado:** análisis estático de componentes de WannaCry para explicar
el caso NHS, contrastado con fuentes históricas y mapeado retrospectivamente a
NIST CSF 2.0. Equipo actual: **cuatro personas**. Fecha de planificación:
15/11/2026. Los nombres y la fecha de entrega se completarán cuando se conozcan.

Este plan organiza trabajo futuro; no presenta sus actividades pendientes como
realizadas. La organización antigua de ocho personas y dos expositores queda
como antecedente. Cada una de las cuatro personas desarrollará, documentará
y expondrá un componente, además de revisar el trabajo de otra.

## 1. Objetivo y preguntas que debe resolver el trabajo

El objetivo no es leer todo ensamblador de memoria. Es poder explicar y comprobar
una cadena de razonamiento: **archivo → estructura → función → instrucciones →
interpretación → fuente histórica → límite → resultado NIST relacionado**.

Preguntas principales:

1. ¿Qué pasó en el NHS según sus informes y la NAO?
2. ¿Qué son los cuatro componentes y cómo se relacionan sus bytes?
3. ¿Qué operaciones y condiciones muestra cada componente?
4. ¿Cómo corroboramos el pseudocódigo con Listing y los datos del archivo?
5. ¿Qué comportamiento del malware explica una observación y qué no demuestra?
6. ¿Qué controles y procesos de NIST ayudan a examinar el caso retrospectivamente?
7. ¿Qué podemos reproducir como lectura estática y ejercicio benigno en Windows 10?

**Alcance de las pruebas:** Ghidra examina muestras como datos; la simulación usa
estados y archivos ficticios. No se planifica ejecutar WannaCry, llamar a PlayGame,
cargar la DLL mediante un ejecutor, contactar el dominio, explotar SMB, cifrar
documentos o borrar copias. La instrucción previa del usuario fue simular sin
realizar el ataque. Una práctica benigna no se etiquetará como ejecución del malware.

## 2. Punto de partida comprobado

La tabla conserva el estado inicial del plan. **Actualización posterior del
15/11/2026:** descargas y DVD listos; base/box y VM creadas, VM apagada con
aislamiento comprobado; 18 pruebas correctas. Windows permanece sin instalar por
indicación del usuario. Ver [materiales preparados](materiales-preparados.md)
y [estado vigente](verificacion.md).

| Elemento | Estado al planificar | Consecuencia |
|---|---|---|
| Ghidra en Linux + MCP | Proyecto local preparado; versión 12.2 DEV | Se puede estudiar código desde ahora |
| Tres originales y derivados | Relaciones y hashes documentados | Usar originales preservados y copias de trabajo |
| Decompilaciones seleccionadas | 15 funciones exportadas, más PlayGame en suplemento | No equivalen a todo el código de todos los componentes |
| Funciones de t.wnry | Cabecera y camino de procesamiento estudiados | Criptografía completa y carga reconstruida pendientes |
| VM forense-nhs-win10 | `./lab status`: not created; VirtualBox no la encuentra | No hay Windows instalado acreditado |
| Box nhs/windows10-installer | No figura en `./lab box list` | Crear hardware vacío antes del primer arranque |
| ISO Windows configurada | No existe local/settings.json | Localizar ISO propia y comprobar edición, versión y hash |
| ISO de herramientas | local/herramientas.iso ausente | Preparar material verificado en el anfitrión |
| Paquetes Windows del lock | Seis archivos de descargas ausentes | Descargar y verificar antes de construir el DVD |
| Tests del repositorio | 16 correctos | Comprueban código del proyecto, no instalación del invitado |
| `./lab validate` | Correcto, con aviso experimental de none_communicator | Valida configuración; no demuestra aislamiento real |
| `check_isolation.py` | No aprobado: VM inexistente | Repetir cuando la VM exista |

La afirmación antigua de una ISO Windows 10 1903 detectada no acredita una ISO
disponible ahora. No asumir que el Windows elegido replica un host NHS ni que
es vulnerable a MS17-010. Windows 10 será una **estación docente**.

## 3. Glosario que los cuatro deben dominar antes de dividirse

| Concepto | Explicación inicial | Ejemplo del caso |
|---|---|---|
| Binario | Archivo de bytes; puede contener instrucciones y datos | Las muestras que abrimos en Ghidra |
| PE | Formato de ejecutables y bibliotecas de Windows | Un archivo puede ser PE aunque termine en .wnry |
| EXE / DLL | Programa ejecutable / biblioteca con funciones que otros componentes pueden usar | ec1383 tiene estructura DLL aunque su nombre termine en .exe |
| x86 / x64 | Arquitecturas de 32 / 64 bits | A y B son x86; D es x64 |
| Sección | Región descrita en la estructura PE | .rsrc suele contener recursos |
| Recurso | Datos incorporados al programa e identificados por tipo y nombre/ID | Un icono legítimo o un ejecutable almacenado como datos |
| Tipo de recurso | Categoría que puede tener nombre definido por el autor | W, R y XIA en estas muestras |
| Identificador | Número o nombre de una entrada de recursos | 101, 1831 y 2058 |
| Hexadecimal | Forma de escribir números en base 16 | 0x65 = 101; 0x727 = 1831; 0x80a = 2058 |
| Hash SHA-256 | Huella que permite cotejar bytes | El hash del recurso R/1831 coincide con ed01 |
| Offset de archivo | Posición contada desde el principio del archivo | Se usa para delimitar una extracción |
| Dirección virtual | Dirección del programa cargado en el modelo de Ghidra | 180001014 no es un offset para cortar el archivo |
| Puntero | Valor que indica una dirección de memoria | pDVar2 apunta a los datos de W/101 |
| DWORD | Valor de 4 bytes | Primer campo de W/101: longitud del contenido |
| Handle | Referencia que devuelve Windows para utilizar un objeto | Handle de archivo o recurso |
| API | Función ofrecida por una biblioteca o sistema | FindResourceA, WriteFile, CreateProcessA |
| Importación | Función externa utilizada por el programa | InternetOpenUrlA en WININET |
| Exportación | Función que una DLL ofrece a otros componentes | PlayGame en ec1383 |
| Decompilado | Reconstrucción en pseudocódigo parecido a C | Una condición if reconstruida por Ghidra |
| Desensamblado | Instrucciones interpretadas desde los bytes | TEST, JNZ y CALL en Listing |
| XREF | Referencia desde una instrucción o dato | Un uso de una cadena dentro del código |
| Dropper | Componente que deposita otra carga | La extracción de un PE desde un recurso |
| Carga/payload | Componente entregado para una siguiente función | No significa automáticamente «cifrador» |
| Análisis estático | Examinar archivos sin ejecutar sus instrucciones como programa | Importar un PE en Ghidra |
| Simulación | Representar un mecanismo con reglas y datos ficticios | Elegir retorno nulo/no nulo en una tabla |

### Qué significa exactamente W/101

Leerlo como **«recurso de tipo W e identificador 101»**. La barra es nuestra
notación para describir una entrada, no necesariamente una carpeta real del
disco. W es un nombre elegido en el programa: no significa necesariamente
Windows, worm o WannaCry. El ID 101 tampoco es un puerto ni una dirección.

```text
ec1383… (archivo PE)
└── estructura de recursos
    └── tipo "W"
        └── identificador 101 (= 0x65)
            └── datos: longitud + ejecutable interno + bytes posteriores
```

`FindResourceA(módulo, identificador, tipo)` localiza esa entrada. Encontrarla,
obtener sus bytes y escribirlos son operaciones diferentes. Microsoft documenta
los argumentos de tipo e identificador y la secuencia con LoadResource/LockResource.
[Microsoft, FindResourceA](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-findresourcea).

El mismo método de lectura sirve para **R/1831** y **XIA/2058**, pero su contenido
es distinto: R/1831 contiene ed01; XIA/2058 contiene un ZIP.

**Ejercicio común de aprobación:** cada integrante explica W/101 en un minuto,
sin usar «carpeta del virus» ni confundir tipo, identificador y archivo extraído.

## 4. Reparto entre cuatro personas

Personas P1–P4 son puestos que se asignarán a nombres reales. Todos leen las
fuentes históricas básicas; nadie queda únicamente como operador de herramientas.

| Persona | Componente principal | Responsabilidad transversal | Revisor |
|---|---|---|---|
| P1 | 24d004… | Coordinación del informe y hechos históricos NHS/NAO | P2 |
| P2 | ed01… | Inventario, relaciones padre/hijo y registro de integridad | P3 |
| P3 | u.wnry | Simulación benigna, recuperación y límites de evidencia | P4 |
| P4 | ec1383… | Configuración de VM, herramientas y pruebas de instalación | P1 |

El revisor debe repetir al menos una comprobación, no solo corregir ortografía.
El laboratorio se prepara entre P4 y otro integrante; no se encarga a P4 que
también investigue toda la criptografía pendiente.

### P1 — Capa A: decisiones, servicio y contención de B

- Identificar arquitectura, tamaño y hash de 24d004.
- `00408140`: explicar resultado de WinINet, condición y ramas; contrastar con
  TEST/JNZ en `004081a3` y `004081a5`.
- `00408090` y `00407f20`: distinguir caminos según argumentos.
- `00407c40`: explicar solicitudes de servicio y controles de retorno.
- `00407ce0`: seguir R/1831 hasta la escritura y demostrar relación con ed01.
- `00407480`: limitar el hallazgo de puerto 445; no afirmar explotación completa.
- Historia: entrada probable, equipos afectados y diferencia infección/interrupción.
- Entrega: mapa A → B, dos pares C/Listing comentados, ficha de servicio y límites.
- Aceptación: P2 reproduce la condición del kill switch y la identidad del recurso.

### P2 — Capa B: paquete y frontera de t.wnry

- Comprobar igualdad entre ed01 y R/1831 de A.
- `00401dab`: explicar XIA/2058 y el ZIP; distinguir extracción PE de extracción ZIP.
- `00401fe7`: seguir preparación del entorno y llamadas condicionadas.
- `00401064`: distinguir creación de proceso, espera y resultado de una orden.
- `004014a6`: relacionar cabecera WANACRY! y campo 256 con bytes de t.wnry.
- `00402158`: explicar CALL EAX y las condiciones anteriores a esa transferencia.
- No presentar contraseña ZIP como clave de recuperación de documentos.
- Entrega: árbol de miembros, ficha de t.wnry y registro de qué está pendiente.
- Aceptación: P3 identifica formato y condiciones; no se exige reconstruir todo
  el cifrador para cerrar el alcance académico acordado.

### P3 — Capa C1: cadena de recuperación y uso potencial

- Identificar u.wnry como PE extraído del ZIP de B.
- `00420fd8`: describir la finalidad de los grupos de operaciones de la cadena,
  sin ejecutarlas ni convertirlas en instrucciones de práctica.
- `004066fe` y `0040670c`: seguir referencias y copia en Listing.
- `00401bb0`: explicar SID/token y diferencia entre fallo de consulta y resultado.
- `00401b50`, `00401a90`: seguir solicitudes de ejecución y condiciones.
- Registrar que el bloque principal no tiene una función contenedora recuperada;
  usar Listing y auxiliares decompilables sin inventar código faltante.
- Historia: alcance documentado de recuperación; no afirmar borrado universal.
- Entrega: tabla cadena → referencia → API → efecto hipotético → evidencia faltante.
- Aceptación: P4 explica por qué crear un proceso no demuestra copias eliminadas.

### P4 — Capa D: recurso W/101, PlayGame y laboratorio

- Identificar ec1383 como DLL x64 y comprobar exportación PlayGame.
- `1800011a4`: explicar ruta C:\WINDOWS\mssecsvc.exe y orden de llamadas.
- `180001014`: reconstruir FindResourceA y longitud/recurso+4 en WriteFile.
- `1800010f8`: explicar solicitud de creación de proceso y su retorno.
- Comparar paso de parámetros x86/x64 con un ejemplo sencillo.
- Cotejar el PE extraído 93db4b26…: distinto de 24d004; procedencia externa pendiente.
- Entrega: diagrama del recurso, decompilado anotado y expediente de preparación VM.
- Aceptación: P1 reproduce límites de extracción y distingue ruta, servicio y exportación.

## 5. Secuencia de trabajo y dependencias

Propuesta: **10 sesiones de 2 horas por integrante**, unas 20 horas por persona,
distribuidas en dos o tres semanas según disponibilidad. Las descargas e instalación
pueden requerir tiempo adicional. No son plazos contractuales ni ejecución ya hecha.

| Sesión | Actividad | Responsable | Entregable / condición para avanzar |
|---|---|---|---|
| 1 | Alcance, glosario y mapa de contención | Todos | Los cuatro explican recurso, hash, dirección y análisis estático |
| 2 | Leer fuentes NHS/NAO y método NIST | P1 coordina; todos | Tabla H con fuente, página, cita breve/paráfrasis y límite |
| 3 | Inventario, hashes, procedencia y carpeta de trabajo | P2 coordina | Registro real; lagunas de procedencia marcadas |
| 4 | Preparar VM/herramientas; practicar Ghidra del anfitrión mientras tanto | P4 + apoyo | Base y primer arranque solo si prerrequisitos están verificados |
| 5 | Análisis individual de componentes | P1–P4 | Entradas, condiciones, operaciones y salidas documentadas |
| 6 | Completar fichas y pares C/Listing | P1–P4 | Cada afirmación principal apunta a evidencia local |
| 7 | Revisión cruzada y corregir contradicciones | Ronda P1→P2→P3→P4→P1 | Registro de repetición y observaciones del revisor |
| 8 | Lectura en Windows y simulación benigna | P3 + P4; todos | Pruebas T01–T05 con resultado observado, o pendiente explícito |
| 9 | Integrar informe, matriz NIST y presentación | Todos | Separación H/L/I/S/P y narrativa coherente |
| 10 | Ensayo oral y comprobación final | Todos | Exposición sin afirmar ejecución o procedencia no demostrada |

Sesiones 5–6 pueden avanzar en Linux si Windows sigue pendiente. La sesión 8
depende de una VM instalada y verificada, no del calendario. No abrir redes
para saltarse esa dependencia. Una persona no debe editar simultáneamente el
mismo proyecto Ghidra abierto por otra: usar copias/archivos exportados identificados
o turnos de edición, preservando el proyecto maestro.

## 6. Procedimiento común para analizar una función

1. Registrar SHA-256 completo del archivo, nombre de programa y versión de herramienta.
2. Abrirlo dentro de Ghidra; distinguir importar para examinar de ejecutar el archivo.
3. Ir a la dirección con G y capturar el contexto del programa activo.
4. Leer primero propósito de las APIs en documentación oficial.
5. Marcar entradas, condiciones, llamadas y salidas en el Decompiler.
6. Corroborar en Listing al menos los argumentos decisivos y un salto condicional.
7. Seguir referencias al dato o al destino; no deducir todo por una cadena aislada.
8. Contrastar con bytes/recursos/hashes cuando la conclusión sea sobre contenido.
9. Escribir observación literal y, separadamente, interpretación e hipótesis.
10. Guardar respuesta MCP o captura local, fecha real, comando y responsable.
11. Solicitar repetición por el revisor. Registrar diferencias de versión o tipos.

**No exigir texto C idéntico entre versiones de Ghidra:** pueden cambiar nombres
y recuperación de variables. La aceptación requiere la misma relación sustentada
en bytes, argumentos y flujo. No modificar una muestra para que coincida con la guía.

## 7. Windows 10: preparación por etapas

### 7.1. Arquitectura y alcance

Configuración existente que se pretende materializar: 2 CPU virtuales, 4096 MiB
RAM, disco dinámico de 64 GiB, consola gráfica y discos ópticos. En este plan
no se modifica Vagrantfile ni se crea la VM todavía.

- Ocho interfaces de red deshabilitadas: sin NAT, puente ni red solo anfitrión.
- Sin carpetas compartidas, portapapeles, arrastrar/soltar, USB ni VRDE.
- Comunicador Vagrant none; instalación por consola, sin WinRM/SSH.
- Ghidra MCP permanece en loopback del anfitrión. Windows usará su Ghidra local:
  no se abre una red para comunicar ambos. Las direcciones 127.0.0.1 pertenecen
  a cada equipo, no son una conexión automática anfitrión/invitado.
- Windows 10 no reproduce automáticamente el parque NHS de 2017. Anotar edición
  y build reales; su compatibilidad con las herramientas debe comprobarse.

Windows 10 Home/Pro terminó su soporte ordinario en octubre de 2025; ediciones
especiales tienen ciclos propios. No se presenta esta VM docente como sistema
actual de producción. [Microsoft, ciclo de Windows 10](https://learn.microsoft.com/en-us/lifecycle/products/windows-10-home-and-pro).

### 7.2. Prerrequisitos — P4 prepara, P1 revisa

1. Localizar ISO Windows 10 x64 propia y licencia correspondiente; registrar hash
   y procedencia en local/. No copiar claves al informe ni al repositorio.
2. Comprobar virtualización, espacio real disponible para base, VM y snapshots,
   y versiones instaladas de VirtualBox/Vagrant. Los 64 GiB son capacidad del
   disco virtual, no espacio reservado suficiente para todas sus copias.
3. Revisar `scripts/create-base.sh`, `scripts/download.sh` y
   `scripts/build-tools-iso.sh` antes de ejecutarlos.
4. Descargar herramientas en el anfitrión y cotejar las versiones fijadas. Si
   una URL ya no sirve o un hash falla, registrar el problema; no actualizar
   silenciosamente el lock ni omitir la verificación.
5. El DVD actual previsto incluye herramientas, configuración y documentación,
   **no incluye automáticamente muestras, proyecto Ghidra ni simulación**.
   Planificar otro medio óptico de trabajo con inventario y hashes si hace falta.

Comandos previstos, desde la raíz del proyecto; todavía no ejecutados como
instalación en este plan:

```bash
bash scripts/download.sh
sha256sum -c config/SHA256SUMS
bash scripts/build-tools-iso.sh
export WIN10_ISO='/ruta/real/a/Windows10.iso'
bash scripts/create-base.sh
./lab validate
./lab up
python3 scripts/check_isolation.py
```

Reemplazar la ruta de ejemplo por la ISO comprobada. Mantener WIN10_ISO en la
sesión o registrar la ruta en local/settings.json. `create-base.sh` crea y
registra hardware vacío y una box local; **no instala Windows**. Si encuentra
una base previa o falla parcialmente, inspeccionar antes de repetir y no borrar
discos como solución automática.

### 7.3. Instalación y comprobación dentro del invitado

1. Antes del primer uso, comprobar que la personalización deshabilitó las NIC;
   validar sintaxis de Vagrant no sustituye inspeccionar el hipervisor real.
2. En la consola de la VM, instalar Windows en el disco vacío de esa VM.
3. Elegir la edición de la licencia y cuenta local; no incorporar datos personales.
   No conectar a Internet para resolver un paso del instalador.
4. Registrar pantalla de versión/build, fecha/zona horaria y disco de instalación.
   Evitar claves y datos personales en capturas.
5. Copiar del DVD herramientas verificadas a C:\Forense\Herramientas.
6. Instalar/configurar el JDK requerido por la distribución Windows seleccionada
   y abrir ghidraRun.bat. El lock prevé Ghidra PUBLIC/JDK 25; el anfitrión usa DEV
   y Java 27. Son entornos distintos, no deben declararse idénticos.
7. Registrar `java -version`, versión de Ghidra y una apertura de prueba con un
   archivo benigno. Compatibilidad se acepta solo después de esa comprobación.
8. Apagar desde Windows y crear snapshot **limpio-herramientas** con `./lab`.
   No usar apagado forzado como procedimiento normal de adquisición.

```bash
./lab snapshot save limpio-herramientas
python3 -m unittest discover -s tests -v
./lab validate
python3 scripts/check_isolation.py
```

Registrar las tres comprobaciones después de cualquier cambio del laboratorio.
Si la última falla, corregir la configuración manteniendo el aislamiento antes
de introducir material de trabajo. Las capturas antiguas del repositorio no
acreditan el estado de esta instalación nueva.

### 7.4. Material de estudio y salida de resultados

Primero llevar al invitado guías y decompilaciones exportadas mediante un medio
óptico inventariado. Para repetir el análisis, utilizar copias verificadas de
las muestras importadas **desde Ghidra**, sin ejecutarlas ni abrirlas como programas.
Si la protección del invitado bloquea o pone en cuarentena una copia, registrar
el evento; continuar con los textos exportados y Ghidra anfitrión, sin introducir
exclusiones ni desactivar controles como atajo.

Crear un proyecto independiente en Windows. No abrir una copia incompleta del
proyecto anfitrión mientras este está en uso. Guardar la versión de cada proyecto
y mantener una sola persona como editora de cada copia.

Resultados textuales, capturas y logs de la práctica se conservan inicialmente
en C:\Forense\Resultados. Para extraerlos, planificar un disco de evidencias
dedicado, conectarlo/desconectarlo con la VM apagada y leer una copia con un
procedimiento de solo lectura en la estación de análisis. Inventariar el medio
y comprobar hashes; no usar el disco del sistema anfitrión ni carpetas compartidas.
Los detalles del medio se documentan antes de implementarlo; este plan no lo crea.

Preservar resultados antes de revertir un snapshot. Un snapshot sirve para volver
a un estado de práctica; no sustituye una adquisición ni demuestra procedencia.

## 8. Qué probar en Windows 10

| Prueba | Acción prevista | Resultado esperado | Qué no demuestra |
|---|---|---|---|
| T01 — entorno | Abrir Ghidra y comprobar Java/build/VM | Herramienta operativa e aislamiento comprobado | Reproducción del NHS o ejecución de malware |
| T02 — lectura estática | Revisar una condición y un recurso en copias de trabajo, o textos si se bloquea la importación | Mismos bytes/flujo o limitación registrada | Que la rama se ejecutó |
| T03 — kill switch ficticio | Elegir manualmente cero/no cero en tabla o simulador sin red | Dos ramas representadas correctamente | Respuesta del dominio real |
| T04 — recursos ficticios | Representar W/101 con una estructura de ejemplo que contenga texto inocuo y longitud | Comprender tipo, ID, longitud y contenido | Extracción/ejecución real de una carga |
| T05 — recuperación ficticia | Crear documentos de prueba y respaldo, marcar un estado simulado y copiar el respaldo a otra carpeta para cotejar hashes y lectura | Evidencia de copia/restauración del ejercicio | Descifrado de WannaCry o recuperación hospitalaria |

T03/T04 pueden comenzar con tablas y archivos de texto; un simulador programado
es opcional y todavía **por elaborar**. Su especificación: solo datos dentro de
una carpeta de práctica, sin red, sin lanzar muestras, sin privilegios elevados,
sin cambiar servicios, permisos del sistema, copias sombra ni configuración de arranque.
Representar «afectado» como un estado, sin cifrar ni destruir documentos.

Los registros de T03–T05 llevarán **SIMULACIÓN** en el título, con datos ficticios.
Si se usa Process Monitor con una operación benigna, etiquetar sus eventos como
actividad del ejercicio. No convertirlos en supuestos eventos de WannaCry.
Capturas de RAM, PCAP y explotación no son requisitos de este alcance estático.

## 9. Documentación uniforme para los cuatro

Cada integrante elaborará una ficha con esta estructura:

1. Pregunta y alcance del componente.
2. Identidad: hash completo, tamaño, tipo PE, arquitectura y procedencia conocida.
3. Glosario propio, definido antes de usar términos en la explicación.
4. Diagrama de contención separado del flujo de llamadas.
5. Tabla de funciones y direcciones virtuales.
6. Dos o más pares de fragmentos Decompiler/Listing con explicación de argumentos,
   condiciones y resultados. Si no hay función decompilable, documentar el límite.
7. Recursos/cadenas/importaciones relevantes y cómo se referencian.
8. Hallazgos con evidencias, interpretaciones y alternativas.
9. Fuente NHS/NAO relacionada, con página/sección y alcance exacto.
10. Mapeo NIST con razón y evidencia que falta para evaluar el resultado.
11. Actuaciones y revisión independiente.
12. Conclusión que pueda leerse en voz alta sin exagerar lo demostrado.

Etiquetas obligatorias para no mezclar resultados:

| Etiqueta | Significado | Ejemplo |
|---|---|---|
| H | Hecho documentado históricamente | Cifra atribuida a NAO con edición y página |
| L | Observación local estática o del entorno | Recurso R/1831 igual a ed01 |
| I | Inferencia o hipótesis | Una restricción de red podría afectar una condición |
| S | Simulación | Registro ficticio de un estado «afectado» |
| P | Pendiente/no comprobado | Procedencia previa o ejecución en un host NHS |

Guardar registros reales en `local/equipo-4/P1/` a `P4/`, con fecha y nombres
reales del responsable y revisor. Las plantillas versionadas permanecen vacías.
En Git pueden quedar planes, metodología y conclusiones académicas revisadas;
no muestras, claves, proyectos, discos o evidencias reales. No publicar rutas
personales o datos sensibles en capturas de exposición.

Entrega sugerida: ficha de 4–6 páginas por componente, glosario común, informe
integrado de unas 18–25 páginas y anexos técnicos locales. Ajustar a la rúbrica;
la aceptación depende de trazabilidad, no de llenar páginas.

## 10. Fuentes históricas y mapeo NIST

P1 coordina la lectura de NAO y NHS; cada persona verifica al menos un pasaje:

- P1: NAO resumen 5–6, PDF pp.8–10; distinguir afectados de infectados y cifras
  observadas de estimaciones. NHS §2.3 para entrada probable.
- P2: NAO resumen 12 y §2.5; sistemas sin parchear. No inferir parches desde Ghidra.
- P3: NHS §2.14, PDF p.12; respetar alcance de recuperación de prácticas infectadas.
- P4: NAO resumen 12; propagación e infraestructura sin asumir una topología
  completa. La historia no acredita el origen de ec1383.

SP 800-86 aporta el método de preservación, examen, análisis e informe. CSF 2.0
aporta resultados de gestión del riesgo. No es una certificación ni una norma
que se aplicara en 2017 bajo esa versión. Consultar los PDFs preservados y
la matriz existente, conservando sus códigos y límites.

| Función | Resultados a trabajar | Trabajo principal y responsable |
|---|---|---|
| Govern | GV.RR-02, GV.OV-01 | P1: roles y seguimiento de avisos; separar equipo académico de gobernanza NHS |
| Identify | ID.AM-01, ID.RA-01 | P4 con P2: inventario y vulnerabilidades; muestras no equivalen a inventario clínico |
| Protect | PR.PS-02, PR.IR-01, PR.DS-11 | P4/P3: software, exposición y respaldos; distinguir diseño de verificación |
| Detect | DE.CM-01, DE.CM-09, DE.AE-03 | P3 con P1: qué logs se necesitarían; no crear evidencia de malware ficticia |
| Respond | RS.AN-03, RS.AN-06, RS.AN-07 | Todos; P2 integra registro, integridad y relación entre muestras |
| Recover | RC.RP-01, RC.RP-03, RC.RP-05 | P3: plan, respaldo y prueba benigna; ninguna implica recuperación del NHS |

No poner «cumple» por encontrar una API. Cada fila debe indicar **fuente →
observación → relación con el resultado → comprobación necesaria → limitación**.
Los roles numerados de ocho personas de la matriz anterior se reconciliarán
con este reparto al integrar la nueva edición, preservando el antecedente.

## 11. Presentación con secuencia clara

Propuesta de 24 minutos, seis por persona; ajustar si el docente fija otra duración.

| Persona | Secuencia de explicación |
|---|---|
| P1 | Pregunta, alcance, hecho histórico, mapa de contención y kill switch/R/1831 |
| P2 | Qué es PE/recurso/ZIP; ed01, paquete, t.wnry y frontera de lo no reconstruido |
| P3 | u.wnry: cadena → referencia → rutina; diferencias entre capacidad y efecto; simulación/recuperación |
| P4 | ec1383 como rama adicional; W/101, PlayGame, x64; estado de VM y síntesis NIST con límites |

Mostrar primero un diagrama simple y después dos o tres instrucciones relevantes.
No proyectar cien líneas y leerlas sin explicar entradas y salidas. Para cada
pantalla: identificar archivo/dirección, explicar una acción y cerrar con una
conclusión y su límite. La rama ec1383 no se presenta como sucesora probada de u.wnry.

Ensayo: otro integrante pregunta «¿cómo lo sabes?» y el expositor debe señalar
bytes, dirección, consulta o página de fuente. Si solo puede responder «lo dijo
Gemini/Codex», el hallazgo aún necesita sustento.

## 12. Criterios para dar por terminado el trabajo

- [ ] Cuatro responsables y revisores identificados; alcance y fecha de entrega acordados.
- [ ] Los cuatro explican W/101, PE, hash, puntero, API y las dos vistas de Ghidra.
- [ ] Identidad de muestras y relaciones documentadas; procedencia desconocida no inventada.
- [ ] Cuatro fichas con fragmentos cotejados y revisión independiente.
- [ ] Diagrama diferencia contención, llamadas y cronología histórica.
- [ ] Historia con edición, página y alcance; hipótesis rotuladas.
- [ ] VM instalada y herramientas comprobadas, o pendientes claramente declarados.
- [ ] T01–T05 registradas solo cuando ocurran; simulación diferenciada de malware.
- [ ] Matriz NIST revisada semánticamente, sin certificación ficticia.
- [ ] Diapositivas, guion y preguntas anteriores reconciliados con las nuevas fichas.
- [ ] Tests/validate/isolation revisados según los cambios; resultados preservados.
- [ ] Ninguna evidencia real, muestra, clave o disco agregado a Git.

## Material para comenzar y referencias

- [Recorrido inicial de Ghidra](recorrido-ghidra-explicado.md).
- [Capas y comparación Decompiler/Listing](guia-capas-decompilado-desensamblado.md).
- [Decompilaciones locales](../local/decompilados-ghidra/LEEME.md); el enlace requiere los archivos locales excluidos de Git.
- [Informe corregido](informe-forense.md), [matriz NIST](matriz-nist.csv) y [guía de comprobación](guia-comprobacion-nist.md).
- [Laboratorio existente](laboratorio.md); el estado actual de este plan prevalece sobre afirmaciones antiguas no comprobadas.
- Kent, K., Chevalier, S., Grance, T., & Dang, H. (2006). *Guide to Integrating Forensic Techniques into Incident Response* (NIST SP 800-86). https://doi.org/10.6028/NIST.SP.800-86
- NIST. (2024). *The NIST Cybersecurity Framework (CSF) 2.0*. https://doi.org/10.6028/NIST.CSWP.29
- NAO. (2018, edición revisada). *Investigation: WannaCry cyber attack and the NHS* (HC 414). PDF preservado en fuentes/NAO-WannaCry-NHS.pdf.
- Department of Health and Social Care. (2018). *Lessons learned review of the WannaCry ransomware cyber attack*. PDF preservado en fuentes/NHS-lessons-learned-2018.pdf.
