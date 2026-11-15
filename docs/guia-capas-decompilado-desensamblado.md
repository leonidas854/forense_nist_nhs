# Capas de WannaCry: del archivo al código y a la conclusión forense

Revisión mediante Ghidra MCP del 15/11/2026. Complementa el
[recorrido inicial](recorrido-ghidra-explicado.md). Nuevas consultas conservadas
en `local/capas-ghidra/`; resultados anteriores en `local/recorrido-ghidra/`.
Los originales, PDFs y manifiestos fijados no se modificaron.

**Código para leer en el IDE:** [índice local de decompilaciones](../local/decompilados-ghidra/LEEME.md).
Incluye 15 funciones consultadas por MCP, en archivos `.c` con el texto literal
de Ghidra, una lectura agrupada por muestra y las respuestas JSON. Es material
local excluido de Git; el enlace solo funciona donde existe esa exportación.

## 1. Qué significa «capa» en este análisis

Una capa es una unidad que distinguimos para estudiar cómo se contiene,
prepara o utiliza otro componente. No todas las capas son archivos ejecutables,
ni todas se ejecutan en un orden único. Un ZIP es un contenedor de datos;
una DLL puede contener otro PE; un mismo ejecutable puede realizar varias tareas.

Usaremos letras didácticas, no nombres originales del malware ni fases NIST:

| Capa | Objeto | Responsabilidad observada | Qué sale o qué se entrega |
|---|---|---|---|
| A | `24d004…`, PE32 x86 | Decisión del dominio, servicio, recurso R/1831 y rutina de conexión 445 | Bytes de R/1831, idénticos a ed01 |
| B | `ed01…`, PE32 x86 | Extraer XIA/2058, preparar entorno y procesar t.wnry | Miembros del ZIP; posible transferencia a una dirección resuelta con TaskStart |
| C1 | `u.wnry`, miembro PE del ZIP | Entre otras funciones, bloque que usa la cadena de sabotaje de recuperación | Solicitudes de creación/ejecución de procesos |
| C2 | `t.wnry`, miembro de datos | Contenedor cuya lectura y validación inicia código de B | Búfer procesado; reconstrucción completa pendiente |
| C3 | `taskdl.exe` / `taskse.exe` | Auxiliares importados | Funciones detalladas pendientes de esta revisión |
| D | `ec1383…`, DLL x64 | Extraer W/101 y solicitar creación de un proceso | PE delimitado de hash 93db4b26… |

```text
CONTENCIÓN COMPROBADA (no cronología de ejecución)

A: 24d004…
   └── R/1831 = B: ed01…
                  └── XIA/2058 = ZIP
                                 ├── C1: u.wnry
                                 ├── C2: t.wnry
                                 └── C3: taskdl.exe / taskse.exe y otros

D: ec1383…
   └── W/101 = longitud de 4 bytes + PE delimitado + bytes posteriores
                                   └── hash 93db4b26…
```

**No conectar D → A como identidad de archivos:** sus hashes son distintos.
**No dibujar C1 → C2 como orden probado:** compartir ZIP no establece quién se
ejecuta antes. La procedencia desde honeypot y el itinerario en una red NHS
requieren fuentes independientes.

## 2. Cómo usar Decompiler y Listing juntos

Abre el programa correcto dentro de Ghidra. En Listing pulsa **G** para ir a
una dirección; activa **Window → Decompiler**. Seleccionar una expresión o
instrucción ayuda a localizar su correspondencia, aunque no siempre será una
relación de una línea a una instrucción.

| Vista | Pregunta que responde | Limitación |
|---|---|---|
| Bytes | ¿Qué está almacenado? | Una secuencia puede ser datos y no instrucciones |
| Listing / desensamblado | ¿Qué operaciones representan esas instrucciones? | Depende de arquitectura y límites correctos; no es una traza de ejecución |
| Decompiler / decompilado | ¿Cómo se puede expresar el flujo en C? | Tipos, parámetros y límites pueden estar mal inferidos |
| Referencias | ¿Qué instrucciones apuntan a este dato o función? | Pueden faltar llamadas indirectas; referencia no equivale a ejecución |
| Artefactos del sistema | ¿Qué ocurrió efectivamente en un equipo? | Aquí no disponemos de disco, RAM o logs adquiridos de un host NHS |

No hay que memorizar todo ensamblador. Empieza por estas operaciones, usando
la sintaxis destino, origen que muestra este proyecto:

| Instrucción | Lectura práctica |
|---|---|
| `MOV ESI,EAX` | Copia un valor a otro registro |
| `MOV ESI,[RDI]` | Lee el valor almacenado en memoria en esa dirección |
| `LEA RDX,[RDI+4]` | Calcula una dirección; no lee los bytes del contenido |
| `PUSH valor` | Coloca un valor en la pila; comprobar si es argumento o registro preservado |
| `CALL dirección` | Llama a una dirección directa |
| `CALL [dirección]` | Obtiene el destino desde memoria, por ejemplo una entrada de importación |
| `CALL EAX` | Llama a la dirección contenida en el registro |
| `TEST EAX,EAX` | Permite comprobar si el valor es cero |
| `CMP a,b` | Compara y establece indicadores |
| `JZ` / `JNZ` | Salta según el indicador de cero de la operación relevante anterior |
| `RET` | Retorna al llamador; no significa necesariamente terminar todo el proceso |

En las llamadas Win32 `__stdcall` examinadas, los argumentos se preparan en
pila de derecha a izquierda. No generalizarlo a todas las funciones: también
hay `__cdecl` y métodos `__thiscall` en estas muestras.
[Microsoft, __stdcall](https://learn.microsoft.com/en-us/cpp/cpp/stdcall?view=msvc-170).

En las llamadas Windows x64 de D, los primeros cuatro argumentos enteros o
punteros se pasan en RCX, RDX, R8 y R9; los siguientes, en pila. Por eso D
no se lee buscando exactamente la misma serie de PUSH que A.
[Microsoft, convención x64](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170).

**Método en cada capa:** identificar entrada → seguir condición → localizar
operación → comprobar qué dato sale → registrar prueba y límite.

## 3. Capa A: decisión, servicio y depósito de la siguiente capa

### A.1. Decisión en 00408140

Entrada: URL embebida y resultado de una API. Salida: una rama que llama a
`00408090`, o retorno sin esa llamada. El siguiente C es un resumen, no la
decompilación íntegra:

```c
handle = InternetOpenUrlA(...);
if (handle == NULL) {
    Preparar_Servicio_Y_Carga();
}
```

| Listing de 24d004 | Equivalencia que debes explicar |
|---|---|
| `00408194 CALL [0040a138]` | Solicita abrir la URL mediante la API importada |
| `0040819a MOV EDI,EAX` | Guarda el valor retornado |
| `004081a3 TEST EDI,EDI` | Comprueba si ese valor es cero |
| `004081a5 JNZ 004081bc` | El no cero evita la llamada posterior |
| `004081ad CALL 00408090` | Camino alcanzable cuando el resultado es cero |

La API devuelve un handle válido o NULL, no un código HTTP directo. El camino
examinado no consulta explícitamente HTTP 200.
[Microsoft, InternetOpenUrlA](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetopenurla).

**Conclusión oral:** «La muestra condiciona una rama a un resultado de WinINet.
Reconstruimos esa lógica; no medimos una conexión desde un hospital».

### A.2. Organización en 00408090 y servicio en 00407c40

`00408090` consulta el número de argumentos. En la rama de menos de dos,
`00407f20` llama a creación del servicio y extracción del recurso. La otra
rama usa el gestor de servicios; no reducir todo el programa a una lista lineal.

En `00407c40`, el Decompiler ayuda a identificar `OpenSCManagerA`,
`CreateServiceA`, el nombre `mssecsvc2.0` y `StartServiceA`. En Listing comprueba
la condición del handle que controla el inicio. El inicio automático solicitado
es una configuración, no evidencia de reinicio ni persistencia efectivamente lograda.

**Artefactos a buscar si existiera una adquisición:** configuración del servicio,
binario señalado por su ruta y registros del sistema con auditoría disponible.
No se presentan esos artefactos como adquiridos aquí.

### A.3. Recurso R/1831 en 00407ce0: cómo comprobar el salto a B

La decompilación muestra una búsqueda equivalente a:

```c
// Equivalencia explicativa; nombres y tipos simplificados.
recurso = FindResourceA(NULL, identificador_1831, "R");
```

Comprueba los argumentos en Listing:

```text
00407d69 PUSH 0x43137c     ; dirección del texto "R"
00407d6e PUSH 0x727        ; 1831 decimal
00407d73 PUSH EBX         ; cero en este camino
00407d74 CALL [0040a05c]   ; FindResourceA
```

Aunque el prototipo presenta un puntero, el identificador de recurso puede
representarse con un entero. `0x727` no debe interpretarse aquí como dirección
de código a la que saltar. Sigue LoadResource, LockResource y SizeofResource:
son pasos diferentes de la escritura a disco.

**Mejora de esta revisión:** el Decompiler no recuperaba todos los argumentos
de `sprintf`. El Listing y los bytes permiten reconstruir el formato:

| Dirección del dato | Cadena comprobada |
|---|---|
| `00431358` | `C:\%s\%s` |
| `00431364` | `WINDOWS` |
| `0043136c` | `tasksche.exe` |

`00407dea`, `00407df2` y `00407dfb` preparan esas referencias para la llamada
de `00407e01`. La composición da **C:\WINDOWS\tasksche.exe** en este camino.
Esto es más sólido que inventar los argumentos que no muestra el Decompiler.

Para verificar qué bytes se escribirían:

```text
00407d9d MOV [ESP+0x10],EAX  ; conserva el puntero obtenido
...
00407daf MOV EBP,EAX         ; conserva el tamaño del recurso
...
00407e54 MOV EAX,[ESP+0x10]  ; recupera el puntero
00407e58 LEA EDX,[ESP+0x10]  ; dirección para recibir bytes escritos
00407e5c PUSH EBX            ; NULL
00407e5d PUSH EDX            ; parámetro de salida
00407e5e PUSH EBP            ; longitud
00407e5f PUSH EAX            ; datos
00407e60 PUSH ESI            ; handle del archivo
00407e61 CALL [00431460]     ; WriteFile resuelta antes con GetProcAddress
```

El mismo espacio local se reutiliza: se carga el puntero en EAX antes de pasar
su antigua ubicación como salida de bytes escritos. Esto explica parte de la
confusión del pseudocódigo automático. Hay que seguir también los cambios de
ESP; un desplazamiento de pila aislado no identifica siempre la misma variable.

**Prueba independiente:** los 3.514.368 bytes extraídos de R/1831 tienen el hash
completo de ed01 y se cotejaron byte a byte. Eso acredita **contención A → B**.
La presencia de WriteFile acredita una operación prevista por el código, no
un archivo creado en un hospital.

**Evidencia local:** `A-recurso-asm.json`, `A-rutas.json` y el manifiesto de
extracción. **Ejercicio:** explicar por qué la igualdad del recurso con ed01
es más informativa que encontrar simplemente el texto «tasksche.exe».

## 4. Capa B: abrir el paquete y preparar componentes

### B.1. XIA/2058 en 00401dab

Entrada: recurso interno. Salida esperada: miembros del paquete tratados por
las rutinas de extracción. El ZIP se extrajo estáticamente; contiene 36 miembros.

La decompilación muestra la secuencia FindResource → LoadResource → LockResource
→ SizeofResource → rutina que recibe datos, tamaño y otro argumento del llamador.

```text
00401db6 PUSH 0x40f43c        ; "XIA"
00401dbb PUSH 0x80a           ; 2058
00401dc0 PUSH [EBP+0x8]       ; módulo pasado como argumento
00401dc3 CALL [00408100]      ; FindResourceA
00401dc9 MOV ESI,EAX
00401dcb TEST ESI,ESI
00401dcd JZ 00401e07          ; camino de fallo
```

Más adelante, `00401df9 CALL 004075ad` entrega los datos a la rutina de apertura
del paquete. El bucle de la decompilación recorre entradas y trata especialmente
`c.wnry` cuando ese archivo ya existe. No todas las entradas se procesan bajo
una condición idéntica.

**Distinción clave:** el recurso PE R/1831 contiene un ejecutable; el recurso
XIA/2058 contiene un ZIP. Buscar MZ o llamar «cifrador» a cualquier recurso no
reemplaza identificar su formato.

### B.2. Preparación en 00401fe7

`004020d0` llama a la extracción. Más adelante aparecen referencias a cadenas
de atributos y permisos; ambas pasan por `00401064`:

```text
004020e8 PUSH 0x40f4fc        ; cadena con icacls
004020ed CALL 00401064        ; rutina de creación de proceso
```

Ahora se comprobó esa rutina: usa `CreateProcessA` y comprueba su retorno.
La espera está condicionada a un parámetro distinto de cero; los llamadores
examinados pasan cero. Por tanto, el orden de llamadas **no demuestra que una
orden externa terminara antes de comenzar la siguiente etapa**. El llamador
tampoco convierte un texto de comando en evidencia de permisos efectivamente cambiados.

**Conclusión oral:** «B prepara varios componentes. Hemos seguido la referencia
de la cadena hasta la API; el éxito y la finalización son hechos distintos».

**Evidencia local:** `B-paquete-asm.json`, `B-transicion-asm.json`,
`B-lectura-t.json` y manifiesto del ZIP.

## 5. Capa C2: t.wnry y la frontera de lo que ya sabemos

Estudiamos esta rama antes de C1 para seguir B; no afirmamos ese orden de ejecución.
El archivo actual mide **65.816 bytes** y empieza por:

```text
Offset 0x00: 57 41 4e 41 43 52 59 21    ASCII: WANACRY!
Offset 0x08: 00 01 00 00                entero little-endian: 256
```

**Es una cabecera de contenedor, no una cabecera PE MZ en el inicio.** No importarlo
como una DLL en claro suponiendo que las instrucciones ya están disponibles.

### C2.1. Qué hace B con este archivo

En **ed01**, `004014a6` recibe el nombre de archivo; la llamada desde `0040212d`
le pasa la referencia a `t.wnry`. Su decompilado muestra apertura, operaciones
de lectura indirectas, comparación de ocho bytes con `WANACRY!`, comprobación
del siguiente campo frente a `0x100`, reserva de memoria y llamadas de procesamiento.

En Listing:

```text
00401564 PUSH 0x8              ; longitud de comparación
00401566 PUSH 0x40eb7c         ; referencia a WANACRY!
...
00401572 CALL 004076ee         ; memcmp según el decompilado/símbolo
0040157a TEST EAX,EAX
0040157c JNZ 004016d0          ; si no coinciden, sale por este camino
...
0040159f MOV EAX,0x100
004015a4 CMP [EBP+...],EAX     ; comprueba el campo leído
004015aa JNZ 004016d0
```

Aquí **cero en memcmp significa igualdad**, no fallo de conexión. Es un ejemplo
de por qué no existe una regla universal «cero = error» para todas las funciones.
Los bytes del archivo y las comparaciones del código se corroboran entre sí.
No basta ver un bloque de 256 bytes para afirmar su algoritmo o papel criptográfico.

### C2.2. Transición hacia una dirección de código

En el llamador `00401fe7`, una representación abreviada de lo observado es:

```c
// Resumen del flujo: no es implementación ni decompilación íntegra.
buffer = FUN_004014a6(..., "t.wnry", &longitud);
if (buffer != NULL) {
    resultado = FUN_004021bd(buffer, longitud);
    if (resultado != 0) {
        destino = FUN_00402924(resultado, "TaskStart");
        if (destino != NULL) {
            destino(0, 0);
        }
    }
}
```

Comprueba esos hitos en Listing:

| Dirección en ed01 | Instrucción / dato | Qué demuestra |
|---|---|---|
| `00402125` | `PUSH 0x40f4f4` | Referencia al nombre t.wnry |
| `0040212d` | `CALL 004014a6` | Entrada a la rutina de lectura/procesamiento |
| `0040213a` | `CALL 004021bd` | Siguiente transformación, pendiente de caracterizar completamente |
| `00402145` | `PUSH 0x40f4e8` | Referencia a TaskStart |
| `0040214b` | `CALL 00402924` | Obtención del valor que se usa como destino |
| `00402154` | `JZ 0040215a` | Evita la llamada cuando el resultado es cero |
| `00402158` | `CALL EAX` | Transferencia indirecta al destino obtenido |

La última llamada no contiene una dirección fija de la función final en el
archivo actual. No renombrar `00402158` como «función de cifrado»: es el sitio
de llamada, no la implementación completa de la función invocada.

**Alcance nuevo:** comprobamos formato inicial, condiciones y camino hacia una
llamada indirecta. **Pendiente:** semántica completa de las rutinas de transformación,
contenido reconstruido de la carga y recorrido criptográfico. No se extrajo una
DLL descifrada ni se ejecutó TaskStart en esta revisión.

**Evidencia:** `B-lectura-t.json`, `B-formato-asm.json`, `B-transicion-asm.json`,
`C-cabecera-t.json`. Esta última registra hash, tamaño y bytes iniciales del archivo.

## 6. Capa C1: u.wnry y solicitudes contra la recuperación

La cadena de interés comienza en `00420fd8`. El bloque que la referencia no
tiene una función contenedora recuperada correctamente por Ghidra; el Decompiler
puede fallar en `004066fe` aunque Listing muestre código. Esta limitación está
registrada, no debe ocultarse creando una función sin comprobar sus límites.

| Listing de u.wnry | Lectura |
|---|---|
| `004066fe MOV ESI,0x420fd8` | Carga la dirección de la cadena |
| `0040670c MOVSD.REP` | Copia sus datos según el contador y punteros preparados |
| `0040672f CALL 00401bb0` | Consulta un SID de Administradores mediante el token |
| `00406736 JNZ 00406750` | Selecciona la rama según el resultado |
| `00406746 CALL 00401b50` | Rutina que utiliza ShellExecuteExA con runas |
| `0040677c CALL 00401a90` | Otra rama: rutina que utiliza CreateProcessA |

En el Decompiler abre **las funciones auxiliares** `00401bb0`, `00401b50` y
`00401a90`, que sí se recuperan. Así se puede contrastar un bloque en Listing
con el pseudocódigo de sus destinos, sin fingir que el bloque entero decompila.

La cadena contiene operaciones contra copias sombra, catálogo y opciones de
recuperación. Sus referencias y los destinos sustentan uso potencial. Un intento
de `runas` no demuestra elevación concedida. Un proceso creado no demuestra
órdenes terminadas ni objetos efectivamente borrados.

**Qué faltaría para demostrar impacto en un host:** registros de ejecución,
contexto de privilegios y estado de recuperación antes/después, con tiempos
correlacionados. No hay evidencia de todos esos hechos en un equipo NHS aquí.

**Frase para exposición:** «La cadena sola sería un indicio. La referencia y
las rutinas de ejecución aumentan el sustento de la capacidad; el efecto real
requiere otras evidencias».

## 7. Capa D: extracción alternativa de W/101 en x64

### Función que conecta las operaciones: PlayGame

Comprobación adicional por MCP: `PlayGame` es una exportación en `1800011a4`
(ordinal 1). Construye `C:\WINDOWS\mssecsvc.exe` en la variable global
`DAT_18000d2a0`, llama a la extracción en `1800011c9` y a la creación del
proceso en `1800011ce`. El Listing confirma ambas llamadas consecutivas,
sin una comparación del resultado de la extracción entre ellas.

Esto acredita el orden previsto dentro de esta función, no que se haya
invocado en un host ni quién la invocó. Una función exportada no se ejecuta
necesariamente solo por cargar la DLL. Tampoco convierte el PE extraído
en idéntico a 24d004: conserva su hash distinto, 93db4b26….

Código y respuestas de esta comprobación: `local/ec1383-detalle/`, fuera de Git.
El nombre `mssecsvc.exe` se forma en tiempo de ejecución; no confundirlo
con el nombre de servicio `mssecsvc2.0` observado en la otra muestra.

Este archivo es DLL x64, pese a su extensión .exe. En `180001014`, el Decompiler
reconstruye una búsqueda de W/101 seguida de operaciones sobre el recurso.

```text
180001023 MOV RCX,[18000d3a8]  ; argumento 1: módulo
18000102a LEA R8,[1800092b0]   ; argumento 3: "W"
180001031 MOV EDX,0x65        ; argumento 2: 101
180001036 CALL [180009030]    ; FindResourceA
```

El orden temporal de estas instrucciones no cambia qué registro representa
cada parámetro. La convención de llamada determina la correspondencia.

Tras obtener el puntero al recurso, el decompilado muestra:

```c
longitud = *puntero_DWORD;
WriteFile(archivo, puntero_DWORD + 1, longitud, ...);
```

Los nombres son explicativos. Contrástalo con instrucciones reales:

```text
18000108b MOV ESI,[RDI]       ; lee los primeros 4 bytes como longitud
...
1800010c4 LEA RDX,[RDI+4]     ; argumento 2: datos desde recurso+4
1800010c8 LEA R9,[RSP+0x50]   ; argumento 4: salida de bytes escritos
1800010cd MOV R8D,ESI         ; argumento 3: longitud
1800010d0 MOV RCX,RAX         ; argumento 1: handle
1800010d3 CALL [180009008]     ; WriteFile
```

`DWORD * + 1` en C equivale a **+4 bytes** en esta dirección. Esta pareja de
vistas demuestra por qué hay que excluir los primeros cuatro bytes del PE.
El recurso completo mide 5.242.880 bytes, pero el contenido declarado mide
3.756.032; no cortar simplemente de MZ hasta el final del recurso.

**Ejemplo de control de errores:** `1800010b8` compara el handle con -1;
si falla, salta a `1800010e2`, que carga 1 en EAX. La misma salida positiva
se alcanza tras la escritura. No interpretar ese 1 como prueba de escritura
correcta: la rutina tampoco comprueba aquí el resultado de WriteFile.

En `1800010f8` hay una rutina que solicita crear un proceso con la ruta global.
No representa por sí misma una captura de red, inyección en otro proceso o
explotación exitosa. El PE extraído tiene hash **93db4b26…**, distinto de A.

**Evidencia:** `D-recurso-asm.json`, decompilaciones anteriores y manifiesto de
extracción. **Ejercicio:** explicar por qué aquí aparece RDX+4 y en A se pasa
directamente el puntero del recurso: los formatos de los recursos son distintos.

## 8. Del código a la explicación del caso NHS

La presentación debe mantener tres columnas mentales:

| Observación local | Interpretación técnica | Comprobación histórica o de host necesaria |
|---|---|---|
| Handle nulo conduce a otra rutina | Condición del flujo | Respuesta real, DNS/proxy/firewall y proceso del host |
| Servicio solicitado | Posible instalación de servicio | Configuración y registros del sistema adquirido |
| Recurso igual a ed01 | Contención entre archivos | Procedencia que vincule la muestra con el host |
| Referencias a puerto 445 | Operaciones orientadas a ese puerto | Tráfico, versión SMB, parche y evidencia de explotación |
| Cadena contra recuperación referenciada | Capacidad de solicitar esas operaciones | Privilegios, resultados y estado de copias |
| Contenedor t.wnry y CALL EAX | Camino condicionado de transferencia | Carga reconstruida y análisis de su implementación |

Para NIST: **RS.AN-03** organiza el análisis de lo ocurrido; **RS.AN-06**, el
registro de actuaciones; **RS.AN-07**, datos/metadatos con integridad y procedencia.
Los riesgos de red y de recuperación se relacionan con **PR.IR-01** y **PR.DS-11**.
Los resultados de Recover requieren pruebas de recuperación; una función del
malware no demuestra que el plan se ejecutó.

El método de recopilación, examen, análisis e informe proviene de SP 800-86.
CSF 2.0 se aplica retrospectivamente al caso de 2017. Véanse el
[informe](informe-forense.md), la [matriz](matriz-nist.csv) y la
[guía NIST](guia-comprobacion-nist.md). No se evalúa cumplimiento de una
organización solo por decompilar estas muestras.

## 9. Guion práctico para explicar las capas en clase

1. **Identificar:** mostrar el programa y hash; explicar que se analiza estáticamente.
2. **Mostrar el mapa:** distinguir contención de ejecución, y la rama separada D.
3. **Explicar una condición:** kill switch en Decompiler y TEST/JNZ en Listing.
4. **Demostrar una relación:** R/1831, WriteFile y coincidencia exacta con ed01.
5. **Mostrar el cambio de formato:** PE → recurso ZIP → miembros PE y contenedor.
6. **Marcar la frontera:** cabecera t.wnry, comprobaciones y CALL EAX; criptografía pendiente.
7. **Seguir un indicio:** cadena de u.wnry → referencias → rutinas; efecto no observado.
8. **Comparar arquitectura:** argumentos x86 frente a registros x64 de W/101.
9. **Cerrar el hallazgo:** qué se observó, dónde, cómo se comprobó y qué falta.

En cada parada conserva una captura o respuesta con programa, dirección,
instrucciones y comentario. Los registros reales van en `local/`, fuera de Git.
No inventar timestamps de infección a partir de la fecha de la consulta.

Preguntas de defensa que debes poder responder:

- **¿Cómo sabes que A contiene B?** Por extracción delimitada, tamaño, hash y
  cotejo de bytes, además de la secuencia de APIs.
- **¿Por qué consultar ambas vistas?** La decompilación facilita entender; el
  Listing permite comprobar argumentos, condiciones y llamadas cuando los tipos fallan.
- **¿Cuál es la clave de descifrado?** No se presenta una clave de víctimas;
  la contraseña del ZIP y el procesamiento de t.wnry son asuntos distintos.
- **¿Todo lo que ves se ejecutó?** No. Mostramos caminos posibles; no una traza.
- **¿Qué pasó en el NHS?** Responder con fuentes históricas del informe, y separar
  esas afirmaciones de las observaciones sobre muestras locales.

Quedan pendientes los componentes y caminos no revisados, la reconstrucción
criptográfica completa y la procedencia anterior de las muestras. No se ejecutó
malware ni se modificaron el laboratorio, sus redes o comparticiones.
