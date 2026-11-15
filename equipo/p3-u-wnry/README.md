# P3 — u.wnry: referencias, privilegios y recuperación

[Equipo](../README.md) · [Código de tus tres funciones](codigo.md) · [Cómo estudiar](../COMO-ESTUDIAR.md)

Tu pregunta central: **¿cómo se relaciona una cadena contra mecanismos de
recuperación con las rutinas que podrían usarla, y qué falta para demostrar efecto?**
Coordinarás los límites de la simulación benigna y la recuperación. P4 revisará tu trabajo.

## Qué estudiar y en qué orden

| Paso | Dirección | Busca | Qué debes explicar |
|---|---|---|---|
| 1 | 00420fd8, dato | Cadena referenciada | Dato estático frente a orden ejecutada |
| 2 | 004066fe, 0040670c, Listing | Referencia y copia | Cómo pasa el dato al bloque de código |
| 3 | [00401bb0](codigo.md#f-00401bb0) | SID y CheckTokenMembership | Éxito de consulta frente a pertenencia habilitada |
| 4 | [00401b50](codigo.md#f-00401b50) | ShellExecuteExA y `runas` | Solicitud frente a elevación concedida |
| 5 | [00401a90](codigo.md#f-00401a90) | CreateProcessA, espera y código de salida | Proceso creado frente a acción completada |

Las tres auxiliares sí tienen decompilación seleccionada. El bloque principal
que referencia la cadena no tiene una función contenedora correctamente recuperada
en este proyecto. **No existe aquí una decompilación completa de ese bloque.**
Su estudio se hace con Listing y referencias; un fallo del Decompiler no indica
ausencia de instrucciones ni autoriza a inventar una función.

## Contraste con Listing

Extracto didáctico de la [guía de capas](../../docs/guia-capas-decompilado-desensamblado.md):

```text
004066fe MOV ESI,0x420fd8  ; dirección de la cadena
0040670c MOVSD.REP        ; copia de datos
0040672f CALL 00401bb0    ; consulta de SID/token
00406736 JNZ 00406750     ; selección de ruta
00406746 CALL 00401b50    ; auxiliar con ShellExecuteExA
0040677c CALL 00401a90    ; auxiliar con CreateProcessA
```

Lee cada destino en `codigo.md`. En `00401bb0`, `BVar1` es el retorno de la API,
mientras `local_10` recibe el resultado consultado. La documentación de
[CheckTokenMembership](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-checktokenmembership)
separa ambos valores. En este auxiliar un fallo acaba también en 0: no todos
los resultados negativos permiten afirmar que la consulta se realizó correctamente.

La cadena de interés se describe por grupos de operaciones en la guía: copias
sombra, catálogo y opciones de recuperación. Se analiza su referencia; no se
convierte en una instrucción para ejecutar en el laboratorio. Usa Ghidra y las
transcripciones; Sysinternals y memoria solo corresponden a prácticas posteriores.

## Historia, NIST y simulación

Lee [NHS §2.14](../../fuentes/NHS-lessons-learned-2018.pdf) y el
[informe](../../docs/informe-forense.md). No extrapoles una descripción de
recuperación de ciertas organizaciones a todos los hospitales.
Trabaja N-07 (PR.DS-11), N-16 (RC.RP-01), N-17 (RC.RP-03) y N-18 (RC.RP-05)
de la [matriz](../../docs/matriz-nist.csv).

Puedes realizar ahora una simulación de mesa, sin ejecutar instrucciones del malware:

| Dato ficticio entregado por el ejercicio | Qué permite afirmar | Qué falta |
|---|---|---|
| Solo se encontró una cadena | Capacidad sugerida | Referencias y contexto |
| Una solicitud de proceso devolvió éxito | Creación informada por la API | Finalización y efecto |
| Hay copia de prueba legible | Lectura de esa copia | Criterio de integridad y aptitud |
| Se restauró un archivo ficticio | Recuperación de ese archivo | Prueba funcional del servicio |

Etiqueta el resultado como S; no es una observación local de WannaCry ni prueba
de recuperación hospitalaria. Las prácticas dentro de Windows siguen pendientes.

## Entrega y revisión

- Tabla cadena → referencia → auxiliar → efecto posible → evidencia faltante.
- Dos fichas: consulta de token y solicitud/espera de proceso.
- Criterios para verificar un respaldo y una restauración benigna futura.
- P4 debe señalar dónde termina la observación estática y empieza la inferencia.

Preguntas: ¿un `runas` implica privilegios concedidos? ¿El retorno 1 de un
auxiliar prueba borrado de copias? ¿Qué demuestra un hash de un respaldo?
¿Puedes afirmar que el bloque principal fue decompilado completamente?
