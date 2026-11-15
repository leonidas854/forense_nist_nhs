# Las 16 funciones: alcance, otras rutinas y ampliación del análisis

[Índice del equipo](README.md) · [Cómo estudiar](COMO-ESTUDIAR.md) · [Plan de sesiones](../docs/plan-trabajo-equipo-4.md)

**Las 16 funciones publicadas son un recorrido inicial, no todo el código de los
cuatro componentes.** Se seleccionaron para explicar decisiones, recursos y
solicitudes de ejecución con localizadores concretos. El trabajo puede y debe
ampliarse cuando una conclusión dependa de funciones todavía no examinadas.

La pregunta forense determina hasta dónde seguir una ruta. El hecho de que una
función no esté en `codigo.md` no significa que no exista ni que sea irrelevante.

## 1. Cuántas funciones reconoce el proyecto

Consulta mediante Ghidra MCP `list_project_binaries`, campo `# of Functions`,
del **15/11/2026 a las 14:50:45, America/La_Paz (18:50:45 UTC)**. Proyecto
Ghidra 12.2 DEV descrito en [ghidra-mcp.md](../docs/ghidra-mcp.md).

| Participante | Componente | Funciones reconocidas | Transcripciones publicadas |
|---|---|---:|---:|
| P1 | 24d004… | 176 | 6 |
| P2 | ed01… | 244 | 4 |
| P3 | u.wnry | 1.070 | 3 |
| P4 | ec1383… | 265 | 3 |
| **Total de los cuatro componentes** | | **1.755** | **16** |

Las identidades SHA-256 completas están en [indice.json](indice.json). El registro
original de la consulta queda en
`local/preparacion/alcance-funciones-20261115185045.json`, fuera de Git.
Esta tabla es una síntesis documental; no distribuye el registro original.

También están importados otros tres programas: `W_101_contenido.exe` (180
funciones), `taskdl.exe` (54) y `taskse.exe` (30). No forman parte del total de
1.755 ni tienen cuadernos completos de análisis publicados. `t.wnry` no se está
contando como una DLL descifrada: solo se ha estudiado parcialmente su contenedor
y el camino que lo procesa.

**Cómo interpretar los números:**

- Son funciones reconocidas en el estado actual del proyecto. Pueden cambiar
  al corregir límites o al modificar el análisis; no son una propiedad inmutable
  del hash del archivo.
- El recuento puede incluir rutinas de bibliotecas, arranque, excepciones y
  pequeños intermediarios de llamadas (*thunks*). No equivale a una cantidad de
  comportamientos maliciosos diferentes.
- Una función reconocida no implica una decompilación correcta ni una
  interpretación revisada. También puede haber instrucciones sin una función
  contenedora bien recuperada, como el bloque de interés de u.wnry.
- 16/1.755 **no es un porcentaje de avance forense**. Las funciones tienen
  tamaños, relevancia y dificultades diferentes; además, el trabajo incluye datos,
  recursos, referencias, fuentes históricas y límites de atribución.

## 2. Por qué se publicaron esas 16

La selección corresponde al recorrido inicial del equipo:

| Persona | Pregunta que cubre la selección | Lo que deja abierto |
|---|---|---|
| P1 | Qué condición lleva a otras rutinas; cómo se solicita el servicio y se accede a R/1831 | Todos los caminos del servicio y la caracterización completa de la propagación |
| P2 | Cómo se accede al ZIP y qué condiciones preceden al procesamiento de t.wnry | Semántica completa de las transformaciones y de la carga final |
| P3 | Qué auxiliares consultan el token y solicitan ejecutar procesos | Decompilación del bloque llamador y análisis del resto de u.wnry |
| P4 | Cómo PlayGame conecta W/101 con una solicitud de proceso | Inicialización completa de la DLL, identidad funcional del PE interno y procedencia histórica |

No hubo un límite de Ghidra que obligara a publicar solo 16. Fue una selección
didáctica. Tampoco hay una exigencia de NIST de estudiar esas 16 concretas.
El alcance exhaustivo de los cuatro componentes **no está completado**.

## 3. Qué son las otras funciones

Los siguientes nombres y direcciones aparecen en el proyecto consultado. La
columna de función habitual explica el símbolo; **no significa que se haya
auditado el cuerpo de cada rutina ni todos sus usos**. Se debe contrastar nombre,
destino, argumentos, instrucciones y referencias antes de emitir una conclusión.

| Grupo | Ejemplo observado | Función habitual / pregunta de análisis |
|---|---|---|
| Copia e inicialización de datos | ed01: `memcpy` en `00407706`; `memset` en `004076ae` | Copiar o inicializar memoria; identificar qué datos y cuánto se procesa |
| Comparación y cadenas | ed01: `strcmp` en `00407740`; `strlen` en `004076b4` | Comparar cadenas o medir su longitud; seguir cómo se usa el resultado |
| Gestión de memoria | ed01: `operator_new` en `00407700`; ec1383: `malloc` en `180005e24` | Reservar memoria; seguir tamaño, contenido y uso posterior |
| Entrada e inicialización | 24d004: `entry` en `00409a16`; ec1383: `_CRT_INIT` en `18000137c` y `__DllMainCRTStartup` en `1800014d0` | Preparar el entorno de ejecución y determinar qué rutas se activan |
| Excepciones y comprobaciones | u.wnry: `Unwind@0041363b`; ec1383: `__security_check_cookie` en `180005a60` | Manejo de excepciones o comprobaciones de pila; distinguirlo de acciones sobre archivos de la víctima |
| Rutinas sin nombre semántico | ed01: `FUN_004021bd` y `FUN_00402924` | Examinar entradas, llamadas, retorno y uso del resultado; su nombre no explica su propósito |

`FUN_004021bd` significa que Ghidra asignó un nombre automático vinculado a una
dirección. No significa «función de cifrado» ni «función sin importancia». Los
nombres españoles, como `Extraer_Recurso_W_101`, fueron añadidos por el analista;
deben mantenerse separados de los símbolos originales o reconocidos automáticamente.

Una rutina de biblioteca puede ser auxiliar y aun así importar: por ejemplo,
una comparación puede decidir si se acepta la cabecera de un archivo. La prioridad
depende de su papel en la pregunta investigada, no solo de su nombre.

## 4. Tres niveles de trabajo y su estado

| Nivel | Qué se hace | Estado actual | Entrega esperada |
|---|---|---|---|
| Inventario | Enumerar funciones por programa, dirección, nombre y condición externa/thunk | Recuentos globales comprobados; inventario fila por fila del equipo pendiente | Registro local completo, con fecha y versión |
| Clasificación | Separar soporte, bibliotecas, rutas de interés y funciones desconocidas | Ejemplos y rutas parciales; sin clasificación exhaustiva | Categoría provisional, fundamento y dudas por función |
| Análisis profundo | Examinar entradas, condiciones, llamadas, datos, retornos y referencias de rutas prioritarias | 16 transcripciones y hallazgos seleccionados; límites documentados | Fichas verificadas y síntesis con alcance explícito |

No pasar de «está en el inventario» a «está analizada» automáticamente. Tampoco
clasificar toda la lista como maliciosa por pertenecer a una muestra de malware.

Para iniciar el inventario, copia [INVENTARIO-FUNCIONES.csv](INVENTARIO-FUNCIONES.csv)
a `local/equipo/Pn/`. Está vacío a propósito. `prioridad` puede ser alta, media o
baja, siempre con justificación; `estado` puede ser pendiente, lectura inicial
o revisado. Ninguna de estas etiquetas equivale a cumplimiento NIST.

## 5. Cómo encontrar y priorizar lo que falta

1. En el proyecto local, selecciona el programa correcto y comprueba su identidad.
   Abre **Symbol Tree → Functions** para recorrer sus funciones. El clon de Git
   contiene las transcripciones, no el proyecto ni las muestras.
2. Registra dirección y nombre. Distingue una rutina propia, un símbolo externo
   y un thunk cuando la herramienta permita identificarlo; anota las dudas.
3. Desde una función seleccionada, identifica **quién la llama** y **a quién
   llama**. Son preguntas diferentes: una referencia a datos tampoco equivale a
   una llamada ejecutada.
4. Prioriza lo que decide una rama, transforma datos relevantes, controla un
   recurso o produce un resultado que tu conclusión necesita explicar.
5. Marca como provisional una clasificación basada solo en el nombre. Antes de
   cerrar una interpretación, contrasta Decompiler, Listing y datos/referencias.
6. Si hay una llamada indirecta, registra cómo se obtiene el destino. No inventes
   una arista a una función concreta si todavía no has resuelto ese destino.
7. Si falta una función recuperada, registra el bloque y sus límites conocidos.
   No crees límites arbitrarios solo para obtener una salida del Decompiler.
8. Conserva el inventario original localmente. Publica una síntesis académica
   revisada, con direcciones, argumentos y limitaciones, siguiendo `AGENTS.md`.

## P1

**Ampliación de 24d004…**, revisada por P2:

- Seguir llamadores y destinos del servicio desde `00408090`, incluida la
  referencia a `LAB_00408000`. `LAB_…` es una etiqueta; no se afirma aquí que
  sea una función nueva correctamente delimitada.
- Examinar el contexto y las referencias de `00407480`, identificando las
  llamadas por ordinal y sus argumentos antes de atribuir un mecanismo de red.
- Distinguir código de arranque en torno a `entry` de las decisiones posteriores.
- Entregar un mapa de llamadas con condiciones y rutas todavía pendientes.

**Criterio de cierre:** explicar las rutas examinadas y señalar qué falta para
afirmar propagación completa. La constante 445 por sí sola no demuestra EternalBlue.

## P2

**Ampliación de ed01…**, revisada por P3:

- Seguir las auxiliares de apertura/recorrido del paquete, entre ellas
  `004075ad`, `004075c4` y `0040763d`, desde el contexto de `00401dab`.
- Examinar las transformaciones referenciadas por `004014a6`, sin asignarles
  automáticamente un algoritmo por observar tamaños o nombres de datos.
- Profundizar en `004021bd` y `00402924`: argumentos, retorno y cómo ese retorno
  acaba utilizado como dirección de código.

```text
00401fe7 (llamador)
  → 004014a6: lectura/procesamiento documentado parcialmente
  → 004021bd: caracterización completa pendiente
  → 00402924: resultado usado para obtener un destino
  → 00402158 CALL EAX: transferencia indirecta observada
```

Este esquema resume el camino documentado, sujeto a sus condiciones. `00402158`
es el sitio de llamada: no es el cuerpo completo de la función invocada.

**Criterio de cierre:** separar formato, procesamiento, resolución de destino y
carga final. Si no se completa la interpretación criptográfica, mantenerla pendiente.

## P3

**Ampliación de u.wnry**, revisada por P4:

- Estudiar el bloque de Listing que referencia `00420fd8`, incluidos `004066fe`
  y `0040670c`, sus predecesores y sus destinos.
- Determinar qué límites de función están sustentados y cuáles siguen sin
  recuperar; usar las auxiliares decompilables como apoyo, no como sustitución
  de un bloque principal que no decompila correctamente.
- Inventariar y clasificar el resto de u.wnry sin asumir que sus 1.070 funciones
  corresponden todas a sabotaje de recuperación.

**Criterio de cierre:** sostener la relación dato → referencia → condición →
solicitud de proceso, dejando separados elevación concedida, ejecución terminada
y efecto real. Para estos últimos harían falta evidencias distintas del código.

## P4

**Ampliación de ec1383…**, revisada por P1:

- Examinar `entry`, `_CRT_INIT` y `__DllMainCRTStartup` para seguir la
  inicialización de la DLL. Estos nombres son puntos de partida, no prueba de
  que PlayGame se invoque automáticamente.
- Rastrear dónde se establece `DAT_18000d3a8` y cómo se usa `DAT_18000d2a0`:
  distinguir el contexto del módulo de la ruta de salida.
- Comparar el PE de W/101 (`93db4b26…`) con 24d004… mediante una pregunta
  concreta sobre estructura o funciones. Diferencia de hash demuestra diferencia
  de bytes; no determina por sí sola cuánto comportamiento comparten.

**Criterio de cierre:** explicar inicialización, extracción y solicitud de proceso
en las rutas examinadas. Mantener pendiente la atribución a una cadena de infección
histórica cuando no haya procedencia y artefactos suficientes.

## 6. Cómo justificar el alcance en la materia y con NIST

El reparto y la profundidad de lectura son decisiones metodológicas del trabajo.
No presentar «16 funciones revisadas» como una exigencia o certificación NIST.
[SP 800-86, capítulo 3](../fuentes/NIST.SP.800-86.pdf) sirve para organizar
recolección, examen, análisis e informe; [CSF 2.0](../fuentes/NIST.CSWP.29.pdf)
aporta los resultados de gestión mapeados retrospectivamente.

En la [matriz del caso](../docs/matriz-nist.csv), N-11, N-12 y N-13 relacionan
análisis, registro e integridad/procedencia. Para cada conclusión, el informe debe
indicar la pregunta, selección de material, procedimiento, observación, interpretación,
limitación y revisión. No se ha auditado el cumplimiento de un hospital.

Una formulación defendible para la exposición es:

> Ghidra reconoce 1.755 funciones en los cuatro componentes seleccionados. Nuestro
> material de lectura contiene 16 transcripciones para estudiar rutas específicas.
> No afirmamos haber analizado todas las funciones ni reconstruido todo WannaCry.
> Las ampliaciones y las limitaciones de cada componente están documentadas.

Cambiar esta formulación únicamente cuando nuevas comprobaciones justifiquen un
alcance mayor. El inventario completo, la clasificación exhaustiva y la revisión
de todos los caminos permanecen pendientes; no se han realizado al escribir esta guía.
